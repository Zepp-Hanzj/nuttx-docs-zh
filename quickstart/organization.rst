.. include:: /substitutions.rst

.. todo::
  此部分大部分内容来自原始文档，未经修改。它实际上不属于
  "快速入门"。此外，需要清理。

.. _organization:

===================
目录结构
===================

此处包含的内容仅供参考，初次使用时不必了解所有细节。

NuttX 的总体目录布局与 Linux 内核的目录结构非常相似——至少在最表层是如此。
顶层是主 Makefile 和一系列子目录，下面将列出并在后续段落中讨论：

**配置文件**。NuttX 的配置由处理器架构目录、*芯片/SoC* 目录和
开发板配置目录中的逻辑组成。完整的配置由 NuttX 配置文件中的
多个设置指定。

-  *处理器架构特定文件*。这些文件包含在 ``arch/<arch-name>/`` 目录中，
   并在 `下文 <#arch-subdirectory-structure>`__ 的段落中讨论。
   例如，所有 ARM 处理器架构都在 ``arch/arm/`` 目录下提供，
   通过 ``CONFIG_ARCH="arm"`` 配置选项选择。

   处理器架构的变体可能在 ``arch/<arch-name>/`` 的子目录中提供。
   延续此示例，ARMv7-M ARM 系列由
   ``arch/arm/include/armv7-m`` 和 ``arch/arm/src/armv7-m`` 目录中的逻辑支持，
   通过 ``CONFIG_ARCH_CORTEXM3=y``、``CONFIG_ARCH_CORTEXM4=y`` 或
   ``CONFIG_ARCH_CORTEXM7=y`` 配置选项选择。

-  *芯片/SoC 特定文件*。每个处理器架构都嵌入在一个
   *片上系统*（SoC）架构中。完整的 SoC 架构包括处理器架构
   加上芯片特定的中断逻辑、时钟逻辑、通用 I/O（GPIO）逻辑
   以及专用的内部外设（如 UART、USB 等）。

   这些芯片特定的文件包含在 ``arch/<arch-name>/`` 目录下的
   芯片特定子目录中，通过 ``CONFIG_ARCH_CHIP`` 选择。

   例如，STMicro STM32 SoC 架构基于 ARMv7-M 处理器，
   由 ``arch/arm/include/stm32`` 和 ``arch/arm/src/stm32`` 目录中的逻辑支持，
   通过 ``CONFIG_ARCH_CHIP="stm32"`` 配置设置选择。

-  *开发板特定配置*。为了可用，芯片必须包含在开发板环境中。
   开发板配置定义了开发板的附加属性，包括外设 LED、外部外设
   （如网络、USB 等）。

   这些开发板特定的配置文件可以在
   ``boards/<arch-name>/<chip-name>/<board-name>/`` 子目录中找到，
   并在 `下文 <#boards-subdirectory-structure>`__ 的段落中讨论。

   目录 ``boards/arm/stm32/stm32f4disovery/`` 作为示例，
   包含 STM32F4 Discovery 开发板的特定逻辑，通过
   ``CONFIG_ARCH_BOARD="stm32f4discovery"`` 配置设置选择。

``nuttx/Documentation``
=======================

此目录包含 NuttX 文档。它使用
`Sphinx 文档系统 <https://www.sphinx-doc.org>`_ 制作。有关如何构建文档的信息，
请参见 README.md 文件。

``nuttx/arch``
==============

此子目录包含 NuttX 支持的架构。

详情请参见 :doc:`/components/arch/index`。

``nuttx/binfmt``
================

``binfmt/`` 子目录包含将文件系统中的二进制文件加载到内存中的逻辑，
使其可以被执行。

``nuttx/audio``
===============

``audio/`` 子目录包含 NuttX 音频子系统。

.. _nuttx_boards:

``nuttx/boards``
================

``boards/`` 子目录包含每个开发板的自定义逻辑和开发板配置数据。
这些开发板特定的配置加上 ``arch/`` 子目录中的架构特定配置，
完整定义了 NuttX 的定制移植。

开发板子目录结构
-----------------------------

``boards/`` 目录包含开发板特定的配置文件。每个开发板必须在
``boards/<arch-name>/<chip-name>/`` 下提供一个 <board-name> 子目录。

详情请参见 :doc:`/components/boards`。

``nuttx/cmake``
===============

此子目录包含 NuttX CMake 函数。

详情请参见 :doc:`/components/cmake`。

``nuttx/crypto``
================

此子目录包含 NuttX 加密子系统。

详情请参见 :doc:`/components/crypto`。

``nuttx/drivers``
=================

此目录包含架构无关的设备驱动程序。

详情请参见 :doc:`/components/drivers/index`。

``nuttx/fs``
============

此目录包含 NuttX 文件系统。此文件系统在 `下文 <#NxFileSystem>`__ 中描述。

``nuttx/graphics``
==================

此目录包含 NuttX 下的图形/视频支持文件。

详情请参见 :doc:`/components/nxgraphics/index`。

``nuttx/include``
=================

此目录包含 NuttX 头文件。标准头文件可以以 *常规* 方式包含：

``nuttx/libs/libc``
===================

此目录包含一组标准 libc 类函数，具有到 NuttX 的自定义接口。

详情请参见 :doc:`/components/libs/index`。

``nuttx/mm``
============

这是 NuttX 内存管理器。

详情请参见 :doc:`/components/mm/index`。

``nuttx/net``
=============

此目录包含 NuttX 网络层的实现，包括内部 socket API。

详情请参见 :doc:`/components/net/index`。

``nuttx/openamp``
=================

此目录包含 NuttX 的 OpenAMP 支持。

详情请参见 :doc:`/components/openamp`。

``nuttx/pass1``
===============

待补充

``nuttx/sched``
===============

构成 NuttX RTOS 核心的文件位于此处。

``nuttx/syscall``
=================

如果 NuttX 被构建为独立编译的内核（使用
``CONFIG_BUILD_PROTECTED=y`` 或 ``CONFIG_BUILD_KERNEL=y``），则此目录的内容将被构建。
此目录包含一个系统调用接口，可用于用户模式应用程序与内核模式 RTOS 之间的通信。

详情请参见 :doc:`/components/syscall`。

``nuttx/tools``
===============

此目录包含一系列工具和脚本，用于简化 NuttX 的配置、构建和维护。

有关各个文件的更多信息，请参阅 :doc:`/components/tools/index` 页面。
其中一些工具在下面关于 `配置和构建 <#configandbuild>`__ NuttX 的讨论中也有涉及。

``nuttx/video``
===============

此目录包含视频子系统的支持。

详情请参见 :doc:`/components/video`。

``nuttx/wireless``
==================

此目录包含硬件无关的无线支持。

详情请参见 :doc:`/components/wireless`。

``nuttx/CMakeLists.txt``
========================

顶层 ``CMakeLists.txt`` 文件。

``nuttx/Makefile``
==================

``$(TOPDIR)`` 目录中的顶层 ``Makefile`` 包含构建 NuttX 的所有顶层控制逻辑。
