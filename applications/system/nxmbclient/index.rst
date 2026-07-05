===================================
``nxmbclient`` NxModbus 客户端工具
===================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``nxmbclient`` 命令行工具提供了一种便捷的方式，从 NuttX shell 执行 Modbus
客户端（主站）操作。它支持 RTU、ASCII 和 TCP 传输，并提供完整的命令行配置。

支持的命令
==================

读操作：

- ``read-coils ADDR COUNT`` – 读取线圈状态 (FC01)
- ``read-discrete ADDR COUNT`` – 读取离散输入状态 (FC02)
- ``read-input ADDR COUNT`` – 读取输入寄存器 (FC04)
- ``read-holding ADDR COUNT`` – 读取保持寄存器 (FC03)

写操作：

- ``write-coil ADDR VALUE`` – 写单个线圈 (FC05)
- ``write-holding ADDR VALUE`` – 写单个保持寄存器 (FC06)
- ``write-coils ADDR VALUE...`` – 写多个线圈 (FC15)
- ``write-holdings ADDR VALUE...`` – 写多个保持寄存器 (FC16)

命令行选项
====================

传输选择（必需）：

- ``-t TYPE`` – 传输类型：``rtu``、``ascii`` 或 ``tcp``

串口传输选项（RTU/ASCII）：

- ``-d DEVICE`` – 串口设备路径（例如 ``/dev/ttyS1``）
- ``-b BAUD`` – 波特率（默认：115200）
- ``-p PARITY`` – 校验位：``none``、``even`` 或 ``odd``（默认：none）

TCP 传输选项：

- ``-h HOST`` – TCP 主机地址（例如 ``192.168.1.100``）
- ``-P PORT`` – TCP 端口（默认：502）

Modbus 选项：

- ``-u UNIT`` – 单元 ID / 从站地址（默认：1）
- ``-T TIMEOUT`` – 超时时间，单位毫秒（默认：1000）
- ``--poll MS`` – 轮询间隔，单位毫秒（0 = 单次模式）

用法示例
==============

RTU 客户端 - 读取保持寄存器::

    nsh> nxmbclient -t rtu -d /dev/ttyS1 -b 115200 read-holding 0 10
    从地址 0 读取 10 个保持寄存器：
    [0]: 0x0000
    [1]: 0x0064
    [2]: 0x00C8
    ...

TCP 客户端 - 写单个寄存器::

    nsh> nxmbclient -t tcp -h 192.168.1.100 -P 502 write-holding 0 1234
    写入地址 0 的保持寄存器：1234

RTU 客户端 - 持续轮询::

    nsh> nxmbclient -t rtu -d /dev/ttyS1 --poll 1000 read-holding 0 5
    从地址 0 读取 5 个保持寄存器：
    [0]: 0x0000
    [1]: 0x0064
    [2]: 0x00C8
    [3]: 0x012C
    [4]: 0x0190
    
    （每 1000ms 重复一次，直到 Ctrl+C）

ASCII 客户端 - 写多个线圈::

    nsh> nxmbclient -t ascii -d /dev/ttyS1 -b 9600 -p even write-coils 0 1 0 1 1
    从地址 0 开始写入 5 个线圈

配置
=============

在 NuttX 配置中启用该工具::

    CONFIG_SYSTEM_NXMBCLIENT=y
    CONFIG_INDUSTRY_NXMODBUS=y
    CONFIG_NXMODBUS_RTU=y      # 用于 RTU 支持
    CONFIG_NXMODBUS_ASCII=y    # 用于 ASCII 支持
    CONFIG_NXMODBUS_TCP=y      # 用于 TCP 支持

Kconfig 选项：

- ``CONFIG_SYSTEM_NXMBCLIENT`` – 启用 nxmbclient 工具
- ``CONFIG_INDUSTRY_NXMBCLIENT_PROGNAME`` – 程序名称（默认："nxmbclient"）
- ``CONFIG_NXMBCLIENT_PRIORITY`` – 任务优先级（默认：100）
- ``CONFIG_NXMBCLIENT_STACKSIZE`` – 栈大小（默认：DEFAULT_TASK_STACKSIZE）

另请参阅
========

- :doc:`/applications/industry/nxmodbus/index` – NxModbus 协议栈
- :doc:`/applications/examples/nxmbserver/index` – NxModbus 服务器示例
