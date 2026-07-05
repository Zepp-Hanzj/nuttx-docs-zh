====================
使用内核线程
====================

.. warning:: 
    迁移自： 
    https://cwiki.apache.org/confluence/display/NUTTX/Using+Kernel+Threads


构建配置
====================

NuttX 可以在三种不同的配置下构建：(1) FLAT 构建，所有代码位于公共地址空间中；(2) PROTECTED 构建，使用内存保护单元 (MPU) 将内存分为操作系统的特权内存和所有应用程序的非特权内存；(3) KERNEL 构建，使用内存管理单元 (MMU) 将操作系统置于特权地址空间，并将任务（或进程）置于其自己的虚拟地址空间中。

在后两种配置中，应用程序位于操作系统地址空间之外，在所有配置中应用程序都无法访问操作系统的任何内部资源。

有关这些构建配置的更多信息，请参阅 `内存配置 Wiki 页面 <https://cwiki.apache.org/confluence/display/NUTTX/Memory+Configurations>`_。

线程类型
============

NuttX 支持三类线程：任务、pthreads 和内核线程。任务和 pthreads 都是应用程序线程，通过一些使用语义和它们的层次关系来区分。任务通过几种不同的机制创建：``task_create()``、``task_spawn()``、``execv()``、``posix_spawn()`` 等。然后任务可以使用 ``pthread_create()`` 创建 pthreads。

有关任务和 pthreads 的更多信息，请参阅 `NuttX 任务 <https://cwiki.apache.org/confluence/display/NUTTX/NuttX+Tasking>`_ Wiki 页面。

内核线程
==============

内核线程实际上就像任务，只是它们在操作系统内部运行，并通过 ``kthread_create()`` 启动，该函数在 ``include/nuttx/kthread.h`` 中有原型。它们与任务的不同之处在于 (1) 在 PROTECTED 和 KERNEL 构建中，它们具有完全的监督者权限，(2) 它们可以完全访问所有操作系统内部资源。

要将任务构建到操作系统中作为内核线程，你只需：(1) 将内核线程代码放在你的板源代码目录中，(2) 在你的板启动逻辑中使用 ``kthread_create()`` 启动它。NuttX 源代码树中有几个这样的示例。这是一个：`https://github.com/apache/nuttx/blob/master/boards/arm/stm32/viewtool-stm32f107/src/stm32_highpri.c <https://github.com/apache/nuttx/blob/master/boards/arm/stm32/viewtool-stm32f107/src/stm32_highpri.c>`_

这是你可以用来构建最优解决方案的另一个技巧：将应用程序的部分创建为内核线程：它们需要位于你的 board/src 目录中，并且需要在你的板启动逻辑中使用 ``kthread_create()`` 启动。就这样。
