====================
地址环境
====================

支持内存管理单元 (MMU) 的 CPU 可以提供 *地址环境*，任务及其子线程在其中执行。配置通过设置配置变量 ``CONFIG_ARCH_HAVE_ADDRENV=y`` 来指示 CPU 支持地址环境的能力。这将启用实际地址环境支持的选择，通过选择配置变量 ``CONFIG_ARCH_ADDRENV=y`` 来指示。这些地址环境仅在通过 ``exec()`` 或 ``exec_module()`` 创建任务时才会创建（参见 ``include/nuttx/binfmt/binfmt.h``）。

当在板级配置中设置了 ``CONFIG_ARCH_ADDRENV=y`` 时，CPU 特定逻辑必须提供头文件 ``include/nuttx/arch.h`` 中定义的一组接口。这些接口在下面列出，并在后续段落中详细描述。

CPU 特定逻辑必须提供两类接口：

#. **二进制加载器支持**。这些是 ``binfmt/`` 中用于实例化具有地址环境的任务的低级接口。这些接口都操作 ``arch_addrenv_t`` 类型，该类型是任务组地址环境的抽象表示，如果定义了 ``CONFIG_ARCH_ADDRENV``，则该类型必须在 ``arch/arch.h`` 中定义。这些低级接口包括：

   - :c:func:`up_addrenv_create()`：创建地址环境。
   - :c:func:`up_addrenv_destroy()`：销毁地址环境。
   - :c:func:`up_addrenv_vtext()`：返回 ``.text`` 地址环境的虚拟基地址。
   - :c:func:`up_addrenv_vdata()`：返回 ``.bss``/``.data`` 地址环境的虚拟基地址。
   - :c:func:`up_addrenv_heapsize()`：返回初始堆大小。
   - :c:func:`up_addrenv_select()`：实例化地址环境。
   - :c:func:`up_addrenv_clone()`：将地址环境从一个位置复制到另一个位置。

#. **任务支持**。必须提供其他接口以支持 NuttX 任务逻辑使用的高级接口。这些接口由 ``sched/`` 中的函数使用，所有接口都操作由 ``up_addrenv_clone()`` 分配了地址环境的任务组。

   - :c:func:`up_addrenv_attach()`：克隆分配给新线程的组地址环境。当创建共享相同地址环境的 pthread 时执行此操作。
   - :c:func:`up_addrenv_detach()`：当任务/线程退出时释放线程对组地址环境的引用。

#. **动态栈支持**。``CONFIG_ARCH_STACK_DYNAMIC=y`` 表示用户进程栈位于其自己的地址空间中。如果选择了 ``CONFIG_BUILD_KERNEL`` 和 ``CONFIG_LIBC_EXECFUNCS``，则此选项也是 *必需的*。为什么？因为当我们实例化新进程的环境以进行初始化时，调用者的栈必须保存在其自己的地址空间中。

   **注意：** ``CONFIG_ARCH_STACK_DYNAMIC`` 选择的命名意味着支持动态栈分配。如果平台支持动态栈分配，则必须设置此选项。但此配置环境更一般的含义是栈拥有自己的地址空间。

   如果选择了 ``CONFIG_ARCH_STACK_DYNAMIC=y``，则平台特定代码必须导出以下额外接口：

   - :c:func:`up_addrenv_ustackalloc()`：创建栈地址环境
   - :c:func:`up_addrenv_ustackfree()`：销毁栈地址环境。
   - :c:func:`up_addrenv_vustack()`：返回栈的虚拟基地址
   - :c:func:`up_addrenv_ustackselect()`：实例化栈地址环境

#. 如果选择了 ``CONFIG_ARCH_KERNEL_STACK``，则每个用户进程将有两个栈：(1) 一个大的（可能是动态的）用户栈和 (2) 一个较小的内核栈。但是，如果同时选择了 ``CONFIG_BUILD_KERNEL`` 和 ``CONFIG_LIBC_EXECFUNCS``，则此选项是 *必需的*。为什么？因为当我们实例化和初始化新用户进程的地址环境时，我们将暂时失去旧用户进程的地址环境，包括其栈内容。内核 C 逻辑将因没有有效的栈而立即崩溃。

   如果选择了 ``CONFIG_ARCH_KERNEL_STACK=y``，则平台特定代码必须导出以下额外接口：

   - :c:func:`up_addrenv_kstackalloc`：分配进程内核栈。

.. c:function:: int up_addrenv_create(size_t textsize, size_t datasize, \
  size_t heapsize, FAR arch_addrenv_t *addrenv);

  当创建新任务时调用此函数，以便为新任务组实例化地址环境。up_addrenv_create() 本质上是新任务物理内存的分配器。

  :param textsize: 任务所需的 ``.text`` 地址环境大小（以字节为单位）。此区域可能只读/可执行。
  :param datasize: 任务所需的 ``.bss/.data`` 地址环境大小（以字节为单位）。此区域可能只读/可写。
  :param heapsize: 任务所需的堆地址环境初始大小（以字节为单位）。此区域可能只读/可写。
  :param addrenv: 返回任务地址环境表示的位置。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。

.. c:function:: int up_addrenv_destroy(arch_addrenv_t *addrenv)

  当最后一个线程离开任务组且任务组被销毁时调用此函数。此函数然后销毁已失效的地址环境，释放由 up_addrenv_create() 分配的底层物理内存。

  :param addrenv: 先前由 ``up_addrenv_create()`` 返回的任务地址环境表示。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。

.. c:function:: int up_addrenv_vtext(FAR arch_addrenv_t addrenv, FAR void **vtext)

  返回与新创建的地址环境关联的虚拟 .text 地址。二进制加载器使用此函数来获取可用于初始化新任务的地址。

  :param addrenv: 先前由 ``up_addrenv_create()`` 返回的任务地址环境表示。
  :param vtext: 返回虚拟地址的位置。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。

.. c:function:: int up_addrenv_vdata(FAR arch_addrenv_t *addrenv, size_t textsize, FAR void **vdata)

  返回与新创建的地址环境关联的虚拟 .data 地址。二进制加载器使用此函数来获取可用于初始化新任务的地址。

  :param addrenv: 先前由 ``up_addrenv_create()`` 返回的任务地址环境表示。
  :param textsize: 对于某些实现，text 和 data 将保存在同一内存区域（读/写/执行）中，在这种情况下，data 的虚拟地址仅位于公共区域的此偏移量处。
  :param vdata: 返回虚拟地址的位置。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。

.. c:function:: ssize_t up_addrenv_heapsize(FAR const arch_addrenv_t *addrenv)

  返回初始堆分配大小。即 up_addrenv_create() 在首次创建堆内存区域时分配的内存量。这可能与传递给 up_addrenv_create() 的 heapsize 参数相同或不同。

  :param addrenv: 先前由 ``up_addrenv_create()`` 返回的任务地址环境表示。

  :return: 成功时返回分配的初始堆大小；失败时返回负的 errno 值。

.. c:function:: int up_addrenv_select(arch_addrenv_t *addrenv)

  在为任务建立地址环境后（通过 up_addrenv_create()），可以调用此函数在虚拟地址空间中实例化该地址环境。例如，从文件加载任务代码或访问地址环境私有数据时可能需要此操作。

  :param addrenv: 先前由 ``up_addrenv_create()`` 返回的任务地址环境表示。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。

.. c:function:: int up_addrenv_clone(FAR const task_group_s *src, FAR struct task_group_s *dest)

  复制地址环境。这不会复制底层内存，只复制可用于将该内存实例化为地址环境的表示。

  :param src: 要复制的地址环境。
  :param dest: 接收复制的地址环境的位置。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。

.. c:function:: int up_addrenv_attach(FAR struct task_group_s *group, FAR struct tcb_s *tcb)

  当创建需要共享其任务组地址环境的线程时，从核心调度逻辑调用此函数。在这种情况下，可能需要为子线程"克隆"组的地址环境。

  注意：在大多数平台上，这种情况不需要做任何事情。仅仅是拥有地址环境的组的成员可能就足够了。

  :param group: 新线程所属的任务组。
  :param ctcb: 需要地址环境的线程的 TCB。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。

.. c:function:: int up_addrenv_detach(FAR struct task_group_s *group, FAR struct task_group_s *tcb)

  当任务或线程退出时调用此函数，以释放其对地址环境的引用。但是，地址环境应持续存在，直到任务组本身被销毁时调用 up_addrenv_destroy()。此线程独有的任何资源现在都可以被销毁。

  :param group: 线程所属的组。
  :param tcb: 其地址环境将被释放的任务或线程的 TCB。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。

.. c:function:: int up_addrenv_ustackalloc(FAR struct tcb_s *tcb, size_t stacksize)

  当创建新线程时调用此函数，以便为新线程的栈实例化地址环境。up_addrenv_ustackalloc() 本质上是新任务栈的物理内存分配器。

  :param tcb: 需要栈地址环境的线程的 TCB。
  :param stacksize: 任务所需的初始栈地址环境大小（以字节为单位）。此区域可能只读/可写。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。

.. c:function:: int up_addrenv_ustackfree(FAR struct tcb_s *tcb)

  当任何线程退出时调用此函数。此函数然后销毁线程栈的已失效地址环境，释放底层物理内存。

  :param tcb: 不再需要栈地址环境的线程的 TCB。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。

.. c:function:: int up_addrenv_vustack(FAR const struct tcb_s *tcb, FAR void **vstack)

  返回与新创建的栈地址环境关联的虚拟地址。

  :param tcb: 具有目标栈地址环境的线程的 TCB。
  :param vstack: 返回栈虚拟基地址的位置。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。

.. c:function:: int up_addrenv_ustackselect(FAR const struct tcb_s *tcb)

  在为任务的栈建立地址环境后（通过 up_addrenv_ustackalloc()）。可以调用此函数在虚拟地址空间中实例化该地址环境。这是每次上下文切换到新创建的线程（包括初始线程启动）之前的必要步骤。

  :param tcb: 具有要实例化的栈地址环境的线程的 TCB。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。

.. c:function:: int up_addrenv_kstackalloc(FAR struct tcb_s *tcb)

  当创建新线程时调用此函数以分配新线程的内核栈。对于某些没有内核栈的终止线程，也可能调用此函数。它必须能够容忍这种情况。

  :param tcb: 需要内核栈的线程的 TCB。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。

.. c:function:: int up_addrenv_kstackfree(FAR struct tcb_s *tcb);

  当任何线程退出时调用此函数。此函数释放内核栈。

  :param tcb: 不再需要内核栈的线程的 TCB。

  :return: 成功时返回零 (OK)；失败时返回负的 errno 值。
