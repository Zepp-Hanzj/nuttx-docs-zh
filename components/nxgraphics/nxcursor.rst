================================
NX Cursor Support (``NXCURSOR``)
================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

.. c:function:: int nxcursor_enable(NXHANDLE hnd, bool enable)

  启用/禁用光标的显示。禁用的光标仍然存在并且仍然可以被控制，但在显示器上不可见。

  :param hnd:
     由 :c:func:`nx_connect` 返回的服务器句柄。
  :param enable: 新的光标位置

  :return: 成功时返回 OK；失败时返回 ERROR 并适当设置 errno。

.. c:function:: int nxcursor_setimage(NXHANDLE hnd, FAR const struct nx_cursorimage_s *image)

  设置光标图像。

  图像以每像素 2 位的图像提供。两位编码如下：

  - 00：透明背景。
  - 01：Color1：光标的主颜色。
  - 10：Color2：任何边框的颜色。
  - 11：Color3：用于更好成像的混合颜色（伪抗锯齿）。

  **注意：** NX 逻辑将反复引用用户图像缓冲区。该图像缓冲区必须在 NX 服务器连接持续期间持续存在。

  :param hnd: 由 :c:func:`nx_connect` 返回的服务器句柄
  :param image:
    描述光标图像的 ``struct struct nx_cursorimage_s`` 实例。参见 ``<nuttx/nx/nxcursor.h>`` 获取此结构的完整描述。

  :return: 成功时返回 OK；失败时返回 ERROR 并适当设置 errno。

.. c:function:: int nxcursor_setposition(NXHANDLE hnd, FAR const struct nxgl_point_s *pos)

  将光标移动到指定位置。

  :param hnd: 由 :c:func:`nx_connect` 返回的服务器句柄
  :param pos: 新的光标位置

  :return: 成功时返回 OK；失败时返回 ERROR 并适当设置 errno。
