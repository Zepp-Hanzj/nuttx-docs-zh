Linux 网络支持
==========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

模拟使用 Linux 下的 TUN/TAP 驱动来提供网络支持。
它可以运行在两种模式之一：主机路由或桥接。在主机路由
模式下无需特殊配置，但默认情况下
模拟器只能被其运行所在的主机访问。

建议尽可能使用桥接模式。它需要稍多的设置工作，
但更加灵活，而且最终可能更容易维护。

主机路由模式
------

如果启用了 CONFIG_SIM_NET_HOST_ROUTE，模拟器将创建并
维护从分配的 IP 地址到实例 tap 设备的主机路由。
如果应用程序更改了模拟器的 IP 地址，此路由将被更新。
请注意，如果你在主机上运行 ifconfig，
你不会在 TAP 设备上看到模拟器的 IP 地址。

无需特殊设置。只需为模拟器分配一个与主机在同一网络中的空闲 IP 地址，
一切即可正常工作。请注意，如果你分配的 IP 已被网络中的其他设备使用，
在模拟器停止之前，你的主机将无法
看到它。主机路由将强制将所有
目标为该 IP 的流量发送到 tap 接口。

.. note::
   If you configure an IP address that is not on the same subnet as your
      将需要额外的手动设置。提供了一个辅助脚本
   `tools/simhostroute.sh` is provided that can do this setup on Linux.
      不建议在 Windows 或 macOS 上使用主机路由模式。

最新版本的 Linux 需要设置内核能力以允许 nuttx
可执行文件访问 tap 网络驱动。你可以在以下链接了解更多关于 tun/tap
驱动需要 Linux 能力的信息：

https://github.com/torvalds/linux/blob/master/Documentation/networking/tuntap.txt

The `boards/sim/sim/sim/configs/tcpblaster/defconfig` is known to work in this
configuration.

编译方法：

.. code-block:: bash

    $ ./tools/configure.sh sim:tcpblaster
    $ make menuconfig  # optional, to adjust configuration
    $ make clean; make

编译 NuttX 模拟器后，你可以执行以下操作：

在 Linux 上：

.. code-block:: bash

    $ # necessary on recent Linux distributions
    $ sudo setcap cap_net_admin+ep ./nuttx
    $ # set up the host route and IP tables rules
    $ # replace ens33 with your Ethernet or wireless interface
    $ sudo ./tools/simhostroute.sh ens33 on
    $ # start the NuttX simulator
    $ ./nuttx

在 NuttX 模拟器中：

.. code-block:: bash

    nsh> # replace or omit dns if needed, IPv6 line is optional
    nsh> ifconfig eth0 inet6 fc00::2/112 dns 2001:4860:4860::8888
    nsh> ifconfig eth0 10.0.1.2 dns 8.8.8.8
    nsh> ifup eth0

在 Linux 上：

.. code-block:: bash

    $ # is nuttx up?
    $ ping 10.0.1.2

桥接模式
----

基本用法
----
如果启用了 CONFIG_SIM_NET_BRIDGE，模拟器的 tap 接口将
自动添加到由 CONFIG_SIM_NET_BRIDGE_DEVICE 配置选项指定的
Linux 桥接设备。请注意，这必须是一个
预先存在的桥接设备，否则初始化将失败。模拟器
不会为你创建桥接器。

要创建桥接器，首先为你的平台安装桥接工具包
（例如 RedHat 中的 net-tools RPM）。然后执行
类似以下的命令：

.. code-block:: bash

  # ip link add nuttx0 type bridge

这将创建 nuttx0 桥接器。创建后，桥接器可以被
一个或多个模拟使用。每个主机只需要一个桥接器；如果你启动
多个模拟，它们都将被添加到同一个桥接器中，并可以相互通信。

选项 1：将本地流量路由到桥接器
----------------
如果你希望主机能够与模拟器通信，你还需要
为桥接器分配一个 IP 地址（这将是你分配给模拟器的默认网关）
并添加网络路由。请注意
所选子网不应已被使用。例如，如果你
想使用 172.26.23.0/24 子网进行模拟，
你可以执行类似以下的操作：

.. code-block:: bash

  # ip link add nuttx0 type bridge
  # ifconfig nuttx0 172.26.23.1/24

标准的 Linux ifconfig 工具将自动添加相应的网络路由，
因此无需进一步操作。

选项 2：实时网络访问
-----------
有两种主要方法可以让模拟器访问你的网络。
一种是将你的 Linux 主机设置为路由器并配置你的网络，
使其知道如何找到相应的子网。这对大多数用例来说
过于复杂，因此除非你有特定需求，否则可以安全地忽略它。

推荐的方法是将真实接口添加到你与 NuttX 一起使用的桥接器中。
例如，如果你的主机上有辅助的 eth1 接口，
你可以简单地将其连接到你希望模拟访问的网络，
并运行以下命令：

.. code-block:: bash

  # ip link set eth1 master nuttx0

从那时起，你的模拟将直接连接到与 eth1 接口相同的网络。
请注意，在这种情况下，你的桥接器通常不需要 IP 地址。

如果你只有一个接口，你可以配置系统使 eth0
（或其他主接口）在桥接器上。为此，你需要从系统控制台
执行类似以下的命令：

.. code-block:: bash

  # ip link add nuttx0 type bridge
  # ip link set eth0 master nuttx0
  # ifconfig nuttx0 <host-ip-address/netmask>
  # route add -net default gw ...

你的其余网络配置将保持不变；你主机的 IP 地址只是从
直接分配给以太网接口，变为分配给包含该接口的桥接器。
连接将正常运行。
NuttX 模拟将像前面的示例一样加入桥接器。

在本文介绍的两种实时访问场景中，你在模拟中配置的默认网关
应该是你所访问网络的正常网关，
无论桥接器是否有 IP 地址。桥接器充当
以太网集线器；你的模拟直接访问正常网关，
就好像模拟是物理连接到网络的设备一样。

启动时配置
-----
大多数 Linux 发行版都有在启动时配置桥接器的机制。
请参阅你发行版的文档获取更多信息。

设置脚本
----

有一个脚本 `tools/simbridge.sh` 可以为你完成设置。

注意事项
----

    - VMware ESXi 用户应注意，桥接器会将包含的以太网接口置于混杂模式
        （不要问我为什么）。ESXi 默认会拒绝此操作，
        什么都不起作用。要修复此问题，请编辑相关 vSwitch 或 VLAN 的属性，
    properties of the relevant vSwitch or VLAN, select the Security tab, and
    set "Promiscuous Mode" to "Accept".

    If anyone knows a better way to deal with this, or if I'm misunderstanding
    what's happening there, please do tell.

        我不知道 VMware 的消费产品是否有类似的问题。

  - tools/simbridge.sh could make the bridge setup easier:

      # tools/simbridge.sh eth0 on
      # tools/simbridge.sh eth0 off

-- Steve <steve@floating.io>
   http://floating.io
