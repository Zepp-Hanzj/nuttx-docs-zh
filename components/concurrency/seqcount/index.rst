===============
Seqcount
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
=======

这是一种高效的 ``Seqlock``（顺序锁）机制，适用于频繁读取和罕见写的并发场景。``Seqlock`` 在通过序列计数确保数据一致性的同时实现无锁读取。

核心特性
-------------

1. 无锁读取
~~~~~~~~~~~~~~~~~~~~

- 读取者无需获取锁即可访问共享数据，消除了锁竞争
- 序列号跟踪检测读取操作期间的数据修改
- 重试机制保证读取一致性

2. 写保护
~~~~~~~~~~~~~~~~~~~

- 写入者利用原子操作和中断保护进行独占访问
- 序列号奇偶性指示写入状态（偶数：可读，奇数：正在写入）
- SMP 环境使用内存屏障进行操作排序

主要接口
---------------

初始化
~~~~~~~~~~~~~~

.. code-block:: c

   void seqlock_init(seqcount_t *s);

读操作
~~~~~~~~~~~~~~~

.. code-block:: c

   uint32_t read_seqbegin(const seqcount_t *s);
   uint32_t read_seqretry(const seqcount_t *s, uint32_t start);

读取者使用模式：

.. code-block:: c

   uint32_t seq;
   do {
       seq = read_seqbegin(&seqlock);
       // 读取共享数据
   } while (read_seqretry(&seqlock, seq));

写操作
~~~~~~~~~~~~~~~~

.. code-block:: c

   irqstate_t write_seqlock_irqsave(seqcount_t *s);
   void write_sequnlock_irqrestore(seqcount_t *s, irqstate_t flags);

写入者使用模式：

.. code-block:: c

   irqstate_t flags = write_seqlock_irqsave(&seqlock);
   // 修改共享数据
   write_sequnlock_irqrestore(&seqlock, flags);

技术细节
-----------------

1. 序列号机制
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 序列计数器初始化为 0（偶数）
- 写入开始时递增 1（变为奇数）
- 写入完成时递增 1（返回偶数）

2. 内存屏障
~~~~~~~~~~~~~~~~~~

- SMP 系统使用适当的读/写内存屏障
- ``SMP_WMB()``：写内存屏障
- ``SMP_RMB()``：读内存屏障
- 确保操作排序和内存可见性

3. 原子操作
~~~~~~~~~~~~~~~~~~~~

- SMP 环境采用原子读/写和 CAS 操作
- 防止数据竞争并保持一致性

4. 中断保护
~~~~~~~~~~~~~~~~~~~~~~~

- 写操作禁用中断
- 防止中断处理程序干扰临界区

适用场景
--------------------

- 读操作远多于写操作
- 读取者可以容忍临时的数据不一致
- 需要高性能的读取操作

性能优势
----------------------

- 读取操作完全无锁，开销极小
- 对读密集型应用程序有显著的性能提升

此实现考虑了 SMP 和单处理器环境之间的差异，确保在各种配置下正确运行。
