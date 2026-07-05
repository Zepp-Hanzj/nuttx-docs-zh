===============
NxScope Library
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NxScope 通过将采样数据缓冲到最多 255 个虚拟通道（向量、点或文本数据），
并通过自定义协议和接口进行流式传输，提供实时数据记录功能。它支持通过命令进行
远程控制、时间戳、采样率分频器以及关键的非缓冲通道。

应用场景
=========

- 实时传感器数据流传输和可视化。
- 控制系统遥测（PID 调参、状态监测）。
- 高频信号捕获（ADC）。
- 远程调试和实时变量跟踪。

配置选项
=============

- ``CONFIG_LOGGING_NXSCOPE_INTF_SERIAL`` – 串口接口
- ``CONFIG_LOGGING_NXSCOPE_INTF_UDP`` – UDP 接口（基于以太网）
- ``CONFIG_LOGGING_NXSCOPE_INTF_DUMMY`` – 虚拟接口（用于调试）
- ``CONFIG_LOGGING_NXSCOPE_PROTO_SER`` – 默认串口协议（CRC-16）
- ``CONFIG_LOGGING_NXSCOPE_DIVIDER`` – 采样率分频器支持
- ``CONFIG_LOGGING_NXSCOPE_ACKFRAMES`` – 设置请求的 ACK 帧
- ``CONFIG_LOGGING_NXSCOPE_USERTYPES`` – 用户自定义帧支持
- ``CONFIG_LOGGING_NXSCOPE_CRICHANNELS`` – 非缓冲通道支持

实现
==============

- 串口接口：``apps/logging/nxscope/nxscope_iser.c``
- UDP 接口：``apps/logging/nxscope/nxscope_iudp.c``
- 虚拟接口：``apps/logging/nxscope/nxscope_idummy.c``
- 默认串口协议：``apps/logging/nxscope/nxscope_pser.c``

串口协议
---------------

默认串口协议（``nxscope_pser.c``）使用一种简单的帧格式，包含头部、数据载荷和
CRC-16 尾部。

帧格式
~~~~~~~~~~~~

+----------+-----------+-----------+------------+-------------+
| SOF (1B) | Len (2B)  | ID (1B)   | Data (nB)  | CRC-16 (2B) |
+==========+===========+===========+============+=============+
| ``0x55`` | u16 (LE)  | u8        | ...        | u16 (BE)    |
+----------+-----------+-----------+------------+-------------+

- **SOF**：帧起始标志，始终为 ``0x55``。
- **Len**：总帧长度（包含头部和尾部），小端序。
- **ID**：帧类型标识符（参见 ``enum nxscope_hdr_id_e``）。
- **Data**：可变长度数据载荷。
- **CRC-16**：头部和数据的 CRC-16-XMODEM（多项式 ``0x1021``）。

帧类型
~~~~~~~~~~~

``enum nxscope_hdr_id_e`` 中定义了以下帧类型：

+----------------------------+----+--------------------------------------------+
| 类型                       | ID | 描述                                       |
+============================+====+============================================+
| ``NXSCOPE_HDRID_STREAM``   | 1  | 实时流数据                                 |
+----------------------------+----+--------------------------------------------+
| ``NXSCOPE_HDRID_CMNINFO``  | 2  | 获取通用信息（chmax、flags、padding）      |
+----------------------------+----+--------------------------------------------+
| ``NXSCOPE_HDRID_CHINFO``   | 3  | 获取通道信息（名称、类型等）               |
+----------------------------+----+--------------------------------------------+
| ``NXSCOPE_HDRID_ACK``      | 4  | 设置请求的 ACK/NACK 响应                   |
+----------------------------+----+--------------------------------------------+
| ``NXSCOPE_HDRID_START``    | 5  | 启动或停止数据流                           |
+----------------------------+----+--------------------------------------------+
| ``NXSCOPE_HDRID_ENABLE``   | 6  | 启用或禁用特定通道                         |
+----------------------------+----+--------------------------------------------+
| ``NXSCOPE_HDRID_DIV``      | 7  | 设置通道的采样分频器                       |
+----------------------------+----+--------------------------------------------+
| ``NXSCOPE_HDRID_USER``     | 8  | 用户自定义帧                               |
+----------------------------+----+--------------------------------------------+

示例
========

以下 NuttX 应用程序演示了 NxScope 库的使用：

1. :doc:`../../examples/nxscope/index` - 基本流式传输示例。

2. :doc:`../../industry/foc/index` - 实时 FOC（磁场定向控制）遥测。

3. :doc:`../../system/adcscope/index` - ADC 数据可视化。

4. :doc:`../../system/sensorscope/index` - 传感器数据流传输。

支持的板卡
================

NuttX 中的多个板卡配置使用了 NxScope 库：

- **nrf52832-dk:nxscope_rtt**：使用 Segger RTT 作为传输接口。
  无需物理 UART 或 USB 线缆即可实现高速数据流传输（需要 J-Link 调试器）。

- **nrf52832-dk:nxscope_uart**：使用物理 UART 接口，高波特率（1Mbps）
  进行数据流传输。

- **stm32f4discovery:nxscope_cdcacm**：使用 USB CDC/ACM 作为传输接口，
  通过 USB 提供标准串口连接。

- **qemu-intel64:jumbo**：使用 UDP 接口，通过模拟以太网连接进行高速数据流传输。

- **thingy53:sensors_cpuapp**：使用 USB CDC/ACM 配合 :doc:`sensorscope
  <../../system/sensorscope/index>` 应用程序，从板载传感器流式传输数据。

- **sim:nxscope**：NuttX 模拟器的配置，可在主机 PC 上方便地测试和开发
  NxScope 相关功能。

- **nucleo-c071rb:adcscope**：使用 UART 和 ST-LINK VCOM 配合
  :doc:`adcscope <../../system/adcscope/index>` 应用程序，从 ADC 通道
  流式传输数据。

外部工具
==============

- `Nxslib <https://github.com/railab/nxslib>`_ - Python 客户端库。

- `Nxscli <https://github.com/railab/nxscli>`_ - 核心命令行界面。

- `Nxscli-mpl <https://github.com/railab/nxscli-mpl>`_ - nxscli 的 Matplotlib
  扩展。

- `Nxscli-pqg <https://github.com/railab/nxscli-pqg>`_ - nxscli 的 PyQtGraph
  扩展。

Nxscli 快速入门
------------------

`Nxscli <https://github.com/railab/nxscli>`_ 是一个 Python 工具，用于与
支持 NxScope 的设备进行交互。它使用基于插件的架构来捕获、存储和可视化数据。

.. note::
   这只是一个快速命令参考。有关所有支持的功能、插件和配置选项的详细描述，
   请访问官方仓库。

.. note::
   ``nxscli`` 的图形用户界面（GUI）目前正在开发中，即将推出。

1. **安装**：

   .. code-block:: bash

      # 核心工具
      pip install nxscli

      # Matplotlib 扩展（可选）
      pip install nxscli-mpl

      # PyQtGraph 扩展（可选）
      pip install nxscli-pqg

2. **接口选择**：

   选择连接设备的接口：

   .. code-block:: bash

      # 串口
      nxscli serial <serial-port> ...

      # Segger RTT
      nxscli rtt <rtt-target> <rtt-buffer-index> <rtt-buffer-size>...

      # UDP（以太网）
      nxscli udp <target-ip> <target-port> ...

      # 模拟/虚拟接口
      nxscli dummy ...

3. **设备信息**：

   显示已连接 NxScope 设备及其可用通道的信息：

   .. code-block:: bash

      # 串口接口
      nxscli serial /dev/ttyACM0 pdevinfo

4. **数据捕获**：

   配置通道并捕获采样数据：

   .. code-block:: bash

      # 通过串口打印通道 0 和 1 的采样数据
      nxscli serial /dev/ttyACM0 chan 0,1 pprinter

5. **可视化**：

   NxScope 支持使用 Matplotlib 或 PyQtGraph 进行实时可视化：

   .. code-block:: bash

      # 使用 Matplotlib 从串口进行实时绘图
      nxscli serial /dev/ttyACM0 chan 0,1 m_live

      # 使用 PyQtGraph 从串口进行实时绘图
      nxscli serial /dev/ttyACM0 chan 0,1 q_live

6. **数据流传输**：

   通过 UDP 流式传输数据（例如，传输到 PlotJuggler）：

   .. code-block:: bash

      nxscli serial /dev/ttyACM0 chan 0,1 pudp 0
