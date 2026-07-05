============================
``ptpd`` PTP 守护进程命令
============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
========

``ptpd`` 应用程序为 NuttX 提供了完整的 IEEE 1588-2008 精密时间协议（PTPv2）实现。该守护进程支持在网络系统间进行亚微秒级时间同步，支持客户端（从时钟）和服务器（主时钟）两种模式。

PTP 守护进程可以将系统时钟同步到远程 PTP 主时钟，在使用软件时间戳时精度优于 1 微秒，在支持硬件时间戳时精度优于 500 纳秒。

特性
--------

- **IEEE 1588-2008 PTPv2 兼容** 的实现
- **双角色支持**：同时作为 PTP 主时钟和从时钟运行
- **多种传输选项**：

  - UDP over IPv4（默认）
  - UDP over IPv6
  - IEEE 802.3 以太网（第二层）

- **硬件时间戳** 支持以提高精度
- **PTP 时钟设备集成**，通过 ``/dev/ptp*`` 设备
- **BMCA（最佳主时钟算法）** 用于自动主时钟选择
- **两种延迟机制**：

  - 端到端（E2E）延迟测量
  - 对等（P2P）延迟测量

- **gPTP 支持**，带有交换机路径延迟校正
- **时钟漂移补偿**，带有自动频率调整
- **仅客户端模式**，用于专用从时钟操作

架构
============

ptpd 实现由两个主要组件组成：

上层（``netutils/ptpd/``）
---------------------------------

提供核心 PTP 协议实现：

- PTP 数据包编解码（Announce、Sync、Follow-Up、Delay_Req、Delay_Resp）
- BMCA（最佳主时钟算法）用于主时钟选择
- 时钟同步和调整算法
- 路径延迟测量和补偿
- 网络套接字管理（组播、单播）
- 硬件和软件时间戳支持

下层（``system/ptpd/``）
-------------------------------

提供命令行接口和守护进程管理：

- 命令行参数解析
- 配置管理
- 守护进程生命周期控制（启动、停止、状态）
- 状态报告和监控

配置选项
=====================

PTP 守护进程可通过 ``apps/netutils/ptpd/Kconfig`` 中的 Kconfig 选项进行配置。主要配置参数包括：

域和优先级
-------------------

``CONFIG_NETUTILS_PTPD_DOMAIN``（默认：0）
  PTP 域号（0-127）。在同一网络上隔离不同的 PTP 域。

``CONFIG_NETUTILS_PTPD_PRIORITY1``（默认：128）
  主优先级字段（0-255）。值越低，在 BMCA 中优先级越高。

``CONFIG_NETUTILS_PTPD_PRIORITY2``（默认：128）
  次优先级字段（0-255）。当 priority1 值相等时使用。

时钟质量
-------------

``CONFIG_NETUTILS_PTPD_CLASS``（默认：248）
  时钟等级值（0-255）：

  - 6：主参考源（如 GPS）
  - 13：应用特定时间源
  - 52：降级模式
  - 248：默认（未知）

``CONFIG_NETUTILS_PTPD_ACCURACY``（默认：254）
  时钟精度（对数刻度）：

  - 32：±25 ns
  - 35：±1 μs
  - 39：±100 μs
  - 41：±1 ms
  - 47：±1 s
  - 254：未知

``CONFIG_NETUTILS_PTPD_CLOCKSOURCE``（默认：160）
  时间源类型：

  - 32：GPS
  - 64：PTP
  - 80：NTP
  - 160：内部振荡器

时序参数
-----------------

``CONFIG_NETUTILS_PTPD_SYNC_INTERVAL_MSEC``（默认：1000）
  作为主时钟时 Sync 消息的发送间隔（毫秒）。

``CONFIG_NETUTILS_PTPD_ANNOUNCE_INTERVAL_MSEC``（默认：10000）
  作为主时钟时 Announce 消息的发送间隔（毫秒）。

``CONFIG_NETUTILS_PTPD_TIMEOUT_MS``（默认：60000）
  切换到备用时钟源的超时时间（毫秒）。

调整阈值
---------------------

``CONFIG_NETUTILS_PTPD_SETTIME_THRESHOLD_MS``（默认：1000）
  使用 ``settimeofday()`` 而非 ``adjtime()`` 的时钟偏移阈值。如果偏移超过此值，将使用步进方式而非渐进方式调整时间。

``CONFIG_NETUTILS_PTPD_ADJTIME_THRESHOLD_NS``（默认：500）
  使用当前 PPB 而非累积 PPB 来加速调整的阈值（纳秒）。

``CONFIG_NETUTILS_PTPD_DRIFT_AVERAGE_S``（默认：600）
  时钟漂移率的平均时间周期（秒，10-86400）。

路径延迟
----------

``CONFIG_NETUTILS_PTPD_MAX_PATH_DELAY_NS``（默认：100000）
  最大可接受的路径延迟（纳秒）。超过此值的延迟将被忽略。

``CONFIG_NETUTILS_PTPD_DELAYREQ_AVGCOUNT``（默认：100）
  路径延迟平均的采样数。

命令行接口
======================

使用方法
-------------

.. code-block:: console

   ptpd [options]

守护进程必须使用 ``&`` 运算符在后台模式运行。

选项
-------

**模式选择**

``-s``
  启用仅客户端模式（仅从时钟，无主时钟功能）

**网络传输**

``-2``
  使用 IEEE 802.3 以太网传输（第二层，原始套接字）

``-4``
  使用 UDP over IPv4（默认）

``-6``
  使用 UDP over IPv6

**时间戳**

``-H``
  使用硬件时间戳（如果启用了 ``CONFIG_NET_TIMESTAMP`` 则为默认）

``-S``
  使用软件时间戳（回退模式）

**协议选项**

``-B``
  启用最佳主时钟算法消息

``-E``
  使用端到端（E2E）延迟机制（支持 Delay_Req/Delay_Resp）

``-r``
  同步系统实时时钟（而非 PTP 时钟设备）

**设备配置**

``-i [device]``
  要使用的网络接口（如 ``eth0``、``eth1``）

``-p [device]``
  要使用的 PTP 时钟设备（如 ``ptp0``）。如果未指定，使用 ``realtime``。

**守护进程控制**

``-t [pid]``
  查询并显示运行中的 PTP 守护进程状态

``-d [pid]``
  停止指定 PID 的 PTP 守护进程

示例
========

启动为 PTP 客户端（从时钟）
----------------------------

使用 IPv4 UDP 的基本客户端同步：

.. code-block:: console

   nsh> ptpd -i eth0 &
   [PTP] Starting ptpd on interface eth0
   [PTP] Operating in client+server mode
   [PTP] Using software timestamps

使用硬件时间戳的仅客户端模式：

.. code-block:: console

   nsh> ptpd -s -H -i eth0 &
   [PTP] Starting ptpd on interface eth0
   [PTP] Client-only mode
   [PTP] Using hardware timestamps

启动为 PTP 主时钟（服务器）
-----------------------------

使用 BMCA 作为 PTP 主时钟：

.. code-block:: console

   nsh> ptpd -B -i eth0 &
   [PTP] Starting ptpd on interface eth0
   [PTP] BMCA enabled

第二层以太网传输
---------------------------

使用 IEEE 802.3 以太网传输用于 gPTP：

.. code-block:: console

   nsh> ptpd -2 -i eth0 &
   [PTP] Starting ptpd on interface eth0
   [PTP] Using Ethernet transport (raw socket)

PTP 时钟设备集成
-----------------------------

同步 PTP 硬件时钟而非系统时钟：

.. code-block:: console

   nsh> ptpd -i eth0 -p ptp0 &
   [PTP] Starting ptpd on interface eth0
   [PTP] Using PTP clock device /dev/ptp0

查询守护进程状态
-------------------

检查运行中守护进程的同步状态：

.. code-block:: console

   nsh> ptpd -t 42
   PTPD (PID 42) status:
   - clock_source_valid: 1
   |- id: 00 1a 2b 3c 4d 5e 6f 70
   |- utcoffset: 37
   |- priority1: 128
   |- class: 6
   |- accuracy: 32
   |- variance: 4321
   |- priority2: 128
   |- gm_id: 00 1a 2b 3c 4d 5e 6f 70
   |- stepsremoved: 0
   '- timesource: 32
   - last_clock_update: 2025-12-15T10:30:45.123456789
   - last_delta_ns: 234
   - last_adjtime_ns: -123
   - drift_ppb: 1234
   - path_delay_ns: 5678
   - last_received_multicast: 0 s ago
   - last_received_announce: 2 s ago
   - last_received_sync: 0 s ago

停止守护进程
-----------

停止运行中的 PTP 守护进程：

.. code-block:: console

   nsh> ptpd -d 42
   Stopped ptpd

状态信息
==================

使用 ``-t [pid]`` 查询状态时，将显示以下信息：

时钟源信息
------------------------

- **clock_source_valid**：是否已选择有效的 PTP 主时钟
- **id**：PTP 时钟标识（EUI-64 格式）
- **utcoffset**：TAI 和 UTC 之间的偏移（秒）
- **priority1/priority2**：BMCA 优先级字段
- **class**：时钟等级（6=GPS，13=应用，248=默认）
- **accuracy**：精度规格（32=±25ns，254=未知）
- **variance**：时钟方差估计
- **gm_id**：主时钟标识
- **stepsremoved**：距主时钟的跳数
- **timesource**：源类型（32=GPS，64=PTP，80=NTP，160=内部）

同步状态
-----------------------

- **last_clock_update**：上次时钟调整的时间戳
- **last_delta_ns**：最新测量的时钟偏移（纳秒）
- **last_adjtime_ns**：先前应用的调整偏移
- **drift_ppb**：平均时钟漂移率（十亿分之一）
- **path_delay_ns**：网络路径延迟估计（纳秒）

活动时间戳
-------------------

自上次接收/发送 PTP 消息以来的时间：

- **last_received_multicast**：任何 PTP 组播数据包
- **last_received_announce**：来自任何主时钟的 Announce 消息
- **last_received_sync**：来自选定主时钟的 Sync 消息
- **last_transmitted_sync**：Sync 消息（作为主时钟时）
- **last_transmitted_announce**：Announce 消息（作为主时钟时）
- **last_transmitted_delayresp**：延迟响应（作为主时钟时）
- **last_transmitted_delayreq**：延迟请求（作为从时钟时）

API 函数
=============

ptpd 库提供 C API 函数用于编程控制：

ptpd_start()
------------

.. code-block:: c

   int ptpd_start(FAR const struct ptpd_config_s *config);

使用指定配置启动 PTP 守护进程。

**参数：**

- ``config``：指向配置结构体的指针

**返回值：**

- 成功时不返回（作为守护进程运行）
- 错误时返回负的 errno 值

**配置结构体：**

.. code-block:: c

   struct ptpd_config_s
   {
     FAR const char *interface;  /* Network interface (e.g., "eth0") */
     FAR const char *clock;       /* Clock device (e.g., "ptp0", "realtime") */
     bool client_only;            /* Client-only mode flag */
     bool hardware_ts;            /* Hardware timestamping flag */
     bool delay_e2e;              /* E2E delay mechanism flag */
     bool bmca;                   /* BMCA enable flag */
     sa_family_t af;              /* Address family (AF_INET, AF_INET6, AF_PACKET) */
   };

ptpd_status()
-------------

.. code-block:: c

   int ptpd_status(pid_t pid, FAR struct ptpd_status_s *status);

查询运行中的 PTP 守护进程状态。

**参数：**

- ``pid``：ptpd 守护进程的进程 ID
- ``status``：指向要填充的状态结构体的指针

**返回值：**

- 成功时返回 ``OK``
- 错误时返回负的 errno 值

ptpd_stop()
-----------

.. code-block:: c

   int ptpd_stop(pid_t pid);

停止运行中的 PTP 守护进程。

**参数：**

- ``pid``：要停止的 ptpd 守护进程的进程 ID

**返回值：**

- 成功时返回 ``OK``
- 错误时返回负的 errno 值

实现细节
======================

同步算法
--------------------------

PTP 守护进程使用多阶段同步方法：

1. **时钟选择（BMCA）**

   - 评估所有主时钟的 Announce 消息
   - 根据优先级、等级、精度选择最佳时钟源
   - 当前主时钟超时时切换时钟源

2. **偏移测量**

   - 使用 Sync 和 Follow-Up 消息测量时钟偏移
   - 使用 Delay_Req/Delay_Resp 补偿网络路径延迟
   - 平均测量值以减少抖动

3. **时钟调整**

   - 小偏移（<1ms）：使用 ``adjtime()`` 进行平滑渐进调整
   - 大偏移（>1ms）：使用 ``settimeofday()`` 进行即时步进调整
   - 跟踪时钟漂移率并应用频率补偿

4. **路径延迟测量**

   - 持续测量往返网络延迟
   - 在可配置的采样数上取平均
   - 检测并拒绝异常值（>MAX_PATH_DELAY）

硬件时间戳
---------------------

当启用硬件时间戳时（``-H`` 选项）：

- TX 时间戳在数据包发送时由 MAC 层捕获
- RX 时间戳在数据包接收时由 MAC 层捕获
- 消除内核和网络栈处理延迟
- 实现亚微秒级同步精度

需要网络驱动程序支持：

- ``SO_TIMESTAMPNS`` 套接字选项
- ``recvmsg()`` 中的 ``MSG_TRUNC`` 标志
- ``SCM_TIMESTAMPNS`` 控制消息

PTP 时钟设备支持
-------------------------

当使用 PTP 时钟设备（``/dev/ptp*``）时：

- 同步硬件 PTP 时钟而非系统时钟
- 通过 CLOCKFD 机制使用 ``clock_adjtime()``
- 支持频率和相位调整
- 维护系统时间域和 PTP 时间域的分离

需要内核支持：

- NuttX 内核中的 ``CONFIG_PTP_CLOCK``
- PTP 时钟驱动程序实现
- ``CONFIG_CLOCK_ADJTIME`` 系统调用

传输模式
---------------

**UDP IPv4（默认）**

- 组播地址：224.0.1.129
- 事件端口：319，通用端口：320
- 防火墙友好，兼容路由器

**UDP IPv6**

- 组播地址：FF0E::181
- 与 IPv4 相同的端口号
- 仅 IPv6 网络支持

**IEEE 802.3 以太网**

- 组播 MAC：01:1B:19:00:00:00（PTP）或 01:80:C2:00:00:0E（gPTP）
- EtherType：0x88F7
- 无 IP/UDP 开销
- gPTP 合规所需

性能注意事项
==========================

同步精度
------------------------

可达到的典型精度：

- **软件时间戳**：10-100 μs
- **硬件时间戳**：100-500 ns
- **使用 PTP 时钟设备**：50-200 ns

影响精度的因素：

- 网络抖动和不对称性
- 中断延迟
- 时钟晶振质量
- 温度变化

CPU 和内存使用
--------------------

- **CPU 开销**：在 ARM Cortex-M4 @ 168MHz 上约 1-3%
- **内存占用**：约 45KB 代码，约 8KB RAM
- **网络带宽**：约 10-20 数据包/秒（典型）

网络要求
--------------------

- **组播支持**：PTP 运行所必需
- **IGMP**：IPv4 组播必须启用
- **交换机兼容性**：建议使用支持 PTP 的交换机以获得最佳效果
- **带宽**：最小（<100 Kbps）

故障排除
===============

常见问题
-------------

**无同步发生**

- 检查网络接口是否已启动并具有 IP 地址
- 验证组播路由已启用
- 确保防火墙允许 UDP 端口 319/320
- 检查 PTP 主时钟是否在同一网络/VLAN 上

**大时钟偏移**

- 验证网络路径延迟合理（典型 <100μs）
- 检查网络延迟是否不对称
- 如果可用，启用硬件时间戳
- 检查 BMCA 优先级设置

**频繁切换主时钟**

- 增加 ``CONFIG_NETUTILS_PTPD_TIMEOUT_MS``
- 检查网络稳定性和丢包率
- 验证所有主时钟具有唯一的时钟标识

**高 CPU 使用率**

- 增加同步间隔（``CONFIG_NETUTILS_PTPD_SYNC_INTERVAL_MSEC``）
- 使用硬件时间戳以减少处理
- 检查是否有过多的数据包错误/重试

调试输出
------------

在内核配置中启用 PTP 调试消息：

- ``CONFIG_DEBUG_PTP_ERROR``：错误消息
- ``CONFIG_DEBUG_PTP_WARN``：警告消息
- ``CONFIG_DEBUG_PTP_INFO``：信息性消息

监控调试输出：

.. code-block:: console

   nsh> dmesg | grep PTP

相关文档
=====================

- :doc:`/components/drivers/special/ptp` - PTP 时钟驱动程序框架
- :doc:`/applications/netutils/index` - 网络工具概述
- IEEE 1588-2008 标准 - 精密时间协议规范
- IEEE 802.1AS 标准 - 时间敏感应用的定时和同步（gPTP）

参考文献
==========

- IEEE 1588-2008："IEEE Standard for a Precision Clock Synchronization Protocol for Networked Measurement and Control Systems"
- IEEE 802.1AS-2020："IEEE Standard for Local and Metropolitan Area Networks - Timing and Synchronization for Time-Sensitive Applications"
- Linux PTP Project: https://linuxptp.sourceforge.net/
- ``apps/netutils/ptpd/`` - PTP 协议实现
- ``apps/system/ptpd/`` - PTP 守护进程命令接口
- ``include/netutils/ptpd.h`` - PTP API 头文件
