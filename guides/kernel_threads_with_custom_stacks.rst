=================================
具有自定义栈的内核线程
=================================

.. warning:: 
    迁移自: 
    https://cwiki.apache.org/confluence/display/NUTTX/Kernel+Threads+with+Custom+Stacks


背景
==========

在某些条件下，可能需要创建一个栈位于某些自定义内存中的内核线程。本页面提供了一个如何做到这一点的示例：

示例
=======

以下是某个函数的主体。它期望有以下输入：

1. ``taskname``：要启动的内核线程的名称
2. ``stacksize``：自定义栈的大小
3. ``priority``：要启动的内核线程的优先级
4. ``entry_point``：要启动的内核线程的入口点
5. ``argv``：传递给内核线程的可选参数字符串数组

.. code-block:: c 

    /* Allocate a TCB for the new kernel thread.  kmm_zalloc() is
    * used to that all fields of the new TCB will be zeroed.
    */

    tcb = kmm_zalloc(sizeof(struct tcb_s));
    if (tcb == NULL)
    {
        return -ENOMEM;
    }

    /* Indicate (1) that this is a kernel thread and that (2) a custom
    * stack will be used.
    */

    tcb->flags = TCB_FLAG_TTYPE_KERNEL | TCB_FLAG_CUSTOM_STACK;

    /* Allocate the custom stack for the new kernel thread.
    *
    * Do whatever it takes to get a reference to the custom stack.
    * Here custom_alloc() is used as a placeholder for whatever
    * that may be.
    */

    stack = (FAR uint32_t *)custom_alloc(stacksize);
    if (stack == NULL)
    {
        kmm_free(tcb);
        return -ENOMEM;
    }

    /* Initialize the TCB.  This will initialize all remaining
    * fields of the TCB, associate the stack to the TCB, allocate
    * any additional resources needed by the kernel thread, and
    * place the TCB in a list of inactive tasks.
    */

    ret = task_init((FAR struct tcb_s *)tcb, progname, priority,
                    stack, stacksize, entry_point, argv);
    if (ret < 0)
    {
        kmm_free(tcb);
        custom_free(stack);
        return ret;
    }

    /* Then activate the kernel thread at the provided priority */

    ret = task_activate((FAR struct tcb_s *)tcb);
    if (ret < 0)
    {
        /* nxtask_unit() will undo all of the operations of nxtask_init().
        * It also has the side-effect of freeing the TCB which it assumes
        * was allocated with one of the kmm_malloc()functions.
        */

        nxtask_uninit(tcb);
        custom_free(stack);
        return ret;
    }

    return OK;


释放 TCB
===============

在调用 ``nxtask_init()`` 之前，可以使用 kmm 分配器释放 TCB，具体来说是函数 ``kmm_free()``。但是，在调用 ``nxtask_init()`` 之后，额外的资源将与 TCB 关联，您必须调用 ``nxtask_uninit()`` 来释放 TCB 及其所有关联资源。``kmm_free()`` 将被 ``nxtask_uninit()`` 内部用于释放 TCB。请注意，在任何情况下，TCB 必须使用 ``kmm_malloc()`` 分配函数之一分配。

在 ``nxtask_activate()`` 成功返回后，您绝不能释放 TCB。

释放自定义栈内存
===============================

``TCB_FLAG_CUSTOM_STACK`` 标志的效果是，如果内核线程退出、崩溃或被杀死，OS 不会尝试释放自定义栈内存。这在您的实现中重要吗？这会导致某种内存泄漏吗？如果您的应用程序需要任何类型的清理来释放自定义栈内存，您可能需要使用 ``on_exit()`` 或 ``atexit()`` 函数在内核线程终止时获取回调。

如果 ``TCB_FLAG_CUSTOM_STACK`` 未在 TCB 标志中设置，OS 将尝试使用 ``kmm_free()`` 释放栈，这在这种情况下可能不是您想要的。

实际逻辑稍微复杂一些且有些冗余：

* 如果 ``TCB_FLAG_CUSTOM_STACK`` 在 TCB 标志中设置，则不会尝试释放自定义栈。
* 如果 ``TCB_FLAG_CUSTOM_STACK`` 未在 TCB 标志中设置，则只有在栈位于内核内存池中时才会为内核线程释放栈。

因此，实际上 ``TCB_FLAG_CUSTOM_STACK`` 可能不是必需的。但在您不希望自定义栈被释放的所有情况下包含它是最安全的选择。

在 ``nxtask_activate()`` 成功返回后且直到内核线程终止之前，您不得释放自定义栈。
