==================================
``nettest`` 基于 TCP 的客户端/服务器
==================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是一个简单的网络测试，用于验证 TCP/IP 连接中的客户端和服务器功能。

- ``CONFIG_EXAMPLES_NETTEST=y`` – 启用 nettest 示例。
- ``CONFIG_EXAMPLES_NETLIB=y`` – 需要网络库。

配置：

- 目标硬件上的服务器；主机上的客户端。
- 目标硬件上的客户端；主机上的服务器。
- 不同目标上的服务器和客户端。
- 回环配置，客户端和服务器在同一目标上。

另请参见 ``examples/tcpecho``。
