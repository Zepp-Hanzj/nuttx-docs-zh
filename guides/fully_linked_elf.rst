===============================
ELF 程序 - 无符号表
===============================

您可以使用通过文件系统提供的 ELF 程序轻松扩展已发布的嵌入式系统中的固件。例如，SD 卡或下载到板载 SPI FLASH 中。

为了支持这种发布后的更新，您发布的固件必须支持执行加载到 RAM 中的 ELF 程序以及通过文件系统提供的符号表（参见 `apps/examples/elf`）。

Alan Carvalho de Assis 还基于此示例制作了视频，并在 `NuttX YouTube 频道 <https://www.youtube.com/watch?v=oL6KAgkTb8M>`_ 上发布。

创建导出包
===========================

在固件发布时，您应该创建并保存一个导出包。此导出包包含为嵌入式系统创建发布后附加模块所需的所有必要文件。

出于演示目的，我们将使用 STM32F4-Discovery 和网络 NSH 配置。此设置假设您拥有 STM32F4DIS-BB 底板。演示还需要支持外部可修改的介质，例如：

- 可移动介质，如 SD 卡或 USB 闪存驱动器。
- 可通过 USB MSC、FTP 或其他协议远程访问的内部文件系统。
- 远程文件系统，如 NFS。

在此演示中，网络 NSH 配置使用 STM32 底板上的 SD 卡。其他 NSH 配置也可以使用，前提是它们提供必要的文件系统支持。

.. tip::
   没有底板？您可以按照以下说明为基本 STM32F4-Discovery 板添加文件系统支持：`USB FLASH 驱动器 <https://www.youtube.com/watch?v=5hB5ZXpRoS4>`__ 或 `SD 卡 <https://www.youtube.com/watch?v=H28t4RbOXqI>`__。

初始化环境：

.. code-block:: console

   $ make distclean
   $ tools/configure.sh -c stm32f4discovery:netnsh
   $ make menuconfig

编辑配置：

- 禁用网络（此示例不需要）：``# CONFIG_NET is not set``。
- 启用无外部符号表的 ELF 二进制支持：``CONFIG_ELF=y``，``CONFIG_LIBC_EXECFUNCS=y``，``# CONFIG_EXECFUNCS_HAVE_SYMTAB is not set``。
- 启用 PATH 变量支持：``CONFIG_LIBC_ENVPATH=y``，``CONFIG_PATH_INITIAL="/addons"``，``# CONFIG_DISABLE_ENVIRON not set``。
- 启用从 NSH 执行 ELF 文件：``CONFIG_NSH_FILE_APPS=y``。

.. note::

   您必须启用某个使用 ``printf()`` 的应用程序。这对于确保符号 ``printf()`` 包含在基础系统中是必要的。这里我们假设 ``apps/examples/hello`` 中的 "Hello, World!" 示例已通过配置选项 ``CONFIG_EXAMPLES_HELLO=y`` 启用。

然后，构建 NuttX 固件映像和导出包：

.. code-block:: console

   $ make
   $ make export

当 ``make export`` 完成时，您会在 NuttX 顶层目录中找到一个名为 ``nuttx-export-x.y.zip`` 的 ZIP 包（其中 ``x.y`` 对应于同目录中 ``.version`` 文件确定的版本）。
此 ZIP 文件的内容组织如下：

.. code-block:: text

   nuttx-export-x.x
   |- arch/
   |- include/
   |- libs/
   |- registry/
   |- scripts/
   |- startup/
   |- tools/
   |- System.map
   `- .config

准备附加组件构建目录
====================================

为了创建附加 ELF 程序，您将需要：

1. 导出包。
2. 用于构建程序的 Makefile。
3. 在 Makefile 中使用的第一链接器脚本（``gnu-elf.ld``）。
4. 用于创建第二链接器脚本（``defines.ld``）的 Bash 脚本。

.. note::

   这些示例文件隐式假设使用 GNU 工具链，并且在至少一处假设目标是 ARMv7-M 平台。非 GNU 工具链可能需要显著不同的 Makefile 和链接器脚本。在创建链接器脚本的脚本（后文称为 ``mkdefines.sh``）中，至少有一处 ARMv7-M 特定的更改需要针对其他平台进行修改。

Hello 示例
=============

为了保持可控性，让我们使用一个具体的示例。假设我们要添加到发布代码中的 ELF 程序是简单的源文件 ``hello.c``：

.. code-block:: c

   #include <stdio.h>

   int main(int argc, char **argv)
   {
     printf("Hello from a fully linked Add-On Program!\n");
     return 0;
   }

假设我们有一个名为 ``addon`` 的目录，其中包含以下内容：

1. ``hello.c`` 源文件。
2. 用于构建 ELF 程序的 Makefile。
3. 导出包 ``nuttx-export-x.y.zip``。
4. 一个名为 ``mkdefines.sh`` 的 Bash 脚本，将创建第二个（``defines.ld``）链接器脚本。

构建 ELF 程序
========================

创建 ELF 程序的第一步是解压导出包。从 ``addon`` 目录开始：

.. code-block:: console

   $ cd addon
   $ ls
   hello.c Makefile mkdefines.sh nuttx-export-x.y.zip

其中：
- ``hello.c`` 是示例源文件。
- ``Makefile`` 构建 ELF 程序。
- ``mkdefines.h`` 是将创建充当符号表的链接器脚本的 Bash 脚本。
- ``nuttx-export-x.y.zip`` 是 NuttX 版本 ``x.y`` 的导出包。

解压导出包并重命名文件夹以便于使用：

.. code-block:: console

   $ unzip nuttx-export-x.y.zip
   $ mv nuttx-export-x.y nuttx-export

这将创建一个名为 ``nuttx-export`` 的新目录，其中包含构建 ELF 程序所需的已发布 NuttX 代码的所有内容。

Makefile
============

ELF 程序的创建很简单：

.. code-block:: console

   $ make

这使用以下 Makefile 生成多个文件：

- ``hello.o``：编译后的 ``hello.c`` 目标文件。
- ``hello.r``：仍有未定义符号的部分链接 ELF 对象。
- ``hello``：完全链接的、可重定位的 ELF 程序。
- ``linker.ld``：由 ``mkdefines.sh`` 创建的链接器脚本。

用于创建 ELF 程序的 Makefile 如下：

.. note::

   复制以下内容时，请记住 Makefile 缩进必须使用正确的制表符，而不仅仅是空格。

.. code-block:: makefile

   include nuttx-export/scripts/Make.defs

   # Long calls are needed to call from RAM into FLASH

   ARCHCFLAGS += -mlong-calls

   # You may want to check these options against the ones in "nuttx-export/scripts/Make.defs"

   ARCHWARNINGS = -Wall -Wstrict-prototypes -Wshadow -Wundef
   ARCHOPTIMIZATION = -Os -fno-strict-aliasing -fno-strength-reduce -fomit-frame-pointer
   ARCHINCLUDES = -I. -isystem nuttx-export/include

   CFLAGS = $(ARCHCFLAGS) $(ARCHWARNINGS) $(ARCHOPTIMIZATION) $(ARCHCPUFLAGS) $(ARCHINCLUDES) $(ARCHDEFINES) $(EXTRADEFINES)

   # Setup up linker command line options

   LDRELFLAGS = --relocatable

   LDELFFLAGS = --relocatable -e main
   LDELFFLAGS += -T defines.ld -T nuttx-export/scripts/gnu-elf.ld

   # This is the generated ELF program

   BIN = hello
   REL = hello.r

   # These are the source files that we use

   SRCS = hello.c
   OBJS = $(SRCS:.c=$(OBJEXT))

   # Build targets

   .PHONY: clean

   all: $(BIN)

   $(OBJS): %$(OBJEXT): %.c
      $(CC) -c $(CFLAGS) -o $@ $<

   System.map: nuttx-export/System.map
      cat nuttx-export/System.map | sed -e "s/\r//g" > System.map

   $(REL): $(OBJS)
      $(LD) $(LDRELFLAGS) -o $@ $<

   defines.ld: System.map $(REL)
      ./mkdefines.sh System.map "$(REL)" > defines.ld

   $(BIN): defines.ld $(REL)
      $(LD) $(LDELFFLAGS) -o $@ $(REL)
      $(STRIP) $@
      #$(CROSSDEV)objdump -f $@

   clean:
      rm -f $(BIN)
      rm -f $(REL)
      rm -f $(OBJS)
      rm -f defines.ld
      rm -f System.map

链接器脚本
=================

使用两个链接器脚本：主脚本 ``gnu-elf.ld`` 是普通文件，而 ``defines.ld`` 如下一节所述动态创建。

此示例中使用的主链接器脚本是导出的 NuttX 包中的：``nuttx-export/scripts/gnu-elf.ld``。

.. admonition:: 这是一个替代的最小（可能已过时）版本

   .. collapse:: 显示内容：

      .. code-block:: text

         SECTIONS
         {
         .text 0x00000000 :
            {
               _stext = . ;
               *(.text)
               *(.text.*)
               *(.gnu.warning)
               *(.stub)
               *(.glue_7)
               *(.glue_7t)
               *(.jcr)
               _etext = . ;
            }

         .rodata :
            {
               _srodata = . ;
               *(.rodata)
               *(.rodata1)
               *(.rodata.*)
               *(.gnu.linkonce.r*)
               _erodata = . ;
            }

         .data :
            {
               _sdata = . ;
               *(.data)
               *(.data1)
               *(.data.*)
               *(.gnu.linkonce.d*)
               _edata = . ;
            }

         .bss :
            {
               _sbss = . ;
               *(.bss)
               *(.bss.*)
               *(.sbss)
               *(.sbss.*)
               *(.gnu.linkonce.b*)
               *(COMMON)
               _ebss = . ;
            }

            /* Stabs debugging sections.    */

            .stab 0 : { *(.stab) }
            .stabstr 0 : { *(.stabstr) }
            .stab.excl 0 : { *(.stab.excl) }
            .stab.exclstr 0 : { *(.stab.exclstr) }
            .stab.index 0 : { *(.stab.index) }
            .stab.indexstr 0 : { *(.stab.indexstr) }
            .comment 0 : { *(.comment) }
            .debug_abbrev 0 : { *(.debug_abbrev) }
            .debug_info 0 : { *(.debug_info) }
            .debug_line 0 : { *(.debug_line) }
            .debug_pubnames 0 : { *(.debug_pubnames) }
            .debug_aranges 0 : { *(.debug_aranges) }
         }

创建 ``defines.ld`` 链接器脚本
=========================================

附加链接器脚本 ``defines.ld`` 通过三步过程创建：

1. Makefile 生成部分链接的 ELF 对象 ``hello.r``。
2. Makefile 然后调用 ``mkdefines.sh`` 脚本，该脚本生成 ``defines.ld`` 链接器脚本，为所有未定义符号提供值。
3. 最后，Makefile 使用 ``defines.ld`` 链接器脚本生成完全链接的、可重定位的 ``hello`` ELF 二进制文件。

以下是此示例中使用的 ``mkdefines.sh`` 脚本的内容：

.. code-block:: bash

   #!/bin/bash

   usage="Usage: $0 <system-map> <relprog>"

   # Check for the required path to the System.map file

   sysmap=$1
   if [ -z "$sysmap" ]; then
   echo "ERROR: Missing <system-map>"
   echo ""
   echo "$usage"
   exit 1
   fi

   # Check for the required partially linked file

   relprog=$2
   if [ -z "$relprog" ]; then
   echo "ERROR: Missing <program-list>"
   echo ""
   echo "$usage"
   exit 1
   fi

   # Verify the System.map and the partially linked file

   if [ ! -r "$sysmap" ]; then
   echo "ERROR:  $sysmap does not exist"
   echo ""
   echo "$usage"
   exit 1
   fi

   if [ ! -r "$relprog" ]; then
   echo "ERROR:  $relprog does not exist"
   echo ""
   echo "$usage"
   exit 1
   fi

   # Extract all of the undefined symbols from the partially linked file and create a
   # list of sorted, unique undefined variable names.

   varlist=$(nm "$relprog" | grep -F ' U ' | sed -e "s/^[ ]*//g" | cut -d' ' -f2 | sort - | uniq)

   # Now output the linker script that provides a value for all of the undefined symbols

   for var in $varlist; do
   map=$(grep " ${var}$" "${sysmap}")
   if [ -z "$map" ]; then
      echo "ERROR:  Variable $var not found in $sysmap"
      echo ""
      echo "$usage"
      exit 1
   fi

   varaddr=$(echo "${map}" | cut -d' ' -f1)
   echo "${var} = 0x${varaddr} | 0x00000001;"
   done

此脚本使用 ``nm`` 实用程序查找 ELF 二进制文件中的所有未定义符号，然后在固件构建时创建的 ``System.map`` 文件中搜索每个未定义符号的地址。最后，它使用符号的名称和地址创建每个符号表条目。

.. note::

   对于 ARMv7-M 架构，地址的第 0 位必须设置为 1 以指示 thumb 模式。如果您使用需要正常对齐地址的不同架构，您需要通过删除 OR 值来更改以下行：

   .. code-block:: shell

      echo "${var} = 0x${varaddr} | 0x00000001;"

.. note::

   如果新的 ELF 二进制文件使用了基础固件中未提供的符号（因此未包含在 ``System.map`` 文件中），此脚本将失败。在这种情况下，如果可能，您需要在 ELF 程序本身中提供缺失的逻辑。

.. important::

   此处描述的技术仅在 FLAT 构建模式下有效。它也可能通过将 ``User.map`` 替换为 ``System.map`` 扩展到 PROTECTED 模式下工作。

以下是 ``mkdefines.sh`` 创建的 ``defines.ld`` 脚本的简短示例：

.. code-block:: shell

   printf = 0x0800aefc | 0x00000001;

替换 NSH 内置函数
================================

可以通过在命令行中简单输入 ELF 程序的名称来从 NSH 执行文件，前提是满足以下要求：

1. 通过 ``CONFIG_NSH_FILE_APP=y`` 启用该功能。
2. 通过 ``CONFIG_LIBC_ENVPATH=y`` 启用 PATH 变量支持。
3. 可能包含 ELF 程序的文件系统的挂载点在 ``CONFIG_PATH_INITIAL`` 中设置。

假设，例如，已存在名为 ``hello`` 的内置应用程序。在将新的替换 ``hello`` ELF 程序安装到文件系统之前，这是 NSH 将执行的 ``hello`` 版本：

.. code-block:: text

   nsh> hello
   Hello, World!
   nsh>

现在假设我们将自定义 ``hello`` 二进制文件添加到适当路径内的文件系统中（参见上面的 ``CONFIG_PATH_INITIAL``）。当 NSH 尝试运行名为 ``hello`` 的程序时，它将优先使用文件系统上的新二进制文件，而不是同名程序的内置版本。

.. code-block:: text

   nsh> mount -t vfat /dev/mmcsd0 /bin
   nsh> hello
   Hello from a fully linked Add-On Program!
   nsh>

版本依赖
==================

.. warning::

   此技术使用版本化发布的 ``System.map`` 文件中的固定地址生成 ELF 程序。生成的 ELF 程序只能与该特定固件版本一起使用。如果与不同的固件版本一起使用，很可能会发生崩溃，因为 ``System.map`` 中的地址将不匹配。

使用 :doc:`符号表 <partially_linked_elf>` 的替代方法或多或少是版本无关的。

紧耦合内存
========================

大多数基于 ARMv7-M 系列处理器的 MCU 支持某种紧耦合内存 (TCM)。这些 TCM 对于专门的操作具有一些不同的属性。根据处理器的总线矩阵，您可能无法从 TCM 执行程序。例如，STM32F4 支持核心耦合内存 (CCM)，
