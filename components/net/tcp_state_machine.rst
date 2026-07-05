=============================
NuttX TCP 状态机说明
=============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本文档描述了当前 NuttX TCP 协议栈如何实现 TCP 状态转换。
它基于树内实现（主要在 ``net/tcp`` 中），侧重于*代码当前的行为*，
而非通用的 RFC 793 描述。

范围
=====

* TCP 连接状态按 ``struct tcp_conn_s`` 跟踪。
* 状态转换主要发生在：

\t* ``net/tcp/tcp_input.c``（传入段和大多数转换）
\t* ``net/tcp/tcp_timer.c``（超时和重传）
\t* ``net/tcp/tcp_conn.c``（连接/监听端分配和初始状态）
\t* ``net/tcp/tcp_close.c``（主动关闭发起）

状态表示
====================

NuttX 将 TCP 状态存储在 ``tcp_conn_s::tcpstateflags`` 中。

* 位 0-3 为状态（``TCP_STATE_MASK``）。
* 位 4 是一个标志（``TCP_STOPPED``），由套接字层用于停止数据流。

状态值定义在 ``include/nuttx/net/tcp.h`` 中：

* ``TCP_CLOSED``
* ``TCP_ALLOCATED``（NuttX 内部：已分配但尚未连接）
* ``TCP_SYN_RCVD``
* ``TCP_SYN_SENT``
* ``TCP_ESTABLISHED``
* ``TCP_FIN_WAIT_1``
* ``TCP_FIN_WAIT_2``
* ``TCP_CLOSE_WAIT``
* ``TCP_CLOSING``
* ``TCP_TIME_WAIT``
* ``TCP_LAST_ACK``
* ``TCP_STOPPED``

支持与不支持（RFC 状态视图）
=========================================

NuttX 基本遵循经典的 TCP 状态机，下表将传统 RFC 793 状态名称
映射到 NuttX 中现有的内容。

.. list-table:: RFC TCP 状态及其 NuttX 支持
\t :header-rows: 1
\t :widths: auto

\t * - RFC 状态名称
\t\t - NuttX 表示
\t\t - 是否支持
\t\t - 备注
\t * - CLOSED
\t\t - ``TCP_CLOSED``
\t\t - 是
\t\t - 连接未使用/可用。
\t * - LISTEN
\t\t - 无 ``tcpstateflags`` 状态
\t\t - 部分
\t\t - 监听通过 ``net/tcp/tcp_listen.c`` 中的监听器表（``tcp_listenports[]``）实现，
       而非每连接的 LISTEN 状态。
\t * - SYN-SENT
\t\t - ``TCP_SYN_SENT``
\t\t - 是
\t\t - 由 ``net/tcp/tcp_conn.c`` 中的 ``tcp_connect()`` 设置。
\t * - SYN-RECEIVED
\t\t - ``TCP_SYN_RCVD``
\t\t - 是
\t\t - 接受传入 SYN 时设置（为监听器分配新连接）。
\t * - ESTABLISHED
\t\t - ``TCP_ESTABLISHED``
\t\t - 是
\t\t - 数据传输状态。
\t * - FIN-WAIT-1
\t\t - ``TCP_FIN_WAIT_1``
\t\t - 是
\t\t - 主动关闭时进入（本地 FIN 已发送）。
\t * - FIN-WAIT-2
\t\t - ``TCP_FIN_WAIT_2``
\t\t - 是
\t\t - 本地 FIN 的 ACK 之后进入（当对端尚未关闭时）。
\t * - CLOSE-WAIT
\t\t - 未实现
\t\t - 是
\t\t - TCP 输入路径明确说明 CLOSE_WAIT 未实现；NuttX 在收到 FIN 时
       强制应用程序关闭，直接转到 ``TCP_LAST_ACK``。
\t * - CLOSING
\t\t - ``TCP_CLOSING``
\t\t - 是
\t\t - 用于同时关闭处理。
\t * - LAST-ACK
\t\t - ``TCP_LAST_ACK``
\t\t - 是
\t\t - 在收到 FIN 并发送 FIN 响应后使用。
\t * - TIME-WAIT
\t\t - ``TCP_TIME_WAIT``
\t\t - 是
\t\t - 关闭握手后使用；定时器驱动的清理。

关于 ``TCP_ALLOCATED`` 的说明
-------------------------

``TCP_ALLOCATED`` 是 NuttX 特有的，没有直接的 RFC 状态名称。
它是新创建的套接字连接的预连接/预接受状态。

高级转换摘要
=============================

本节总结最常见的状态路径。

主动打开（connect）
---------------------

典型的客户端流程：

::

\tTCP_ALLOCATED
\t\t-> TCP_SYN_SENT        (tcp_connect() 准备 SYN)
\t\t-> TCP_ESTABLISHED     (tcp_input 收到 SYN|ACK 并回复 ACK)

被动打开（listen/accept）
----------------------------

监听套接字注册在监听器表中（不是 LISTEN 状态）。
当 SYN 到达时：

::

\ttcp_listenports[] 中的监听器
\t\t-> 新连接：TCP_SYN_RCVD  (tcp_conn.c 中的 tcp_allocaccept())
\t\t-> TCP_ESTABLISHED         (tcp_input 收到最终 ACK)
\t\t-> accept() 唤醒           (tcp_accept_connection())

正常关闭（主动关闭）
-----------------------------

当应用程序发起关闭（或 ``shutdown(SHUT_WR)``）时，
协议栈发送 FIN 并转换：

::

\tTCP_ESTABLISHED
\t\t-> TCP_FIN_WAIT_1
\t\t-> TCP_FIN_WAIT_2          (我们 FIN 的 ACK)
\t\t-> TCP_TIME_WAIT           (来自对端的 FIN)
\t\t-> TCP_CLOSED              (定时器过期)

同时关闭
------------------

如果在 ``TCP_FIN_WAIT_1`` 期间收到 FIN，且我们的 FIN 尚未完全被 ACK，
NuttX 可以进入 ``TCP_CLOSING``：

::

\tTCP_FIN_WAIT_1
\t\t-> TCP_CLOSING
\t\t-> TCP_TIME_WAIT           (我们 FIN 的 ACK)

被动关闭（对端先关闭）
---------------------------------

当在 ESTABLISHED 状态收到 FIN 时，通过回调通知应用程序。
协议栈发送 ACK 并转到 ``TCP_CLOSE_WAIT``：

::

\tTCP_ESTABLISHED
\t\t-> TCP_CLOSE_WAIT          (收到 FIN)
\t\t-> TCP_CLOSED              (我们 FIN 的 ACK)

详细状态处理
=======================

TCP_SYN_SENT
------------

* 由 ``tcp_connect()``（``net/tcp/tcp_conn.c``）进入。
* 收到带有有效 ACK 的 ``SYN|ACK`` 时：

\t* 解析选项（例如 MSS）。
\t* 设置 ``TCP_ESTABLISHED``。
\t* 更新 ``rcvseq`` 和窗口跟踪。
\t* 使用 ``TCP_CONNECTED`` 通知套接字层。

* 收到意外控制段或失败时：

\t* 连接被中止（``TCP_ABORT`` 回调），可能会发送 RST。

TCP_SYN_RCVD
------------

* 当 SYN 匹配监听器时，为新接受的连接进入。
\t分配和初始化发生在 ``tcp_allocaccept()``
\t（``net/tcp/tcp_conn.c``）中。
* 发送 SYN-ACK。重传由 ``tcp_timer.c`` 处理。
* 收到最终 ACK（``TCP_ACKDATA``）时：

\t* 转换到 ``TCP_ESTABLISHED``。
\t* 调用 ``tcp_accept_connection()`` 将连接交给
\t\t监听套接字/accept 逻辑。

TCP_ESTABLISHED
---------------

* 正常数据传输在此进行。
* 传入数据和 ACK 处理在 ``net/tcp/tcp_input.c`` 中处理。
* 如果收到 FIN：

\t* 通知应用程序（回调中包含 ``TCP_CLOSE`` 标志）。
\t* NuttX 转换到 ``TCP_CLOSE_WAIT`` 并发送 ``ACK``。

TCP_CLOSE_WAIT
--------------

* 仅在 ESTABLISHED 状态收到 FIN 时进入。
* 通知应用程序（回调中的 ``TCP_CLOSE`` 标志）。
* NuttX 可以发送数据，直到应用程序发起关闭。
* 应用程序关闭请求时：
\t* NuttX 发送 FIN 并转换到 ``TCP_LAST_ACK``。

TCP_FIN_WAIT_1
--------------

* 当应用程序请求正常关闭时进入。
\t这在 ``net/tcp/tcp_appsend.c`` 中当回调结果
\t包含 ``TCP_CLOSE`` 时发起。

* 收到 FIN 时：

\t* 如果 FIN 也 ACK 了我们的 FIN 且 ``tx_unacked == 0``：转换到
\t\t``TCP_TIME_WAIT``。
\t* 否则：转换到 ``TCP_CLOSING``。
\t* 两种情况下，都 ACK 对端的 FIN。

* 收到完成我们 FIN 的 ACK 时（且对端未发送 FIN）：

\t* 转换到 ``TCP_FIN_WAIT_2``。

* FIN_WAIT_1 中收到数据：

\t* 可以继续接收数据直到关闭或对端 FIN。

TCP_FIN_WAIT_2
--------------

* 在我们的 FIN 被 ACK 后等待对端 FIN。
* 收到 FIN 时：

\t* 转换到 ``TCP_TIME_WAIT``。
\t* ACK FIN 并通知关闭。

* FIN_WAIT_2 中收到数据：

\t* 可以继续接收数据直到关闭或对端 FIN。

TCP_CLOSING
-----------

* 同时关闭情况。
* 当我们 FIN 的 ACK 被收到时（``TCP_ACKDATA``）：

\t* 转换到 ``TCP_TIME_WAIT``。

TCP_LAST_ACK
------------

* 在 ESTABLISHED 状态收到 FIN 且应用程序选择关闭时进入，
\t导致协议栈发送 FIN。
* 收到我们 FIN 的 ACK 时（``TCP_ACKDATA``）：

\t* 转换到 ``TCP_CLOSED``。
\t* 通过回调通知关闭。

TCP_TIME_WAIT
-------------

* NuttX 通过发送 ACK 来响应段。
* 清理由定时器驱动（参见 ``tcp_timer.c``）：

\t* ``TCP_TIME_WAIT`` 被处理为"等待超时"状态。
\t* 当每连接定时器过期时，状态变为 ``TCP_CLOSED``。

定时器、重传和故障处理
=============================================

``net/tcp/tcp_timer.c`` 中的 TCP 定时器处理器驱动：

* 对 ``tx_unacked > 0`` 的连接进行重传。
* 特定状态的重传行为：

\t* ``TCP_SYN_RCVD``：重传 SYN-ACK。
\t* ``TCP_SYN_SENT``：重传 SYN。
\t* ``TCP_ESTABLISHED``：通过回调请求重传（``TCP_REXMIT``）。
\t* ``TCP_FIN_WAIT_1``、``TCP_CLOSING``、``TCP_LAST_ACK``：重传 FIN|ACK。

* 超时清理：

\t* ``TCP_SYN_RCVD``：如果 SYN-ACK 重传超过限制，半开连接将被关闭并释放。
\t* ``TCP_SYN_SENT`` 和已建立连接：如果重传超过限制，连接将被关闭，
\t\t套接字被通知（``TCP_TIMEDOUT``），可能会发送 RST。

偏差和显著简化
======================================

* LISTEN 不是显式的 TCP 状态；它由监听器表条目表示。
* RST 处理故意简单（接受 RST 并关闭）。

代码中的位置
=========================

* 状态定义：``include/nuttx/net/tcp.h``
* 传入段状态逻辑：``net/tcp/tcp_input.c``
* 重传/超时逻辑：``net/tcp/tcp_timer.c``
* 连接路径 / SYN_SENT 设置：``net/tcp/tcp_conn.c``
* 接受路径 / SYN_RCVD 分配：``net/tcp/tcp_conn.c``
* 主动关闭发起：``net/tcp/tcp_close.c`` 和 ``net/tcp/tcp_shutdown.c``
* 监听器表（LISTEN 语义）：``net/tcp/tcp_listen.c``
