===============
网络设备
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

-  ``include/nuttx/net/netdev.h``。所有与网络驱动相关
   的结构体和 API 都在此头文件中提供。
   结构体 ``struct net_driver_s`` 定义了该接口，
   并通过 ``netdev_register()`` 注册到网络。

-  ``include/nuttx/net/netdev_lowerhalf.h``。（推荐用于新驱动，
   参见 :ref:`网络驱动 <netdriver>`）
   此头文件定义了网络设备与网络协议栈之间的接口。
   网络设备是一个下层驱动，为网络协议栈提供发送和接收数据包的能力。

IP 地址
============

结构体 ``struct net_driver_s`` 现在支持一个 IPv4 地址和
多个 IPv6 地址。多个 IPv6 地址在现代网络设备中很常见。
例如，一个网络设备可能有一个链路本地地址和一个全局地址。
链路本地地址用于邻居发现协议，全局地址用于与 Internet 通信。

配置选项
---------------------

``CONFIG_NETDEV_MULTIPLE_IPv6``
  启用每个网络设备支持多个 IPv6 地址的功能。
  依赖于 ``CONFIG_NET_IPv6``。
``CONFIG_NETDEV_MAX_IPv6_ADDR``
  可分配给单个网络设备的最大 IPv6 地址数量。
  通常需要一个链路本地地址和一个全局地址。

IPv4 接口
---------------

目前每个网络设备仅支持一个 IPv4 地址，直接使用
:c:struct:`net_driver_s` 中的 :c:member:`d_ipaddr`、
:c:member:`d_draddr` 和 :c:member:`d_netmask`。

.. c:struct:: net_driver_s

  .. code-block:: c

    struct net_driver_s
    {
    #ifdef CONFIG_NET_IPv4
      in_addr_t      d_ipaddr;      /* 分配给网络接口的主机 IPv4 地址 */
      in_addr_t      d_draddr;      /* 默认路由器 IP 地址 */
      in_addr_t      d_netmask;     /* 网络子网掩码 */
    #endif
    };

IPv6 接口
---------------

现在每个网络设备支持多个 IPv6 地址，使用
:c:struct:`net_driver_s` 中的 :c:member:`d_ipv6` 来存储 IPv6 地址。
出于历史原因，为了向后兼容，我们保留了旧名称
:c:member:`d_ipv6addr` 和 :c:member:`d_ipv6netmask`。
新驱动请使用 :c:member:`d_ipv6`。

.. c:struct:: net_driver_s

  .. code-block:: c

    struct net_driver_s
    {
    #ifdef CONFIG_NET_IPv6
      struct netdev_ifaddr6_s d_ipv6[CONFIG_NETDEV_MAX_IPv6_ADDR];
    #endif
    };

通过提供的 API 管理 IPv6 地址将更加灵活：

  - :c:func:`netdev_ipv6_add()`
  - :c:func:`netdev_ipv6_del()`
  - :c:func:`netdev_ipv6_srcaddr()`
  - :c:func:`netdev_ipv6_lladdr()`
  - :c:func:`netdev_ipv6_lookup()`
  - :c:func:`netdev_ipv6_foreach()`

.. c:function:: int netdev_ipv6_add(FAR struct net_driver_s *dev, const net_ipv6addr_t addr, \
                                    unsigned int preflen);
.. c:function:: int netdev_ipv6_del(FAR struct net_driver_s *dev, const net_ipv6addr_t addr, \
                                    unsigned int preflen);

  在网络设备上添加或删除 IPv6 地址

  :return: 如果操作在设备上成功应用则返回零；
    失败时返回负的 errno 值。

.. c:function:: FAR const uint16_t *netdev_ipv6_srcaddr(FAR struct net_driver_s *dev, \
                                                        const net_ipv6addr_t dst);

  获取源 IPv6 地址 (RFC6724)。

  :return: 成功时返回指向 IPv6 地址的指针。该指针不会为
    NULL，但可能是一个包含 g_ipv6_unspecaddr 的地址。

.. c:function:: FAR const uint16_t *netdev_ipv6_lladdr(FAR struct net_driver_s *dev);

  获取网络设备的链路本地地址。

  :return: 成功时返回指向链路本地地址的指针。
    如果在设备上未找到该地址则返回 NULL。

.. c:function:: FAR struct netdev_ifaddr6_s *netdev_ipv6_lookup(FAR struct net_driver_s *dev, \
                                                    const net_ipv6addr_t addr, bool maskcmp);

  在网络设备的 IPv6 地址中查找 IPv6 地址

  :return: 成功时返回指向匹配的 IPv6 地址条目的指针。
    如果在设备中未找到该 IPv6 地址则返回 NULL。

.. c:function:: int netdev_ipv6_foreach(FAR struct net_driver_s *dev, \
                      devif_ipv6_callback_t callback, FAR void *arg);

  枚举网络设备上的每个 IPv6 地址。当以下条件之一满足时
  该函数将终止：(1) 所有地址已被枚举，或 (2) 回调函数
  返回任何非零值。

  :return: 如果枚举成功完成则返回零；
    如果枚举因回调而提前终止则返回非零值。

IP 地址的 Ioctl 命令
-----------------------

  - :c:macro:`SIOCGIFADDR`
  - :c:macro:`SIOCSIFADDR`
  - :c:macro:`SIOCDIFADDR`
  - :c:macro:`SIOCGLIFADDR`
  - :c:macro:`SIOCSLIFADDR`
  - :c:macro:`SIOCGIFNETMASK`
  - :c:macro:`SIOCSIFNETMASK`
  - :c:macro:`SIOCGLIFNETMASK`
  - :c:macro:`SIOCSLIFNETMASK`

.. c:macro:: SIOCGIFADDR
.. c:macro:: SIOCSIFADDR
.. c:macro:: SIOCDIFADDR

  我们遵循 Linux 惯例 [1]：

    使用 :c:member:`ifr_addr` 或 :c:member:`ifr6_addr` 配合
    :c:member:`ifr6_prefixlen` 来获取、设置或删除设备的地址。
    为了兼容性，:c:macro:`SIOCGIFADDR` 仅返回 :c:macro:`AF_INET`
    地址，:c:macro:`SIOCSIFADDR` 接受 :c:macro:`AF_INET` 和
    :c:macro:`AF_INET6` 地址，:c:macro:`SIOCDIFADDR` 仅删除
    :c:macro:`AF_INET6` 地址。可以通过 :c:macro:`SIOCSIFADDR`
    将 :c:macro:`AF_INET` 地址设置为零来删除它。

  注意：与 Linux 不同，NuttX 中 IPv6 地址的最大数量是有限制的。
  如果在已达到限制时添加更多 IPv6 地址，新地址将替换具有相同
  范围的地址。

  [1]: https://man7.org/linux/man-pages/man7/netdevice.7.html

.. c:macro:: SIOCGLIFADDR
.. c:macro:: SIOCSLIFADDR

  使用 :c:member:`lifr_addr` 获取或设置设备的 IPv6 地址。

  我们遵循 Linux 惯例 [1] 允许接口名称为
  <eth>:<num>[2]，以支持多个 IPv6 地址。

  注意：建议使用 :c:macro:`SIOCSIFADDR` 和 :c:macro:`SIOCDIFADDR`
  来管理 IPv6 地址，这样您无需关心存储地址的槽位。

硬件校验和卸载
=========================

结构体 :c:struct:`net_driver_s` 包含支持硬件校验和卸载的字段。
此功能允许网络协议栈将校验和计算委托给网络设备硬件，从而提高性能。

实现细节
----------------------

支持硬件校验和卸载的驱动应使用以下辅助函数来获取校验和卸载信息：

* :c:func:`netdev_checksum_start`：获取从数据包开头到 L4 头部起始位置
  （校验和计算起始点）的偏移量。
* :c:func:`netdev_checksum_offset`：获取从 L4 头部起始位置到校验和字段
  的偏移量。
* :c:func:`netdev_upperlayer_header_checksum`：计算伪头部校验和。

.. code-block:: c

   int netdev_checksum_start(FAR struct net_driver_s *dev);
   int netdev_checksum_offset(FAR struct net_driver_s *dev);
   uint16_t netdev_upperlayer_header_checksum(FAR struct net_driver_s *dev);

支持硬件校验和卸载的驱动应在传输数据包之前使用这些函数
来相应地配置硬件。

  [1]: https://man7.org/linux/man-pages/man7/netdevice.7.html
  [2]: 例如 'eth0:0' 表示 eth0 上的辅助地址

.. c:macro:: SIOCGIFNETMASK
.. c:macro:: SIOCSIFNETMASK

  使用 :c:member:`ifr_netmask` 获取或设置设备的 IPv4 网络掩码。

.. c:macro:: SIOCGLIFNETMASK
.. c:macro:: SIOCSLIFNETMASK

  使用 :c:member:`lifr_netmask` 获取或设置设备的 IPv6 网络掩码。

  我们遵循 Linux 惯例允许接口名称为 <eth>:<num>，
  以支持多个 IPv6 地址。

  注意：建议使用 :c:macro:`SIOCSIFADDR` 和 :c:macro:`SIOCDIFADDR`
  来管理 IPv6 地址，这样您无需关心存储地址的槽位。
