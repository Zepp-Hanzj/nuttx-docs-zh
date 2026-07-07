=====================
互斥锁
=====================

nxmutex
=======

使用 `nxmutex` 前缀的 API 来保护资源。实际上，nxmutex 是基于 nxsem 实现的。nxmutex 和 nxsem 的区别在于，nxmutex 默认支持优先级继承，而 nxsem 默认不支持优先级继承。

典型用法
-------------

为驱动调用 nxmutex_init()，当两个任务使用该驱动时，它们的时序如下：

=================  ====================
taskA              taskB
=================  ====================
nxmutex_lock()     nxmutex_lock()
获得锁，运行中     等待锁
nxmutex_unlock()   等待锁
-                  获得锁，运行中
-                  nxmutex_unlock()
=================  ====================

优先级继承
====================

如果选择了 `CONFIG_PRIORITY_INHERITANCE`，持有互斥锁的任务的优先级可能会被改变。
以下是一个示例：

  有三个任务，优先级分别为高、中、低。
  我们称它们为 `Htask`、`Mtask`、`Ltask`。

  `Htask` 和 `Ltask` 将持有同一个互斥锁。`Mtask` 不持有互斥锁。

如果未选择 `CONFIG_PRIORITY_INHERITANCE`，任务执行顺序为：
  #. `Ltask` 先获得互斥锁
  #. 然后 `Htask` 运行，`Htask` 无法获得互斥锁，因此等待
  #. 然后 `Mtask` 运行，因为 `Mtask` 的优先级高于 `Ltask`
  #. 当 `Mtask` 完成后，`Ltask` 开始运行
  #. 当 `Ltask` 完成后，`Htask` 开始运行

从上述过程可以看出，中优先级任务在高优先级任务之前运行，这是不可接受的。

如果选择了 `CONFIG_PRIORITY_INHERITANCE`，任务执行顺序为：
  #. `Ltask` 先获得互斥锁
  #. 然后 `Htask` 运行，`Htask` 无法获得互斥锁，然后将 `Ltask` 的优先级提升到与 `Htask` 相同
  #. 因为 `Ltask` 的优先级高于 `Mtask`，所以 `Mtask` 不会运行
  #. 当 `Ltask` 完成后，`Htask` 开始运行
  #. 当 `Htask` 完成后，`Mtask` 开始运行

优先级继承可以防止中优先级任务在高优先级任务之前运行。

API 描述
===============
.. c:function:: void nxmutex_init(FAR mutex_t *mutex)

    此函数初始化未命名的互斥锁。
    :param mutex: 要初始化的互斥锁。

    :return:
      成功返回零 (OK)。失败返回取负的 errno 值。

.. c:function:: void nxmutex_destroy(FAR mutex_t *mutex)

    此函数销毁未命名的互斥锁。
    :param mutex: 要销毁的互斥锁。

    :return:
      成功返回零 (OK)。失败返回取负的 errno 值。

.. c:function:: void nxmutex_lock(FAR mutex_t *mutex)

    此函数尝试锁定 ``mutex`` 引用的互斥锁。互斥锁通过信号量实现，
    因此如果信号量值为（<=）零，则调用任务在成功获取锁之前不会返回。

    :param mutex: 互斥锁描述符。

    :return:
      成功返回零 (OK)。失败返回取负的 errno 值。

.. c:function:: void nxmutex_trylock(FAR mutex_t *mutex)

    此函数仅在互斥锁当前未被锁定时才锁定它。
    如果互斥锁已被锁定，调用将不阻塞地返回。

    :param mutex: 互斥锁描述符。

    :return:
      成功返回零 (OK)。失败返回取负的 errno 值。
      可能的返回错误：

      EINVAL - 锁定互斥锁的无效尝试
      EAGAIN - 互斥锁不可用。

.. c:function:: void nxmutex_is_locked(FAR mutex_t *mutex)

    此函数获取 ``mutex`` 引用的互斥锁的锁定状态。

    :param mutex: 互斥锁描述符。

    :return:
      如果互斥锁已锁定则返回 `true`，否则返回 `false`。

.. c:function:: void nxmutex_unlock(FAR mutex_t *mutex)

    此函数尝试解锁 ``mutex`` 引用的互斥锁。

    :param mutex: 互斥锁描述符。

    :return:
      成功返回零 (OK)。失败返回取负的 errno 值。

.. c:function:: void nxmutex_reset(FAR mutex_t *mutex)

    此函数重置 ``mutex`` 引用的互斥锁状态。

    :param mutex: 互斥锁描述符。

    :return:
      成功返回零 (OK)。失败返回取负的 errno 值。
