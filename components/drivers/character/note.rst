=====================
Note 驱动程序接口
=====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Note 驱动程序是访问检测数据的接口。提供以下设备。

- :ref:`notectl`
- :ref:`noteram`

.. _notectl:

Notectl 设备 (``/dev/notectl``)
=================================

  ``/dev/notectl`` 是控制 NuttX 内核中检测过滤器的设备。该设备仅具有 ioctl 函数来控制过滤器。

``/dev/notectl`` 头文件
-----------------------------

  头文件 ``include/nuttx/note/notectl_driver.h`` 提供了该设备的接口定义。

``/dev/notectl`` 数据结构
--------------------------------

.. c:struct:: note_filter_mode_s

  .. code-block:: c

    struct note_filter_mode_s
    {
      unsigned int flag;          /* 过滤模式标志 */
    #ifdef CONFIG_SMP
      unsigned int cpuset;        /* 被监控的 CPU 集合 */
    #endif
    };

  - ``flag``：过滤模式标志。以下定义的按位 OR 可用。

    .. c:macro:: NOTE_FILTER_MODE_FLAG_ENABLE

      启用检测

    .. c:macro:: NOTE_FILTER_MODE_FLAG_SYSCALL

      启用系统调用检测

    .. c:macro:: NOTE_FILTER_MODE_FLAG_IRQ

      启用 IRQ 检测

  - ``cpuset``：（仅 SMP）仅监控位集中的 CPU。位 0=CPU0，位 1=CPU1，依此类推。

.. c:struct:: note_filter_syscall_s

  .. code-block:: c

    struct note_filter_syscall_s
    {
      uint8_t syscall_mask[];
    };

  - ``syscall_mask``：系统调用过滤器的位图数组。如果某位被设置，则对应的系统调用不会被记录。
    以下辅助宏可用：

    .. c:macro:: NOTE_FILTER_SYSCALLMASK_SET(nr, s)

      将系统调用号 `nr` 设置为被屏蔽。`s` 指定 `struct note_filter_syscall_s` 的变量

    .. c:macro:: NOTE_FILTER_SYSCALLMASK_CLR(nr, s)

      将系统调用号 `nr` 设置为未屏蔽。

    .. c:macro:: NOTE_FILTER_SYSCALLMASK_ISSET(nr, s)

      检查系统调用号 `nr` 是否被屏蔽。如果被屏蔽则返回 True。

    .. c:macro:: NOTE_FILTER_SYSCALLMASK_ZERO(s)

      清除所有屏蔽。

.. c:struct:: note_filter_irq_s

  .. code-block:: c

    struct note_filter_irq_s
    {
      uint8_t irq_mask[];
    };

  - ``irq_mask``：IRQ 过滤器的位图数组。如果某位被设置，则对应的 IRQ 不会被记录。
    以下辅助宏可用：

    .. c:macro:: NOTE_FILTER_IRQMASK_SET(nr, s)

      将 IRQ 号 `nr` 设置为被屏蔽。`s` 指定 `struct note_filter_irq_s` 的变量

    .. c:macro:: NOTE_FILTER_IRQMASK_CLR(nr, s)

      将 IRQ 号 `nr` 设置为未屏蔽。

    .. c:macro:: NOTE_FILTER_IRQMASK_ISSET(nr, s)

      检查 IRQ 号 `nr` 是否被屏蔽。如果被屏蔽则返回 True。

    .. c:macro:: NOTE_FILTER_IRQMASK_ZERO(s)

      清除所有屏蔽。

``/dev/notectl`` Ioctl
-----------------------

.. c:macro:: NOTECTL_GETMODE

  获取 note 过滤模式

  :argument: 指向 :c:struct:`note_filter_mode_s` 的可写指针

  :return: 成功时返回 0 (``OK``)，当前 note 过滤模式存储到给定指针。
    失败时返回取反的 ``errno``。

.. c:macro:: NOTECTL_SETMODE

  设置 note 过滤模式

  :argument: 指向 :c:struct:`note_filter_mode_s` 的只读指针

  :return: 成功时返回 0 (``OK``)，给定的过滤模式被设置为当前设置。
    失败时返回取反的 ``errno``。

.. c:macro:: NOTECTL_GETSYSCALLFILTER

  获取系统调用过滤器设置

  :argument: 指向 :c:struct:`note_filter_syscall_s` 的可写指针

  :return: 成功时返回 0 (``OK``)，当前系统调用过滤模式存储到给定指针。
    失败时返回取反的 ``errno``。

.. c:macro:: NOTECTL_SETSYSCALLFILTER

  设置系统调用过滤器设置

  :argument: 指向 :c:struct:`note_filter_syscall_s` 的只读指针

  :return: 成功时返回 0 (``OK``)，给定的系统调用过滤模式被设置为当前设置。
    失败时返回取反的 ``errno``。

.. c:macro:: NOTECTL_GETIRQFILTER

  获取 IRQ 过滤器设置

  :argument: 指向 :c:struct:`note_filter_irq_s` 的可写指针

  :return: 成功时返回 0 (``OK``)，当前 IRQ 过滤模式存储到给定指针。
    失败时返回取反的 ``errno``。

.. c:macro:: NOTECTL_SETIRQFILTER

  设置 IRQ 过滤器设置

  :argument: 指向 :c:struct:`note_filter_irq_s` 的只读指针

  :return: 成功时返回 0 (``OK``)，给定的 IRQ 过滤模式被设置为当前设置。
    失败时返回取反的 ``errno``。

.. _noteram:

Noteram 设备 (``/dev/note``)
==============================

  ``/dev/note`` 是获取跟踪（检测）数据的设备。该设备具有读取函数来获取数据和 ioctl 函数来控制缓冲模式。

``/dev/note`` 头文件
--------------------------

  头文件 ``include/nuttx/note/noteram_driver.h`` 提供了该设备的接口定义。

``/dev/note`` 数据结构
--------------------------------

.. c:struct:: noteram_get_taskname_s

  .. code-block:: c

    struct noteram_get_taskname_s
    {
      pid_t pid;
      char taskname[CONFIG_TASK_NAME_SIZE + 1];
    };

  - ``pid``：要获取任务名称的任务 ID。

  - ``taskname``：与给定 pid 对应的任务名称字符串。

``/dev/note`` Ioctl
--------------------

.. c:macro:: NOTERAM_CLEAR

  清除循环缓冲区的所有内容

  :argument: 忽略

  :return: 始终返回 0。

.. c:macro:: NOTERAM_GETMODE

  获取覆写模式

  :argument: 指向 ``unsigned int`` 的可写指针。
    覆写模式取以下值之一。

    .. c:macro:: NOTERAM_MODE_OVERWRITE_DISABLE

      禁用覆写模式。当缓冲区已满时，将停止接收数据。

    .. c:macro:: NOTERAM_MODE_OVERWRITE_ENABLE

      启用覆写模式。

    .. c:macro:: NOTERAM_MODE_OVERWRITE_OVERFLOW

      禁用覆写模式且缓冲区已满。

  :return: 成功时返回 0 (``OK``)，当前覆写模式存储到给定指针。
           失败时返回取反的 ``errno``。

.. c:macro:: NOTERAM_SETMODE

  设置覆写模式

  :argument: 指向 ``unsigned int`` 的只读指针。

  :return: 成功时返回 0 (``OK``)，给定的覆写模式被设置为当前设置。
    失败时返回取反的 ``errno``。

.. c:macro:: FIONREAD

  获取缓冲区中未读字节数

  :argument: 指向 ``unsigned int`` 的可写指针，用于接收未读字节数。

  :return: 成功时返回 0 (``OK``)，未读字节数存储到给定指针。
    失败时返回取反的 ``errno``。

.. c:macro:: PIPEIOC_POLLINTHRD

  设置 POLLIN 事件的轮询阈值

  :argument: 一个 unsigned int 值，指定以字节为单位的阈值。当缓冲区中的未读数据大于或等于此值时，将通知 POLLIN。

  :return: 成功时返回 0 (``OK``) 并设置阈值。失败时返回取反的 ``errno``。

过滤器控制 API
===================

以下 API 是直接控制 note 过滤器的函数。这些是内核 API，应用程序只能在 FLAT 构建中使用它们。

使用以下 API 需要头文件 ``include/nuttx/sched_note.h``。

API 描述
---------------

.. c:function:: void sched_note_filter_mode(struct note_filter_mode_s *oldm, struct note_filter_mode_s *newm);

  设置和获取 note 过滤模式。
  （与 :c:macro:`NOTECTL_GETMODE` / :c:macro:`NOTECTL_SETMODE` ioctl 相同）

  :param oldm: 指向 :c:struct:`note_filter_mode_s` 的可写指针，用于获取当前过滤模式。
    如果为 0，则不写入数据。
  :param newm: 指向 :c:struct:`note_filter_mode_s` 的只读指针，包含新的过滤模式。
    如果为 0，则不更新过滤模式。

  :return: 无

.. c:function:: void sched_note_filter_syscall(struct note_filter_syscall_s *oldf, struct note_filter_syscall_s *newf);

  设置和获取系统调用过滤器设置。
  （与 :c:macro:`NOTECTL_GETSYSCALLFILTER` / :c:macro:`NOTECTL_SETSYSCALLFILTER` ioctl 相同）

  :param oldf: 指向 :c:struct:`note_filter_syscall_s` 的可写指针，用于获取当前系统调用过滤器设置。
    如果为 0，则不写入数据。
  :param newf: 指向 :c:struct:`note_filter_syscall_s` 的只读指针，包含新的系统调用过滤器设置。
    如果为 0，则不更新设置。

  :return: 无

.. c:function:: void sched_note_filter_irq(struct note_filter_irq_s *oldf, struct note_filter_irq_s *newf);

  设置和获取 IRQ 过滤器设置。
  （与 :c:macro:`NOTECTL_GETIRQFILTER` / :c:macro:`NOTECTL_SETIRQFILTER` ioctl 相同）

  :param oldf: 指向 :c:struct:`note_filter_irq_s` 的可写指针，用于获取当前 IRQ 过滤器设置。
    如果为 0，则不写入数据。
  :param newf: 指向 :c:struct:`note_filter_irq_s` 的只读指针，包含新的 IRQ 过滤器设置。
    如果为 0，则不更新设置。

  :return: 无
