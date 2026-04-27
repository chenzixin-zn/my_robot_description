# my_robot_description

[中文](./README.md)

This repository is `chenzixin-zn/my_robot_description`, the robot description package used by this workspace. The ROS 2 package name remains `agx_arm_description` so existing launch files, URDF references, RViz configs, and package dependencies stay compatible.

The main branch currently keeps only the AgileX Nero baseline. Piper, Piper H, Piper L, Piper X, and standalone Revo2 hand models are no longer kept on this branch.

## Remotes

- `origin`: `https://github.com/chenzixin-zn/my_robot_description.git`
- `upstream`: `https://github.com/agilexrobotics/agx_arm_urdf.git`

When syncing official Nero updates, use a `sync/<topic>` branch first and merge the reviewed result into `main`.

## Layout

```text
.
├── nero/
│   ├── config/
│   ├── launch/
│   ├── meshes/
│   ├── rviz/
│   ├── srdf/
│   └── urdf/
├── CMakeLists.txt
├── package.xml
└── README.md
```

Planned custom content should use these meanings:

- `nero/`: official Nero baseline
- `custom_end_effectors/`: custom tools, flanges, cameras, and grippers
- `robot_variants/`: composed robot entry points
- `config/` and `launch/`: custom control and launch configuration

## Usage

Build in a ROS 2 workspace:

```bash
colcon build --packages-select agx_arm_description --symlink-install
source install/setup.bash
```

Display the Nero model:

```bash
ros2 launch agx_arm_description display.launch.py
```

## License

This repository keeps the upstream license notice. See [LICENSE](./LICENSE).
