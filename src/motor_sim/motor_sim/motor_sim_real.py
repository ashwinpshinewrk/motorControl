import rclpy # type: ignore
from rclpy.node import Node # type: ignore

from std_msgs.msg import String, Float32MultiArray # type: ignore

PUBLISH_TIME_PERIOD = 0.02 # 50Hz

def clamp(v,min_v,max_v) -> float:
    return max(min_v,min(max_v,v))

"""Used so that the sudden surge in the rpm wont burn the motor."""
class LagFilter():
    def __init__(self):
        self.TAU = 1 # reaches to 63 percentage that sec, 95 in thrice that.
        self.alpha = PUBLISH_TIME_PERIOD  / self.TAU
        self.max_delta_rpm = 10
        self.max_step = self.max_delta_rpm * PUBLISH_TIME_PERIOD
    def do(self,current, target):
        step = self.alpha * (target - current)
        step = clamp(step, -self.max_delta_rpm,self.max_delta_rpm)
        return (current + step)


class MotorCompute(Node):
    def __init__(self):
        super().__init__('motor_sim_real')
        self.subscription = self.create_subscription(Float32MultiArray,'/motor_sim/motor_target_rpm' , self.listener_callback, 10)
        self.publisher = self.create_publisher(String, '/motor_sim/telemetry',10)
        self.timer = self.create_timer(PUBLISH_TIME_PERIOD,self.timer_callback)

        self.l_rpm_target = 0.0
        self.r_rpm_target = 0.0
        self.l_rpm_current =0.0
        self.r_rpm_current =0.0
        self.lag_filter = LagFilter()

    def listener_callback(self, msg):
        [self.l_rpm_target,self.r_rpm_target] = msg.data

    def timer_callback(self):
        self.compute_next_rpm()

        msg = String()
        msg.data = f"Left RPM : {self.l_rpm_current}, Right RPM : {self.r_rpm_current}"
        self.publisher.publish(msg)

    def compute_next_rpm(self):
        self.l_rpm_current = self.lag_filter.do(self.l_rpm_current,self.l_rpm_target)
        self.r_rpm_current = self.lag_filter.do(self.r_rpm_current,self.r_rpm_target)


def main(args=None):
    rclpy.init(args=args)

    motor_compute = MotorCompute()

    rclpy.spin(motor_compute)
    motor_compute.destroy_node()
    rclpy.shutdown()

main()