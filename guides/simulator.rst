.. include:: /substitutions.rst
.. _simulator:

=========
模拟器
=========

Apache NuttX 有一个模拟器，可以在 Linux、Mac 和 Windows 计算机上作为普通程序运行。它对于调试与特定设备驱动无关的操作系统功能非常有用——例如 TCP/IP 协议栈本身、应用程序的 Web 界面或 API，或其他通信协议。它也方便在没有嵌入式硬件的情况下试用 Apache NuttX。

本指南假设你使用的是 Linux。它也适用于 Windows 和 Mac——如果你知道怎么做，请提交 PR 来改进本指南！

.. todo:: Windows 说明

macOS 前提条件
=======================

我们需要 ``genromfs`` 来构建模拟器（非 GUI）。

   .. code-block:: console

      $ git clone https://github.com/chexum/genromfs.git
      $ cd genromfs
      $ make
      $ make install

现在将构建好的 `genromfs` 可执行文件复制到 /opt/local/bin。

对于 GUI 应用程序，我们需要 X11 库，libx11 也可以使用 Homebrew 构建或通过安装 XQuartz 来获取。

   .. code-block:: console
   
      $ sudo port install xorg-libX11
      $ sudo port install xorg-server

编译
=========

#. 配置模拟器

   有很多可用的模拟器配置，可以设置你测试各种操作系统功能。

   这里我们将使用 ``sim:nsh`` 基本 NuttX Shell 配置。

    .. code-block:: console

       $ cd nuttx
       $ ./tools/configure.sh sim:nsh

#. 编译

    .. code-block:: console

       $ make

#. 运行模拟器：

    .. code-block:: console

       $ ./nuttx

       NuttShell (NSH) NuttX-12.10.0
       nsh> help
       help usage:  help [-v] [<cmd>]

         [         cp        exit      losetup   mv        rmdir     true
         ?         cmp       false     ls        mw        set       uname
         basename  dirname   free      mb        poweroff  sh        unset
         break     dd        help      mkdir     ps        sleep     usleep
         cat       echo      hexdump   mkfatfs   pwd       test      xd
         cd        exec      kill      mh        rm        time

       Builtin Apps:
         hello  nsh

       nsh>

#. 停止模拟器：

    .. code-block:: console

       nsh> poweroff
       $
       $ # 我们回到了 Linux 提示符。

.. _simulator_accessing_the_network:

访问网络
=====================

#. 这里我们将使用 ``sim:tcpblaster`` 配置，因为它带有即用型的网络支持。

    .. code-block:: console

       $ make distclean
       $ ./tools/configure.sh sim:tcpblaster
       $ make

#. 赋予模拟器权限

   在最新的 Linux 发行版上，你需要赋予 ``nuttx`` 程序访问网络的能力（类似于权限）：

    .. code-block:: console

       $ sudo setcap cap_net_admin+ep ./nuttx

#. 运行模拟器：

    .. code-block:: console

       $ ./nuttx

#. 启动网络接口

   在 Apache NuttX 上：

    .. code-block:: console

       nsh> ifup eth0

   在 Linux 上，首先你需要找到你的主网络接口——这通常是无线网络适配器或以太网适配器。执行以下操作：

    .. code-block:: console

       $ ifconfig
       lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
               inet 127.0.0.1  netmask 255.0.0.0
               inet6 ::1  prefixlen 128  scopeid 0x10<host>
               loop  txqueuelen 1000  (Local Loopback)
               RX packets 5846  bytes 614351 (614.3 KB)
               RX errors 0  dropped 0  overruns 0  frame 0
               TX packets 5846  bytes 614351 (614.3 KB)
               TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

       wlp0s20f3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
               inet 192.168.1.209  netmask 255.255.255.0  broadcast 192.168.1.255
               inet6 fe80::1161:c26b:af05:d784  prefixlen 64  scopeid 0x20<link>
               ether 24:41:8c:a8:30:d1  txqueuelen 1000  (Ethernet)
               RX packets 219369  bytes 176416490 (176.4 MB)
               RX errors 0  dropped 0  overruns 0  frame 0
               TX packets 108399  bytes 27213617 (27.2 MB)
               TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

   ``lo0`` 是回环接口，所以 ``wlp0s20f3`` 是无线接口。注意它在本地网络上有一个 IP 地址。可能会列出其他接口，你需要选择适合你系统的那个。

   然后，在 Linux 上执行以下操作来设置 tap 网络接口和路由，使 Apache NuttX 模拟器能够访问网络：

    .. code-block:: console

       $ sudo ./tools/simhostroute.sh wlp0s20f3 on
       $ ping -c 1 10.0.1.2  # nuttx system
       PING 10.0.1.2 (10.0.1.2) 56(84) bytes of data.
       64 bytes from 10.0.1.2: icmp_seq=1 ttl=64 time=7.52 ms

       --- 10.0.1.2 ping statistics ---
       1 packets transmitted, 1 received, 0% packet loss, time 0ms
       rtt min/avg/max/mdev = 7.529/7.529/7.529/0.000 m

#. 测试 Apache NuttX 是否能访问互联网

   首先让我们 ping 一下 Linux 主机的网络接口，以证明我们可以看到互联网网关：

    .. code-block:: console

       nsh> ping -c 1 10.0.1.1
       nsh> ping -c 1 10.0.1.1
       PING 10.0.1.1 56 bytes of data
       56 bytes from 10.0.1.1: icmp_seq=0 time=0 ms
       1 packets transmitted, 1 received, 0% packet loss, time 1010 ms

    现在让我们 ping 一下 Google 的 DNS 服务器，以证明我们可以访问互联网的其他部分：

    .. code-block:: console

       nsh> ping -c 1 8.8.8.8
       PING 8.8.8.8 56 bytes of data
       56 bytes from 8.8.8.8: icmp_seq=0 time=10 ms
       1 packets transmitted, 1 received, 0% packet loss, time 1010 ms

    如果不起作用，你需要在计算机上启用 IP 转发：

    .. code-block:: console

       sudo sysctl -w net.ipv4.ip_forward=1

   成功！

测试/捕获 TCP 网络流量
=======================================

#. 在 Linux 上启动 Wireshark（或 tcpdump）并捕获出现的 tap0 接口。

#. 可选地在 Linux 上激活模拟丢包：

    .. code-block:: console

       $ sudo iptables -A INPUT -p tcp --dport 31337 -m statistic --mode random --probability 0.01 -j DROP

#. 在 Linux 上运行 netcat 服务器：

    .. code-block:: console

       $ netcat -l -p 31337

#. 在 Apache NuttX 上运行 netcat 客户端：

    .. code-block:: console

       nsh> dd if=/dev/zero of=/tmp/test.bin count=1000
       nsh> netcat LINUX_HOST_IP_ADDRESS 31337 /tmp/test.bin

#. 在 Linux 的 Wireshark / tcpdump 中观察 TCP 网络流量。

在模拟器上测试 NxModbus RTU
=================================

#. 在 Linux 上创建虚拟 UART 对：

    .. code-block:: console

       $ socat PTY,link=/tmp/ttyNXB0 PTY,link=/tmp/ttyNXB1 &
       $ stty -F /tmp/ttyNXB0 raw
       $ stty -F /tmp/ttyNXB1 raw

#. 使用 NxModbus RTU 模拟器配置构建 NuttX：

    .. code-block:: console

       $ ./tools/configure.sh sim:nxmbrtu
       $ make

#. 启动服务器实例（从站）：

    .. code-block:: console

       $ ./nuttx
       nsh> nxmbserver -t rtu -d /tmp/ttyNXB0 -b 9600 -p none -u 1
       Starting Modbus RTU server on /tmp/ttyNXB0 (baud=9600, unit=1)
       Server running. Press Ctrl+C to stop.
       Register map:
       Coils:          1-100 (read/write)
       Discrete:       1-100 (read-only)
       Input regs:     1-100 (read-only, value=addr*10)
       Holding regs:   1-100 (read/write, initial=addr*100)

#. 在另一个终端中，启动第二个模拟器实例并对服务器运行客户端命令（主站）：

    .. code-block:: console

       $ ./nuttx
       nsh> nxmbclient -t rtu -d /tmp/ttyNXB1 -b 9600 -p none -u 1 read-holding 0 10
       0	0
       1	100
       2	200
       3	300
       4	400
       5	500
       6	600
       7	700
       8	800
       9	900

#. 可选的写入/读回检查：

    .. code-block:: console

       nsh> nxmbclient -t rtu -d /tmp/ttyNXB1 -b 9600 -p none -u 1 write-holding 0 123
       OK
       nsh> nxmbclient -t rtu -d /tmp/ttyNXB1 -b 9600 -p none -u 1 read-holding 0 1
       0	123

停止
========

#. 正常停止方式：

    .. code-block:: console

       nsh> poweroff
       $
       $ # 我们回到了 Linux 提示符。

   如果你没有 nsh 提示符，停止模拟器的唯一有效方式是从另一个终端终止它：

    .. code-block:: console

       $ pkill nuttx

#. 可选地在 Linux 上停用模拟丢包：

    .. code-block:: console

       $ sudo iptables -D INPUT -p tcp --dport 31337 -m statistic --mode random --probability 0.01 -j DROP

#. 如果你不再需要 tap0 接口，可以在 Linux 上按如下方式禁用：

    .. code-block:: console

       $ sudo ./tools/simhostroute.sh wlan0 off

调试
=========

你可以像调试任何普通 Linux 程序一样调试模拟器。
