# GPS-Denied Navigation with VINS-Mono ROS2

This repository contains a ROS2-based setup for Visual-Inertial Navigation using **VINS-Mono**. It bridges VINS-Mono outputs to PX4 vehicle messages, enabling navigation in GPS-denied environments.

---

## Motivation
GPS signals are not always reliable, especially indoors, in tunnels, dense urban areas, or environments where signals can be blocked or jammed. Autonomous systems like drones and robots must still navigate accurately in such conditions. GPS denied navigation enables these systems to estimate their position and orientation using cameras, IMUs, and other onboard sensors, ensuring safe and reliable operation even when GPS is unavailable. This capability is essential for applications such as search and rescue, industrial inspections, and autonomous delivery in challenging environments.

---

## Features 
- ROS2 port of VINS-Mono: Real-time monocular visual-inertial odometry for UAVs and robots, fully compatible with ROS2.
- PX4-compatible odometry bridge (`vins_px4_bridge`): Converts VINS odometry to PX4 format for navigation and autonomous flight.
- Drift monitoring (`drift_monitor`): Tracks odometry drift and alerts when positional deviation exceeds a configurable threshold.

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

### Clone this repository
```bash
cd ~/ros2_vio_px4_ws/src
git clone https://github.com/DevangPatwardhan/GPS-Denied-Navigation.git
```

### Initialize workspace
```bash
cd ~/ros2_vio_px4_ws
rosdep install --from-paths src --ignore-src -r -y
```
### Build workspace
```bash
colcon build --symlink-install
```

## Nodes  

Each new terminal must source:  

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_vio_px4_ws/install/setup.bash
```
### Terminal 1 – Run VINS Estimator
```bash
source /opt/ros/humble/setup.bash
source ~/ros2_vio_px4_ws/install/setup.bash
ros2 launch vins_estimator euroc.launch.py
```


### Terminal 2 – Run PX4 Bridge
```bash
source /opt/ros/humble/setup.bash
source ~/ros2_vio_px4_ws/install/setup.bash
ros2 run vins_px4_bridge pose_bridge --ros-args \
  -p vins_odom_topic:=/vins_estimator/odometry
```

### Terminal 3 – Drift Monitor (Optional)

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_vio_px4_ws/install/setup.bash

ros2 run vins_px4_bridge drift_monitor --ros-args \
  -p vins_odom_topic:=/vins_estimator/odometry \
  -p drift_threshold_m:=0.5
```
### Terminal 4 – PX4 Gazebo Iris SITL (Or whichever is comfortable)
```bash
cd ~/PX4-Autopilot
make px4_sitl_default gazebo-classic_iris
```


