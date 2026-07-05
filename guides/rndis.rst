.. include:: /substitutions.rst
.. _rndis:

================
如何使用 RNDIS
================

本指南说明了使 USB RNDIS 工作所需的步骤，以 STM32F4Discovery 板为例。

如果你不了解 RNDIS，它是一种在不使用任何外部设备的情况下，通过 USB 端口共享类以太网连接的方式。只需在你的板子（具有 USB Device）和计算机之间连接一根 USB 线即可。

警告：RNDIS 将从 Linux 内核中移除，因为他们认为它是一个不安全的协议。因此使用时请注意此风险，并注意它仅在 Ubuntu 22.04 LTS 上测试过，可能在未来版本中无法工作。

编译
========

#. 配置 RNDIS

   在 stm32f4discovery 板上有一个使用 RNDIS 的示例配置。如果你的板子没有示例配置，那么你需要参考此配置自行创建配置。

   只需使用 ``stm32f4discovery:rndis`` 板配置文件即可。

    .. code-block:: console

       $ cd nuttx
       $ ./tools/configure.sh stm32f4discovery:rndis

#. 编译

    .. code-block:: console

       $ make -j

烧录
========

#. 将生成的 nuttx.bin 烧录到你的板子：

    .. code-block:: console

       $ $ sudo openocd -f interface/stlink.cfg -f target/stm32f4x.cfg -c init -c "reset halt" -c "flash write_image erase nuttx.bin 0x08000000"
       ...
       Open On-Chip Debugger 0.11.0
       ...
       Info : STLINK V2J14S0 (API v2) VID:PID 0483:3748
       Info : Target voltage: 3.203144
       Info : stm32f4x.cpu: hardware has 6 breakpoints, 4 watchpoints
       Info : starting gdb server for stm32f4x.cpu on 3333
       Info : Listening on port 3333 for gdb connections
       target halted due to debug-request, current mode: Thread 
       xPSR: 0x01000000 pc: 0x08000188 msp: 0x20003f24
       Info : device id = 0x10036413
       Info : flash size = 1024 kbytes
       auto erase enabled
       wrote 262144 bytes from file nuttx.bin in 11.043253s (23.182 KiB/s)
       Info : Listening on port 6666 for tcl connections
       Info : Listening on port 4444 for telnet connections


在你的计算机上设置 RNDIS
============================

   以下步骤展示了如何将你的板子连接到 Linux 机器。

.. todo:: 添加 Mac 和 Windows 说明

#. 重置你的板子

#. 将 USB 线从 STM32F4Discovery 的 microUSB 连接到你的计算机

#. 确认你的板子被检测为 USB RNDIS 设备：

    .. code-block:: console

       $ dmesg
       ...
       [ 1099.821480] usb 3-3: new full-speed USB device number 12 using xhci_hcd
       [ 1099.972379] usb 3-3: New USB device found, idVendor=584e, idProduct=5342, bcdDevice= 0.01
       [ 1099.972389] usb 3-3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
       [ 1099.972393] usb 3-3: Product: RNDIS gadget
       [ 1099.972396] usb 3-3: Manufacturer: NuttX
       [ 1099.972398] usb 3-3: SerialNumber: 1234
       [ 1099.988952] usbcore: registered new interface driver cdc_ether
       [ 1099.990144] rndis_host 3-3:1.0: skipping garbage
       [ 1099.990641] rndis_host 3-3:1.0: dev can't take 1558 byte packets (max 660), adjusting MTU to 602
       [ 1099.992089] rndis_host 3-3:1.0 eth0: register 'rndis_host' at usb-0000:00:14.0-3, RNDIS device, a0:e0:de:ad:ca:fe
       [ 1099.992102] usbcore: registered new interface driver rndis_host
       [ 1099.994026] usbcore: registered new interface driver rndis_wlan
       [ 1099.997001] rndis_host 3-3:1.0 enxa0e0deadcafe: renamed from eth0

#. 配置你的 Linux 发行版以将网络共享到此 USB RNDIS 设备：

   点击 Ubuntu 右上角并进入：

   NuttX Ethernet -> Wired Settings

   点击"齿轮图标"并在"IPv4"选项卡中选择："Shared to other computers"

   点击"Apply"

   断开并重新连接 USB 线以强制获取 IP。

#. 确定你的板子获得了哪个 IP 地址：

    .. code-block:: console

       $ tail -f /var/log/syslog
       ...
       Jan 28 10:30:24 dev dnsmasq-dhcp[35526]: DHCPDISCOVER(enxa0e0deadcafe) 00:e0:de:ad:ca:fe 
       Jan 28 10:30:24 dev dnsmasq-dhcp[35526]: DHCPOFFER(enxa0e0deadcafe) 10.42.0.86 00:e0:de:ad:ca:fe 
       Jan 28 10:30:24 dev dnsmasq-dhcp[35526]: DHCPREQUEST(enxa0e0deadcafe) 10.42.0.86 00:e0:de:ad:ca:fe 
       Jan 28 10:30:24 dev dnsmasq-dhcp[35526]: DHCPACK(enxa0e0deadcafe) 10.42.0.86 00:e0:de:ad:ca:fe nuttx
       Jan 28 10:30:29 dev systemd[1]: NetworkManager-dispatcher.service: Deactivated successfully.
       ^C

#. Ping 此 IP 以确认其正常工作：

    .. code-block:: console

       $ ping 10.42.0.86
       PING 10.42.0.86 (10.42.0.86) 56(84) bytes of data.
       64 bytes from 10.42.0.86: icmp_seq=1 ttl=64 time=0.809 ms
       64 bytes from 10.42.0.86: icmp_seq=2 ttl=64 time=0.849 ms
       ^C
       --- 10.42.0.86 ping statistics ---
       2 packets transmitted, 2 received, 0% packet loss, time 1027ms
       rtt min/avg/max/mdev = 0.809/0.829/0.849/0.020 ms

#. 通过 telnet 连接到你的板子：

    .. code-block:: console

       $ telnet 10.42.0.86
       Trying 10.42.0.86...
       Connected to 10.42.0.86.
       Escape character is '^]'.

       NuttShell (NSH) NuttX-12.0.0
       nsh> 
