.. _notifier_chain:

==============
Notifier Chain
==============

NuttX 提供了一种称为 *通知链（Notifier Chain）* 的回调列表机制。
通知链本质上是在特定时刻（如系统断言、关机和重启）使用的回调列表。

**通知链** 与 Linux 的通知链非常相似，但实现上存在一些差异。

通知链的类别
=========================

目前有两种不同类别的通知链。

原子通知链
----------------------

原子通知链：链中的回调在中断/原子上下文中运行。
在 NuttX 中，回调允许阻塞（而在 Linux 中，原子通知链的回调不允许阻塞）。
原子通知链的一个示例是在断言时关闭 FPU。

阻塞通知链
------------------------

阻塞通知链：链中的回调在进程上下文中运行。
回调允许阻塞。阻塞通知链的一个示例是需要有序关机时的处理。

通用通知链接口
================================

通知链块类型
--------------------

-  ``struct notifier_block``：定义一个通知回调条目。

通知链接口
-------------------------

.. c:function:: void panic_notifier_chain_register(FAR struct notifier_block *nb)

  将通知器添加到 panic 通知链中。

  panic 通知链是一个原子通知链，它将在系统断言时被调用。

  :param nb: 通知链中的新条目。

.. c:function:: void panic_notifier_chain_unregister(FAR struct notifier_block *nb)

  从 panic 通知链中移除通知器。

  panic 通知链是一个原子通知链，它将在系统断言时被调用。

  :param nh: 要从通知链中移除的条目。

.. c:function:: void panic_notifier_call_chain(unsigned long action, FAR void *data)

  调用 panic 通知链中的函数。

  panic 通知链是一个原子通知链，它将在系统断言时被调用。

  :param action: 原样传递给通知函数的值。
  :param data: 原样传递给通知函数的指针。

.. c:function:: void register_reboot_notifier(FAR struct notifier_block *nb)

  将通知器添加到 reboot 通知链中。

  reboot 通知链是一个原子通知链。

  :param nb: 通知链中的新条目。

.. c:function:: void unregister_reboot_notifier(FAR struct notifier_block *nb)

  从 reboot 通知链中移除通知器。

  reboot 通知链是一个原子通知链。

  :param nh: 要从通知链中移除的条目。

.. c:function:: void reboot_notifier_call_chain(unsigned long action, FAR void *data)

  调用 reboot 通知链中的函数。

  reboot 通知链是一个原子通知链。

  :param action: 原样传递给通知函数的值。
  :param data: 原样传递给通知函数的指针。
