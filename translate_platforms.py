#!/usr/bin/env python3
"""Translate NuttX platform docs from English to Chinese (Simplified).
For each .rst file, preserves RST directives, cross-references, code blocks.
Translates only prose text. Keeps code, commands, paths, Kconfig in English.
"""

import os
import re

SRC = "/home/hanzj-mi/workspace/nuttx-docs-zh/_upstream/platforms"
DST = "/home/hanzj-mi/workspace/nuttx-docs-zh/platforms"

NOTE_AFTER_TITLE = (
    ".. note:: 本文档翻译自 NuttX 官方文档，"
    "如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/"
)

DIRS = ["z80", "mips", "renesas", "sparc", "sim", "tricore", "hc", "z16",
        "x86_64", "x86", "or1k", "misco", "ceva"]


def get_all_rst_files():
    files = []
    for d in DIRS:
        src_dir = os.path.join(SRC, d)
        if not os.path.exists(src_dir):
            continue
        for root, _, fnames in os.walk(src_dir):
            for f in fnames:
                if f.endswith('.rst'):
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, SRC)
                    files.append((full, rel))
    return sorted(files)


# ==================== Translation Maps ====================

# Per-file translations: key = relative path, value = list of (old, new) pairs
# applied line-by-line with full match
FILE_TRANSLATIONS = {}


def _ft(relpath, pairs):
    """Register per-file translation pairs."""
    FILE_TRANSLATIONS[relpath] = pairs


# ---- z80/index.rst ----
_ft("z80/index.rst", [
    ("The following Z80 SoC are supported:", "支持以下 Z80 SoC："),
])

# ---- z80/z80/index.rst ----
_ft("z80/z80/index.rst", [
    ("**Z80 Instruction Set Simulator**. This port uses the",
     "**Z80 指令集模拟器**。此移植使用"),
    ("Z80 instruction simulator called z80sim.",
     "名为 z80sim 的 Z80 指令模拟器进行验证。"),
    ("be tested using an instruction set simulator. Refer to the NuttX board",
     "已完整且稳定。请参阅 NuttX 开发板"),
    ("**XTRS: TRS-80 Model I/III/4/4P Emulator for Unix**. A very similar Z80",
     "**XTRS：Unix 下的 TRS-80 Model I/III/4/4P 模拟器**。一个非常相似的 Z80"),
    ("port is available for `XTRS <http://www.tim-mann.org/xtrs.html>`__, the",
     "移植可用于 `XTRS <http://www.tim-mann.org/xtrs.html>`__，即"),
    ("TRS-80 Model I/III/4/4P Emulator for Unix. That port also uses the",
     "Unix 下的 TRS-80 Model I/III/4/4P 模拟器。该移植也使用"),
    ("This port was contributed by Jacques Pelletier. Refer to the NuttX board",
     "此移植由 Jacques Pelletier 贡献。请参阅 NuttX 开发板"),
    ("unsupported, and (2) the TRS-80 simulation is a sub-optimal platform.i",
     "以及（2）TRS-80 模拟是一个次优平台。"),
    ("That platform includes a 16-bit ROM image and only a 48Kb RAM space for",
     "该平台包含一个 16 位 ROM 映像，仅有 48Kb RAM 空间供 NuttX 使用。"),
    ("NuttX. The removed board support is still available in the ``Obsoleted``",
     "被移除的开发板支持仍可在 ``Obsoleted``"),
    ("repository if anyone would ever like to resurrect it.",
     "仓库中找到，如果有人想要恢复它的话。"),
    ("The ``arch/z80`` directories contain files to support a variety of 8-bit architectures",
     "``arch/z80`` 目录包含支持多种 8 位架构的文件，"),
    ("from ZiLOG (and spin-architectures such as the Rabbit2000).  The arch/z80/src/z80",
     "这些架构来自 ZiLOG（以及衍生架构如 Rabbit2000）。arch/z80/src/z80"),
    ("sub-directory contains logic unique to the classic Z80 chip.",
     "子目录包含经典 Z80 芯片特有的逻辑。"),
    ("Files in this directory include:", "此目录中的文件包括："),
    ("    This is the main entry point into the Z80 program.  This includes the",
     "    这是 Z80 程序的主入口点。包括 RESET、上电中断向量和地址零"),
    ("    handler for the RESET, power-up interrupt vector and address zero and all",
     "    以及所有 RST 中断的处理程序。"),
    ("    Some architectures may have ROM located at address zero.  In this case, a",
     "    部分架构可能在地址零处放置 ROM。在这种情况下，"),
    ('    special version of the "head" logic must be used.  This special "head"',
     '    必须使用特殊的"head"逻辑版本。此特殊的"head"文件'),
    ("    file is probably board-specific and, hence, belongs in the board-specific",
     "    可能是特定于开发板的，因此属于特定于开发板的"),
    ("    boards/z80/z80/<board-name>/src directory.  This file may, however, be",
     "    boards/z80/z80/<board-name>/src 目录。但此文件"),
    ("    used as a model for such a board-specific file.",
     "    可以用作此类特定于开发板文件的模板。"),
    ("    z80_rom.S is enabled by specifying CONFIG_LINKER_ROM_AT_0000 in the",
     "    通过在配置文件中指定 CONFIG_LINKER_ROM_AT_0000 来启用 z80_rom.S。"),
    ("    A board specific version in the boards/z80/z80/<board-name>/src directory",
     "    boards/z80/z80/<board-name>/src 目录中的特定于开发板的版本可通过以下方式使用："),
    ("    can be used by", ""),
    ("    This is the standard makefile fragment that must be provided in all",
     "    这是必须在所有芯片目录中提供的标准 makefile 片段。"),
    ("    chip directories.  This fragment identifies the chip-specific file to",
     "    此片段标识用于构建 libarch 的芯片特定文件。"),
    ("    be used in building libarch.", ""),
    ("    This is the standard header file that must be provided in all chip",
     "    这是必须在所有芯片目录中提供的标准头文件。"),
    ("    These files implement the Z80 context switching logic",
     "    这些文件实现了 Z80 上下文切换逻辑"),
    ("    These files implement Z80 signal handling.",
     "    这些文件实现了 Z80 信号处理。"),
    ("Supported Boards", "支持的开发板"),
])

# ---- z80/z8/index.rst ----
_ft("z80/z8/index.rst", [
    ("**Zilog Z8Encore! Microcontroller**. This port uses the either:",
     "**Zilog Z8Encore! 微控制器**。此移植使用以下之一："),
    ("and the Zilog ZDS-II Windows command line tools. The development",
     "以及 Zilog ZDS-II Windows 命令行工具。开发环境"),
    ("environment is either Windows native or Cygwin under Windows.",
     "为 Windows 原生或 Windows 下的 Cygwin。"),
    ("Z8Encore! chip simulation as of nuttx-0.3.9. Refer to the NuttX board",
     "Z8Encore! 芯片仿真上进行了验证（截至 nuttx-0.3.9）。请参阅 NuttX 开发板"),
    ("Supported Boards", "支持的开发板"),
])

# ---- z80/z180/index.rst ----
_ft("z80/z180/index.rst", [
    ("**P112**. The P112 is a hobbyist single board computer based on a 16MHz",
     "**P112**。P112 是一款基于 16MHz Z80182 的爱好者单板计算机，"),
    ("Z80182 with up to 1MB of memory, serial, parallel and diskette IO, and",
     "配备高达 1MB 内存、串口、并口和磁盘 IO，"),
    ("realtime clock, in a 3.5-inch drive form factor. The P112 computer",
     "以及实时时钟，采用 3.5 英寸驱动器外形尺寸。P112 计算机"),
    ('originated as a commercial product of "D-X Designs Pty Ltd"[ of',
     '最初是澳大利亚 "D-X Designs Pty Ltd" 的商业产品。'),
    ("Dave Brooks was successfully funded through Kickstarter for and another",
     "Dave Brooks 于 2012 年 11 月通过 Kickstarter 成功众筹了"),
    ("run of P112 boards in November of 2012. In addition Terry Gulczynski",
     "又一批 P112 开发板。此外，Terry Gulczynski"),
    ("makes additional P112 derivative hobbyist home brew computers.",
     "还制作了额外的 P112 衍生爱好者自制计算机。"),
    ("P112 board. Boards from Kickstarter project will not be available,",
     "来自 Kickstarter 项目的开发板要到"),
    ("however, until the third quarter of 2013. So it will be some time before",
     "2013 年第三季度才会可用。因此还需要一些时间"),
    ("this port is verified on hardware. Refer to the NuttX board",
     "才能在硬件上验证此移植。请参阅 NuttX 开发板"),
    ("sub-directory contains logic unique to the classic Z180 family of chips.",
     "子目录包含经典 Z180 芯片系列特有的逻辑。"),
    ("Files in this directory include:", "此目录中的文件包括："),
    ("\tThis is the main entry point into the Z180 program.  This includes the",
     "\t这是 Z180 程序的主入口点。包括 RESET、上电中断向量和地址零"),
    ("\thandler for the RESET, power-up interrupt vector and address zero and all",
     "\t以及所有 RST 中断的处理程序。"),
    ("\tSome architectures may have ROM located at address zero.  In this case, a",
     "\t部分架构可能在地址零处放置 ROM。在这种情况下，"),
    ('\tspecial version of the "head" logic must be used.  This special "head"',
     '\t必须使用特殊的"head"逻辑版本。此特殊的"head"文件'),
    ("\tfile is probably board-specific and, hence, belongs in the board-specific",
     "\t可能是特定于开发板的，因此属于特定于开发板的"),
    ("\tboards/z80/z180/<board-name>/src directory.  This file may, however, be",
     "\tboards/z80/z180/<board-name>/src 目录。但此文件"),
    ("\tused as a model for such a board-specific file.",
     "\t可以用作此类特定于开发板文件的模板。"),
    ("\tz180_rom.S is enabled by specifying CONFIG_LINKER_ROM_AT_0000 in the",
     "\t通过在配置文件中指定 CONFIG_LINKER_ROM_AT_0000 来启用 z180_rom.S。"),
    ("\tA board specific version in the boards/z80/z180/<board-name>/src",
     "\tboards/z80/z180/<board-name>/src 目录中的特定于开发板的版本可通过以下方式使用："),
    ("\tdirectory can be used by", ""),
    ("\tThis is the standard makefile fragment that must be provided in all",
     "\t这是必须在所有芯片目录中提供的标准 makefile 片段。"),
    ("\tchip directories.  This fragment identifies the chip-specific file to",
     "\t此片段标识用于构建 libarch 的芯片特定文件。"),
    ("\tbe used in building libarch.", ""),
    ("\tThis is the standard header file that must be provided in all chip",
     "\t这是必须在所有芯片目录中提供的标准头文件。"),
    ("  These files implement the Z180 context switching logic",
     "  这些文件实现了 Z180 上下文切换逻辑"),
    ("\tThese files implement Z180 signal handling.",
     "\t这些文件实现了 Z180 信号处理。"),
    ("Supported Boards", "支持的开发板"),
])

# ---- z80/ez80/index.rst ----
_ft("z80/ez80/index.rst", [
    ("**Zilog eZ80Acclaim! Microcontroller**. There are four eZ80Acclaim!",
     "**Zilog eZ80Acclaim! 微控制器**。有四个 eZ80Acclaim! 移植："),
    ("All three boards are based on the eZ80F091 part and all use the Zilog",
     "所有开发板均基于 eZ80F091 芯片，均使用 Zilog"),
    ("ZDS-II Windows command line tools. The development environment is either",
     "ZDS-II Windows 命令行工具。开发环境为"),
    ("Windows native or Cygwin or MSYS2 under Windows.",
     "Windows 原生、Cygwin 或 Windows 下的 MSYS2。"),
    ("It is also possible to compile using ``clang`` and the GNU ``binutils``",
     "也可以使用 ``clang`` 和 GNU ``binutils`` 工具链进行编译。"),
    ("toolchain. You must have a variant of ``clang`` that supports the eZ80,",
     "你必须拥有支持 eZ80 的 ``clang`` 变体，"),
    ("and an install of ``binutils`` built with Z80 support.",
     "以及构建时启用了 Z80 支持的 ``binutils`` 安装。"),
    ("GNU ``binutils`` supports the Z80 family. It will require compilation with",
     "GNU ``binutils`` 支持 Z80 系列。需要使用适当的配置进行编译"),
    ("appropriate configuration to enable support.",
     "以启用支持。"),
    ("C intrinsics are also required. Some may be found in the Zilog ZDS-II",
     "还需要 C 内联函数。部分可在 Zilog ZDS-II"),
    ("distribution, requiring some modification to build with the GNU assembler.",
     "发行版中找到，需要进行一些修改才能使用 GNU 汇编器构建。"),
    ("Additional intrinsics for 64-bit support must be supplied.",
     "还必须提供用于 64 位支持的额外内联函数。"),
    ("Supported Boards", "支持的开发板"),
])

# ---- z80/ez80/boards/z20x/index.rst ----
_ft("z80/ez80/boards/z20x/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the z80x board",
     "微控制器。此目录包含将 NuttX 移植到 z80x 开发板的内容，"),
    ("based on an ez80Acclaim! eZ80F091 microcontroller.",
     "该开发板基于 ez80Acclaim! eZ80F091 微控制器。"),
    ("Configurations", "配置"),
    ("  is a simple ZDS-II project that will allow you to use the ZDS-II debugger.",
     "  是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。"),
    ("  is a simple project that will allow you to use the Smart Flash",
     "  是一个简单的项目，允许你使用智能闪存编程。"),
    ("  Programming.  NOTE:  As of this writing this project does not work, probably",
     "  注意：截至编写时此项目可能无法正常工作，"),
    ("  due to RAM configuration in the project.  Use ZDS-II instead as is described",
     "  可能是由于项目中的 RAM 配置。请改用 ZDS-II，"),
    ("  in the upper README.txt file",
     "  如上层 README.txt 文件中所述"),
    ("  is the target file that accompanies the project files.",
     "  是伴随项目文件的目标文件。"),
    ("  This one is identical to ``boards/scripts/z20x_ram.ztgt``.",
     "  此文件与 ``boards/scripts/z20x_ram.ztgt`` 相同。"),
    ("  This one is identical to ``boards/scripts/z20x_flash.ztgt``.",
     "  此文件与 ``boards/scripts/z20x_flash.ztgt`` 相同。"),
    ("  This one is identical to boards/scripts/z20x_ram.ztgt.",
     "  此文件与 boards/scripts/z20x_ram.ztgt 相同。"),
    ("  This one is identical to boards/scripts/z20x_flash.ztgt.",
     "  此文件与 boards/scripts/z20x_flash.ztgt 相同。"),
])

# ---- z80/ez80/boards/makerlisp/index.rst ----
_ft("z80/ez80/boards/makerlisp/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the MakerLisp",
     "微控制器。此目录包含将 NuttX 移植到 MakerLisp 开发板的内容，"),
    ("board based on an ez80Acclaim! eZ80F091 microcontroller.",
     "该开发板基于 ez80Acclaim! eZ80F091 微控制器。"),
    ("Configurations", "配置"),
    ("  is a simple ZDS-II project that will allow you to use the ZDS-II debugger.",
     "  是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。"),
    ("  is a simple project that will allow you to use the Smart Flash",
     "  是一个简单的项目，允许你使用智能闪存编程。"),
    ("  Programming.  NOTE:  As of this writing this project does not work, probably",
     "  注意：截至编写时此项目可能无法正常工作，"),
    ("  due to RAM configuration in the project.  Use ZDS-II instead as is described",
     "  可能是由于项目中的 RAM 配置。请改用 ZDS-II，"),
    ("  in the upper README.txt file",
     "  如上层 README.txt 文件中所述"),
    ("  is the target file that accompanies the project files.",
     "  是伴随项目文件的目标文件。"),
])

# ---- z80/z80/boards/z80sim/index.rst ----
_ft("z80/z80/boards/z80sim/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the z80sim",
     "微控制器。此目录包含将 NuttX 移植到 z80sim 模拟器的内容。"),
    ("simulator.", ""),
    ("Configurations", "配置"),
    ("  is a simple ZDS-II project that will allow you to use the ZDS-II debugger.",
     "  是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。"),
    ("  is a simple project that will allow you to use the Smart Flash",
     "  是一个简单的项目，允许你使用智能闪存编程。"),
    ("  Programming.  NOTE:  As of this writing this project does not work, probably",
     "  注意：截至编写时此项目可能无法正常工作，"),
    ("  due to RAM configuration in the project.  Use ZDS-II instead as is described",
     "  可能是由于项目中的 RAM 配置。请改用 ZDS-II，"),
    ("  in the upper README.txt file",
     "  如上层 README.txt 文件中所述"),
    ("  is the target file that accompanies the project files.",
     "  是伴随项目文件的目标文件。"),
])

# ---- z80/ez80/boards/ez80f910200kitg/index.rst ----
_ft("z80/ez80/boards/ez80f910200kitg/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("ez80f910200kitg development board", "ez80f910200kitg 开发板的内容"),
    ("based on an ez80Acclaim! eZ80F091 microcontroller.",
     "该开发板基于 ez80Acclaim! eZ80F091 微控制器。"),
    ("Configurations", "配置"),
    ("  is a simple ZDS-II project that will allow you to use the ZDS-II debugger.",
     "  是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。"),
    ("  is a simple project that will allow you to use the Smart Flash",
     "  是一个简单的项目，允许你使用智能闪存编程。"),
    ("  Programming.  NOTE:  As of this writing this project does not work, probably",
     "  注意：截至编写时此项目可能无法正常工作，"),
    ("  due to RAM configuration in the project.  Use ZDS-II instead as is described",
     "  可能是由于项目中的 RAM 配置。请改用 ZDS-II，"),
    ("  in the upper README.txt file",
     "  如上层 README.txt 文件中所述"),
    ("  is the target file that accompanies the project files.",
     "  是伴随项目文件的目标文件。"),
])

# ---- z80/ez80/boards/ez80f910200zco/index.rst ----
_ft("z80/ez80/boards/ez80f910200zco/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("ez80f910200zcog development board",
     "ez80f910200zcog 开发板的内容"),
    ("based on an ez80Acclaim! eZ80F091 microcontroller.",
     "该开发板基于 ez80Acclaim! eZ80F091 微控制器。"),
    ("Configurations", "配置"),
    ("  is a simple ZDS-II project that will allow you to use the ZDS-II debugger.",
     "  是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。"),
    ("  is a simple project that will allow you to use the Smart Flash",
     "  是一个简单的项目，允许你使用智能闪存编程。"),
    ("  Programming.  NOTE:  As of this writing this project does not work, probably",
     "  注意：截至编写时此项目可能无法正常工作，"),
    ("  due to RAM configuration in the project.  Use ZDS-II instead as is described",
     "  可能是由于项目中的 RAM 配置。请改用 ZDS-II，"),
    ("  in the upper README.txt file",
     "  如上层 README.txt 文件中所述"),
    ("  is the target file that accompanies the project files.",
     "  是伴随项目文件的目标文件。"),
])

# ---- z80/z8/boards/z8f64200100kit/index.rst ----
_ft("z80/z8/boards/z8f64200100kit/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("z8f64200100kit development board",
     "z8f64200100kit 开发板的内容"),
    ("based on a Zilog Z8F6423 Z8Encore! microcontroller.",
     "该开发板基于 Zilog Z8F6423 Z8Encore! 微控制器。"),
    ("Configurations", "配置"),
    ("  is a simple ZDS-II project that will allow you to use the ZDS-II debugger.",
     "  是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。"),
    ("  is a simple project that will allow you to use the Smart Flash",
     "  是一个简单的项目，允许你使用智能闪存编程。"),
    ("  Programming.  NOTE:  As of this writing this project does not work, probably",
     "  注意：截至编写时此项目可能无法正常工作，"),
    ("  due to RAM configuration in the project.  Use ZDS-II instead as is described",
     "  可能是由于项目中的 RAM 配置。请改用 ZDS-II，"),
    ("  in the upper README.txt file",
     "  如上层 README.txt 文件中所述"),
    ("  is the target file that accompanies the project files.",
     "  是伴随项目文件的目标文件。"),
])

# ---- z80/z8/boards/z8encore000zco/index.rst ----
_ft("z80/z8/boards/z8encore000zco/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("z8encore000zco development board",
     "z8encore000zco 开发板的内容"),
    ("based on a Zilog Z8F6403 Z8Encore! microcontroller.",
     "该开发板基于 Zilog Z8F6403 Z8Encore! 微控制器。"),
    ("Configurations", "配置"),
    ("  is a simple ZDS-II project that will allow you to use the ZDS-II debugger.",
     "  是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。"),
    ("  is a simple project that will allow you to use the Smart Flash",
     "  是一个简单的项目，允许你使用智能闪存编程。"),
    ("  Programming.  NOTE:  As of this writing this project does not work, probably",
     "  注意：截至编写时此项目可能无法正常工作，"),
    ("  due to RAM configuration in the project.  Use ZDS-II instead as is described",
     "  可能是由于项目中的 RAM 配置。请改用 ZDS-II，"),
    ("  in the upper README.txt file",
     "  如上层 README.txt 文件中所述"),
    ("  is the target file that accompanies the project files.",
     "  是伴随项目文件的目标文件。"),
])

# ---- z80/z180/boards/p112/index.rst ----
_ft("z80/z180/boards/p112/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the P112",
     "微控制器。此目录包含将 NuttX 移植到 P112 开发板的内容，"),
    ("board based on a Zilog Z80182 Z180 family microcontroller.",
     "该开发板基于 Zilog Z80182 Z180 系列微控制器。"),
    ("Configurations", "配置"),
    ("  is a simple ZDS-II project that will allow you to use the ZDS-II debugger.",
     "  是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。"),
    ("  is a simple project that will allow you to use the Smart Flash",
     "  是一个简单的项目，允许你使用智能闪存编程。"),
    ("  Programming.  NOTE:  As of this writing this project does not work, probably",
     "  注意：截至编写时此项目可能无法正常工作，"),
    ("  due to RAM configuration in the project.  Use ZDS-II instead as is described",
     "  可能是由于项目中的 RAM 配置。请改用 ZDS-II，"),
    ("  in the upper README.txt file",
     "  如上层 README.txt 文件中所述"),
    ("  is the target file that accompanies the project files.",
     "  是伴随项目文件的目标文件。"),
])


# ---- sim/ files ----
_ft("sim/index.rst", [
    ("A user-mode port of NuttX to the x86 Linux/Cygwin platform is available.",
     "NuttX 已移植到 x86 Linux/Cygwin 平台的用户模式。"),
    ("The purpose of this port is primarily to support OS feature development.",
     "此移植的目的主要是为了支持操作系统功能开发。"),
    ("The following Simulator/Emulators are supported:", "支持以下模拟器："),
])

_ft("sim/sim/index.rst", [
    ("It is possible to run NuttX in a simulator called ``sim``, but some features",
     "可以在名为 ``sim`` 的模拟器中运行 NuttX，但部分功能"),
    ("currently are supported only on Linux host (i.e.: Bluetooth, I2C, SPI, etc).",
     "目前仅在 Linux 主机上支持（例如：蓝牙、I2C、SPI 等）。"),
    ("Using ``sim`` you can test many of NuttX features without a supported board.",
     "使用 ``sim`` 你无需支持的开发板即可测试 NuttX 的许多功能。"),
    ("Examples of supported features: Audio, Bluetooth, ELF, I2C, SPI, LVGL, Flash",
     "支持的功能示例：Audio、Bluetooth、ELF、I2C、SPI、LVGL、Flash"),
    ("File System, NX Serves, NX Demos, NX Window Manager, ROMFS, Network: TCP,",
     "文件系统、NX 服务器、NX 演示、NX 窗口管理器、ROMFS、网络：TCP、"),
    ("UDP, IP,6LoWPAN, and many more.",
     "UDP、IP、6LoWPAN 等等。"),
    ("All you need is your machine ``gcc`` working.",
     "你只需要确保机器上的 ``gcc`` 正常工作即可。"),
    ("All you need to do is select your desired board profile configuration",
     "你只需选择所需的开发板配置文件"),
    ("When the compilation finishes it will create a ``nuttx`` binary, then run it::",
     "编译完成后将生成 ``nuttx`` 二进制文件，然后运行它："),
    ("It is possible to run the LVGL Demo directly in the NuttX simulator ::",
     "可以直接在 NuttX 模拟器中运行 LVGL 演示："),
    ("You should see a window with the touch calibration and then the LVGL demo:",
     "你将看到一个触摸校准窗口，然后是 LVGL 演示："),
    ("   LVGL Demo running in the NuttX's simulator",
     "   在 NuttX 模拟器中运行的 LVGL 演示"),
    ("NuttX supports a VNC server, so it means even boards without a LCD display",
     "NuttX 支持 VNC 服务器，这意味着即使没有 LCD 显示屏的开发板"),
    ("could export a display interface over network. Also you can test it on NuttX",
     "也可以通过网络导出显示接口。你还可以在 NuttX 模拟器上测试它，"),
    ("simulator before getting it working on your board, just follow these steps ::",
     "然后再在开发板上运行，只需按照以下步骤操作："),
    ("   remmina connected to sim's VNC Server",
     "   remmina 连接到 sim 的 VNC 服务器"),
    ("The simulator supports CAN support via SocketCAN on the host.",
     "模拟器通过主机上的 SocketCAN 支持 CAN。"),
    ("The CAN interface of the host must be properly configured::",
     "主机的 CAN 接口需要正确配置："),
    ("Virtual CAN interface can be used as well::",
     "也可以使用虚拟 CAN 接口："),
    ("Supported Boards", "支持的开发板"),
])

_ft("sim/sim/boards/sim/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the NuttX",
     "微控制器。此目录包含将 NuttX 移植到 NuttX"),
    ("simulator.", "模拟器的内容。"),
    ("Configurations", "配置"),
    ("  is the NSH configuration.", "  是 NSH 配置。"),
    ("  is a configuration that includes LVGL support with framebuffer.",
     "  是一个包含 LVGL 帧缓冲支持的配置。"),
    ("  is a configuration that includes VNC server support.",
     "  是一个包含 VNC 服务器支持的配置。"),
    ("  is a configuration that includes network via TUN/TAP.",
     "  是一个包含通过 TUN/TAP 网络的配置。"),
    ("  is a configuration that includes network via VPNKit.",
     "  是一个包含通过 VPNKit 网络的配置。"),
])

_ft("sim/network_linux.rst", [
    ("The simulation uses the TUN/TAP driver under Linux to provide network support.",
     "模拟使用 Linux 下的 TUN/TAP 驱动来提供网络支持。"),
    ("It can operate in one of two modes: host routed, or bridged.  In the host",
     "它可以运行在两种模式之一：主机路由或桥接。在主机路由"),
    ("routed case no special configuration is necessary, but by default the",
     "模式下无需特殊配置，但默认情况下"),
    ("simulation will only be accessible to the host on which it runs.",
     "模拟器只能被其运行所在的主机访问。"),
    ("Bridge mode is recommended where possible.  It requires slightly more effort",
     "建议尽可能使用桥接模式。它需要稍多的设置工作，"),
    ("to set up, but is much more flexible, and is likely to be easier to maintain",
     "但更加灵活，而且最终可能更容易维护。"),
    ("in the end.", ""),
    ("Host Route Mode", "主机路由模式"),
    ("If CONFIG_SIM_NET_HOST_ROUTE is enabled, the simulation will create and",
     "如果启用了 CONFIG_SIM_NET_HOST_ROUTE，模拟器将创建并"),
    ("maintain a host route from the assigned IP address to the instance's tap",
     "维护从分配的 IP 地址到实例 tap 设备的主机路由。"),
    ("device.  This route will be updated if the application changes the",
     "如果应用程序更改了模拟器的 IP 地址，此路由将被更新。"),
    ("simulation's IP address.  Note that you will not see the simulation's IP",
     "请注意，如果你在主机上运行 ifconfig，"),
    ("address on the TAP device if you run ifconfig on the host.",
     "你不会在 TAP 设备上看到模拟器的 IP 地址。"),
    ("No special setup is required.  Simply assign your simulation a free IP address",
     "无需特殊设置。只需为模拟器分配一个与主机在同一网络中的空闲 IP 地址，"),
    ("on the same network as your host, and everything will Just Work.  Note that if",
     "一切即可正常工作。请注意，如果你分配的 IP 已被网络中的其他设备使用，"),
    ("you assign an IP that is already in use on your network, your host won't be",
     "在模拟器停止之前，你的主机将无法"),
    ("able to see it until the simulation is stopped.  The host route will force all",
     "看到它。主机路由将强制将所有"),
    ("traffic destined for that IP to be sent to the tap interface.",
     "目标为该 IP 的流量发送到 tap 接口。"),
    ("   host, additional manual setup will be required. A helper script,",
     "   将需要额外的手动设置。提供了一个辅助脚本"),
    ("   On Windows or macOS using host route mode is not recommended.",
     "   不建议在 Windows 或 macOS 上使用主机路由模式。"),
    ("Recent versions of Linux require setting kernel capabilities to allow the nuttx",
     "最新版本的 Linux 需要设置内核能力以允许 nuttx"),
    ("executable access to the tap network driver. You can see more about the tun/tap",
     "可执行文件访问 tap 网络驱动。你可以在以下链接了解更多关于 tun/tap"),
    ("driver requiring Linux capabilities here:",
     "驱动需要 Linux 能力的信息："),
    ("To compile:", "编译方法："),
    ("You can do the following after compiling the NuttX simulator:",
     "编译 NuttX 模拟器后，你可以执行以下操作："),
    ("On Linux:", "在 Linux 上："),
    ("On the NuttX Simulator:", "在 NuttX 模拟器中："),
    ("Bridge Mode", "桥接模式"),
    ("Basic Usage", "基本用法"),
    ("If CONFIG_SIM_NET_BRIDGE is enabled, the simulation's tap interface will",
     "如果启用了 CONFIG_SIM_NET_BRIDGE，模拟器的 tap 接口将"),
    ("automatically be added to the Linux bridge device specified by the",
     "自动添加到由 CONFIG_SIM_NET_BRIDGE_DEVICE 配置选项指定的"),
    ("CONFIG_SIM_NET_BRIDGE_DEVICE configuration option.  Note that this MUST be a",
     "Linux 桥接设备。请注意，这必须是一个"),
    ("pre-existing bridge device, or the initialization will fail.  The simulation",
     "预先存在的桥接设备，否则初始化将失败。模拟器"),
    ("will NOT create the bridge for you.",
     "不会为你创建桥接器。"),
    ("To create the bridge, first install the bridge utilities package for your",
     "要创建桥接器，首先为你的平台安装桥接工具包"),
    ("platform (the net-tools RPM in RedHat, for example).  Then execute a",
     "（例如 RedHat 中的 net-tools RPM）。然后执行"),
    ("command like the following:",
     "类似以下的命令："),
    ("This will create the nuttx0 bridge.  Once created, the bridge may be used by",
     "这将创建 nuttx0 桥接器。创建后，桥接器可以被"),
    ("one or more simulations.  You only need one bridge per host; if you start",
     "一个或多个模拟使用。每个主机只需要一个桥接器；如果你启动"),
    ("multiple simulations, they will all be added to the same bridge and can talk",
     "多个模拟，它们都将被添加到同一个桥接器中，并可以相互通信。"),
    ("amongst themselves.", ""),
    ("Option 1: Routing Local Traffic to the Bridge",
     "选项 1：将本地流量路由到桥接器"),
    ("If you want the host to be able to talk to the simulator, you will",
     "如果你希望主机能够与模拟器通信，你还需要"),
    ("also need to assign the bridge an IP address (this will be the default",
     "为桥接器分配一个 IP 地址（这将是你分配给模拟器的默认网关）"),
    ("gateway you assign to the simulator) and add a network route.  Note",
     "并添加网络路由。请注意"),
    ("that the subnet chosen should not already be in use.  For example, if",
     "所选子网不应已被使用。例如，如果你"),
    ("you want to use the 172.26.23.0/24 subnet for your simluations, you",
     "想使用 172.26.23.0/24 子网进行模拟，"),
    ("would do something like the following:",
     "你可以执行类似以下的操作："),
    ("The standard Linux ifconfig utility will automatically add the appropriate",
     "标准的 Linux ifconfig 工具将自动添加相应的网络路由，"),
    ("network route, so no further effort is needed.",
     "因此无需进一步操作。"),
    ("Option 2: Live Network Access", "选项 2：实时网络访问"),
    ("There are two main methods of giving the simulator access to your network",
     "有两种主要方法可以让模拟器访问你的网络。"),
    ("at large.  One is to set up your Linux host as a router and configure your",
     "一种是将你的 Linux 主机设置为路由器并配置你的网络，"),
    ("network so that it knows where to find the appropriate subnet.  This is far",
     "使其知道如何找到相应的子网。这对大多数用例来说"),
    ("too complex for most use cases, so you can safely ignore it unless you have",
     "过于复杂，因此除非你有特定需求，否则可以安全地忽略它。"),
    ("specific needs.", ""),
    ("The recommended method is to add a real interface to the bridge you're using",
     "推荐的方法是将真实接口添加到你与 NuttX 一起使用的桥接器中。"),
    ("with NuttX.  For example, if you have a secondary eth1 interface on your host,",
     "例如，如果你的主机上有辅助的 eth1 接口，"),
    ("you can simply connect it to the network you want your simulations to access,",
     "你可以简单地将其连接到你希望模拟访问的网络，"),
    ("and run the following command:",
     "并运行以下命令："),
    ("From that point on, your simulations will be directly connected to the same",
     "从那时起，你的模拟将直接连接到与 eth1 接口相同的网络。"),
    ("network as your eth1 interface.  Note that your bridge will generally not need",
     "请注意，在这种情况下，你的桥接器通常不需要 IP 地址。"),
    ("an IP address in this case.", ""),
    ("If you only have a single interface, you can configure your system so that eth0",
     "如果你只有一个接口，你可以配置系统使 eth0"),
    ("(or other primary interface) is on the bridge.  To do this, you would execute",
     "（或其他主接口）在桥接器上。为此，你需要从系统控制台"),
    ("commands like the following from the system console:",
     "执行类似以下的命令："),
    ("The rest of your network configuration would remain the same; your host's IP",
     "你的其余网络配置将保持不变；你主机的 IP 地址只是从"),
    ("address has simply moved from being assigned directly to the ethernet interface,",
     "直接分配给以太网接口，变为分配给包含该接口的桥接器。"),
    ("to being assigned to the bridge that contains that interface.  The connection",
     "连接将正常运行。"),
    ("will operate as normal.  NuttX simulations will join the bridge as with the",
     "NuttX 模拟将像前面的示例一样加入桥接器。"),
    ("previous example.", ""),
    ("In either of the live access scenarios presented here, the default gateway you",
     "在本文介绍的两种实时访问场景中，你在模拟中配置的默认网关"),
    ("configure in your simluation should be the normal one for the network you're",
     "应该是你所访问网络的正常网关，"),
    ("accessing, whether or not the bridge has an IP address.  The bridge is acting",
     "无论桥接器是否有 IP 地址。桥接器充当"),
    ("as an ethernet hub; your simluation has direct access to the normal gateway as",
     "以太网集线器；你的模拟直接访问正常网关，"),
    ("if the simluation were a device physically connected to the network.",
     "就好像模拟是物理连接到网络的设备一样。"),
    ("Configuring at Startup", "启动时配置"),
    ("Most Linux distributions have a mechanism for configuring a bridge at startup.",
     "大多数 Linux 发行版都有在启动时配置桥接器的机制。"),
    ("See your distribution's documentation for more information.",
     "请参阅你发行版的文档获取更多信息。"),
    ("Setup Script", "设置脚本"),
    ("There is a script, `tools/simbridge.sh` that will do the setup for you.",
     "有一个脚本 `tools/simbridge.sh` 可以为你完成设置。"),
    ("Notes", "注意事项"),
    ("  - Users of VMware ESXi should be aware that the bridge will place the contained",
     "  - VMware ESXi 用户应注意，桥接器会将包含的以太网接口置于混杂模式"),
    ("    ethernet interface into promiscuous mode (don't ask me why).  ESXi will",
     "    （不要问我为什么）。ESXi 默认会拒绝此操作，"),
    ("    reject this by default, and nothing will work.  To fix this, edit the",
     "    什么都不起作用。要修复此问题，请编辑相关 vSwitch 或 VLAN 的属性，"),
    ("    I don't know if VMware's consumer products have similar issues or not.",
     "    我不知道 VMware 的消费产品是否有类似的问题。"),
])

_ft("sim/network_vpnkit.rst", [
    ("The simulation can be configured to use VPNKit to provide network support.",
     "可以配置模拟使用 VPNKit 来提供网络支持。"),
    ("While this was developed for macOS, it should work on other platforms",
     "虽然这是为 macOS 开发的，但它也应该能在其他平台上工作。"),
    ("as well.", ""),
    ("You can use the ``sim:vpnkit`` configuration, which includes the above",
     "你可以使用 ``sim:vpnkit`` 配置，其中包含上述设置。"),
    ("settings.", ""),
    ("VPNKit setup", "VPNKit 设置"),
    ("See `https://github.com/moby/vpnkit` for build instructions.",
     "请参阅 `https://github.com/moby/vpnkit` 获取构建说明。"),
    ("If you have Docker Desktop for Mac installed on your machine,",
     "如果你的机器上安装了 Docker Desktop for Mac，"),
    ("you can find a vpnkit binary at:",
     "你可以在以下位置找到 vpnkit 二进制文件："),
    ("A docker image containing a static Linux binary is also available:",
     "也提供包含静态 Linux 二进制文件的 Docker 镜像："),
    ("How to run", "如何运行"),
    ("You can use it as the following:",
     "你可以按如下方式使用："),
    ("NuttX's ``CONFIG_SIM_NETDEV_VPNKIT_PATH`` should match vpnkit's",
     "NuttX 的 ``CONFIG_SIM_NETDEV_VPNKIT_PATH`` 应与 vpnkit 的"),
    ("``--ethernet`` option.",
     "``--ethernet`` 选项匹配。"),
])

_ft("sim/sim_gpiochip.rst", [
    ("Overview", "概述"),
    ("The Sim GPIO Chip driver provides a mechanism for NuttX simulation (sim) to access",
     "Sim GPIO 芯片驱动为 NuttX 模拟器（sim）提供了一种访问"),
    ("the Linux host's GPIO chip devices (``/dev/gpiochipN``). This allows NuttX applications",
     "Linux 主机 GPIO 芯片设备（``/dev/gpiochipN``）的机制。这使得"),
    ("running in simulation mode to interact with real hardware GPIO pins connected to the",
     "在模拟模式下运行的 NuttX 应用程序能够与连接到 Linux 主机系统的真实硬件 GPIO 引脚进行交互。"),
    ("Linux host system.", ""),
    ("This driver is particularly useful for:", "此驱动特别适用于："),
    ("- Testing GPIO-based applications in a simulated environment with real hardware",
     "- 在带有真实硬件的模拟环境中测试基于 GPIO 的应用程序"),
    ("- Interfacing with USB-to-GPIO adapters (e.g., CH341A) from NuttX simulation",
     "- 从 NuttX 模拟器与 USB 转 GPIO 适配器（如 CH341A）进行接口"),
    ("- Developing and debugging GPIO drivers without dedicated embedded hardware",
     "- 无需专用嵌入式硬件即可开发和调试 GPIO 驱动"),
    ("Host Prepare", "主机准备"),
    ("Preparation required on the host side:", "主机端需要的准备工作："),
    ("- Hardware module required: USB-CH341A module",
     "- 所需硬件模块：USB-CH341A 模块"),
    ("- Verify existence of /dev/gpiochipN device file",
     "- 验证 /dev/gpiochipN 设备文件是否存在"),
    ("The driver consists of two layers:", "驱动由两层组成："),
    ("   interface, providing standard GPIO operations to upper-layer NuttX drivers.",
     "   接口，为上层 NuttX 驱动提供标准 GPIO 操作。"),
    ("   GPIO character device (``/dev/gpiochipN``) using the GPIO v2 ABI.",
     "   GPIO 字符设备（``/dev/gpiochipN``）使用 GPIO v2 ABI 进行接口。"),
    ("Header Files", "头文件"),
    ("   and function prototypes.",
     "   和函数原型。"),
    ("Configuration Options", "配置选项"),
    ("The following configuration options are relevant to this driver:",
     "以下配置选项与此驱动相关："),
    ("- ``CONFIG_SIM_GPIOCHIP``: Enable the sim GPIO chip driver.",
     "- ``CONFIG_SIM_GPIOCHIP``：启用 sim GPIO 芯片驱动。"),
    ("- ``CONFIG_IOEXPANDER_NPINS``: Maximum number of GPIO pins supported (default: 64).",
     "- ``CONFIG_IOEXPANDER_NPINS``：支持的最大 GPIO 引脚数（默认：64）。"),
    ("- ``CONFIG_IOEXPANDER_INT_ENABLE``: Enable interrupt support for GPIO pins.",
     "- ``CONFIG_IOEXPANDER_INT_ENABLE``：启用 GPIO 引脚的中断支持。"),
    ("Supported Operations", "支持的操作"),
    ("The driver supports the following GPIO operations:",
     "驱动支持以下 GPIO 操作："),
    ("Direction Control", "方向控制"),
    ("Set GPIO pin direction. Supported directions:",
     "设置 GPIO 引脚方向。支持的方向："),
    ("- ``IOEXPANDER_DIRECTION_IN``: Configure as input",
     "- ``IOEXPANDER_DIRECTION_IN``：配置为输入"),
    ("- ``IOEXPANDER_DIRECTION_OUT``: Configure as output",
     "- ``IOEXPANDER_DIRECTION_OUT``：配置为输出"),
    ("- ``IOEXPANDER_DIRECTION_OUT_OPENDRAIN``: Configure as open-drain output",
     "- ``IOEXPANDER_DIRECTION_OUT_OPENDRAIN``：配置为开漏输出"),
    ("Read/Write Pin", "读取/写入引脚"),
    ("Read or write the value of a GPIO pin.",
     "读取或写入 GPIO 引脚的值。"),
    ("Interrupt Configuration", "中断配置"),
    ("Configure GPIO pin options. Supported interrupt edge configurations:",
     "配置 GPIO 引脚选项。支持的中断边沿配置："),
    ("- ``IOEXPANDER_VAL_RISING``: Trigger on rising edge",
     "- ``IOEXPANDER_VAL_RISING``：上升沿触发"),
    ("- ``IOEXPANDER_VAL_FALLING``: Trigger on falling edge",
     "- ``IOEXPANDER_VAL_FALLING``：下降沿触发"),
    ("- ``IOEXPANDER_VAL_BOTH``: Trigger on both edges",
     "- ``IOEXPANDER_VAL_BOTH``：双沿触发"),
    ("- ``IOEXPANDER_VAL_DISABLE``: Disable interrupt",
     "- ``IOEXPANDER_VAL_DISABLE``：禁用中断"),
    ("Interrupt Callback", "中断回调"),
    ("Attach or detach an interrupt callback function for GPIO pins.",
     "附加或分离 GPIO 引脚的中断回调函数。"),
    ("Host Layer API", "主机层 API"),
    ("The host layer (``sim_linux_gpiochip.c``) provides the following functions:",
     "主机层（``sim_linux_gpiochip.c``）提供以下功能："),
    ("   /* Allocate and initialize a host GPIO chip device */",
     "   /* 分配并初始化主机 GPIO 芯片设备 */"),
    ("   /* Free a host GPIO chip device */",
     "   /* 释放主机 GPIO 芯片设备 */"),
    ("   /* Set GPIO pin direction */",
     "   /* 设置 GPIO 引脚方向 */"),
    ("   /* Read GPIO pin value */",
     "   /* 读取 GPIO 引脚值 */"),
    ("   /* Write GPIO pin value */",
     "   /* 写入 GPIO 引脚值 */"),
    ("   /* Request GPIO interrupt */",
     "   /* 请求 GPIO 中断 */"),
    ("   /* Check if GPIO interrupt is active */",
     "   /* 检查 GPIO 中断是否激活 */"),
    ("   /* Get GPIO line information */",
     "   /* 获取 GPIO 线路信息 */"),
    ("Linux Kernel Version Requirements", "Linux 内核版本要求"),
    ("The driver uses Linux GPIO v2 ABI, which requires:",
     "驱动使用 Linux GPIO v2 ABI，要求："),
    ("- **Linux kernel >= 6.8.0**: Full functionality with GPIO v2 API support.",
     "- **Linux 内核 >= 6.8.0**：具有 GPIO v2 API 支持的完整功能。"),
    ("- **Linux kernel < 6.8.0**: The driver compiles but provides stub implementations",
     "- **Linux 内核 < 6.8.0**：驱动可以编译但提供存根实现"),
    ("  that return 0 or NULL.",
     "  返回 0 或 NULL。"),
    ("Usage Example", "使用示例"),
    ("Initialization", "初始化"),
    ("     /* Initialize the GPIO chip device */",
     "     /* 初始化 GPIO 芯片设备 */"),
    ("     /* Register GPIO pins using gpio_lower_half */",
     "     /* 使用 gpio_lower_half 注册 GPIO 引脚 */"),
    ("Application Usage", "应用使用"),
    ("After initialization, GPIO pins can be accessed through standard NuttX GPIO interface:",
     "初始化后，可以通过标准 NuttX GPIO 接口访问 GPIO 引脚："),
    ("     /* Open GPIO device */",
     "     /* 打开 GPIO 设备 */"),
    ("     /* Read GPIO value */",
     "     /* 读取 GPIO 值 */"),
    ("Interrupt Handling", "中断处理"),
    ("The driver uses a work queue to poll for GPIO events. The polling interval is",
     "驱动使用工作队列来轮询 GPIO 事件。轮询间隔"),
    ("defined by ``SIM_GPIOCHIP_WORK_DELAY`` (default: 500 microseconds).",
     "由 ``SIM_GPIOCHIP_WORK_DELAY`` 定义（默认：500 微秒）。"),
    ("When an interrupt event is detected on a GPIO pin, the registered callback",
     "当在 GPIO 引脚上检测到中断事件时，已注册的回调"),
    ("function is invoked with the pin number and user-provided argument.",
     "函数将使用引脚号和用户提供的参数被调用。"),
    ("   /* Attach interrupt handler */",
     "   /* 附加中断处理程序 */"),
    ("   /* Configure interrupt edge */",
     "   /* 配置中断边沿 */"),
    ("Files", "文件"),
    ("-  ``arch/sim/src/sim/sim_gpiochip.c``: NuttX IO expander implementation",
     "-  ``arch/sim/src/sim/sim_gpiochip.c``：NuttX IO 扩展器实现"),
    ("-  ``arch/sim/src/sim/posix/sim_linux_gpiochip.c``: Linux host GPIO interface",
     "-  ``arch/sim/src/sim/posix/sim_linux_gpiochip.c``：Linux 主机 GPIO 接口"),
    ("-  ``arch/sim/src/sim/sim_hostgpiochip.h``: Host GPIO chip header file",
     "-  ``arch/sim/src/sim/sim_hostgpiochip.h``：主机 GPIO 芯片头文件"),
    ("Limitations", "限制"),
    ("1. **Polling-based interrupts**: Due to simulation constraints, interrupts are",
     "1. **基于轮询的中断**：由于模拟限制，中断"),
    ("   implemented using polling rather than true hardware interrupts.",
     "   使用轮询而非真正的硬件中断来实现。"),
    ("2. **Linux kernel version**: Full functionality requires Linux kernel >= 6.8.0.",
     "2. **Linux 内核版本**：完整功能需要 Linux 内核 >= 6.8.0。"),
    ("3. **Pin count**: Limited by ``CONFIG_IOEXPANDER_NPINS`` configuration.",
     "3. **引脚数量**：受 ``CONFIG_IOEXPANDER_NPINS`` 配置限制。"),
    ("4. **Invert option**: The ``IOEXPANDER_OPTION_INVERT`` option is not yet implemented.",
     "4. **反转选项**：``IOEXPANDER_OPTION_INVERT`` 选项尚未实现。"),
    ("See Also", "另请参阅"),
])


# ---- tricore/ files ----
_ft("tricore/index.rst", [
    ("All TriCore source reside in lower-level common, chip-specific, and architecture-specific",
     "所有 TriCore 源代码位于底层通用、芯片特定和架构特定的"),
    ("directories.", "目录中。"),
    ("Architecture-Specific Directories", "架构特定目录"),
    ("This directory holds source files common to all TriCore architectures.",
     "此目录包含所有 TriCore 架构通用的源文件。"),
    ("Architecture-specific directories hold common source files shared for by",
     "架构特定目录包含特定 TriCore 架构实现共享的通用源文件。"),
    ("implementations of specific TriCore architectures.", ""),
    ("Chip-Specific directories", "芯片特定目录"),
    ("For SoC chips, in particular, on-chip devices and differing interrupt",
     "特别是对于 SoC 芯片，片上设备和不同的中断"),
    ("structures may require special, chip-specific definitions in these chip-",
     "结构可能需要在这些芯片特定目录中进行特殊的芯片特定定义。"),
    ("specific directories.", ""),
    ("The core Chip implementation is based on Infineon Low Level Drivers (iLLDs).",
     "核心芯片实现基于英飞凌底层驱动（iLLDs）。"),
    ("The unified API is more friendly to developers familiar with Infineon SDK/HAL.",
     "统一的 API 对熟悉英飞凌 SDK/HAL 的开发者更加友好。"),
    ("We can get more code examples on Infineon's official Github:",
     "你可以在英飞凌官方 Github 上获取更多代码示例："),
    ("  This directory holds logic appropriate for any instantiation of the 32-bit",
     "  此目录包含适用于 32 位 TriCore 架构任何实例化的逻辑。"),
    ("  This is the implementation of NuttX on the Infineon's AURIX(TM)- TC3xx/TC4xx microcontroller family.",
     "  这是 NuttX 在英飞凌 AURIX(TM) TC3xx/TC4xx 微控制器系列上的实现。"),
])

_ft("tricore/tc397/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
    ("All TriCore source reside in lower-level common, chip-specific, and architecture-specific",
     "所有 TriCore 源代码位于底层通用、芯片特定和架构特定的"),
    ("directories.", "目录中。"),
])

_ft("tricore/tc4d9/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("tricore/tc397/boards/kit_a2g_tc397_tft/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the Infineon TriCore",
     "微控制器。此目录包含将 NuttX 移植到英飞凌 TriCore"),
    ("TC397 TFT kit board.", "TC397 TFT 套件开发板的内容。"),
    ("Configurations", "配置"),
])

_ft("tricore/tc4d9/boards/triboard_tc4x9_com/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the Infineon TriCore",
     "微控制器。此目录包含将 NuttX 移植到英飞凌 TriCore"),
    ("TC4D9 TriBoard.", "TC4D9 TriBoard 开发板的内容。"),
    ("Configurations", "配置"),
])


# ---- sparc/ files ----
_ft("sparc/index.rst", [
    ("SPARC Architecture", "SPARC 架构"),
    ("The SPARC (Scalable Processor Architecture) is a RISC instruction set architecture",
     "SPARC（可扩展处理器架构）是一种 RISC 指令集架构"),
    ("(ISA) developed by Sun Microsystems.", "（ISA），由 Sun Microsystems 开发。"),
    ("The following SPARC chips are supported:", "支持以下 SPARC 芯片："),
])

_ft("sparc/bm3803/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("sparc/bm3803/boards/xx3803/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])

_ft("sparc/bm3823/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("sparc/bm3823/boards/xx3823/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])

_ft("sparc/s698pm/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("sparc/s698pm/boards/s698pm-dkit/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])


# ---- renesas/ files ----
_ft("renesas/index.rst", [
    ("Renesas Architecture", "瑞萨架构"),
    ("The following Renesas architectures are supported:", "支持以下瑞萨架构："),
])

_ft("renesas/sh1/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("renesas/sh1/boards/us7032evb1/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])

_ft("renesas/rx65n/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("renesas/rx65n/boards/rx65n-grrose/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])

_ft("renesas/rx65n/boards/rx65n-rsk2mb/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])

_ft("renesas/m16c/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("renesas/m16c/boards/skp16c26/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])


# ---- mips/ files ----
_ft("mips/index.rst", [
    ("MIPS Architecture", "MIPS 架构"),
    ("The following MIPS architectures are supported:", "支持以下 MIPS 架构："),
])

_ft("mips/pic32mx/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("mips/pic32mz/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("mips/pic32mx/boards/pic32mx-starterkit/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])

_ft("mips/pic32mx/boards/ubw32/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])

_ft("mips/pic32mx/boards/sure-pic32mx/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])

_ft("mips/pic32mx/boards/pic32mx7mmb/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])

_ft("mips/pic32mx/boards/mirtoo/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])

_ft("mips/pic32mz/boards/pic32mz-starterkit/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])

_ft("mips/pic32mz/boards/chipkit-wifire/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])

_ft("mips/pic32mz/boards/flipnclick-pic32mz/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])


# ---- hc/ files ----
_ft("hc/index.rst", [
    ("HC/S12 (Freescale M9S12)", "HC/S12（Freescale M9S12）"),
    ("The following Freescale/NXP HCS12 (9S12) architecture is supported:",
     "支持以下 Freescale/NXP HCS12（9S12）架构："),
])

_ft("hc/m9s12/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("hc/m9s12/boards/demo9s12ne64/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])

_ft("hc/m9s12/boards/ne64badge/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])


# ---- z16/ files ----
_ft("z16/index.rst", [
    ("Z16F (Zilog Z16F Series)", "Z16F（Zilog Z16F 系列）"),
    ("The following Zilog Z16F architecture is supported:",
     "支持以下 Zilog Z16F 架构："),
])

_ft("z16/z16f/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("z16/z16f/boards/z16f2800100zcog/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])


# ---- x86_64/ files ----
_ft("x86_64/index.rst", [
    ("x86_64 Architecture", "x86_64 架构"),
    ("The following x86_64 architecture is supported:",
     "支持以下 x86_64 架构："),
])

_ft("x86_64/intel64/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("x86_64/intel64/boards/qemu-intel64/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])


# ---- x86/ files ----
_ft("x86/index.rst", [
    ("x86 Architecture", "x86 架构"),
    ("The following x86 architecture is supported:",
     "支持以下 x86 架构："),
])

_ft("x86/qemu/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("x86/qemu/boards/qemu-i486/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])


# ---- or1k/ files ----
_ft("or1k/index.rst", [
    ("OpenRISC 1000 (or1k)", "OpenRISC 1000（or1k）"),
    ("The following OpenRISC 1000 architecture is supported:",
     "支持以下 OpenRISC 1000 架构："),
])

_ft("or1k/mor1kx/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("or1k/mor1kx/boards/or1k/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])


# ---- misco/ files ----
_ft("misco/index.rst", [
    ("MiSoC (Mico32)", "MiSoC（Mico32）"),
    ("The following MiSoC architecture is supported:",
     "支持以下 MiSoC 架构："),
])

_ft("misco/lm32/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("misco/lm32/boards/misoc/index.rst", [
    ("Microcontroller.  This directory holds the port of NuttX to the",
     "微控制器。此目录包含将 NuttX 移植到"),
    ("Configurations", "配置"),
])


# ---- ceva/ files ----
_ft("ceva/index.rst", [
    ("CEVA DSP", "CEVA DSP"),
    ("The following CEVA DSP architectures are supported:",
     "支持以下 CEVA DSP 架构："),
])

_ft("ceva/xc5/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])

_ft("ceva/xm6/index.rst", [
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
])


# ==================== Title Translations ====================

TITLE_MAP = {
    "Z80": "Z80",
    "Zilog Z80": "Zilog Z80",
    "Zilog Z8Encore!": "Zilog Z8Encore!",
    "Zilog Z180": "Zilog Z180",
    "Zilog eZ80 Acclaim!": "Zilog eZ80 Acclaim!",
    "Z8": "Z8",
    "Z180": "Z180",
    "eZ80": "eZ80",
    "z20x": "z20x",
    "z80sim": "z80sim",
    "MakerLisp": "MakerLisp",
    "ez80f910200kitg": "ez80f910200kitg",
    "ez80f910200zco": "ez80f910200zco",
    "z8f64200100kit": "z8f64200100kit",
    "z8encore000zco": "z8encore000zco",
    "P112": "P112",
    "Simulators": "模拟器",
    "SIM": "SIM",
    "TriCore": "TriCore",
    "SPARC": "SPARC",
    "Renesas": "瑞萨",
    "MIPS": "MIPS",
    "HC": "HC",
    "Z16": "Z16",
    "x86_64": "x86_64",
    "x86": "x86",
    "OR1K": "OR1K",
    "MiSoC": "MiSoC",
    "CEVA": "CEVA",
    "Network Support on Linux": "Linux 网络支持",
    "Network support with VPNKit": "使用 VPNKit 的网络支持",
    "Sim GPIO Chip Driver (Linux Host GPIO)": "Sim GPIO 芯片驱动（Linux 主机 GPIO）",
    "Network Support on Linux Host": "Linux 主机网络支持",
    "MIPS Architecture": "MIPS 架构",
    "Renesas Architecture": "瑞萨架构",
    "SPARC Architecture": "SPARC 架构",
    "Infineon TriCore": "英飞凌 TriCore",
    "NuttX Simulator": "NuttX 模拟器",
    "HC/S12 (Freescale M9S12)": "HC/S12（Freescale M9S12）",
    "Z16F (Zilog Z16F Series)": "Z16F（Zilog Z16F 系列）",
    "x86_64 Architecture": "x86_64 架构",
    "x86 Architecture": "x86 架构",
    "OpenRISC 1000 (or1k)": "OpenRISC 1000（or1k）",
    "MiSoC (Mico32)": "MiSoC（Mico32）",
    "CEVA DSP": "CEVA DSP",
    "x86 (i486)": "x86（i486）",
    "QEMU i486": "QEMU i486",
    "Intel64": "Intel64",
    "QEMU Intel64": "QEMU Intel64",
}


# ==================== Sub-heading Translations ====================

HEADING_MAP = {
    "Supported Boards": "支持的开发板",
    "Configurations": "配置",
    "Overview": "概述",
    "Architecture": "架构",
    "Header Files": "头文件",
    "Configuration Options": "配置选项",
    "Supported Operations": "支持的操作",
    "Usage Example": "使用示例",
    "Initialization": "初始化",
    "Application Usage": "应用使用",
    "Files": "文件",
    "Limitations": "限制",
    "See Also": "另请参阅",
    "Notes": "注意事项",
    "Setup Script": "设置脚本",
    "Host Route Mode": "主机路由模式",
    "Bridge Mode": "桥接模式",
    "Basic Usage": "基本用法",
    "Compiling": "编译",
    "Running": "运行",
    "Toolchain": "工具链",
    "Direction Control": "方向控制",
    "Read/Write Pin": "读取/写入引脚",
    "Interrupt Configuration": "中断配置",
    "Interrupt Callback": "中断回调",
    "Host Layer API": "主机层 API",
    "Interrupt Handling": "中断处理",
    "Host Prepare": "主机准备",
    "Running LVGL": "运行 LVGL",
    "Running VNC Server": "运行 VNC 服务器",
    "Running Simulated CAN": "运行模拟 CAN",
    "Network Support on Linux": "Linux 网络支持",
    "Network support with VPNKit": "使用 VPNKit 的网络支持",
    "Configuration": "配置",
    "VPNKit setup": "VPNKit 设置",
    "How to run": "如何运行",
    "Linux Kernel Version Requirements": "Linux 内核版本要求",
    "Architecture-Specific Directories": "架构特定目录",
    "Chip-Specific directories": "芯片特定目录",
    "Chip-Specific Directories": "芯片特定目录",
    "Option 1: Routing Local Traffic to the Bridge": "选项 1：将本地流量路由到桥接器",
    "Option 2: Live Network Access": "选项 2：实时网络访问",
    "Configuring at Startup": "启动时配置",
}


# ==================== Processing Logic ====================

def process_file(src_path, rel_path):
    """Read source file, apply translations, write output."""
    with open(src_path, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    
    # Get per-file translations
    file_trans = FILE_TRANSLATIONS.get(rel_path, {})
    # Build lookup dict for fast matching
    trans_dict = {}
    for old, new in file_trans:
        trans_dict[old] = new
    
    out = []
    i = 0
    in_code_block = False
    title_done = False
    
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()
        
        # ---- Code block handling ----
        if not in_code_block:
            if stripped.startswith('.. code-block::'):
                in_code_block = True
                out.append(line)
                i += 1
                continue
            if stripped == '::':
                in_code_block = True
                out.append(line)
                i += 1
                continue
        else:
            out.append(line)
            if stripped == '':
                # Look ahead
                j = i + 1
                while j < len(lines) and lines[j].strip() == '':
                    j += 1
                if j < len(lines) and lines[j].strip():
                    next_indent = len(lines[j]) - len(lines[j].lstrip())
                    # Stay in code block if next non-empty line is indented
                    if next_indent > 0:
                        i += 1
                        continue
                in_code_block = False
            i += 1
            continue
        
        # ---- RST directive handling (.. directive:: ...) ----
        if stripped.startswith('.. ') and '::' in stripped:
            # Check for special directives that contain prose
            if stripped.startswith('.. note::'):
                out.append(line)
                i += 1
                continue
            out.append(line)
            i += 1
            # Collect directive body
            base_indent = len(line) - len(line.lstrip())
            while i < len(lines):
                curr = lines[i]
                if curr.strip() == '':
                    out.append(curr)
                    i += 1
                    if i < len(lines):
                        nl = lines[i]
                        nl_lstripped = nl.lstrip()
                        if nl.strip() and (len(nl) - len(nl_lstripped) > base_indent or nl_lstripped.startswith(':')):
                            continue
                    break
                elif (len(curr) - len(curr.lstrip()) > base_indent or 
                      curr.lstrip().startswith(':')):
                    out.append(curr)
                    i += 1
                else:
                    break
            continue
        
        # ---- Title detection ----
        if (i + 1 < len(lines) and 
            stripped and 
            lines[i+1].strip() and 
            re.match(r'^([=\-~^`#"*+])\1+$', lines[i+1].strip()) and
            not re.match(r'^[=\-~^`#"*+]+$', stripped)):
            
            title_text = stripped
            underline_char = lines[i+1].strip()[0]
            
            # Translate title
            translated = TITLE_MAP.get(title_text, title_text)
            # Check if it's a sub-heading in HEADING_MAP
            if title_text in HEADING_MAP:
                translated = HEADING_MAP[title_text]
            
            new_underline = underline_char * len(translated)
            out.append(translated)
            out.append(new_underline)
            i += 2
            
            # Insert note after main title
            if not title_done:
                out.append('')
                out.append(NOTE_AFTER_TITLE)
                title_done = True
            
            continue
        
        # ---- Regular line translation ----
        if stripped in trans_dict:
            result = trans_dict[stripped]
            indent = len(line) - len(line.lstrip())
            if result:
                out.append(' ' * indent + result)
            # If result is empty, skip the line (merged with previous)
            i += 1
            continue
        
        # Check partial matches for tab-indented content
        found = False
        for old, new in file_trans:
            if stripped == old.strip() and stripped:
                indent = len(line) - len(line.lstrip())
                if new:
                    out.append(' ' * indent + new)
                found = True
                break
        if found:
            i += 1
            continue
        
        # No translation found - keep original line
        out.append(line)
        i += 1
    
    return '\n'.join(out)


def main():
    files = get_all_rst_files()
    print(f"Found {len(files)} .rst files to process")
    
    success = 0
    failed = 0
    
    for full_path, rel_path in files:
        dst_path = os.path.join(DST, rel_path)
        try:
            translated = process_file(full_path, rel_path)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(translated)
            print(f"  OK: {rel_path}")
            success += 1
        except Exception as e:
            print(f"  FAIL: {rel_path}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print(f"\nDone: {success} OK, {failed} failed, {len(files)} total")


if __name__ == "__main__":
    main()
