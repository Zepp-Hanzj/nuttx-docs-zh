.. _nx-graphics-library-nxgl-1:

==============================
NX Graphics Library (``NXGL``)
==============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NXGL 提供了许多 API，有些可供 NX 内部使用，有些也可供应用程序使用。此处仅记录供应用程序使用的 API。参见 ``include/nuttx/nx/nxglib.h`` 获取完整的 API 集合；如果您直接渲染到帧缓冲区或 LCD 内存，这些 API 可能会引起您的兴趣。

NXGL 类型
----------

.. c:type:: nxgl_mxpixel_t

  持有一个设备像素。NXGLIB 将选择刚好包含像素的 ``nxgl_mxpixel_t`` 最小大小：如果禁用了 16、24 和 32 分辨率支持则为 ``byte``，如果禁用了 24 和 32 分辨率支持则为 ``uint16_t``，否则为 ``uint32_t``。

.. c:type:: nxgl_coord_t

  给定坐标受限于屏幕高度和宽度。如果任一值超过 32,767 像素，则需要更改以下内容：

.. c:struct:: nxgl_point_s

  描述显示器上的一个点：

  .. code-block:: c

    struct nxgl_point_s
    {
      nxgl_coord_t x;         /* X 位置，范围：0 到屏幕宽度 - 1 */
      nxgl_coord_t y;         /* Y 位置，范围：0 到屏幕高度 - 1 */
    };

.. c:struct:: nxgl_size_s

  描述矩形区域的大小。

  .. code-block:: c

    struct nxgl_size_s
    {
      nxgl_coord_t w;        /* 宽度（像素） */
      nxgl_coord_t h;        /* 高度（行） */
    };

.. c:struct:: nxgl_rect_s

  描述显示器上的一个定位矩形。

  .. code-block:: c

    struct nxgl_rect_s
    {
      struct nxgl_point_s pt1; /* 左上角 */
      struct nxgl_point_s pt2; /* 右下角 */
    };

.. c:struct:: nxgl_run_s

  描述一个游程，即一条水平线。注意起始/结束位置具有分数精度。这对于当更复杂的形状分解为梯形时梯形的良好连接是必要的。

  .. code-block:: c

    struct nxgl_run_s
    {
      b16_t        x1;        /* 左侧 X 位置，范围：0 到 x2 */
      b16_t        x2;        /* 右侧 X 位置，范围：x1 到屏幕宽度 - 1 */
      nxgl_coord_t y;         /* 顶部 Y 位置，范围：0 到屏幕高度 - 1 */
    };

.. c:struct:: nxgl_trapezoid_s

  描述显示器上的一个水平梯形，以梯形顶部和底部的游程表示。

  .. code-block:: c

    struct nxgl_trapezoid_s
    {
      struct nxgl_run_s top;  /* 顶部游程 */
      struct nxgl_run_s bot;  /* 底部游程 */
    };

.. c:function:: void nxgl_rgb2yuv(uint8_t r, uint8_t g, uint8_t b, uint8_t *y, uint8_t *u, uint8_t *v)

  将 8 位 RGB 三元组转换为 8 位 YUV 三元组。

.. c:function:: void nxgl_yuv2rgb(uint8_t y, uint8_t u, uint8_t v, uint8_t *r, uint8_t *g, uint8_t *b);

  将 8 位 YUV 三元组转换为 8 位 RGB 三元组。

.. c:function:: void nxgl_rectcopy(FAR struct nxgl_rect_s *dest, FAR const struct nxgl_rect_s *src)

  这本质上是矩形的 ``memcpy()``。我们不做结构赋值，因为某些编译器对此处理不好。

.. c:function:: void nxgl_rectoffset(FAR struct nxgl_rect_s *dest, \
                     FAR const struct nxgl_rect_s *src, \
                     nxgl_coord_t dx, nxgl_coord_t dy);

  按指定的 dx、dy 值偏移矩形位置。

.. c:function:: void nxgl_vectoradd(FAR struct nxgl_point_s *dest, \
                    FAR const struct nxgl_point_s *v1, \
                    FAR const struct nxgl_point_s *v2);

 将两个 2x1 向量相加并将结果保存到第三个。

.. c:function:: void nxgl_vectsubtract(FAR struct nxgl_point_s *dest, \
                       FAR const struct nxgl_point_s *v1, \
                       FAR const struct nxgl_point_s *v2);

  从向量 ``v1`` 中减去向量 ``v2`` 并将结果返回到向量 dest。

.. c:function:: void nxgl_rectintersect(FAR struct nxgl_rect_s *dest, \
                        FAR const struct nxgl_rect_s *src1, \
                        FAR const struct nxgl_rect_s *src2);

  返回表示两个矩形交集的矩形。

.. c:function:: void nxgl_rectunion(FAR struct nxgl_rect_s *dest, \
                    FAR const struct nxgl_rect_s *src1, \
                    FAR const struct nxgl_rect_s *src2);

  给定两个矩形 ``src1`` 和 ``src2``，返回包含两者的更大矩形 ``dest``。

.. c:function:: void nxgl_nonintersecting(FAR struct nxgl_rect_s result[4], \
                     FAR const struct nxgl_rect_s *rect1, \
                     FAR const struct nxgl_rect_s *rect2);

  返回矩形 ``rect1`` 中不与 ``rect2`` 相交的区域。这将返回四个矩形，其中一些可能是退化的（可以用 :c:func:`nxgl_nullrect` 挑出）。

.. c:function:: bool nxgl_rectoverlap(FAR struct nxgl_rect_s *rect1, \
                      FAR struct nxgl_rect_s *rect2);

  如果两个矩形重叠则返回 true。

.. c:function:: bool nxgl_rectinside(FAR const struct nxgl_rect_s *rect, \
                     FAR const struct nxgl_point_s *pt);

  如果点 ``pt`` 位于 ``rect`` 内则返回 true。

.. c:function:: void nxgl_rectsize(FAR struct nxgl_size_s *size, \
                   FAR const struct nxgl_rect_s *rect);

  返回指定矩形的大小。

.. c:function:: bool nxgl_nullrect(FAR const struct nxgl_rect_s *rect);

  如果矩形面积 <= 0 则返回 true。

.. c:function:: void nxgl_runoffset(FAR struct nxgl_run_s *dest, \
                    FAR const struct nxgl_run_s *src, \
                    nxgl_coord_t dx, nxgl_coord_t dy);

  按指定的 ``dx``、``dy`` 值偏移游程位置。

.. c:function:: void nxgl_runcopy(FAR struct nxgl_run_s *dest, \
                  FAR const struct nxgl_run_s *src);

  这本质上是游程的 ``memcpy()``。我们不做结构赋值，因为某些编译器对此处理不好。

.. c:function:: void nxgl_trapoffset(FAR struct nxgl_trapezoid_s *dest, \
                     FAR const struct nxgl_trapezoid_s *src, \
                     nxgl_coord_t dx, nxgl_coord_t dy);

  按指定的 ``dx``、``dy`` 值偏移梯形位置。

.. c:function:: void nxgl_trapcopy(FAR struct nxgl_trapezoid_s *dest, \
                   FAR const struct nxgl_trapezoid_s *src);

  这本质上是梯形的 ``memcpy()``。我们不做结构赋值，因为某些编译器对此处理不好。

.. c:function:: void nxgl_colorcopy(nxgl_mxpixel_t dest[CONFIG_NX_NPLANES], \
               const nxgl_mxpixel_t src[CONFIG_NX_NPLANES]);

  这本质上是颜色的 ``memcpy()``。这对我们来说除了在一个地方隐藏所有平面颜色的条件编译之外没有其他作用。

.. c:function:: int nxgl_splitline(FAR struct nxgl_vector_s *vector, FAR struct nxgl_trapezoid_s *traps, \
                   FAR struct nxgl_rect_s *rect, nxgl_coord_t linewidth);

  在一般情况下，有宽度的线可以表示为一个平行四边形，顶部和底部各有一个三角形。三角形和平行四边形都是梯形的退化版本。此函数将宽线分解为三角形和梯形。此函数还检测其他退化情况：

  #. 如果 ``y1 == y2``，则线是水平的，更适合表示为矩形。
  #. 如果 ``x1 == x2``，则线是垂直的，也更适合表示为矩形。
  #. 如果线的宽度为 1，则顶部和底部没有三角形（如果宽度较窄且线接近垂直，也可能如此）。
  #. 如果线以某些角度定向，它可能仅由上下三角形组成，中间没有梯形。在这种情况下，将返回 3 个梯形，但 traps[1] 将是退化的。

  :param vector: 指向描述要绘制的线的向量的指针。
  :param traps: 指向梯形数组（大小 3）的指针。
  :param rect: 指向矩形的指针。

  :return:
    - 0：线成功分解为三个梯形。traps[0]、traps[1] 和 traps[2] 中的值有效。
    - 1：线成功表示为一个梯形。traps[1] 中的值有效。
    - 2：线成功表示为一个矩形。rect 中的值有效。
    - <0：错误时，返回取反的 errno 值。

.. c:function:: void nxgl_circlepts(FAR const struct nxgl_point_s *center, nxgl_coord_t radius, \
                    FAR struct nxgl_point_s *circle);

  给定圆的描述，返回圆周上的 16 个点。然后这些点可由 :c:func:`nx_drawcircle` 或相关 API 用于绘制圆的轮廓。

  :param center: 指向圆心点的指针。
  :param radius: 圆的半径（像素）。
  :param circle: 指向 16 个点数组中第一个条目的指针，圆点将返回到此处。

.. c:function:: void nxgl_circletraps(FAR const struct nxgl_point_s *center, nxgl_coord_t radius, \
                     FAR struct nxgl_trapezoid_s *circle);

  给定圆的描述，返回 8 个梯形，可用于通过 :c:func:`nx_fillcircle` 和其他接口填充圆。

  :param center: 指向圆心点的指针。
  :param radius: 圆的半径（像素）。
  :param circle: 指向 8 个梯形数组中第一个条目的指针，圆的描述将返回到此处。
