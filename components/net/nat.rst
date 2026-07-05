=================================
网络地址转换 (NAT)
=================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

网络地址转换 (NAT) 修改转发数据包中的地址、端口或 ICMP
标识符，使来自一个网络的流量可以使用另一个接口的地址。

NuttX 支持构建时可选择的 NAT44 和 NAT66 模式：

``full-cone NAT``
    将本地地址和端口（或 ICMP 标识符）映射到外部地址和端口
    （或标识符）。对端不是 NAT 条目键的一部分。

``symmetric NAT``
    将本地端点映射到外部端点，用于特定的对端端点。
    对端是 NAT 条目键的一部分，因此来自同一本地端点到
    不同对端的流量可能使用不同的映射。

NuttX NAT 实现支持：

  * TCP
  * UDP
  * ICMP

    * ECHO (REQUEST / REPLY)
    * Error Messages (DEST_UNREACHABLE / TIME_EXCEEDED / PARAMETER_PROBLEM)

  * ICMPv6

    * ECHO (REQUEST / REPLY)
    * Error Messages (DEST_UNREACHABLE / PACKET_TOO_BIG / TIME_EXCEEDED / PARAMETER_PROBLEM)

工作流程
========

::

  本地网络 (LAN)                              外部网络 (WAN)
                    |----------------|
       <local IP,   |                | <external IP,             <peer IP,
         -----------|                |-----------------------------
        local port> |                |  external port>            peer port>
                    |----------------|

- 出站

  - **LAN** -> **转发** -> **NAT**（仅当目标为 WAN 时） -> **WAN**

  - 所有来自 **LAN** 且目标为 **WAN** 的数据包将被伪装，
    ``local ip:port`` 被更改为 ``external ip:port``。

- 入站

  - **WAN** -> **NAT**（仅来自 WAN，更改目标地址） -> **转发** -> **LAN**

  - 来自 **WAN** 的数据包将尝试从 ``external ip:port`` 更改回
    ``local ip:port`` 并发送到 **LAN**。

配置选项
=====================

``CONFIG_NET_NAT``
    启用网络地址转换。此选项依赖于 ``CONFIG_NET_IPFORWARD``。
``CONFIG_NET_NAT44`` / ``CONFIG_NET_NAT66``
    启用 IPv4 到 IPv4 / IPv6 到 IPv6 NAT。此选项依赖于
    ``CONFIG_NET_NAT``。
``CONFIG_NET_NAT44_FULL_CONE`` / ``CONFIG_NET_NAT66_FULL_CONE``
    为 NAT44 / NAT66 选择全锥 NAT 模式。
``CONFIG_NET_NAT44_SYMMETRIC`` / ``CONFIG_NET_NAT66_SYMMETRIC``
    为 NAT44 / NAT66 选择对称 NAT 模式。
``CONFIG_NET_NAT_HASH_BITS``
    设置 NAT 条目哈希表使用的位数。哈希表有
    ``1 << CONFIG_NET_NAT_HASH_BITS`` 个桶。
``CONFIG_NET_NAT_TCP_EXPIRE_SEC``
    设置空闲 TCP NAT 条目的过期时间（秒）。默认值为 86400 秒，
    如 RFC 2663 第 2.6 节第 5 页所述。但为了更好的性能，
    可以设置为更短的时间如 240 秒。
``CONFIG_NET_NAT_UDP_EXPIRE_SEC``
    设置空闲 UDP NAT 条目的过期时间（秒）。
``CONFIG_NET_NAT_ICMP_EXPIRE_SEC``
    设置空闲 ICMP NAT 条目的过期时间（秒）。
``CONFIG_NET_NAT_ICMPv6_EXPIRE_SEC``
    设置空闲 ICMPv6 NAT 条目的过期时间（秒）。
``CONFIG_NET_NAT_ENTRY_RECLAIM_SEC``
    设置自动回收所有过期 NAT 条目的时间。值为零将禁用自动回收。
    因为过期条目会在匹配入站/出站条目时自动回收，
    所以此配置在 NAT 正常使用时不会产生重大影响，
    但在哈希表很大且只有少量连接使用 NAT 时非常有用
    （这只会触发哈希表中少量链的回收）。

使用方法
=====

- 可以直接从 C 代码启用 NAT：

  .. c:function:: int nat_enable(FAR struct net_driver_s *dev)

   在网络设备上启用 NAT。通过此设备转发的出站数据包可能会被转换。

   :return: 如果 NAT 在设备上成功启用则返回零。
     失败时返回负的 errno 值。

  .. c:function:: int nat_disable(FAR struct net_driver_s *dev)

   在网络设备上禁用 NAT。

   :return: 如果 NAT 在设备上成功禁用则返回零。
     失败时返回负的 errno 值。

- 也可以使用 NSH 中的 ``iptables`` 命令启用 NAT。
  规则被添加到 NAT 表，传递给 ``-o`` 的输出接口
  是 NuttX 外部接口：

  .. code-block:: console

    nsh> iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE

  要删除规则，使用 ``-D`` 指定相同的规则：

  .. code-block:: console

    nsh> iptables -t nat -D POSTROUTING -o eth1 -j MASQUERADE

  .. note::

   以上命令是 NuttX 的 ``iptables`` 命令。它们在 NuttX 内部配置 NAT。
   它们与 Linux 主机的 ``iptables`` 命令是分开的。

验证
==========

以下设置在 Ubuntu 22.04 x86_64 Linux 主机上使用 NuttX 模拟器验证 NAT。
主要以 IPv4 作为示例。

测试使用两个 Linux 网络命名空间：

  * ``private`` 表示 NuttX NAT 后面的主机。
  * ``public`` 表示 NuttX NAT 外部侧的主机。

这使测试在主机本地进行，不需要 Internet 访问。

拓扑结构为：

::

  私有命名空间                      NuttX 模拟器                      公有命名空间
                         |----------------------------------|
      tap0               | eth0: 192.168.0.2/24             |
   192.168.0.1/24  ------|                                  |
                         |                                  |
                         |                eth1: 10.0.1.2/24 |------ 10.0.1.1/24
                         |                    (NAT enabled) |        tap1
                         |----------------------------------|

在此拓扑中：

  * ``eth0`` 是 NuttX 私有侧接口。
  * ``eth1`` 是 NuttX 外部接口。NAT 在 ``eth1`` 上启用。
  * ``tap0`` 被移入 Linux ``private`` 命名空间，是 ``eth0`` 的对端。
  * ``tap1`` 被移入 Linux ``public`` 命名空间，是 ``eth1`` 的对端。

步骤 1：配置 NuttX 模拟器
---------------------------------

使用至少两个 TAP 设备、IP 转发和 NAT 配置 NuttX 模拟器：

.. code-block:: kconfig

    CONFIG_NET_IPFORWARD=y
    CONFIG_NET_NAT=y
    CONFIG_NET_NAT44=y
    CONFIG_simulator_NETDEV_NUMBER=2

步骤 2：启动 NuttX 模拟器
-----------------------------

启动 NuttX 模拟器并确保它在 Linux 主机上创建两个 TAP 接口。
创建或配置 TAP 接口可能需要 root 权限或 ``CAP_NET_ADMIN`` 等能力。
以下命令中假设接口名称为 ``tap0`` 和 ``tap1``。

步骤 3：配置 Linux 命名空间
----------------------------------

在 Linux 主机上运行以下命令：

.. code-block:: bash

    NS_PRIVATE="private"
    NS_PUBLIC="public"

    IF_PRIVATE="tap0"
    IP_PRIVATE="192.168.0.1"
    IP_NUTTX_PRIVATE="192.168.0.2"

    IF_PUBLIC="tap1"
    IP_PUBLIC="10.0.1.1"
    IP_NUTTX_PUBLIC="10.0.1.2"

    sudo ip netns add "$NS_PRIVATE"
    sudo ip netns add "$NS_PUBLIC"

    sudo ip link set "$IF_PRIVATE" netns "$NS_PRIVATE"
    sudo ip link set "$IF_PUBLIC" netns "$NS_PUBLIC"

    # 私有命名空间
    sudo ip netns exec "$NS_PRIVATE" ip link set lo up
    sudo ip netns exec "$NS_PRIVATE" ip link set "$IF_PRIVATE" up
    sudo ip netns exec "$NS_PRIVATE" ip addr add "$IP_PRIVATE/24" dev "$IF_PRIVATE"
    sudo ip netns exec "$NS_PRIVATE" ip route add default via "$IP_NUTTX_PRIVATE" dev "$IF_PRIVATE"

    # 公有命名空间
    sudo ip netns exec "$NS_PUBLIC" ip link set lo up
    sudo ip netns exec "$NS_PUBLIC" ip link set "$IF_PUBLIC" up
    sudo ip netns exec "$NS_PUBLIC" ip addr add "$IP_PUBLIC/24" dev "$IF_PUBLIC"

对于正常的 NAT 验证，``public`` 命名空间不需要到 ``192.168.0.0/24`` 的
路由，因为返回流量的目标地址是转换后的外部地址 ``10.0.1.2``。

步骤 4：配置 NuttX 网络接口
------------------------------------------

从 NSH 配置 NuttX 接口地址：

.. code-block:: console

    nsh> ifconfig eth0 192.168.0.2
    nsh> ifup eth0
    nsh> ifconfig eth1 10.0.1.2
    nsh> ifup eth1
    nsh> addroute default 10.0.1.1 eth1

在 NuttX ``eth1`` 上启用 NAT。可以在网络初始化期间调用 ``nat_enable()``
或从 NSH 运行以下命令：

.. code-block:: console

    nsh> iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE

步骤 5：验证基本连通性
-----------------------------------

在测试 NAT 之前，验证每个直接链路是否正常工作。

从 NuttX ping 私有侧对端：

.. code-block:: console

    nsh> ping 192.168.0.1

从 NuttX ping 公有侧对端：

.. code-block:: console

    nsh> ping 10.0.1.1

从私有命名空间 ping NuttX 私有侧接口：

.. code-block:: bash

    sudo ip netns exec private ping 192.168.0.2

从公有命名空间 ping NuttX 外部接口：

.. code-block:: bash

    sudo ip netns exec public ping 10.0.1.2

步骤 6：测试 TCP NAT
--------------------

在 ``public`` 命名空间中启动 iperf 服务器：

.. code-block:: bash

    sudo ip netns exec public iperf -B 10.0.1.1 -s -i 1

从 ``private`` 命名空间运行 iperf 客户端：

.. code-block:: bash

    sudo ip netns exec private iperf -B 192.168.0.1 -c 10.0.1.1 -i 1

服务器应该看到连接来自 NuttX 外部地址 ``10.0.1.2``，
而不是来自私有地址 ``192.168.0.1``。

步骤 7：测试 ICMP NAT
---------------------

从 ``private`` 命名空间 ping ``public`` 命名空间：

.. code-block:: bash

    sudo ip netns exec private ping 10.0.1.1

在公有侧，ICMP Echo Request 应该被转换为使用 NuttX 外部地址
``10.0.1.2`` 作为源地址。

步骤 8：测试 HTTP NAT
---------------------

在 ``public`` 命名空间中启动一个简单的 HTTP 服务器：

.. code-block:: bash

    sudo ip netns exec public python3 -m http.server 8000 -b 10.0.1.1

从 ``private`` 命名空间运行 HTTP 请求：

.. code-block:: bash

    for i in $(seq 1 20000); do
      sudo ip netns exec private curl -sS -o /dev/null 'http://10.0.1.1:8000/'
    done

步骤 9：捕获数据包
-----------------------

在私有侧捕获：

.. code-block:: bash

    sudo ip netns exec private tcpdump -nn -i tap0

在公有侧捕获：

.. code-block:: bash

    sudo ip netns exec public tcpdump -nn -i tap1

对于出站 IPv4 流量，``tap0`` 应显示源地址为 ``192.168.0.1`` 的数据包，
``tap1`` 应显示转换后源地址为 ``10.0.1.2`` 的相同流量。
入站返回路径应显示反向转换。
