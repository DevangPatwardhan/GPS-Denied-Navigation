#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool, String
from px4_msgs.msg import VehicleOdometry
import math
import numpy as np

class DriftMonitor(Node):
    def __init__(self):
        super().__init__('vins_drift_monitor')
        self.declare_parameter('vins_odom_topic', '/vins_estimator/odometry')
        self.declare_parameter('px4_odom_topic', '/fmu/out/vehicle_odometry')
        self.declare_parameter('drift_threshold_m', 0.5)

        self.vins_topic = self.get_parameter('vins_odom_topic').get_parameter_value().string_value
        self.px4_topic = self.get_parameter('px4_odom_topic').get_parameter_value().string_value
        self.threshold = float(self.get_parameter('drift_threshold_m').get_parameter_value().double_value)

        self.vins_pose = None
        self.px4_pose = None

        self.alert_pub = self.create_publisher(String, '/vins_px4/drift_alert', 10)
        self.sub_vins = self.create_subscription(Odometry, self.vins_topic, self.vins_cb, 10)
        # px4 may publish px4_msgs VehicleOdometry; we try subscribe to nav_msgs/Odometry and px4_msgs
        try:
            self.sub_px4 = self.create_subscription(VehicleOdometry, self.px4_topic, self.px4_cb_px4type, 10)
        except Exception:
            self.sub_px4 = self.create_subscription(Odometry, self.px4_topic, self.px4_cb, 10)

        self.get_logger().info(f'DriftMonitor listening {self.vins_topic} and {self.px4_topic}; threshold {self.threshold} m')

    def vins_cb(self, msg: Odometry):
        self.vins_pose = (msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z)
        self.check_drift()

    def px4_cb(self, msg: Odometry):
        self.px4_pose = (msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z)
        self.check_drift()

    def px4_cb_px4type(self, msg: VehicleOdometry):
        # px4 VehicleOdometry fields: x,y,z
        self.px4_pose = (msg.x, msg.y, msg.z)
        self.check_drift()

    def check_drift(self):
        if self.vins_pose is None or self.px4_pose is None:
            return
        dx = self.vins_pose[0] - self.px4_pose[0]
        dy = self.vins_pose[1] - self.px4_pose[1]
        dz = self.vins_pose[2] - self.px4_pose[2]
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist > self.threshold:
            alert = String()
            alert.data = f'DRIFT_ALERT {dist:.3f} m > threshold {self.threshold} m'
            self.alert_pub.publish(alert)
            self.get_logger().warn(alert.data)

def main(args=None):
    rclpy.init(args=args)
    node = DriftMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
