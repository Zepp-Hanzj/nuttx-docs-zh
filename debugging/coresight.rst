======================================
Coresight - ARM 硬件辅助追踪
======================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
--------

Coresight 是一组允许调试基于 ARM 的 SoC 的技术总称。它包括 JTAG 和硬件辅助追踪的解决方案。本文档关注后者。

在处理包含多个 SoC 以及 GPU 和 DMA 引擎等其他组件的系统时，硬件辅助追踪变得越来越有用。开发者可以监控软件在设备上运行时的行为，查看其实时执行数据，并快速识别和调试问题。

Coresight 组件通常分为源、链路和接收器三类。源设备根据追踪场景生成表示处理器指令路径的压缩流。链路设备负责将数据流从源设备传输到接收器设备。接收器设备作为 coresight 实现的端点，将压缩流存储在内存缓冲区中，或创建一个与外部通信的接口，以便将数据传输到主机而不用担心填满板载 coresight 内存缓冲区。

更多详情请参考以下文档：
https://developer.arm.com/documentation/102520/latest/


缩写与分类
---------------------------

缩写：

PTM:
    Program Trace Macrocell（程序追踪宏单元）
ETM:
    Embedded Trace Macrocell（嵌入式追踪宏单元）
STM:
    System trace Macrocell（系统追踪宏单元）
ETB:
    Embedded Trace Buffer（嵌入式追踪缓冲区）
ITM:
    Instrumentation Trace Macrocell（仪器追踪宏单元）
TPIU:
     Trace Port Interface Unit（追踪端口接口单元）
TMC-ETR:
        Trace Memory Controller, configured as Embedded Trace Router（追踪内存控制器，配置为嵌入式追踪路由器）
TMC-ETF:
        Trace Memory Controller, configured as Embedded Trace FIFO（追踪内存控制器，配置为嵌入式追踪 FIFO）

分类：

源（Source）:
   ETM, STM, ITM
链路（Link）:
   Funnel, replicator, TMC-ETF
接收器（Sinks）:
   ETB, TPIU, TMC-ETR

框架与实现
----------------------------

coresight 框架提供了一个中心点来表示、配置和管理平台上的 coresight 设备。任何 coresight 兼容设备都可以注册到框架中，只要它们使用正确的 API：

.. c:function:: int coresight_register(FAR struct coresight_dev_s *csdev, FAR const struct coresight_desc_s *desc);
.. c:function:: void coresight_unregister(FAR struct coresight_dev_s *csdev);

``struct coresight_desc *desc`` 描述当前 coresight 设备的类型及其连接位置。当所有 coresight 设备注册完成后，可以通过调用以下函数启用追踪流路径上的设备：

.. c:function:: int coresight_enable(FAR struct coresight_dev_s *srcdev, FAR struct coresight_dev_s *destdev);

``coresight_enable`` 函数将根据 ``struct coresight_desc *desc`` 构建从 srcdev 到 destdev 的路径。
