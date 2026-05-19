# my_robot_description

`my_robot_description` 是当前工作空间维护的机器人描述包，负责 Nero 机械臂、末端执行器、相机安装、工位和组合机器人模型。

## 包职责

- 维护 Nero 机器人 URDF / xacro / mesh。
- 维护 grinder、camera、TCP 相关末端描述。
- 维护 blade polishing 工位描述。
- 提供组合入口 `nero_with_grinder`。
- 提供 Tesseract / MoveIt 使用的 SRDF 和插件配置。

本包只描述几何、语义和静态配置，不实现 ROI、三维重建、BT 流程、刀路规划或轨迹执行逻辑。

## 主要入口

```text
urdf/robots/nero/
urdf/end_effectors/grinder/
urdf/workcells/blade_polishing/
urdf/variants/nero_with_grinder/
srdf/variants/nero_with_grinder/
config/variants/nero_with_grinder/
launch/display.launch.py
```

## 构建

```bash
colcon build --packages-select my_robot_description --symlink-install
source install/setup.bash
```

## 显示模型

```bash
ros2 launch my_robot_description display.launch.py
```

## 关键维护边界

- `vendor/agx_arm_urdf/nero/` 保留上游 AgileX Nero 基线，尽量不做项目定制。
- 项目定制内容放在 `urdf/`、`meshes/`、`srdf/`、`config/` 的标准目录中。
- 最终相机外参、TCP、collision 和 ready pose 必须来自实机或硬件确认，不得写入猜测值。
- 包内 README 只记录包级职责、入口和维护边界；系统总架构写在 root `docs/Architecture.md`。

## 远端

- `origin`: `https://github.com/chenzixin-zn/my_robot_description.git`
- `upstream`: `https://github.com/agilexrobotics/agx_arm_urdf.git`
