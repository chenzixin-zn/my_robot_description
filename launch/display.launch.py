import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    package_name = "my_robot_description"
    package_path = get_package_share_directory(package_name)
    urdf_path = os.path.join(package_path, "urdf", "robots", "nero", "nero_description.urdf")
    rviz_config_path = os.path.join(package_path, "rviz", "robots", "nero", "piper_no_gripper.rviz")
    joint_config_path = os.path.join(package_path, "config", "robots", "nero", "joint_names_nero_description.yaml")

    model_doc = xacro.parse(open(urdf_path))
    xacro.process_doc(model_doc)
    robot_description = model_doc.toxml()

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output = "screen",
        parameters=[{"robot_description": robot_description}]
    )


    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        parameters=[joint_config_path]
    )


    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
    )


    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d",rviz_config_path]
    )


    ld.add_action(robot_state_publisher_node)
    # ld.add_action(joint_state_publisher_node)
    ld.add_action(joint_state_publisher_gui_node)
    ld.add_action(rviz_node)

    return ld
