=====================
更小的向量表
=====================

.. warning:: 
    迁移自： 
    https://cwiki.apache.org/confluence/display/NUTTX/Smaller+Vector+Tables 


最大的 OS 数据结构之一是向量表 ``g_irqvector[]``。这是在调用 ``irq_attach()`` 时保存向量信息的表，并被 ``irq_dispatch()`` 用于分派中断。最近的更改使该表变得更大，对于 32 位 arm，该表的大小由以下公式给出：

.. code-block:: c

    nbytes = number_of_interrupts * (2 * sizeof(void *))

我们将重点关注 STM32 来讨论此问题以保持简单。然而，此讨论适用于所有架构。

MCU 硬件支持的（物理）中断向量数量由 ``NR_IRQ`` 定义给出，该定义在 ``arch/arm/include/stm32`` 的头文件中提供。默认情况下，这是上述方程中 ``number_of_interrupts`` 的值。

对于像 STM32 这样的 32 位 ARM，假设有 100 个中断向量，此大小将是 800 字节的内存。对于拥有大量 RAM 的高端 MCU 来说，这不算多，但对于 RAM 极少的 MCU 来说，这可能是致命的。

下面描述了两种减少向量表大小的方法。两者都依赖于这样一个事实：并非所有中断都在给定的 MCU 上使用。大多数时候，``g_irqvector[]`` 中的大多数条目为零，因为只有少数中断实际上被应用程序附加和启用。如果你知道某些 IRQ 编号不会被使用，那么可以将其过滤掉，将大小减少到支持的中断数量。

例如，如果实际使用的中断数量为 20，上述需求将从 800 字节减少到 160 字节。

软件 IRQ 重映射
======================

`[2017 年 3 月 3 日，对此"软件 IRQ 重映射"的支持已包含在 NuttX 仓库中。]`

减少 ``g_irqvector[]`` 大小最简单的方法之一是将大量物理中断向量重映射到实际使用的更小的中断集。为了讨论，让我们想象两个新的配置设置：

* ``CONFIG_ARCH_MINIMAL_VECTORTABLE``：启用 IRQ 映射
* ``CONFIG_ARCH_NUSER_INTERRUPTS``：映射后的 IRQ 数量。

然后可以将中断向量表分配为 ``CONFIG_IRQ_NMAPPED_IRQ`` 大小，而不是更大的 ``NR_IRQS``：

.. code-block:: c 

    #ifdef CONFIG_ARCH_MINIMAL_VECTORTABLE
    struct irq_info_s g_irqvector[CONFIG_ARCH_NUSER_INTERRUPTS];
    #else
    struct irq_info_s g_irqvector[NR_IRQS];
    #endif

``g_irqvector[]`` 表仅在三个地方被访问：

``irq_attach()``
----------------

``irq_attach()`` 接收物理向量号以及稍后分派中断所需的信息：

.. code-block:: c

    int irq_attach(int irq, xcpt_t isr, FAR void *arg);

``irq_attach()`` 中的逻辑将传入的物理向量号映射到表索引，如下所示：

.. code-block:: c 

    #ifdef CONFIG_ARCH_MINIMAL_VECTORTABLE
    int ndx = g_irqmap[irq];
    #else
    int ndx = irq;
    #endif

其中 ``up_mapirq[]`` 是一个以物理中断向量号为索引的数组，包含新的、映射后的中断向量表索引。此数组必须由平台特定代码提供。

``irq_attach()`` 将使用此索引设置 ``g_irqvector[]``。

.. code-block:: c 

    g_irqvector[ndx].handler = isr;
    g_irqvector[ndx].arg     = arg;

``irq_dispatch()``
------------------

``irq_dispatch()`` 在接收到中断时由 MCU 逻辑调用：

.. code-block:: c 

    void irq_dispatch(int irq, FAR void *context);

其中 irq 再次是物理中断向量号。

``irq_dispatch()`` 将执行与 ``irq_attach()`` 基本相同的操作。首先它将 irq 编号映射到表索引：

.. code-block:: c 

    #ifdef CONFIG_ARCH_MINIMAL_VECTORTABLE
    int ndx = g_irqmap[irq];
    #else
    int ndx = irq;
    #endif

然后将中断处理分派到附加的中断处理程序。注意物理向量号被传递给处理程序，因此它完全不知道底层的"变换"游戏：

.. code-block:: c 

    vector = g_irqvector[ndx].handler;
    arg    = g_irqvector[ndx].arg;
    
    vector(irq, context, arg);

``irq_initialize()``
--------------------

``irq_initialize()``：只需在上电时将 ``g_irqvector[]`` 表设置为已知状态。它只需要区分大小的差异。

.. code-block:: c 

    #ifdef CONFIG_ARCH_MINIMAL_VECTORTABLE
    #  define TAB_SIZE CONFIG_ARCH_NUSER_INTERRUPTS
    #else
    #  define TAB_SIZE NR_IRQS
    #endif
    
    for (i = 0; i < TAB_SIZE; i++)

``g_mapirq[]``
--------------

``up_mapirq()`` 的实现可能如下所示：

.. code-block:: c 

    #include <nuttx/irq.h>

    const irq_mapped_t g_irqmap[NR_IRQS] =
    {
    ... IRQ to index mapping values ...
    };

``g_irqmap[]`` 是一个映射 irq 表索引的数组。它包含映射后的索引值，并且本身以物理中断向量号为索引。它提供一个范围在 0 到 ``CONFIG_ARCH_NUSER_INTERRUPTS`` 之间的 ``irq_mapped_t`` 值，这是向量表中新的、映射后的索引。不支持的 IRQ 将简单地映射到超出范围的值，如 ``IRQMAPPED_MAX``。例如，如果 ``g_irqmap[37] == 24``，则硬件中断向量 37 将被映射到索引 24 处的中断向量表。如果 ``g_irqmap[42] == IRQMAPPED_MAX``，则硬件中断向量 42 未被使用，如果发生将导致意外中断崩溃。

硬件向量重映射
=========================

`[此技术方案在此讨论，但因本节末尾讨论的技术"复杂性"和"可疑的性能改进"而不被推荐。]`

大多数 ARMv7-M 架构支持两种处理中断的机制：

* 由 ``CONFIG_ARMV7M_CMNVECTOR=y`` 启用的所谓 `通用` 向量处理逻辑，可以在 ``arch/arm/src/armv7-m/`` 中找到，以及
* MCU 特定的中断处理逻辑。对于 STM32，此逻辑可以在 ``arch/arm/src/stm32/gnu/stm32_vectors.S`` 中找到。

`通用` 向量逻辑效率稍高，MCU 特定逻辑灵活性稍好。

如果我们不使用由 ``CONFIG_ARMV7M_CMNVECTOR=y`` 启用的 `通用` 向量逻辑，而是使用更灵活的 MCU 特定实现，那么我们也可以使用它来将大量硬件中断向量号映射到更小的软件中断号集合。这只需要对 OS 进行最小的更改，不需要任何神奇的软件查找表。但实现起来要复杂得多。

此技术方案需要修改三个文件：

* 在 ``arch/arm/include/stm32`` 下创建一个新的头文件，为讨论起见称为 ``xyz_irq.h``。此新头文件类似于该目录中的其他 IRQ 定义头文件，但它只定义重映射后的 IRQ 编号。因此，不是基于物理向量号的原始 IRQ 头文件中的 100 个 IRQ 编号定义，此头文件将只定义从 0 到 19 的 20 个 `映射` IRQ 编号。它还将 ``NR_IRQS`` 设置为值 20。
* 在 ``arch/arm/src/stm32/hardware`` 下创建一个新的头文件，称为 ``xyz_vector.h``。它将类似于该目录中的其他向量定义文件：它将包含 100 个 ``VECTOR`` 和 ``UNUSED`` 宏的序列。它将为 20 个有效中断定义 ``VECTOR`` 条目，为未使用的中断向量号定义 80 个 ``UNUSED`` 条目。更多信息见下文。
* 修改 ``stm32_vectors.S`` 文件。这些更改是微不足道的，仅涉及有条件地包含新的、特殊的 ``xyz_vectors.h`` 头文件。

**重新审视**：这需要更新。在当前实现中，``xyz_vector.h`` 文件和 ``stm32_vectors.S`` 都不存在。所有这些都已被 ``arch/arm/src/armv7-m`` 中的通用向量处理所取代。

向量定义
==================

在 ``arch/arm/src/stm32/gnu/stm32_vector.S`` 中，注意 ``xyz_vector.h`` 文件将被包含两次。在每次包含之前，定义宏 ``VECTOR`` 和 ``UNUSED``。

第一次包含 ``xyz_vector.h`` 时，它定义硬件向量表。硬件向量表由数组中 ``NR_IRQS`` 个 32 位地址组成。这通过以下设置实现：

.. code-block:: c 

    #undef VECTOR
    #define VECTOR(l,i) .word l
    
    #undef UNUSED
    #define UNUSED(i)   .word stm32_reserved

然后包含 ``xyz_vector.h``。考虑原始文件中的以下定义：

.. code-block:: c

    ...
    VECTOR(stm32_usart1, STM32_IRQ_USART1) /* Vector 16+37: USART1 global interrupt */
    VECTOR(stm32_usart2, STM32_IRQ_USART2) /* Vector 16+38: USART2 global interrupt */
    VECTOR(stm32_usart3, STM32_IRQ_USART3) /* Vector 16+39: USART3 global interrupt */
    ...

假设我们只想支持 USART1，并且我们希望 USART1 的 IRQ 编号为 12。这将在 ``xyz_vector.h`` 头文件中实现如下：

.. code-block:: c

    ...
    VECTOR(stm32_usart1, STM32_IRQ_USART1) /* Vector 16+37: USART1 global interrupt */
    UNUSED(0)                              /* Vector 16+38: USART2 global interrupt */
    UNUSED(0)                              /* Vector 16+39: USART3 global interrupt */
    ...

其中 ``STM32_IRQ_USART1`` 的值在 ``arch/arm/include/stm32/xyz_irq.h`` 头文件中定义为 12。当 ``stm32_vectors.S`` 使用上述 ``VECTOR`` 和 ``UNUSED`` 定义包含 ``xyz_vector.h`` 时，将产生以下结果：

.. code-block:: c 

    ...
    .word stm32_usart1
    .word stm32_reserved
    .word stm32_reserved
    ...

这些分别是向量 53、54 和 55 的设置。整个向量表将以这种方式填充。``stm32_reserved`` 如果被调用将导致"意外 ISR"崩溃。``stm32_usart1`` 如果被调用将正常处理 USART1 中断，如下所示。

中断处理程序定义
-----------------------------

在向量表中，所有有效向量都设置为 `handler` 函数的地址。所有未使用的向量都被强制指向 ``stm32_reserved``。目前，只有硬件不支持的向量被标记为 ``UNUSED``，但你可以将任何向量标记为 ``UNUSED`` 以消除它。

当 ``stm32_vector.S`` 第二次包含 ``xyz_vector.h`` 时，生成 `handler` 函数。每个有效向量指向匹配的处理程序函数。在这种情况下，你不需要为 ``UNUSED`` 向量提供处理程序，只为使用的 ``VECTOR`` 向量提供。所有未使用的向量将转到公共的 ``stm32_reserved`` 处理程序。剩余的处理程序集合非常稀疏。

这些是 ``stm32_vectors.S`` 第二次包含 ``xzy_vector.h`` 时 ``UNUSED`` 和 ``VECTOR`` 宏的值：

.. code-block:: asm

    .macro HANDLER, label, irqno
        .thumb_func
    label:
        mov r0, #\irqno
        b       exception_common
    .endm
    
    #undef VECTOR
    #define VECTOR(l,i) HANDLER l, i
    
    #undef UNUSED
    #define UNUSED(i)

在上面的 USART1 示例中，将生成一个处理程序，提供 IRQ 编号 12。记住 12 是 ``arch/arm/include/stm32/xyz_irq.h`` 头文件中提供的宏 ``STM32_IRQ_USART1`` 的展开值：

.. code-block:: asm 

        .thumb_func
    stm32_usart1:
        mov r0, #12
        b       exception_common

现在，当向量 16+37 发生时，它被映射到 IRQ 12，没有显著的软件开销。

复杂性
--------------

David Sidrane 指出了上述逻辑中的一个复杂性：当我们在 ``stm32_irq.c`` 中访问 NVIC 以启用和禁用中断时，逻辑需要物理向量号来选择 NVIC 寄存器和要修改的 NVIC 寄存器中的位。

这可以用另一个小的 IRQ 查找表来处理（在我们的示例情况中为 20 个 ``uint8_t`` 条目）。但这种方法并不比上面描述的 `软件向量映射` 好多少，后者没有这个问题。当然，启用/禁用中断是低频率操作，至少不会将查找放在关键中断路径中。

David Sidrane 提出的另一个选项同样不优雅：

* 不要更改 ``arch/arm/include/stm32`` IRQ 定义文件。
* 而是将 IRQ 编号编码为同时包含索引和物理向量号：

.. code-block:: c 

    ...
    VECTOR(stm32_usart1, STM32_IRQ_USART1 << 8 | STM32_INDEX_USART1)
    UNUSED(0)
    UNUSED(0)
    ...

STM32_INDEX_USART1 将具有值 12，STM32_IRQ_USART1 将像以前一样（53）。这个编码值将被 ``irq_dispatch()`` 接收，它将解码索引和物理向量号。它将使用索引在 ``g_irqvector[]`` 表中查找，但将物理向量号作为 IRQ 编号传递给中断处理程序。

在 ``irq_attach()`` 中仍然需要查找以将物理向量号转换回索引（在我们的示例中为 100 个 ``uint8_t`` 条目）。因此一些查找是不可避免的。

基于这些分析，我的建议是不再进一步考虑第二个选项。第一个选项更清晰、更可移植，通常是更好的选择。

可疑的性能改进
--------------------------------

第二个选项的目的是提供比选项 1 的纯软件映射更高性能的物理中断向量到 IRQ 编号的映射。然而，为了实现这种方法，我们必须使用效率较低的非通用向量处理逻辑。该逻辑效率低得不多，成本可能只是一个 16 位立即数加载指令和分支到 FLASH 中的另一个位置（这将导致 CPU 流水线被刷新）。

选项 2 的变体，其中同时编码物理向量号和向量表索引，将需要在 ``irq_dispatch()`` 中进行更多处理以解码物理向量号和向量表索引。可能只是 AND 和 SHIFT 指令。

然而，第一种纯软件映射方法的最小成本可能只是在 ``irq_attach()`` 中从 FLASH 进行一次索引字节获取。当然，在 ARM ISA 中，索引本质上是 `免费的`，主要成本将是 FLASH 内存访问。因此我的初步评估是两种方法的性能基本相同。如果实现得当，第一种方法可能性能更好。

两种选项都需要在 ``irq_attach()`` 中进行一些小的范围检查。

由于这个原因以及第一种选项的简单性，我认为没有理由支持或进一步考虑这第二个选项。

复杂性和通用性
-------------------------------

选项 2 过于复杂；它依赖于对 MCU 中断逻辑如何工作的深入理解以及高水平的 Thumb 汇编语言技能。

选项 2 的另一个问题是它实际上只适用于 Cortex-M 系列处理器，也许还有其他以类似方式支持中断向量中断的处理器。它不是可以与任何 CPU 架构一起使用的通用解决方案。

更糟糕的是，此支持所依赖的 MCU 特定中断处理逻辑非常有限。一旦添加了通用中断处理逻辑，我就停止在所有较新的 ARMv7-M 移植中实现 MCU 特定逻辑。因此，MCU 特定中断处理逻辑仅存在于 EFM32、Kinetis、LPC17、SAM3/4、STM32、Tiva 中，没有其他。非常有限！

这些是不推荐选项 2 且不会明确支持它的进一步原因。
