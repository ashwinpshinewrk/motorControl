import rclpy # type: ignore
from rclpy.node import Node # type: ignore

from std_msgs.msg import String, Float32MultiArray # type: ignore

class MotorCompute(Node):
    def __init__(self):
        super().__init__('motor_sim_real')
        self.subscription = self.create_subscription(Float32MultiArray,'' , self.listener_callback, 10)

        self.l_rpm_target = 0.0
        self.r_rpm_target = 0.0
    def listener_callback(self, msg):
        [self.l_rpm_target,self.r_rpm_target] = msg.data

def main(args=None):
    rclpy.init(args=args)

    motor_compute = MotorCompute()

    rclpy.spin(motor_compute)
    motor_compute.destroy_node()
    rclpy.shutdown()

main()