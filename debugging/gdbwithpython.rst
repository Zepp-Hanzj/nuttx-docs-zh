===============
使用 Python 的 GDB
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

简介
============

可以使用 GDB 的 Python 扩展有效地调试 NuttX 内核。常用的类和工具在 ``nuttx/tools/gdb/nuttxgdb`` 目录中实现。用户还可以创建自定义 Python 脚本以满足其调试需求，更高效地分析和排查 NuttX 内核问题。

用法
=====

1. 编译 NuttX 时启用 CONFIG_DEBUG_SYMBOLS=y 并将 ``CONFIG_DEBUG_SYMBOLS_LEVEL`` 改为 ``-g3``。
2. 使用 GDB 调试 NuttX ELF 二进制文件（在真实设备、模拟器或使用 coredump）。
3. 将以下参数添加到 GDB 命令行：``-ix="nuttx/tools/pynuttx/gdbinit.py"``
4. GDB 将自动加载 Python 脚本，从而启用自定义命令。

如何编写 GDB Python 脚本
================================

这是一篇介绍 GDB 中 Python 基本原理的文章。阅读它以获得基本理解。
`Automate Debugging with GDB Python API <https://interrupt.memfault.com/blog/automate-debugging-with-gdb-python-api>`_。

有关 gdb python 的更多文档，请参阅 GDB 的官方文档。
`GDB Python API <https://sourceware.org/gdb/current/onlinedocs/gdb.html/Python-API.html#Python-API>`_。

要求
============

要使用带有 Python 的 GDB，必须满足以下要求：

- 使用编译时带有 Python 支持的 GDB，Python 3.8 或更高版本
- 安装所需的 Python 包：``pip install -r tools/pynuttx/requirements.txt``
- 以调试级别 3 编译 NuttX：``CONFIG_DEBUG_SYMBOLS_LEVEL="-g3"``

.. Warning::
   GDB Python API 并非在所有版本的 GDB 中都可用。请确保使用支持 Python 的版本。

.. Warning::
   NuttX 必须使用 ``CONFIG_DEBUG_SYMBOLS=y`` 和 ``CONFIG_DEBUG_SYMBOLS_LEVEL="-g3"`` 编译才能使用带有 Python 的 GDB。

.. toctree::
   :caption: GDB 插件命令
   :maxdepth: 1

   gdb/irqinfo.rst
