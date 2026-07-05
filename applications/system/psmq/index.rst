========================================
``psmq`` 发布订阅消息队列
========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``psmq`` 是发布订阅消息队列。它是一组程序和库，用于在 POSIX 消息队列之上实现
发布/订阅方式的进程间通信。

手册、源代码和更多信息请访问：https://psmq.bofc.pl

使用 ``psmqd`` 代理、``psmq_pub`` 和 ``psmq_sub`` 的简单演示：

启动代理并使其记录到文件::

  nsh> psmqd -b/brok -p/sd/psmqd/psmqd.log &

启动订阅线程，读取 ``/can/*`` 和 ``/adc/*`` 主题上发送的所有消息，
并将所有读数转储到文件::

  nsh> psmq_sub -n/sub -b/brok -t/can/* -t/adc/* -o/sd/psmq-sub/can.log &
  n/connected to broker /brok
  n/subscribed to: /can/*
  n/subscribed to: /adc/*
  n/start receiving data
  n/reply timeout set 100

发布一些消息::

  nsh> psmq_pub -b/brok -t/can/engine/rpm -m50
  nsh> psmq_pub -b/brok -t/adc/volt -m30
  nsh> psmq_pub -b/brok -t/can/room/10/temp -m23
  nsh> psmq_pub -b/brok -t/pwm/fan1/speed -m300

查看订阅线程日志::

  nsh> cat /sd/psmq-sub/can.log

  [2021-05-23 17:53:59] p:0 l:   3  /can/engine/rpm  50
  [2021-05-23 17:53:59] p:0 l:   3  /adc/volt  30
  [2021-05-23 17:53:59] p:0 l:   3  /can/room/10/temp  23

如您所见，``/pwm/fan1/speed`` 没有被订阅线程接收到，因为我们没有订阅它。

内容：

- ``psmqd`` – 代理，在客户端之间转发消息。
- ``psmq_sub`` – 监听指定主题，可用作通信记录器（可选）。
- ``psmq_pub`` – 直接从 shell 发布消息。可以发送二进制数据，但需要管道，
  因此在 NuttX 上只能发送 ASCII 数据。
- ``libpsmq`` – 用于与代理通信以及发送/接收消息的库。
