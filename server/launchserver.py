from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="socket_server",
            namespace="controllsocketserver",
            executable="car_control_server",
            name="nw_chassis_control_node"
        )
    ])
