=============================
测试 TCP/IP 网络协议栈
=============================

在开发网络协议栈时，需要测试和验证所做的更改。虽然问题可能偶然被发现，但很难重现这种情况。以下部分展示了一些对目标进行压力测试或生成特定流量的方法。

在示例中，目标的 IP 地址为 192.168.2.135

SYN 洪泛攻击
================

向目标发送大量 SYN 数据包以耗尽其资源。这是测试网络驱动缓冲区管理的好方法。

.. code-block:: bash

   sudo hping3 --flood -S -p 80 192.168.2.135

使用 Scapy 构建数据包
===========================

一个出色的网络测试工具是 Scapy 库。它使你能够构建几乎任何你需要的测试数据包组合。

你需要添加一个 iptables 规则来阻止来自操作系统网络协议栈的传出 RST 数据包，因为它对我们的测试连接一无所知。

禁用传出 RST 数据包：

.. code-block:: bash

   sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -d 192.168.2.135 -j DROP

移除规则：

.. code-block:: bash

   sudo iptables -D OUTPUT -p tcp --tcp-flags RST RST -d 192.168.2.135 -j DROP

**测试重传行为**

当只发送三次握手时，目标应该超时并重置连接。

以下 Python Scapy 脚本启动一个 HTTP 请求而不进一步响应。协议栈应该开始重传数据包并最终超时。

.. code-block:: python

   #!/usr/bin/env python
 
   import logging
   logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
   from scapy.all import *
 
   get = 'GET / HTTP/1.1\r\n\r\n'
 
   ip = IP(dst="192.168.2.135")
   port = RandNum(1024, 65535)
 
   # Create SYN packet
   SYN = ip/TCP(sport=port, dport=80, flags="S", seq=42)
 
   # Send SYN and receive SYN,ACK
   SYNACK = sr1(SYN)
 
   # Create ACK with GET request
   ACK = ip/TCP(sport=SYNACK.dport, dport=80, flags="A", seq=SYNACK.ack, ack=SYNACK.seq + 1)
 
   # SEND our ACK
   send(ACK)
 
   reply, err = sr(ip/TCP(sport=SYNACK.dport, dport=80, flags="A", seq=SYNACK.ack, ack=SYNACK.seq + 1) / get)

模拟丢包
======================

通过模拟丢包，可以测试目标协议栈的重传行为。

开始丢包：

.. code-block:: bash

   # 随机丢弃 10% 的传入数据包：
   sudo iptables -A INPUT -m statistic --mode random --probability 0.1 -j DROP
 
   # 丢弃 10% 的传出数据包：
   sudo iptables -A OUTPUT -m statistic --mode random --probability 0.1 -j DROP

移除规则：

.. code-block:: bash

   # 传入数据包：
   sudo iptables -D INPUT -m statistic --mode random --probability 0.1 -j DROP
 
   # 传出数据包：
   sudo iptables -D OUTPUT -m statistic --mode random --probability 0.1 -j DROP

模糊测试
============

对于网络应用程序的模糊测试，可以使用出色的
`SPIKE <https://www.immunitysec.com/resources-freesoftware.shtml>`_ 工具。要在 Ubuntu 14.04 LTS 下编译，你需要将 ``-fno-stack-protector`` 添加到 CFLAGS。

SPIKE 报怨缺少 SSL 库。我只是将现有的链接到需要的文件名::

  /lib/i386-linux-gnu$ sudo ln -s ./libssl.so.1.0.0 ./libssl.so.0
  /lib/i386-linux-gnu$ sudo ln -s ./libcrypto.so.1.0.0 ./libcrypto.so.0

也许这些库版本不是 SPIKE 期望的，但如果你不使用 SSL，它工作得很好。

SPIKE 提供了一个代理服务器来记录对你 Web 应用程序的请求。基于这些请求，可以生成针对应用程序的模糊测试。

.. code-block:: bash

   ~/SPIKE/src$ mkdir requests && cd requests
   # 记录对目标 192.168.2.135 端口 80 的请求
   ~/SPIKE/src/requests$ ../webmitm -t 192.168.2.135 -p 80

现在通过 localhost 使用你的 Web 应用程序来记录一些请求。然后你可以从记录的请求生成针对应用程序的模糊测试。

.. code-block:: bash

   ~/SPIKE/src$ ./makewebfuzz.pl ./requests/http_request-1.0 > myfuzz.c
   ~/SPIKE/src$ gcc ./myfuzz.c -I../include -o myfuzz -L. -ldlrpc -ldl

现在你可以对目标进行模糊测试：

.. code-block:: bash

   ~/SPIKE/src$ LD_LIBRARY_PATH=. ./myfuzz 192.168.2.135 80
