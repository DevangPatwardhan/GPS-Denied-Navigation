import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/deva/ros2_vio_px4_ws/install/vins_px4_bridge'
