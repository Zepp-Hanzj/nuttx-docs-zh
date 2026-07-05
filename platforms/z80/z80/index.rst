=========
Zilog Z80
=========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**Z80 指令集模拟器**。此移植使用
`SDCC <http://sdcc.sourceforge.net/>`__ toolchain under Linux or Cygwin
(verified using version 2.6.0). This port has been verified using only a
名为 z80sim 的 Z80 指令模拟器进行验证。

**STATUS:** This port is complete and stable to the extent that it can
已完整且稳定。请参阅 NuttX 开发板
`README <https://github.com/apache/nuttx/blob/master/Documentation/platforms/z80/z80/boards/z80sim/README.txt>`__
file for further information.

**XTRS：Unix 下的 TRS-80 Model I/III/4/4P 模拟器**。一个非常相似的 Z80
移植可用于 `XTRS <http://www.tim-mann.org/xtrs.html>`__，即
Unix 下的 TRS-80 Model I/III/4/4P 模拟器。该移植也使用
`SDCC <http://sdcc.sourceforge.net/>`__ toolchain under Linux or Cygwin
(verified using version 2.6.0).

**STATUS:** Basically the same as for the Z80 instruction set simulator.
此移植由 Jacques Pelletier 贡献。请参阅 NuttX 开发板
`README <https://bitbucket.org/patacongo/obsoleted/src/master/configs/xtrs/README.txt>`__
file for further information.

**NOTE:** This port was removed from the NuttX source tree on
2017-11-24. It was removed because (1) it is unfinished, unverified, and
以及（2）TRS-80 模拟是一个次优平台。
该平台包含一个 16 位 ROM 映像，仅有 48Kb RAM 空间供 NuttX 使用。
被移除的开发板支持仍可在 ``Obsoleted``
仓库中找到，如果有人想要恢复它的话。

   \* A highly modified `buildroot <http://buildroot.uclibc.org/>`__ is
   available that may be used to build a NuttX-compatible ELF toolchain
   under Linux or Cygwin. Configurations are available in that buildroot
   to support ARM, Cortex-M3, avr, m68k, m68hc11, m68hc12, m9s12,
   blackfin, m32c, h8, and SuperH ports.


``arch/z80`` 目录包含支持多种 8 位架构的文件，
这些架构来自 ZiLOG（以及衍生架构如 Rabbit2000）。arch/z80/src/z80
子目录包含经典 Z80 芯片特有的逻辑。

此目录中的文件包括：

``z80_head.asm``
        这是 Z80 程序的主入口点。包括 RESET、上电中断向量和地址零
        以及所有 RST 中断的处理程序。
    RST interrupts.

``z80_rom.asm``
        部分架构可能在地址零处放置 ROM。在这种情况下，
        必须使用特殊的"head"逻辑版本。此特殊的"head"文件
        可能是特定于开发板的，因此属于特定于开发板的
        boards/z80/z80/<board-name>/src 目录。但此文件
        可以用作此类特定于开发板文件的模板。

        通过在配置文件中指定 CONFIG_LINKER_ROM_AT_0000 来启用 z80_rom.S。
    configuration file.

        boards/z80/z80/<board-name>/src 目录中的特定于开发板的版本可通过以下方式使用：
    can be used by:

    1. Define CONFIG_ARCH_HAVEHEAD
    2. Add the board-specific head file, say <filename>.asm, to
       boards/z80/z80/<board-name>/src
    3. Add a file called Make.defs in the boards/z80/z80/<board-name>/src
       directory containing the line:  HEAD_ASRC = <file-name>.asm

``Make.defs``
        这是必须在所有芯片目录中提供的标准 makefile 片段。
        此片段标识用于构建 libarch 的芯片特定文件。

``chip.h``
        这是必须在所有芯片目录中提供的标准头文件。
    directories.

``z80_initialstate.c``, ``z80_copystate.c``,  ``z80_restoreusercontext.asm``, and ``z80_saveusercontext.asm``
        这些文件实现了 Z80 上下文切换逻辑

``z80_schedulesigaction.c`` and  ``z80_sigdeliver.c``
        这些文件实现了 Z80 信号处理。

支持的开发板
======

.. toctree::
   :glob:
   :maxdepth: 1

   boards/*/*
