from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package="zhang_pkg",
            executable="student_publisher.py",
            name="student_publisher",
            output="screen",
        ),
        Node(
            package="zhang_pkg",
            executable="student_subscriber.py",
            name="student_subscriber",
            output="screen",
        ),
        Node(
            package="zhang_pkg",
            executable="add_two_ints_server.py",
            name="add_two_ints_server",
            output="screen",
        ),
    ])
