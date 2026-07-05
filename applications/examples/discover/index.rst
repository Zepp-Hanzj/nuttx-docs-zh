================================
``discover`` UDP 发现守护进程
================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此示例测试 ``netutils/discover`` 工具。此示例初始化并启动 UDP 发现守护进程。此守护进程用于发现本地网络中的设备，特别是使用 DHCP 配置的设备。它监听 UDP 广播，广播可以包含设备类别，以便发现设备组。也可以通过一种广播发现来寻址所有类别。

如果选择了 ``CONFIG_NSH_BUILTIN_APPS``，此示例将自动构建为 NSH 内置应用。否则，它将作为独立程序运行，入口点为 ``discover_main``。

NuttX 配置设置：

- ``CONFIG_EXAMPLES_DISCOVER_DHCPC`` – DHCP 客户端。
- ``CONFIG_EXAMPLES_DISCOVER_NOMAC`` – 使用预设 MAC 地址。
- ``CONFIG_EXAMPLES_DISCOVER_IPADDR`` – 目标 IP 地址。
- ``CONFIG_EXAMPLES_DISCOVER_DRIPADDR`` – 路由器 IP 地址。
- ``CONFIG_EXAMPLES_DISCOVER_NETMASK`` – 网络掩码。
