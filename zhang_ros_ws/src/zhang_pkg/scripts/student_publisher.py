#!/usr/bin/env python3
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from zhang_pkg.msg import StudentInfo


class StudentPublisher(Node):
    def __init__(self):
        super().__init__("student_publisher")
        self.publisher = self.create_publisher(StudentInfo, "student_info", 10)
        self.timer = self.create_timer(1.0, self.publish_student_info)
        self.count = 0

    def publish_student_info(self):
        self.count += 1
        msg = StudentInfo()
        msg.name = "张嘉玮"
        msg.student_id = 202342971
        msg.major = "Robotics"
        msg.score = 95.0
        msg.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(msg)
        self.get_logger().info(f"publish #{self.count}: {msg}")


def main():
    rclpy.init()
    node = StudentPublisher()
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
