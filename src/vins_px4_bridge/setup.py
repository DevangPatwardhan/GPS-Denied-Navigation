from setuptools import find_packages, setup

package_name = 'vins_px4_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='deva',
    maintainer_email='patwardhandevang@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pose_bridge = vins_px4_bridge.pose_bridge:main', 
            'drift_monitor = vins_px4_bridge.drift_monitor:main',
        ],
    },
)
