import launch 
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import UnlessCondition, IfCondition
import os

def generate_launch_description():
    pkgPath = FindPackageShare(package="nav2_test").find("nav2_test")
    urdfModelPath = os.path.join(pkgPath, "urdf/my_robot.urdf")
    configPath = os.path.join(pkgPath, "rviz/config.rviz")

    with open(urdfModelPath, 'r') as infp:
        robot_desc = infp.read()

    params = {"robot_description": robot_desc}

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[params],
        output= "screen"
    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        parameters=[params],
        condition=UnlessCondition(LaunchConfiguration("gui"))
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        condition=IfCondition(LaunchConfiguration("gui"))
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=['-d', configPath]
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name="gui", default_value="True", description="This is a flag for Joint_state_publisher_gui"),
        launch.actions.DeclareLaunchArgument(name="model", default_value=urdfModelPath, description="Path to the urdf model file"),
        robot_state_publisher_node,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])