===================
Memory Management
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本页讨论 NuttX 内存管理逻辑。

.. toctree::
   :maxdepth: 1

   shm

标准内存管理函数
------------------------------------

标准函数
~~~~~~~~~~~~~~~~~~

标准内存管理函数的原型在 stdlib.h 中定义，如 IEEE Std 1003.1-2001 的基本定义卷所规定。这包括以下文件：

* 标准接口：``mm_malloc.c``、``mm_calloc.c``、``mm_realloc.c``、``mm_memalign.c``、``mm_free.c``
* 较不标准的接口：``mm_zalloc.c``、``mm_mallinfo.c``
* 内部实现：``mm_initialize.c``、``mm_sem.c``、``mm_addfreechunk.c``、``mm_size2ndx.c``、``mm_shrinkchunk.c``
* 构建和配置文件：``Kconfig``、``Makefile``

内存模型
~~~~~~~~~~~~~

* 小内存模型。如果 MCU 仅支持 16 位数据寻址，则自动使用小内存模型。堆的最大大小为 64K。通过在 NuttX 配置文件中定义 CONFIG_SMALL_MEMORY，也可以在具有更宽寻址的 MCU 上强制使用小内存模型。
* 大内存模型。否则，分配器使用支持最大 4G 堆的模型。

  此实现使用具有以下属性的可变长度分配器：

     * 开销：大模型和小模型每次分配分别需要 8 字节或 4 字节。
     * 对齐：大模型和小模型的所有分配分别对齐到 8 字节或 4 字节。

多堆管理
~~~~~~~~~~~~~~

此分配器可用于管理多个堆（尽管使用了一些非标准接口）。堆由 ``mm/include/nuttx/mm/mm.h`` 中定义的 ``struct mm_heap_s`` 表示。要创建另一个堆实例，您需要分配一个堆结构，最可能是在内存中静态分配：

.. code-block:: C

   include <nuttx/mm/mm.h>
   static struct mm_heap_s *g_myheap;

然后使用以下方式初始化堆：

.. code-block:: C

   g_myheap = mm_initialize(myheap_start, myheap_size);

其中 ``mm_initialize()`` 和所有相关接口在头文件 ``include/nuttx/mm/mm.h`` 中声明。

新的堆实例初始化后，可以使用这些几乎熟悉的接口：``mm_malloc()``、``mm_realloc()``、``mm_free()`` 等。这些接口"几乎熟悉"是因为它们类似于标准的 ``malloc()``、``realloc()``、``free()`` 等，只是它们期望一个对已初始化堆结构的引用作为第一个参数。

事实上，标准的 ``malloc()``、``realloc()``、``free()`` 使用相同的机制，只是使用一个名为 ``g_mmheap`` 的全局堆结构。

用户/内核堆
~~~~~~~~~~~~~~~~~

这种多堆能力在一些更复杂的 NuttX 构建配置中被利用，以提供分离的内核模式和用户模式堆。

子目录
~~~~~~~~~~~~~~~

- ``mm/mm_heap`` - 包含所有堆分配器的通用基础逻辑
- ``mm/umm_heap`` - 包含用户模式内存分配接口
- ``mm/kmm_heap`` - 包含内核模式内存分配接口

调试
~~~~~~~~~

请按照以下步骤挂钩所有内存相关例程：

1. 添加一个新的头文件（例如 ``xxx_malloc.h``）：

   .. code-block:: C

     ...
     #include <malloc.h>
     #include <stdlib.h>
     #include <string.h>
     #include <strings.h>

     #ifndef __ASSEMBLY__
     FAR void *xxx_malloc(FAR const char *file, int line, size_t size);
     void xxx_free(FAR const char *file, int line, FAR const void *ptr);
     FAR void *xxx_memcpy(FAR const char *file, int line,
                           FAR void *dst, FAR const void *src, size_t len);
     ...
     #define malloc(s) xxx_malloc(__FILE__, __LINE__, s)
     #define free(p) xxx_free(__FILE__, __LINE__, p)
     #define memcpy(d, s, l) xxx_memcpy(__FILE__, __LINE__, d, s, l)
     ...
     #endif
     ...

2. 在源代码中实现 ``xxx_malloc``、``xxx_free``、``xxx_memcpy``...，您可以：

   - 修改某些参数（例如为红区扩展分配大小）
   - 检查范围内的关键参数（例如指针和长度）
   - 转发到原始实现（调用 malloc/free/memcpy）
   - 在返回前附加上下文信息（例如文件和行号）

3. 通过以下方式之一启用钩子：

   - 在您的源代码中包含 ``xxx_malloc.h`` 以挂钩单个文件
   - 将 ``-include xxx_malloc.h`` 添加到 ``CFLAGS`` 以挂钩所有源代码

颗粒分配器
-----------------

此目录中还提供了一个非标准的颗粒分配器。颗粒分配器以固定大小的块（"颗粒"）为单位分配内存。分配可以对齐到用户提供的地址边界。

颗粒分配器接口在 ``nuttx/include/nuttx/mm/gran.h`` 中定义。颗粒分配器由此目录中的以下文件组成：``mm_gran.h``、``mm_granalloc.c``、``mm_grancritical.c``、``mm_granfree.c``、``mm_graninit.c``

截至撰写本文时，颗粒分配器未在基本 NuttX 代码中的任何地方使用。颗粒分配器的目的是提供一个工具来支持平台特定的对齐 DMA 内存管理。

注意：由于每个颗粒可能被对齐且每次分配以颗粒大小为单位，选择颗粒大小很重要：较大的颗粒将提供更好的性能和更少的开销，但由于量化浪费会有更多的内存损失。额外的内存浪费可能来自对齐；当然，除非 (a) 您正在使用颗粒分配器管理 DMA 内存且 (b) 您的硬件有特定的内存对齐要求，否则不应使用堆对齐。

当前实现还将最大分配大小限制为 32 个颗粒。此限制可以通过一些额外的编码工作消除，但目前需要较大的颗粒大小才能进行较大的分配。

通用使用示例
~~~~~~~~~~~~~~~~~~~~~

这是一个使用 GCC section 属性在内存中定位 DMA 堆的示例（链接器脚本中的逻辑会将 .dmaheap section 分配到 DMA 内存）：

.. code-block:: C

   FAR uint32_t g_dmaheap[DMAHEAP_SIZE] locate_data(.dmaheap);

通过调用 gran_initialize 创建堆。此处颗粒大小设置为 64 字节，对齐设置为 16 字节：

.. code-block:: C

   GRAN_HANDLE handle = gran_initialize(g_dmaheap, DMAHEAP_SIZE, 6, 4);

然后可以使用 ``GRAN_HANDLE`` 分配内存：

.. code-block:: C

   FAR uint8_t *dma_memory = (FAR uint8_t *)gran_alloc(handle, 47);

实际分配的内存为 64 字节（浪费 17 字节），并且将至少对齐到 (``1 << log2align``)。

子目录：

- ``mm/mm_gran`` - 包含颗粒分配逻辑

页分配器
--------------

页分配器是颗粒分配器的一个应用。它是一个专用内存分配器，旨在为具有内存管理单元 (MMU) 的系统分配物理内存页。

子目录：

- ``mm/mm_gran`` - 页分配器与颗粒分配器共存于同一目录。

共享内存管理
------------------------

当 NuttX 在具有分离的特权内核模式地址空间和多个非特权用户模式地址空间的内核模式下构建时，还必须管理共享内存区域。共享内存区域是用户可访问的内存区域，可以附加到用户进程地址空间以在用户进程之间共享。

子目录：

- ``mm/shm`` - 共享内存逻辑

共享内存管理逻辑有自己的页面，可以在 :doc:`shm` 找到。

I/O 缓冲区
-----------

iob 子目录包含一个简单的 I/O 缓冲区分配器。这些 I/O 缓冲区（IOB）在网络中被广泛使用，但通常也可供驱动使用。I/O 缓冲区具有以下属性：

#. 使用固定数量的固定大小缓冲区的池。
#. 空闲缓冲区保存在空闲列表中：当缓冲区被分配时，它从空闲列表中移除；当缓冲区被释放时，它返回到空闲列表。
#. 如果没有空闲缓冲区，调用应用程序将等待。
#. IOB 可以链接在一起形成更大的缓冲区。
#. 扩展接口 ``iob_init_with_data`` 在启用 CONFIG_IOB_ALLOC 时支持将外部缓冲区初始化为 iob 结构。此接口允许不同的协议模块使用自己独特的 I/O 缓冲区源和分配策略，而不会相互干扰。
