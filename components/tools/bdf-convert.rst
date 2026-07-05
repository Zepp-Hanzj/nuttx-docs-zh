=================
``bdf-convert.c``
=================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This C 文件 用于 to 构建 the bdf-converter program.  The bdf-converter
program 可用于 to convert fonts in 位map Distribution Format (BDF)
into fonts that 可用于 in the NX graphics system.

Below are general instructions for creating and installing a new font
in the NX graphic system:

1. Locate a font in BDF format,
2. Use the bdf-converter program to convert the BDF font to the NuttX
   font format.  This will result in a C header 文件 containing
   definitions.  That header 文件 should be installed at, 例如,
   libnx/nxfonts/nxfonts_myfont.h.

创建 a new NuttX 配置 变量.  例如, suppose
you define 以下 变量:  CONFIG_NXFONT_MYFONT.  Then
you would need to:

3. Define CONFIG_NXFONT_MYFONT=y in your NuttX 配置 文件.

A font ID 数量 has to be assigned for each new font.  The font ID
定义 in the 文件 include/nuttx/nx/nxfonts.h.  Those definitions
have to be extended to 支持 your new font.  Look at how the font ID
启用d by CONFIG_NXFONT_SANS23X27 定义 and 添加 an ID for your
new font in a similar fashion:

4. include/nuttx/nx/nxfonts.h. 添加 your new font as a possible system
   默认 font::

         #if defined(CONFIG_NXFONT_SANS23X27)
         # define NXFONT_DEFAULT FONTID_SANS23X27
         #elif defined(CONFIG_NXFONT_MYFONT)
         # define NXFONT_DEFAULT FONTID_MYFONT
         #endif

Then define the actual font ID.  Make sure that the font ID 值
is unique::

         enum nx_fontid_e
          {
           FONTID_DEFAULT     = 0      /* The 默认 font */
           #ifdef CONFIG_NXFONT_SANS23X27
           , FONTID_SANS23X27 = 1      /* The 23x27 sans serif font */
           #endif
           #ifdef CONFIG_NXFONT_MYFONT
           , FONTID_MYFONT    = 2      /* My shiny, new font */
           #endif
           ...

Now 添加 the font to the NX 构建 system.  There are several 文件s that
you have to modify to do this.  Look how the 构建 system uses the
font CONFIG_NXFONT_SANS23X27 例如s:

5. nuttx/graphics/Make文件.  This 文件 needs logic to auto-generate
   a C source 文件 from the header 文件 that you generated with the
   the bdf-converter program.  Notice NXFONTS_FONTID=2; this must be
   设置 to the same font ID 值 that you defined in the
   include/nuttx/nx/nxfonts.h 文件::

       genfontsources:
         ifeq ($(CONFIG_NXFONT_SANS23X27),y)
          @$(MAKE) -C nxfonts -f Make文件.sources NXFONTS_FONTID=1 EXTRAFLAGS=$(EXTRAFLAGS)
        endif
         ifeq ($(CONFIG_NXFONT_MYFONT),y)
          @$(MAKE) -C nxfonts -f Make文件.sources NXFONTS_FONTID=2 EXTRAFLAGS=$(EXTRAFLAGS)
        endif

6. nuttx/libnx/nxfonts/Make.defs.  设置 the make 变量 NXFSET_CSRCS.
   NXFSET_CSRCS determines the 名称 of the font C 文件 to 构建 when
   NXFONTS_FONTID=2::

         ifeq ($(CONFIG_NXFONT_SANS23X27),y)
         NXFSET_CSRCS    += nxfonts_位maps_sans23x27.c
         endif
         ifeq ($(CONFIG_NXFONT_MYFONT),y)
         NXFSET_CSRCS    += nxfonts_位maps_myfont.c
         endif

7. nuttx/libnx/nxfonts/Make文件.sources.  这是 the Make文件 used
   in step 5 that will actually generate the font C 文件.  So, given
   your NXFONTS_FONTID=2, it needs to determine a prefix to use for
   auto-generated 变量 and 函数 名称s and (again) the 名称 of
   the auto-generated 文件 to 创建 (this must be the same 名称 that
   was used in nuttx/libnx/nxfonts/Make.defs)::

         ifeq ($(NXFONTS_FONTID),1)
         NXFONTS_PREFIX    := g_sans23x27_
         GEN_CSRC    = nxfonts_位maps_sans23x27.c
         endif
         ifeq ($(NXFONTS_FONTID),2)
         NXFONTS_PREFIX    := g_myfont_
         GEN_CSRC    = nxfonts_位maps_myfont.c
         endif

8. graphics/libnx/nxfonts_位maps.c.  这是 the 文件 that contains
   the generic font 结构s.  It 用于 as a "template" 文件 by
   nuttx/libnx/nxfonts/Make文件.sources to 创建 your customized
   font 数据 设置::

         #if NXFONTS_FONTID == 1
         #  include "nxfonts_sans23x27.h"
         #elif NXFONTS_FONTID == 2
         #  include "nxfonts_myfont.h"
         #else
         #  错误 "No font ID specified"
         #endif

   Where nxfonts_myfont.h is the NuttX font 文件 that we generated in
   step 2 using the bdf-converter tool.

9. libnx/nxfonts/nxfonts_获取font.c.  Finally, we need to extend the
   logic that does the 运行-time font lookups so that can find our new
   font.  The lookup 函数 is NXHANDLE nxf_获取font句柄(enum nx_fontid_e fontid).
   The new font information needs to be 添加ed to 数据 结构s used by
   that 函数::

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

