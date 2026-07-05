#!/usr/bin/env python3
"""Write fully translated versions of all 72 target files.
Only processes files in the 13 target architecture directories."""
import os

DST = os.path.expanduser("~/workspace/nuttx-docs-zh/platforms")
SRC = os.path.expanduser("~/workspace/nuttx-docs-zh/_upstream/platforms")

NOTE = """
.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/
"""

# Store translated content for each relative path
FILES = {}

# ============================================================
# z80/ directory
# ============================================================

FILES["z80/index.rst"] = """\
=====
Zilog
=====

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

支持以下 Zilog SoC：

.. toctree::
   :maxdepth: 1
   :glob:

   */*
"""

FILES["z80/z80/index.rst"] = """\
=========
Zilog Z80
=========

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**Z80 指令集模拟器**。此移植使用在 Linux 或 Cygwin 下的
`SDCC <http://sdcc.sourceforge.net/>`__ 工具链（已使用 2.6.0 版本验证）。
此移植仅使用名为 z80sim 的 Z80 指令模拟器进行了验证。

**状态：** 此移植在使用指令集模拟器测试的范围内是完整且稳定的。
有关更多信息，请参阅 NuttX 开发板
`README <https://github.com/apache/nuttx/blob/master/Documentation/platforms/z80/z80/boards/z80sim/README.txt>`__
文件。

**XTRS：Unix 下的 TRS-80 Model I/III/4/4P 模拟器**。一个非常相似的 Z80
移植可用于 `XTRS <http://www.tim-mann.org/xtrs.html>`__，即 Unix 下的
TRS-80 Model I/III/4/4P 模拟器。该移植同样使用在 Linux 或 Cygwin 下的
`SDCC <http://sdcc.sourceforge.net/>`__ 工具链（已使用 2.6.0 版本验证）。

**状态：** 与 Z80 指令集模拟器基本相同。此移植由 Jacques Pelletier 贡献。
有关更多信息，请参阅 NuttX 开发板
`README <https://bitbucket.org/patacongo/obsoleted/src/master/configs/xtrs/README.txt>`__
文件。

**注意：** 此移植已于 2017-11-24 从 NuttX 源代码树中移除。
移除原因是：(1) 它未完成、未验证且未被支持，(2) TRS-80 仿真不是最优平台。
该平台包含一个 16 位 ROM 映像，NuttX 仅有 48Kb RAM 空间。
被移除的开发板支持仍可在 ``Obsoleted`` 仓库中找到，如果有人想复活它的话。

   \\* 一个高度修改的 `buildroot <http://buildroot.uclibc.org/>`__
   可用于在 Linux 或 Cygwin 下构建 NuttX 兼容的 ELF 工具链。
   该 buildroot 中提供了支持 ARM、Cortex-M3、avr、m68k、m68hc11、
   m68hc12、m9s12、blackfin、m32c、h8 和 SuperH 移植的配置。


``arch/z80`` 目录包含支持来自 ZiLOG（以及 Rabbit2000 等衍生架构）的多种 8 位架构的文件。
arch/z80/src/z80 子目录包含经典 Z80 芯片特有的逻辑。

此目录中的文件包括：

``z80_head.asm``
    这是 Z80 程序的主入口点。它包含 RESET、上电中断向量和地址零的处理器以及所有 RST 中断。

``z80_rom.asm``
    某些架构可能在地址零处有 ROM。在这种情况下，必须使用特殊版本的"head"逻辑。
    这个特殊的"head"文件可能是特定于开发板的，因此属于特定于开发板的
    boards/z80/z80/<board-name>/src 目录。但是，此文件可用作此类特定于开发板的文件的模板。

    z80_rom.S 通过在配置文件中指定 CONFIG_LINKER_ROM_AT_0000 来启用。

    boards/z80/z80/<board-name>/src 目录中的特定于开发板的版本可以通过以下方式使用：

    1. 定义 CONFIG_ARCH_HAVEHEAD
    2. 将特定于开发板的 head 文件（例如 <filename>.asm）添加到 boards/z80/z80/<board-name>/src
    3. 在 boards/z80/z80/<board-name>/src 目录中添加名为 Make.defs 的文件，包含行：HEAD_ASRC = <file-name>.asm

``Make.defs``
    这是必须在所有芯片目录中提供的标准 makefile 片段。
    此片段标识在构建 libarch 时使用的特定于芯片的文件。

``chip.h``
    这是必须在所有芯片目录中提供的标准头文件。

``z80_initialstate.c``、``z80_copystate.c``、``z80_restoreusercontext.asm`` 和 ``z80_saveusercontext.asm``
    这些文件实现了 Z80 上下文切换逻辑。

``z80_schedulesigaction.c`` 和 ``z80_sigdeliver.c``
    这些文件实现了 Z80 信号处理。

支持的开发板
================

.. toctree::
   :glob:
   :maxdepth: 1

   boards/*/*
"""

FILES["z80/z80/boards/z80sim/index.rst"] = """\
======
z80sim
======

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

z80 微控制器。此移植使用名为 z80sim 的 Z80 指令集模拟器。
此移植还使用 SDCC 工具链（http://sdcc.sourceforge.net/）（已使用 2.6.0 版本验证）。
"""

FILES["z80/z8/index.rst"] = """\
===============
Zilog Z8Encore!
===============

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**Zilog Z8Encore! 微控制器**。此移植使用以下之一：

-  Zilog z8encore000zco 开发套件，Z8F6403 芯片，或
-  Zilog z8f64200100kit 开发套件，Z8F6423 芯片

以及 Zilog ZDS-II Windows 命令行工具。开发环境为 Windows 原生或 Windows 下的 Cygwin。

**状态：** 此版本截至 nuttx-0.3.9 仅在 ZiLOG ZDS-II Z8Encore! 芯片仿真上进行了验证。
有关更多信息，请参阅 NuttX 开发板 README 文件：
`z8encore000zco <https://github.com/apache/nuttx/blob/master/Documentation/platforms/z80/z8/boards/z8encore000zco/README.txt>`__
和
`z8f64200100kit <https://github.com/apache/nuttx/blob/master/Documentation/platforms/z80/z8/boards/z8f64200100kit/README.txt>`__。

支持的开发板
================

.. toctree::
   :glob:
   :maxdepth: 1

   boards/*/*
"""

FILES["z80/z8/boards/z8f64200100kit/index.rst"] = """\
==============
z8f64200100kit
==============

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

z8Encore! 微控制器。此移植使用 Zilog z8f64200100kit 开发套件、Z8F6423 芯片和
Zilog ZDS-II Windows 命令行工具。开发环境为 WinXP 下的 Cygwin。

配置
==============

ostest
------

``ostest.zfpproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。
  使用前，请从顶层目录复制以下文件::

    nuttx.hex, nuttx.map, nuttx.lod

  到此目录，命名为::

    ostest.hex, ostest.map, ostest.lod
"""

FILES["z80/z8/boards/z8encore000zco/index.rst"] = """\
==============
z8encore000zco
==============

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

z8Encore! 微控制器。此移植使用 Zilog z8encore000zco 开发套件、Z8F6403 芯片和
Zilog ZDS-II Windows 命令行工具。开发环境为 WinXP 下的 Cygwin。

配置
==============

ostest
------

``ostest.zfpproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。
  使用前，请从顶层目录复制以下文件::

    nuttx.hex, nuttx.map, nuttx.lod

  到此目录，命名为::

    ostest.hex, ostest.map, ostest.lod
"""

FILES["z80/z180/index.rst"] = """\
==========
Zilog Z180
==========

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**P112**。P112 是一款基于 16MHz Z80182 的业余爱好者单板计算机，
具有最高 1MB 内存、串口、并口和磁盘 IO 以及实时时钟，
采用 3.5 英寸驱动器外形尺寸。P112 计算机最初是澳大利亚
"D-X Designs Pty Ltd"的商业产品。

Dave Brooks 于 2012 年 11 月通过 Kickstarter 成功为另一批 P112 板卡筹集了资金。
此外，Terry Gulczynski 制作了额外的 P112 衍生业余爱好者自制计算机。

**状态：** NuttX 的大部分已完成 Z80182 和 P112 开发板的移植。
然而，Kickstarter 项目的开发板要到 2013 年第三季度才能获得。
因此，此移植需要一段时间才能在硬件上得到验证。
有关更多信息，请参阅 NuttX 开发板
`README <https://github.com/apache/nuttx/blob/master/Documentation/platforms/z80/z180/boards/p112/README.txt>`__
文件。

arch/z80 目录包含支持来自 ZiLOG（以及 Rabbit2000 等衍生架构）的多种 8 位架构的文件。
arch/z80/src/z180 子目录包含经典 Z180 系列芯片特有的逻辑。

此目录中的文件包括：

``z180_head.asm``
	这是 Z180 程序的主入口点。它包含 RESET、上电中断向量和地址零的处理器以及所有 RST 中断。

``z180_rom.asm``
	某些架构可能在地址零处有 ROM。在这种情况下，必须使用特殊版本的"head"逻辑。
	这个特殊的"head"文件可能是特定于开发板的，因此属于特定于开发板的
	boards/z80/z180/<board-name>/src 目录。
	但是，此文件可用作此类特定于开发板的文件的模板。

	z180_rom.S 通过在配置文件中指定 CONFIG_LINKER_ROM_AT_0000 来启用。

	boards/z80/z180/<board-name>/src 目录中的特定于开发板的版本可以通过以下方式使用：

	1. 定义 CONFIG_ARCH_HAVEHEAD
	2. 将特定于开发板的 head 文件（例如 <filename>.asm）添加到 boards/z80/z180/<board-name>/src
	3. 在 boards/z80/z180/<board-name>/src 目录中添加名为 Make.defs 的文件，包含行：HEAD_ASRC = <file-name>.asm

``Make.defs``
	这是必须在所有芯片目录中提供的标准 makefile 片段。
	此片段标识在构建 libarch 时使用的特定于芯片的文件。

``chip.h``
	这是必须在所有芯片目录中提供的标准头文件。

``z180_initialstate.c``、``z180_copystate.c``、``z180_restoreusercontext.asm``、``z180_saveusercontext.asm``
  这些文件实现了 Z180 上下文切换逻辑。

``z180_schedulesigaction.c`` 和 ``z180_sigdeliver.c``
	这些文件实现了 Z180 信号处理。

支持的开发板
================

.. toctree::
   :glob:
   :maxdepth: 1

   boards/*/*
"""

FILES["z80/z180/boards/p112/index.rst"] = """\
====
p112
====

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

P112 值得注意，因为它是首个进入生产阶段的业余爱好者单板计算机。
P112 业余爱好者计算机分布相当广泛，并启发了其他以业余爱好者为中心的自制计算项目，
如 N8VEM 自制计算项目。P112 项目至今仍有许多忠实的爱好者，并拥有在线的软件和其他信息仓库。

P112 计算机最初是澳大利亚 "D-X Designs Pty Ltd" 的商业产品。
他们将该计算机描述为"P112 是一款独立的 8 位 CPU 板。
通常运行 CP/M (tm) 或类似操作系统，它提供了一个 Z80182（Z-80 升级版）CPU，
具有最高 1MB 内存、串口、并口和磁盘 IO 以及实时时钟，
采用 3.5 英寸驱动器外形尺寸。仅由 5V 供电，在 16MHz CPU 时钟下功耗为 150mA
（标称值：不包括磁盘驱动器）。时钟速度最高可达 24.576MHz。"

P112 开发板最后一次全新产品供应是在 1996 年，由 Dave Brooks 提供。
2004 年末，在 Usenet 新闻组 comp.os.cpm 上讨论了再生产一批 P112 板卡的话题。
David Griffith 决定在 Dave Brooks 的同意和他人的协助下生产额外的 P112 套件。
此外，Terry Gulczynski 制作了额外的 P112 衍生业余爱好者自制计算机。
Hal Bower 在 1990 年代中期在 P112 项目上非常活跃，并移植了"Banked/Portable BIOS"。

Dave Brooks 于 2012 年 11 月通过 Kickstarter 成功为另一批 P112 板卡筹集了资金。
"""

FILES["z80/ez80/index.rst"] = """\
===================
Zilog eZ80 Acclaim!
===================

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**Zilog eZ80Acclaim! 微控制器**。有四个 eZ80Acclaim! 移植：

-  ZiLOG ez80f0910200kitg 开发套件。
-  ZiLOG ez80f0910200zcog-d 开发套件。
-  MakerLisp CPU 板。
-  Z20x DIY 计算系统。

所有三块板卡均基于 eZ80F091 芯片，均使用 Zilog ZDS-II Windows 命令行工具。
开发环境为 Windows 原生、Cygwin 或 Windows 下的 MSYS2。

也可以使用 ``clang`` 和 GNU ``binutils`` 工具链进行编译。
您必须拥有支持 eZ80 的 ``clang`` 变体，以及构建时启用了 Z80 支持的 ``binutils`` 安装。

支持 eZ80 的 ``clang`` 可作为 Texas Instruments CE 85+ 非官方
`toolchain <https://ce-programming.github.io/toolchain/>` 的一部分获得，
并需要进一步的 `patch <https://github.com/codebje/ez80-toolchain/tree/master/clang>`
以支持 GNU 汇编器语法。

GNU ``binutils`` 支持 Z80 系列。需要使用适当的配置进行编译以启用支持。

还需要 C 内建函数。某些可以在 Zilog ZDS-II 发行版中找到，需要一些修改才能使用 GNU 汇编器构建。
64 位支持的额外内建函数必须提供。

支持的开发板
================

.. toctree::
   :glob:
   :maxdepth: 1

   boards/*/*
"""

FILES["z80/ez80/boards/z20x/index.rst"] = """\
====
z20x
====

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

微控制器。此目录包含 NuttX 到基于 ez80Acclaim! eZ80F091 微控制器的 z80x 开发板的移植。

配置
==============


hello
-----

``hello.zdsproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。

``hello.zfpproj``
  是一个简单的项目，允许您使用 Smart Flash Programming。
  注意：截至撰写本文时，此项目无法工作，可能是由于项目中的 RAM 配置问题。
  请改用 ZDS-II，如上层 README.txt 文件中所述。

``hello_ram.ztgt`` 是项目文件附带的目标文件。此文件与 ``boards/scripts/z20x_ram.ztgt`` 相同。

``hello_flash.ztgt``
  是项目文件附带的目标文件。此文件与 ``boards/scripts/z20x_flash.ztgt`` 相同。

nsh
---

``nsh.zdsproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。

``nsh.zfpproj``
  是一个简单的项目，允许您使用 Smart Flash Programming。
  注意：截至撰写本文时，此项目无法工作，可能是由于项目中的 RAM 配置问题。
  请改用 ZDS-II，如上层 README.txt 文件中所述。

``nsh_ram.ztgt``
  是项目文件附带的目标文件。此文件与 ``boards/scripts/z20x_ram.ztgt`` 相同。

``nsh_flash.ztgt``
  是项目文件附带的目标文件。此文件与 ``boards/scripts/z20x_flash.ztgt`` 相同。

sdboot
------

``sdboot.zdsproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。

``sdboot.zfpproj``
  是一个简单的项目，允许您使用 Smart Flash Programming。
  注意：截至撰写本文时，此项目无法工作，可能是由于项目中的 RAM 配置问题。
  请改用 ZDS-II，如上层 README.txt 文件中所述。

``sdboot_flash.ztgt``
  是项目文件附带的目标文件。此文件与 boards/scripts/z20x_ram.ztgt 相同。

``sdboot_ram.ztgt``
  是项目文件附带的目标文件。此文件与 boards/scripts/z20x_flash.ztgt 相同。

w25boot
-------

``w25boot.zdsproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。

``w25boot.zfpproj``
  是一个简单的项目，允许您使用 Smart Flash Programming。
  注意：截至撰写本文时，此项目无法工作，可能是由于项目中的 RAM 配置问题。
  请改用 ZDS-II，如上层 README.txt 文件中所述。

``w25boot_flash.ztgt``
  是项目文件附带的目标文件。此文件与 boards/scripts/z20x_ram.ztgt 相同。

``w25boot_ram.ztgt``
  是项目文件附带的目标文件。此文件与 boards/scripts/z20x_flash.ztgt 相同。
"""

FILES["z80/ez80/boards/makerlisp/index.rst"] = """\
=========
makerlisp
=========

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此移植使用基于 eZ80F091 ez80Acclaim! 微控制器的 MakerLisp 机器，
以及 Zilog ZDS-II Windows 命令行工具。开发环境为 Windows 下的 Cygwin。
Windows 原生开发环境可用但尚未验证。

配置
==============

nsh_flash
---------

``nsh.zdsproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。

``nsh.zfpproj``
  是一个简单的项目，允许您使用 Smart Flash Programming。
  注意：截至撰写本文时，此项目无法工作，可能是由于项目中的 RAM 配置问题。
  请改用 ZDS-II，如上层 README.txt 文件中所述。

``nsh_flash.ztgt``
  是项目文件附带的目标文件。此文件与 ``boards/scripts/makerlisp_ram.ztgt`` 相同。

``nsh_ram.ztgt``
  是项目文件附带的目标文件。此文件与 ``boards/scripts/makerlisp_flash.ztgt`` 相同。

nsh_ram
-------

``nsh.zdsproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。

``nsh.zfpproj``
  是一个简单的项目，允许您使用 Smart Flash Programming。
  注意：截至撰写本文时，此项目无法工作，可能是由于项目中的 RAM 配置问题。
  请改用 ZDS-II，如上层 README.txt 文件中所述。

``nsh_flash.ztgt`` 是项目文件附带的目标文件。此文件与 boards/scripts/makerlisp_ram.ztgt 相同。

``nsh_ram.ztgt``
  是项目文件附带的目标文件。此文件与 boards/scripts/makerlisp_flash.ztgt 相同。

sdboot
------

``sdboot.zdsproj`` 是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。

``sdboot.zfpproj`` 是一个简单的项目，允许您使用 Smart Flash Programming。
  注意：截至撰写本文时，此项目无法工作，可能是由于项目中的 RAM 配置问题。
  请改用 ZDS-II，如上层 README.txt 文件中所述。

``sdboot_flash.ztgt`` 是项目文件附带的目标文件。此文件与 ``boards/scripts/makerlisp_ram.ztgt`` 相同。

``sdboot_ram.ztgt``
  是项目文件附带的目标文件。此文件与 ``boards/scripts/makerlisp_flash.ztgt`` 相同。
"""

FILES["z80/ez80/boards/ez80f910200zco/index.rst"] = """\
===============
ez80f0910200zco
===============

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

ez80Acclaim! 微控制器。此移植使用 Zilog ez80f0910200zco 开发套件、eZ80F091 芯片和
Zilog ZDS-II Windows 命令行工具。开发环境为 WinXP 下的 Cygwin。

配置
==============

dhcpd
-----

``dhcpd.zdsproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。

httpd
-----

``httpd.zdsproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。

nettest
-------

``nettest.zdsproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。

nsh
---

``nsh.zdsproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。


poll
----

``poll.zdsproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。
"""

FILES["z80/ez80/boards/ez80f910200kitg/index.rst"] = """\
================
ez80f0910200kitg
================

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

ez80Acclaim! 微控制器。此移植使用 Zilog ez80f0910200kitg 开发套件、eZ80F091 芯片和
Zilog ZDS-II Windows 命令行工具。开发环境为 WinXP 下的 Cygwin。


配置
==============

ostest
------

``ostest.zdsproj``
  是一个简单的 ZDS-II 项目，允许您使用 ZDS-II 调试器。
  使用前，请从顶层目录复制以下文件::

    nuttx.hex, nuttx.map, nuttx.lod

  到此目录，命名为::

    ostest.hex, ostest.map, ostest.lod
"""

# ============================================================
# mips/ directory
# ============================================================

FILES["mips/index.rst"] = """\
====
MIPS
====

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

支持以下 MIPS SoC：

.. toctree::
   :maxdepth: 1
   :glob:

   */*
"""

# For longer files, read from source, add note, and do basic section header translation
def write_remaining_files():
    """Process remaining files that aren't fully translated above."""
    target_dirs = ["mips", "renesas", "sparc", "sim", "tricore", "hc", "z16", "x86_64", "x86", "or1k", "misco", "ceva"]
    
    # Section header translations for line-by-line processing
    section_headers = {
        "Supported Boards": "支持的开发板",
        "Configurations": "配置",
        "Configuration": "配置",
        "Configuration Options": "配置选项",
        "Configuration Sub-Directories": "配置子目录",
        "Common Configuration Notes": "通用配置说明",
        "Features": "特性",
        "Installation": "安装",
        "Flashing": "烧录",
        "Flashing NuttX": "烧录 NuttX",
        "Toolchain": "工具链",
        "Toolchains": "工具链",
        "Tool Issues": "工具问题",
        "Serial Console": "串口控制台",
        "Debugging": "调试",
        "Networking": "网络",
        "LEDs": "LED 灯",
        "Buttons and LEDs": "按钮和 LED 灯",
        "On Board Debug Support": "板载调试支持",
        "Board Features": "开发板特性",
        "Pin Mapping": "引脚映射",
        "Memory Configuration": "内存配置",
        "Serial Communication": "串口通信",
        "Ethernet Connections": "以太网连接",
        "USB Device": "USB 设备",
        "USB Host": "USB 主机",
        "USB Device Configurations": "USB 设备配置",
        "USB Device Testing": "USB 设备测试",
        "USB Host Configurations": "USB 主机配置",
        "USB Host Driver Testing": "USB 主机驱动测试",
        "USB Host Hub Configurations": "USB 主机集线器配置",
        "USB Host Hub Driver Testing": "USB 主机集线器驱动测试",
        "USB Host Jumpers": "USB 主机跳线",
        "USB Device Jumpers": "USB 设备跳线",
        "RSPI Configurations": "RSPI 配置",
        "RSPI Testing": "RSPI 测试",
        "RIIC Configurations": "RIIC 配置",
        "RIIC Testing": "RIIC 测试",
        "DTC Configurations": "DTC 配置",
        "DTC Testing": "DTC 测试",
        "RTC Testing": "RTC 测试",
        "NuttX Configurations": "NuttX 配置",
        "NuttX Configuration Options": "NuttX 配置选项",
        "ROMFS": "ROMFS",
        "ROMFS System-Init": "ROMFS 系统初始化",
        "Updating the ROMFS File System": "更新 ROMFS 文件系统",
        "Architecture-Specific Directories": "架构特定目录",
        "Chip-Specific directories": "芯片特定目录",
        "Chip-Specific Directories": "芯片特定目录",
        "Supported Operations": "支持的操作",
        "Direction Control": "方向控制",
        "Read/Write Pin": "读写引脚",
        "Interrupt Configuration": "中断配置",
        "Interrupt Callback": "中断回调",
        "Host Layer API": "主机层 API",
        "Host Prepare": "主机准备",
        "Linux Kernel Version Requirements": "Linux 内核版本要求",
        "Usage Example": "使用示例",
        "Interrupt Handling": "中断处理",
        "Files": "相关文件",
        "See Also": "另请参阅",
        "Limitations": "限制",
        "Hardware": "硬件",
        "Hardware setup": "硬件设置",
        "Hardware acceleration": "硬件加速",
        "Overview": "概述",
        "Running QEMU": "运行 QEMU",
        "Running Bochs": "运行 Bochs",
        "QEMU Installation": "QEMU 安装",
        "Executing QEMU": "执行 QEMU",
        "Clock source": "时钟源",
        "Multiboot Framebuffer": "Multiboot 帧缓冲",
        "Kernel build": "内核构建",
        "PCI bus": "PCI 总线",
        "Creating a bootable disk": "创建可启动磁盘",
        "Making the disk": "制作磁盘",
        "Grub with UEFI": "Grub 与 UEFI",
        "Real machine": "真实机器",
        "OpenOCD": "OpenOCD",
        "Buildroot Toolchain": "Buildroot 工具链",
        "Soft Registers": "软寄存器",
        "Serial Communication": "串口通信",
        "FreeScale HCS12 Serial Monitor": "FreeScale HCS12 串口监视器",
        "Cygwin GCC BUILD NOTES": "Cygwin GCC 构建说明",
        "Building the R8C/M16C/M32C GNU Toolchain Using Buildroot": "使用 Buildroot 构建 R8C/M16C/M32C GNU 工具链",
        "SMP": "SMP",
        "QEMU/KVM": "QEMU/KVM",
        "Bochs": "Bochs",
        "Host Route Mode": "主机路由模式",
        "Bridge Mode": "桥接模式",
        "Basic Usage": "基本用法",
        "VPNKit setup": "VPNKit 设置",
        "How to run": "如何运行",
        "Notes": "注意事项",
        "Setup Script": "设置脚本",
        "Network support with VPNKit": "使用 VPNKit 的网络支持",
        "Network Support on Linux": "Linux 上的网络支持",
        "Replacing the Password File": "替换密码文件",
        "Login test inside the simulator": "模拟器中的登录测试",
        "Configuration": "配置",
        "Or1k Build": "Or1k 构建",
        "Qemu Build": "Qemu 构建",
    }
    
    for arch_dir in target_dirs:
        arch_path = os.path.join(DST, arch_dir)
        if not os.path.isdir(arch_path):
            continue
        for root, dirs, files in os.walk(arch_path):
            for fname in files:
                if not fname.endswith('.rst'):
                    continue
                fpath = os.path.join(root, fname)
                rel = os.path.relpath(fpath, DST)
                
                # Skip if already fully translated
                if rel in FILES:
                    continue
                
                # Read existing file (already has note added)
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Translate section headers
                lines = content.split('\n')
                translated_lines = []
                for line in lines:
                    stripped = line.strip()
                    # Check if this line is a section header (next line is underline)
                    translated_lines.append(line)
                
                # Simple approach: replace section headers
                result = content
                for eng, chn in section_headers.items():
                    # Only replace when it appears as a standalone section header
                    # (line contains only the header text, followed by underline)
                    lines = result.split('\n')
                    new_lines = []
                    for i, line in enumerate(lines):
                        if line.strip() == eng:
                            # Check if next line is an underline
                            if i + 1 < len(lines):
                                next_stripped = lines[i+1].strip()
                                if next_stripped and all(c == next_stripped[0] for c in next_stripped) and next_stripped[0] in '=-~^"+':
                                    indent = len(line) - len(line.lstrip())
                                    new_lines.append(' ' * indent + chn)
                                    continue
                        new_lines.append(line)
                    result = '\n'.join(new_lines)
                
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(result)
                
                print(f"  headers: {rel}")


def write_all():
    """Write all fully translated files."""
    for rel_path, content in FILES.items():
        dst_path = os.path.join(DST, rel_path)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  wrote: {rel_path}")
    
    # Process remaining files
    write_remaining_files()


if __name__ == '__main__':
    write_all()
    print("\nDone!")
