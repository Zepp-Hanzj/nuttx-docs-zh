=====================
Netlink 路由支持
=====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Netlink Route (:c:macro:`NETLINK_ROUTE`) 允许在网络变化时发送通知消息。
应用程序可以通过监听 netlink 套接字消息来获取这些变化。

NuttX 支持的 Netlink Route 组

- RTMGRP_IPV4_ROUTE | RTMGRP_IPV6_ROUTE
  - 当 IPV4|IPV6 路由表变化时发送通知。

- RTMGRP_NEIGH
  - 当 ARP (IPV4) 或邻居 (IPV6) 表变化时发送通知。

- RTNLGRP_IPV6_PREFIX
  - 当 IPV6 前缀变化时发送通知。

消息内容
================

1. RTMGRP_IPV4_ROUTE | RTMGRP_IPV6_ROUTE

  ``RTM_NEWROUTE``、``RTM_DELROUTE``、``RTM_GETROUTE``：
  创建、删除或接收有关网络路由的信息。这些消息包含一个 rtmsg 结构
  和 3 个可选的 rtattr 结构序列。

  .. code-block:: c

    struct getroute_recvfrom_ipv4addr_s
    {
      struct rtattr attr;
      in_addr_t     addr;
    };

    struct getroute_recvfrom_ipv4response_s
    {
      struct nlmsghdr hdr;
      struct rtmsg    rte;
      struct getroute_recvfrom_ipv4addr_s dst;
      struct getroute_recvfrom_ipv4addr_s genmask;
      struct getroute_recvfrom_ipv4addr_s gateway;
    };

    struct getroute_recvfrom_ipv6addr_s
    {
      struct rtattr  attr;
      net_ipv6addr_t addr;
    };

    struct getroute_recvfrom_ipv6response_s
    {
      struct nlmsghdr hdr;
      struct rtmsg    rte;
      struct getroute_recvfrom_ipv6addr_s dst;
      struct getroute_recvfrom_ipv6addr_s genmask;
      struct getroute_recvfrom_ipv6addr_s gateway;
    };

2. RTMGRP_NEIGH

  ``RTM_NEWNEIGH``、``RTM_DELNEIGH``、``RTM_GETNEIGH``：
  添加、删除或接收有关邻居表条目（例如 ARP 条目）的信息。
  消息包含一个 ndmsg 结构和可选的 rtattr 结构序列。
  数据将是 ``include/netinet/arp.h`` 中的 ``struct arpreq``
  或 ``include/net/neighbor.h`` 中的 ``struct neighbor_entry_s``

  .. code-block:: c

    struct getneigh_recvfrom_response_s
    {
      struct nlmsghdr hdr;
      struct ndmsg    msg;
      struct rtattr   attr;
      uint8_t         data[1];
    };

3. RTNLGRP_IPV6_PREFIX

  ``RTM_NEWPREFIX``：
  接收有关 IPV6 前缀的信息。消息包含一个 prefixmsg 结构
  和两个可选的 rtattr 结构序列。``addr`` 和
  ``prefix_cacheinfo`` 是从 RA 消息中解析的。

  .. code-block:: c

    struct getprefix_recvfrom_addr_s
    {
      struct rtattr  attr;
      net_ipv6addr_t addr;
    };

    struct getprefix_recvfrom_cache_s
    {
      struct rtattr           attr;
      struct prefix_cacheinfo pci;
    };

    struct getprefix_recvfrom_response_s
    {
      struct nlmsghdr  hdr;
      struct prefixmsg pmsg;
      struct getprefix_recvfrom_addr_s  prefix;
      struct getprefix_recvfrom_cache_s pci;
    };

使用方法
=====

.. code-block:: c

  struct sockaddr_nl addr;
  struct nlmsghdr *hdr;
  uint8_t buffer[BUFSIZE];
  int sd = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE); 

  addr.nl_family  = AF_NETLINK;
  addr.nl_groups  = RTMGRP_IPV4_ROUTE | RTMGRP_IPV6_ROUTE |
                    RTMGRP_NEIGH | RTMGRP_IPV6_PREFIX;

  bind(sd, (FAR struct sockaddr *)&addr, sizeof(addr)); /* 绑定到设备 */
  while (1)
    {
      recv(sd, buf, BUFSIZE, 0);
      for (hdr = buf; NLMSG_OK(hdr, ret); hdr = NLMSG_NEXT(hdr, ret))
        {
          if (hdr->nlmsg_type == RTM_...)
            {
              /* 解析 netlink 消息的函数 */
              ...
            }
        }
    }

  close(sd); /* 关闭套接字 */
