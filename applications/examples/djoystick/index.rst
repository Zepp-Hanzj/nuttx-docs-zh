===============================
``djoystick`` 离散摇杆
===============================

这是一个简单的离散摇杆驱动测试。有关该驱动的详细信息，请参阅 ``nuttx/include/nuttx/input/djoystick.h``。

配置前置条件：

- ``CONFIG_INPUT_DJOYSTICK`` – 离散摇杆驱动。

示例配置：

- ``CONFIG_EXAMPLES_DJOYSTICK`` – 启用离散摇杆示例。
- ``CONFIG_EXAMPLES_DJOYSTICK_DEVNAME`` – 摇杆设备名称。默认为 ``/dev/djoy0``。
- ``CONFIG_EXAMPLES_DJOYSTICK_SIGNO`` – 用于通知测试应用程序的信号。默认为 ``32``。
