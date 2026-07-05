============================
``ping`` ICMP "ping" 命令
============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
--------
``ping`` 应用程序向目标主机发送 ICMPv4 Echo Request 数据包，并报告回复、
丢包率、往返时间 (RTT) 统计和基本错误。它对于验证 IP 连通性和测量延迟非常有用。

系统要求
------------
- 启用网络：``CONFIG_NET=y``
- 操作系统中的 ICMP 和原始套接字支持
- 构建应用程序：``CONFIG_SYSTEM_PING=y``
- 可选 DNS 解析：``CONFIG_LIBC_NETDB`` 和 ``CONFIG_NETDB_DNSCLIENT``
- 可选设备绑定支持（``-I``）：``CONFIG_NET_BINDTODEVICE``

命令格式
--------

::

	ping [-c <count>] [-i <interval>] [-W <timeout>] [-s <size>] [-I <interface>] <hostname|ip-address>

其中 ``<hostname>`` 可以是 DNS 名称（启用 DNS 客户端时）或 IPv4 地址。
没有 DNS 时，需要 IPv4 地址。

选项
-------

- ``-c <count>``：要发送的 echo 请求数量（默认：实现定义，通常为 10）。
- ``-i <interval>``：请求之间的延迟，单位毫秒（默认：1000 ms）。
- ``-W <timeout>``：每个回复的超时时间，单位毫秒（默认：1000 ms）。
- ``-s <size>``：要发送的 ICMP 负载字节数（默认：56）。
- ``-I <interface>``：将套接字流量绑定到特定网络设备名称（需要 ``CONFIG_NET_BINDTODEVICE``）。
- ``-h``：显示帮助并退出。

输出
------

对于每个回复，``ping`` 打印类似以下的行：

::

	56 bytes from 10.0.2.2: icmp_seq=3 time=6.0 ms

超时时：

::

	No response from 10.0.2.2: icmp_seq=3 time=1000 ms

完成时，打印摘要统计信息，包括发送的数据包数、接收的数据包数、丢包率、
总时间和 RTT 最小/平均/最大/标准差：

::

	10 packets transmitted, 10 received, 0% packet loss, time 10011 ms
	rtt min/avg/max/mdev = 0.000/0.600/6.000/1.800 ms

退出状态
-----------

- 成功 (0)：完成且无致命错误。
- 失败 (!=0)：报告了致命错误（例如套接字/DNS 错误、无效参数）。

示例
--------

基本 IP 连通性测试：

.. code-block:: bash

	ping 1.1.1.1

使用自定义请求数和负载大小 ping 主机名：

.. code-block:: bash

	ping -c 3 -s 100 example.com

减小间隔和超时以加快探测：

.. code-block:: bash

	ping -i 500 -W 500 10.0.2.2

将流量绑定到特定接口（需要 ``CONFIG_NET_BINDTODEVICE``）：

.. code-block:: bash

	ping -I wlan0 10.0.2.2

如果设备名称无效，``ping`` 报告绑定错误并终止。

注意事项
--------

- 设备绑定 (``-I``) 在存在多个接口或路由不明确的早期网络设置时非常有用。
  它强制流量使用指定的设备。
- ``<hostname>`` 的 DNS 解析需要 DNS 客户端配置；否则请提供 IPv4 地址。
- ICMPv6 支持由单独的 ``ping6`` 应用程序提供（启用时，
  ``CONFIG_NETUTILS_PING6``），具有类似的选项和输出。

故障排除
---------------

- ``ERROR: ping_gethostip(...) failed``：DNS 查找失败或地址无效。
- ``ERROR: socket() failed: <errno>``：原始套接字创建失败。
- ``ERROR: setsockopt error: <errno>``：设备绑定 (``-I``) 失败；检查接口名称和 ``CONFIG_NET_BINDTODEVICE``。
- ``ERROR: poll/recvfrom failed``：链路问题或网络栈错误。

实现细节
----------------------

内部实现中，应用程序使用 ``apps/netutils/ping/icmp_ping.c`` 驱动 ICMP Echo
请求和解析回复。命令行界面和打印逻辑在 ``apps/system/ping/ping.c`` 中实现。
