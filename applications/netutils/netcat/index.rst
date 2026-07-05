======================
``netcat`` NetCat 工具
======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

netcat TCP/IP 瑞士军刀。

它是为 NuttX 从头重新实现的。

演示
----

.. image:: https://files.mastodon.social/media_attachments/files/105/163/916/892/863/178/original/05468e28b4463f95.png

* https://mastodon.social/@rzr/105225153152922220#weboftwins-osvehicle-2020-rzr
* https://purl.org/rzr/weboftwins

用法
-----

使用方法很简单::

    nsh> help ; netcat
    Usage: netcat [-l] [destination] [port] [file]

    nsh> renew eth0 ; ifconfig

    eth0    Link encap:Ethernet HWaddr 52:13:FF:FF:FF:FF at UP
            inet addr:192.168.1.42 DRaddr:192.168.1.254 Mask:255.255.255.0

在以下示例中，使用以下配置：

- 目标（nuttx）为 192.168.1.42
- 主机（linux）为 192.168.1.55

服务器
~~~~~~

作为 NuttX 上的服务器，Linux 的 netcat 作为客户端::

    nsh> netcat -l

    sh> cat /proc/version | netcat 192.168.1.42 31337
    Linux ...

默认端口为 31337，但可以更改::

    nsh> renew eth0 ; ifconfig ; netcat -l
    log: net: listening on :31337
    Linux ...

客户端
~~~~~~

在 GNU/Linux 上启动服务器::

    sh> ip addr show && netcat -l 31337

NuttX 上的客户端::

    nsh> help ; renew eth0 ; ifconfig
    nsh> netcat 192.168.1.55 31337 /proc/version

使用管道
~~~~~~~~~~~

.. code-block:: bash

   mkfifo /dev/fifo
   netcat 192.168.1.55 31337 /proc/fifo
   help > /dev/fifo

   fxos8700cq > /dev/fifo &
   fxos8700cq [7:100]
   netcat 192.168.1.55 31337  /dev/fifo

资源
~~~~~~~~~

* <https://en.wikipedia.org/wiki/Netcat>
* <https://purl.org/rzr/weboftwins>
* <https://github.com/rzr/aframe-smart-home/issues/3>
