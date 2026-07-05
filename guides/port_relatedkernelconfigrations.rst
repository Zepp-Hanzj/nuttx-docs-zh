相关内核配置列表
=========================================

此列表的前提：NuttX12.4.0、cxd56xx、非 SMP 和 Flat 构建。

通过分析启动序列，我发现了以下内核配置。
我认为最好考虑它们，尽管其中大部分可能已设置为默认值。

+-----------------+-------------------------------+------------------+
| 类别            | 项目                          | 说明             |
+-----------------+-------------------------------+------------------+
| 内存映射        | CONFIG_RAM_START              | `arch/Kconfig`_  |
+                 +-------------------------------+                  +
|                 | CONFIG_RAM_SIZE               |                  |
+                 +-------------------------------+------------------+
|                 | CONFIG_IDLETHREAD_STACKSIZE   | `sched/Kconfig`_ |
+                 +-------------------------------+------------------+
|                 | CONFIG_MM_REGIONS             | `mm/Kconfig`_    |
+                 +-------------------------------+------------------+
|                 | CONFIG_ARCH_HAVE_EXTRA_HEAPS  | `arch/Kconfig`_  |
+-----------------+-------------------------------+------------------+
| 中断            | CONFIG_ARCH_RAMVECTORS        | `arch/Kconfig`_  |
+                 +-------------------------------+                  +
|                 | CONFIG_ARCH_IRQPRIO           |                  |
+                 +-------------------------------+                  +
|                 | CONFIG_ARCH_INTERRUPTSTACK    |                  |
+                 +-------------------------------+                  +
|                 | CONFIG_SUPPRESS_INTERRUPTS    |                  |
+                 +-------------------------------+                  +
|                 | CONFIG_SUPPRESS_TIMER_INTS    |                  |
+                 +-------------------------------+------------------+
|                 | CONFIG_IRQCHAIN               | `sched/Kconfig`_ |
+-----------------+-------------------------------+------------------+
| 定时器          | CONFIG_SYSTEMTICK_EXTCLK      | `sched/Kconfig`_ |
+                 +-------------------------------+                  +
|                 | CONFIG_SCHED_TICKLESS         |                  |
+-----------------+-------------------------------+------------------+
| 串口            | CONFIG_STANDARD_SERIAL        | `serial/Kconfig`_|
+                 +-------------------------------+------------------+
|                 | CONFIG_DEV_CONSOLE            | `sched/Kconfig`_ |
+-----------------+-------------------------------+------------------+
| 板              | CONFIG_BOARD_EARLY_INITIALIZE | `sched/Kconfig`_ |
+                 +-------------------------------+                  +
|                 | CONFIG_BOARD_LATE_INITIALIZE  |                  |
+                 +-------------------------------+                  +
|                 | CONFIG_INIT_ENTRYPOINT        |                  |
+-----------------+-------------------------------+------------------+
| POSIX API       | CONFIG_PRIORITY_INHERITANCE   | `sched/Kconfig`_ |
+                 +-------------------------------+                  +
|                 | CONFIG_SEM_PREALLOCHOLDERS    |                  |
+                 +-------------------------------+                  +
|                 | CONFIG_DISABLE_MQUEUE         |                  |
+                 +-------------------------------+                  +
|                 | CONFIG_DISABLE_MQUEUE_SYSV    |                  |
+                 +-------------------------------+                  +
|                 | CONFIG_PREALLOC_MQ_MSGS       |                  |
+                 +-------------------------------+                  +
|                 | CONFIG_PREALLOC_MQ_IRQ_MSGS   |                  |
+                 +-------------------------------+                  +
|                 | CONFIG_MQ_MAXMSGSIZE          |                  |
+-----------------+-------------------------------+------------------+

.. _arch/Kconfig: https://github.com/apache/nuttx/blob/master/arch/Kconfig
.. _sched/Kconfig: https://github.com/apache/nuttx/blob/master/sched/Kconfig
.. _mm/Kconfig: https://github.com/apache/nuttx/blob/master/mm/Kconfig
.. _serial/Kconfig: https://github.com/apache/nuttx/blob/master/drivers/serial/Kconfig
