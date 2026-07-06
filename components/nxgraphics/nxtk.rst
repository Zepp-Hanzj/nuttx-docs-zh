======================
NX 工具包 (``NXTK``)
======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NXTK 实现了*框架窗口*。NX 框架窗口在单个 NX 窗口中包含三个组成部分：

  #. 窗口*边框*，
  #. 主*客户窗口*区域，以及
  #. *工具栏*区域

每个子窗口代表一个窗口内的某个区域。`图 1 <#screenshot>`__
展示了一些简单的 NX 框架窗口示例。NXTK 允许对这些子窗口进行相对独立的管理：

  -  每个组件都有自己的回调函数，用于处理重绘、位置事件以及鼠标和键盘输入。客户子窗口的回调函数在通过
     :c:func:`nxtk_openwindow` 创建框架窗口时注册；工具栏子窗口的回调函数在通过
     :c:func:`nxtk_opentoolbar` 添加工具栏时注册。（注意：(1)
     只有客户子窗口会接收键盘输入，(2) 边框回调函数目前不对用户开放。）
  -  回调中提供的所有位置信息都是相对于特定子窗口的。也就是说，每个子窗口的坐标系原点
     (0,0) 位于该子窗口的左上角。这意味着工具栏逻辑无需关心客户窗口的几何信息（反之亦然），例如，通用的工具栏逻辑可以在不同的窗口中复用。

.. c:type:: FAR void *NXTKWINDOW

  这是用于访问窗口数据区域的句柄。

.. c:function:: int nxtk_block(NXWINDOW hwnd, FAR void *arg)

  调用此函数会产生两个效果：(1)
  该窗口的所有已排队的回调消息将被"阻塞"，(2)
  后续的窗口消息也将被阻塞。

  ``NXEVENT_BLOCKED`` 事件的 ``event`` 回调是
  ``nxtk_block()`` 的响应。此阻塞接口用于确保不再有消息发送到该窗口。收到
  ``NXEVENT_BLOCKED`` 事件表示：(1) 没有待处理的回调，且 (2)
  该窗口已处于*失效*状态，不会再收到任何回调。

  此回调支持窗口的协调销毁。客户窗口逻辑必须保持完整，直到所有已排队的回调都被处理完毕，然后才能安全地关闭窗口。如果在有待处理回调的情况下关闭窗口，可能会导致回调执行时出现异常行为。

  :param wnd: 要被阻塞的窗口
  :param arg: 伴随阻塞消息的参数（在事件回调中为 ``arg2``）。

  :return: 成功时返回 OK；失败时返回 ERROR 并设置相应的 errno。

.. c:function:: int nxtk_synch(NXWINDOW hwnd, FAR void *arg);

  此接口用于同步窗口客户端与 NX
  服务器。它实际上实现了一个*回显*机制：同步消息从窗口客户端发送到服务器，服务器立即通过将
  ``NXEVENT_SYNCHED`` 发送回窗口客户端来进行响应。

  由于客户端-服务器通信具有高度异步性，``nx_synch()``
  有时是必要的，以确保客户端和服务器在时间上完全同步。

  窗口客户端的用法示例如下：

  .. code-block:: c

    extern bool g_synched;
    extern sem_t g_synch_sem;

    g_synched = false;
    ret = nxtk_synch(hfwnd, handle);
    if (ret < 0)
      {
         -- Handle the error --
      }

    while (!g_synched)
      {
        ret = sem_wait(&g_sync_sem);
        if (ret < 0)
          {
             -- Handle the error --
          }
      }

  当窗口监听线程收到 ``NXEVENT_SYNCHED`` 事件时，会将 ``g_synched``
  设置为 ``true`` 并释放 ``g_synch_sem`` 信号量，从而唤醒上述循环。

  :param wnd:
     要同步的窗口
  :param arg:
     伴随同步消息的参数（在事件回调中为 ``arg2``）。

  :return: 成功时返回 OK；失败时返回 ERROR 并设置相应的 errno。

.. c:function:: NXTKWINDOW nxtk_openwindow(NXHANDLE handle, uint8_t flags, \
                           FAR const struct nx_callback_s *cb, \
                           FAR void *arg);

  创建一个新的框架窗口。

  :param handle:
     由 ```nx_connect()`` <#nxconnectinstance>`__ 返回的句柄。
  :param flags:
     可选标志，包括：

     -  ``NXBE_WINDOW_RAMBACKED``：创建 RAM 支持的窗口。此选项仅在启用
        ``CONFIG_NX_RAMBACKED`` 时有效。
     -  ``NXBE_WINDOW_HIDDEN``：以隐藏状态创建窗口，之后可通过
        ``nxtk_setvisibility()`` 使其可见。

  :param cb:
     用于处理窗口事件的回调函数。
  :param arg:
     用户提供的参数（参见 ```nx_openwindow()`` <#nxopenwindow>`__）。

  :return: 成功时返回一个非 NULL 的句柄，用于后续 NXTK 窗口操作；失败时返回 NULL 并设置相应的
    errno。

.. c:function:: int nxtk_closewindow(NXTKWINDOW hfwnd);

  关闭由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 打开的窗口。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_getposition(NXTKWINDOW hfwnd);

  请求指定框架窗口的位置和大小信息。客户窗口和工具栏的大小/位置将通过客户回调函数指针异步返回。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_setposition(NXTKWINDOW hfwnd, FAR struct nxgl_point_s *pos);

  设置指定客户窗口的位置。此位置不包括边框或工具栏的偏移量。这些偏移量会被自动添加，以设置完整的窗口位置。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param pos:
     客户子窗口的新位置。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_setsize(NXTKWINDOW hfwnd, FAR struct nxgl_size_s *size);

  设置指定客户窗口的大小。此大小不包括边框或工具栏的尺寸。这些尺寸会被自动添加，以设置完整的窗口大小。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param size:
     客户子窗口的新大小。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_raise(NXTKWINDOW hfwnd);

  将包含指定客户子窗口的窗口提升到显示的最顶层。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄，指定要提升的窗口。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_lower(NXTKWINDOW hfwnd);

  将包含指定客户子窗口的窗口降低到显示的最底层。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄，指定要降低的窗口。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_modal(NXWINDOW hwnd, bool modal);

  可用于：(1) 将窗口提升到显示的最顶层并启用模态行为，或 (2) 禁用模态行为。

  :param hwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 返回的句柄，指定要修改的窗口。
  :param modal:
     True：进入模态状态；False：退出模态状态。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_setvisibility(NXWINDOW hwnd, bool hide);

  设置窗口是否可见。隐藏的窗口仍然存在并会正常更新，但在取消隐藏之前不会在显示上可见。

  :param hwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 返回的句柄，指定要修改的窗口。
  :param hide:
     True：窗口将被隐藏；False：窗口将可见。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: bool nxtk_ishidden(NXTKWINDOW hfwnd);

  如果窗口处于隐藏状态则返回 true。

  **注意**：通过 ```nxtk_setvisibility()`` <#nxtksetvisibility>`__
  更改窗口可见性后，在 ``nxtk_ishidden()``
  报告新设置之前会有一段延迟。如果需要时间同步，可以使用
  ``nxtk_synch()``。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 返回的句柄，标识要查询的窗口。

  :return: *True*：窗口已隐藏；*false*：窗口可见。

.. c:function:: int nxtk_fillwindow(NXTKWINDOW hfwnd, FAR const struct nxgl_rect_s *rect, \
                    nxgl_mxpixel_t color[CONFIG_NX_NPLANES]);

  用指定颜色填充客户窗口中的指定矩形区域。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param rect:
     客户窗口内要填充的位置。
  :param color:
     填充使用的颜色。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: void nxtk_getwindow(NXTKWINDOW hfwnd, FAR const struct nxgl_rect_s *rect, \
                    unsigned int plane, FAR uint8_t *dest, \
                    unsigned int deststride);

  获取矩形区域内图形内存的原始内容。注意：由于返回的是原始图形内存，返回的内存内容可能是位于此窗口之上的其他窗口的内存，除非确保此窗口是最顶层窗口，否则内容不一定属于此窗口。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param rect:
     客户窗口内要检索的位置。
  :param plane:
     指定要获取的颜色平面。
  :param dest:
     复制内存区域的目标位置。
  :param deststride:
     目标内存的宽度（以字节为单位）。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_filltrapwindow(NXTKWINDOW hfwnd, \
                        FAR const struct nxgl_trapezoid_s *trap, \
                        nxgl_mxpixel_t color[CONFIG_NX_NPLANES]);

  用指定颜色填充客户窗口中的指定梯形区域。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param trap:
     要填充的梯形区域。
  :param color:
     填充使用的颜色。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_drawlinewindow(NXTKWINDOW hfwnd, FAR struct nxgl_vector_s *vector, \
                        nxgl_coord_t width, nxgl_mxpixel_t color[CONFIG_NX_NPLANES], \
                        uint8_t caps);

  在窗口中用指定颜色绘制指定线段。这实际上是一个封装函数，使用
  ``nxgl_splitline()`` 将线段分解为梯形，然后调用
  ``nxtk_filltrapwindow()`` 来渲染线段。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param vector:
     描述要绘制的线段。
  :param width:
     线段的宽度。
  :param color:
     绘制线段使用的颜色。
  :param caps:
     在线段端点绘制圆形端帽，以支持更好的线段连接。取值为：

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_drawcirclewindow(NXTKWINDOW hfwnd, FAR const struct nxgl_point_s *center, \
                          nxgl_coord_t radius, nxgl_coord_t width, \
                          nxgl_mxpixel_t color[CONFIG_NX_NPLANES]);

  使用指定的线宽和颜色绘制圆形轮廓。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param center:
     指向圆心的指针。
  :param radius:
     圆的半径（以像素为单位）。
  :param width:
     线段的宽度。
  :param color:
     绘制线段使用的颜色。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_fillcirclewindow(NXWINDOW hfwnd, FAR const struct nxgl_point_s *center, \
                          nxgl_coord_t radius, nxgl_mxpixel_t color[CONFIG_NX_NPLANES]);

  使用指定颜色填充圆形区域。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param center:
     指向圆心的指针。
  :param radius:
     圆的半径。
  :param color:
     填充圆形使用的颜色。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_movewindow(NXTKWINDOW hfwnd, FAR const struct nxgl_rect_s *rect, \
                    FAR const struct nxgl_point_s *offset);

  移动框架窗口客户子窗口内的矩形区域。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄，指定要执行移动操作的客户子窗口。
  :param rect:
     描述相对于客户子窗口的要移动的矩形区域。
  :param offset:
     移动区域的偏移量。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_bitmapwindow(NXTKWINDOW hfwnd, \
                      FAR const struct nxgl_rect_s *dest, \
                      FAR const void *src[CONFIG_NX_NPLANES], \
                      FAR const struct nxgl_point_s *origin, \
                      unsigned int stride);

  将较大图像中的矩形区域复制到指定客户子窗口的矩形区域中。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄，指定接收位图的客户子窗口。
  :param dest:
     描述客户子窗口中接收位图的矩形区域。
  :param src:
     源图像的起始地址。这是一个大小为 ``CONFIG_NX_NPLANES``（通常为 1）的源图像数组。
  :param origin:
     完整位图左上角的原点。dest 和 origin 均使用子窗口坐标，但 origin 可能位于子窗口显示区域之外。
  :param stride:
     完整源图像的宽度（以像素为单位）。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_opentoolbar(NXTKWINDOW hfwnd, nxgl_coord_t height, \
                     FAR const struct nx_callback_s *cb, \
                     FAR void *arg);

  在指定框架窗口的顶部创建工具栏。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param height:
     请求的工具栏高度（以像素为单位）。
  :param cb:
     用于处理工具栏事件的回调函数。
  :param arg:
     用户提供的值，将在工具栏回调中返回。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_closetoolbar(NXTKWINDOW hfwnd);

  移除指定框架窗口顶部的工具栏。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_filltoolbar(NXTKWINDOW hfwnd, FAR const struct nxgl_rect_s *rect, \
                     nxgl_mxpixel_t color[CONFIG_NX_NPLANES]);

  用指定颜色填充工具栏子窗口中的指定矩形区域。

  :param hfwnd:
    由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param rect:
    工具栏窗口内要填充的位置。
  :param color:
    填充使用的颜色。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_gettoolbar(NXTKWINDOW hfwnd, FAR const struct nxgl_rect_s *rect, \
                    unsigned int plane, FAR uint8_t *dest, \
                    unsigned int deststride);

  获取矩形区域内图形内存的原始内容。注意：由于返回的是原始图形内存，返回的内存内容可能是位于此窗口之上的其他窗口的内存，除非确保此窗口是最顶层窗口，否则内容不一定属于此窗口。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param rect:
     工具栏窗口内要检索的位置。
  :param plane:
     指定要获取的颜色平面。
  :param dest:
     复制内存区域的目标位置。
  :param deststride:
     目标内存的宽度（以字节为单位）。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_filltraptoolbar(NXTKWINDOW hfwnd, FAR const struct nxgl_trapezoid_s *trap, \
                         nxgl_mxpixel_t color[CONFIG_NX_NPLANES]);

  用指定颜色填充工具栏子窗口中的指定梯形区域。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param trap:
     要填充的梯形区域。
  :param color:
     填充使用的颜色。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_drawlinetoolbar(NXTKWINDOW hfwnd, FAR struct nxgl_vector_s *vector, \
                         nxgl_coord_t width, nxgl_mxpixel_t color[CONFIG_NX_NPLANES], \
                         uint8_t caps);

  在工具栏子窗口中用指定颜色绘制指定线段。这实际上是一个封装函数，使用
  ``nxgl_splitline()`` 将线段分解为梯形，然后调用
  ``nxtk_filltraptoolbar()`` 来渲染线段。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param vector:
     描述要绘制的线段。
  :param width:
     线段的宽度。
  :param color:
     绘制线段使用的颜色。
  :param caps:
     在线段端点绘制圆形端帽，以支持更好的线段连接。取值为：

     .. code-block:: c

      /* Line caps */

      #define NX_LINECAP_NONE  0x00, /* No line caps */
      #define NX_LINECAP_PT1   0x01  /* Line cap on pt1 on of the vector only */
      #define NX_LINECAP_PT2   0x02  /* Line cap on pt2 on of the vector only */
      #define NX_LINECAP_BOTH  0x03  /* Line cap on both ends of the vector only */

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_drawcircletoolbar(NXTKWINDOW hfwnd, FAR const struct nxgl_point_s *center, \
                           nxgl_coord_t radius, nxgl_coord_t width, \
                           nxgl_mxpixel_t color[CONFIG_NX_NPLANES]);

  使用指定的线宽和颜色绘制圆形轮廓。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param center:
     指向圆心的指针。
  :param radius:
     圆的半径（以像素为单位）。
  :param width:
     线段的宽度。
  :param color:
     绘制线段使用的颜色。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_fillcircletoolbar(NXWINDOW hfwnd, FAR const struct nxgl_point_s *center, \
                           nxgl_coord_t radius, nxgl_mxpixel_t color[CONFIG_NX_NPLANES]);

  使用指定颜色填充圆形区域。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param center:
     指向圆心的指针。
  :param radius:
     圆的半径。
  :param color:
     填充圆形使用的颜色。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_movetoolbar(NXTKWINDOW hfwnd, FAR const struct nxgl_rect_s *rect, \
                     FAR const struct nxgl_point_s *offset);

  移动框架窗口工具栏子窗口内的矩形区域。

  :param hfwnd:
     标识包含工具栏的子窗口的句柄，用于执行移动操作。此句柄必须由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回。
  :param rect:
     描述相对于工具栏子窗口的要移动的矩形区域。
  :param offset:
     移动区域的偏移量。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. c:function:: int nxtk_bitmaptoolbar(NXTKWINDOW hfwnd, \
                       FAR const struct nxgl_rect_s *dest, \
                       FAR const void *src[CONFIG_NX_NPLANES], \
                       FAR const struct nxgl_point_s *origin, \
                       unsigned int stride);

  将较大图像中的矩形区域复制到指定工具栏子窗口的矩形区域中。

  :param hfwnd:
     由 ```nxtk_openwindow()`` <#nxtkopenwindow>`__ 先前返回的句柄。
  :param dest:
     描述工具栏子窗口中接收位图的矩形区域。
  :param src:
     源图像的起始地址。
  :param origin:
     完整位图左上角的原点。dest 和 origin 均使用子窗口坐标，但 origin 可能位于子窗口显示区域之外。
  :param stride:
     完整源图像的宽度（以字节为单位）。

  :return: 成功时返回 ``OK``；失败时返回 ``ERROR`` 并设置相应的
    ``errno``。

.. _nx-fonts-support-nxfonts-1:
