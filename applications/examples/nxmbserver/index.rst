======================================
``nxmbserver`` NxModbus 服务器示例
======================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``nxmbserver`` 示例演示了如何使用 NxModbus 协议栈创建 Modbus 服务器（从站）。
它支持 RTU、ASCII 和 TCP 传输以及模拟寄存器数据。

寄存器映射
============

示例服务器提供以下模拟寄存器：

线圈（读/写，FC01/FC05/FC15）：

- 地址范围：1-100
- 初始状态：全零
- 可通过 FC05（写单个）和 FC15（写多个）进行写入

离散输入（只读，FC02）：

- 地址范围：1-100
- 初始状态：全零
- 只读（不能被客户端修改）

输入寄存器（只读，FC04）：

- 地址范围：1-100
- 初始值：``register[i] = i * 10``（寄存器 1 = 10，寄存器 2 = 20，寄存器 10 = 100）

保持寄存器（读/写，FC03/FC06/FC16/FC23）：

- 地址范围：1-100
- 初始值：``register[i] = i * 100``（寄存器 1 = 100，寄存器 2 = 200，寄存器 10 = 1000）
- 可通过 FC06（写单个）、FC16（写多个）、FC23（读/写）进行写入

命令行选项
====================

传输选择（必需）：

- ``-t TYPE`` – 传输类型：``rtu``、``ascii`` 或 ``tcp``

串行传输选项（RTU/ASCII）：

- ``-d DEVICE`` – 串行设备路径（例如 ``/dev/ttyS1``）
- ``-b BAUD`` – 波特率（默认：115200）
- ``-p PARITY`` – 校验：``none``、``even`` 或 ``odd``（默认：none）

TCP 传输选项：

- ``-a ADDR`` – 绑定地址（默认：0.0.0.0 – 所有接口）
- ``-P PORT`` – TCP 端口（默认：502）

Modbus 选项：

- ``-u UNIT`` – 单元 ID / 从站地址（默认：1）

用法示例
==============

串口上的 RTU 服务器::

    nsh> nxmbserver -t rtu -d /dev/ttyS1 -b 115200
    Starting Modbus RTU server on /dev/ttyS1 (baud=115200, unit=1)
    Server running. Press Ctrl+C to stop.
    Register map:
      Coils:          1-100 (read/write)
      Discrete:       1-100 (read-only)
      Input regs:     1-100 (read-only, value=addr*10)
      Holding regs:   1-100 (read/write, initial=addr*100)

默认端口上的 TCP 服务器::

    nsh> nxmbserver -t tcp -P 502
    Starting Modbus TCP server on port 502 (unit=1)
    Server running. Press Ctrl+C to stop.
    Register map:
      Coils:          1-100 (read/write)
      Discrete:       1-100 (read-only)
      Input regs:     1-100 (read-only, value=addr*10)
      Holding regs:   1-100 (read/write, initial=addr*100)

偶校验的 ASCII 服务器::

    nsh> nxmbserver -t ascii -d /dev/ttyS1 -b 9600 -p even -u 5
    Starting Modbus ASCII server on /dev/ttyS1 (baud=9600, unit=5)
    Server running. Press Ctrl+C to stop.
    ...

使用 nxmbclient 进行测试
=======================

可以使用 ``nxmbclient`` 工具对服务器进行测试：

读取输入寄存器（初始值）::

    nsh> nxmbclient -t tcp -h 127.0.0.1 read-input 1 5
    Read 5 input registers from address 1:
    [1]: 10
    [2]: 20
    [3]: 30
    [4]: 40
    [5]: 50

读取保持寄存器（初始值）::

    nsh> nxmbclient -t tcp -h 127.0.0.1 read-holding 1 5
    Read 5 holding registers from address 1:
    [1]: 100
    [2]: 200
    [3]: 300
    [4]: 400
    [5]: 500

写入并回读保持寄存器::

    nsh> nxmbclient -t tcp -h 127.0.0.1 write-holding 10 9999
    Wrote holding register at address 10: 9999
    
    nsh> nxmbclient -t tcp -h 127.0.0.1 read-holding 10 1
    Read 1 holding register from address 10:
    [10]: 9999

配置
=============

在 NuttX 配置中启用该示例::

    CONFIG_EXAMPLES_NXMBSERVER=y
    CONFIG_INDUSTRY_NXMODBUS=y
    CONFIG_NXMODBUS_RTU=y      # For RTU support
    CONFIG_NXMODBUS_ASCII=y    # For ASCII support
    CONFIG_NXMODBUS_TCP=y      # For TCP support

Kconfig 选项：

- ``CONFIG_EXAMPLES_NXMBSERVER`` – 启用 nxmbserver 示例
- ``CONFIG_EXAMPLES_NXMBSERVER_PROGNAME`` – 程序名称（默认："nxmbserver"）
- ``CONFIG_EXAMPLES_NXMBSERVER_PRIORITY`` – 任务优先级（默认：100）
- ``CONFIG_EXAMPLES_NXMBSERVER_STACKSIZE`` – 堆栈大小（默认：DEFAULT_TASK_STACKSIZE）

另请参见
========

- :doc:`/applications/industry/nxmodbus/index` – NxModbus 协议栈
- :doc:`/applications/system/nxmbclient/index` – NxModbus 客户端工具
