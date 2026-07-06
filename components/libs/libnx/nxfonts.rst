======
nxfont
======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本目录包含 NuttX 的字体支持。仅当在 NuttX 配置文件中定义了
CONFIG_NXFONTS 时，才会构建本目录的内容。

安装新字体
====================

在目录 tools/ 中有一个名为 bdf-converter 的工具。bdf-converter 程序
用于将位图分发格式（BDF）的字体转换为可在 NX 图形系统中使用的字体。

以下是在 NX 图形系统中创建和安装新字体的一般步骤：

#. 找到一个 BDF 格式的字体，
#. 使用 bdf-converter 程序将 BDF 字体转换为 NuttX 字体格式。这将
   生成一个包含定义的 C 头文件。该头文件应安装在例如
   ``graphics/nxfonts/nxfonts_myfont.h``。

创建一个新的 NuttX 配置变量。例如，假设您定义了以下变量：
CONFIG_NXFONT_MYFONT。那么您需要：

#. 在 NuttX 配置文件中定义 ``CONFIG_NXFONT_MYFONT=y``。

必须为每个新字体分配一个字体 ID 号。字体 ID 在文件
``include/nuttx/nx/nxfonts.h`` 中定义。需要扩展这些定义以支持
您的新字体。参考 ``CONFIG_NXFONT_SANS23X27`` 启用的字体 ID 的定义方式，
以类似方式添加您的新字体 ID：

3. ``include/nuttx/nx/nxfonts.h`` 将新字体添加为可能的系统默认字体：

       .. code-block:: C

          #if defined(CONFIG_NXFONT_SANS23X27)
          # define NXFONT_DEFAULT FONTID_SANS23X27
          #elif defined(CONFIG_NXFONT_MYFONT)
          # define NXFONT_DEFAULT FONTID_MYFONT
          #endif

          然后定义实际的字体 ID。确保字体 ID 值是唯一的：

          enum nx_fontid_e
          {
            FONTID_DEFAULT     = 0      /* The default font */
          #ifdef CONFIG_NXFONT_SANS23X27
            , FONTID_SANS23X27 = 1      /* The 23x27 sans serif font */
          #endif
          #ifdef CONFIG_NXFONT_MYFONT
            , FONTID_MYFONT    = 2      /* My shiny, new font */
          #endif
          ...

将字体添加到 NX 构建系统。需要修改多个文件来完成此操作。
参考构建系统使用 CONFIG_NXFONT_SANS23X27 字体的方式：

#. ``nuttx/graphics/Makefile``  此文件需要逻辑来从您使用 bdf-converter
   程序生成的头文件自动生成 C 源文件。注意 NXFONTS_FONTID=2；
   这必须设置为您在 ``include/nuttx/nx/nxfonts.h`` 文件中定义的
   相同的字体 ID 值。

       .. code-block:: make
                       
          genfontsources:
            ifeq ($(CONFIG_NXFONT_SANS23X27),y)
             @$(MAKE) -C nxfonts -f Makefile.sources NXFONTS_FONTID=1 EXTRAFLAGS=$(EXTRAFLAGS)
           endif
            ifeq ($(CONFIG_NXFONT_MYFONT),y)
             @$(MAKE) -C nxfonts -f Makefile.sources NXFONTS_FONTID=2 EXTRAFLAGS=$(EXTRAFLAGS)
           endif

#. ``nuttx/graphics/nxfonts/Make.defs``.  设置 make 变量 NXFSET_CSRCS。
   NXFSET_CSRCS 决定当 NXFONTS_FONTID=2 时要构建的字体 C 文件名：

       .. code-block:: make

          ifeq ($(CONFIG_NXFONT_SANS23X27),y)
          NXFSET_CSRCS += nxfonts_bitmaps_sans23x27.c
          endif
          ifeq ($(CONFIG_NXFONT_MYFONT),y)
          NXFSET_CSRCS += nxfonts_bitmaps_myfont.c
          endif

#. ``nuttx/graphics/nxfonts/Makefile.sources``.  这是步骤 5 中使用的
   Makefile，它将实际生成字体 C 文件。因此，给定您的 NXFONTS_FONTID=2，
   它需要确定用于自动生成的变量和函数名称的前缀，以及（再次）要创建的
   自动生成文件的名称（这必须与 nuttx/graphics/nxfonts/Make.defs 中
   使用的名称相同）：

       .. code-block:: C

          ifeq ($(NXFONTS_FONTID),1)
          NXFONTS_PREFIX := g_sans23x27_
          GEN_CSRC = nxfonts_bitmaps_sans23x27.c
          endif
          ifeq ($(NXFONTS_FONTID),2)
          NXFONTS_PREFIX := g_myfont_
          GEN_CSRC = nxfonts_bitmaps_myfont.c
          endif

#. ``graphics/nxfonts/nxfonts_bitmaps.c``.  这是包含通用字体结构的文件。
   ``nuttx/graphics/nxfonts/Makefile.sources`` 将其用作"模板"文件来创建
   您的自定义字体数据集。

       .. code-block:: C

          #if NXFONTS_FONTID == 1
          #  include "nxfonts_sans23x27.h"
          #elif NXFONTS_FONTID == 2
          #  include "nxfonts_myfont.h"
          #else
          #  error "No font ID specified"
          #endif

   其中 nxfonts_myfont.h 是我们在步骤 2 中使用 bdf-converter 工具
   生成的 NuttX 字体文件。

#. ``graphics/nxfonts/nxfonts_getfont.c``.  最后，我们需要扩展执行
   运行时字体查找的逻辑，以便能够找到我们的新字体。查找函数为
   NXHANDLE nxf_getfonthandle(enum nx_fontid_e fontid)。
   需要将新字体信息添加到该函数使用的数据结构中

       .. code-block:: C

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

配置设置
======================

NxFonts
-------

* ``CONFIG_NXFONTS``

  启用字体支持
* ``CONFIG_NXFONTS_CHARBITS``

  字符集中的位数。当前仅支持 7 和 8，默认为 7。

* ``CONFIG_NXFONTS_DISABLE_1BPP``、``CONFIG_NXFONTS_DISABLE_2BPP``、
  ``CONFIG_NXFONTS_DISABLE_4BPP``、``CONFIG_NXFONTS_DISABLE_8BPP``、
  ``CONFIG_NXFONTS_DISABLE_16BPP``、``CONFIG_NXFONTS_DISABLE_24BPP`` 和
  ``CONFIG_NXFONTS_DISABLE_32BPP``

  NX 支持多种像素深度。您可以通过禁用未使用的颜色深度来节省内存。

* ``CONFIG_NXFONTS_PACKEDMSFIRST``

  如果使用的像素深度小于 8 位，则 NX 需要知道像素是从 MS 到 LS
  还是从 LS 到 MS 进行打包。

字体选择
---------------

* ``CONFIG_NXFONT_SANS17X22``

  此选项启用对 17x22 小型无衬线字体的支持（字体 ID FONTID_SANS17X22 == 14）。

* ``CONFIG_NXFONT_SANS20X26``

  此选项启用对 20x26 小型无衬线字体的支持（字体 ID FONTID_SANS20X26 == 15）。

* ``CONFIG_NXFONT_SANS23X27``

  此选项启用对 23x27 小型无衬线字体的支持（字体 ID FONTID_SANS23X27 == 1）。

* ``CONFIG_NXFONT_SANS22X29``

  此选项启用对 22x29 小型无衬线字体的支持（字体 ID FONTID_SANS22X29 == 2）。

* ``CONFIG_NXFONT_SANS28X37``

  此选项启用对 28x37 中型无衬线字体的支持（字体 ID FONTID_SANS28X37 == 3）。

* ``CONFIG_NXFONT_SANS39X48``

  此选项启用对 39x48 大型无衬线字体的支持（字体 ID FONTID_SANS39X48 == 4）。

* ``CONFIG_NXFONT_SANS17X23B``

  此选项启用对 17x23 小型无衬线粗体字体的支持（字体 ID FONTID_SANS17X23B == 16）。

* ``CONFIG_NXFONT_SANS20X27B``

  此选项启用对 20x27 小型无衬线粗体字体的支持（字体 ID FONTID_SANS20X27B == 17）。

* ``CONFIG_NXFONT_SANS22X29B``

  此选项启用对 22x29 小型无衬线粗体字体的支持（字体 ID FONTID_SANS22X29B == 5）。

* ``CONFIG_NXFONT_SANS28X37B``

  此选项启用对 28x37 中型无衬线粗体字体的支持（字体 ID FONTID_SANS28X37B == 6）。

* ``CONFIG_NXFONT_SANS40X49B``

  此选项启用对 40x49 大型无衬线粗体字体的支持（字体 ID FONTID_SANS40X49B == 7）。

* ``CONFIG_NXFONT_SERIF22X29``

  此选项启用对 22x29 小型衬线字体的支持（字体 ID FONTID_SERIF22X29 == 8）。

* ``CONFIG_NXFONT_SERIF29X37``

  此选项启用对 29x37 中型衬线字体的支持（字体 ID FONTID_SERIF29X37 == 9）。

* ``CONFIG_NXFONT_SERIF38X48``

  此选项启用对 38x48 大型衬线字体的支持（字体 ID FONTID_SERIF38X48 == 10）。

* ``CONFIG_NXFONT_SERIF22X28B``
  
  此选项启用对 27x38 小型粗体衬线字体的支持（字体 ID FONTID_SERIF22X28B == 11）。

* ``CONFIG_NXFONT_SERIF27X38B``

  此选项启用对 27x38 中型粗体衬线字体的支持（字体 ID FONTID_SERIF27X38B == 12）。

* ``CONFIG_NXFONT_SERIF38X49B``

  此选项启用对 38x49 大型粗体衬线字体的支持（字体 ID FONTID_SERIF38X49B == 13）。

[REVISIT... this list is not complete]
