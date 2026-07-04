#!/usr/bin/env python3
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from zhang_pkg.msg import StudentInfo


class StudentSubscriber(Node):
    def __init__(self):
        super().__init__("student_subscriber")
        self.subscription = self.create_subscription(
            StudentInfo, "student_info", self.listener_callback, 10
        )

    def listener_callback(self, msg):
        self.get_logger().info(
            f"receive: name={msg.name}, id={msg.student_id}, "
            f"major={msg.major}, score={msg.score:.1f}"
        )


def main():
    rclpy.init()
    node = StudentSubscriber()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
