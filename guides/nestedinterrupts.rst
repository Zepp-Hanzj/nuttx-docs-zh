=================
嵌套中断
=================

是否需要嵌套中断？
=============================

大多数 NuttX 架构不支持嵌套中断：中断在进入时被禁用，在返回时恢复。
能够处理嵌套中断在进行大量中断级处理的简单架构中至关重要：
在这种情况下，你可以对中断进行优先级排序，并确保最高优先级的
中断处理不会被较低级别的中断处理延迟。

然而，在 RTOS 模型中，所有中断处理应尽可能简短；
任何扩展处理应推迟到用户任务中执行，而不是在中断处理程序中完成。
不过，你可能也会发现 NuttX 中需要嵌套中断处理。
缺乏嵌套中断支持并非 NuttX 固有的问题，也无需如此；
修改中断处理以实现嵌套中断应该是一件简单的事情。

分层中断处理架构
=======================================

中断处理发生在多个文件中。在大多数实现中，
有几层中断处理逻辑：

#. 一些低级逻辑，通常是汇编语言，用于捕获中断并确定 IRQ 编号。
   以 ``arch/arm/src/armv7-m/up_exception.S`` 作为 Cortex-M 系列的示例。

#. 该低级逻辑随后调用一些 MCU 特定的中级函数，
   通常称为 ``up_doirq()``。示例是 ``arch/arm/src/armv7-m/up_doirq.c``。

#. 该 MCU 特定函数随后调用 NuttX 通用中断分发逻辑 ``irq_dispatch()``，
   可在 ``sched/irq_dispatch.c`` 中找到。

如何在分层中断处理架构中实现嵌套中断
=================================================================================

前两层中的逻辑必须修改以支持嵌套中断处理。
以下是一种技术方案：

#. 添加一个全局变量，例如 ``g_nestlevel``，用于计算中断嵌套级别。
   初始值为零；每次中断进入时递增，中断退出时递减
   （确保在每种情况下都禁用中断，因为递增和递减通常不是原子操作）。

#. 在最低级别，通常有一些汇编语言逻辑用于从用户栈切换到
   特殊的中断级栈。此行为由 ``CONFIG_ARCH_INTERRUPTSTACK`` 控制。
   此处的逻辑必须按以下方式更改：如果 ``g_nestlevel`` 为零，
   则正常行为，从用户栈切换到中断栈；如果 ``g_nestlevel`` 大于零，
   则不切换栈。在后一种情况下，我们已经在使用中断栈了。

#. 在中级、MCU 特定的位置是 ``g_nestlevel`` 递增的地方。
   并且需要根据 ``g_nestlevel`` 的状态做出一些额外的决策。
   如果 ``g_nestlevel`` 为零，则我们中断了用户代码，
   需要特别处理上下文信息并处理中断级上下文切换。
   如果 ``g_nestlevel`` 大于零，则中断处理程序被另一个中断中断。
   在这种情况下，中断处理必须始终返回到中断处理程序。
   这里不能发生上下文切换。直到最外层的嵌套中断处理程序
   返回到用户任务之前，都不能发生上下文切换。

#. 你还需要在中断处理程序中支持某种临界区以防止嵌套中断。
   例如，在 ``up_block_task()`` 等函数的逻辑中。
   此类逻辑在任何情况下都必须是原子的。

**注意 1**：ARMv7-M 也可以配置为使用独立的 MSP 和 PSP 栈，
中断处理使用 MSP 栈，所有任务使用 PSP 栈。
这与现有设计的某些部分不兼容，需要更多的工作，但可能产生更好的解决方案。

**注意 2**：SMP 有与第 2 点相同的问题，但处理方式不同：
在 SMP 中有一个按 CPU 编号索引的栈数组，
以便所有 CPU 都可以拥有一个中断栈。例如参见
`LC823450 <https://bitbucket.org/nuttx/nuttx/src/ca4ef377fb789ddc3e70979b28acb6730ff6a98c/arch/arm/src/lc823450/chip.h>`_
或
`i.MX6 <https://bitbucket.org/nuttx/nuttx/src/ca4ef377fb789ddc3e70979b28acb6730ff6a98c/arch/arm/src/imx6/chip.h>`_
SMP 逻辑。

一个通用的 ``up_doirq()`` 可能如下所示。
由于中断被禁用，它可以非常简单：

.. code-block:: c

  uint32_t *up_doirq(int irq, uint32_t *regs)
  {
    /* Current regs non-zero indicates that we are processing an interrupt;
     * current_regs is also used to manage interrupt level context switches.
     */
  
    current_regs = regs;
  
    /* Deliver the IRQ */
  
    irq_dispatch(irq, regs);
  
    /* If a context switch occurred while processing the interrupt then
     * current_regs may have change value.  If we return any value different
     * from the input regs, then the lower level will know that a context
     * switch occurred during interrupt processing.
     */
  
    regs = (uint32_t*)current_regs;
    current_regs = NULL;
    return regs;
  }

支持嵌套中断需要更改的是：

#. 如果我们处于嵌套状态，则必须保留 ``current_regs`` 的原始值。
   当最外层中断处理程序返回以处理中断级上下文切换时将需要它。

#. 如果我们处于嵌套状态，则需要始终返回接收到的 ``regs`` 的相同值。

因此修改后的 ``up_doirq()`` 版本如下。
这里我们假设中断已启用。

.. code-block:: c

  uint32_t *up_doirq(int irq, uint32_t *regs)
  {
    irqstate_t flags;
  
    /* Current regs non-zero indicates that we are processing an interrupt;
     * regs holds the state of the interrupted logic; current_regs holds the
     * state of the interrupted user task.  current_regs should, therefore,
     * only be modified for outermost interrupt handler (when g_nestlevel == 0)
     */
  
    flags = irqsave();
    if (g_nestlevel == 0)
      {
        current_regs = regs;
      }
    g_nestlevel++
    irqrestore(flags);
  
    /* Deliver the IRQ */
  
    irq_dispatch(irq, regs);
  
    /* Context switches are indicated by the returned value of this function.
     * If a context switch occurred while processing the interrupt then
     * current_regs may have change value.  If we return any value different
     * from the input regs, then the lower level will know that a context
     * switch occurred during interrupt processing.  Context switching should
     * only be performed when the outermost interrupt handler returns.
     */
  
    flags = irqsave();
    g_nestlevel--;
    if (g_nestlevel == 0)
      {
        regs = (uint32_t*)current_regs;
        current_regs = NULL;
      }
  
    /* Note that interrupts are left disabled.  This needed if context switch
     * will be performed.  But, any case, the correct interrupt state should
     * be restored when returning from the interrupt.
     */
  
    return regs;
  }

**注意：** 另一种更清晰的设计也是可能的。
如果将所有上下文切换推迟到 *PendSV* 处理程序，
那么中断可以向 ``do_irq()`` 逻辑向量化，
然后所有中断将自然可嵌套。

SVCall 与 PendSV
================

一个可能与嵌套中断处理相关的问题是 NuttX 中 ``SVCall`` 异常的使用。
``SVCall`` 异常在 NuttX 中用作经典的软件中断，用于执行上下文切换、
用户模式到内核模式的切换（反之亦然），以及当 NuttX 作为内核构建时的系统调用。

``SVCall`` 异常永远不会从中断级、处理程序模式的处理中执行；
仅从线程模式逻辑中执行。``SVCall`` 异常按如下方式用于执行系统调用：

* 禁用所有中断：有几个步骤必须在临界区中执行。
  这些设置和 ``SVCall`` 必须作为单个、不间断的原子操作工作。

* 设置特殊的寄存器配置：参数通过寄存器传递给 ``SVCall``，
  就像普通函数调用一样。

* 执行 Cortex SVC 指令。这将导致 ``SVCall`` 异常，
  被分发到 ``SVCall`` 异常处理程序。
  此异常必须在输入寄存器设置就位时发生；
  它不能被延迟到稍后执行。``SVCall`` 异常处理程序解码寄存器
  并执行请求的操作。如果没有发生上下文切换，
  ``SVCall`` 将立即返回给调用者。

* 返回时将重新启用中断。

那么这与嵌套中断处理有什么关系？
由于在整个 ``SVCall`` 序列中中断被禁用，实际上没有什么关系。
然而，存在一些担忧，因为如果使用 ``BASEPRI`` 来禁用中断，
那么 ``SVCall`` 异常必须具有最高优先级：
``BASEPRI`` 寄存器被设置为禁用除 ``SVCall`` 之外的所有中断。

支持嵌套中断的动机大概是确保某些高优先级中断
不会被较低优先级的中断处理延迟。
由于 ``SVCall`` 异常具有最高优先级，它将延迟所有其他中断
（当然，禁用中断也会延迟所有其他中断）。

PendSV 异常是 Cortex 架构提供的另一种机制。
有人建议可以通过使用 PendSV 中断来避免
``SVCall`` 异常的这些问题。使用 PendSV 异常而不是
``SVCall`` 中断的架构在我脑海中还不太清晰。
但我会将此说明保留在这里以供将来参考。

可能出现什么问题？
====================

每当你处理软硬件接口的逻辑时，很多事情都可能出错。
但是，除了这个一般风险之外，NuttX 唯一的特定风险是
你可能会发现一些假设中断已被禁用的微妙的中断级逻辑。
在这些情况下，可能需要在中断级处理中添加额外的临界区。
这种情况的可能性可能相当低，但不能完全排除。
