#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from px4_msgs.msg import VehicleOdometry

import numpy as np 
import math 
from builtin_interfaces.msg import Time


class PoseBridge(Node):
    def __init__(self):
        super().__init__('vins_pose_bridge')

        # Input odom topic from VINS (adjust if your estimator publishes different topic)
        self.declare_parameter('vins_odom_topic', '/vins_estimator/odometry')
        self.vins_odom_topic = self.get_parameter(
            'vins_odom_topic').get_parameter_value().string_value

        # Publisher: PX4 expects /fmu/in/vehicle_visual_odometry OR /fmu/in/vehicle_odometry
        self.pub = self.create_publisher(
            VehicleOdometry, '/fmu/in/vehicle_visual_odometry', 10)

        # Subscriber: VINS-Mono odometry
        self.sub = self.create_subscription(
            Odometry, self.vins_odom_topic, self.odom_cb, 10)

        self.get_logger().info(
            f'PoseBridge listening to {self.vins_odom_topic} '
            'and publishing to /fmu/in/vehicle_visual_odometry'
        )

    def odom_cb(self, msg: Odometry):
        v = VehicleOdometry()

        # PX4 timestamps are in microseconds
        v.timestamp = int(self.get_clock().now().nanoseconds // 1000)

        # Position
        v.x = float(msg.pose.pose.position.x)
        v.y = float(msg.pose.pose.position.y)
        v.z = float(msg.pose.pose.position.z)

        # Orientation quaternion [w, x, y, z]
        v.q = [
            float(msg.pose.pose.orientation.w),
            float(msg.pose.pose.orientation.x),
            float(msg.pose.pose.orientation.y),
            float(msg.pose.pose.orientation.z)
        ]

        # Linear velocity (if available)
        v.vx = float(msg.twist.twist.linear.x)
        v.vy = float(msg.twist.twist.linear.y)
        v.vz = float(msg.twist.twist.linear.z)

        # PX4 extra fields
        v.local_frame = 1     # 1 = LOCAL_FRAME_NED
        v.quality = 255       # max quality

        self.pub.publish(v)


def main(args=None):
    rclpy.init(args=args)
    node = PoseBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

