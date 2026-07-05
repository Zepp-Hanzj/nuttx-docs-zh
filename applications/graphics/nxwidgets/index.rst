.. _nxwidgets:

=======================
``nxwidgets`` NXWidgets
=======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

为了更好地支持基于 NuttX 的平台，创建了一个名为 NXWidgets 的特殊图形用户界面。NXWidgets 使用 C++ 编写，与 NuttX :ref:`NX 图形子系统 <nxgraphics>` 无缝集成，以在 NX 图形子系统中提供图形对象或"部件"。

NXWidgets 的一些功能包括：

-  **保守的 C++**。NXWidgets 完全使用 C++ 编写，但仅使用在 NuttX 下完全支持的特定"嵌入式友好"C++ 构造。不需要额外的 C++ 支持库。
-  **NX 集成**。NXWidgets 与 :ref:`NX 图形子系统 <nxgraphics>` 无缝集成。可以类比 Linux 下的 X 服务器……NX 图形系统就像一个小型 X 服务器，在 NuttX 下提供窗口功能。通过添加 NXWidgets，您可以在 NX 窗口和工具栏中支持按钮和文本框等图形对象。
-  **小占用空间**。NXWidgets 专为嵌入式应用中的 MCU 使用而定制。它非常适合大多数 MCU 系列的中高端产品。完整的 NXWidgets 仅需约 40K FLASH 和约 4K SRAM。
-  **输出设备**。NXWidgets 既可在高端帧缓冲设备上工作，也可在通过串行或并行端口连接到小型 MCU 的 LCD 上工作。
-  **输入设备**。NXWidgets 接受来自鼠标或触摸屏的位置和选择输入。它还支持来自键盘（如 USB 键盘）的字符输入。NXWidgets 支持一个非常特殊的部件 CKeypad，它通过可通过鼠标或触摸屏输入操作的屏幕键盘提供键盘输入。
-  **众多图形对象**。NXWidgets 支持的图形对象包括标签、按钮、文本框、按钮数组、复选框、循环按钮、图像、滑块、可滚动列表框、进度条等。
-  **DOxygen 文档** DOxygen 文档可用。

注意：NxWidgets 中的许多基础类源自 Antony Dzeryn 的"Woopsi"项目，该项目也使用 BSD 风格许可证。详见 COPYING 文件。

NXWidgets Doxygen 文档
===============================

.. todo::
   NXWidgets 支持通过 Doxygen 构建 HTML 文档。我们应将其集成到 Sphinx 文档构建中。

感谢 Jose Pablo Carballo 的贡献！

目录结构
-------------------

- ``Kconfig``

  这是一个应放置在 ``apps/NxWidgets/Kconfig`` 的 ``Kconfig`` 文件。当复制到该位置时，NuttX 配置系统将使用它来配置 NxWidgets 和 NxWM 的设置。

- ``nxwidgets``

  本目录提供 NxWidgets 的源代码、头文件和构建环境。

- ``UnitTests``

  为 ``nxwidgets`` 提供的许多单个部件提供单元级别测试集合。

Doxygen
-------

在 Ubuntu 中安装必要的软件包
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 安装以下软件包::

   $ sudo aptitude install doxygen doxygen-doc doxygen-gui dot2tex graphviz

2. （可选）从最新源代码安装 Doxygen。

   Ubuntu 软件包已过时。Doxygen 版本越新，文档外观越好。

   进入临时文件夹下载源代码，然后运行 [1]::

     $ svn co https://doxygen.svn.sourceforge.net/svnroot/doxygen/trunk doxygen-svn
     $ cd doxygen-svn
     $ ./configure
     $ make
     $ make install

生成文档
~~~~~~~~~~~~~~~~~~~~~~~~

此处描述两种方法：

1. 使用提供的 ``gendoc.sh`` 脚本::

     trunk/NXWidgets/Doxygen/gendoc.sh

   该脚本只需要一个参数，即生成文档的绝对路径。即::

     $ cd /path/to/nuttx/trunk/NXWidgets/Doxygen/
     $ mkdir doc
     $ ./gendoc.sh $PWD/doc

2. 直接使用 ``Doxyfile``：

   ``Doxyfile`` 文件包含 Doxygen 设置的运行配置，仅在必要时编辑。

   要生成文档，请输入::

     $ cd /path/to/nuttx/trunk/NXWidgets/Doxygen/
     $ doxygen Doxyfile

参考文献
~~~~~~~~~~

[1] http://www.stack.nl/~dimitri/doxygen/download.html


单元测试
----------

安装和构建单元测试
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 设置 NuttX

   1. 配置 NuttX

      配置 NuttX 以运行目标配置之一。例如，假设您使用 ``sim/nsh2`` 配置。``sim/nsh2`` 配置是专门为在模拟平台上使用 NXWidgets 而创建的。类似地，``stm3210e-eval/nsh2`` 特殊配置也适用于 ``STM3210E-EVAL``。不过，单元测试可以在其他配置上运行（见下面的步骤 d 和 e）。

      **注意**：还有一些其他推荐的特殊配置用于 NxWM 的单元级别测试，因为该情况下的配置更复杂。这些是：

      1) ``sim/nxwmm``，模拟平台（无触摸屏），以及
      2) ``stm3240g-evel``，用于 ``STM3240G-EVAL`` 板（带 STMPE11 触摸屏）

      在本讨论中，我们假设使用 ``sim/nsh2`` 配置。``sim/nsh2`` 配置的安装方式如下::

        cd <nuttx-directory-path>
        make distclean
        tools/configure.sh sim:nsh2

      其中：

      ``<nuttx-directory-path>`` 是 NuttX 构建目录的完整绝对路径。

      如果您使用 ``sim/nsh2`` 或 ``stm3210e-eval`` 配置，请跳到步骤 2（嗯……最好也检查一下 1d）。

      您选择的配置可能有某些要求……例如，某些部件测试可能需要触摸屏支持或特殊字体选择。这些测试特定的要求在下面的"单元测试目录"中说明。

   2. 启用 C++ 支持

      如果您不使用 ``sim/nsh2`` 或 ``stm3210e-eval``，则需要在 ``nuttx/.config`` 中添加以下定义以启用 C++ 支持::

        CONFIG_HAVE_CXX=y

      请先检查，某些配置已经启用了 C++ 支持（截至撰写本文时，**仅** ``sim/nsh2`` 和 ``stm321-e-eval`` 配置预启用了 C++ 支持）。

   3. 启用调试选项

      如果您在模拟目标上运行，您可能还需要启用调试符号::

        CONFIG_DEBUG_SYMBOLS=y

      然后您可以使用 GDB 或 DDD 运行模拟，这是一个非常强大的调试环境！

   4. nxwm 单元测试的特殊配置要求::

        CONFIG_NXTERM=y

   5. 其他 ``.config`` 文件更改——仅限 NSH 配置。

      如果您使用的配置支持 NSH 和 NSH 内置任务，则一切正常。如果是 NSH 配置，则还需要在 ``nuttx/.config`` 文件中定义以下内容（如果尚未定义）::

        CONFIG_NSH_BUILTIN_APPS=y

      ``sim/nsh2`` 和 ``stm3210e-eval/nsh2`` 已经有此设置。如果您使用这些配置中的任何一个，则不需要在 ``nuttx/.config`` 文件中进行任何进一步更改。

   6. 其他 ``.config`` 文件更改——仅限非 NSH 配置。

      入口点。您需要在 .config 文件中设置入口点。对于 NSH 配置，入口点始终是 ``nsh_main``，您将看到如下设置::

        CONFIG_INIT_ENTRYPOINT="nsh_main"

      如果不使用 NSH，则每个单元测试都有一个唯一的入口点。该入口点是单元测试目录名称的小写加上后缀 ``_main``。因此，例如，``UnitTests/CButton`` 的正确入口是::

        CONFIG_INIT_ENTRYPOINT="cbutton_main"

      而 ``UnitTests/nxwm`` 的正确入口点是::

        CONFIG_INIT_ENTRYPOINT="nxwm_main"

      等等。

      对于非 NSH 配置（如 ``sim/touchscreen``），您需要移除提供 ``main`` 函数的配置设置，以便使用单元测试代码中的 ``main``。因此，例如，使用 ``sim/touchscreen`` 配置时，您需要从 NuttX 配置文件（``.config``）中移除以下内容::

        CONFIG_EXAMPLES_TOUSCHCREEN=y  ## 移除（提供 "tc_main"）

2. 调整栈大小

   如果使用模拟配置（如 ``sim/nsh2``）且您的单元测试使用 X11 作为显示设备，则需要增加单元测试栈的大小，如下面"X11 模拟的栈大小问题"中所述。

3. 构建 NuttX，包括单元测试和 NXWidgets 库::

     cd <nuttx-directory-path>
     . ./setenv.sh
     make

变通方法
~~~~~~~~~~~~

构建问题
............

1. 在 Cygwin 上构建 C++ 代码时报告了此错误::

     LD:  nuttx.rel
     ld: skipping incompatible /home/patacongo/projects/nuttx/nuttx/trunk/nuttx/libxx//liblibxx.a when searching for -llibxx
     ld: cannot find -llibxx

   该问题似乎是由 ``gcc`` 构建 32 位代码而 ``g++`` 构建 64 位代码引起的。在 ``g++`` 命令行中添加 ``-m32`` 选项似乎可以解决问题。在 ``Make.defs`` 中::

     CXXFLAGS = -m32 $(ARCHWARNINGSXX) $(ARCHOPTIMIZATION) \\
                $(ARCHCXXFLAGS) $(ARCHINCLUDESXX) $(ARCHDEFINES) $(EXTRADEFINES) -pipe

2. X11 模拟的栈大小问题

   当您运行 NuttX 模拟时，它使用 NuttX 从 NuttX 堆中分配的栈。模拟中的内存管理模型与真实目标系统完全相同。这是好的，因为这产生了更高保真度的模拟。

   然而，当模拟调用 Linux/Cygwin 库时，它仍然使用这些小的模拟栈。例如，当您调用系统在控制台窗口中获取和放置字符时，或当您调用系统进行 x11 调用时，就会发生这种情况。这些库中的编程模型将假定 Linux/Cygwin 环境，其中栈大小动态增长。

   因此，这些系统库可能在栈上分配大型数据结构并溢出小的 NuttX 栈。特别是 X11 需要大的栈。如果您在模拟中使用 X11，请确保为 X11 系统调用留出"大量"栈空间（可能 8 或 16Kb）。以用户启动开始的线程的栈大小由配置设置 ``CONFIG_INIT_STACKSIZE`` 控制；您可能需要将此值增加到更大的数字以在 X11 系统调用中存活。

   如果您将 X11 应用程序作为 NSH 附加程序运行，则附加程序的栈大小以另一种方式控制。以下是在该情况下增加栈大小的步骤::

     cd ../apps/namedapps  # 进入 namedapps 目录
     vi namedapps_list.h   # 编辑此文件并增加附加程序的栈大小
     rm .built *.o         # 这将强制 namedapps 逻辑重新构建

单元测试目录
~~~~~~~~~~~~~~~~~~~~~~

以下为每个 NXWidgets 提供简单的单元测试。此外，这些单元测试提供了每种部件类型使用的示例。

- ``CButton``

  - 测试 ``CButton`` 部件。
  - 依赖 ``CLabel``。

- ``CButtonArray``

  - 测试 ``CButtonArray`` 部件。

- ``CCheckBox``

  - 测试 ``CCheckBox`` 部件。
  - 依赖 ``CLabel`` 和 ``CButton``。

- ``CGlyphButton``

  - 测试 ``CGlyphButton`` 部件。
  - 依赖 ``CLabel`` 和 ``CButton``。

- ``CImage``

  - 测试 ``CImage`` 部件。

- ``CLabel``

  - 测试 ``CLabel`` 部件。

- ``CProgressBar``

  - 测试 ``CProgressBar`` 部件。

- ``CRadioButton``

  - 测试 ``CRadioButton`` 和 ``CRadioButtonGroup`` 部件。
  - 依赖 ``CLabel`` 和 ``CButton``。

- ``CScrollBarHorizontal``

  - 测试 ``ScrollbarHorizontal``。
  - 依赖 ``CSliderHorizontal`` 和 ``CGlyphButton``。

- ``CScrollBarVertical``

  - 测试 ``ScrollbarHorizontal``。
  - 依赖 ``CSliderVertical`` 和 ``CGlyphButton``。

- ``CSliderHorizontal``

  - 测试 ``CSliderHorizontal``。
  - 依赖 ``CSliderHorizontalGrip``。

- ``CSliderVertical``

  - 测试 ``CSliderVertical``。
  - 依赖 ``CSliderVerticalGrip``。

- ``CTextBox``

  - 测试 ``CTextBox`` 部件。
  - 依赖 ``CLabel``。
