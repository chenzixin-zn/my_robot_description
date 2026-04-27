# my_robot_description

[中文](./README.md)

This repository is `chenzixin-zn/my_robot_description`, the robot, end-effector, and workcell description package used by this workspace. The ROS 2 package name is `my_robot_description`.

The main branch uses the AgileX Nero arm as the official baseline and keeps this project's grinder, camera, workbench, and composed robot variants in separate directories.

## Remotes

- `origin`: `https://github.com/chenzixin-zn/my_robot_description.git`
- `upstream`: `https://github.com/agilexrobotics/agx_arm_urdf.git`

When syncing official Nero updates, use a `sync/<topic>` branch first, update only `vendor/agx_arm_urdf/nero/`, then review whether the public standard layout and composed variants need follow-up changes.

## Layout

```text
.
├── vendor/agx_arm_urdf/nero/          # Official Nero baseline for upstream sync
├── urdf/
│   ├── robots/nero/
│   ├── end_effectors/grinder/
│   ├── workcells/blade_polishing/
│   └── variants/nero_with_grinder/
├── meshes/
│   ├── robots/nero/
│   ├── end_effectors/grinder/
│   └── workcells/blade_polishing/
├── srdf/
│   ├── robots/nero/
│   └── variants/nero_with_grinder/
├── config/
│   ├── robots/nero/
│   ├── workcells/blade_polishing/
│   └── variants/nero_with_grinder/
├── launch/
├── rviz/
├── CMakeLists.txt
├── package.xml
└── README.md
```

Directory meanings:

- `vendor/agx_arm_urdf/nero/`: official baseline, kept as unchanged as practical
- `urdf/robots/nero/`: public Nero description entry points
- `urdf/end_effectors/`: custom tools, flanges, cameras, and grippers
- `urdf/workcells/`: workcell, fixture, and static calibration descriptions
- `urdf/variants/`: composed robot, end-effector, and workcell entry points

## Usage

Build in a ROS 2 workspace:

```bash
colcon build --packages-select my_robot_description --symlink-install
source install/setup.bash
```

Display the Nero model:

```bash
ros2 launch my_robot_description display.launch.py
```

## License

This repository keeps the upstream license notice. See [LICENSE](./LICENSE).
