# my_robot_description

[English](./README_EN.md)

本仓库是 `chenzixin-zn/my_robot_description`，用于维护当前工作区使用的机器人描述文件。ROS 2 包名仍为 `agx_arm_description`，以保持已有 launch、URDF、RViz 和依赖关系兼容。

当前主干只保留 AgileX Nero 机械臂基线。Piper、Piper H、Piper L、Piper X 和 Revo2 独立手模型不再放在本仓库主干中。

## 远端关系

- `origin`: `https://github.com/chenzixin-zn/my_robot_description.git`
- `upstream`: `https://github.com/agilexrobotics/agx_arm_urdf.git`

后续同步官方 Nero 更新时，建议先在 `sync/<topic>` 分支处理，再合入 `main`。

## 目录结构

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

计划中的自定义内容按语义分层：

- `nero/`: 官方 Nero 基线
- `custom_end_effectors/`: 自定义末端、法兰、相机、夹爪
- `robot_variants/`: 不同组合入口
- `config/`、`launch/`: 自定义控制和启动配置

## 使用方式

在 ROS 2 工作空间中构建：

```bash
colcon build --packages-select agx_arm_description --symlink-install
source install/setup.bash
```

显示 Nero 模型：

```bash
ros2 launch agx_arm_description display.launch.py
```

## 许可证

本仓库保留上游项目的许可证声明，详见 [LICENSE](./LICENSE)。
