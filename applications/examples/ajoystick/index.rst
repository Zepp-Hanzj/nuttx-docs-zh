=============================
``ajoystick`` 模拟摇杆
=============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是模拟摇杆驱动程序的简单测试。有关此驱动程序的详细信息，请参阅 ``nuttx/include/nuttx/input/ajoystick.h``。

配置前置条件：

- ``CONFIG_AJOYSTICK`` – 模拟摇杆驱动程序。

示例配置：
- ``CONFIG_EXAMPLES_AJOYSTICK`` – 启用模拟摇杆示例。
- ``CONFIG_EXAMPLES_AJOYSTICK_DEVNAME`` – 摇杆设备名称。默认：``/dev/adjoy0``。
- ``CONFIG_EXAMPLES_AJOYSTICK_SIGNO`` – 用于通知测试应用程序的信号。默认：``32``。
