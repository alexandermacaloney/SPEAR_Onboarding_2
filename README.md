# Arm teleop — ROS 2 Humble

- Run these in Ubuntu, from the workspace root. Assumes ROS 2 Humble is installed.
- After connecting the controller by USB, check detection with `ros2 run joy joy_enumerate_devices` after sourcing ROS.

```bash
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-select plex_arm_5
source install/setup.bash
ros2 launch plex_arm_5 teleop.launch.py
```

- Launch starts Joy, teleop, RViz, MoveIt Servo, and mock arm controllers. Allow at leadst 10 seconds for Servo startup.
- Center the stick to select a pair: A = joints 1/2, B = 3/4, X = 5/6.
- Left stick horizontal = first joint; vertical = second. Triggers unused in current implenantion but could be used for the endeffector as per conversation withj Levi
- Controller button/axis mapping still needs checking on native Ubuntu. Synthetic Joy input and RViz movement tested in WSL.
- Without a controller, publish fake input from a second terminal:

```bash
source /opt/ros/humble/setup.bash
ros2 topic pub --rate 20 /joy sensor_msgs/msg/Joy \
  "{axes: [0.5, 0.0], buttons: [0, 0, 0]}"
```

- Ctrl+C stops the fake input; Servo stops movement after commands expire (~0.5 seconds).
