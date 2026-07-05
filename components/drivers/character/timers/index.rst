==============
定时器驱动程序
==============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

.. toctree::
  :caption: 支持的驱动程序

  timer.rst
  oneshot.rst
  pwm.rst
  watchdog.rst
  rtc.rst
  capture.rst
  dshot.rst

NuttX 定时子系统由四层组成：

  .. figure:: timer.svg

  * 1 硬件定时器驱动程序：包含各种硬件定时器驱动程序的实现。
  * 2 定时器驱动程序抽象：如 Oneshot 和 Timer，提供单次/周期定时器硬件抽象。
  * 3 操作系统定时器接口：Arch_Timer(up_timer_*) 和 Arch_Alarm(up_alarm_*)，
    提供相对定时器（在一定延迟后触发事件）和绝对定时器（在特定时间触发事件）接口。
  * 4 操作系统定时器抽象：wdog 定时器管理软件定时器，并为上层提供统一的定时器 API。

定时器驱动程序抽象不是必需的。如果驱动程序足够简单（例如仅提供周期性 tick），可以直接实现操作系统定时器接口 Arch_Timer，绕过定时器驱动程序抽象层。

定时器驱动程序抽象的设计目的是简化驱动程序实现、提高性能并增强驱动程序代码的可重用性。
