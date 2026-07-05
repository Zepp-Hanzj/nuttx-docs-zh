====
IPv6
====

.. warning:: 
    迁移自: https://cwiki.apache.org/confluence/display/NUTTX/IPv6

NuttX 多年来一直支持互联网协议版本 4 (IPv4)。代码库中也存在 IPv6 的片段多年，但这些片段只是占位符，没有功能性。

但最近，在 NuttX-7.6 之后，我投入了一些精力来完成 IPv6 实现。此 Wiki 页面包含该集成工作的笔记，并有望发展为提供 NuttX IPv6 支持的完整文档。

当前状态：基本功能已完成并经过验证。这包括 ICMPv6 邻居发现协议、ICMPv6 回显请求/响应（用于 ``ping6``）、TCP/IPv6 和 UDP/IPv6。也已证明您可以支持同时启用 IPv4 和 IPv6 的平台。

以太网驱动程序要求
============================

基本驱动程序要求
-------------------------

为了支持 IPv6，以太网驱动程序必须做到以下几点：

* 它们必须识别 IPv6 数据包并调用 ``ipv6_input`` 以将数据包传递到网络栈中。这相当于在接收到 IPv4 数据包时调用 ``ipv4_input``。
* 发送 IPv6 时，驱动程序必须调用 ``neighbor_out()`` 以将目标的 MAC 地址添加到链路层报头中。IPv6 的 `ICMPv6 邻居发现协议` 相当于 IPv6 使用的 `地址解析协议` (ARP)。IPv6 的 ``neighbor_out()`` 执行与 IPv4 的 ``arp_out()`` 函数类似的功能。
* 以太网驱动程序还必须支持一些额外的地址过滤。对于 IPv4 支持，大多数以太网驱动程序配置为仅接受匹配 MAC 地址的以太网数据包和广播数据包（如果启用了 IGMP 支持，则为选定的多播数据包）。需要额外的过滤支持来支持 IPv6。

所有现有的 NuttX 以太网驱动程序已经过修改以支持前两个要点的要求。然而，大多数现有的以太网驱动程序需要添加额外的逻辑来支持最后的要求。

多播地址过滤
---------------------------

每个以太网设备通过 PHY 连接到以太网线，因此可以访问线上传递的每个数据包。在 `混杂` 模式下，这是期望的行为，但通常不是：混杂模式下线上的流量会使大多数中等 MCU 不堪重负。因此，以太网 MAC 硬件将支持地址过滤。也就是说，硬件将查看每个数据包开头的以太网报头，并忽略以太网报头中没有所需信息的数据包。软件将只看到所需的过滤后的数据包。

通常，以太网 MAC 设置为 `单播` 地址过滤：硬件被编程为仅接受目标以太网 MAC 地址与编程到硬件中的 MAC 地址匹配的数据包。此外，特殊的 `广播` 以太网地址也将被接受。通过这种方式，MCU 接收的以太网数据量大大减少。

`多播` 地址略有不同。与广播地址不同，有许多可能的多播地址，因此以太网 MAC 硬件必须支持某种特殊功能，以将传入数据包中的目标以太网地址与各种多播地址进行匹配。通常这涉及对以太网地址进行 `哈希` 并执行 `哈希表查找` 以检查地址匹配。

每个以太网驱动程序使用在 ``nuttx/include/nuttx/net/netdev.h`` 中定义的公共接口。该接口定义了对以太网驱动程序的一组调用，以执行各种功能。其中一个功能是多播地址过滤：

.. code-block:: c

    #ifdef CONFIG_NET_IGMP
    int (*d_addmac)(FAR struct net_driver_s *dev, FAR const uint8_t *mac);
    int (*d_rmmac)(FAR struct net_driver_s *dev, FAR const uint8_t *mac);
    #endif

``d_addmac()`` 接口将多播地址添加到哈希表；``d_rmmac()`` 从哈希表中删除多播地址。

此接口仅在支持 IGMP 时需要，但对多播地址过滤进行编程的底层能力对于完整的 IPv6 支持是必需的。此接口存在于所有以太网驱动程序中，但大多数目前只是占位符，`待提供`。目前，只有 STMicro STM32、TI Tiva TM4C 和 Atmel SAM3/4 以及 SAMA5D3/4 以太网驱动程序支持多播哈希表。必须将此功能添加到为支持 IPv6 而修改的任何额外以太网驱动程序中。

ICMPv6 邻居发现协议
----------------------------------

ICMPv6 邻居发现协议是此额外地址过滤的原因。ICMPv6 邻居发现协议是 IPv4 ARP 的替代品。它与 ARP 的不同之处在于它不是在以太网链路层实现的，而是在 IPv6 层内实现的。为了接收 ICMPv6 的广播数据包，使用 IPv6 多播地址 33.33.ff.xx.xx.xx，其中 xx.xx.xx 部分来自 IPv6 地址。必须修改以太网驱动程序过滤逻辑，使其接受定向到该 MAC 地址的数据包。

目前，此额外支持仅为 TI Tiva TM4C129X 以太网驱动程序实现。以下是该驱动程序的代码片段，显示了如何实现：

.. code-block:: c

    /* Set the MAC address */
    
    tiva_macaddress(priv);
    
    #ifdef CONFIG_NET_ICMPv6
    /* Set up the IPv6 multicast address */
    
    tiva_ipv6multicast(priv);
    #endif

其中 `tiva_macaddress()` 设置正常的 MAC 地址过滤，`tiva_ipv6multicast()` 设置 IPv6 所需的特殊过滤：

.. code-block:: c 

    /****************************************************************************
   * Function: tiva_ipv6multicast
   *
   * Description:
   *   Configure the IPv6 multicast MAC address.
   *
   * Parameters:
   *   priv - A reference to the private driver state structure
   *
   * Returned Value:
   *   OK on success; Negated errno on failure.
   *
   * Assumptions:
   ***************************************************************************/
   
    #ifdef CONFIG_NET_ICMPv6
    static void tiva_ipv6multicast(FAR struct tiva_ethmac_s *priv)
    {
        struct net_driver_s *dev;
        uint16_t tmp16;
        uint8_t mac[6];
    
        /* For ICMPv6, we need to add the IPv6 multicast address
        * For IPv6 multicast addresses, the Ethernet MAC is derived by
        * the four low-order octets OR'ed with the MAC 33:33:00:00:00:00,
        * so for example the IPv6 address FF02:DEAD:BEEF::1:3 would map
        * to the Ethernet MAC address 33:33:00:01:00:03.
        * NOTES: This appears correct for the ICMPv6 Router Solicitation
        * Message, but the ICMPv6 Neighbor Solicitation message seems to
        * use 33:33:ff:01:00:03.
        */
    
        mac[0] = 0x33;
        mac[1] = 0x33;
    
        dev    = &priv->dev;
        tmp16  = dev->d_ipv6addr[6];
        mac[2] = 0xff;
        mac[3] = tmp16 >> 8;
    
        tmp16  = dev->d_ipv6addr[7];
        mac[4] = tmp16 & 0xff;
        mac[5] = tmp16 >> 8;
    
        nvdbg("IPv6 Multicast: %02x:%02x:%02x:%02x:%02x:%02x\n",
            mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
    
        (void)tiva_addmac(dev, mac);
   
    #ifdef CONFIG_NET_ICMPv6_AUTOCONF
        /* Add the IPv6 all link-local nodes Ethernet address.  This is the
        * address that we expect to receive ICMPv6 Router Advertisement
        * packets.
        */
    
        (void)tiva_addmac(dev, g_ipv6_ethallnodes.ether_addr_octet);
   
    #endif /* CONFIG_NET_ICMPv6_AUTOCONF */
    #ifdef CONFIG_NET_ICMPv6_ROUTER
        /* Add the IPv6 all link-local routers Ethernet address.  This is the
        * address that we expect to receive ICMPv6 Router Solicitation
        * packets.
        */
    
        (void)tiva_addmac(dev, g_ipv6_ethallrouters.ether_addr_octet);
   
    #endif /* CONFIG_NET_ICMPv6_ROUTER */
    }
    #endif /* CONFIG_NET_ICMPv6 */


以下以太网驱动程序已完成且支持 IPv6。所有其他以太网驱动程序具有所有必需的 IPv6 支持，`除了` 它们缺少 (1) 上述所需的 ICMPv6 地址过滤和/或 (2) 多播地址过滤支持。

* STMicro STM32
* TI Tiva TM4C
* Atmel SAMA5D4
* NXP LPC17xx


板级配置
====================

目前，有三个预先配置为使用 IPv6 的板级配置：``nuttx/boards/arm/tiva/dk-tm4c129x/configs/ipv6``、``nuttx/boards/arm/stm32/stm32f4discovery/ipv6`` 和 ``nuttx/boards/arm/tiva/tm4c1294-launchpad/configs/ipv6``。这些默认配置仅启用了 IPv6。但这些板目录中的 `README` 文件描述了如何同时启用 IPv4 和 IPv6。

Ping
====

从主机 PC Ping
-----------------

从 Windows cmd 终端 Ping
``````````````````````````````

.. code-block:: bash

    ping -6 fc00::2

从 Linux shell Ping
`````````````````````

.. code-block:: bash

    ping6 fc00::2

从 NuttShell (NSH) Ping
-----------------------------

.. code-block:: bash

    nsh> ping6 fc00::2

NSH ifconfig
============

仅 IPv4
---------

``CONFIG_NET_IPv4=y`` 和 ``CONFIG_NET_IPv6=n``

.. code-block:: bash

    nsh> ifconfig
    eth0    Link encap: Ethernet HWaddr 00:1a:b6:02:81:14 at UP
            inet addr:10.0.0.2 DRaddr:10.0.0.1 Mask:255.255.255.0
    
                 IPv4   TCP   UDP  ICMP
    Received     003b  001c  0000  0004
    Dropped      001b  0000  0000  0000
      IPv4        VHL: 0000 Frg: 0000
      Checksum   0000  0000  0000  ----
      TCP         ACK: 0000 SYN: 0000
                  RST: 0000 0000
      Type       0000  ----  ----  0000
    Sent         0031  002d  0000  0004
      Rexmit     ----  ----  0000  ----

注意：只有在启用 ``CONFIG_NET_STATISTICS`` 时才会显示详细的数据包统计信息。

仅 IPv6
---------

``CONFIG_NET_IPv4=n`` 和 ``CONFIG_NET_IPv6=y``

.. code-block:: bash

    nsh> ifconfig
    eth0    Link encap: Ethernet HWaddr 00:1a:b6:02:81:14 at UP
            inet6 addr:fc00::2
            inet6 DRaddr:fc00::1
            inet6 Mask:ffff:ffff:ffff::ffff:ffff:ffff:ff80
    
                IPv6   TCP   UDP  ICMPv6
    Received     0007  0000  0000  0007
    Dropped      0000  0000  0000  0000
      IPv6        VHL: 0000
      Checksum   ----  0000  0000  ----
      TCP         ACK: 0000 SYN: 0000
                  RST: 0000 0000
      Type       0000  ----  ----  0000
    Sent         0011  0000  0000  0011
      Rexmit     ----  ----  0000  ----

同时启用 IPv4 和 IPv6
------------------

``CONFIG_NET_IPv4=y`` 和 ``CONFIG_NET_IPv6=y``

.. code-block:: bash

    nsh> ifconfig
    eth0    Link encap: Ethernet HWaddr 00:1a:b6:02:81:14 at UP
            inet addr:10.0.0.2 DRaddr:10.0.0.1 Mask:255.255.255.0
            inet6 addr:fc00::2
            inet6 DRaddr:fc00::1
            inet6 Mask:ffff:ffff:ffff::ffff:ffff:ffff:ff80
    
                 IPv4  IPv6   TCP   UDP  ICMP  ICMPv6
    Received     0047  000a  001c  0000  0004  000a
    Dropped      0027  0000  0000  0000  0000  0000
      IPv4        VHL: 0000 Frg: 0000
      IPv6        VHL: 0000
      Checksum   0000  ----  0000  0000  ----  ----
      TCP         ACK: 0000 SYN: 0000
                  RST: 0000 0000
      Type       0000  0000  ----  ----  0000  0000
    Sent         0033  000a  002f  0000  0004  000a
      Rexmit     ----  ----  ----  0000  ----  ----

测试、应用程序和网络实用工具
==========================================

除了核心 RTOS 支持 IPv6 之外，网络测试、网络感知应用程序以及所有网络实用工具（``netutils``）也需要更改。

* NuttShell (NSH)：IPv6 支持部分可用。NSH 能够初始化 IPv6 域，一些 NSH 命令已适配支持 IPv6。已添加 ping6 命令。但仍有许多命令需要更新。
* 测试：``apps/examples`` 中有几个网络测试。``nettest`` 测试和 ``udp`` 测试已适配在 IPv6 域中工作，但其他测试尚未适配。
* Netutils：``apps/netutils`` 中的网络实用工具已适配支持 IPv6：DHCP、FTP、TFTP、Telnet 等。``netlib`` 中已包含管理 IPv6 地址的支持，但其他内容尚未更新。
