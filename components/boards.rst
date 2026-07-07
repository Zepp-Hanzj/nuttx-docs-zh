==============
Boards Support
==============

本页面讨论 NuttX 的板级支持逻辑。

``nuttx/boards`` 目录是内部操作系统的一部分。它应仅包含操作系统启动逻辑和驱动初始化逻辑。

**此目录中不应包含任何应用可调用的逻辑。**

如果你有板级特定的、应用可调用的逻辑，该逻辑不应放在这里。请考虑使用 ``apps/platform`` 下的子目录代替。

Board-Specific Configurations
=============================

NuttX 配置由以下部分组成：

* 处理器架构特定文件。这些文件包含在 ``arch/<arch>/`` 目录中。

* 芯片/SoC 特定文件。每种处理器架构都嵌入在芯片或片上系统 (SoC) 架构中。完整的芯片架构包括处理器架构加上芯片特定的中断逻辑、通用 I/O (GIO) 逻辑以及专用的内部外设（如 UART、USB 等）。

  这些芯片特定文件包含在 ``arch/<arch>/`` 目录中的芯片特定子目录中，并通过 ``CONFIG_ARCH_name`` 选择来选择。

* 板级特定文件。为了可使用，芯片必须包含在板级环境中。板级配置定义了板的附加属性，包括外围 LED、外部外设（如网络、USB 等）。

  这些板级特定配置文件可以在 ``boards/<arch>/<chip>/<board>/`` 子目录中找到。附加配置信息可在板级特定文档页面 ``Documentation/platforms/<arch>/<chip>/<board>`` 中获取。

``boards/`` 子目录包含每个板的配置数据。这些板级特定配置加上 ``arch/`` 子目录中的架构特定配置完全定义了 NuttX 的定制移植。

``boards/`` Directory Structure
===============================

``boards/`` 目录包含板级特定配置逻辑。每个板必须在 ``boards/`` 下提供一个 ``<board>`` 子目录，具有以下特征::

  <board>
  |-- include/
  |   `-- (board-specific header files)
  |-- src/
  |   |-- Makefile
  |   `-- (board-specific source files)
  |-- <config1-dir>
  |   |-- Make.defs
  |   `-- defconfig
  |-- <config2-dir>
  |   |-- Make.defs
  |   `-- defconfig
  ...

Summary of Files
================

* ``include/`` -- 此目录包含板级特定头文件。此目录将在配置时被链接为 include/arch/board，并可通过 ``#include <arch/board/header.h>`` 来包含。这些头文件只能被 ``arch/<arch>/include/`` 和 ``arch/<arch>/src`` 中的文件包含。

* ``src/`` -- 此目录包含板级特定驱动。此目录将在配置时被链接为 ``arch/<arch>/src/board``，并集成到构建系统中。

* ``src/Makefile`` -- 此 makefile 将被调用以构建板级特定驱动。它必须支持以下目标：``libext$(LIBEXT)``、``clean`` 和 ``distclean``。

一个板可以使用这些公共源文件拥有多种不同的配置。每个板配置由两个文件描述：Make.defs 和 defconfig。通常，每组配置文件保存在单独的配置子目录中（上图中的 ``<config1-dir>``、``<config2-dir>`` 等）。

* ``Make.defs`` -- 此 makefile 片段提供架构和工具特定的构建选项。它将被构建中的所有其他 makefile 包含（安装后）。此 make 片段应定义::

    Tools: CC, LD, AR, NM, OBJCOPY, OBJDUMP
    Tool options: CFLAGS, LDFLAGS

  当此 makefile 片段运行时，它将被传入 TOPDIR，即构建根目录的路径。此 makefile 片段应包含::

    $(TOPDIR)/.config          : NuttX configuration
    $(TOPDIR)/tools/Config.mk  : Common definitions

  ``Make.defs`` 文件中的定义可能依赖于 ``.config`` 文件中的某些设置。例如，如果 ``CONFIG_DEBUG_FEATURES=y``，``CFLAGS`` 很可能会不同。

  包含的 ``tools/Config.mk`` 文件包含附加定义，可在架构特定的 ``Make.defs`` 文件中根据需要覆盖::

    COMPILE, ASSEMBLE, ARCHIVE, CLEAN, and MKDEP macros

* ``defconfig`` -- 这是一个类似 Linux 配置文件的配置文件。它包含变量/值对，如::

    CONFIG_VARIABLE=value

  此配置文件将在构建时使用：

    (1) 作为 makefile 片段包含在其他 makefile 中，以及
    (2) 用于生成 include/nuttx/config.h，该头文件被系统中的大多数 C 文件包含。

Configuration Variables
=======================

此前，本节提供了所有 NuttX 配置变量的列表。然而，NuttX 已经转换为使用 kconfig-frontends 工具（参见 https://bitbucket.org/nuttx/tools/src/master/kconfig-frontends/）。现在，NuttX 配置由一组自文档化的 Kconfig 文件确定。

当前的 NuttX 配置变量也在单独的、自动生成的配置变量文档中记录。该配置变量文档使用 nuttx/tools 目录中的 kconfig2html 工具生成。该工具分析 NuttX Kconfig 文件并生成一个详尽的 HTML 文档。

最新的配置变量文档可以随时使用该工具重新生成，或者更恰当地说，使用 nuttx/tools/mkconfigvars.sh 中的包装脚本。该脚本将生成文件 nuttx/Documentation/NuttXConfigVariables.html。

Supported Boards
================

支持的板列表可以在 :ref:`Supported Platforms <platforms>` 中找到。

Configuring NuttX
=================

配置 NuttX 只需复制::

  boards/<arch>/<chip>/<board>/<config-dir>/Make.def to ${TOPDIR}/Make.defs
  boards/<arch>/<chip>/<board>/<config-dir>/defconfig to ${TOPDIR}/.config

- ``tools/configure.sh``

  有一个脚本可以自动化这些步骤。以下步骤将完成相同的配置::

   tools/configure.sh <board>:<config-dir>

  还有一个替代的 Windows 批处理文件可以在 Windows 原生环境中使用，如::

    tools\configure.bat <board>:<config-dir>

  有关这些脚本的更多信息，请参阅 :doc:`tools/index`。

  如果你的应用程序目录不在标准位置（``../apps`` 或 ``../apps-<version>``），那么你还应该在命令行上指定应用程序目录的位置，如::

    cd tools
    ./configure.sh -a <app-dir> <board>:<config-dir>


Adding a New Board Configuration
================================

好的，你已经创建了一个新的板级配置目录。现在，如何将这个板挂接到配置系统中，以便可以通过 ``make menuconfig`` 来选择它？

你需要修改 ``boards/Kconfig`` 文件。让我们看一下 ``Kconfig`` 文件中的 STM32F4-Discovery 配置，了解如何将新的板级目录添加到配置中。对于此配置，假设你的新板位于 ``boards/myarch/mychip/myboard`` 目录中；它使用通过 ``CONFIG_ARCH_CHIP_MYMCU`` 选择的 MCU；你希望该板通过 ``CONFIG_ARCH_BOARD_MYBOARD`` 来选择。那么你可以按照以下方式克隆 ``boards/Kconfig`` 中的 STM32F4-Discovery 配置来支持你的新板配置。

在 ``boards/Kconfig`` 中的 stm32f4-discovery 部分，你会看到类似这样的配置定义：

上述内容选择了 STM32F4-Discovery 板。``select`` 行表明该板同时具有 LED 和按键，并且该板可以通过按键按下产生中断。你只需将上述配置定义复制到新位置（注意配置按字母顺序排列）。然后你应该编辑配置以支持你的板。最终的配置定义可能类似：

在 ``boards/Kconfig`` 文件后面，你会看到一个很长的字符串配置，带有很多默认值，如：

此逻辑将为一个名为 ``CONFIG_ARCH_BOARD`` 的配置变量分配字符串值，该变量将命名板级特定文件所在的目录。在我们的例子中，这些文件位于 ``boards/myarch/mychip/myboard``，我们在默认值的长列表中添加以下内容（再次按字母顺序）：

现在构建系统知道在哪里找到你的板级配置了！

最后，在 ``boards/myarch/mychip/myboard`` 附近添加类似这样的内容：

这将在 ``boards/myarch/mychip/myboard/Kconfig`` 中包含附加的板级特定配置变量定义。

Building Symbol Tables
======================

符号表在多个 binfmt 接口中是必需的，以便将模块绑定到基础代码。这些符号表可能很难创建，并且可能需要针对任何特定应用程序进行定制，在符号数量和符号表大小与应用程序所需的符号之间取得平衡。

顶层 System.map 文件是符号信息的一个好来源（当然，它只是使用 GNU 'nm' 工具从顶层 nuttx 文件生成的）。

源代码中还有逗号分隔值 (CSV) 文件提供符号信息。特别是::

  nuttx/syscall/syscall.csv - 描述 NuttX RTOS 接口，以及
  nuttx/lib/libc.csv        - 描述 NuttX C 库接口。

nuttx/tools/mksymtab 中有一个工具，它使用这些 CSV 文件作为输入来生成通用符号表。有关使用 mksymtab 工具的更多信息，请参阅 ``nuttx/tools/README.txt``。
