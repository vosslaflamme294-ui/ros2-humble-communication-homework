# Ubuntu 22.04 + ROS2 Humble 作业

本作业基于当前已安装的 Ubuntu 22.04 与 ROS2 Humble 环境完成。

- 工作空间：`zhang_ros_ws`
- 功能包：`zhang_pkg`
- 自定义消息：`msg/StudentInfo.msg`
- 自定义服务：`srv/AddTwoInts.srv`
- 自定义动作：`action/CountUntil.action`
- 报告：`实验报告_ROS2_Humble_按原表格_张同学.docx`

## 编译

```bash
source /opt/ros/humble/setup.bash
cd zhang_ros_ws
colcon build --packages-select zhang_pkg
source install/setup.bash
```

## 运行

Topic：

```bash
ros2 run zhang_pkg student_subscriber.py
ros2 run zhang_pkg student_publisher.py
```

Service：

```bash
ros2 run zhang_pkg add_two_ints_server.py
ros2 run zhang_pkg add_two_ints_client.py 12 30
```

Action：

```bash
ros2 run zhang_pkg count_until_action_server.py
ros2 run zhang_pkg count_until_action_client.py 5 0.2
```
