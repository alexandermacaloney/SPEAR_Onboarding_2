# Teleop Node
""" The pursuit of this node is to subscribe to the /joy topic, 
which is published by the joy_node, and then convert the joystick input into commands 
for the robot arm. The node will then publish these commands to the appropriate topics 
that control the robot arm's movement. """

import rclpy # Import the ROS 2 Python client library, which provides the necessary tools to create ROS 2 nodes and interact with the ROS 2 ecosystem.
from rclpy.node import Node # Import the Node class from rclpy, which is used to create a ROS 2 node that can communicate with other nodes in the ROS 2 network
from sensor_msgs.msg import Joy # Import the Joy message type from the sensor_msgs package, which is used to represent joystick input data, including axes and button states
from control_msgs.msg import JointJog # Import the JointJog message type from the control_msgs package, which names the joints to move and supplies their requested velocities

velocity_scale = 1.0 # This variable defines the scale factor for the joint velocities. It is used to control the speed of the robot arm's movement based on joystick input. A higher value will result in faster movement, while a lower value will result in slower movement.

class TeleopNode(Node): # Creates a new class called TeleopNode that inherits from the Node class. Inherits functionality from the Node class in ROS 2
    def __init__(self): # Initializes the TeleopNode class. It sets up the node's name and initializes the subscription to the /joy topic.
        super().__init__('teleop_node') # Calls the constructor of the parent Node class and sets the name of this node to 'teleop_node'. This is important for identifying the node in the ROS 2 network.
        
        self.active_joint = 1 # This variable is used to keep track of the currently active joint that the joystick input will control. It allows the user to switch between different joints of the robot arm for teleoperation. The value of 1 indicates that the first joint is initially active.
        
        self.subscription = self.create_subscription( # Create a subscription to the /joy topic, which is published by the joy_node. This allows the teleop_node to receive joystick input data.
            Joy, # Specify the message type for the subscription, which is Joy in this case.
            '/joy', # Specify the topic name to subscribe to, which is /joy. This topic is where the joystick input data is published by the joy_node.
            self.joy_callback, # Specify the callback function to be called whenever a new message is received on the /joy topic.
            10, # Number of messages to queue if the subscriber is not able to process them fast enough
        )
        self.joint_publisher = self.create_publisher( # Create a publisher to the /servo_node/delta_joint_cmds topic, which is used to send joint movement commands to the robot arm. This allows the teleop_node to control the robot arm's movement based on joystick input
            JointJog, # Specify the message type for the publisher, which is JointJog in this case
            '/servo_node/delta_joint_cmds', # Specify the topic name to publish to, which is /servo_node/delta_joint_cmds
            10, # Number of messages to queue if the subscriber is not able to process them fast enough
        )

    def joy_callback(self, msg): # Defines the callback function that will be called whenever a new Joy message is received on the /joy topic
        self.get_logger().info(f'axes: {msg.axes}, buttons: {msg.buttons}') # Logs the received joystick input data (axes and buttons) to the console. This is useful for debugging and verifying that the node is receiving the correct input from the joystick.

        if len(msg.axes) < 2 or len(msg.buttons) < 3: # Only proceed if there are two axes or three buttons in the message. This check ensures that the node does not attempt to process an empty message, which could lead to errors
            return

        horizontal = msg.axes[0] # Get the horizontal axis value from the joystick input message
        vertical = msg.axes[1] # Get the vertical axis value from the joystick input message        


        stick_centered = (
            abs(horizontal) <= 0.1 and abs(vertical) <= 0.1
        )

        if stick_centered: # If the joystick is centered, allow the toggling of the joints 
            if msg.buttons[0] == 1: # If the 'A' button on the joystick is pressed, switch to controlling joint 1. This allows the user to select which joint of the robot arm they want to control using the joystick.
                self.active_joint = 1 # Set the active joint to joint 1. This means that subsequent joystick input will control joint 1 of the robot arm.
            elif msg.buttons[1] == 1: # If the 'B' button on the joystick is pressed, switch to joint 3
                self.active_joint = 3 # Set the active joint to joint 3. This means that subsequent joystick input will control joint 3 of the robot arm.
            elif msg.buttons[2] == 1: # If the 'X' button on the joystick is pressed, switch to joint 5
                self.active_joint = 5 # Set the active joint to joint 5. This means that subsequent joystick input will control joint 5 of the robot arm.

        command = JointJog() # Creates a new JointJog message object, which will be used to send joint movement commands to the robot arm based on the joystick input. This object will hold the joint names and their corresponding velocities that will be published to the /servo_node/delta_joint_cmds topic.
        command.header.stamp = self.get_clock().now().to_msg() # Timestamp for the command
        command.joint_names = [ # Name of the joint to move
            f'joint_{self.active_joint}',
            f'joint_{self.active_joint + 1}',
            ] 


        horizontal_velocity = 0.0 # Initialize the horizontal velocity to 0
        vertical_velocity = 0.0 # Initialize the vertical velocity to 0


        if abs(horizontal) > 0.1: # If outside deadzone, set the horizontal velocity based on the joystick input and the velocity scale
            horizontal_velocity = horizontal * velocity_scale

        if abs(vertical) > 0.1: # If outside deadzone, set the vertical velocity based on the joystick input and the velocity scale
            vertical_velocity = vertical * velocity_scale

        command.velocities = [ # Set the velocities for the active joint and the next joint based on the calculated horizontal and vertical velocities. This allows the user to control the movement of two joints simultaneously using the joystick input.
            horizontal_velocity,
            vertical_velocity,
        ]

        self.joint_publisher.publish(command) # Publishes the JointJog command to the /servo_node/delta_joint_cmds topic, which sends the joint movement commands to the robot arm



def main(args=None):
    # 1. Initialize ROS communications.
    rclpy.init(args=args) # Initializes the ROS 2 Python client library 
    # 2. Create a TeleopNode object and store it in node.
    node = TeleopNode() # Creates an instance of the TeleopNode class, which sets up the subscription to the /joy topic and prepares the node to receive joystick input data.
    try:
        # 3. Spin the node so ROS can run its callbacks.
        rclpy.spin(node) # Spins the node. This keeps the node running and responsive to joystick input.
    except KeyboardInterrupt:
        pass
    finally:
        # 4. Destroy the node.
        node.destroy_node() # Destroys the TeleopNode instance
        # 5. Shut down ROS if it is still running.
        if rclpy.ok():
            rclpy.shutdown() # Shuts down the ROS 2 Python client library, cleaning up any resources used by the node and ensuring a graceful exit from the program

if __name__ == '__main__':
    main() # Calls the main function to start the teleop_node. This is the entry point of the script