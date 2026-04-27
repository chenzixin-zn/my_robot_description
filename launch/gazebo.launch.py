import os
import xacro
import yaml
import logging
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, DeclareLaunchArgument, SetEnvironmentVariable
from launch.event_handlers import OnProcessStart
import inspect
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch.actions import ExecuteProcess

logger = logging.getLogger('gazebo_launch')


def generate_launch_description():

    # --- Key configurable names/paths (edit here) ---
    PACKAGE_NAME = 'nero_description'
    URDF_XACRO = 'nero_description.urdf.xacro'
    JOINT_NAMES_YAML = 'joint_names_nero_description.yaml'
    ROS2_CONTROL_YAML = 'ros2_control.yaml'
    GAZEBO_USE_SIM_TIME = 'true'
    GAZEBO_VERBOSE = 'true'
    SPAWN_ENTITY_NAME = 'nero'
    TMP_URDF = os.path.join('/tmp', PACKAGE_NAME + '_rendered.urdf')
    # -----------------------------------------------

    ld = LaunchDescription()

    package_path = get_package_share_directory(PACKAGE_NAME)
    urdf_path = os.path.join(package_path, 'urdf', URDF_XACRO)
    joint_names_path = os.path.join(package_path, 'config', JOINT_NAMES_YAML)
    # defaults
    controllers_path_default = os.path.join(package_path, 'config', ROS2_CONTROL_YAML)
    model_path_default = os.path.join(package_path, 'models') if os.path.isdir(os.path.join(package_path, 'models')) else ''

    # Declare launch arguments so users can override at runtime
    ld.add_action(DeclareLaunchArgument('controllers_path', default_value=controllers_path_default,
                                       description='Path to ros2_control controllers YAML'))
    ld.add_action(DeclareLaunchArgument('use_sim_time', default_value=GAZEBO_USE_SIM_TIME,
                                       description='Use simulation time'))
    ld.add_action(DeclareLaunchArgument('gazebo_model_database_uri', default_value='',
                                       description='Gazebo model database URI (empty to disable network access)'))
    ld.add_action(DeclareLaunchArgument('gazebo_model_path', default_value=model_path_default,
                                       description='Additional Gazebo model path'))
    ld.add_action(DeclareLaunchArgument('gui', default_value='true', description='Start gzclient GUI'))

    # LaunchConfiguration substitutions
    controllers_path = LaunchConfiguration('controllers_path')
    use_sim_time = LaunchConfiguration('use_sim_time')
    gazebo_model_database_uri = LaunchConfiguration('gazebo_model_database_uri')
    gazebo_model_path = LaunchConfiguration('gazebo_model_path')

    # Render xacro (use context manager to avoid file-handle leakage)
    try:
        with open(urdf_path, 'r') as xf:
            model_doc = xacro.parse(xf)
            xacro.process_doc(model_doc)
            robot_description = model_doc.toxml()
    except Exception as e:
        logger.exception('Failed to process xacro: %s', urdf_path)
        raise

    # Write rendered URDF to temporary file for gazebo spawn (prefer file)
    # Write rendered URDF to temporary file for gazebo spawn (prefer file)
    try:
        with open(TMP_URDF, 'w') as f:
            f.write(robot_description)
        tmp_urdf_path = TMP_URDF
    except Exception:
        tmp_urdf_path = None

    # robot_state_publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': use_sim_time}]
    )

    # Start gazebo server and client
    start_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gzserver.launch.py')),
        launch_arguments={'verbose': GAZEBO_VERBOSE, 'use_sim_time': use_sim_time}.items()
    )

    start_gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gzclient.launch.py')),
        condition=IfCondition(LaunchConfiguration('gui'))
    )

    # Spawn robot into gazebo (prefer file, fallback to topic)
    spawn_args = ['-entity', SPAWN_ENTITY_NAME]
    if tmp_urdf_path and os.path.exists(tmp_urdf_path):
        spawn_args += ['-file', tmp_urdf_path]
    else:
        spawn_args += ['-topic', 'robot_description']

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=spawn_args,
        output='screen'
    )

    # ros2_control node (loads controllers YAML). Include robot_description param so
    # controllers/hardware that expect the URDF can access it immediately.
    ros2_control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        output='screen',
        parameters=[controllers_path, {'robot_description': robot_description, 'use_sim_time': use_sim_time}],
        remappings=[('~/robot_description', 'robot_description')],
    )

    # Spawn controllers declared in the controllers YAML
    spawner_controllers = []
    # Load controllers YAML and prepare spawner Nodes. Add YAML parse error handling.
    # Pre-parse default controllers YAML to prepare spawner nodes (won't reflect runtime overrides)
    try:
        with open(controllers_path_default, 'r') as f:
            controllers = yaml.safe_load(f)
        for key, val in controllers.get('controller_manager', {}).get('ros__parameters', {}).items():
            if isinstance(val, dict) and isinstance(val.get('type'), str):
                spawner_exec = 'spawner' if os.environ.get('ROS_DISTRO', '') > 'foxy' else 'spawner.py'
                spawner_controllers.append({'name': key, 'exec': spawner_exec})
    except FileNotFoundError:
        logger.warning('Controllers file not found: %s', controllers_path_default)
    except yaml.YAMLError as ye:
        logger.exception('Failed to parse controllers YAML: %s', controllers_path_default)
    except Exception:
        logger.exception('Unexpected error loading controllers file: %s', controllers_path_default)

    # Add actions to launch description in logical order with event handlers:
    # 1) Start robot_state_publisher immediately
    # 2) Start gazebo server/client
    # 3) When gazebo server starts, spawn the robot
    # 4) When robot is spawned, start ros2_control_node
    # 5) When ros2_control_node starts, spawn controllers

    ld.add_action(robot_state_publisher_node)
    # set Gazebo model env vars before starting server
    ld.add_action(SetEnvironmentVariable('GAZEBO_MODEL_DATABASE_URI', gazebo_model_database_uri))
    ld.add_action(SetEnvironmentVariable('GAZEBO_MODEL_PATH', gazebo_model_path))

    ld.add_action(start_gazebo_server)
    # start gzclient only after gzserver and only if gui is enabled
    # Helper matchers: OnProcessStart expects an ExecuteProcess or a callable matcher
    def _is_gzserver(action):
        return hasattr(action, 'cmd') and any('gzserver' in str(c) for c in getattr(action, 'cmd', []))

    def _is_spawn_entity(action):
        return hasattr(action, 'cmd') and any('spawn_entity.py' in str(c) for c in getattr(action, 'cmd', []))

    def _is_ros2_control(action):
        return hasattr(action, 'cmd') and any('ros2_control_node' in str(c) or 'controller_manager' in str(c) for c in getattr(action, 'cmd', []))

    # Helper matchers: OnProcessStart expects an ExecuteProcess or a callable matcher

    ld.add_action(RegisterEventHandler(
        OnProcessStart(action_matcher=_is_gzserver, on_start=[start_gazebo_client])
    ))

    # spawn robot after gazebo server starts
    ld.add_action(RegisterEventHandler(
        OnProcessStart(action_matcher=_is_gzserver, on_start=[spawn_robot])
    ))

    # start ros2_control_node after robot is spawned
    ld.add_action(RegisterEventHandler(
        OnProcessStart(action_matcher=_is_spawn_entity, on_start=[ros2_control_node])
    ))

    # spawn controllers after ros2_control_node starts
    # Spawn controllers after ros2_control_node starts
    if spawner_nodes:
        ld.add_action(RegisterEventHandler(
            OnProcessStart(action_matcher=_is_ros2_control, on_start=spawner_nodes)
        ))

    return ld