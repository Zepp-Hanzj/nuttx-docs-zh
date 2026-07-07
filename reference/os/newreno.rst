==========================
拥塞控制 NewReno
==========================

NewReno 拥塞控制算法用于解决网络拥塞崩溃问题，包括：
 - 慢启动
 - 拥塞避免
 - 快速重传
 - 快速恢复。

 实现参考了 RFC6582 和 RFC5681。此外，我们对拥塞算法进行了优化。在拥塞避免状态，使用最大拥塞窗口（max_cwnd）来限制 cwnd 的过度增长，防止拥塞引起的网络抖动。当发生 RTO 超时时，最大拥塞窗口（max_cwnd）随当前拥塞窗口（cwnd）更新，更新权重为 0.875。

工作流程
========

tcp 发送端的 NewReno 根据接收到的 ack 和重传超时 (RTO) 事件调整 cwnd 和 ssthresh。

使用 cwnd 与 snd_wnd 一起控制发送到网络的字节数。以下是 newreno 的工作方式，如下所述：

- 在建立 tcp 连接时初始化 ssthresh 和 cwnd。
- 当收到 ack 时，检查 ack 是否重复。

 + 如果是，增加 dupack 计数。如果 dupack 超过快速重传阈值 3，在重传丢失的段（快速重传）后，进入快速恢复状态。
 + 如果否，接收新的 ack。

   * 如果当前 ackno 大于 fr_ack（即快速重传发生时的 snd_seq），则退出快速恢复状态并进入拥塞避免。
   * 如果 cwnd 小于 ssthresh，在慢启动状态增加 cwnd。
   * 如果 cwnd 大于或等于 ssthresh，增加的 cwnd 不能超过 max_cwnd。

- 当 RTO 超时时，重置 cwnd 和 ssthresh 的值，更新 max_cwnd，并进入慢启动状态。
- 当发送段时，使用 cwnd 和 snd_wnd 的最小值来计算可以发送的字节数。

NewReno 的简单状态转换图如下所示。

::

                                    |           ^
                                    | ------------------------
                                    | initialize cwnd ssthresh
                                    V
                              +------------+
             .--------------->| Slow Start |-----------------.
             |                +------------+                 |
             |                     |  |                      |
             |    timeout          |  |  recv dup ack        | recv new ack
             |------------------   |  |  ---------------     | ----------------
             |reset cwnd ssthresh  |  |  dupack >= 3         | cwnd >= ssthresh
             |update max_cwnd      |  |  fr_ack = snd_seq    |
             |<--------------------'  |<------------------.  |
             |                        |                   |  |
             |                        v                   |  V
             |                    +--------+     +--------------------+
             |                    |   FT   |     |Congestion Avoidance|
             |                    +--------+     +--------------------+
             |                        |                   ^  |
             |              retransmit|lost segment       |  |
             |                        |                   |  |
             |                        |      recv new ack |  |
             |                        v      ------------ |  |
             |                    +--------+ ack > fr_ack |  |
             |                    |   FR   |--------------'  |
             |                    +--------+                 |
             |                        |                      |
             |                        v                      v
             '-----------------------------------------------'

配置选项
=====================
``NET_TCP_CC_NEWRENO``
  启用或禁用 NewReno 功能。

  依赖于 ``NET_TCP_FAST_RETRANSMIT``。

测试
====


测试拓扑
-------------

::

                         IP:10.0.1.1

                         +--------+
                 --------| nuttx0 |--------
                 |       +--------+       |
                 |          /|\           |
                 |           |            |
                 |       +-------+        |
                 |       | ifb0  |        |
                 |       +-------+        |
                \|/         /|\          \|/
             +-------+       |        +-------+
             | tap0  |------/ \-------| tap1  |
             +-------+                +-------+
                /|\                      /|\
                 |                        |
                \|/                      \|/
             +-------+                +-------+
        sim1 | eth0  |                | eth0  | sim2
             +-------+                +-------+

             IP:10.0.1.3              IP:10.0.1.4

测试步骤
----------

在 Ubuntu 22.04 x86_64 上使用 NuttX SIM 按以下步骤测试功能：

:1.配置测试环境：

- 将 nuttx0 入站速度设置为 10Mbps。

 ..  code-block:: bash

    # 加载 fib 模块，启动 ifb0 接口
    modprobe ifb
    ip link set dev ifb0 up

    # 将 nuttx0 入站数据包导入 ifb0
    tc qdisc add dev nuttx0 handle ffff: ingress
    tc filter add dev nuttx0 parent ffff: u32 match u32 0 0 action mirred egress redirect dev ifb0

    # 限制 nuttx0 入站 10Mbps
    tc qdisc add dev ifb0 root tbf rate 10Mbit latency 50ms burst 1540

- 配置 sim 模拟器。

 + 在 ubuntu 上启动 iperf3 服务器。

 ..  code-block:: bash

     iperf3 -s -i1 -p10003  #用于 sim1
     iperf3 -s -i1 -p10004  #用于 sim2


 + 启动模拟器 sim1 和 sim2 并配置 ip 地址。

 ..  code-block:: bash

  # 启动并配置 sim1
  start gdb nuttx
  ifconfig eth0 10.0.1.3

  # 启动并配置 sim2
  start gdb nuttx
  ifconfig eth0 10.0.1.4 # sim2


:2.流测试：


- 使用 iperf3 进行流测试。

 ..  code-block:: bash

  iperf3 -c 10.0.1.1 -i1 -t60 -p10003 # sim1
  iperf3 -c 10.0.1.1 -i1 -t60 -p10004 # sim2


:3.对比测试：

 比较启用和禁用 NewReno 的测试结果。


测试结果
------------

 测试结果应表明，启用 NewReno 拥塞控制时，总网络吞吐量显著增加，接近实际总网络带宽，并且两个 sim 设备的速率稳定。
