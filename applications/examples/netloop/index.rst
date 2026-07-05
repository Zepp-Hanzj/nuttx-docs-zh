===================================
``netloop`` 网络回环设备
===================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是一个简单的网络回环设备测试。``examples/nettest`` 也可以配置为提供
（更好的）本地回环传输测试。此版本源自 ``examples/poll``，
专注于使用回环设备测试 ``poll()``。

- ``CONFIG_EXAMPLES_NETLOOP=y`` – 启用 nettest 示例。

依赖项：

- ``CONFIG_NET_LOOPBACK`` – 需要本地回环支持。
- ``CONFIG_NET_TCP`` – 需要 TCP 支持，包含以下内容：
   - ``CONFIG_NET_TCPBACKLOG``
   - ``CONFIG_NET_TCP_WRITE_BUFFERS``
- ``CONFIG_NET_IPv4`` – 目前仅支持 IPv4。
