=========================
``bridge`` 网络桥接
=========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

多网络系统的简单测试。它将在网络 ``1`` 和网络 ``2`` 上接收到的所有 UDP 数据包分别回传到网络 ``2`` 和网络 ``1``。接口 ``1`` 和接口可能在同一网络上，也可能不在。

- ``CONFIG_EXAMPLES_BRIDGE`` – 启用简单的 UDP 桥接测试。

两个网络各有相同的配置，``NETn`` 其中 ``n`` 指正在配置的网络 ``n={1,2}``。设 ``m`` 指另一个网络。

- ``CONFIG_EXAMPLES_BRIDGE_NETn_IFNAME`` – 网络 ``n`` 设备的注册名称。必须与先前注册的驱动程序名称匹配，且不能与其他网络设备名称 ``CONFIG_EXAMPLES_BRIDGE_NETm_IFNAME`` 相同。
- ``CONFIG_EXAMPLES_BRIDGE_NETn_RECVPORT`` – 网络 ``n`` 监听端口号。
- ``CONFIG_EXAMPLES_BRIDGE_NETn_SNDPORT`` – 网络 ``2`` 发送端口号。
- ``CONFIG_EXAMPLES_BRIDGE_NETn_IOBUFIZE`` – 网络 ``n`` UDP 发送/接收 I/O 缓冲区大小。
- ``CONFIG_EXAMPLES_BRIDGE_NETn_STACKSIZE`` – 网络 ``n`` 守护进程栈大小。
- ``CONFIG_EXAMPLES_BRIDGE_NETn_PRIORITY`` – 网络 ``n`` 守护进程任务优先级。

如果用作 NSH 附加组件，则假定在测试开始之前，两个网络的初始化已在外部完成。否则，以下选项可用：

- ``CONFIG_EXAMPLES_BRIDGE_NETn_NOMAC`` – 选择网络 ``n`` 硬件是否没有内置 MAC 地址。如果选择，将使用 ``CONFIG_EXAMPLES_BRIDGE_NETn_MACADDR`` 提供的 MAC 地址分配给网络 n 设备。
- ``CONFIG_EXAMPLES_BRIDGE_NETn_DHCPC`` – 使用 DHCP 客户端获取网络 n 的 IP 地址。
- ``CONFIG_EXAMPLES_BRIDGE_NETn_IPADDR`` – 如果 ``CONFIG_EXAMPLES_BRIDGE_NETn_DHCPC`` 未选择，则这是网络 ``n`` 的固定 IP 地址。
- ``CONFIG_EXAMPLES_BRIDGE_NETn_DRIPADDR`` – 网络 ``n`` 默认路由器 IP 地址（网关）。
- ``CONFIG_EXAMPLES_BRIDGE_NETn_NETMASK`` – 网络 ``n`` 掩码。
