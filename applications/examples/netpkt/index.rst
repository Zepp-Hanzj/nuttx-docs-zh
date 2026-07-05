====================================
``netpkt`` ``AF_PACKET`` 原始套接字
====================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

一个 ``AF_PACKET`` 原始套接字的测试。由 Lazlo Sitzer 贡献。

概述
========

``netpkt`` 示例演示了使用原始数据包套接字（``AF_PACKET``）在链路层发送和接收以太网帧，
绕过 TCP/IP 协议栈。这对于网络协议测试、驱动验证和低级网络分析非常有用。

配置
=============

- ``CONFIG_EXAMPLES_NETPKT=y`` – 启用 netpkt 示例。

用法
=====

``netpkt`` 程序支持以下命令行选项：

.. code-block:: bash

   netpkt [options]

选项：

- ``-a`` – 发送和接收数据包
- ``-r`` – 仅接收数据包
- ``-t`` – 仅发送数据包
- ``-v`` – 详细模式（以十六进制显示数据包内容）
- ``-i <IF>`` – 指定网络接口名称（例如 ``eth0``）

示例：

.. code-block:: bash

   # Send 3 packets on eth0 interface with verbose output
   netpkt -i eth0 -t -v

   # Receive packets on eth0 interface
   netpkt -i eth0 -r -v

   # Both send and receive on eth0
   netpkt -i eth0 -a -v

   # Send packets without specifying interface (uses default)
   netpkt -t
