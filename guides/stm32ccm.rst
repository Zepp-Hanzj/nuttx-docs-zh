===================
STM32 CCM 分配器
===================

CCM 内存
==========

STM32 F2、F3 和 F4 系列有一个称为 CCM（核心耦合内存）的特殊 SRAM 块。此内存的缺点是不能用于 STM32 DMA 操作。

默认情况下，CCM 内存在创建 NuttX 堆时与其他内存合并在一起。但这可能是一个问题，因为当调用 ``malloc()`` 时，是返回不可用于 DMA 的 CCM 内存还是其他可用于 DMA 的内存将取决于运气。这通常无关紧要，但如果你正在分配用于 DMA 的内存，那就完全不同了！在这种情况下，为你的 DMA 缓冲区获取 CCM 内存将导致失败。

CONFIG_STM32_CCMEXCLUDE
=======================

有一个名为 ``CONFIG_STM32_CCMEXCLUDE`` 的配置选项可用于从堆中排除 CCM 内存。这解决了在你想分配 DMA 缓冲区时获取 CCM 内存的问题。但你如何处理 CCM 内存呢？让它闲置不用吗？

CCM 分配器
=============

为了利用 CCM 内存，提供了一个 CCM 内存分配器。当设置以下选项时，此内存分配器会自动启用：

* ``CONFIG_STM32_CCMEXCLUDE`` CCM 内存从正常堆中排除，以及
* ``CONFIG_MM_MULTIHEAP`` 启用对多堆的支持。

在这些条件下，CCM 内存分配器被启用，``arch/arm/src/stm32/stm32_ccm.h`` 中原型化的分配器接口可用。

注意：这些接口在技术上不是原型化的，因为它们实际上是通过 C 预处理器宏提供的。

注意：要使用 CCM 内存分配器函数，你必须在早期启动逻辑中的某处先调用 ``ccm_initialize()``。

通过这些接口，你有一个（几乎）标准的方式来管理来自 CCM SRAM 组成的堆的内存。而且，由于 CCM 内存不再是正常堆的一部分，所有分配的 I/O 缓冲区都将是可以用于 DMA 的（除非你在栈中包含了其他不可用于 DMA 的内存区域）。

CCM 栈
==========

Petteri Aimonen 报告的一个特定问题需要一些额外的变通方法。STM32 SPI 驱动支持 DMA，对于 SPI，有时需要进行一些非常小的传输，使用 DMA 没有实际收益。在这种情况下，Petteri 设计了一种巧妙的方法，既 1) 利用 CCM 内存，又 2) 强制回退到非 DMA 传输来处理这些小的栈传输。

以下是 Petteri 所做的：

#. 首先，他修改了 ``arch/arm/src/common/up_createstack.c`` 和 ``up_releasestack.c``，使栈从 CCM 内存分配。分配方式如下：

   .. code-block:: C

      void *result = ccm_zalloc(size);
      if (!result)
        {
         /* Fall back to main heap */
          result = zalloc(size);
        }

   匹配的释放：

   .. code-block:: C

      if (((uint32_t)p & 0xF0000000) == 0x10000000)
        {
          ccm_free(p);
        }
      else
        {
          free(p);
        }

#. 然后 Petteri 添加了由 ``CONFIG_STM32_DMACAPABLE`` 启用的特殊 DMA 支持。该选项在所有 DMA 逻辑中启用一个选项：

   .. code-block:: C

      bool stm32_dmacapable(uint32_t maddr);

   如果可以从该地址进行 DMA 则返回 true，否则返回 false。

#. 最后，Petteri 向 STM32 SPI 驱动添加了使用 ``stm32_dmacapable()`` 的逻辑：如果地址不支持 DMA，SPI 驱动将回退到非 DMA 操作。

   通过 Petteri 的更改，所有大型 I/O 缓冲区将从可 DMA 的内存分配。所有栈将从不可 DMA 的 CCM 内存分配（假设有空间）。不可 DMA 栈上的小 SPI DMA 缓冲区将被 ``stm32_dmacapable()`` 检测到，在这种情况下，STM32 SPI 驱动将回退并使用非 DMA 传输。

   从所有报告来看，这工作得相当好。
