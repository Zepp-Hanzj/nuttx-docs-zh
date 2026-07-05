===================
``alarm`` RTC 闹钟
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

一个测试 RTC 驱动程序闹钟 IOCTL 的简单示例。

依赖项：

- ``CONFIG_RTC_DRIVER`` – RTC 驱动程序必须初始化以允许用户空间访问 RTC。
- ``CONFIG_RTC_ALARM`` – 必须启用 RTC 闹钟支持。

配置：

- ``CONFIG_EXAMPLES_ALARM`` – 启用 RTC 驱动程序闹钟测试。
- ``CONFIG_EXAMPLES_ALARM_PROGNAME`` – 安装 NSH ELF 程序时使用的程序名称。
- ``CONFIG_EXAMPLES_ALARM_PRIORITY`` – 闹钟守护进程优先级。
- ``CONFIG_EXAMPLES_ALARM_STACKSIZE`` – 闹钟守护进程栈大小。
- ``CONFIG_EXAMPLES_ALARM_DEVPATH`` – RTC 设备路径（``/dev/rtc0``）。
- ``CONFIG_EXAMPLES_ALARM_SIGNO`` – 闹钟信号。
