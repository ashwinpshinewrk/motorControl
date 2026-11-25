#!/usr/bin/env python3

import rclpy # type: ignore
from rclpy.node import Node # type: ignore
from geometry_msgs.msg import Twist # type: ignore
from std_msgs.msg import String, Float32MultiArray # type: ignore

WHEEL_RADIUS = 0.2 # metre
WHEEL_BASE_LENGTH = 1.0 # metre
MAX_MOTOR_RPM = 50.0
PUBLISH_TIME_PERIOD = 0.02 # 50Hz
def clamp(v,min_v,max_v) -> float:
    return max(min_v,min(max_v,v))

class CmdListener(Node):
    def __init__(self):
        super().__init__('cmd_listener')
        self.lisenter = self.create_subscription(Twist, 'cmd_vel', self.listener_callback,10)
        self.publisher = self.create_publisher(Float32MultiArray, '/motor_sim/motor_target_rpm', 10)

        self.publish_timer = self.create_timer(PUBLISH_TIME_PERIOD,self.timer_callback)
        self.left_rpm = 0
        self.right_rpm = 0

    def timer_callback(self):
        msg = Float32MultiArray()
        msg.data = [self.left_rpm,self.right_rpm]
        self.publisher.publish(msg)
    def listener_callback(self,msg : Twist):
        self.get_logger().info(f"Linear :  {msg.linear} , Angular : {msg.angular}")
        v_l, v_r = self.angular_velocity(msg)
        self.left_rpm = self.convert_velocity_to_rpm(v_l)
        self.right_rpm = self.convert_velocity_to_rpm(v_r)
        self.get_logger().info(f"Left rpm {self.left_rpm} , Right rpm : {self.right_rpm}")

    """IN RADIAN PER SEC"""
    def angular_velocity(self,msg) -> tuple[float, float]:
        linear_v = msg.linear.x # type: ignore
        angular_v = msg.angular.z # type: ignore

        # v_l = w * (R + ( l / 2)) w*r => v..
        v_l = (linear_v - ((angular_v * WHEEL_BASE_LENGTH) / 2.0)) / WHEEL_RADIUS
        v_r = (linear_v + ((angular_v * WHEEL_BASE_LENGTH) / 2.0)) / WHEEL_RADIUS

        return (v_l,v_r)
    def convert_velocity_to_rpm(self,v : float) -> float:
        # 60 / 2pi
        return clamp(v * (60 / (6.28)),-MAX_MOTOR_RPM,MAX_MOTOR_RPM)


def main(args=None):
    rclpy.init(args=args)

    cmd_listener = CmdListener()

    rclpy.spin(cmd_listener)

    cmd_listener.destroy_node()
    rclpy.shutdown()

main()