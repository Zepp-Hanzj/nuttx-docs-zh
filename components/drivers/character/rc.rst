======================
遥控设备
======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 为红外输入和输出设备提供遥控（RC）框架。用户空间接口遵循 LIRC 模型，并将每个设备暴露为字符节点，如 ``/dev/lirc0``。

与许多 NuttX 驱动程序一样，RC 子系统分为两部分：

#. 位于 ``drivers/rc/lirc_dev.c`` 的通用上半部分，
#. 由平台或设备特定代码提供的下半部分。

上半部分负责字符驱动程序注册、每次打开的缓冲、``poll()`` 支持和通用 ``ioctl()`` 接口。下半部分负责硬件特定的工作，如接收脉冲时序、传输 IR 数据或报告解码的扫描码。

与 RC 框架相关的文件位于：

- ``include/nuttx/lirc.h``
- ``include/nuttx/rc/lirc_dev.h``
- ``drivers/rc/lirc_dev.c``

应用程序编程接口
=================================

应用程序应包含以下头文件：

.. code-block:: c

  #include <nuttx/lirc.h>
  #include <sys/ioctl.h>

每个 RC 设备注册为 ``/dev`` 中的 POSIX 字符设备。应用程序使用标准 ``open()`` 调用打开设备，然后像其他字符驱动程序一样使用 ``read()``、``write()``、``poll()`` 和 ``ioctl()``。

RC 框架支持三种类型的下半部分设备：

- ``LIRC_DRIVER_SCANCODE`` 用于报告解码扫描码的设备
- ``LIRC_DRIVER_IR_RAW`` 用于报告原始脉冲/间隔时序的设备
- ``LIRC_DRIVER_IR_RAW_TX`` 仅传输的原始设备

原始脉冲/间隔格式
======================

原始 IR 时序以 LIRC ``mode2`` 格式传输。每个样本是一个 32 位 ``unsigned int`` 值。高 8 位描述样本类型，低 24 位携带有效载荷，通常是以微秒为单位的持续时间。

``include/nuttx/lirc.h`` 中的辅助函数用于构建和检查这些值：

- ``LIRC_PULSE(usec)``
- ``LIRC_SPACE(usec)``
- ``LIRC_FREQUENCY(value)``
- ``LIRC_TIMEOUT(usec)``
- ``LIRC_IS_PULSE(sample)``
- ``LIRC_IS_SPACE(sample)``
- ``LIRC_VALUE(sample)``

典型的原始传输数据如下：

.. code-block:: c

  unsigned int txbuf[] =
  {
    LIRC_PULSE(9000),
    LIRC_SPACE(4500),
    LIRC_PULSE(560),
    LIRC_SPACE(560),
    LIRC_PULSE(560),
  };

对于原始传输，``write()`` 期望奇数个 ``unsigned int`` 样本。上半部分将脉冲/间隔序列转发到下半部分的 ``tx_ir()`` 回调。

IOCTL 命令
==============

RC 上半部分支持 ``include/nuttx/lirc.h`` 中定义的标准 LIRC ``ioctl()`` 命令。常用命令包括：

- ``LIRC_GET_FEATURES``
- ``LIRC_GET_SEND_MODE``
- ``LIRC_GET_REC_MODE``
- ``LIRC_SET_SEND_MODE``
- ``LIRC_SET_REC_MODE``
- ``LIRC_GET_REC_RESOLUTION``
- ``LIRC_SET_SEND_CARRIER``
- ``LIRC_SET_SEND_DUTY_CYCLE``
- ``LIRC_SET_REC_TIMEOUT``

对特定命令的支持取决于下半部分的能力。在实践中，应用程序通常从查询 ``LIRC_GET_FEATURES`` 开始，然后仅使用设备通告的操作。

下半部分注册
=======================

平台代码通过填充 ``struct lirc_lowerhalf_s`` 并调用 ``lirc_register()`` 来注册 RC 下半部分。

.. code-block:: c

  int ret = lirc_register(lower, devno);

下半部分提供 ``struct lirc_ops_s`` 回调表。根据硬件情况，它可以实现 open/close 回调、通过 ``tx_ir()`` 的原始传输、通过 ``tx_scancode()`` 的扫描码传输、载波和占空比配置或接收超时处理。

测试
-------

``nuttx-apps/system/irtest`` 中的 ``irtest`` 应用程序可用于从 NSH 测试 RC 设备。典型的验证序列是：

#. 打开 ``/dev/lircN``
#. 查询 ``LIRC_GET_FEATURES``
#. 查询或设置发送/接收模式
#. 在具有传输能力的设备上写入原始 mode2 样本
#. 从具有接收能力的设备读回 mode2 样本

Espressif RMT LIRC 适配器
==========================

Espressif 目标可能提供基于 RMT 外设构建的架构本地 LIRC 适配器：

- ``arch/xtensa/src/common/espressif/esp_lirc.c``
- ``arch/risc-v/src/common/espressif/esp_lirc.c``

这些适配器通过 RC 框架将 RMT 外设暴露为 ``/dev/lircN`` 设备，同时将硬件特定的 RMT 实现保留在 Espressif 下半部分驱动程序中。
