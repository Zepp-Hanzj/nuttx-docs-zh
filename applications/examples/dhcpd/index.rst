=====================
``dhcpd`` DHCP 服务器
=====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此示例为目标系统构建一个小型 DHCP 服务器。

**注意**：出于测试目的，此示例可以构建为基于主机的 DHCPD 服务器。可以按以下方式构建::

  cd examples/dhcpd
  make -f Makefile.host TOPDIR=<nuttx-directory>

NuttX 配置设置：

- ``CONFIG_NET=y`` – 当然需要。
- ``CONFIG_NET_UDP=y`` – DHCP 需要 UDP 支持（以及各种其他 UDP 相关配置设置）。
- ``CONFIG_NET_BROADCAST=y`` – 需要 UDP 广播支持。
- ``CONFIG_NETUTILS_NETLIB=y`` – 需要网络库。
- ``CONFIG_EXAMPLES_DHCPD_NOMAC`` – （可定义为使用软件分配的 MAC）

另请参阅其他地方描述的 ``CONFIG_NETUTILS_DHCPD_*`` 设置，这些设置在 ``netutils/dhcpd/dhcpd.c`` 中使用。这些设置用于描述守护进程的行为。
