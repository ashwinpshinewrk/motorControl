from launch import LaunchDescription # type: ignore
from launch_ros.actions import Node # type: ignore

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="motor_sim",
            executable = "motor_calc",
            name = "cmd_listener",
            output="screen"
        ),
        Node(
                    package="motor_sim",
                    executable = "motor_real_world",
                    name = "motor_sim_real",
                    output="screen"
                )
    ])