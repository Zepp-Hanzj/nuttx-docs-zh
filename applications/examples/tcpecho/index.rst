===========================
``tcpecho`` TCP Echo Server
===========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Simple single threaded, poll based TCP echo server. This example implements the
TCP Echo Server from W. Richard Stevens "UNIX Network Programming" Book.
Contributed by Max Holtberg.

See also ``examples/nettest``

- ``CONFIG_EXAMPLES_TCPECHO=y`` – Enables the TCP echo server.
- ``CONFIG_XAMPLES_TCPECHO_PORT`` – Server Port, default ``80``.
- ``CONFIG_EXAMPLES_TCPECHO_BACKLOG`` – Listen Backlog, default ``8``.
- ``CONFIG_EXAMPLES_TCPECHO_NCONN`` – Number of Connections, default ``8``.
- ``CONFIG_EXAMPLES_TCPECHO_DHCPC`` – DHCP Client, default ``n``.
- ``CONFIG_EXAMPLES_TCPECHO_NOMAC`` – Use Canned MAC Address, default ``n``.
- ``CONFIG_EXAMPLES_TCPECHO_IPADDR`` – Target IP address, default ``0x0a000002``.
- ``CONFIG_EXAMPLES_TCPECHO_DRIPADDR`` – Default Router IP address (Gateway),
  default ``0x0a000001``.
- ``CONFIG_EXAMPLES_TCPECHO_NETMASK`` – Network Mask, default ``0xffffff00``.
