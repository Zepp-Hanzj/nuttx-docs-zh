===============================
ARMv7-M 运行时栈检查
===============================

.. warning:: 
    迁移自: 
    https://cwiki.apache.org/confluence/display/NUTTX/ARMv7-M+Run+Time+Stack+Checking

概述
========

NuttX 支持验证功能，用于检查在 NuttX 下运行的任务和中断上下文所使用的动态分配栈和固定栈。有 2 种类型的栈检查，可以单独使用或组合使用。

1. 栈监视器
2. 每函数调用检查（仅限 ARMV7）

栈监视器
-----------------

使用栈监视器应用程序需要启用 ``CONFIG_STACK_COLORATION``。该编译时选项会在创建时将已知模式 ``STACK_COLOR`` 写入栈内存。对于空闲任务和中断，这在复位后启动时运行的代码中完成。这被称为栈着色。

一旦建立了模式，函数 ``up_check_stack`` 及相关函数通过在分配的栈中查找模式的最低字来执行栈检查。

栈监视器通过 ``CONFIG_SYSTEM_STACKMONITOR`` 启用，它将启用一个守护进程，定期运行并检查系统上运行的任务的栈渗透情况。

栈监视器有助于确定任务大小和检查使用情况。然而，它对于检测某些类型的栈溢出以及栈溢出的原因并不是很有用。

原因是损坏的栈可能不是被逐渐消耗的。它可能在函数调用中将栈指针设置在栈底以下很远的地方来分配栈上的局部变量，从而发生溢出。函数调用中的代码随后可能损坏栈底以下的内存，恢复栈指针并返回到调用者，而实际上并未覆盖栈底的着色。

这引出了下一种栈检查方法。


每函数调用检查
-----------------
这种栈检查方法利用了编译器支持的分析器钩子机制。使用 ``CONFIG_ARMV7M_STACKCHECK`` 启用后，会保留一个寄存器（默认为 ``R10``）并将栈基址的值保存在其中（``rBS``）。然后每个函数调用都会添加前导代码和后置代码。前导代码（``__cyg_profile_func_enter``）检查当前栈指针减去 64 字节的余量（``FP`` 寄存器额外增加 136 字节）与保留寄存器 ``rBS`` 中的值进行比较。如果计算值低于 ``rBS`` 中的值，则生成硬件故障。后置代码（``__cyg_profile_func_exit``）仅返回到调用者。

减去余量的理由可以从两个方面来看。如果配置未使用单独的 ISR 栈，则保留的空间将容纳 CPU 和可选 FPU 寄存器的上下文保存，以在用户栈上服务中断。如果配置使用单独的 ISR 栈，其中 64 字节将容纳到中断栈的转换，其余 60-200 字节仅作为余量。无论哪种方式，栈分配时应始终保留至少 200 字节的余量。

由于保留寄存器 rBS 包含当前上下文的栈基址，且 rBS 在进入 ISR 时不会更新，因此使用每函数调用栈检查无法检查中断的栈渗透情况。

需要考虑的一点是这种栈检查方法对代码大小和速度的影响。每个函数将增加两个额外的调用和返回指令。在每个函数的执行路径中，将增加一组指令来执行前导和后置功能。在嵌套多层的调用树中，这会累积起来。在某个特定使用场景中，我们看到 CPU 利用率增加了 30% 到 35% 来支持每函数调用栈检查。

这只是调试工具吗？可以想象，在关键任务应用中，如果代码大小和速度影响可以接受，这可能是发布版本的一部分。

从提交 4942867 开始，寄存器 R11 将包含导致故障时栈指针会达到的值。这可用于计算故障任务所需的栈大小。具体方法是取 R10-R11 的差值并向上取整 12 字节（向上取整是为了弥补栈分配中可能发生的 8 字节栈对齐和 4 字节减少），然后将该数量添加到故障任务的栈大小中。

每调用栈检查支持详情
----------------------------------------------

目前只有 ARMV7 衍生版本支持每调用栈检查。支持需要以下组件：

启动函数必须在 ``rBS`` 中建立值（默认为 ``R10``，见下文）。为此，启动函数不能添加前导和后置代码。这通过使用以下 gcc 属性来实现：

.. code-block:: c

    #ifdef CONFIG_ARMV7M_STACKCHECK
    /* we need to get r10 set before we can allow instrumentation calls */
    
    void __start(void) __attribute__ ((no_instrument_function));
    #endif

...

.. code-block:: c

    void __start(void)
    {
      const uint32_t *src;
      uint32_t *dest;
    
    #ifdef CONFIG_ARMV7M_STACKCHECK
    
      /* Set the stack limit before we attempt to call any functions */
    
      __asm__ volatile ("sub r10, sp, %0" : : "r" (CONFIG_IDLETHREAD_STACKSIZE -64) : );
    #endif

减去 64 是将限制设置在栈底上方 64 字节处。注意：这可能会增加另外 64 字节的余量。

对于创建任务上下文，需要以下代码来设置 ``rBS``

.. code-block:: c

    void up_initial_state(struct tcb_s *tcb)
    {
      struct xcptcontext *xcp = &tcb->xcp;
    
      /* Initialize the initial exception register context structure */
    
      memset(xcp, 0, sizeof(struct xcptcontext));

      /* Save the initial stack pointer */

      xcp->regs[REG_SP]      = (uint32_t)tcb->adj_stack_ptr;

    #ifdef CONFIG_ARMV7M_STACKCHECK
      /* Set the stack limit value */

      xcp->regs[REG_R10]     = (uint32_t)tcb->stack_alloc_ptr + 64;
    #endif

最后，需要在构建中包含 up_stackcheck.c，并设置编译器标志以保留 ``R10`` 并启用插桩。

这在给定架构的 nuttx/arch/arm/src/<arch>/Make.defs 中完成：

.. code-block:: makefile

    ifeq ($(CONFIG_ARMV7M_STACKCHECK),y)
    CMN_CSRCS += up_stackcheck.c
    endif

编译器标志在 nuttx/arch/arm/src/armv7-m/Toolchain.defs 中添加

.. code-block:: makefile

    # enable precise stack overflow tracking
    ifeq ($(CONFIG_ARMV7M_STACKCHECK),y)
    INSTRUMENTATIONDEFINES   = -finstrument-functions -ffixed-r10
    endif

其他注意事项
--------------------

如果使用 NuttX 的导出构建功能：对于运行时栈检查，应用程序和 NuttX 都需要使用相同的 ``CONFIG_ARMV7M_STACKCHECK`` 选项状态（启用或禁用）来构建。任何不匹配都会导致编译时或运行时问题。
