#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class TrajectoryPublisher(Node):

    def __init__(self):
        super().__init__('trajectory_publisher')
        self.publisher_ = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )

        self.timer = self.create_timer(2.0, self.send_trajectory)

    def send_trajectory(self):
        msg = JointTrajectory()

        msg.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]

        point = JointTrajectoryPoint()
        point.positions = [0.0, -1.57, 1.57, 0.0, 0.0, 0.0]
        point.time_from_start.sec = 3

        msg.points.append(point)

        self.publisher_.publish(msg)
        self.get_logger().info("Trajetória enviada!")

def main():
    rclpy.init()
    node = TrajectoryPublisher()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
