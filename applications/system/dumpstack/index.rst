========================================
``dumpstack`` 任务调用栈回溯
========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

描述
-----------

``dumpstack`` 应用程序是一个调试工具，用于显示 NuttX 系统中一个或多个任务（线程）
的调用栈回溯信息。它帮助开发者理解任务的执行路径和函数调用层次结构，这对于调试
崩溃、死锁或异常行为特别有用。

该应用程序利用 NuttX 内核中的 ``sched_dumpstack()`` 函数来检索和显示回溯信息。
根据配置，回溯可以显示原始内存地址或符号化的函数名。

特性
--------

* 按 PID 转储单个任务的回溯
* 按 PID 范围转储多个任务的回溯
* 支持符号化回溯显示（需要 ``CONFIG_ALLSYMS``）

用法
-----

基本语法
^^^^^^^^^^^^

.. code-block:: bash

   dumpstack [start_pid] [end_pid]

**无参数** – 转储当前任务的回溯：

.. code-block:: bash

   nsh> dumpstack

**单个 PID** – 转储特定任务的回溯：

.. code-block:: bash

   nsh> dumpstack 5

**PID 范围** – 转储从 start_pid 到 end_pid（包含）的所有任务的回溯：

.. code-block:: bash

   nsh> dumpstack 3 10

示例
^^^^^^^^

1. **转储 PID 4 到 6 的任务回溯（未启用 CONFIG_ALLSYMS）：**

   .. code-block:: bash

      nsh> dumpstack 4 6
      sched_dumpstack: backtrace| 4: 0x0000000010024fe8 0x000000001000cccc 0x000000001002504c 0x000000001002759c 0x000000001002a870
      sched_dumpstack: backtrace| 5: 0x0000000010024fe8 0x000000001000cccc 0x000000001002504c 0x000000001002759c 0x000000001002a870
      sched_dumpstack: backtrace| 6: 0x000000001002bbb4 0x000000001002bd70 0x00000000100d3890 0x00000000100d3908 0x000000001005193c 0x000000001004fc74 0x0000000010051514 0x000000001005160c
      sched_dumpstack: backtrace| 6: 0x0000000010051870 0x0000000010047fa8 0x000000001002cd50 0x000000001003d5ec 0x000000001002a888

2. **转储 PID 4 的任务回溯（启用 CONFIG_ALLSYMS）：**

   .. code-block:: bash

      nsh> dumpstack 4
      sched_dumpstack: backtrace:
      sched_dumpstack: [ 4] [<0x10025174>] nxsem_wait_slow+0x158/0x1ac
      sched_dumpstack: [ 4] [<0x1000cccc>] nxsem_wait+0x94/0xb0
      sched_dumpstack: [ 4] [<0x100251d8>] nxsem_wait_uninterruptible+0x10/0x2c
      sched_dumpstack: [ 4] [<0x10027728>] work_thread+0x1b4/0x238
      sched_dumpstack: [ 4] [<0x1002a9fc>] nxtask_start+0x7c/0xa4

配置
-------------

**CONFIG_SYSTEM_DUMPSTACK**

依赖
^^^^^^^^^^^^

dumpstack 应用程序需要以下内核配置：

* **CONFIG_SCHED_BACKTRACE** – 必须启用以提供 ``sched_backtrace()`` 函数
* **CONFIG_ALLSYMS** – 可选，启用回溯输出中的符号化函数名

限制
-----------

* 每次迭代的最大回溯深度为 16 帧
* 某些架构可能有有限的或没有回溯支持（已知问题：sim 环境无法查看其他线程的栈）
