==============
事件
==============

事件组是同步原语，允许任务在继续之前等待多个条件得到满足。在任务需要等待多个事件同时发生的场景中，它们特别有用。这个概念在实时操作系统 (RTOS) 中尤其强大。

概述
=========================

事件组由一组二进制标志组成，每个标志代表一个特定事件。任务可以设置、清除和等待这些标志。当任务在事件组上等待时，它可以指定感兴趣的标志，以及是否希望等待所有指定的标志被设置还是只需其中任何一个。

配置选项
=====================

``CONFIG_SCHED_EVENTS``
	 此选项启用事件对象。线程可以在事件对象上等待特定事件，但线程和 ISR 都可以向事件对象传递事件。

通用事件接口
================================

事件类型
--------------------

-  ``nxevent_t``。定义一个事件组条目。
-  ``nxevent_mask_t``。定义一个事件掩码值。

通知链接口
-------------------------

.. c:function:: int nxevent_init(FAR nxevent_t *event, nxevent_mask_t events)

  初始化事件对象，设置要发布到事件的默认事件集。

  :param event: 事件对象的地址
  :param events: 要发布到事件的事件集

.. c:function:: int nxevent_destroy(FAR nxevent_t *event)

  此函数用于销毁事件。

  :param event: 事件对象的地址

.. c:function:: int nxevent_reset(FAR nxevent_t *event, nxevent_mask_t events)

  将事件掩码重置为特定值。

  :param event: 事件对象的地址
  :param events: 要发布到事件的事件集

.. c:function:: int nxevent_post(FAR nxevent_t *event, nxevent_mask_t events, nxevent_flags_t eflags)

  向事件对象发布一个或多个事件。

  此例程向事件对象发布一个或多个事件。所有在事件对象上等待且其等待条件因本次发布而满足的任务将立即解除挂起。

  发布与设置不同，因为发布的事件与事件对象跟踪的当前事件集合并。

  :param event: 事件对象的地址
  :param events: 要发布到事件的事件集。将 events 设置为 0 将被视为 any，立即唤醒等待线程。
  :param eflags: 事件标志

.. c:function:: nxevent_mask_t nxevent_wait(FAR nxevent_t *event, nxevent_mask_t events, nxevent_flags_t eflags)

  等待所有指定的事件。

  此例程在事件对象上等待，直到所有指定的事件都已传递到事件对象。线程可以等待最多 32 个不同编号的事件，这些事件表示为单个 32 位字中的位。

  :param event: 事件对象的地址
  :param events: 要等待的事件集，0 表示等待任何事件
  :param eflags: 事件标志

.. c:function:: nxevent_mask_t nxevent_tickwait(FAR nxevent_t *event, nxevent_mask_t events, nxevent_flags_t eflags, uint32_t delay)

  等待所有指定的事件，直到指定的 tick 时间。

  此例程在事件对象上等待，直到所有指定的事件都已传递到事件对象，或最大等待时间超时已过期。线程可以等待最多 32 个不同编号的事件，这些事件表示为单个 32 位字中的位。

  :param event: 事件对象的地址。
  :param events: 要等待的事件集，0 表示等待任何事件
  :param eflags: 事件标志
  :param delay: 从开始时间到事件发布之间的等待 tick 数。如果 ticks 为零，则此函数等同于 nxevent_trywait()。

.. c:function:: nxevent_mask_t nxevent_trywait(FAR nxevent_t *event, nxevent_mask_t events, nxevent_flags_t eflags)

  尝试等待所有指定的事件。

  此例程尝试在事件对象上等待，如果任何指定的事件已传递到事件对象。线程可以等待最多 32 个不同编号的事件，这些事件表示为单个 32 位字中的位。

  :param event: 事件对象的地址
  :param events: 要等待的事件集，0 表示等待任何事件
  :param eflags: 事件标志

.. c:function:: nxevent_mask_t nxevent_clear(FAR nxevent_t *event, nxevent_mask_t mask)

  此函数用于从给定事件对象的事件掩码中清除特定位。

  :param event: 事件对象的地址
  :param mask: 指定应清除哪些事件标志的位掩码

.. c:function:: nxevent_mask_t nxevent_getmask(FAR nxevent_t *event)

  此函数返回当前事件对象的事件掩码值。

  :param event: 返回事件组引用的位置。

  :return: 当前事件对象的事件掩码值。

.. c:function:: int nxevent_open(FAR nxevent_t **event, FAR const char *name, int oflags, ...)

  此函数在命名事件组和任务之间建立连接。任务可以使用此调用返回的地址引用与名称关联的事件组。事件组可在后续调用 nxevent_wait() 或 nxevent_post() 中使用。事件组保持可用，直到通过成功调用 nxevent_close() 关闭事件组。

  如果任务使用相同名称多次调用 event_open()，则返回相同的事件组地址。

  :param event: 返回事件组引用的位置。
  :param name: 事件组名称。
  :param oflags: 事件组创建选项。这可以是以下设置：

    -  ``oflags`` = 0：仅在事件组已存在时连接。
    -  ``oflags`` = O_CREAT：如果事件组存在则连接，否则创建事件组。
    -  ``oflags`` = O_CREAT|O_EXCL：创建新事件组，除非已存在。

  :param ...: 可选参数。当指定 O_CREAT 标志时，需要两个可选参数：

    -  ``mode``：mode 参数的类型为 mode_t。此参数是必需的但在当前实现中未使用。
    -  ``events``：events 参数的类型为 unsigned。事件组以 ``events`` 的初始值创建。

  :return: 0 (OK)，如果失败则返回负的 errno。

.. c:function:: int nxevent_close(FAR nxevent_t *event)

    调用此函数表示调用任务已完成对指定命名事件组的使用。event_close() 释放系统为此命名事件组分配的任何系统资源。

  :param event: 事件描述符

  :return: 0 (OK)，如果失败则返回负的 errno。
