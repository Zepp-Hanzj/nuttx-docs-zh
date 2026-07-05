===============
``iperf`` iperf
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
--------

这是 ESP-IDF iperf 示例的 NuttX 移植版本。[1]

它不支持标准 iperf 的所有功能。
它应该与 iperf 版本 2.x 兼容。[2]

[1] https://github.com/espressif/esp-idf/tree/master/examples/wifi/iperf
[2] https://sourceforge.net/projects/iperf2/

配置 NuttX 以使用无线路由器（即接入点）
----------------------------------------------------------------

由于您已经在 NuttX/ 仓库的根目录中，执行
make menuconfig 来定义您的无线路由器和密码::

    $ make menuconfig

    按以下方式浏览菜单：

    Application Configuration  --->
        Network Utilities  --->
            Networking Configuration  --->
                WAPI Configuration  --->
                    (myApSSID) SSID
                    (mySSIDpassphrase) Passprhase

将 myApSSID 的 SSID 替换为您的无线路由器名称，
将 Passprhase 替换为您的 WiFi 密码。

退出并保存配置。

iperf 测试示例
------------------

要设置，请执行 ``make menuconfig`` 并选择 Apps > netutils > iperf 示例。默认情况下，NuttX 将作为发送数据的客户端；主机计算机（Linux、macOS 或 Windows）将作为服务器。

设置网络，使 NuttX 计算机可以 ping 通主机，主机也可以 ping 通 NuttX。现在您可以运行测试了。

如果您使用无线网卡，必须首先连接到路由器：

在主机上::

    $ iperf -s -p 5471 -i 1 -w 416K
    ------------------------------------------------------------
    Server listening on TCP port 5471
    TCP window size:  416 KByte
    ------------------------------------------------------------

在 NuttX 上::

    nsh> iperf -c 192.168.1.181 -p 5471 -i 1 -t 10
    mode=tcp-client sip=192.168.1.198:5001, dip=192.168.1.181:5471, interval=1, time=10

            Interval Bandwidth

    0-   1 sec,  0.39 Mbits/sec
    1-   2 sec,  0.26 Mbits/sec
    2-   3 sec,  0.39 Mbits/sec
    3-   4 sec,  0.26 Mbits/sec
    4-   5 sec,  0.26 Mbits/sec
    5-   6 sec,  0.26 Mbits/sec
    6-   7 sec,  0.26 Mbits/sec
    7-   8 sec,  0.26 Mbits/sec
    8-   9 sec,  0.26 Mbits/sec
    9-  10 sec,  0.26 Mbits/sec
    0-  10 sec,  0.28 Mbits/sec


现在在主机上您应该看到类似以下内容::

    $ iperf -s -p 5471 -i 1 -w 416K
    ------------------------------------------------------------
    Server listening on TCP port 5471
    TCP window size:  416 KByte
    ------------------------------------------------------------
    [  5] local 192.168.1.181 port 5471 connected with 192.168.1.198 port 4210
    [  5]  0.0- 1.0 sec  60.8 KBytes   498 Kbits/sec
    [  5]  1.0- 2.0 sec  34.9 KBytes   286 Kbits/sec
    [  5]  2.0- 3.0 sec  33.7 KBytes   276 Kbits/sec
    [  5]  3.0- 4.0 sec  33.4 KBytes   274 Kbits/sec
    [  5]  4.0- 5.0 sec  32.0 KBytes   262 Kbits/sec
    [  5]  5.0- 6.0 sec  32.0 KBytes   262 Kbits/sec
    [  5]  6.0- 7.0 sec  33.4 KBytes   274 Kbits/sec
    [  5]  7.0- 8.0 sec  32.0 KBytes   262 Kbits/sec
    [  5]  8.0- 9.0 sec  32.0 KBytes   262 Kbits/sec
    [  5]  9.0-10.0 sec  33.4 KBytes   274 Kbits/sec
    [  5]  0.0-10.3 sec   368 KBytes   292 Kbits/sec


这将告诉您链路速度，单位为 Kbits/sec——千比特每秒。如果您需要千字节，请除以 8。

