===========================================
对称多处理 (SMP) 应用
===========================================

根据维基百科："对称多处理 (SMP) 涉及一种对称多处理器系统的硬件和软件架构，其中两个或多个相同的处理器连接到单一的共享主存，可以完全访问所有 I/O 设备，并由单一的操作系统实例控制，该实例对所有处理器一视同仁，不为特殊目的保留任何处理器。当今大多数多处理器系统使用 SMP 架构。对于多核处理器，SMP 架构适用于各核心，将它们视为独立的处理器。"

"SMP 系统是紧密耦合的多处理器系统，具有一组独立运行的同构处理器，每个处理器执行不同的程序、处理不同的数据，并具有共享公共资源（内存、I/O 设备、中断系统等）的能力，通过系统总线或交叉开关互连。"

有关 NuttX SMP 实现的技术说明，请参阅 NuttX `SMP Wiki
页面 <https://cwiki.apache.org/confluence/display/NUTTX/SMP>`__。

.. c:function:: spinlock_t up_testset(volatile FAR spinlock_t *lock)

  对提供的自旋锁执行原子测试并设置操作。

  :param lock: 自旋锁对象的地址。

  :return: 返回时自旋锁始终处于锁定状态。返回自旋锁变量的先前值，
    如果自旋锁之前已锁定则返回 SP_LOCKED（表示测试并设置操作未能获取锁），
    如果自旋锁之前未锁定则返回 SP_UNLOCKED（表示我们成功获取了锁）。

.. c:function:: int up_cpu_index(void)

  返回一个范围在 0 到 (CONFIG_SMP_NCPUS-1) 之间的索引，
  对应于当前正在执行的 CPU。

  :return: 一个范围在 0 到 (CONFIG_SMP_NCPUS-1) 之间的整数索引，
    对应于当前正在执行的 CPU。

.. c:function:: int up_cpu_start(int cpu)

  在 SMP 配置中，最初只有 CPU 0 是活跃的。系统初始化在该单线程上进行。
  在 OS 初始化完成之后、开始正常多任务之前，将通过调用此函数启动其他 CPU。

  每个 CPU 启动时会获得其 IDLE 任务的入口点。每个 CPU 的 IDLE 任务的 TCB
  已被初始化并放置在该 CPU 的 g_assignedtasks[cpu] 列表中。栈也已分配并初始化。

  OS 初始化逻辑会反复调用此函数，直到每个 CPU 都已启动，即从 1 到
  (CONFIG_SMP_NCPUS-1)。

  :param cpu: 要启动的 CPU 的索引。这将是一个范围从 1 到
    ``(CONFIG_SMP_NCPUS-1)`` 的数值。（CPU 0 已经处于活跃状态）。

  :return: 成功返回零 (OK)；失败返回取负的 errno 值。

.. c:function:: int up_cpu_pause(int cpu)

  保存 ``g_assignedtasks[cpu]`` 任务列表头部的当前任务状态，
  然后暂停该 CPU 上的任务执行。

  当一个 CPU 上执行的逻辑需要修改另一个 CPU 的 ``g_assignedtasks[cpu]``
  列表状态时，OS 会调用此函数。

  :param cpu: 要暂停的 CPU 的索引。这不应该是当前正在执行的 CPU 的索引。

  :return: 成功返回零 (OK)；失败返回取负的 errno 值。

.. c:function:: int up_cpu_resume(int cpu)

  在通过 up_cpu_pause() 暂停后重新启动 CPU，恢复
  ``g_assignedtasks[cpu]`` 列表头部的任务状态，并恢复正常任务调度。

  此函数在 ``up_cpu_pause()`` 之后调用，用于在修改其
  ``g_assignedtasks[cpu]`` 列表后恢复 CPU 的运行。

  :param cpu: 要恢复的 CPU 的索引。这不应该是当前正在执行的 CPU 的索引。

  :return: 成功返回零 (OK)；失败返回取负的 errno 值。
