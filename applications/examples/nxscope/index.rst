===================================
``nxscope`` NxScope 库示例
===================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``nxscope`` 示例演示了 NxScope 库的基本用法，用于实时数据流传输。

有关 NxScope 库和主机端工具的更多详情，请参见 :doc:`/applications/logging/nxscope/index`。

此应用程序初始化一组示例通道，并启动一个线程生成各种波形（正弦波、计数器等），
以便流式传输到主机客户端。

配置
=============

要使用此示例，请启用 ``CONFIG_EXAMPLES_NXSCOPE=y``。可用的配置选项
取决于 ``nxscope`` 配置中选择的接口。

通用选项
--------------

- ``CONFIG_EXAMPLES_NXSCOPE_STREAMBUF_LEN``：NxScope 流缓冲区大小。
- ``CONFIG_EXAMPLES_NXSCOPE_RXBUF_LEN``：NxScope 接收缓冲区大小。
- ``CONFIG_EXAMPLES_NXSCOPE_MAIN_INTERVAL``：主循环间隔（微秒）。
- ``CONFIG_EXAMPLES_NXSCOPE_FORCE_ENABLE``：启动时自动启用所有通道并开始流式传输。
- ``CONFIG_EXAMPLES_NXSCOPE_CHARLOG``：演示通过专用通道（通道 19）发送文本消息。

串行接口选项
------------------------

当 ``CONFIG_LOGGING_NXSCOPE_INTF_SERIAL=y`` 时可用以下选项：

- ``CONFIG_EXAMPLES_NXSCOPE_SERIAL_PATH``：设备路径（例如 ``/dev/ttyUSB0``）。
- ``CONFIG_EXAMPLES_NXSCOPE_SERIAL_BAUD``：串行接口的波特率。
- ``CONFIG_EXAMPLES_NXSCOPE_CDCACM``：启用 USB CDC/ACM 串行传输支持。

UDP 接口选项
---------------------

当 ``CONFIG_LOGGING_NXSCOPE_INTF_UDP=y`` 时可用以下选项：

- ``CONFIG_EXAMPLES_NXSCOPE_UDP_PORT``：NxScope 接口的本地 UDP 端口。

定时器选项
-------------

当 ``CONFIG_EXAMPLES_NXSCOPE_TIMER=y`` 时可用以下选项：

- ``CONFIG_EXAMPLES_NXSCOPE_TIMER_PATH``：硬件定时器的设备路径。
- ``CONFIG_EXAMPLES_NXSCOPE_TIMER_INTERVAL``：定时器间隔（微秒）。
- ``CONFIG_EXAMPLES_NXSCOPE_TIMER_SIGNO``：定时器通知的信号编号。

命令行参数
======================

该示例接受以下命令行参数：

- ``-i <stream_interval_us>``：数据采样线程间隔（微秒）。
  覆盖默认值（如果使用定时器则为 ``CONFIG_EXAMPLES_NXSCOPE_TIMER_INTERVAL``，否则为 100us）。
- ``-m <main_interval_us>``：主循环间隔（微秒）。
  覆盖默认值（``CONFIG_EXAMPLES_NXSCOPE_MAIN_INTERVAL``）。

支持的通道
==================

该示例初始化 32 个通道来演示不同的数据类型和功能：

- **通道 0-7**：标准整数类型（uint8 到 int64）。
- **通道 8-9**：浮点类型（float 和 double）。
- **通道 10-15**：定点类型（b8、b16、b32）。
- **通道 16**：浮点向量（3 相正弦波形）。
- **通道 17**：带元数据的浮点向量。
- **通道 18**：带元数据的无数据通道。
- **通道 19**：用于文本日志的字符通道（如果启用）。
- **通道 20**：关键通道（如果启用）。
