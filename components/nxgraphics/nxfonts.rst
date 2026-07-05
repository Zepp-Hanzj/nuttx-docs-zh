==============================
NX Fonts Support (``NXFONTS``)
==============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NXFONTS 类型
=============

.. c:struct:: nx_fontmetric_s

  此结构提供一个字形的度量信息：

  .. code-block:: c

    struct nx_fontmetric_s
    {
      uint32_t stride   : 2;      /* 一行字体的宽度（字节） */
      uint32_t width    : 6;      /* 字体的宽度（位） */
      uint32_t height   : 6;      /* 字体的高度（行） */
      uint32_t xoffset  : 6;      /* 左上角 X 偏移（像素） */
      uint32_t yoffset  : 6;      /* 左上角 Y 偏移（像素） */
      uint32_t unused   : 6;
    };

.. c:struct:: nx_fontbitmap_s

  此结构将字形度量与字形位图绑定：

  .. code-block:: c

    struct nx_fontbitmap_s
    {
      struct nx_fontmetric_s metric; /* 字符度量 */
      FAR const uint8_t *bitmap;     /* 指向字符位图的指针 */
    };

.. c:struct:: nx_fontset_s

  此结构描述一个可以由以 ``first`` 开头并通过（``first`` + ``nchars`` - 1）扩展的数组描述的连续字形分组。

  .. code-block:: c

    struct nx_fontset_s
    {
      uint8_t  first;             /* 第一个位图字符代码 */
      uint8_t  nchars;            /* 位图字符代码数量 */
      FAR const struct nx_fontbitmap_s *bitmap;
    };

.. c:struct:: nx_font_s

  此结构描述整体字体集。

  .. code-block:: c

    struct nx_font_s
    {
      uint8_t  mxheight;          /* 一个字形的最大高度（行） */
      uint8_t  mxwidth;           /* 任何字形的最大宽度（像素） */
      uint8_t  mxbits;            /* 每个字符代码的最大位数 */
      uint8_t  spwidth;           /* 空格的宽度（像素） */
    };

.. c:function:: NXHANDLE nxf_getfonthandle(enum nx_fontid_e fontid);

  给定一个数字字体 ID，返回一个后续可用于访问字体数据集的句柄。

  :param fontid: 标识要使用的字体集

  :return: 一个后续可用于访问字体数据集的句柄。

.. c:function:: FAR const struct nx_font_s *nxf_getfontset(NXHANDLE handle);

  返回关于当前字体集的信息。

  :param handle: 之前由 :c:func:`nxf_getfonthandle` 返回的字体句柄。
  :return: 描述字体集的 ``struct nx_font_s`` 实例。

.. c:function:: FAR const struct nx_fontbitmap_s *nxf_getbitmap(NXHANDLE handle, uint16_t ch)

  返回所选字符编码的字体位图信息。

  :param ch: 请求位图的字符代码。
  :param handle: 之前由 :c:func:`nxf_getfonthandle` 返回的字体句柄。
  :return: 描述字形的 :c:struct:`nx_fontbitmap_s` 实例。

.. c:function:: int nxf_convert_2bpp(FAR uint8_t *dest, uint16_t height, \
                     uint16_t width, uint16_t stride, \
                     FAR const struct nx_fontbitmap_s *bm, \
                     nxgl_mxpixel_t color);

.. c:function:: int nxf_convert_4bpp(FAR uint8_t *dest, uint16_t height, \
                     uint16_t width, uint16_t stride, \
                     FAR const struct nx_fontbitmap_s *bm, \
                     nxgl_mxpixel_t color);

.. c:function:: int nxf_convert_8bpp(FAR uint8_t *dest, uint16_t height, \
                     uint16_t width, uint16_t stride, \
                     FAR const struct nx_fontbitmap_s *bm, \
                     nxgl_mxpixel_t color);

.. c:function:: int nxf_convert_16bpp(FAR uint16_t *dest, uint16_t height, \
                      uint16_t width, uint16_t stride, \
                      FAR const struct nx_fontbitmap_s *bm, \
                      nxgl_mxpixel_t color);

.. c:function:: int nxf_convert_24bpp(FAR uint32_t *dest, uint16_t height, \
                      uint16_t width, uint16_t stride, \
                      FAR const struct nx_fontbitmap_s *bm, \
                      nxgl_mxpixel_t color);

.. c:function:: int nxf_convert_32bpp(FAR uint32_t *dest, uint16_t height, \
                      uint16_t width, uint16_t stride, \
                      FAR const struct nx_fontbitmap_s *bm, \
                      nxgl_mxpixel_t color);

  将 1BPP 字体转换为新的像素深度。

  :param dest: 调用者提供的目标缓冲区。
  :param height: 返回字符的最大高度（行）。
  :param width: 返回字符的最大宽度（像素）。
  :param stride: 目标缓冲区的宽度（字节）。
  :param bm: 描述要转换的字符字形
  :param color: 字体位图中 '1' 位使用的颜色（0 位透明）。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并适当设置 ``errno``。

宽字体支持
=================

问题::

  > 我的团队正在尝试使用中文字体的 nuttx 图形，但 nx 似乎不支持超过 256 个字符的字体，对吗？

回答::

  NuttX 当前仅使用 7 位和 8 位字符集的字体。但我认为这种限制大多是任意的。将字体子系统扩展为使用 16 位字体应该是一个简单的扩展。

添加 16 位字体支持
--------------------------

当前 7/8 位字体实现
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

所有关键字体接口都允许 16 位字符集：

.. code-block:: C

   FAR const struct nx_fontbitmap_s *nxf_getbitmap(NXHANDLE handle, uint16_t ch)

字符代码仅用于在表中查找字形。有一个控制字符集宽度的定义：CONFIG_NXFONTS_CHARBITS。当前默认为 7，但所有现有字体支持 8 位。

我的第一个猜测是，唯一需要更改的是单个文件 nxfonts_bitmaps.c（以及文件 nxfonts_getfont.c 中的函数 nxf_getglyphset()）。nxfonts_bitmaps.c 用于自动生成 7/8 位字体数据集。以下是其工作原理：

* 每个 7-8 位文件由一个头文件描述，例如 nxfonts_sans17x22.h。

* 在构建时，每个头文件用于创建一个 C 文件，例如 nxfonts_bitmaps_sans17x22.c。

* 它通过编译 nxfonts_bitmaps.c 并包含 nxfonts_sans17x22.h 在构建时创建字体数据集来创建 C 文件（如 nxfonts_bitmaps_sans17x22.c）。

nxfonts_getfont.c 中的函数 nxf_getglyphset() 选择 7 位字体范围（代码 < 128）或 8 位范围（代码 >= 128 > 256）。字体保存在简单的数组中，将数据分成值范围可以让您跳过每个范围开头和结尾的不可打印代码。代码中甚至有一条评论"也许有一天，16 位字体会出现在这里"。

添加宽字体
~~~~~~~~~~~~~~~~~

要添加单个宽字体，最简单的方法是直接添加最终的 .C 文件而不经过 C 自动生成步骤。这应该非常简单。（但由于它从未用于更大的字符集，我相信存在需要修复的错误和问题）。

如果您要添加许多宽字体，那么也许您需要创建一个新版本的 C 自动生成逻辑。这需要更多的努力。

我愿意提供帮助和建议。在 NuttX 图形中拥有良好的宽字符支持将是 NuttX 的一个重要改进。这不是很多代码，也不是非常困难的代码，所以您不应该让它成为障碍。

字体存储问题
-------------------

一个潜在的问题可能是包含数千个字符的字体所需的内存量。如果您有大量的 flash，这可能不是问题，但在许多微控制器上这将相当受限。

选项包括：

* **字体压缩** 在 NuttX 中添加一些字体压缩算法。然而，中文字体位图压缩效果不佳：许多包含的数据太多，没有什么可压缩的。某些在特定压缩算法下实际上会膨胀。

* **大容量存储** 更好的选择是将宽字体放在文件系统中，放在 NAND 或串行 FLASH 上，或放在 SD 卡上。在这种情况下，需要额外的逻辑来 (1) 格式化字体二进制文件和 (2) 根据需要从文件系统访问字体二进制文件。
