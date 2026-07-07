=====================================================
架构特定逻辑导出给 NuttX 的 API
=====================================================

.. c:function:: void up_initialize(void)

  在基本 OS 服务初始化后，在 OS 初始化期间调用一次。此处将处理初始化 OS 的架构特定细节。诸如设置中断服务例程、启动时钟和注册设备等事情因每个处理器和硬件平台而异。

  ``up_initialize()`` 在 OS 初始化后但在 init 进程启动之前以及库初始化之前调用。OS 服务和驱动程序服务可用。

.. c:function:: void up_idle(void)

  当没有其他就绪运行的任务时执行的逻辑。这是处理器空闲时间，将持续直到某个中断发生以引起从空闲任务的上下文切换。

  此状态下的处理可能是处理器特定的。例如，这可能是执行电源管理操作的地方。

.. c:function:: void up_initial_state(FAR struct tcb_s *tcb)

  一个新线程正在启动，已创建新的 TCB。调用此函数以初始化新 TCB 的处理器特定部分。

  此函数必须设置初始架构寄存器和/或栈，以便在下一次上下文切换时执行将从 tcb->start 开始。

  此函数可能还需要设置处理器寄存器，以便新线程以正确的权限执行。如果在 NuttX 配置中选择了 ``CONFIG_BUILD_PROTECTED`` 或 ``CONFIG_BUILD_KERNEL``，则可能需要根据 TCB 的 flags 字段中指定的任务类型执行特殊初始化：内核线程将需要内核模式权限；用户任务和 pthread 应该只有用户模式权限。如果既未选择 ``CONFIG_BUILD_PROTECTED`` 也未选择 ``CONFIG_BUILD_KERNEL``，则所有线程应该具有内核模式权限。

.. c:function:: STATUS up_create_stack(FAR struct tcb_s *tcb, size_t stack_size, uint8_t ttype)

  为新线程分配栈并在 TCB 中设置栈相关信息。

  必须初始化以下 TCB 字段：

  -  ``adj_stack_size``：针对硬件、处理器等调整后的栈大小。此值仅保留用于调试目的。
  -  ``stack_alloc_ptr``：指向已分配栈的指针
  -  ``stack_base_ptr``：在从栈分配中移除 TLS 数据和参数后调整的栈基指针。

  :param tcb: 新任务的 TCB。
  :param stack_size: 请求的栈大小。至少必须分配这么多。
  :param ttype: 线程类型。这可能是以下之一（在 ``include/nuttx/sched.h`` 中定义）：

     -  ``TCB_FLAG_TTYPE_TASK``：普通用户任务
     -  ``TCB_FLAG_TTYPE_PTHREAD``：用户 pthread
     -  ``TCB_FLAG_TTYPE_KERNEL``：内核线程

     此线程类型通常在 TCB 的 flags 字段中可用，但是，在某些上下文中，当调用 up_create_stack 时 TCB 可能尚未完全初始化。

     如果定义了 ``CONFIG_BUILD_PROTECTED`` 或 ``CONFIG_BUILD_KERNEL``，则此线程类型可能会影响栈的分配方式。例如，内核线程栈应从受保护的内核内存中分配。用户任务和线程的栈必须来自用户代码可访问的内存。

.. c:function:: STATUS up_use_stack(FAR struct tcb_s *tcb, FAR void *stack, size_t stack_size)

  使用预分配的栈内存在 TCB 中设置栈相关信息。此函数仅在启动任务或内核线程时从 ``nxtask_init()`` 调用（从不用于 pthread）。

  必须初始化以下 TCB 字段：

  -  ``adj_stack_size``：针对硬件、处理器等调整后的栈大小。此值仅保留用于调试目的。
  -  ``stack_alloc_ptr``：指向已分配栈的指针
  -  ``stack_base_ptr``：在从栈分配中移除 TLS 数据和参数后调整的栈基指针。

  :param tcb: 新任务的 TCB。
  :param stack_size: 已分配的栈大小。

  注意：与 ``up_stack_create()`` 和 ``up_stack_release`` 不同，此函数不需要任务类型（``ttype``）参数。如果信息需要该信息，TCB 标志将始终被设置以向 ``up_use_stack()`` 提供任务类型。

.. c:function:: FAR void *up_stack_frame(FAR struct tcb_s *tcb, size_t frame_size)

  在 TCB 的栈中分配一个栈帧以保存线程特定数据。可以在调用 ``up_create_stack()`` 或 ``up_use_stack()`` 之后但在任务启动之前的任何时间调用此函数。

  线程数据可以保存在栈中（而不是在 TCB 中），如果用户代码直接访问它。这包括诸如 ``argv[]`` 之类的内容。栈内存保证与线程处于相同的保护域中。

  将重新初始化以下 TCB 字段：

  -  ``adj_stack_size``：从栈中移除栈帧后的栈大小。
  -  ``stack_base_ptr``：在从栈分配中移除 TLS 数据和参数后调整的栈基指针。

  以下是某些分配（tls、arg）后的示意图::

                     +-------------+ <-stack_alloc_ptr(lowest)
                     |  TLS Data   |
                     +-------------+
                     |  Arguments  |
    stack_base_ptr-> +-------------+\
                     |  Available  | +
                     |    Stack    | |
                  |  |             | |
                  |  |             | +->adj_stack_size
                  v  |             | |
                     |             | |
                     |             | +
                     +-------------+/

  :param tcb: 新任务的 TCB。
  :param frame_size: 要分配的栈帧大小。

  :return:
    指向已分配栈帧底部的指针。任何失败将返回 NULL。返回值的对齐方式与栈本身的对齐方式相同。

.. c:function:: void up_release_stack(FAR struct tcb_s *dtcb)

  任务已停止。释放已失效 TCB 中保留的所有栈相关资源。

  :param dtcb: 包含有关要释放的栈的信息的 TCB。

  :param ttype: 线程类型。这可能是以下之一（在 ``include/nuttx/sched.h`` 中定义）：

     -  ``TCB_FLAG_TTYPE_TASK``：普通用户任务
     -  ``TCB_FLAG_TTYPE_PTHREAD``：用户 pthread
     -  ``TCB_FLAG_TTYPE_KERNEL``：内核线程

     此线程类型通常在 TCB 的 flags 字段中可用，但是，在某些错误恢复上下文中，当调用 up_release_stack 时 TCB 可能尚未完全初始化。

     如果定义了 ``CONFIG_BUILD_PROTECTED`` 或 ``CONFIG_BUILD_KERNEL``，则此线程类型可能会影响栈的释放方式。例如，内核线程栈可能是从受保护的内核内存中分配的。用户任务和线程的栈必须来自用户可访问的内存。

.. c:function:: void up_switch_context(FAR struct tcb_s *tcb, FAR struct tcb_s *rtcb)

  任务当前在就绪运行列表中但已被准备好执行。恢复其上下文并开始执行。

  此函数仅从 NuttX 调度逻辑调用。调用此函数时中断将始终被禁用。

  :param tcb: 指将要执行的就绪运行列表的头部任务。
  :param rtcb: 指将被阻塞的正在运行的任务。

.. c:macro:: noreturn_function

.. c:function:: void up_exit(int status) noreturn_function;

  此函数使当前执行的任务停止存在。这是 task_delete() 的特殊情况。

  与其他 UP API 不同，此函数可以直接从处于各种状态的用户程序调用。此函数的实现应在执行调度操作之前禁用中断。

.. c:function:: void up_dump_register(FAR void *dumpregs)

  寄存器转储可以以架构特定的方式处理。

.. c:function:: void up_schedule_sigaction(FAR struct tcb_s *tcb, sig_deliver_t sigdeliver)

  当一个或多个信号处理操作已排队等待执行时，OS 调用此函数。架构特定代码必须配置事物，以便尽快在 'tcb' 指定的线程上执行 'sigdeliver' 回调。

  此函数可能从中断处理逻辑调用。

  此操作不应导致任务被解除阻塞，也不应导致 sigdeliver 的任何立即执行。通常，需要考虑几种情况：

    #. 可能从中断处理程序调用此函数。在中断处理期间，所有 xcptcontext 结构应对所有任务有效。应修改该结构以在（此）中断返回时或在某些后续上下文切换到接收任务时调用 sigdeliver()。
    #. 如果不在中断处理程序中且 tcb 不是当前正在执行的任务，则再次只需修改接收任务的已保存 xcptcontext 结构，以便在该任务稍后恢复时调用 sigdeliver。
    #. 如果不在中断处理程序中且 tcb 是当前正在执行的任务——只需立即调用信号处理程序。

.. c:function:: void up_allocate_heap(FAR void **heap_start, size_t *heap_size)

  将调用此函数以动态设置堆区域。

  对于内核构建（``CONFIG_BUILD_PROTECTED=y`` 或 ``CONFIG_BUILD_KERNEL=y``）且同时具有内核空间和用户空间堆（``CONFIG_MM_KERNEL_HEAP=y``），此函数提供非受保护的用户空间堆的大小。如果提供了受保护的内核空间堆，则内核堆必须由类似的 ``up_allocate_kheap()`` 分配（和保护）。

.. c:function:: bool up_interrupt_context(void)

  如果我们当前在中断处理程序上下文中执行，则返回 true。

.. c:function::  void up_disable_irq(int irq)

  禁用 'irq' 指定的 IRQ。在许多架构上，有三个级别的中断启用：(1) 全局级别，(2) 中断控制器级别，和 (3) 设备级别。为了接收中断，必须在所有三个级别上启用它们。

  此函数实现在中断控制器级别启用 'irq' 指定的设备（如果架构支持）（up_irq_save() 支持全局级别，设备级别是硬件特定的）。

  如果架构不支持 ``up_disable_irq``，应在 NuttX 配置文件中定义 ``CONFIG_ARCH_NOINTC``。由于此 API 无法在所有架构上支持，因此应尽可能避免在通用实现中使用。

.. c:function:: void up_enable_irq(int irq)

  此函数实现在中断控制器级别禁用 'irq' 指定的设备（如果架构支持）（up_irq_restore() 支持全局级别，设备级别是硬件特定的）。

  如果架构不支持 ``up_disable_irq``，应在 NuttX 配置文件中定义 ``CONFIG_ARCH_NOINTC``。由于此 API 无法在所有架构上支持，因此应尽可能避免在通用实现中使用。

.. c:function:: void up_prioritize_irq(int irq)

  设置 IRQ 的优先级。

  如果架构支持 ``up_enable_irq``，应在 NuttX 配置文件中定义 ``CONFIG_ARCH_IRQPRIO``。由于此 API 无法在所有架构上支持，因此应尽可能避免在通用实现中使用。

.. c:function::  void up_putc(int ch)

  这是架构特定逻辑导出的调试接口。在控制台上输出一个字符。
