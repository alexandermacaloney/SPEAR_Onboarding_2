from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'plex_arm_5'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
            (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.py'))),
            (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*'))),
            (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*'))),
            (os.path.join('share', package_name, 'meshes'), glob(os.path.join('meshes', '*'))),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='spearua',
    maintainer_email='TODO',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'teleop_node = plex_arm_5.teleop_node:main', # Calls the main function in the teleop_node.py file when the teleop_node command is executed. This allows the user to run the teleop_node directly from the command line without needing to specify the full path to the script.
        ],
    },
)
