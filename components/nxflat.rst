.. _nxflat:

======
NXFLAT
======

Overview
========

Functionality
-------------

NXFLAT 是几年前实现的一种称为 `XFLAT <http://xflat.sourceforge.net/>`__ 的二进制格式的定制和简化版本。使用 NXFLAT 二进制格式，你将能够执行以下操作：

  - 将单独链接的程序放置在文件系统中，以及
  - 通过将这些程序动态链接到基础 NuttX 代码来执行它们。

这允许你在 NuttX 基础代码写入 FLASH 后对其进行扩展。实现 NXFLAT 的一个动机是支持 HTTPD 服务器下的干净 CGI。

当与 NuttX ROMFS 支持结合使用时，此功能特别有吸引力：ROMFS 允许你在 FLASH 中就地执行程序 (XIP)，除了将 .data 段复制到 RAM 外，无需复制任何其他内容。事实上，最初的 NXFLAT 版本仅适用于 ROMFS。后来的扩展也支持从 SRAM 副本执行 NXFLAT 二进制文件。

此 NuttX 功能包括：

  - 构建到 NuttX 内核中的动态加载器（参见 `GIT <https://github.com/apache/nuttx/blob/master/binfmt/>`__）。
  - 对 RTOS 的轻微更改以支持位置无关代码，以及
  - 用于绑定 ELF 二进制文件以产生 NXFLAT 二进制格式的链接器（参见 GIT）。

Background
----------

NXFLAT 源自 `XFLAT <http://xflat.sourceforge.net/>`__。XFLAT 是一个工具链附加组件，为没有内存管理单元 (MMU:sup:`1`) 的处理器提供完整的共享库和 XIP 可执行文件支持。NXFLAT 针对 NuttX 所面向的深度嵌入式环境进行了大幅简化：

  - NXFLAT 不支持共享库，因为
  - NXFLAT 不支持从模块 *导出* 符号值

相反，NXFLAT 模块只 *导入* 符号值。在 NXFLAT 模型中，(PIC:sup:`2`) NXFLAT 模块驻留在 FLASH 文件系统中，当它在运行时被加载时，它只被动态链接到（非 PIC 的）基础 NuttX 代码：基础 NuttX *导出* 符号表；NXFLAT 模块 *导入* 这些符号值以将模块动态绑定到基础代码。

Limitations
-----------

  - **仅限 ROMFS（或 RAM 映射）**：
    当前的 NXFLAT 版本仅适用于 (1) 驻留在 ROMFS 文件系统上的 NXFLAT 可执行模块，或 (2) 定义了 CONFIG_FS_RAMMAP 时驻留在其他文件系统上的可执行文件。此限制是因为加载器依赖于 mmap() 代码段的能力。有关更多信息，请参阅 NuttX 用户指南。

    NUTTX 不提供任何通用的文件映射功能。事实上，真正的文件映射仅在提供 MMU1 的 MCU 上才有可能。如果没有 MMU，文件系统可以支持就地执行 (XIP) 来模拟文件映射。只有 ROMFS 文件系统支持 NXFLAT 所需的那种 XIP 执行。

    也可以通过分配内存、将 NXFLAT 二进制文件复制到内存中，并在 RAM 中的可执行文件副本上执行来模拟文件映射。此功能可以通过 CONFIG_FS_RAMMAP 配置选项启用。启用该选项后，NXFLAT 将与那种文件系统一起工作，但需要将所有 NXFLAT 可执行文件复制到 RAM。

  - **仅限 GCC/ARM/Cortex-M3/4**：
    目前，NXFLAT 工具链仅适用于 ARM 和 Cortex-M3/4 (thumb2) 目标。

  - **RAM 中的只读数据**：
    使用较旧的 GCC 编译器（至少到 4.3.3），只读数据必须驻留在 RAM 中。在 GCC 生成的代码中，所有数据引用都通过 PIC2 基址寄存器（通常是 ARM 处理器的 R10 或 sl）索引。这包括只读数据 (.rodata)。嵌入式固件开发人员通常希望将 .rodata 与代码段一起保留在 FLASH 中。但由于所有数据都使用 PIC 基址寄存器引用，所有这些数据必须位于 RAM 中。正在研究一种 NXFLAT 更改来解决此问题3。

    较新的 GCC 编译器（至少从 4.6.3 开始），只读数据不再是 GOT 相对的，而是现在通过 PC 相对寻址访问。使用 PC 相对寻址，只读数据必须驻留在 I-Space 中。

  - **全局作用域函数指针**：
    如果对静态定义的函数取函数指针，那么（至少对于 ARM）GCC 将生成 NXFLAT 无法处理的重定位。解决方法是使所有此类函数具有全局作用域。修复将涉及对 GCC 编译器的更改，如附录 B 所述。

  - **回调的特殊处理**：
    必须避免通过函数指针的回调，或者当无法避免时，需要非常特殊地处理。原因是 PIC 模块需要在 PIC 寄存器中设置特殊值。如果回调没有设置 PIC 寄存器，那么回调的函数将失败，因为它将无法正确访问数据内存。某些 NuttX 回调有特殊逻辑来处理：信号回调和看门狗定时器回调。但其他回调（如那些用于 qsort() 的回调）必须在 NXFLAT 模块中避免使用。

Supported Processors
--------------------

如上所述，NXFLAT 工具链仅适用于 ARM 和 Cortex-M3 (thumb2) 目标。此外，NXFLAT 仅在 Eagle-100 LMS6918 Cortex-M3 板上进行了测试。

Development Status
------------------

NXFLAT 的初始版本在 NuttX 版本 0.4.9 中发布。测试仅限于源代码树中 ``apps/examples/nxflat`` 下的测试。存在一些已知问题（参见 `TODO <https://github.com/apache/nuttx/blob/master/TODO>`__ 列表）。因此，NXFLAT 目前处于早期 alpha 阶段。

NXFLAT Toolchain
================

Building the NXFLAT Toolchain
-----------------------------

为了使用 NXFLAT，你必须使用特殊的 NXFLAT 工具在 FLASH 中创建二进制模块。为此，你需要下载 buildroot 包并在你的 Linux 或 Cygwin 机器上构建它。buildroot 可以从 `Bitbucket.org <https://bitbucket.org/nuttx/buildroot/downloads>`__ 下载。你需要版本 0.1.7 或更高版本。

以下是一些通用构建说明：

-  你必须已在 ``<some-dir>/nuttx`` 中配置了 NuttX
-  将 buildroot 包 ``buildroot-0.x.y`` 下载到 ``<some-dir>``
-  使用类似 ``tar zxf buildroot-0.x.y`` 的命令解压 ``<some-dir>/buildroot-0.x.y.tar.gz``。这将产生一个类似 ``<some-dir>/buildroot-0.x.y`` 的新目录
-  将其移动到位：
   ``mv <some-dir>/buildroot-0.x.y``\\ <some-dir>/buildroot
-  ``cd``\\ <some-dir>/buildroot
-  将配置文件复制到顶层 buildroot 目录：
   ``cp boards/abc-defconfig-x.y.z .config``。
-  通过 ``make menuconfig`` 启用 NXFLAT 工具的构建。选择使用 GCC 构建 NXFLAT 工具链（你也可以选择省略构建 GCC，仅为自己的 GCC 工具链构建 NXFLAT 工具链）。
-  制作工具链：``make``。当 make 完成后，工具二进制文件将在 ``<some-dir>/buildroot/build_abc/staging_dir/bin`` 下可用

mknxflat
--------

``mknxflat`` 用于构建 *thunk* 文件。用法如下::

  Usage: mknxflat [options] <bfd-filename>

  Where options are one or more of the following.  Note
  that a space is always required between the option and
  any following arguments.

    -d Use dynamic symbol table. [symtab]
    -f <cmd-filename>
        Take next commands from <cmd-filename> [cmd-line]
    -o <out-filename>
       Output to  [stdout]
    -v Verbose output [no output]
    -w Import weakly declared functions, i.e., weakly
       declared functions are expected to be provided at
       load-time [not imported]

ldnxflat
--------

``ldnxflat`` 用于将你的目标文件与 ``mknxflat`` 生成的 *thunk* 文件链接以产生 NXFLAT 二进制模块。用法如下::

  Usage: ldnxflat [options] <bfd-filename>

  Where options are one or more of the following.  Note
  that a space is always required between the option and
  any following arguments.

    -d Use dynamic symbol table [Default: symtab]
    -e <entry-point>
       Entry point to module [Default: _start]
    -o <out-filename>
       Output to <out-filename> [Default: <bfd-filename>.nxf]
    -s <stack-size>
       Set stack size to <stack-size> [Default: 4096]
    -v Verbose output. If -v is applied twice, additional
       debug output is enabled [Default: no verbose output].

mksymtab
--------

``nuttx/tools`` 中有一个名为 ``mksymtab`` 的小型辅助程序。``mksymtab`` 可用于为典型 NXFLAT 应用程序可用的 NuttX 基础代码生成符号表。``mksymtab`` 从逗号分隔值 (CSV) 文件构建符号表。特别是以下 CSV 文件：

  #. ``nuttx/syscall/syscall.csv`` 描述 NuttX RTOS 接口，以及
  #. ``nuttx/libc/libc.csv`` 描述 NuttX C 库接口。
  #. ``nuttx/libc/math.cvs`` 描述任何数学库。

::

  USAGE: ./mksymtab <cvs-file> <symtab-file>

  Where:

    <cvs-file>   : The path to the input CSV file
    <symtab-file>: The path to the output symbol table file
    -d           : Enable debug output

例如，

::

  cd nuttx/tools
  cat ../syscall/syscall.csv ../libc/libc.csv | sort >tmp.csv
  ./mksymtab.exe tmp.csv tmp.c

Making an NXFLAT module
-----------------------

以下是 NXFLAT makefile 的片段（简化自 NuttX `Hello, World! <https://github.com/apache/nuttx-apps/blob/master/examples/nxflat/tests/hello/Makefile>`__ 示例）。

* 目标 1：

  .. code-block:: makefile

    hello.r1: hello.o
      abc-nuttx-elf-ld -r -d -warn-common -o $@ $^

* 目标 2：

  .. code-block:: makefile

    hello-thunk.S: hello.r1
      mknxflat -o $@ $^

* 目标 3：

  .. code-block:: makefile

    hello.r2: hello-thunk.S
      abc-nuttx-elf-ld -r -d -warn-common -T binfmt/libnxflat/gnu-nxflat-gotoff.ld -no-check-sections -o $@ hello.o hello-thunk.o

* 目标 4：

  .. code-block:: makefile

    hello: hello.r2
      ldnxflat -e main -s 2048 -o $@ $^

**目标 1**。此目标将模块的所有目标文件链接在一起形成一个可重定位目标。将生成两个可重定位目标；这是第一个（因此后缀为 ``.r1``）。在这个"Hello, World!"示例中，只有一个目标文件 ``hello.o``，被链接以产生 ``hello.r1`` 目标。

当模块的目标文件被编译时，必须提供一些特殊的编译器 CFLAGS。首先，选项 ``-fpic`` 是必需的，用于告诉编译器生成位置无关代码（其他 GCC 选项，如 ``-fno-jump-tables`` 也可能需要）。对于 ARM 编译器，还需要两个额外的编译选项：``-msingle-pic-base`` 和 ``-mpic-register=r10``。

**目标 2**。给定 ``hello.r1`` 可重定位目标，此目标将调用 `mknxflat <#mknxflat>`__ 来制作 *thunk* 文件 ``hello-thunk.S``。此 *thunk* 文件包含创建导入函数列表所需的所有信息。

**目标 3**。此目标类似于 **目标 1**。在这种情况下，它将模块的目标文件（这里只有 ``hello.o``）与汇编的 *thunk* 文件 ``hello-thunk.o`` 链接在一起以创建第二个可重定位目标 ``hello.r2``。链接脚本 ``gnu-nxflat-gotoff.ld`` 在此点是必需的，用于正确定位各段。此链接脚本生成两个段：一个 *I-Space*（指令空间）段，主要包含 ``.text``；一个 *D-Space*（数据空间）段，包含 ``.got``、``.data`` 和 ``.bss`` 段。I-Space 段必须起始于地址 0（这样段的地址实际上是 I-Space 段内的偏移量），D-Space 段也必须起始于地址 0（这样段的地址实际上是 I-Space 段内的偏移量）。选项 ``-no-check-sections`` 是必需的，以防止链接器因为这些段重叠而失败。

**注意：** 有两个链接脚本位于 ``binfmt/libnxflat/``。

  #. ``binfmt/libnxflat/gnu-nxflat-gotoff.ld``。较旧版本的 GCC（至少到 GCC 4.3.3）使用 GOT 相对寻址来访问 RO 数据。在这种情况下，只读数据 (.rodata) 必须驻留在 D-Space 中，应使用此链接脚本。
  #. ``binfmt/libnxflat/gnu-nxflat-pcrel.ld``。较新版本的 GCC（至少从 GCC 4.6.3 开始）使用 PC 相对寻址来访问 RO 数据。在这种情况下，只读数据 (.rodata) 必须驻留在 I-Space 中，应使用此链接脚本。

**目标 4**。最后，此目标将使用 ``hello.r2`` 可重定位目标，通过执行 ``ldnxflat`` 来创建最终的 NXFLAT 模块 ``hello``。

**binfmt 注册**。NXFLAT 调用 :c:func:`register_binfmt` 将自身纳入系统。

Appendix A: No GOT Operation
============================

当 GCC 生成位置无关代码时，新的代码段将出现在你的程序中。其中之一是 GOT（全局偏移表），在 ELF 环境中，另一个是 PLT（过程查找表）。例如，如果你的 C 代码在没有 PIC 的情况下生成了如下（ARM）汇编语言：

.. code-block:: asm

          ldr     r1, .L0         /* Fetch the offset to 'x' */
          ldr     r0, [r10, r1]   /* Load the value of 'x' with PIC offset */
          /* ... */
  .L0:    .word   x               /* Offset to 'x' */

那么当启用 PIC 时（例如使用 -fpic 编译器选项），它将生成如下代码：

.. code-block:: asm

          ldr     r1, .L0         /* Fetch the offset to the GOT entry */
          ldr     r1, [r10, r1]   /* Fetch the (relocated) address of 'x' from the GOT */
          ldr     r0, [r1, #0]    /* Fetch the value of 'x' */
          /* ... */
  .L1     .word   x(GOT)          /* Offset to entry in the GOT */

参见 `reference <http://xflat.sourceforge.net/NoMMUSharedLibs.html#shlibsgot>`__

注意，这通过 GOT 生成了一层额外的间接寻址。此间接寻址对 NXFLAT 来说是不必要的，只会增加 RAM 使用和执行时间。

NXFLAT（像 `XFLAT <http://xflat.sourceforge.net/>`__ 一样）在没有 GOT 的情况下可以工作得更好。存在针对较旧版本 GCC 的补丁来消除 GOT 间接寻址。如果你有灵感将它们移植到新 GCC 版本，可以在 `here <http://xflat.cvs.sourceforge.net/viewvc/xflat/xflat/gcc/>`__ 找到几个补丁。

Appendix B: PIC Text Workaround
================================

GCC 中的内存模型存在问题，阻止了在 NXFLAT 上下文中按需使用它。问题是 GCC PIC 模型假定可执行文件位于平坦、连续的（虚拟）地址空间中，如::

  Virtual
  .text
  .got
  .data
  .bss

它假定 PIC 基址寄存器（对于 ARM 通常是 r10）指向 ``.text`` 的基址，这样 ``.text``、``.got``、``.data``、``.bss`` 中的任何地址都可以通过与同一基址的偏移量找到。但这不是我们在 XIP 嵌入式环境中需要的内存布局。我们需要两个内存区域，一个在 FLASH 中包含共享代码，另一个在 RAM 中按任务包含任务特定数据::

  Flash\t  RAM
  .text   .got
          .data
          .bss

PIC 基址寄存器需要指向 ``.got`` 的基址，只有 ``.got``、``.data`` 和 ``.bss`` 段中的地址可以作为 PIC 基址寄存器的偏移量来访问。另请参阅此 `XFLAT 讨论 <http://xflat.cvs.sourceforge.net/viewvc/*checkout*/xflat/xflat/gcc/README?revision=1.1.1.1>`__。

存在针对较旧版本 GCC 的补丁来纠正此 GCC 行为。如果你有灵感将它们移植到新 GCC 版本，可以在 `here <http://xflat.cvs.sourceforge.net/viewvc/xflat/xflat/gcc/>`__ 找到几个补丁。
