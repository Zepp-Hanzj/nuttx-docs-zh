============================
``ntpc`` NTP 守护进程命令
============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本示例演示如何使用 NTP 客户端同步系统时间并获取当前时间和日期。它使用网络时间协议（NTP）提供精确的时间同步。

描述
-----------

ntpc 示例：

- 使用 NTP 客户端库同步系统时间

- 连接到 NTP 服务器（默认：pool.ntp.org）

- 支持从 DHCP 选项 42 学习的 NTP 服务器配置

- 在后台启动 NTP 客户端以进行持续同步

- 提供检查状态和停止 NTP 客户端的命令

- 允许通过命令行选项管理 NTP 客户端

注意：本示例假设网络连接已建立。

NTP（网络时间协议）是一个复杂的协议，提供高精度的时间同步，是网络时间服务的标准。

配置
-------------

本示例需要以下 NuttX 配置选项：

- CONFIG_NET：启用网络支持
- CONFIG_NET_UDP：启用 UDP 支持
- CONFIG_NETUTILS_NTPCLIENT：启用 NTP 客户端支持
- CONFIG_SYSTEM_NTPC：启用本示例

其他配置选项：

- CONFIG_NETUTILS_NTPCLIENT_SERVER：NTP 服务器主机名（默认："pool.ntp.org"）
- CONFIG_NETUTILS_DHCPC：当 NTP 服务器应从 DHCP 选项 42 动态学习时启用 DHCP 客户端支持

使用方法
-------------

1. 使用网络支持配置 NuttX 构建
2. 确保网络连接已建立（例如，通过 NSH 网络命令）如果 DHCP 通过选项 42 提供 NTP 服务器，``ntpc`` 可以自动使用该服务器列表。
3. 构建并烧录镜像到目标板
4. 运行命令：
   - ``ntpcstart``、``ntpcstop``、``ntpcstatus``

**可用命令：**

- ``ntpcstart`` - 在后台启动 NTP 客户端

- ``ntpcstop`` - 停止 NTP 客户端

- ``ntpcstatus`` - 显示 NTP 客户端状态信息

预期输出
---------------

**启动 NTP 客户端（ntpcstart）：**

::

   Starting NTP client...
   Using NTP servers: pool.ntp.org
   NTP client started successfully (task ID: 123)
   NTP client is now running in the background

**停止 NTP 客户端（ntpcstop）：**

::

   Stopping NTP client...
   Stopped the NTP daemon

**显示 NTP 状态（ntpcstatus）：**

::

    The number of last samples: 3
    [0] srv <ip> offset -0.033502142 delay 0.249973549
    [1] srv <ip> offset -0.020698070 delay 0.029928000
    [2] srv <ip> offset -0.015448935 delay 0.019815119

**使用 date 命令验证：**

在有网络连接的情况下，执行 `date` 应返回正确的时间和日期。

::

    nsh> ntpcstart
    Starting NTP client...
    Using NTP servers: 0.pool.ntp.org;1.pool.ntp.org;2.pool.ntp.org
    NTP client started successfully (task ID: 10)
    NTP client is now running in the background
    nsh> date
    Fri, Sep 05 18:49:37 2025

DHCP 提供的 NTP 服务器
-------------------------

当启用 ``CONFIG_NETUTILS_DHCPC`` 时，DHCP 客户端可以将从 DHCP 选项 42 学习的 NTP 服务器 IPv4 地址传递给 ``ntpc``。

这允许 ``ntpc`` 在配置中没有固定服务器主机名的情况下运行，并跟踪 DHCP 提供的 NTP 服务器更新。

测试 DHCP 提供的 NTP 服务器的一种方法是使用 ``dnsmasq``：

::

   dnsmasq --no-daemon --log-dhcp --log-queries \
     --interface=tap0 --bind-interfaces \
     --dhcp-authoritative \
     --dhcp-range=192.168.50.20,192.168.50.50,255.255.255.0 \
     --dhcp-option=option:router,192.168.50.1 \
     --dhcp-option=option:dns-server,1.1.1.1 \
     --dhcp-option=option:ntp-server,162.159.200.123

注意事项
-------------

- 本示例需要互联网连接
- 运行本示例前必须配置并连接网络
- NTP 服务器必须可访问（默认：pool.ntp.org）
- UDP 端口 123（NTP）不得被防火墙阻止
- 本示例包含网络故障的错误处理
- NTP 比简单时间协议提供更精确的时间同步
