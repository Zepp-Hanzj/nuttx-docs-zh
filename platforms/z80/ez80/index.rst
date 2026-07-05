===================
Zilog eZ80 Acclaim!
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**Zilog eZ80Acclaim! 微控制器**。有四个 eZ80Acclaim! 移植：
ports:

-  The ZiLOG ez80f0910200kitg development kit.
-  The ZiLOG ez80f0910200zcog-d development kit.
-  The MakerLisp CPU board.
-  The Z20x DIY computing system.

所有开发板均基于 eZ80F091 芯片，均使用 Zilog
ZDS-II Windows 命令行工具。开发环境为
Windows 原生、Cygwin 或 Windows 下的 MSYS2。

也可以使用 ``clang`` 和 GNU ``binutils`` 工具链进行编译。
你必须拥有支持 eZ80 的 ``clang`` 变体，
以及构建时启用了 Z80 支持的 ``binutils`` 安装。

``clang`` with eZ80 support is available as part of the Texas Instruments
CE 85+ unofficial `toolchain <https://ce-programming.github.io/toolchain/>`
and requires a further `patch <https://github.com/codebje/ez80-toolchain/tree/master/clang>`
to support GNU assembler syntax.

GNU ``binutils`` 支持 Z80 系列。需要使用适当的配置进行编译
以启用支持。

还需要 C 内联函数。部分可在 Zilog ZDS-II
发行版中找到，需要进行一些修改才能使用 GNU 汇编器构建。
还必须提供用于 64 位支持的额外内联函数。

支持的开发板
======

.. toctree::
   :glob:
   :maxdepth: 1

   boards/*/*
