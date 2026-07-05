==========================
``modbus`` FreeModBus 移植
==========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此目录包含 FreeModBus 最后一个开源版本（BSD 许可证）的移植。
此目录中的代码是 FreeModBus 1.5.0 版本（2010 年 6 月 6 日）的子集，
完整版本可从 http://developer.berlios.de/project/showfiles.php?group_id=6120 下载。

包含 Armink(383016632@qq.com) 对 RTU 主站模式支持的扩展：
https://github.com/armink/FreeModbus_Slave-Master-RTT-STM32。由 Darcy Gong 移植到 NuttX。

目录结构 / 与 freemodbus-v1.5.0 的关系
---------------------------------------------------

原始 FreeModBus 下载包含多个目录。此子集仅获取一个目录 ``modbus/`` 的内容，
该目录实现核心 modbus 逻辑并将该目录集成到 NuttX 构建系统中。
``freemodbus-v1.5.0`` 与 nuttx 目录之间的映射如下所示::

  --------------------------- ----------------------------------------------
  freemodbus-v1.5.0           NuttX
  --------------------------- ----------------------------------------------
   All top level .txt files    Not included
   demo/                       Not included. This directory contains demo
                               and porting code for a variety of platforms.
                               The NuttX demo was ported from the LINUX
                               demo in this directory and can be found at
                               apps/examples/modbus.
   doc/                        Not included. This directory contains Doxygen
                               support files.
   modbus/                     Included in its entirety in various locations:
           ascii                  apps/modbus/ascii
           functions              apps/modbus/functions
           include                apps/include/modbus
           mb.c                   apps/modbus/mb.c
           rtu                    apps/modbus/rtu
           tcp                    apps/modbus/tcp
   tools/                      Not included. This directory contains Doxygen
                               tools.
  --------------------------- ----------------------------------------------

因此，此目录等同于 ``freemodbus-v1.5.0/modbus`` 目录，不同之处在于
（1）它可能包含为与 NuttX 集成而做的修改，以及
（2）modbus/include 目录已移至 ``apps/modbus``。

原始的、未修改的 ``freemodbus-v1.5.0`` 作为 SVN 版本 ``4960`` 提交。

此处的另一个目录 ``nuttx/`` 实现 NuttX modbus 接口。
它源自 ``freemodbus-v1.5.0/demo/LINUX/port`` 目录。

配置选项
---------------------

在原始 ``freemodbus-v1.5.0`` 发布中，FreeModBus 配置由头文件 ``mbconfig.h`` 控制。
此头文件已被取消（版本 ``4960`` 之后），FreeModBus 配置已集成到 NuttX 配置系统中。

可用的 NuttX 命名配置选项包括：

- ``CONFIG_MODBUS`` – 通用 ModBus 支持。
- ``CONFIG_MB_ASCII_ENABLED`` – Modbus ASCII 支持。
- ``CONFIG_MB_ASCII_MASTER`` – Modbus ASCII 主站支持。
- ``CONFIG_MB_RTU_ENABLED`` – Modbus RTU 支持。
- ``CONFIG_MB_RTU_MASTER`` – Modbus RTU 主站支持。
- ``CONFIG_MB_TCP_ENABLED`` – Modbus TCP 支持。
- ``CONFIG_MB_ASCII_TIMEOUT_SEC`` – Modbus ASCII 的字符超时值。
  Modbus ASCII 的字符超时值不是固定的，因此是一个配置选项。
  应将其设置为网络的预期最大延迟时间。默认：``1``。
- ``CONFIG_MB_ASCII_TIMEOUT_WAIT_BEFORE_SEND_MS`` – 在 ASCII 中启用发射器之前的等待超时。
  如果定义了此选项，函数将以参数 ``CONFIG_MB_ASCII_TIMEOUT_WAIT_BEFORE_SEND_MS`` 调用
  ``vMBPortSerialDelay``，以允许在启用串行发射器之前进行延迟。
  这是必需的，因为某些目标速度太快，在接收和发送帧之间没有时间。
  如果主站启用接收器太慢，它将无法正确接收响应。
- ``CONFIG_MB_FUNC_HANDLERS_MAX`` – 协议栈应支持的最大 Modbus 功能码数量。
  支持的最大 Modbus 函数数必须大于此文件中所有已启用函数和自定义函数处理器的总和。
  如果设置太小，添加更多函数将失败。
- ``CONFIG_MB_FUNC_OTHER_REP_SLAVEID_BUF`` – 应为 Report Slave ID 命令分配的字节数。
  此数字限制了 report slave id 函数中附加段的最大大小。
  有关如何设置此值的更多信息，请参阅 ``eMBSetSlaveID()``。
  仅在 ``CONFIG_MB_FUNC_OTHER_REP_SLAVEID_ENABLED`` 设置为 ``1`` 时使用。
- ``CONFIG_MB_FUNC_OTHER_REP_SLAVEID_ENABLED`` – 是否应启用 Report Slave ID 函数。
- ``CONFIG_MB_FUNC_READ_INPUT_ENABLED`` – 是否应启用 Read Input Registers 函数。
- ``CONFIG_MB_FUNC_READ_HOLDING_ENABLED`` – 是否应启用 Read Holding Registers 函数。
- ``CONFIG_MB_FUNC_WRITE_HOLDING_ENABLED`` – 是否应启用 Write Single Register 函数。
- ``CONFIG_MB_FUNC_WRITE_MULTIPLE_HOLDING_ENABLED`` – 是否应启用 Write Multiple registers 函数。
- ``CONFIG_MB_FUNC_READ_COILS_ENABLED`` – 是否应启用 Read Coils 函数。
- ``CONFIG_MB_FUNC_WRITE_COIL_ENABLED`` – 是否应启用 Write Coils 函数。
- ``CONFIG_MB_FUNC_WRITE_MULTIPLE_COILS_ENABLED`` – 是否应启用 Write Multiple Coils 函数。
- ``CONFIG_MB_FUNC_READ_DISCRETE_INPUTS_ENABLED`` – 是否应启用 Read Discrete Inputs 函数。
- ``CONFIG_MB_FUNC_READWRITE_HOLDING_ENABLED`` – 是否应启用 Read/Write Multiple Registers 函数。

另请参阅其他串行设置，特别是：

- ``CONFIG_SERIAL_TERMIOS`` – 串行驱动程序支持 ``termios.h`` 接口。
  如果未定义，则终端设置（波特率、奇偶校验等）在运行时不可配置。

注意事项
----

FreeModBus 的开发者 Christian Walter 仍在开发 Modbus 库，尽管它们现在是商业的。
有关更多信息，请参阅 http://www.embedded-solutions.at/。
