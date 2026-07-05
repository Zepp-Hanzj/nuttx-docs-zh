=================
Make 构建系统
=================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

目前，NuttX 同时支持 CMake 和 Make 构建系统。
本指南介绍 NuttX 基于 ``make`` 的构建系统。

由于*需求、约束和构建过程的复杂性*，NuttX 将此工作分为多个文件，每个文件处理构建过程的特定部分。

如 :doc:`/introduction/inviolables` 中所述，应支持多个平台：

- :ref:`win_mk`：处理 Windows 平台支持。
- :ref:`unix_mk`：处理类 Unix 平台支持。

NuttX 支持多种构建模式。参见 :doc:`/guides/protected_build`：

- :ref:`flatlibs_mk`：内核和用户空间构建为单个 ``blob``。
- :ref:`protectedlibs_mk`：内核和用户空间构建为两个独立的 ``blob``。
- :ref:`kernelibs_mk`：内核构建为单个 ``blob``。用户应用程序必须加载到内存中执行。

NuttX 目标为多个库或 ``silo``，每个处理自己的编译：

.. note::

  Gregory Nutt 有一个很好的关于
  `NuttX 架构 <https://cwiki.apache.org/confluence/pages/viewpage.action?
  pageId=139629399&preview=/139629402/140774623/nuttx-3-archoverview.pdf>`_ 的演示。

  其中解释了 ``silo`` 概念。下面列出的只是那些 silo 作为库。
  构建模式影响所需的库。

.. code-block:: console

  $ ls -l staging/
  drwxr-xr-x  2 xxx xxx    4096 Oct  6 16:02 .
  drwxr-xr-x 27 xxx xxx    4096 Oct  6 16:02 ..
  -rw-r--r--  1 xxx xxx  323640 Oct  6 16:02 libapps.a
  -rw-r--r--  1 xxx xxx  384352 Oct  6 16:02 libarch.a
  -rw-r--r--  1 xxx xxx   62182 Oct  6 16:02 libbinfmt.a
  -rw-r--r--  1 xxx xxx    6468 Oct  6 16:01 libboards.a
  -rw-r--r--  1 xxx xxx 2820054 Oct  6 16:02 libc.a
  -rw-r--r--  1 xxx xxx  161486 Oct  6 16:01 libdrivers.a
  -rw-r--r--  1 xxx xxx  981638 Oct  6 16:02 libfs.a
  -rw-r--r--  1 xxx xxx  224446 Oct  6 16:02 libmm.a
  -rw-r--r--  1 xxx xxx 2435746 Oct  6 16:01 libsched.a
  -rw-r--r--  1 xxx xxx   51768 Oct  6 16:02 libxx.a

.. _verbosity:

详细程度
---------

``V`` 变量可以传递给 ``make`` 以控制构建详细程度。

- **安静（默认）：** 构建输出是最小的。
- **详细（`V=1 V=2`）：** 显示完整的编译器命令*（启用命令回显）*。
- **工具详细（`V=2`）：** 启用工具和脚本的详细输出。

.. code-block:: console

  # V=1,2：启用命令回显
  $ make V=1

  # V=2：   启用工具和脚本中的调试/详细选项
  $ make V=2

构建过程
-------------

.. note::

	保持配置步骤和板级文件夹布局简短。
	应创建单独的文档。

基于 ``Make`` 的构建过程从 NuttX 树配置开始。
这是通过运行 ``tools/configure.sh`` 脚本完成的。
配置步骤准备 NuttX 内核树，设置特定于板级的 arch、chip 和 board 文件。

``Make`` 构建系统使用*通用*命名来引用所需的子系统：

- *当前*架构称为 ``arch``
- *当前*芯片称为 ``chip``
- *当前*板称为 ``board``

这些*通用*名称通过符号链接映射到*实际*名称：

- *当前*芯片目录被符号链接到 ``nutt/include/arch/chip``。
- *当前*板目录被符号链接到 ``nutt/include/arch/board``。
- *当前*架构目录被符号链接到 ``nutt/include/arch``。

板配置存储为 ``defconfig`` 文件，这是一个最小配置，只存储与默认配置值不同的配置。
由于 NuttX 对 ``app`` 目录的严格依赖的特殊性，``.config`` 文件不是由 ``kconfiglib`` 或 ``kconfig-frontends`` 生成的，而是由树内的 ``tools/process_config.sh`` 脚本生成的。此脚本接受"基础"输入文件（板的 ``defconfig`` 文件）、额外的包含路径（最相关的是 ``apps`` 顶级目录），并生成输出文件（``$(TOPDIR)/.config`` 文件）。

.. code-block:: console

  # configure.sh shell 脚本的一部分，从第 240 行开始
  #
  # src_config=${configpath}/defconfig
  # dest_config="${TOPDIR}/.config"
  # original_config="${TOPDIR}/.config.orig"
  # backup_config="${TOPDIR}/defconfig"

  $ ln -sf ${src_makedefs} ${dest_makedefs} || \
    { echo "Failed to symlink ${src_makedefs}" ; exit 8 ; }
  $ ${TOPDIR}/tools/process_config.sh -I ${configpath}/../../common/configs \
    -I ${configpath}/../common \
    -I ${configpath} -I ${TOPDIR}/../apps \
    -I ${TOPDIR}/../nuttx-apps \
    -o ${dest_config} ${src_config}

启动构建
^^^^^^^^^^^^^^^^^^

根 **Makefile** 是构建过程的入口点。它的主要工作是检查 ``.config`` 文件并包含适当的**特定于主机的 Makefile**。构建过程的"实际"第一步由特定于主机的 **Makefile**（``Win.mk`` 或 ``Unix.mk``）处理。

在解析的早期，两个特定于主机的 **Makefile** 也将包含

- 上面提到的板的 ``Make.defs`` 文件。这还将包含

  - 主 ``.config`` 文件。
  - 工具 ``config.mk`` 文件。
  - 架构 ``toolchain.defs`` 文件。

- 基于构建模式，以下文件之一：

  - :ref:`flatlibs_mk`
  - :ref:`protectedlibs_mk`
  - :ref:`kernelibs_mk`

- :ref:`directories_mk`

内置依赖机制
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

  :ref:`mkdeps` 的文档应该扩展。缺少很多细节。
  这里部分文档应该被移动。

NuttX 实现了内置的依赖机制。参见 :ref:`mkdeps`。
此机制使用 ``gcc`` 生成类似 ``*.d`` 的依赖文件，这些文件可以被 **Makefile** 包含以跟踪文件依赖关系。
此机制由 ``depend`` 目标启动，并根据构建模式定位 NuttX 树中的特定目录。它被 ``pass1dep`` 和 ``pass2dep`` *需要*。

.. code-block:: makefile

  pass1dep: context tools/mkdeps$(HOSTEXEEXT) tools/cnvwindeps$(HOSTEXEEXT)
  	$(Q) for dir in $(USERDEPDIRS) ; do \
  	  $(MAKE) -C $$dir depend || exit; \
  	done
  pass2dep: context tools/mkdeps$(HOSTEXEEXT) tools/cnvwindeps$(HOSTEXEEXT)
  	$(Q) for dir in $(KERNDEPDIRS) ; do \
  	  $(MAKE) -C $$dir EXTRAFLAGS="$(KDEFINE) $(EXTRAFLAGS)" depend || exit; \
  	done

``pass1dep`` 和 ``pass2dep`` 设置不同的目录和运行 ``depend`` 目标的顺序。参见 :ref:`directories_mk`。

构建 NuttX 库
^^^^^^^^^^^^^^^^^^^

特定于主机的 **Makefile** 不会构建所需的 NuttX 库。它将通过在 ``$(USERLIBS)`` 和 ``$(NUTTXLIBS)`` 变量中列出的每个目录中"递归"调用 make 来延迟工作。

pass1 和 pass2
^^^^^^^^^^^^^^^^^^^^^^^^^

NuttX 二进制文件始终通过运行 ``pass1`` 和 ``pass2`` 目标生成。上述目标的实际依赖关系可能因构建模式而异。

不同的 NuttX 构建模式不会影响 ``pass1`` 和 ``pass2`` 目标的"执行"，而是会影响这些目标拉取的依赖关系。

- ``pass1`` 目标依赖于 ``$(USERLIBS)``。
- ``pass2`` 目标依赖于 ``$(NUTTXLIBS)``。

.. code-block:: makefile

  all: pass1 pass2

  pass1: $(USERLIBS)
  pass2: $(NUTTXLIBS)

``$(USERLIBS)`` 和 ``$(NUTTXLIBS)`` 变量的内容在每个构建模式 makefile 中定义。参见上面的 :ref:`build_modes`。

暂存库
^^^^^^^^^^^^^^^^

在前一步中编译由 ``$(USERLIBS)`` 和 ``$(NUTTXLIBS)`` 定义的库后，``make`` 构建系统将把它们 ``install`` 到位于 NuttX 树根的特殊 ``staging/`` 目录中。

这些库被传递给最终目标规则（``$(BIN)``）。

.. code-block:: makefile

  # Unix.mk：第 536 行
  $(BIN): pass1 pass2
  # ...
  	$(Q) $(MAKE) -C $(ARCH_SRC) EXTRA_OBJS="$(EXTRA_OBJS)" LINKLIBS="$(LINKLIBS)" APPDIR="$(APPDIR)" EXTRAFLAGS="$(KDEFINE) $(EXTRAFLAGS)" $(BIN)
  # ...

.. _win_mk:

Win.mk
------

尽管针对不同的平台，**Win.mk** 和 **Unix.mk** 都旨在产生相同的输出。需要独立文件的原因是平台方法的差异。

正斜杠与反斜杠
^^^^^^^^^^^^^^^^^^^^^^^

主要区别之一是在类 Unix 平台上使用正斜杠（``/``）而在 Windows 上使用反斜杠（``\\``）

${HOSTEXEEXT} ${HOSTDYNEXT}
^^^^^^^^^^^^^^^^^^^^^^^^^^^

这些变量被构建系统用来配置平台所需的可执行文件后缀。它们在 :ref:`config_mk` 中定义。

对于 Windows 平台：

- ``${HOSTEXEEXT}`` 设置为 ``.exe``。
- ``${HOSTDYNEXT}`` 设置为 ``.dll``。

符号链接
^^^^^^^^^^^^^^^^

对于 Windows 平台，构建系统以不同的方式处理符号链接。

.. _unix_mk:

Unix.mk
-------

版本控制
^^^^^^^^^^

如果 NuttX 作为仓库克隆，构建系统将影响版本控制。参见 :ref:`versioning`。

config.h、.config、mkconfig
^^^^^^^^^^^^^^^^^^^^^^^^^^^

NuttX 的构建系统将 ``config.h`` 的生成延迟到一个名为 ``mkconfig`` 的单独工具。参见 :ref:`makefile_host`。

.. code-block:: makefile

  tools/mkconfig$(HOSTEXEEXT): prebuild
	    $(Q) $(MAKE) -C tools -f Makefile.host mkconfig$(HOSTEXEEXT)

``include/nuttx/config.h`` 规则调用上面规则生成的 ``mkconfig`` 可执行文件，从当前的 ``.config`` 文件创建 ``config.h`` 文件。

符号链接和目录链接
^^^^^^^^^^^^^^^^^^^^^^^^

目录链接是符号链接，允许构建系统使用通用路径，同时指向特定于架构、芯片或板的目录。这使得在许多不同硬件配置上使用单一构建系统工作流成为可能。

- 将 ``arch/<arch-name>/include`` 符号链接到 ``include/arch``
- 将 ``boards/<arch>/<chip>/<board>/include`` 符号链接到 ``include/arch/board``
- 将 ``arch/<arch-name>/include/<chip-name>`` 符号链接到 ``include/arch/chip``
- 将 ``boards/<arch>/<chip>/<board>`` 符号链接到 ``arch/<arch-name>/src/board/<board>``

.. note::

  某些板使用 ``common`` 目录。在这种情况下：

  - ``boards/<arch>/<chip>/common`` 被符号链接到 ``arch/<arch-name>/src/board``
  - ``boards/<arch>/<chip>/<board>`` 被符号链接到 ``arch/<arch-name>/src/board/<board>``

- 将 ``arch/<arch-name>/src/<chip-name>`` 符号链接到 ``arch/<arch-name>/src/chip``

``.dirlinks`` 文件本身只是一个时间戳标记，指示所有目录链接已创建。

虚拟文件
^^^^^^^

使用虚拟文件的主要原因是处理一些特定场景，例如外部代码库、自定义芯片和板，或克服工具限制。如果下面的任何功能未使用，构建系统将回退到虚拟文件。

- **${EXTERNALDIR}**

  ``$(EXTERNALDIR)`` 的可能值为 ``external`` 或 ``dummy``。

  NuttX 代码库可以通过使用 ``$(TOPDIR)/external/`` 目录来扩展。构建系统在该目录中搜索 ``Kconfig`` 文件。如果找到，构建系统将 ``EXTERNALDIR`` 变量定义为 ``external``，并将另一个库（``libexternal``）附加到构建过程中。

  .. code-block:: makefile

    # 外部代码支持
    # 如果 external/ 包含 Kconfig，我们将 EXTERNALDIR 变量定义为 'external'
    # 以便主 Kconfig 可以找到它。否则，我们将其重定向到虚拟 Kconfig
    # 这是由于 kconfig 无法进行条件包含。

    EXTERNALDIR := $(shell if [ -r $(TOPDIR)/external/Kconfig ]; then echo 'external'; else echo 'dummy'; fi)

- **dummy/Kconfig**

  ``dummy/Kconfig`` 用于处理自定义芯片和板。

  如果使用树内芯片/板，构建系统将解析为 dummy_kconfig 文件。
  - ``$(CHIP_KCONFIG)`` 设置为 ``$(TOPDIR)$(DELIM)arch$(DELIM)dummy$(DELIM)dummy_kconfig``
  - ``$(BOARD_KCONFIG)`` 设置为 ``$(TOPDIR)$(DELIM)boards$(DELIM)dummy$(DELIM)dummy_kconfig``

  如果使用自定义芯片/板，构建系统将解析为它们的自定义路径。

  .. code-block:: makefile

    # 将 $(CHIP_KCONFIG) 复制到 arch/dummy/Kconfig

    arch/dummy/Kconfig:
    	@echo "CP: $@ to $(CHIP_KCONFIG)"
    	$(Q) cp -f $(CHIP_KCONFIG) $@

    # 将 $(BOARD_KCONFIG) 复制到 boards/dummy/Kconfig

    boards/dummy/Kconfig:
    	@echo "CP: $@ to $(BOARD_KCONFIG)"
    	$(Q) cp -f $(BOARD_KCONFIG) $@

- **boards/dummy.c**

  构建系统使用特殊的 ``boards/dummy.c`` 文件生成一个无用的对象。无用对象的目的是确保创建 libboards.a/lib。某些归档器（ZDS-II、SDCC）需要非空的库，否则会生成错误。

.. _build_modes:

构建模式
^^^^^^^^^^^

如上所述，NuttX 支持多种构建模式。构建模式基于特定的 ``Kconfig`` 选项选择。

.. code-block:: makefile

  # 库构建选择
  #
  # NUTTXLIBS 是传递给特定于处理器的 Makefile 以构建最终 NuttX 目标的
  #   NuttX 库列表。
  # USERLIBS 是用于构建最终用户空间应用程序的库列表
  # EXPORTLIBS 是 'make export' 应该导出的库列表

  ifeq ($(CONFIG_BUILD_PROTECTED),y)
  include tools/ProtectedLibs.mk
  else ifeq ($(CONFIG_BUILD_KERNEL),y)
  include tools/KernelLibs.mk
  else
  include tools/FlatLibs.mk
  endif

上面引用的每个文件的内容在其各自的部分中记录。

- tools/ProtectedLibs.mk :ref:`protectedlibs_mk`
- tools/FlatLibs.mk :ref:`flatlibs_mk`
- tools/KernelLibs.mk :ref:`kernelibs_mk`

.. _config_mk:

Config.mk
---------

``Config.mk`` 包含许多配置文件使用的通用定义。

* 它定义了 :ref:`verbosity` 背后的逻辑
* 它解析平台特定的特殊性，例如

  * 构建*工具* ``例如 mkdeps、cnvwindeps、link.sh/.bat、unlink.sh/.bat``
  * 文件扩展名 ``例如 .exe、.dll 用于 Windows，.o、.a 用于 Unix``
  * 基于主机平台的分隔符。``例如 \ 用于 Windows，/ 用于 Unix``

* 解析自定义板/芯片/架构
* 定义依赖机制的规则

  .. code-block:: makefile

    OBJPATH ?= .

    %.dds: %.S
    	$(Q) $(MKDEP) --obj-path $(OBJPATH) --obj-suffix $(OBJEXT) $(DEPPATH) "$(CC)" -- $(CFLAGS) -- $< > $@

    %.ddc: %.c
    	$(Q) $(MKDEP) --obj-path $(OBJPATH) --obj-suffix $(OBJEXT) $(DEPPATH) "$(CC)" -- $(CFLAGS) -- $< > $@

    %.ddp: %.cpp
    	$(Q) $(MKDEP) --obj-path $(OBJPATH) --obj-suffix $(OBJEXT) $(DEPPATH) "$(CXX)" -- $(CXXFLAGS) -- $< > $@

    %.ddx: %.cxx
    	$(Q) $(MKDEP) --obj-path $(OBJPATH) --obj-suffix $(OBJEXT) $(DEPPATH) "$(CXX)" -- $(CXXFLAGS) -- $< > $@

    %.ddh: %.c
    	$(Q) $(MKDEP) --obj-path $(OBJPATH) --obj-suffix $(OBJEXT) $(DEPPATH) "$(CC)" -- $(HOSTCFLAGS) -- $< > $@

* 根据编译器定义包含标志前缀
* 定义用于编译、汇编、归档文件等的通用函数

此文件（连同 *<nuttx>*/.config）必须包含在每个特定于配置的 Make.defs 文件的顶部，例如

.. code-block:: makefile

  include $(TOPDIR)/.config
  include $(TOPDIR)/tools/Config.mk

特定于配置的 Make.defs 文件中的后续逻辑可以根据需要覆盖这些默认定义。


.. _flatlibs_mk:

FlatLibs.mk
-----------

此文件为**平板构建模式**定义库集。在此模式下，NuttX 内核和所有用户空间应用程序被编译并链接到单个单体二进制文件中。

其主要职责是：

-   **填充 ``NUTTXLIBS``：** 此文件系统地将所有必需的库附加到 ``NUTTXLIBS`` 变量。这包括核心操作系统库（``libsched``、``libmm``、``libc``）、架构和板支持库，以及设备驱动程序。

-   **条件库包含：** 它使用 ``ifeq ($(CONFIG_XXX),y)`` 检查来根据系统的 Kconfig 条件包含可选功能的库。例如，``staging/libnet.a`` 仅在 ``CONFIG_NET=y`` 时添加，``staging/libcrypto.a`` 在 ``CONFIG_CRYPTO=y`` 时添加。

-   **定义 ``USERLIBS``：** 在平板构建中，没有单独的用户空间二进制文件，因此 ``USERLIBS`` 变量被初始化但保持为空。

-   **设置 ``EXPORTLIBS``：** 它将 ``NUTTXLIBS`` 的完整列表分配给 ``EXPORTLIBS`` 变量。这确保 ``make export`` 命令打包链接最终二进制文件所需的所有编译库。

.. _protectedlibs_mk:

ProtectedLibs.mk
----------------

此文件为**保护构建模式**定义库集。在此模式下，NuttX 内核和用户空间应用程序被构建为两个不同的二进制文件，启用内存保护和更健壮的系统架构。

其主要职责是：

-   **独立的库列表：** 与平板构建不同，此文件填充 ``NUTTXLIBS`` 变量（用于内核二进制文件）和 ``USERLIBS`` 变量（用于用户空间应用程序）。

-   **内核与用户库变体：** 它明确区分核心库的内核和用户变体。例如：

    -   内核特定库（例如 ``libkc.a``、``libkmm.a``、``libkarch.a``）被添加到 ``NUTTXLIBS``。
    -   用户空间对应库（例如 ``libc.a``、``libmm.a``、``libarch.a``）被添加到 ``USERLIBS``。

-   **系统调用机制：** 它包含系统调用接口的基本组件：

    -   ``staging/libstubs.a``（系统调用存根）被添加到 ``NUTTXLIBS``。
    -   ``staging/libproxies.a``（系统调用代理）被添加到 ``USERLIBS``。这些促进用户应用程序与内核之间的安全通信。

-   **条件库包含：** 与其他构建模式类似，它使用 ``ifeq ($(CONFIG_XXX),y)`` 检查来根据 Kconfig 设置条件包含内核和用户空间的可选功能库。

-   **导出用户库：** 一个关键区别是 ``EXPORTLIBS`` 设置为 ``$(USERLIBS)``。这意味着 ``make export`` 命令将主要打包用户空间库，然后由外部构建系统或用于链接用户应用程序。

.. _kernelibs_mk:

KernelLibs.mk
-------------

此文件为**内核构建模式**定义库集。在此模式下，仅将 NuttX 内核编译并链接到单个二进制文件中。用户应用程序预计将单独加载和执行，通常在受保护的用户空间环境中。

其主要职责是：

-   **仅内核的 ``NUTTXLIBS``：** 此文件用所有必要的内核空间库填充 ``NUTTXLIBS`` 变量。这包括核心操作系统组件（例如 ``libsched``、``libdrivers``）、通用库的内核变体（例如 ``libkc.a``、``libkmm.a``、``libkarch.a``）和板支持。

-   **空的 ``USERLIBS``：** ``USERLIBS`` 变量被显式初始化但保持为空，因为此构建模式不产生用户空间二进制文件。

-   **系统调用存根：** 它在 ``NUTTXLIBS`` 中包含 ``staging/libstubs.a``，提供系统调用的内核端实现。用户空间系统调用代理（``libproxies.a``）不包含在内，与缺少用户空间构建一致。

-   **条件库包含：** 它使用 ``ifeq ($(CONFIG_XXX),y)`` 检查来根据系统的 Kconfig 条件包含内核特定的可选功能库。

-   **导出用户库（空）：** ``EXPORTLIBS`` 设置为 ``$(USERLIBS)``。因此，在这种仅内核的构建模式中，``EXPORTLIBS`` 将为空，反映没有为外部打包产生用户空间库。

.. _directories_mk:

Directories.mk
--------------

此文件定义了整个 NuttX 构建过程中使用的目录。这些目录列表不是静态的，而是根据活动的 Kconfig 配置**动态构建**的。

该文件首先定义一个 ``BASEDIRS`` 变量，其中包含始终是构建一部分的核心目录。随后，它使用条件逻辑（``ifeq ($(CONFIG_XXX),y)``）仅在其对应的 Kconfig 选项启用时才将额外的目录附加到各种主列表中，如 ``ALLDIRS`` 和 ``CLEANDIRS``。

例如：

- ``net/`` 目录仅在 ``CONFIG_NET=y`` 时添加到构建列表中。
- 如果 ``CONFIG_GRAPHICS=y``，则包含 ``graphics/`` 目录。
- 如果 ``CONFIG_CRYPTO=y``，则包含 ``crypto/`` 目录。

该文件定义了保存这些动态生成的目录列表的关键变量：

- ``KERNDEPDIRS``：包含用于依赖生成的内核文件的目录。
- ``USERDEPDIRS``：包含用于依赖生成的用户空间文件的目录。
- ``CCLEANDIRS``：``clean_context`` 目标将执行的目录。
- ``CLEANDIRS``：``clean`` 目标将执行的所有已知目录。
- ``CONTEXTDIRS``：具有特殊预构建要求的目录，例如自动生成文件或创建符号链接。

.. _libtargets_mk:

LibTargets.mk
-------------

``LibTargets.mk`` 文件定义了从各自的源目录构建 NuttX 库并将生成的库文件安装到 ``staging/`` 目录所需的所有目标。

对于许多核心库（例如 ``libc``、``libm``、``libmm``、``libbuiltin``、``libnx``、``libarch``），``LibTargets.mk`` 为**内核**和**用户**变体定义了不同的目标。

-   **内核库**通常以 ``libk`` 为前缀（例如 ``libkc.a`` 用于内核 C 库，``libkmm.a`` 用于内核内存管理）。这些使用包含 ``$(KDEFINE)`` 的特定 ``EXTRAFLAGS`` 编译，后者设置内核特定的预处理器定义（例如 ``-D__KERNEL__``）。这确保它们使用内核环境所需的上下文和 API 构建。

-   **用户库**保留其标准名称（例如 ``libc.a``、``libmm.a``）。这些在没有 ``$(KDEFINE)`` 标志的情况下编译，使其适合用户空间应用程序。用户模式库的构建过程通常依赖于 ``pass1dep``，而内核模式库依赖于 ``pass2dep``，反映了保护和内核构建模式中的两遍构建策略。

对于每个库变体，定义了两个主要目标：

1.  **构建目标：** 此目标在库的源目录中递归调用 ``make``（例如 ``libs/libc/``、``mm/``）以编译源文件并创建库归档（``.a``）文件。根据它是内核模式还是用户模式构建，它传递适当的 ``EXTRAFLAGS``。这些目标的依赖关系是 ``pass1dep`` 或 ``pass2dep``，确保在构建之前检查依赖关系。

2.  **暂存目标：** 此目标依赖于前一步成功创建的库归档。其规则调用 ``INSTALL_LIB`` 宏（在 ``Unix.mk`` 或 ``Win.mk`` 中定义）以将新创建的库复制到顶级 ``staging/`` 目录。

该文件包含条件逻辑，主要基于 ``CONFIG_BUILD_FLAT``，以调整可以是用户或内核空间一部分的库的依赖关系（``pass1dep`` 与 ``pass2dep``），确保它们根据选定的构建模式在正确的遍中构建。
