=====================
``dhcpd`` DHCP 服务器
=====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

有关接口信息，请参阅 ``apps/include/netutils/dhcpd.h``。

DHCPC 使用提示
--------------------

如果您使用 DHCPC/D，则需要一些特殊的网络配置选项。这些包括：

- ``CONFIG_NET=y``
- ``CONFIG_NET_UDP=y`` – DHCP 需要 UDP 支持（以及其他各种与 UDP 相关的配置设置）。
- ``CONFIG_NET_BROADCAST=y`` – 需要 UDP 广播支持。
- ``CONFIG_NET_ETH_PKTSIZE=650`` 或更大。客户端必须准备好接收最多 ``576`` 字节的 DHCP 消息（不包括以太网、IP 或 UDP 头部和 FCS）。**注意**：实际的 MTU 设置将取决于具体的链路协议。这里显示的是以太网。
