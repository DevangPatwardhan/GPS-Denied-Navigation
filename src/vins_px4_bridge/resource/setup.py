from setuptools import setup

package_name = 'vins_px4_bridge'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='Bridge VINS odom to PX4 and monitor drift',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'pose_bridge = vins_px4_bridge.pose_bridge:main',
            'drift_monitor = vins_px4_bridge.drift_monitor:main',
        ],
    },
)

