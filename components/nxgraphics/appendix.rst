========
Appendix
========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``graphics/`` 目录结构
=================================

图形能力既包含 RTOS 内部的组件，也包含用户可调用的接口。在 NuttX 内核模式构建中，图形子系统的某些组件可以在用户模式下调用，而其他组件则是 RTOS 内部的。``nuttx/graphics`` 目录仅包含 RTOS 内部的组件。用户可调用的函数必须是可与用户应用程序链接的库的一部分。这些用户可调用的接口在 ``nuttx/libnx`` 下的子目录中提供。

``libnx/nx``
   逻辑上属于 nxmu 和 nxsu 的通用可调用接口。
``graphics/nxglib`` 和 ``libnx/nxglib``
   NuttX 小型图形库。该目录包含对基本图形对象进行操作的通用工具支持逻辑，以及直接光栅化到帧缓冲区或通过 LCD 驱动接口的逻辑。它没有窗口的概念（除了一个帧缓冲区或 LCD 窗口）。
``graphics/nxbe``
   这是一个小型窗口系统的*后端*。它可以与两种前端之一配合使用以完成窗口系统（参见下面的 ``nxmu`` 和 ``nxsu``）。它包含大多数重要的窗口管理逻辑：裁剪、窗口控制、窗口绘制等。
``graphics/nxmu`` 和 ``libnx/nxmu``
   这是 NX 多用户*前端*。当与通用*后端*（``nxbe``）结合时，它实现了一个多线程、多用户的窗口系统。此目录中的文件提供了 ``include/nuttx/nx/nx.h`` 中描述的窗口 API。多用户前端包括一个在自己的线程上执行的图形服务器；多个图形客户端然后通过 POSIX 消息队列与服务器通信，以序列化来自多个线程的窗口操作。
``libnx/nxfonts``
   这是 NXFONTS 实现所在的位置。这是一组相对底层的字符集/字形管理 API。参见 ``include/nuttx/nx/nxfonts.h``。
``libnx/nxtk``
   这是 NXTOOLKIT 实现所在的位置。此工具包构建在 NX 之上，与多用户 NX 前端配合工作。参见 ``include/nuttx/nx/nxtk.h``。
``apps/graphics/NxWidgets``
   :ref:`NxWidgets <nxwidgets>` 代码作为 ``apps/`` 存储库中提供的单独包提供。
``graphics/nxterm``
   NxTerm 驱动构建在 NX 之上，与多用户 NX 前端配合工作。参见 ``include/nuttx/nx/nxterm.h``。

NX 配置选项
========================

通用配置设置
------------------------------

``CONFIG_NX``
   启用图形库和 NX 的整体支持
``CONFIG_NX_RAMBACKED``
   启用 RAM 支持的窗口支持。如果选择了此选项，则可以选择创建带有 RAM 帧缓冲区备份窗口内容的窗口。渲染到窗口将导致渲染到备份帧缓冲区，然后从帧缓冲区更新物理显示。

   此选项的优势在于管理窗口的应用程序将不再接收 redraw() 回调。这些调用通常在例如上面的窗口移动暴露下面窗口的一部分时发生。如果选择了此选项，系统将从备份帧缓冲区重新绘制窗口的暴露部分，无需窗口应用程序的干预。这大大降低了应用程序的复杂性并提高了窗口性能，但代价是增加了内存使用。

   例外情况是当窗口调整为更宽和/或更高的大小时。在这种情况下，重新绘制回调仍会发生。在这种情况下，需要为扩展的窗口区域提供新的图形内容。

   其他情况下的重新绘制请求也会被抑制：窗口位置、大小等的更改。

NXGL 配置设置
---------------------------

``CONFIG_NX_NPLANES``：
   某些 YUV 颜色格式需要多平面支持，每种颜色分量一个平面。除非您有这样的特殊硬件，否则此值应未定义或设置为 1。
``CONFIG_NX_DISABLE_1BPP``、``CONFIG_NX_DISABLE_2BPP``、``CONFIG_NX_DISABLE_4BPP``、``CONFIG_NX_DISABLE_8BPP``、``CONFIG_NX_DISABLE_16BPP``、``CONFIG_NX_DISABLE_24BPP`` 和 ``CONFIG_NX_DISABLE_32BPP``：
   NX 支持各种像素深度。您可以通过禁用未使用的颜色深度支持来节省一些内存。
``CONFIG_NX_PACKEDMSFIRST``：
   如果使用小于 8 位的像素深度，则 NX 需要知道像素是从 MS 到 LS 打包还是从 LS 到 MS 打包
``CONFIG_NX_LCDDRIVER``：
   默认情况下，NX 构建为使用帧缓冲区驱动（参见 ``include/nuttx/video/fb.h``）。如果定义了此选项，NX 将构建为使用 LCD 驱动（参见 ``include/nuttx/lcd/lcd.h``）。
``CONFIG_NX_ANTIALIASING``：
   启用在渲染不同方向的线条时的抗锯齿支持。此选项仅适用于帧缓冲区驱动，且仅适用于 16、24 或 32 位 RGB 颜色格式。

配置设置
----------------------

``CONFIG_NX_XYINPUT``：
   构建对 X/Y 输入（如鼠标或触摸屏）的支持。
``CONFIG_NX_KBD``：
   构建对键盘/小键盘输入的支持。
``CONFIG_NX_WRITEONLY``：
   如果底层图形设备不支持读操作则定义。如果定义了 ``CONFIG_NX_LCDDRIVER`` 和 ``CONFIG_LCD_NOGETRUN`` 则自动定义。

NX 服务器配置设置
--------------------------------

``CONFIG_NX_BLOCKING``
   以阻塞模式打开客户端消息队列。在这种情况下，``nx_eventhandler()`` 在接收并处理消息之前不会返回。
``CONFIG_NX_MXSERVERMSGS`` 和 ``CONFIG_NX_MXCLIENTMSGS``
   指定消息队列中可容纳的最大消息数。不会分配额外的资源，但可以设置此项以防止过多消息淹没客户端或服务器（``CONFIG_PREALLOC_MQ_MSGS`` 控制预分配的消息数量）。

NXTK 配置设置
---------------------------

``CONFIG_NXTK_BORDERWIDTH``：
   指定带框窗口使用的边框宽度（以像素为单位）。默认为 4。
``CONFIG_NXTK_BORDERCOLOR1``、``CONFIG_NXTK_BORDERCOLOR2`` 和 ``CONFIG_NXTK_BORDERCOLOR3``：
   指定带框窗口使用的边框颜色。
``CONFIG_NXTK_BORDERCOLOR2``
   阴影侧颜色，因此通常较暗。
``CONFIG_NXTK_BORDERCOLOR3``
   亮侧颜色，因此通常较亮。默认分别为中灰色、深灰色和浅灰色。
``CONFIG_NXTK_AUTORAISE``：
   如果设置，当鼠标位置在窗口的可见部分上方时，窗口将被提升到顶部。默认：必须在窗口的可见部分上方点击鼠标按钮。

NXFONTS 配置设置
------------------------------

``CONFIG_NXFONTS_CHARBITS``：
   字符集中的位数。当前选项仅为 7 和 8。默认为 7。
``CONFIG_NXFONT_SANS17X22``：
   此选项启用对小型 17x22 无衬线字体的支持（字体 ID ``FONTID_SANS17X22`` == 14）。
``CONFIG_NXFONT_SANS20X26``：
   此选项启用对小型 20x26 无衬线字体的支持（字体 ID ``FONTID_SANS20X26`` == 15）。
``CONFIG_NXFONT_SANS23X27``：
   此选项启用对小型 23x27 无衬线字体的支持（字体 ID ``FONTID_SANS23X27`` == 1）。
``CONFIG_NXFONT_SANS22X29``：
   此选项启用对小型 22x29 无衬线字体的支持（字体 ID ``FONTID_SANS22X29`` == 2）。
``CONFIG_NXFONT_SANS28X37``：
   此选项启用对中型 28x37 无衬线字体的支持（字体 ID ``FONTID_SANS28X37`` == 3）。
``CONFIG_NXFONT_SANS39X48``：
   此选项启用对大型 39x48 无衬线字体的支持（字体 ID ``FONTID_SANS39X48`` == 4）。
``CONFIG_NXFONT_SANS17X23B``：
   此选项启用对小型 17x23 无衬线粗体字体的支持（字体 ID ``FONTID_SANS17X23B`` == 16）。
``CONFIG_NXFONT_SANS20X27B``：
   此选项启用对小型 20x27 无衬线粗体字体的支持（字体 ID ``FONTID_SANS20X27B`` == 17）。
``CONFIG_NXFONT_SANS22X29B``：
   此选项启用对小型 22x29 无衬线粗体字体的支持（字体 ID ``FONTID_SANS22X29B`` == 5）。
``CONFIG_NXFONT_SANS28X37B``：
   此选项启用对中型 28x37 无衬线粗体字体的支持（字体 ID ``FONTID_SANS28X37B`` == 6）。
``CONFIG_NXFONT_SANS40X49B``：
   此选项启用对大型 40x49 无衬线粗体字体的支持（字体 ID ``FONTID_SANS40X49B`` == 7）。
``CONFIG_NXFONT_SERIF22X29``：
   此选项启用对小型 22x29 字体（带衬线）的支持（字体 ID ``FONTID_SERIF22X29`` == 8）。
``CONFIG_NXFONT_SERIF29X37``：
   此选项启用对中型 29x37 字体（带衬线）的支持（字体 ID ``FONTID_SERIF29X37`` == 9）。
``CONFIG_NXFONT_SERIF38X48``：
   此选项启用对大型 38x48 字体（带衬线）的支持（字体 ID ``FONTID_SERIF38X48`` == 10）。
``CONFIG_NXFONT_SERIF22X28B``：
   此选项启用对小型 27x38 粗体字体（带衬线）的支持（字体 ID ``FONTID_SERIF22X28B`` == 11）。
``CONFIG_NXFONT_SERIF27X38B``：
   此选项启用对中型 27x38 粗体字体（带衬线）的支持（字体 ID ``FONTID_SERIF27X38B`` == 12）。
``CONFIG_NXFONT_SERIF38X49B``：
   此选项启用对大型 38x49 粗体字体（带衬线）的支持（字体 ID ``FONTID_SERIF38X49B`` == 13）。

NxTerm 配置设置
-----------------------------

通用 NxTerm 设置。

``CONFIG_NXTERM``：
   启用 NxTerm 驱动的构建。

NxTerm 输出文本/图形选项：

``CONFIG_NXTERM_BPP``：
   目前，NxTerm 仅支持单个像素深度。必须提供此配置设置以支持该单个像素深度。默认：最小的已启用像素深度。（参见 ``CONFIG_NX_DISABLE_*BPP``）
``CONFIG_NXTERM_CURSORCHAR``：
   用作光标的位图代码。默认为 '_'
``CONFIG_NXTERM_MXCHARS``：
   NxTerm 需要记住写入控制台的每个字符，以便可以重新绘制窗口。此设置确定用于保存字符数据的某些内部分配的大小。默认：128。
``CONFIG_NXTERM_CACHESIZE``：
   NxTerm 支持已渲染字体的缓存。此字体缓存出于两个原因而需要：(1) 首先，它提高了文本性能，但更重要的是 (2) 它保留了字体内存。由于 NX 服务器在单独的服务器线程上运行，它需要渲染的字体内存持续存在直到服务器有机会渲染字体。不幸的是，如果保存所有字体，字体缓存会相当大。``CONFIG_NXTERM_CACHESIZE`` 设置将控制字体缓存的大小（以字形数量计）。仅保留最近使用的字形数量。默认：16。

      注意：NxTerm 驱动和 NX 任务之间仍可能存在竞争条件。如果您看到字符损坏（尤其是在打印大量数据或滚动时），那么增加 ``CONFIG_NXTERM_CACHESIZE`` 的值是您应该尝试的方法。或者，您可以减小 ``CONFIG_MQ_MAXMSGSIZE`` 的大小，这将强制 NxTerm 任务对服务器任务进行步调控制。``CONFIG_NXTERM_CACHESIZE`` 在任何情况下都应大于 ``CONFIG_MQ_MAXMSGSIZE``。

``CONFIG_NXTERM_LINESEPARATION``：
   这是每行测试之间的间距（以行数为单位）。默认：0
``CONFIG_NXTERM_NOWRAP``：
   默认情况下，当测试到达窗口右侧时，行会换行。可以定义此设置来更改此行为，使文本被简单截断直到遇到新行。

NxTerm 输入选项：

``CONFIG_NXTERM_NXKBDIN``：
   从 NX 键盘输入回调获取输入。默认情况下，键盘输入从 stdin（``/dev/console``）获取。如果设置了此选项，则启用接口 ``nxterm_kdbin()``。该接口可由窗口回调函数驱动，使键盘输入*仅*到达顶部窗口。
``CONFIG_NXTERM_KBDBUFSIZE``：
   如果启用了 ``CONFIG_NXTERM_NXKBDIN``，则此值可用于定义每窗口键盘输入缓冲区的大小。默认：16
``CONFIG_NXTERM_NPOLLWAITERS``：
   可以等待读取数据可用的线程数。默认：4

安装新字体
====================

**BDF 字体转换器**。在 ``tools/.`` 目录中有一个名为 *bdf-converter* 的工具。*bdf-converter* 程序可用于将位图分发格式 (BDF) 的字体转换为可在 NX 图形系统中使用的字体。BDF 格式最为人所知的是传统上用于 X-11 位图字体的字体格式。

   关于字体版权的说明：我的理解是，传统字体的底层位图字体数据不受版权保护（可缩放字体则不同）。这是因为版权仅涵盖字体的交付形式，而不涵盖底层字体内容，并且至少对于传统字体来说，底层字体设计是古老的。但是，如果您从现代的、有商标的图像转换，则可能存在问题。但请记住，我是程序员而不是律师，我对字体版权问题的了解仅限于通过 Google 搜索获得的信息。

**字体安装步骤**，以下是在 NX 图形系统中创建和安装新字体的一般说明。前两个步骤仅在您使用 BDF 字体转换器程序时适用。

#. 以 BDF 格式查找字体。X-11 捆绑了许多优秀的 BDF 位图字体。参见 `此链接 <http://www.cl.cam.ac.uk/~mgk25/ucs-fonts.html>`__ 作为示例。

#. 使用 *bdf-converter* 程序将 BDF 字体转换为 NuttX 字体格式。这将产生一个包含定义的 C 头文件。该头文件应安装在例如 ``graphics/nxfonts/nxfonts_myfont.h``。

其余步骤适用于您设法创建 NuttX C 字体头文件的任何方式。在您有了 C 字体头文件之后，下一步是创建一个新的 NuttX 配置变量来选择字体。例如，假设您定义以下变量：``CONFIG_NXFONT_MYFONT``。那么您需要：

3. 在您的 NuttX 配置文件中定义 ``CONFIG_NXFONT_MYFONT=y``。

必须为每个新字体分配一个字体 ID 号。字体 ID 在文件 ``include/nuttx/nx/nxfonts.h`` 中定义。这些定义必须扩展以支持您的新字体。查看 ``CONFIG_NXFONT_SANS23X27`` 启用的字体 ID 是如何定义的，并以类似方式为您的新字体添加 ID：

4. ``include/nuttx/nx/nxfonts.h``。将您的新字体添加为可能的系统默认字体：

   .. code-block:: c

    #if defined(CONFIG_NXFONT_SANS23X27)
    # define NXFONT_DEFAULT FONTID_SANS23X27
    #elif defined(CONFIG_NXFONT_MYFONT)
    # define NXFONT_DEFAULT FONTID_MYFONT
    #endif

   然后定义实际的字体 ID。确保字体 ID 值是唯一的：

   .. code-block:: c

    #if defined(CONFIG_NXFONT_SANS23X27)
    # define NXFONT_DEFAULT FONTID_SANS23X27
    #elif defined(CONFIG_NXFONT_MYFONT)
    # define NXFONT_DEFAULT FONTID_MYFONT
    #endif

将字体添加到 NX 构建系统。有几个文件需要修改。查看构建系统如何使用字体 CONFIG_NXFONT_SANS23X27 作为示例：

5. ``nuttx/graphics/Makefile``。此文件需要逻辑来从您使用 *bdf-converter* 程序生成的头文件自动生成 C 源文件。注意 ``NXFONTS_FONTID=2``；这必须设置为您在 ``include/nuttx/nx/nxfonts.h`` 文件中定义的相同字体 ID 值。

   .. code-block:: makefile

    genfontsources:
      ifeq ($(CONFIG_NXFONT_SANS23X27),y)
          @$(MAKE) -C nxfonts -f Makefile.sources NXFONTS_FONTID=1 EXTRAFLAGS=$(EXTRAFLAGS)
      endif
      ifeq ($(CONFIG_NXFONT_MYFONT),y)
          @$(MAKE) -C nxfonts -f Makefile.sources NXFONTS_FONTID=2 EXTRAFLAGS=$(EXTRAFLAGS)
      endif

6. ``nuttx/graphics/nxfonts/Make.defs``。设置 make 变量 ``NXFSET_CSRCS``。``NXFSET_CSRCS`` 确定当 ``NXFONTS_FONTID=2`` 时要构建的字体 C 文件的名称：

   .. code-block:: makefile

    ifeq ($(CONFIG_NXFONT_SANS23X27),y)
    NXFSET_CSRCS += nxfonts_bitmaps_sans23x27.c
    endif
    ifeq ($(CONFIG_NXFONT_MYFONT),y)
    NXFSET_CSRCS += nxfonts_bitmaps_myfont.c
    endif

7. ``nuttx/graphics/nxfonts/Makefile.sources``。这是步骤 5 中使用的 Makefile，它将实际生成字体 C 文件。因此，给定您的 NXFONTS_FONTID=2，它需要确定用于自动生成变量和函数名称的前缀，以及要创建的自动生成文件的名称（这必须与 ``nuttx/graphics/nxfonts/Make.defs`` 中使用的名称相同）：

   .. code-block:: makefile

    ifeq ($(NXFONTS_FONTID),1)
    NXFONTS_PREFIX  := g_sans23x27_
    GEN_CSRC  = nxfonts_bitmaps_sans23x27.c
    endif
    ifeq ($(NXFONTS_FONTID),2)
    NXFONTS_PREFIX  := g_myfont_
    GEN_CSRC  = nxfonts_bitmaps_myfont.c
    endif

8. ``graphics/nxfonts/nxfonts_bitmaps.c``。这是包含通用字体结构的文件。它被 ``nuttx/graphics/nxfonts/Makefile.sources`` 用作"模板"文件，在构建时创建您的自定义字体数据集。

   .. code-block:: c

    #if NXFONTS_FONTID == 1
    #  include "nxfonts_sans23x27.h"
    #elif NXFONTS_FONTID == 2
    #  include "nxfonts_myfont.h"
    #else
    #  error "No font ID specified"
    #endif

   其中 ``nxfonts_myfont.h`` 是我们在步骤 2 中使用 *bdf-converter* 工具生成的 NuttX 字体文件。

9. ``graphics/nxfonts/nxfonts_getfont.c``。最后，我们需要扩展执行运行时字体查找的逻辑，以便可以找到我们的新字体。查找函数是 ``NXHANDLE nxf_getfonthandle(enum nx_fontid_e fontid)``。注意查找基于步骤 4 中定义的字体 ID。新字体信息需要添加到该函数使用的数据结构中：

   .. code-block:: c

    #ifdef CONFIG_NXFONT_SANS23X27
    extern const struct nx_fontpackage_s g_sans23x27_package;
    #endif
    #ifdef CONFIG_NXFONT_MYFONT
    extern const struct nx_fontpackage_s g_myfont_package;
    #endif

    static FAR const struct nx_fontpackage_s *g_fontpackages[] =
    {
    #ifdef CONFIG_NXFONT_SANS23X27
      &g_sans23x27_package,
    #endif
    #ifdef CONFIG_NXFONT_MYFONT
      &g_myfont_package,
    #endif
      NULL
    };

NX 测试覆盖
================

``apps/examples/nx``。调试 NX 的主要测试工具位于 ``apps/examples/nx``。

**构建** ``apps/examples/nx``。NX 测试使用 ``apps/examples/nx`` 配合基于 Linux/Cygwin 的 NuttX 模拟器进行。构建此测试的配置文件可在 ``boards/sim/sim/sim/configs/nx`` 和 ``boards/sim/sim/sim/configs/nx11`` 中找到。有两种替代配置用于构建模拟：

#. 使用位于 ``boards/sim/sim/sim/configs/nx/defconfig`` 的配置文件的配置。此默认配置在 8 BPP 下运行 NX 逻辑，但不提供视觉反馈。在此配置中，使用了一个非常简单的模拟帧缓冲区驱动，该驱动基于一个简单的内存区域充当显存。该默认配置可按如下方式构建::

    tools/configure.sh sim:nx
    make
    ./nuttx

#. 首选配置位于 ``boards/sim/sim/sim/configs/nx11/defconfig``。此配置通过使用 X 窗口作为帧缓冲区的模拟帧缓冲区驱动扩展了测试。这是一个更优的测试配置，因为 X 窗口出现在您的桌面上，您可以看到 NX 输出。此首选配置可按如下方式构建::

    tools/configure sim:nx11
    make
    ./nuttx

   *更新*：sim 目标多年来出现了一些问题，因此需要添加以下注意事项：

   -  X 目标在最近的 Cygwin 配置下可以构建，但无法执行。（在 ``XOpenDisplay()`` 内部失败。）

   -  X 目标在当前 (9.09) Ubuntu 发行版下无法构建。我需要进行以下更改：

      构建也将无法找到 X 头文件，除非您安装 X11 开发包。

   -  参见 :doc:`/platforms/sim/sim/boards/sim/index` 文件获取更多信息。

**测试覆盖**。目前，``apps/examples/nx`` 仅运行 NX 的一个子集；其余部分基本上未经测试。下表描述了对每个 NX API 执行的测试：

NXGLIB API 测试覆盖
------------------------

================================ ==================================== ========
函数                             特殊设置/说明                        已验证
================================ ==================================== ========
``nxgl_rgb2yuv()``               .                                    否
``nxgl_yuv2rgb()``               .                                    否
``nxgl_rectcopy()``              .                                    是
``nxgl_rectoffset()``            .                                    是
``nxgl_vectoradd()``             .                                    是
``nxgl_vectorsubtract()``        .                                    是
``nxgl_rectintersect()``         .                                    是
``nxgl_rectunion()``             .                                    是
``nxgl_nonintersecting()``       .                                    是
``nxgl_rectoverlap()``           .                                    是
``nxgl_rectinside()``            .                                    是
``nxgl_rectsize()``              .                                    是
``nxgl_nullrect()``              .                                    是
``nxgl_runoffset()``             由 apps/examples/nxlines 验证。       是
``nxgl_runcopy()``               .                                    否
``nxgl_trapoffset()``            由 apps/examples/nxlines 验证。       是
``nxgl_trapcopy()``              由 apps/examples/nxlines 验证。       是
``nxgl_colorcopy``               .                                    是
``nxgl_splitline``               使用 apps/examples/nxlines 验证       是
                                 通常工作良好，但对于接近水平的宽线
                                 有一些精度/溢出问题。有一个"修正
                                 系数"似乎可以消除问题，但在某些
                                 配置中仍可能存在。
``nxgl_circlepts``               由 apps/examples/nxlines 验证。       是
``nxgl_circletraps``             由 apps/examples/nxlines 验证。       是
================================ ==================================== ========

NX 服务器回调测试覆盖
---------------------------------

============== ==================== ========
函数           特殊设置/说明        已验证
============== ==================== ========
``redraw()``   .                    是
``position()`` .                    是
``mousein()``  .                    是
``kbdin()``    .                    是
============== ==================== ========

NX API 测试覆盖
--------------------

========================= ===============================================================  ========
函数                      特殊设置/说明                                                      已验证
========================= ===============================================================  ========
``nx_runinstance()``      .                                                                是
``nx_connectinstance()``  .                                                                是
``nx_disconnect()``       .                                                                是
``nx_eventhandler()``     .                                                                是
``nx_eventnotify()``      这在当前版本的 apps/examples/nx 中未使用，                       否
                          在之前的版本中已测试
``nx_openwindow()``       在 ``<NuttX-Directory>/.config`` 文件中更改为                    是
                          ``CONFIG_EXAMPLES_NX_RAWWINDOWS=y``
``nx_closewindow()``      在 ``<NuttX-Directory>/.config`` 文件中更改为                    是
                          ``CONFIG_EXAMPLES_NX_RAWWINDOWS=y``
``nx_requestbkgd()``      由 ``apps/examples/nxtext`` 和                                    是
                          ``apps/examples/nxhello`` 验证。
``nx_releasebkgd()``      由 ``apps/examples/nxtext`` 和                                    是
                          ``apps/examples/nxhello`` 验证。
``nx_getposition()``      .                                                                否
``nx_setposition()``      在 ``<NuttX-Directory>/.config`` 文件中更改为                    是
                          ``CONFIG_EXAMPLES_NX_RAWWINDOWS=y``
``nx_setsize()``          在 ``<NuttX-Directory>/.config`` 文件中更改为                    是
                          ``CONFIG_EXAMPLES_NX_RAWWINDOWS=y``
``nx_raise()``            在 ``<NuttX-Directory>/.config`` 文件中更改为                    是
                          ``CONFIG_EXAMPLES_NX_RAWWINDOWS=y``
``nx_lower()``            在 ``<NuttX-Directory>/.config`` 文件中更改为                    是
                          ``CONFIG_EXAMPLES_NX_RAWWINDOWS=y``
``nx_modal()``            .                                                                否
``nx_setvisibility()``    使用 Twm4Nx 运行                                                  是，非正式
``nx_ishidden()``         使用 Twm4Nx 运行                                                  是，非正式
``nx_fill()``             在 ``<NuttX-Directory>/.config`` 文件中更改为                    是
                          ``CONFIG_EXAMPLES_NX_RAWWINDOWS=y``
``nx_getrectangle()``     .                                                                是
``nx_filltrapezoid()``    由 ``apps/examples/nxlines`` 验证。                                是
``nx_drawline()``         由 ``apps/examples/nxlines`` 验证。                                是
``nx_drawcircle()``       由 ``apps/examples/nxlines`` 验证。                                是
``nx_fillcircle()``       由 ``apps/examples/nxlines`` 验证。                                是
``nx_setbgcolor()``       .                                                                是
``nx_move()``             在 ``<NuttX-Directory>/.config`` 文件中更改为                    是
                          ``CONFIG_EXAMPLES_NX_RAWWINDOWS=y``
``nx_bitmap()``           在 ``<NuttX-Directory>/.config`` 文件中更改为                    是
                          ``CONFIG_EXAMPLES_NX_RAWWINDOWS=y``。
``nx_kbdin()``            .                                                                是
``nx_mousein()``          .                                                                是
========================= ===============================================================  ========

NXTK API 测试覆盖
----------------------

============================ ========================= ========
函数                         特殊设置/说明              已验证
============================ ========================= ========
``nxtk_openwindow()``        .                         是
``nxtk_closewindow()``       .                         是
``nxtk_getposition()``       .                         否
``nxtk_setposition()``       .                         是
``nxtk_setsize()``           .                         是
``nxtk_raise()``             .                         是
``nxtk_lower()``             .                         是
``nxtk_modal()``             .                         否
``nxtk_setvisibility()``     使用 Twm4Nx 运行          是，非正式
``nxtk_ishidden()``          使用 Twm4Nx 运行          是，非正式
``nxtk_fillwindow()``        .                         是
``nxtk_getwindow()``         .                         否
``nxtk_filltrapwindow()``    .                         否
``nxtk_drawlinewindow()``    .                         是
``nxtk_drawcirclewindow()``  .                         是
``nxtk_fillcirclewindow()``  .                         是
``nxtk_movewindow()``        .                         否
``nxtk_bitmapwindow()``      .                         是
``nxtk_opentoolbar()``       .                         是
``nxtk_closetoolbar()``      .                         是
``nxtk_filltoolbar()``       .                         是
``nxtk_gettoolbar()``        .                         否
``nxtk_filltraptoolbar()``   .                         否
``nxtk_drawlinetoolbar()``   .                         否
``nxtk_drawcircletoolbar()`` .                         否
``nxtk_fillcircletoolbar()`` .                         否
``nxtk_movetoolbar()``       .                         否
``nxtk_bitmaptoolbar()``     .                         否
============================ ========================= ========

NXFONTS API 测试覆盖
-------------------------

======================== ============================= ========
函数                     特殊设置/说明                  已验证
======================== ============================= ========
``nxf_getfonthandle()``  .                             是
``nxf_getfontset()``     .                             是
``nxf_getbitmap()``      .                             是
``nxf_convert_2bpp()``   .                             否
``nxf_convert_4bpp()``   .                             否
``nxf_convert_8bpp()``   构建时使用 defconfig。         是
``nxf_convert_16bpp()``  .                             是
``nxf_convert_24bpp()``  .                             否
``nxf_convert_32bpp()``  .                             是
======================== ============================= ========
