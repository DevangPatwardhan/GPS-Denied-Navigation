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


