==================================
BOARDIOC_SPINLOCK 自旋锁示例
==================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
========

此示例演示了 BOARDIOC_SPINLOCK 板控制接口在 NuttX 中管理硬件自旋锁操作的用法。BOARDIOC_SPINLOCK 接口提供了一种底层机制，用于使用自旋锁原语同步多线程或 CPU 之间对共享资源的访问。

什么是 BOARDIOC_SPINLOCK？
==========================

BOARDIOC_SPINLOCK 是一个板控制请求，允许应用程序通过 boardctl() 接口执行原子自旋锁操作。

BOARDIOC_SPINLOCK 接口支持三种主要操作：

* **BOARDIOC_SPINLOCK_LOCK** - 获取自旋锁（阻塞直到可用）
* **BOARDIOC_SPINLOCK_TRYLOCK** - 尝试获取自旋锁（非阻塞）
* **BOARDIOC_SPINLOCK_UNLOCK** - 释放自旋锁

前置条件
=============

以下配置选项必须启用：

.. code-block:: bash

    # Enable board spinlock support
    CONFIG_BOARDCTL_SPINLOCK=y


基本用法
===========

头文件
------------

在您的应用程序中包含以下头文件：

.. code-block:: c

    #include <sys/boardctl.h>        /* For boardctl() interface */
    #include <nuttx/spinlock.h>      /* For spinlock types */

数据结构
---------------

BOARDIOC_SPINLOCK 接口使用以下结构：

.. code-block:: c

    struct boardioc_spinlock_s
    {
        int action;                   /* Operation: LOCK, TRYLOCK, or UNLOCK */
        spinlock_t *lock;             /* Pointer to the spinlock variable */
        void *flags;                  /* Optional flags (reserved, set to NULL) */
    };

操作
-------

支持以下操作值：

.. code-block:: c

    BOARDIOC_SPINLOCK_LOCK        /* Acquire lock (blocks if unavailable) */
    BOARDIOC_SPINLOCK_TRYLOCK     /* Try to acquire (non-blocking) */
    BOARDIOC_SPINLOCK_UNLOCK      /* Release lock */

返回值
^^^^^^^^^^^^^

* **0** - 成功
* **负值** - 错误代码（转换为 errno）

简单锁示例
-------------------

以下是获取和释放自旋锁的基本示例：

.. code-block:: c

    spinlock_t my_lock;
    struct boardioc_spinlock_s spinlock_op;
    int ret;

    /* Initialize the spinlock */
    spin_lock_init(&my_lock);

    /* Acquire the spinlock */
    spinlock_op.action = BOARDIOC_SPINLOCK_LOCK;
    spinlock_op.lock = &my_lock;
    spinlock_op.flags = NULL;
    
    ret = boardctl(BOARDIOC_SPINLOCK, (uintptr_t)&spinlock_op);
    if (ret == 0) {
        printf("Spinlock acquired successfully\n");
    } else {
        printf("Failed to acquire spinlock: %d\n", ret);
    }

    printf("Inside spinlock\n");

    /* Release the spinlock */
    spinlock_op.action = BOARDIOC_SPINLOCK_UNLOCK;
    ret = boardctl(BOARDIOC_SPINLOCK, (uintptr_t)&spinlock_op);
    if (ret == 0) {
        printf("Spinlock released successfully\n");
    }
