================================================
``mquickjs`` MicroQuickJS JavaScript 解释器
================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 `MicroQuickJS <https://github.com/bellard/mquickjs>`_ 的移植版本，
MicroQuickJS 是由 Fabrice Bellard 创建的轻量级 JavaScript 解释器。
MicroQuickJS 专为资源受限的嵌入式系统设计，在提供 JavaScript 语言支持的同时
保持最小的内存占用。

严格模式
===========

MQuickJS 在**更严格的模式**下运行，某些容易出错或低效的 JavaScript 功能被禁用。
主要限制包括：

- 仅支持严格模式构造（不支持 ``with`` 关键字，全局变量必须使用 ``var``）
- 数组不能有空洞；越界数组写入（数组末尾除外）会抛出 TypeError
- 仅支持全局 ``eval``；间接 eval 不能访问局部变量
- 不支持值装箱（例如，不支持 ``new Number(1)``）

配置选项
=====================

``CONFIG_INTERPRETERS_MQJS``
  启用 MicroQuickJS JavaScript 解释器（默认：n）

``CONFIG_INTERPRETERS_MQJS_PRIORITY``
  解释器的任务优先级（默认：100）

``CONFIG_INTERPRETERS_MQJS_STACKSIZE``
  解释器的栈大小，以字节为单位（默认：8192）

用法
=====

``mqjs`` 命令在 NSH 中可用，具有以下选项::

  mqjs [options] [file [args]]

  Options:
    -h, --help           列出选项
    -e, --eval EXPR      求值表达式
    -i, --interactive    进入交互模式
    -I, --include file   包含额外文件
    -d, --dump           转储内存使用统计
    --memory-limit n     将内存使用限制为 n 字节
    --no-column          调试信息中不包含列号
    -o FILE              将字节码保存到 FILE
    -m32                 强制 32 位字节码输出
    -b, --allow-bytecode 允许输入文件中的字节码

示例：

- 执行脚本：``mqjs script.js``
- 交互式 REPL：``mqjs -i``
- 带内存限制运行：``mqjs --memory-limit 10k script.js``
- 求值表达式：``mqjs -e 'print("Hello")'``

.. warning::
   **重要**：默认内存限制为 16 MB（``16 << 20`` 字节），这对于大多数嵌入式系统来说太大了。
   在 NuttX 上运行 mquickjs 时**务必设置内存限制**，通常使用
   ``--memory-limit 10k`` 或类似的小值。例如::

     nsh> mqjs --memory-limit 10k script.js

   如果没有内存限制，mquickjs 可能会耗尽系统内存并导致不稳定。

功能
========

- **JavaScript 子集**：实现了一个严格的 ES5 兼容 JavaScript 子集，具有更严格的模式，禁用容易出错或低效的构造
- **跟踪垃圾收集器**：用于较小对象的压缩 GC，减少内存碎片
- **基于 ROM 的标准库**：标准库驻留在 ROM 中，在编译时生成，可快速实例化
- **字节码编译**：可以编译为字节码并保存到持久存储（文件或 ROM），适用于嵌入式系统
