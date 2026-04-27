# my_robot_description

[English](./README_EN.md)

本仓库是 `chenzixin-zn/my_robot_description`，用于维护当前工作区使用的机器人、末端工具和工位描述文件。ROS 2 包名为 `my_robot_description`。

当前主干以 AgileX Nero 机械臂为官方基线，并在独立目录中维护本项目的 grinder、camera、workbench 和组合入口。

## 远端关系

- `origin`: `https://github.com/chenzixin-zn/my_robot_description.git`
- `upstream`: `https://github.com/agilexrobotics/agx_arm_urdf.git`

后续同步官方 Nero 更新时，建议先在 `sync/<topic>` 分支处理，只更新 `vendor/agx_arm_urdf/nero/`，再检查标准对外目录和组合入口是否需要跟随调整。

## 目录结构

```text
.
├── vendor/agx_arm_urdf/nero/          # 官方 Nero 基线，用于 upstream 同步
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

目录语义：

- `vendor/agx_arm_urdf/nero/`: 官方基线，尽量保持原样
- `urdf/robots/nero/`: 对外使用的 Nero 描述入口
- `urdf/end_effectors/`: 自定义末端、法兰、相机、夹爪
- `urdf/workcells/`: 工位、工装、静态标定相关描述
- `urdf/variants/`: 机器人与末端、工位组合后的入口

## 使用方式

在 ROS 2 工作空间中构建：

```bash
colcon build --packages-select my_robot_description --symlink-install
source install/setup.bash
```

显示 Nero 模型：

```bash
ros2 launch my_robot_description display.launch.py
```

## 许可证

本仓库保留上游项目的许可证声明，详见 [LICENSE](./LICENSE)。
