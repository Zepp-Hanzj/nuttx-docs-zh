=========================================
``whetstone`` Whetstone FPU 基准测试
=========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
========

Whetstone 是一个经典的合成基准测试程序，旨在评估处理器算术性能。
通过执行一系列标准化的计算任务，它提供了对浮点和整数运算能力的精确评估。

此实现是双精度 Whetstone 基准测试的 C 语言转换版本，
基于 Rich Painter（Painter Engineering, Inc.）从 netlib.org 版本的工作。

测试结果帮助开发者：

- 量化 FPU（浮点单元）性能
- 分析编译器优化级别（-O2、-O3 等）对代码执行效率的影响
- 比较不同硬件平台或系统配置下的算术性能

配置
=============

在运行测试之前，启用以下 Kconfig 选项：

.. code-block:: bash

   # 启用自定义宽松许可证组件
   CONFIG_ALLOW_CUSTOM_PERMISSIVE_COMPONENTS=y

   # 启用 Whetstone 基准测试
   CONFIG_BENCHMARK_WHETSTONE=y

   # Whetstone 需要 C 库中的浮点支持
   CONFIG_LIBC_FLOATINGPOINT=y

其他配置选项：

- ``CONFIG_BENCHMARK_WHETSTONE_PROGNAME`` - 程序名称（默认："whetstone"）
- ``CONFIG_BENCHMARK_WHETSTONE_PRIORITY`` - 任务优先级（默认：100）
- ``CONFIG_BENCHMARK_WHETSTONE_STACKSIZE`` - 栈大小（默认：DEFAULT_TASK_STACKSIZE）

用法
=====

命令语法
--------------

.. code-block:: bash

   whetstone [-c] [loops]

参数
----------

- ``[loops]`` - 模块循环次数。设置每个内部测试模块的迭代次数。
  增加此值会显著增加计算和执行时间。默认：1000
- ``-c`` - 连续模式。指定时，基准测试将无限重复直到被中断。默认：禁用

示例
--------

使用默认参数（1000 次循环）运行标准测试：

.. code-block:: bash

   nsh> whetstone

增加每个模块的计算负载（100000 次循环）：

.. code-block:: bash

   nsh> whetstone 100000

使用自定义循环次数运行连续模式：

.. code-block:: bash

   nsh> whetstone -c 100000

输出解读
=====================

完成后，whetstone 输出测试配置、总持续时间和最终性能分数。

示例输出
--------------

.. code-block:: bash

   nsh> whetstone 100000

   Loops: 100000, Iterations: 1, Duration: 5765 millisecond.
   C Converted Double Precision Whetstones: 1.7 MIPS

- **Loops: 100000** - 每个模块执行了 100,000 次循环迭代
- **Iterations: 1** - 测试套件运行了 1 轮
- **Duration: 5765 millisecond** - 总执行时间
- **1.7 MIPS** - 最终性能分数

性能指标
-------------------

**MIPS / KIPS**

- **定义**：Whetstone 性能单位 - MIPS（每秒百万 Whetstone 指令）和 KIPS（每秒千 Whetstone 指令）
- **计算**：``KIPS = (100.0 * loops * iterations) / (duration_sec * 1000)``
- **解读**：分数越高表示处理器算术性能越好
- **单位转换**：低于 1000 时结果以 KIPS 显示，否则以 MIPS 显示

测试模块
============

Whetstone 基准测试由 11 个精心设计的计算模块组成，涵盖不同的运算类型：

.. list-table::
   :header-rows: 1

   * - 模块
     - 描述
   * - 模块 1
     - 简单标识符 - 基本浮点运算
   * - 模块 2
     - 数组元素 - 基于数组的浮点运算
   * - 模块 3
     - 数组作为参数 - 使用数组参数的过程调用
   * - 模块 4
     - 条件跳转 - 分支操作
   * - 模块 5
     - （已省略）
   * - 模块 6
     - 整数算术 - 复杂整数运算
   * - 模块 7
     - 三角函数 - sin、cos、atan 计算
   * - 模块 8
     - 过程调用 - 函数调用开销
   * - 模块 9
     - 数组引用 - 数组索引操作
   * - 模块 10
     - 整数算术 - 简单整数运算
   * - 模块 11
     - 标准函数 - 链式数学函数（sqrt、exp、log）

注意事项
============

- 此基准测试使用双精度浮点算术
- 为获得准确的测量结果，确保系统不在高负载下
- 如果报告"持续时间不足"，请增加循环次数
- 时间精度为毫秒，即使在高性能嵌入式 CPU 上使用较少的循环迭代也能获得快速准确的结果

参考文献
==========

- 原始 Whetstone 基准测试：H.J. Curnow 和 B.A. Wichmann，
  "A Synthetic Benchmark", The Computer Journal, Vol 19, No 1,
  February 1976, pp. 43-49
- netlib.org Whetstone: https://www.netlib.org/benchmark/whetstone.c
