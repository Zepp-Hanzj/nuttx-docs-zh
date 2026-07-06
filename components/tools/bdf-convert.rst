=================
``bdf-convert.c``
=================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此 C 文件用于构建 bdf-converter 程序。bdf-converter
程序可用于将位图分发格式（BDF）中的字体
转换为可在 NX 图形系统中使用的字体。

以下是在 NX 图形系统中创建和安装新字体的一般说明：

1. 找到一个 BDF 格式的字体，
2. 使用 bdf-converter 程序将 BDF 字体转换为 NuttX
   字体格式。这将生成一个包含
   定义的 C 头文件。该头文件应安装在例如
   libnx/nxfonts/nxfonts_myfont.h 的位置。

创建一个新的 NuttX 配置变量。例如，假设
你定义了以下变量：CONFIG_NXFONT_MYFONT。那么
你需要：

3. 在你的 NuttX 配置文件中定义 CONFIG_NXFONT_MYFONT=y。

每个新字体都需要分配一个字体 ID 编号。字体 ID
定义在文件 include/nuttx/nx/nxfonts.h 中。这些定义
需要扩展以支持你的新字体。查看 CONFIG_NXFONT_SANS23X27
启用的字体 ID 如何定义，并以类似的方式
为你的新字体添加一个 ID：

4. include/nuttx/nx/nxfonts.h。将你的新字体添加为可能的系统
   默认字体::

         #if defined(CONFIG_NXFONT_SANS23X27)
         # define NXFONT_DEFAULT FONTID_SANS23X27
         #elif defined(CONFIG_NXFONT_MYFONT)
         # define NXFONT_DEFAULT FONTID_MYFONT
         #endif

然后定义实际的字体 ID。确保字体 ID 值
是唯一的::

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

现在将字体添加到 NX 构建系统中。你需要修改
几个文件来完成此操作。查看构建系统如何使用
字体 CONFIG_NXFONT_SANS23X27 的示例：

5. nuttx/graphics/Makefile。此文件需要自动从
   bdf-converter 程序生成的头文件生成 C 源文件的
   逻辑。注意 NXFONTS_FONTID=2；这必须
   设置为你在 include/nuttx/nx/nxfonts.h 文件中
   定义的相同字体 ID 值::

       genfontsources:
         ifeq ($(CONFIG_NXFONT_SANS23X27),y)
          @$(MAKE) -C nxfonts -f Makefile.sources NXFONTS_FONTID=1 EXTRAFLAGS=$(EXTRAFLAGS)
        endif
         ifeq ($(CONFIG_NXFONT_MYFONT),y)
          @$(MAKE) -C nxfonts -f Makefile.sources NXFONTS_FONTID=2 EXTRAFLAGS=$(EXTRAFLAGS)
        endif

6. nuttx/libnx/nxfonts/Make.defs。设置 make 变量 NXFSET_CSRCS。
   NXFSET_CSRCS 决定了 NXFONTS_FONTID=2 时要构建的
   字体 C 文件的名称::

         ifeq ($(CONFIG_NXFONT_SANS23X27),y)
         NXFSET_CSRCS    += nxfonts_bitmaps_sans23x27.c
         endif
         ifeq ($(CONFIG_NXFONT_MYFONT),y)
         NXFSET_CSRCS    += nxfonts_bitmaps_myfont.c
         endif

7. nuttx/libnx/nxfonts/Makefile.sources。这是步骤 5 中使用的
   Makefile，它将实际生成字体 C 文件。因此，给定
   你的 NXFONTS_FONTID=2，它需要确定用于自动生成的
   变量和函数名称的前缀，以及（再次）要创建的
   自动生成文件的名称（这必须与 nuttx/libnx/nxfonts/Make.defs
   中使用的名称相同）::

         ifeq ($(NXFONTS_FONTID),1)
         NXFONTS_PREFIX    := g_sans23x27_
         GEN_CSRC    = nxfonts_bitmaps_sans23x27.c
         endif
         ifeq ($(NXFONTS_FONTID),2)
         NXFONTS_PREFIX    := g_myfont_
         GEN_CSRC    = nxfonts_bitmaps_myfont.c
         endif

8. graphics/libnx/nxfonts_bitmaps.c。这是包含
   通用字体结构的文件。它被 nuttx/libnx/nxfonts/Makefile.sources
   用作"模板"文件来创建你的自定义
   字体数据集::

         #if NXFONTS_FONTID == 1
         #  include "nxfonts_sans23x27.h"
         #elif NXFONTS_FONTID == 2
         #  include "nxfonts_myfont.h"
         #else
         #  error "No font ID specified"
         #endif

   其中 nxfonts_myfont.h 是我们在步骤 2 中使用 bdf-converter 工具
   生成的 NuttX 字体文件。

9. libnx/nxfonts/nxfonts_getfont.c。最后，我们需要扩展
   运行时字体查找的逻辑，以便能够找到我们的新
   字体。查找函数是 NXHANDLE nxf_getfonthandle(enum nx_fontid_e fontid)。
   新的字体信息需要添加到该函数使用的
   数据结构中::

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
