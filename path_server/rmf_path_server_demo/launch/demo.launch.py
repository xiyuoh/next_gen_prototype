from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def launch_setup(context, *args, **kwargs):
    robots_str = LaunchConfiguration('robots').perform(context)
    # Support space or comma-separated lists
    robots_list = [r.strip() for r in robots_str.replace(',', ' ').split() if r.strip()]

    nodes = []

    # 1. Start the RMF path server
    nodes.append(Node(
        package='rmf_path_server',
        executable='rmf_path_server',
        name='rmf_path_server',
        output='both'
    ))

    # 2. Start the destination server
    nodes.append(Node(
        package='rmf_simple_destination_server',
        executable='rmf_simple_destination_server',
        name='rmf_simple_destination_server',
        output='both'
    ))

    # 3. Start the plan executor
    nodes.append(Node(
        package='rmf_plan_executor',
        executable='rmf_plan_executor',
        name='rmf_plan_executor',
        output='both'
    ))

    # 4. Start the path visualizers for each robot
    for robot in robots_list:
        nodes.append(Node(
            package='rmf_path_visualizer',
            executable='rmf_path_visualizer',
            name=f'rmf_path_visualizer_{robot}',
            arguments=[robot],
            output='both'
        ))

    return nodes

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'robots',
            default_value='robot0 robot1',
            description='List of robots to launch visualizers for (e.g. robots:="robot0 robot1")'
        ),
        OpaqueFunction(function=launch_setup)
    ])
