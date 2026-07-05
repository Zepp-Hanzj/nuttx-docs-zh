===============================
将驱动移植到 STM32 F7
===============================

.. warning:: 
    迁移自： 
    https://cwiki.apache.org/confluence/display/NUTTX/Porting+Drivers+to+the+STM32+F7

问题陈述
=================

我最近完成了到 STMicro STM32F746G Discovery 板的移植。
该 MCU 显然是 STM32 F3/F4 的衍生产品，许多外设实际上与 STM32F429 基本相同。
最大的区别是 STM32F746 配备了 Cortex-M7，它包含对 Cortex-M4 的多项改进，
其中与本讨论最相关的是完全集成的数据缓存（`D-Cache`）。

由于这一个差异，我选择将 STM32 F7 代码放在与 STM32 F1、F2、F3 和 F4
分开的独立目录中。

移植简单驱动
======================

一些 STM32 F4 驱动可以非常简单地用于 STM32 F7；
许多移植只需复制文件和一些搜索替换即可。例如：

* 比较两个寄存器定义文件；确保 STM32 F4 外设与 F7 外设相同（或几乎相同）。
  如果是，则
* 将寄存器定义文件从 ``stm32/hardware`` 复制到 ``stm32f7/hardware`` 目录，
  适当进行名称更改并更新任何微小的寄存器差异。
* 将相应的 C 文件（可能还有 ``.h`` 文件）从 ``stm32/`` 目录复制到
  ``stm32f7/`` 目录，同样进行任何命名更改和寄存器差异的修改。
* 更新 ``Make.defs`` 文件以在构建中包含新的 C 文件。

移植复杂驱动
=======================

然而，Cortex-M7 D-Cache 确实引发了大多数复杂 STM32 F4 和 F7 驱动的
兼容性问题。即使 STM32F429 和 STM32F746 之间的外设寄存器基本相同，
STM32F429 的许多驱动也无法直接兼容 STM32F746，
特别是使用 DMA 的驱动。这包括大多数复杂的 STM32 驱动！

缓存一致性
===============

使用 DMA 时，物理 RAM 内存内容由外设硬件直接访问，
无需 CPU 干预。CPU 本身仅通过 D-Cache 间接处理 RAM：
当你从 RAM 读取数据时，它首先加载到 D-Cache 中，
然后由 CPU 访问。如果 RAM 内容已在 D-Cache 中，
则根本不访问物理 RAM！类似地，当你将数据写入 RAM
（启用写缓冲时），它实际上可能不会写入物理 RAM，
而可能只是保留在 D-Cache 中的 `脏` 缓存行中，
直到该缓存行被刷新到内存。因此，由于 DMA 相关的原因，
D-Cache 的内容和物理 RAM 的内容可能存在不一致。
此类问题被称为 `缓存一致性` 问题。

DMA
===

DMA 读访问
-----------------

当我们编程 DMA 硬件从外设读取数据并将其存储到 RAM 中时，
发生 DMA 读访问。例如，当我们从网络读取数据包时、
当我们从 UART 读取串行数据字节时、
当我们从 MMC/SD 卡读取块时等等。

在这种情况下，DMA 硬件将在 CPU 不知情的情况下更改物理 RAM 的内容。
因此，如果被 DMA 读操作修改的同一内存也在 D-Cache 中，
那么 D-Cache 的内容将不再有效；它将不再与内存的物理内容匹配。
为了解决这个问题，Cortex-M7 支持一种特殊的 `缓存操作`，
可用于 `使无效` 与读 DMA 缓冲区地址范围关联的 D-Cache 内容。
使无效只是意味着丢弃当前缓存的 D-Cache 行，
以便从物理 RAM 重新获取它们。**规则 1a**：始终在启动读 DMA 之前
或之后的某个时间使 RX DMA 缓冲区无效，但肯定在访问读缓冲区数据 `之前`。
**规则 1b**：在读 DMA 缓冲区完成之前，永远不要从读 DMA 缓冲区读取，
否则你将重新缓存 DMA 缓冲区内容。

`如果 D-Cache 行也是脏的怎么办？如果我们有从未刷新到物理 RAM 的
对 DMA 缓冲区的写入怎么办？` 如果 D-Cache 被使无效，
这些写入将永远不会到达物理内存。**规则 2**：永远不要写入读 DMA 缓冲区内存！
**规则 3**：确保所有读 DMA 缓冲区都与 D-Cache 行大小对齐，
以便在使无效的缓存行边界处没有溢出缓存效应。

DMA 写访问
------------------

当我们编程 DMA 硬件将数据从 RAM 写入外设时，发生 DMA 写访问。
例如，当我们在网络上发送数据包或向 MMC/SD 卡写入数据块时。
在这种情况下，硬件期望在执行写 DMA 时物理 RAM 中有正确的数据。
如果没有，则将发送错误的数据。

我们通过 `清理`（或 `刷新`）`脏` 缓存行来确保没有挂起的写入；
即，强制 D-Cache 行中的任何挂起写入被写入物理 RAM。
**规则 4**：始终 `清理`（或 `刷新`）D-Cache 以强制所有数据
从 D-Cache 写入物理 RAM。

`如果你有两个相邻的 DMA 缓冲区并排放置怎么办？
清理写缓冲区不会强制写入相邻的读缓冲区吗？` 是的！
**规则 5**：确保所有写 DMA 缓冲区都与 D-Cache 行大小对齐，
以便在清理的缓存行边界处没有溢出缓存效应。

写回与写透 D-Cache
------------------------------------

Cortex-M7 支持 `写回` 和 `写透` 两种数据缓存配置。
写回 D-Cache 的工作方式如上所述：`脏` 缓存行不会写入物理内存，
直到缓存行被刷新。但写透 D-Cache 的工作方式与没有 D-Cache 一样。
写入始终直接进入物理 RAM。

`如果我使用写透 D-Cache，我不能就忘记清理 D-Cache 吗？` 不行，
因为你不知道用户将如何配置 D-Cache。**规则 6**：始终假设正在执行
`写回` 缓存；否则，你的驱动将不可移植。

你可能在 ``/arch/arm/src/armv7-m/cache.h`` 中注意到：

.. code-block:: c

    #if defined(CONFIG_ARMV7M_DCACHE) && !defined(CONFIG_ARMV7M_DCACHE_WRITETHROUGH)
    void arch_clean_dcache(uintptr_t start, uintptr_t end);
    #else
    #  define arch_clean_dcache(s,e)
    #endif

注意：我经历过其他情况（在 SAMV7 上）写缓冲 `必须` 被禁用：
在一种情况下，某个外设在数组中使用 16 字节的 DMA 描述符。
在这种情况下，用 32 字节缓存行管理 16 字节 DMA 描述符的缓存显然是不可能的：
我认为唯一的选择是禁用写缓冲。

如果驱动从应用程序接收任意对齐的缓冲区怎么办？那该怎么办？
在这种情况下也应该禁用写缓冲吗？禁用写缓冲的性能成本是多少？


DMA 模块
----------

一些 STM32 F7 外设具有内置 DMA。下面讨论的 STM32 F7 以太网驱动
就是具有内置 DMA 功能的此类外设的一个好例子。
然而，大多数 STM32 F7 外设没有内置 DMA 功能，
而是必须使用公共 STM32 F7 DMA 模块来执行 DMA 数据传输。
该公共 DMA 模块的接口在 ``arch/arm/src/stm32f7/stm32_dma.h`` 中描述。

DMA 模块 `不执行任何缓存操作`。相反，DMA 模块的客户端
必须执行缓存操作。以下是基本规则：

* TX DMA 传输。在调用 ``stm32_dmastart()`` 启动 TX 传输之前，
  DMA 客户端必须清理 DMA 缓冲区，以便要 DMA 传输的内容存在于物理内存中。
* RX DMA 传输。在所有 DMA 完成时，DMA 客户端将收到提供
  DMA 传输最终状态的回调。对于 RX DMA 完成回调的情况，
  回调处理程序中的逻辑应在尝试访问新的 RX 缓冲区内容之前
  使 RX 缓冲区无效。

将 STM32F429 驱动转换为 STM32F746
================================================

由于 STM32 F7 与 STM32 F4 如此相似，我们有大量可移植的工作驱动。
只需要很少的工作。以下是将 STM32F429 驱动转换为 STM32F746
所需做的事情的摘要。

示例
----------

STM32 以太网驱动中有一个很好的例子。STM32 F7 以太网驱动
（``arch/arm/src/stm32f7/stm32_ethernet.c``）直接派生自
STM32 F4 以太网驱动（``arch/arm/src/stm32/stm32_eth.c``）。
这两个以太网 MAC 外设几乎相同。只需要进行因 STM32 F7 D-Cache
而直接导致的更改即可使驱动在 STM32 F7 上工作。
这些更改总结如下。

重组 DMA 数据结构
-----------------------------

STM32 以太网驱动有四种不同的 DMA 缓冲区：

* RX DMA 描述符，
* TX DMA 描述符，
* RX 数据包缓冲区，和
* TX 数据包缓冲区，

在 STM32F429 驱动中，这些只是作为驱动数据结构的一部分实现的：

.. code-block:: c

    struct stm32_ethmac_s
    {
        ...
        /* Descriptor allocations */
        
        struct eth_rxdesc_s rxtable[CONFIG_STM32_ETH_NRXDESC];
        struct eth_txdesc_s txtable[CONFIG_STM32_ETH_NTXDESC];
        
        /* Buffer allocations */
        
        uint8_t rxbuffer[CONFIG_STM32_ETH_NRXDESC*CONFIG_STM32_ETH_BUFSIZE];
        uint8_t alloc[STM32_ETH_NFREEBUFFERS*CONFIG_STM32_ETH_BUFSIZE];
    };

这可能有三个问题：(1) 我们不知道数据结构将定义在什么类型的内存中。
如果是 DTCM 内存怎么办？那么 DMA 将失败。(2) 我们不知道 DMA 缓冲区的对齐方式。
它们必须在 D-Cache 行边界上对齐。(3a) RX 或 TX 描述符的大小是 16 或 32 字节。
为了单独清理或使缓存行无效，它们的大小必须是缓存行大小的倍数，
(3b) 同样适用于 DMA 缓冲区。

为了解决这个问题，做了以下几件事：

* 将缓冲区分配从设备结构移到可以具有属性的独立声明中。
* 可以添加的一个属性是节名称，以确保结构被链接到 DMA 可用的内存中
  （通过链接器脚本中的定义）。
* 另一个属性是我们可以强制结构与 D-Cache 行大小对齐。

添加了以下定义以支持将缓冲区大小与 Cortex-M7 D-Cache 行大小对齐：

.. code-block:: c

   /* Buffers used for DMA access must begin on an address aligned with the
   * D-Cache line and must be an even multiple of the D-Cache line size.
   * These size/alignment requirements are necessary so that D-Cache flush
   * and invalidate operations will not have any additional effects.
   *
   * The TX and RX descriptors are normally 16 bytes in size but could be
   * 32 bytes in size if the enhanced descriptor format is used (it is not).
   */
    
    #define DMA_BUFFER_MASK    (ARMV7M_DCACHE_LINESIZE - 1)
    #define DMA_ALIGN_UP(n)    (((n) + DMA_BUFFER_MASK) & ~DMA_BUFFER_MASK)
    #define DMA_ALIGN_DOWN(n)  ((n) & ~DMA_BUFFER_MASK)
    
    #ifndef CONFIG_STM32F7_ETH_ENHANCEDDESC
    #  define RXDESC_SIZE       16
    #  define TXDESC_SIZE       16
    #else
    #  define RXDESC_SIZE       32
    #  define TXDESC_SIZE       32
    #endif
    
    #define RXDESC_PADSIZE      DMA_ALIGN_UP(RXDESC_SIZE)
    #define TXDESC_PADSIZE      DMA_ALIGN_UP(TXDESC_SIZE)
    #define ALIGNED_BUFSIZE     DMA_ALIGN_UP(ETH_BUFSIZE)
    
    #define RXTABLE_SIZE        (STM32F7_NETHERNET * CONFIG_STM32F7_ETH_NRXDESC)
    #define TXTABLE_SIZE        (STM32F7_NETHERNET * CONFIG_STM32F7_ETH_NTXDESC)
    
    #define RXBUFFER_SIZE       (CONFIG_STM32F7_ETH_NRXDESC * ALIGNED_BUFSIZE)
    #define RXBUFFER_ALLOC      (STM32F7_NETHERNET * RXBUFFER_SIZE)
    
    #define TXBUFFER_SIZE       (STM32_ETH_NFREEBUFFERS * ALIGNED_BUFSIZE)
    #define TXBUFFER_ALLOC      (STM32F7_NETHERNET * TXBUFFER_SIZE)

RX 和 TX 描述符类型被替换为联合类型，
以确保分配的大小对齐：

.. code-block:: c

    /* This union type forces the allocated size of RX descriptors to be the
    * padded to a exact multiple of the Cortex-M7 D-Cache line size.
    */
     
    union stm32_txdesc_u
    {
      uint8_t             pad[TXDESC_PADSIZE];
      struct eth_txdesc_s txdesc;
    };
     
    union stm32_rxdesc_u
    {
      uint8_t             pad[RXDESC_PADSIZE];
      struct eth_rxdesc_s rxdesc;
    };

然后，最后，新缓冲区由以下全局变量定义：

.. code-block:: c

    /* DMA buffers.  DMA buffers must:
    *
    * 1. Be a multiple of the D-Cache line size.  This requirement is assured
    *    by the definition of RXDMA buffer size above.
    * 2. Be aligned a D-Cache line boundaries, and
    * 3. Be positioned in DMA-able memory (*NOT* DTCM memory).  This must
    *    be managed by logic in the linker script file.
    *
    * These DMA buffers are defined sequentially here to best assure optimal
    * packing of the buffers.
    */
    
    /* Descriptor allocations */
    
    static union stm32_rxdesc_u g_rxtable[RXTABLE_SIZE]
    __attribute__((aligned(ARMV7M_DCACHE_LINESIZE)));
    static union stm32_txdesc_u g_txtable[TXTABLE_SIZE]
    __attribute__((aligned(ARMV7M_DCACHE_LINESIZE)));
    
    /* Buffer allocations */
    
    static uint8_t g_rxbuffer[RXBUFFER_ALLOC]
    __attribute__((aligned(ARMV7M_DCACHE_LINESIZE)));
    static uint8_t g_txbuffer[TXBUFFER_ALLOC]
    __attribute__((aligned(ARMV7M_DCACHE_LINESIZE)));

当然，这强制对初始化缓冲区链的函数进行额外更改，
但我将留给感兴趣的读者自行探索。

添加缓存操作
--------------------

Cortex-M7 缓存操作在包含以下文件时可用：

.. code-block:: c

    #include "cache.h"

以下是使 RX 描述符无效的示例：

.. code-block:: c

    static int stm32_recvframe(struct stm32_ethmac_s *priv)
    {
    ...
    /* Scan descriptors owned by the CPU.  */
    
    rxdesc = priv->rxhead;
    
    /* Forces the first RX descriptor to be re-read from physical memory */
    
    arch_invalidate_dcache((uintptr_t)rxdesc,
                            (uintptr_t)rxdesc + sizeof(struct eth_rxdesc_s));
    
    for (i = 0;
        (rxdesc->rdes0 & ETH_RDES0_OWN) == 0 &&
            i < CONFIG_STM32F7_ETH_NRXDESC &&
            priv->inflight < CONFIG_STM32F7_ETH_NTXDESC;
        i++)
        {
        ...
        /* Try the next descriptor */
    
        rxdesc = (struct eth_rxdesc_s *)rxdesc->rdes3;
    
        /* Force the next RX descriptor to be re-read from physical memory */
    
        arch_invalidate_dcache((uintptr_t)rxdesc,
                                (uintptr_t)rxdesc + sizeof(struct eth_rxdesc_s));
        }
    ...
    }

以下是清理 TX 描述符的示例：

.. code-block:: c

    static int stm32_transmit(struct stm32_ethmac_s *priv)
    {
    ...
            /* Give the descriptor to DMA */
    
            txdesc->tdes0 |= ETH_TDES0_OWN;
    
            /* Flush the contents of the modified TX descriptor into physical
            * memory.
            */
    
            arch_clean_dcache((uintptr_t)txdesc,
                                (uintptr_t)txdesc + sizeof(struct eth_txdesc_s));
    ...
    }

以下是在完成读 DMA 后使读缓冲区无效的位置：

.. code-block:: c

    static int stm32_recvframe(struct stm32_ethmac_s *priv)
    {
    ...
        /* Force the completed RX DMA buffer to be re-read from
        * physical memory.
        */
    
        arch_invalidate_dcache((uintptr_t)dev->d_buf,
                            (uintptr_t)dev->d_buf + dev->d_len);
    
        nllvdbg("rxhead: %p d_buf: %p d_len: %d\n",
                priv->rxhead, dev->d_buf, dev->d_len);
    
        /* Return success*/
    
        return OK;
    ...
    }

以下是在启动写 DMA 之前清理写缓冲区的位置：

.. code-block:: c

    static int stm32_transmit(struct stm32_ethmac_s *priv)
    {
    ...
    /* Flush the contents of the TX buffer into physical memory */
    
    arch_clean_dcache((uintptr_t)priv->dev.d_buf,
                        (uintptr_t)priv->dev.d_buf + priv->dev.d_len);
    ...
    }
