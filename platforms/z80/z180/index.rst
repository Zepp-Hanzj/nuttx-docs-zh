==========
Zilog Z180
==========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**P112**。P112 是一款基于 16MHz Z80182 的爱好者单板计算机，
配备高达 1MB 内存、串口、并口和磁盘 IO，
以及实时时钟，采用 3.5 英寸驱动器外形尺寸。P112 计算机
最初是澳大利亚 "D-X Designs Pty Ltd" 的商业产品。
Australia.

Dave Brooks 于 2012 年 11 月通过 Kickstarter 成功众筹了
又一批 P112 开发板。此外，Terry Gulczynski
还制作了额外的 P112 衍生爱好者自制计算机。

**STATUS:** Most of the NuttX is in port for both the Z80182 and for the
来自 Kickstarter 项目的开发板要到
2013 年第三季度才会可用。因此还需要一些时间
才能在硬件上验证此移植。请参阅 NuttX 开发板
`README <https://github.com/apache/nuttx/blob/master/Documentation/platforms/z80/z180/boards/p112/README.txt>`__
file for further information.

The arch/z80 directories contain files to support a variety of 8-bit architectures
from ZiLOG (and spin-architectures such as the Rabbit2000).  The arch/z80/src/z180
子目录包含经典 Z180 芯片系列特有的逻辑。

此目录中的文件包括：

``z180_head.asm``
 	这是 Z180 程序的主入口点。包括 RESET、上电中断向量和地址零
 	以及所有 RST 中断的处理程序。
	RST interrupts.

``z180_rom.asm``
 	部分架构可能在地址零处放置 ROM。在这种情况下，
 	必须使用特殊的"head"逻辑版本。此特殊的"head"文件
 	可能是特定于开发板的，因此属于特定于开发板的
 	boards/z80/z180/<board-name>/src 目录。但此文件
 	可以用作此类特定于开发板文件的模板。

 	通过在配置文件中指定 CONFIG_LINKER_ROM_AT_0000 来启用 z180_rom.S。
	configuration file.

 	boards/z80/z180/<board-name>/src 目录中的特定于开发板的版本可通过以下方式使用：
	directory can be used by:

	1. Define CONFIG_ARCH_HAVEHEAD
	2. Add the board-specific head file, say <filename>.asm, to
	   boards/z80/z180/<board-name>/src
	3. Add a file called Make.defs in the boards/z80/z180/<board-name>/src
	   directory containing the line:  HEAD_ASRC = <file-name>.asm

``Make.defs``
 	这是必须在所有芯片目录中提供的标准 makefile 片段。
 	此片段标识用于构建 libarch 的芯片特定文件。

``chip.h``
 	这是必须在所有芯片目录中提供的标准头文件。
	directories.

``z180_initialstate.c``, ``z180_copystate.c``,  ``z180_restoreusercontext.asm``, ``z180_saveusercontext.asm``
    这些文件实现了 Z180 上下文切换逻辑

``z180_schedulesigaction.c`` and  ``z180_sigdeliver.c``
 	这些文件实现了 Z180 信号处理。

支持的开发板
======

.. toctree::
   :glob:
   :maxdepth: 1

   boards/*/*
