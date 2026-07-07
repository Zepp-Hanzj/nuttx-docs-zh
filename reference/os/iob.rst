=====================
I/O 缓冲区管理
=====================

NuttX 支持通用 I/O 缓冲区管理 (IOB) 逻辑。此逻辑最初是为了支持网络 I/O 缓冲而添加的，但已扩展为满足所有设备驱动程序的缓冲需求。在撰写本文时，IOB 目前不仅用于网络，还用于 ``drivers/syslog`` 和 ``drivers/wireless`` 中的逻辑。请注意，本节中的一些措辞仍然反映了其作为网络子系统一部分的传统根源。此功能的目标是：

  #. 为所有驱动程序提供通用的 I/O 缓冲区管理逻辑，
  #. 支持从任务级和中断级上下文进行 I/O 缓冲区分配。
  #. 使用固定数量的预分配内存。
  #. 没有昂贵的、非确定性的动态内存分配。
  #. 当固定数量的预分配 I/O 缓冲区用尽时，任务逻辑的进一步分配尝试将导致任务阻塞并等待，直到 I/O 缓冲区被释放。
  #. 每个 I/O 缓冲区应该很小，但可以链接在一起以支持更大内容的缓冲，例如全尺寸网络数据包。
  #. 支持 *节流* 逻辑，以防止低优先级任务占用所有可用的 I/O 缓冲。

配置选项
=====================

``CONFIG_MM_IOB``
   启用通用 I/O 缓冲区支持。此设置将构建通用 I/O 缓冲区 (IOB) 支持库。
``CONFIG_IOB_NBUFFERS``
   预分配的 I/O 缓冲区数量。每个数据包由一系列小型 I/O 缓冲区链接表示。此设置确定可用于数据包数据的预分配 I/O 缓冲区数量。默认值是为网络支持设置的。如果既未启用 TCP/UDP 也未启用写入缓冲（既不是 ``CONFIG_NET_TCP_WRITE_BUFFERS`` 也不是 ``CONFIG_NET_TCP``），则默认为 8 个缓冲区；如果仅启用 TCP/UDP，则为 24 个；如果同时启用 TCP/UDP 和写入缓冲，则为 36 个。
``CONFIG_IOB_BUFSIZE``
   一个 I/O 缓冲区的有效载荷大小。每个数据包由一系列小型 I/O 缓冲区链接表示。此设置确定每个预分配 I/O 缓冲区的数据有效载荷。默认值为 196 字节。
``CONFIG_IOB_NCHAINS``
   预分配的 I/O 缓冲区链头数量。这些微小节点用作 *容器* 以支持 I/O 缓冲区链的排队。这将限制在任何给定时间可以 *在途* 的 I/O 事务数量。默认值零禁用此功能。
   这些通用 I/O 缓冲区链容器目前未被 NuttX 中的任何逻辑使用。这是因为存在其他专门的 I/O 缓冲区链容器，它们还携带特定于使用的信息有效载荷。如果既未启用 TCP 也未启用 UDP（即既不是 ``CONFIG_NET_TCP`` 也不是 ``CONFIG_NET_UDP``），则默认值为零；如果启用了其中任一，则为八。
``CONFIG_IOB_THROTTLE``
   I/O 缓冲区节流值。TCP 写入缓冲和预读缓冲使用相同的空闲 I/O 缓冲区池。为了防止不受控制的传入 TCP 数据包占用所有可用的预分配 I/O 缓冲区，需要节流值。此节流值确保在 TCP 写入停止之前，I/O 缓冲区将被拒绝用于预读逻辑。
   如果既未启用 TCP 写入缓冲也未启用 TCP 预读缓冲，则默认为 0。否则，默认为 8。
``CONFIG_IOB_DEBUG``
   强制 I/O 缓冲区调试。此选项将强制来自 I/O 缓冲区逻辑的调试输出。通常这不是您想要做的事情，但如果您正在调试 I/O 缓冲区逻辑并且不想被其他不相关的调试输出淹没，则很方便。请注意，如果未启用 DEBUG 功能（``CONFIG_DEBUG_FEATURES``）且 IOB 正在用于 syslog 缓冲逻辑（``CONFIG_SYSLOG_BUFFER``），则此选择不可用。

节流
==========

添加了分配节流。I/O 缓冲区分配逻辑支持节流值，最初是为了预读缓冲，以防止预读逻辑消耗所有可用的 I/O 缓冲区并阻塞写入缓冲逻辑。只有同时使用写入缓冲和预读缓冲时，才需要网络的节流逻辑。I/O 缓冲的使用可能有其他节流动机。

公共类型
============

此结构表示一个 I/O 缓冲区。一个数据包由链中的一个或多个 I/O 缓冲区包含。``io_pktlen`` 仅对链头部的 I/O 缓冲区有效。

.. code-block:: c

   struct iob_s
   {
     /* Singly-link list support */

     FAR struct iob_s *io_flink;

     /* Payload */

   #if CONFIG_IOB_BUFSIZE < 256
     uint8_t  io_len;      /* Length of the data in the entry */
     uint8_t  io_offset;   /* Data begins at this offset */
   #else
     uint16_t io_len;      /* Length of the data in the entry */
     uint16_t io_offset;   /* Data begins at this offset */
   #endif
     uint16_t io_pktlen;   /* Total length of the packet */

     uint8_t  io_data[CONFIG_IOB_BUFSIZE];
   };

此容器结构支持 I/O 缓冲区链的排队。此结构仅供 IOB 模块内部使用。

.. code-block:: c

   #if CONFIG_IOB_NCHAINS > 0
   struct iob_qentry_s
   {
     /* Singly-link list support */

     FAR struct iob_qentry_s *qe_flink;

     /* Payload -- Head of the I/O buffer chain */

     FAR struct iob_s *qe_head;
   };
   #endif /* CONFIG_IOB_NCHAINS > 0 */

I/O 缓冲区队列头结构。

.. code-block:: c

   #if CONFIG_IOB_NCHAINS > 0
   struct iob_queue_s
   {
     /* Head of the I/O buffer chain list */

     FAR struct iob_qentry_s *qh_head;
     FAR struct iob_qentry_s *qh_tail;
   };
   #endif /* CONFIG_IOB_NCHAINS > 0 */

公共函数原型
==========================

  - :c:func:`iob_initialize()`
  - :c:func:`iob_alloc()`
  - :c:func:`iob_tryalloc()`
  - :c:func:`iob_free()`
  - :c:func:`iob_free_chain()`
  - :c:func:`iob_add_queue()`
  - :c:func:`iob_tryadd_queue()`
  - :c:func:`iob_remove_queue()`
  - :c:func:`iob_peek_queue()`
  - :c:func:`iob_free_queue()`
  - :c:func:`iob_free_queue_qentry()`
  - :c:func:`iob_get_queue_size()`
  - :c:func:`iob_copyin()`
  - :c:func:`iob_trycopyin()`
  - :c:func:`iob_copyout()`
  - :c:func:`iob_clone()`
  - :c:func:`iob_clone_partial()`
  - :c:func:`iob_concat()`
  - :c:func:`iob_trimhead()`
  - :c:func:`iob_trimhead_queue()`
  - :c:func:`iob_trimtail()`
  - :c:func:`iob_pack()`
  - :c:func:`iob_contig()`
  - :c:func:`iob_count()`
  - :c:func:`iob_dump()`

.. c:function:: void iob_initialize(void);

  设置 I/O 缓冲区以进行正常操作。

.. c:function:: FAR struct iob_s *iob_alloc(bool throttled);

  通过获取空闲列表头部的缓冲区来分配 I/O 缓冲区。

.. c:function:: FAR struct iob_s *iob_tryalloc(bool throttled);

  尝试通过获取空闲列表头部的缓冲区来分配 I/O 缓冲区，而不等待缓冲区变为空闲。

.. c:function:: FAR struct iob_s *iob_free(FAR struct iob_s *iob);

  释放缓冲区链头部的 I/O 缓冲区，将其返回到空闲列表。返回链中下一个 I/O 缓冲区的链接。

.. c:function:: void iob_free_chain(FAR struct iob_s *iob);

  释放整个缓冲区链，从 I/O 缓冲区链的开头开始。

.. c:function:: int iob_add_queue(FAR struct iob_s *iob, FAR struct iob_queue_s *iobq)

  将一个 I/O 缓冲区链添加到队列末尾。可能因资源不足而失败。

.. c:function:: void iob_tryadd_queue(FAR struct iob_s *iob, FAR struct iob_queue_s *iobq)

  将一个 I/O 缓冲区链添加到队列末尾，而不等待资源变为空闲。

.. c:function:: FAR struct iob_s *iob_remove_queue(FAR struct iob_queue_s *iobq);

  从队列头部移除并返回一个 I/O 缓冲区链。

  :return: 返回队列头部 I/O 缓冲区链的引用。

.. c:function:: FAR struct iob_s *iob_peek_queue(FAR struct iob_queue_s *iobq)

  返回队列头部 I/O 缓冲区链的引用。这与 iob_remove_queue 类似，只是 I/O 缓冲区链保留在队列头部。调用者可以安全地修改 I/O 缓冲区链，但在释放之前必须将其从队列中移除。

  :return: 返回队列头部 I/O 缓冲区链的引用。

.. c:function:: void iob_free_queue(FAR struct iob_queue_s *qhead);

  释放整个 I/O 缓冲区链队列。

.. c:function:: void iob_free_queue_qentry(FAR struct iob_s *iob, \
                  FAR struct iob_queue_s *iobq);

  获取 iob 队列缓冲区大小的队列辅助函数。

.. c:function:: unsigned int iob_get_queue_size(FAR struct iob_queue_s *queue);

  释放 iob 整个 I/O 缓冲区链队列。

.. c:function:: int iob_copyin(FAR struct iob_s *iob, FAR const uint8_t *src, \
                  unsigned int len, unsigned int offset, bool throttled);

  从用户缓冲区复制 ``len`` 字节的数据到 I/O 缓冲区链中，从 ``offset`` 开始，根据需要扩展链。

.. c:function:: int iob_trycopyin(FAR struct iob_s *iob, FAR const uint8_t *src, \
                     unsigned int len, unsigned int offset, bool throttled);

  从用户缓冲区复制 ``len`` 字节的数据到 I/O 缓冲区链中，从 ``offset`` 开始，根据需要扩展链，但如果缓冲区不可用则不等待。

.. c:function:: int iob_copyout(FAR uint8_t *dest, FAR const struct iob_s *iob, \
                   unsigned int len, unsigned int offset);

  从 I/O 缓冲区的 ``offset`` 开始复制 ``len`` 字节的数据到用户缓冲区，返回实际复制的字节数。

.. c:function:: int iob_clone(FAR struct iob_s *iob1, FAR struct iob_s *iob2, \
                   bool throttled, bool block)

  在 ``iob2`` 中复制（并打包）``iob1`` 中的数据。``iob2`` 必须为空。

.. c:function:: int iob_clone_partial(FAR struct iob_s *iob1, unsigned int len, \
                      unsigned int offset1, FAR struct iob_s *iob2, \
                      unsigned int offset2, bool throttled, bool block);

  从 ``iob1`` 的部分字节复制数据到 ``iob2``。

.. c:function:: void iob_concat(FAR struct iob_s *iob1, FAR struct iob_s *iob2)

  将 iob_s 链 iob2 连接到 iob1。

.. c:function:: FAR struct iob_s *iob_trimhead(FAR struct iob_s *iob, \
                   unsigned int trimlen)

  从 I/O 链的开头移除字节。已清空的 I/O 缓冲区将被释放，因此链的开头可能会更改。

.. c:function:: FAR struct iob_s *iob_trimhead_queue(FAR struct iob_queue_s *qhead, \
                                        unsigned int trimlen);

  从队列头部的 I/O 链的开头移除字节。已清空的 I/O 缓冲区将被释放，因此队列头部可能会更改。

  此函数只是 iob_trimhead() 的包装器，确保队列头部的 iob 通过修剪操作进行修改。

  :return: 返回队列头部的新 iob。

.. c:function:: FAR struct iob_s *iob_trimtail(FAR struct iob_s *iob, \
                                        unsigned int trimlen);

  从 I/O 链的末尾移除字节。已清空的 I/O 缓冲区将被释放，在输入 I/O 缓冲区链被释放的特殊情况下将返回 NULL。

.. c:function:: FAR struct iob_s *iob_pack(FAR struct iob_s *iob);

  打包 I/O 缓冲区链中的所有数据，使数据偏移量为零，并且链中除最后一个缓冲区外的所有缓冲区都已填满。链末尾的任何已清空缓冲区将被释放。

.. c:function:: int iob_contig(FAR struct iob_s *iob, unsigned int len);

  确保从 ``iob`` 开始的 I/O 缓冲区链的开头有 ``len`` 字节的连续空间。

.. c:function:: int iob_count(FAR struct iob_s *iob);

  获取链中 ``iob`` 条目的数量。

.. c:function:: void iob_dump(FAR const char *msg, FAR struct iob_s *iob, unsigned int len, \
                 unsigned int offset);

  转储 I/O 缓冲区链的内容。
