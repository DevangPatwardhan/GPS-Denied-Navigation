# GPS-Denied Navigation with VINS-Mono ROS2

This repository contains a ROS2-based setup for Visual-Inertial Navigation using **VINS-Mono**. It bridges VINS-Mono outputs to PX4 vehicle messages, enabling navigation in GPS-denied environments.

---

## Background Theory

**Visual-Inertial Odometry (VIO)** combines camera measurements with inertial sensors (IMU) to estimate the position and orientation of a vehicle in 3D space. This is crucial in environments where GPS is unavailable or unreliable, such as indoors, urban canyons, or under dense foliage.

**VINS-Mono** is a widely used VIO framework that fuses monocular camera images with IMU data to estimate state with high accuracy. The `vins_px4_bridge` in this repository converts VINS outputs into PX4-compatible messages, enabling integration with autopilot systems for autonomous navigation.

---

## Features / What’s New

- ROS2 port of VINS-Mono
- PX4-compatible odometry bridge (`vins_px4_bridge`)
- Real-time visualization via `pose_graph`
- Parameterizable launch configurations
- Example Euroc dataset configuration included
- Support for drift monitoring using `drift_monitor`

---

## Dependencies

- ROS2 Humble
- PX4 ROS messages: `px4_msgs`
- OpenCV ≥ 4.5
- Numpy
- Python 3.10+
- Other dependencies as listed in VINS-Mono ROS2 package

---

## Installation

```bash
# Clone this repository
cd ~/ros2_vio_px4_ws/src
git clone https://github.com/DevangPatwardhan/GPS-Denied-Navigation.git

# Initialize workspace
cd ~/ros2_vio_px4_ws
rosdep install --from-paths src --ignore-src -r -y

# Build workspace
colcon build --symlink-install
'''

