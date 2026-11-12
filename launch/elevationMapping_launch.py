import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # -------------------------
    # Directories
    # -------------------------
    elevation_dir = get_package_share_directory('elevation_mapping')
    grid_map_demos_dir = get_package_share_directory('grid_map_demos')

    config_dir = os.path.join(elevation_dir, 'config')

    # -------------------------
    # Launch configs
    # -------------------------
    filters_config_file = LaunchConfiguration('filters_config')
    visualization_config_file = LaunchConfiguration('visualization_config')


    # -------------------------
    # Launch arguments
    # -------------------------
    declare_filters_config_file_cmd = DeclareLaunchArgument(
        'filters_config',
        default_value=os.path.join(
            elevation_dir,
            'config',
            'grid_maps/filters_demo_filter_chain.yaml'
        )
    )

    declare_visualization_config_file_cmd = DeclareLaunchArgument(
        'visualization_config',
        default_value=os.path.join(
            elevation_dir,
            'config',
            'grid_maps/filters_demo.yaml'
        )
    )

    # -------------------------
    # Elevation Mapping Node
    # -------------------------
    elevation_mapping_node = Node(
        package='elevation_mapping',
        executable='elevation_mapping',
        name='elevation_mapping',
        output='screen',
        parameters=[
            os.path.join(config_dir, "robots/ground_truth_demo.yaml"),
            os.path.join(config_dir, "elevation_maps/long_range.yaml"),
            os.path.join(config_dir, "sensor_processors/perfect.yaml"),
            os.path.join(config_dir, "postprocessing/postprocessor_pipeline.yaml"),
        ],
    )

    # -------------------------
    # Grid map filter demo node
    # -------------------------
    grid_map_filter_demo_node = Node(
        package='grid_map_demos',
        executable='filters_demo',
        name='grid_map_filters',
        output='screen',
        parameters=[filters_config_file]
    )

    # -------------------------
    # Visualization node
    # -------------------------
    grid_map_visualization_node = Node(
        package='grid_map_visualization',
        executable='grid_map_visualization',
        name='grid_map_visualization',
        output='screen',
        parameters=[visualization_config_file]
    )

    # -------------------------
    # Launch description
    # -------------------------
    ld = LaunchDescription()

    ld.add_action(declare_filters_config_file_cmd)
    ld.add_action(declare_visualization_config_file_cmd)


    ld.add_action(elevation_mapping_node)
    ld.add_action(grid_map_filter_demo_node)

    ld.add_action(grid_map_visualization_node)


    return ld