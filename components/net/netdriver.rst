.. _netdriver:

===============
网络驱动
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 网络驱动分为两个部分：

#. "上层"通用驱动，为应用层代码提供通用网络接口，
#. "下层"平台相关驱动，实现低层定时器控制以实现网络功能。

支持网络驱动的文件可在以下位置找到：

-  **接口定义**。NuttX 网络驱动的头文件位于
   ``include/nuttx/net/netdev_lowerhalf.h``。此头文件包含
   "上层"和"下层"驱动之间的接口。
-  **"上层"驱动**。通用的"上层"网络驱动位于
   ``drivers/net/netdev_upperhalf.c``。
-  **"下层"驱动**。平台相关的网络驱动位于
   ``arch/<architecture>/src/<hardware>`` 或 ``drivers/net``
   目录中，针对特定的处理器 ``<architecture>`` 和
   特定的 ``<chip>`` 网络外设。

**特别说明**：并非所有网络驱动都使用此架构实现。
已知的下层驱动包括：
``arch/sim/src/sim/sim_netdriver.c``、``drivers/virtio/virtio-net.c``

如何将完整网络驱动改为下层驱动
=====================================================

我们有许多使用 ``include/nuttx/net/netdev.h`` 实现的完整网络驱动，
可以将它们改为下层驱动以移除通用代码（这些代码已在上层驱动中实现）。
以下是操作指南：

1.  将网络驱动结构中的 ``struct net_driver_s`` 改为
    ``struct netdev_lowerhalf_s``。如果确实需要访问
    ``struct net_driver_s`` 中的某些字段（如 MAC 地址），
    可以通过 ``struct netdev_lowerhalf_s::netdev`` 访问。
2.  将网络驱动文件中调用的函数名称改为带有 ``netdev_lower_`` 前缀
    的名称，例如 ``netdev_lower_register`` 和
    ``netdev_lower_carrier_on``。
3.  将工作队列调用的核心函数（如 ``txpoll``）改为
    ``netdev_ops_s`` 结构中的 ``transmit`` 和 ``receive``。
    可能需要将 ``d_buf`` 的 ``memcpy`` 改为 ``netpkt_copyin`` 和
    ``netpkt_copyout``。

    -  注意 ``receive`` 函数只需返回接收到的数据包，
       而不是调用 ``ipv4_input`` 等函数或进行回复。
       上层将调用 ``receive`` 来获取所有数据包，直到它返回 ``NULL``，
       然后将这些数据包发送到网络协议栈。
    -  还要注意对已传输的数据包调用 ``netpkt_free``。

4.  移除与发送和接收相关的工作队列，替换为调用
    ``netdev_lower_txdone`` 和 ``netdev_lower_rxready``。
    然后上层驱动将调用 ``transmit`` 和 ``receive`` 来
    发送/获取数据包。
5.  移除与 ``d_buf`` 相关的缓冲区，确保下层驱动中不使用 ``d_buf``。
6.  移除 ``txavail`` 函数，当上层驱动有数据包要发送时将调用
    ``transmit``。
7.  移除统计宏如 ``NETDEV_TXPACKETS``、``NETDEV_TXDONE``、
    ``NETDEV_RXPACKETS`` 或 ``NETDEV_RXDROPPED``，这些宏在
    上层中已妥善处理。但可以保留 ``NETDEV_TXTIMEOUTS`` 和
    ``NETDEV_RXERRORS`` 等宏，因为上层无法知道这些错误是否发生。
8.  为驱动找到合适的 ``quota``，并在驱动初始化函数中设置。
    quota 是驱动可以同时持有的最大缓冲区数量。
    例如，如果 TX 配额设置为 5，意味着如果驱动有 5 个未释放的
    数据包（``netpkt_free``），上层将不会调用 ``transmit`` 直到
    它们被释放。
9.  为驱动找到合适的 ``rxtype``，并在驱动初始化函数中设置。
    有几种接收通知方法类型，定义在 ``enum netdev_rx_e`` 中，
    如 ``NETDEV_RX_WORK``、``NETDEV_RX_THREAD`` 和
    ``NETDEV_RX_THREAD_RSS``。选择最适合您驱动的类型。
10. 为驱动找到合适的 ``priority``，并在驱动初始化函数中设置。
    这是接收通知工作队列或线程的优先级。当 ``rxtype`` 为
    ``NETDEV_RX_WORK`` 时，它是工作队列 ``qid``；
    当 ``rxtype`` 为 ``NETDEV_RX_THREAD`` 时，它是线程优先级。

    -  注意：有一个例外，如果网络协议栈正在回复 RX 数据包，
       这个回复的数据包将始终被放入 ``transmit``，这可能会
       暂时超过 TX 配额。

"下层"驱动示例
====================

.. code-block:: c

  struct <chip>_priv_s
  {
    /* 这里保存对 NuttX 网络层可见的信息 */

    struct netdev_lowerhalf_s dev;

    ...
  };

  static const struct netdev_ops_s g_ops =
  {
    .ifup     = <chip>_ifup,
    .ifdown   = <chip>_ifdown,
    .transmit = <chip>_transmit,
    .receive  = <chip>_receive,
    .addmac   = <chip>_addmac,
    .rmmac    = <chip>_rmmac,
    .ioctl    = <chip>_ioctl
  };

  /* Wi-Fi 驱动注册函数可以如下实现，
   * 其中 <chip> 指芯片名称。netdev_lower_register() 是
   * 上层驱动提供的用于注册网络设备驱动的网络设备接口。
   */

  int <chip>_netdev_init(FAR struct <chip>_priv_s *priv)
  {
      FAR struct netdev_lowerhalf_s *dev = &priv->dev;

      dev->ops = &g_ops;

      /* 驱动可以同时持有的最大缓冲区数量。
       * 例如，如果 TX 配额设置为 5，意味着如果驱动有 5 个
       * 未释放的数据包（netpkt_free），上层将不会调用 transmit
       * 直到它们被释放。当 rx 配额用完且无法分配新缓冲区
       * （netpkt_alloc）时，需要通知上层（netdev_lower_rxready）
       * 并通过 receive 函数提交缓冲区来恢复配额。
       * 如果驱动逐个处理每个数据包（不在发送/接收前积累多个数据包），
       * 可以将其设置为 1。
       */

      dev->quota[NETPKT_TX] = 1;
      dev->quota[NETPKT_RX] = 1;
      dev->rxtype           = NETDEV_RX_WORK;
      dev->priority         = HPWORK;

      return netdev_lower_register(dev, NET_LL_ETHERNET);
  }

  /* 发送函数可以如下实现，其中 <chip> 指芯片名称。 */

  static int <chip>_transmit(FAR struct netdev_lowerhalf_s *dev,
                             FAR netpkt_t *pkt)
  {
    FAR struct <chip>_priv_s *priv = (FAR struct <chip>_priv_s *)dev;
    unsigned int len = netpkt_getdatalen(dev, pkt);

  #if you want to do offloading
    if (!netpkt_is_fragmented(pkt))
      {
        /* 连续内存，直接使用数据指针 */

        FAR uint8_t *databuf = netpkt_getdata(dev, pkt);
        FAR uint8_t *devbuf  = databuf - sizeof(struct <chip>_txhead_s);

        /* 执行发送。注意：`databuf` 指向 L2 数据，
         * 在 databuf 之前有一个大小为 `CONFIG_NET_LL_GUARDSIZE` 的
         * 保留内存用于驱动头部，驱动可以在那里（`devbuf`）填充数据
         * 并开始传输。
         */

        ...
      }
    else
  #endif
      {
        /* 复制出 L2 数据并发送。 */

        uint8_t devbuf[1600];
        netpkt_copyout(dev, devbuf, pkt, len, 0);

        /* 执行发送 */

        ...
      }

    return OK;
  }

  static void <chip>_txdone_interrupt(FAR struct <chip>_priv_s *priv)
  {
    FAR struct netdev_lowerhalf_s *dev = &priv->dev;

    /* 在驱动中执行一些处理（如有必要） */

    ...

    /* 释放缓冲区并通知上层 */

    netpkt_free(dev, pkt, NETPKT_TX);
    netdev_lower_txdone(dev);
  }

  /* 接收函数可以如下实现，其中 <chip> 指芯片名称。 */

  static void <chip>_rxready_interrupt(FAR struct <chip>_priv_s *priv)
  {
    FAR struct netdev_lowerhalf_s *dev = &priv->dev;
    netdev_lower_rxready(dev);
  }

  static FAR netpkt_t *<chip>_receive(FAR struct netdev_lowerhalf_s *dev)
  {
    /* 也可以提前分配 pkt 并接收数据，
     * 然后调用 rxready 并通过 receive 返回 pkt
     */

    FAR netpkt_t *pkt = netpkt_alloc(dev, NETPKT_RX);

    if (pkt)
      {
  #if NETPKT_BUFLEN > 15xx && you want to do offloading
        /* 直接写入 pkt 内部的缓冲区，len 对应 L2 数据的长度
         * （需要 NETPKT_BUFLEN 足够大以容纳数据）。
         * `<chip>_rxhead_s` 是实际数据之前的驱动头部
         * （可能没有）。
         */

        len = receive_data_into(netpkt_getbase(pkt));
        netpkt_resetreserved(&priv->dev, pkt, sizeof(struct <chip>_rxhead_s));
        netpkt_setdatalen(&priv->dev, pkt, len);
  #else
        uint8_t devbuf[1600];

        /* 从源复制，len 对应 L2 数据的长度，您始终可以
         * 使用此方法接收数据。`<chip>_rxhead_s` 是实际数据
         * 之前的驱动头部（可能没有）。
         */

        len = receive_data_into(devbuf);
        netpkt_copyin(dev, pkt, devbuf + sizeof(struct <chip>_rxhead_s), len, 0);
  #endif
      }

    return pkt;
  }
