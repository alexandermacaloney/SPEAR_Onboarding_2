# Central Launch file. Launches joy_node, teleop_node, and other launch files.
from launch import LaunchDescription # Import the LaunchDescription class, which is used to describe the launch configuration.
from launch.actions import IncludeLaunchDescription # Import the IncludeLaunchDescription action, which allows you to include other launch files within this one.
from launch.launch_description_sources import PythonLaunchDescriptionSource # tells ROS that the included launch file is Python.
from ament_index_python.packages import get_package_share_directory # Import the get_package_share_directory function, which is used to find the directory of a specific ROS package.
from launch_ros.actions import Node # Import the Node action, which is used to launch ROS nodes.
import os # Import the os module, which provides a way to interact with the operating system, such as file path manipulations.


def generate_launch_description(): 
    package_dir = get_package_share_directory('plex_arm_5') # Finds the package directory for plex_arm_5. So my specific directory isnt hardcoded. This allows it to work on any machine that has the package installed.
    bringup_path = os.path.join(package_dir, 'launch', 'bringup.launch.py') # Combines the identified directory path with the path to the bringup.launch.py file.

    arm_bringup = IncludeLaunchDescription( # Creates an IncludeLaunchDescription action that includes the bringup.launch.py file. This allows the launch file to include and run the bringup.launch.py file as part of its launch process.
        PythonLaunchDescriptionSource(bringup_path)
    )

    # Launch joy_node
    joy_node = Node(
        package='joy', # Finds the joy package, which is responsible for handling joystick input
        executable='joy_node', # Run its joystick driver, which reads input from a joystick and publishes it as ROS messages in the /joy topic
        parameters=[{'autorepeat_rate': 20.0}], # Joy repeats the last message (or unchanged inputs) every 0.05 seconds (20 Hz). Keeps commands fresh while the stick is held steady

        output='screen', # Shows the output of the node in the terminal window
    )

    # Launch teleop_node
    teleop_node = Node(
        package='plex_arm_5', # Finds the plex_arm_5 package, which contains the teleop_node.py file
        executable='teleop_node', # Run the teleop_node.py file, which subscribes to the /joy topic and converts joystick input into commands for the robot arm
        output='screen', # Shows the output of the node in the terminal window
    )
    return LaunchDescription([arm_bringup, joy_node, teleop_node]) # This line returns a LaunchDescription object that contains the IncludeLaunchDescription action for the arm_bringup.launch.py file. When this launch file is executed, it will include and run the arm_bringup.launch.py file as part of the launch process.



