#!/usr/bin/env python3
import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from zhang_pkg.action import CountUntil


class CountUntilActionClient(Node):
    def __init__(self):
        super().__init__("count_until_action_client")
        self.client = ActionClient(self, CountUntil, "count_until")

    def send_goal(self, target_number, period):
        goal = CountUntil.Goal()
        goal.target_number = target_number
        goal.period = period

        self.client.wait_for_server()
        self.get_logger().info(
            f"send goal: target={target_number}, period={period:.2f}s"
        )
        return self.client.send_goal_async(goal, feedback_callback=self.feedback_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f"feedback: current={feedback.current_number}, "
            f"progress={feedback.progress:.0%}"
        )


def main():
    rclpy.init()
    node = CountUntilActionClient()
    target = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    period = float(sys.argv[2]) if len(sys.argv) > 2 else 0.2

    goal_future = node.send_goal(target, period)
    rclpy.spin_until_future_complete(node, goal_future)
    goal_handle = goal_future.result()
    if not goal_handle.accepted:
        node.get_logger().error("goal rejected")
        node.destroy_node()
        rclpy.shutdown()
        return

    result_future = goal_handle.get_result_async()
    rclpy.spin_until_future_complete(node, result_future)
    result = result_future.result().result
    node.get_logger().info(
        f"result: success={result.success}, final_number={result.final_number}"
    )
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
