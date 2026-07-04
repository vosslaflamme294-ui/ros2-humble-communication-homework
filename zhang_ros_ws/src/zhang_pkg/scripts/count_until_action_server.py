#!/usr/bin/env python3
import time

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from zhang_pkg.action import CountUntil


class CountUntilActionServer(Node):
    def __init__(self):
        super().__init__("count_until_action_server")
        self.action_server = ActionServer(
            self,
            CountUntil,
            "count_until",
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
        )
        self.get_logger().info("action /count_until is ready")

    def goal_callback(self, goal_request):
        self.get_logger().info(
            f"receive goal: target={goal_request.target_number}, "
            f"period={goal_request.period:.2f}s"
        )
        if goal_request.target_number <= 0:
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info("cancel request accepted")
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        target = goal_handle.request.target_number
        period = max(goal_handle.request.period, 0.1)
        feedback = CountUntil.Feedback()

        for number in range(1, target + 1):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result = CountUntil.Result()
                result.success = False
                result.final_number = number - 1
                return result

            feedback.current_number = number
            feedback.progress = number / float(target)
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(
                f"feedback: current={number}, progress={feedback.progress:.0%}"
            )
            time.sleep(period)

        goal_handle.succeed()
        result = CountUntil.Result()
        result.success = True
        result.final_number = target
        return result


def main():
    rclpy.init()
    node = CountUntilActionServer()
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
