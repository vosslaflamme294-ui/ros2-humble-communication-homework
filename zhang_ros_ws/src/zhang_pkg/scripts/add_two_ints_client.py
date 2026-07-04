#!/usr/bin/env python3
import sys

import rclpy
from rclpy.node import Node

from zhang_pkg.srv import AddTwoInts


class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__("add_two_ints_client")
        self.client = self.create_client(AddTwoInts, "add_two_ints")

    def send_request(self, a, b):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for /add_two_ints service...")
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        return self.client.call_async(request)


def main():
    rclpy.init()
    node = AddTwoIntsClient()
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    b = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    future = node.send_request(a, b)
    rclpy.spin_until_future_complete(node, future)
    response = future.result()
    node.get_logger().info(f"{a} + {b} = {response.sum}")
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
