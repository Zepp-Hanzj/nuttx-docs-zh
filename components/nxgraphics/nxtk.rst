======================
NX Tool Kit (``NXTK``)
======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NXTK implements where the *framed 窗口*. NX framed 窗口s consist of
three components within one NX 窗口:

  #. The 窗口 *border*,
  #. The main *client 窗口* area, and
  #. A *toolbar* area

Each sub-窗口 represents a region within one 窗口. `Figure
1 <#屏幕shot>`__ shows some simple NX framed 窗口s. NXTK allows
these sub-窗口s to be managed more-or-less independently:

  -  Each component has its own callbacks for redraw and position events
     as well as mouse and keyboard 输入s. The client sub-窗口 callbacks
     are 注册ed when the framed 窗口 is 创建d with a call to
     :c:func:`nxtk_打开窗口`; Separate toolbar
     sub-窗口 callbacks are reigistered when the toolbar is 添加ed using
     :c:func:`nxtk_打开toolbar`. (NOTES: (1) only the
     client sub-窗口 接收s keyboard 输入 and, (2) border callbacks
     are not currently accessible by the user).
  -  All position informational provided within the callback is relative
     to the specific sub-窗口. That is, the origin (0,0) of the
     coordinate system for each sub-窗口 begins at the top left
     corner of the sub窗口. This means that toolbar logic need not
     be concerned about client 窗口 geometry (and vice versa) and,
     例如, common toolbar logic 可用于 with different 窗口s.

.. c:type:: FAR void *NXTKWINDOW

  这是 the 句柄 that 可用于 to access the 窗口 数据 region.

.. c:function:: int nxtk_block(NXWINDOW hwnd, FAR void *arg)

  The response to this 函数 call is two things: (1)
  any queued callback messages to the 窗口 are 'blocked' and then (2)
  also subsequent 窗口 messaging is blocked.

  The ``event`` callback with the ``NXEVENT_BLOCKED`` event is the
  response from ``nxtk_block()``. This blocking 接口 用于 to
  assure that no further messages are are directed to the 窗口. Receipt
  of the ``NXEVENT_BLOCKED`` event signifies that (1) there are no further
  pending callbacks and (2) that the 窗口 is now *defunct* and will
  接收 no further callbacks.

  This callback 支持s coordinated destruction of a 窗口. The client
  窗口 logic must stay intact until all of the queued callbacks are
  processed. Then the 窗口 may be safely 关闭d. Closing the 窗口
  prior with pending callbacks can lead to bad behavior when the callback
  is 执行d.

  :param wnd: The 窗口 to be blocked
  :param arg: An 参数 that will accompany the block messages (这是 ``arg2`` in
    the event callback).

  :返回: OK on 成功; ERROR on 失败 with errno 设置
    appropriately.

.. c:function:: int nxtk_synch(NXWINDOW hwnd, FAR void *arg);

  This 接口 可用于 to synchronize the 窗口
  client with the NX server. It really just implements an *echo*: A synch
  message is sent from the 窗口 client to the server which then responds
  immediately by 发送ing the ``NXEVENT_SYNCHED`` back to the 窗口s
  client.

  Due to the highly asynchronous nature of client-server communications,
  ``nx_synch()`` is sometimes necessary to assure that the client and
  server are fully synchronized in time.

  Usage by the 窗口 client might be something like this:

  .. code-block:: c

    extern bool g_synched;
    extern sem_t g_synch_sem;

    g_synched = false;
    ret = nxtk_synch(hfwnd, 句柄);
    if (ret < 0)
      {
         -- 句柄 the 错误 --
      }

    while (!g_synched)
      {
        ret = sem_wait(&g_sync_sem);
        if (ret < 0)
          {
             -- 句柄 the 错误 --
          }
      }

  When the 窗口 listener th读取 接收s the ``NXEVENT_SYNCHED`` event,
  it would set ``g_synched`` to ``true`` and post ``g_synch_sem``, waking
  up the above loop.

  :param wnd:
     The 窗口 to be synched
  :param arg:
     An 参数 that will accompany the synch messages (这是 ``arg2``
     in the event callback).

  :返回: OK on 成功; ERROR on 失败 with errno 设置
    appropriately

.. c:function:: NXTKWINDOW nxtk_openwindow(NXHANDLE handle, uint8_t flags, \
                           FAR const struct nx_callback_s *cb, \
                           FAR void *arg);

  创建 a new, framed 窗口.

  :param 句柄:
     The 句柄 返回ed by ```nx_连接()`` <#nx连接instance>`__.
  :param flags:
     选项al flags. These include:

     -  ``NXBE_WINDOW_RAMBACKED``: 创建s a RAM backed 窗口. This
        选项 is only valid if ``CONFIG_NX_RAMBACKED`` 启用.
     -  ``NXBE_WINDOW_HIDDEN``: The 窗口 is 创建 in the HIDDEN state
        and can be made visible later with ``nxtk_设置visibility()``.

  :param cb:
     Callbacks used to process 窗口 events
  :param arg:
     User provided 参数 (see ```nx_打开窗口()`` <#nx打开窗口>`__)

  :返回: Success: A non-NULL 句柄 used with subsequent NXTK 窗口 accesses
    Failure: NULL is 返回ed and errno is 设置 appropriately.

.. c:function:: int nxtk_closewindow(NXTKWINDOW hfwnd);

  关闭 the 窗口 打开ed by
  ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_getposition(NXTKWINDOW hfwnd);

  Request the position and 大小 information for the
  selected framed 窗口. The 大小/position for the client 窗口 and
  toolbar will be 返回 asynchronously through the client callback
  函数 指针.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_setposition(NXTKWINDOW hfwnd, FAR struct nxgl_point_s *pos);

  设置 the position for the selected client 窗口. This
  position does not include the off设置s for the borders nor for any
  toolbar. Those off设置s will be 添加ed in to 设置 the full 窗口 position.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param pos:
     The new position of the client sub-窗口

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_setsize(NXTKWINDOW hfwnd, FAR struct nxgl_size_s *size);

  设置 the 大小 for the selected client 窗口. This 大小
  does not include the 大小s of the borders nor for any toolbar. Those
  大小s will be 添加ed in to 设置 the full 窗口 大小.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param 大小:
     The new 大小 of the client sub-窗口.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_raise(NXTKWINDOW hfwnd);

  Bring the 窗口 containing the specified client
  sub-窗口 to the top of the 显示.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__ specifying the 窗口 to
     be raised.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_lower(NXTKWINDOW hfwnd);

  Lower the 窗口 containing the specified client
  sub-窗口 to the bottom of the 显示.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__ specifying the 窗口 to
     be lowered.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_modal(NXWINDOW hwnd, bool modal);

  May be used to either (1) raise a 窗口 to the top of
  the 显示 and select modal behavior, or (2) 禁用 modal behavior.

  :param hwnd:
     The 句柄 返回ed by ```nxtk_打开窗口()`` <#nxtk打开窗口>`__
     specifying the 窗口 to be modified.
  :param modal:
     True: enter modal state; False: leave modal state

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_setvisibility(NXWINDOW hwnd, bool hide);

  Select if the 窗口 is visible or hidden. A hidden
  窗口 is still present and will update normally, but will not be
  visible on the 显示 until it is unhidden.

  :param hwnd:
     The 句柄 返回ed by ```nxtk_打开窗口()`` <#nxtk打开窗口>`__
     specifying the 窗口 to be modified.
  :param hide:
     True: 窗口 will be hidden; false: 窗口 will be visible

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: bool nxtk_ishidden(NXTKWINDOW hfwnd);

  返回 true if the 窗口 is hidden.

  **NOTE**: There will be a delay between the time that the visibility of
  the 窗口 is changed via
  ```nxtk_设置visibily()`` <#nxtk设置visibility>`__ before that new 设置
  is reported by ``nxtk_ishidden()``. ``nxtk_synch()`` may be used if
  temporal synchronization 需要.

  :param hfwnd:
     The 句柄 返回ed by ```nxtk_打开窗口()`` <#nxtk打开窗口>`__
     that identifies the 窗口 to be queried.

  :返回: *True*: the 窗口 is hidden, *false*: the 窗口 is
    visible

.. c:function:: int nxtk_fillwindow(NXTKWINDOW hfwnd, FAR const struct nxgl_rect_s *rect, \
                    nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES]);

  Fill the specified rectangle in the client 窗口 with
  the specified 颜色.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param rect:
     The location within the client 窗口 to be filled
  :param 颜色:
     The 颜色 to use in the fill

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: void nxtk_getwindow(NXTKWINDOW hfwnd, FAR const struct nxgl_rect_s *rect, \
                    unsigned int plane, FAR uint8_t *dest, \
                    unsigned int deststride);

  获取 the raw contents of graphic 内存 within a
  rectangular region. 注意： Since raw graphic 内存 is 返回ed, the
  返回ed 内存 content may be the 内存 of 窗口s above this one and
  may not necessarily belong to this 窗口 unless you assure that this is
  the top 窗口.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param rect:
     The location within the client 窗口 to be retrieved.
  :param plane:
     Specifies the 颜色 plane to 获取 from.
  :param dest:
     The location to copy the 内存 region
  :param deststride:
     The 宽度, in 字节s, of the dest 内存

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_filltrapwindow(NXTKWINDOW hfwnd, \
                        FAR const struct nxgl_trapezoid_s *trap, \
                        nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES]);

  Fill the specified trapezoid in the client 窗口 with
  the specified 颜色

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param trap:
     The trapezoidal region to be filled.
  :param 颜色:
     The 颜色 to use in the fill.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_drawlinewindow(NXTKWINDOW hfwnd, FAR struct nxgl_vector_s *vector, \
                        nxgl_coord_t 宽度, nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES], \
                        uint8_t caps);

  Fill the specified trapezoidal region in the 窗口
  with the specified 颜色. Fill the specified line in the 窗口 with the
  specified 颜色. 这是 simply a wrapper that uses ``nxgl_splitline()``
  to break the line into trapezoids and then calls
  ``nxtk_filltrap窗口()`` to render the line.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param vector:
     Describes the line to be drawn.
  :param 宽度:
     The 宽度 of the line
  :param 颜色:
     The 颜色 to use to fill the line
  :param caps:
     Draw a circular cap on the ends of the line to 支持 better line
     joins. One of:

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_drawcirclewindow(NXTKWINDOW hfwnd, FAR const struct nxgl_point_s *center, \
                          nxgl_coord_t radius, nxgl_coord_t 宽度, \
                          nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES]);

  Draw a circular outline using the specified line
  thickness and 颜色.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param center:
     A 指针 to the point that is the center of the circle.
  :param radius:
     The radius of the circle in 像素s.
  :param 宽度:
     The 宽度 of the line
  :param 颜色:
     The 颜色 to use to fill the line

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_fillcirclewindow(NXWINDOW hfwnd, FAR const struct nxgl_point_s *center, \
                          nxgl_coord_t radius, nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES]);

  Fill a circular region using the specified 颜色.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param center:
     A 指针 to the point that is the center of the circle.
  :param radius:
     The 宽度 of the line
  :param 颜色:
     The 颜色 to use to fill the circle

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_movewindow(NXTKWINDOW hfwnd, FAR const struct nxgl_rect_s *rect, \
                    FAR const struct nxgl_point_s *off设置);

  Move a rectangular region within the client sub-窗口
  of a framed 窗口.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__ specifying the client
     sub-窗口 within which the move is to be done.
  :param rect:
     Describes the rectangular region relative to the client sub-窗口 to
     move.
  :param off设置:
     The off设置 to move the region

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_bitmapwindow(NXTKWINDOW hfwnd, \
                      FAR const struct nxgl_rect_s *dest, \
                      FAR const void *src[CONFIG_NX_NPLANES], \
                      FAR const struct nxgl_point_s *origin, \
                      unsigned int stride);

  Copy a rectangular region of a larger 图像 into the
  rectangle in the specified client sub-窗口.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__ specifying the client
     sub-窗口 that will 接收 the 位map.
  :param dest:
     Describes the rectangular region on in the client sub-窗口 will
     接收 the 位 map.
  :param src:
     The 启动 of the source 图像(s). 这是 an array source 图像s of
     大小 ``CONFIG_NX_NPLANES`` (probably 1).
  :param origin:
     The origin of the upper, left-most corner of the full 位map. Both
     dest and origin are in sub-窗口 coordinates, however, the origin
     may lie outside of the sub-窗口 显示.
  :param stride:
     The 宽度 of the full source 图像 in 像素s.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_opentoolbar(NXTKWINDOW hfwnd, nxgl_coord_t height, \
                     FAR const struct nx_callback_s *cb, \
                     FAR void *arg);

  创建 a tool bar at the top of the specified framed
  窗口.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param 高度:
     The requested 高度 of the toolbar in 像素s.
  :param cb:
     Callbacks used to process toolbar events.
  :param arg:
     User provided 值 that will be 返回ed with toolbar callbacks.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_closetoolbar(NXTKWINDOW hfwnd);

  移除 the tool bar at the top of the specified framed
  窗口.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_filltoolbar(NXTKWINDOW hfwnd, FAR const struct nxgl_rect_s *rect, \
                     nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES]);

  Fill the specified rectangle in the toolbar sub-窗口
  with the specified 颜色.

  :param hfwnd:
    A 句柄 previously 返回ed by
    ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param rect:
    The location within the toolbar 窗口 to be filled.
  :param 颜色:
    The 颜色 to use in the fill.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_gettoolbar(NXTKWINDOW hfwnd, FAR const struct nxgl_rect_s *rect, \
                    unsigned int plane, FAR uint8_t *dest, \
                    unsigned int deststride);

  获取 the raw contents of graphic 内存 within a
  rectangular region. 注意： Since raw graphic 内存 is 返回ed, the
  返回ed 内存 content may be the 内存 of 窗口s above this one and
  may not necessarily belong to this 窗口 unless you assure that this is
  the top 窗口.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param rect:
     The location within the toolbar 窗口 to be retrieved.
  :param plane:
     Specifies the 颜色 plane to 获取 from.
  :param dest:
     The location to copy the 内存 region.
  :param deststride:
     The 宽度, in 字节s, of the dest 内存.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_filltraptoolbar(NXTKWINDOW hfwnd, FAR const struct nxgl_trapezoid_s *trap, \
                         nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES]);

  Fill the specified trapezoid in the toolbar sub-窗口
  with the specified 颜色.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param trap:
     The trapezoidal region to be filled
  :param 颜色:
     The 颜色 to use in the fill

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_drawlinetoolbar(NXTKWINDOW hfwnd, FAR struct nxgl_vector_s *vector, \
                         nxgl_coord_t 宽度, nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES], \
                         uint8_t caps);

  Fill the specified line in the toolbar sub-窗口 with
  the specified 颜色. 这是 simply a wrapper that uses
  ``nxgl_splitline()`` to break the line into trapezoids and then calls
  ``nxtk_filltraptoolbar()`` to render the line.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param vector:
     Describes the line to be drawn.
  :param 宽度:
     The 宽度 of the line
  :param 颜色:
     The 颜色 to use to fill the line
  :param caps:
     Draw a circular cap on the ends of the line to 支持 better line
     joins. One of:

     .. code-block:: c

      /* Line caps */

      #define NX_LINECAP_NONE  0x00, /* No line caps */
      #define NX_LINECAP_PT1   0x01  /* Line cap on pt1 on of the vector only */
      #define NX_LINECAP_PT2   0x02  /* Line cap on pt2 on of the vector only */
      #define NX_LINECAP_BOTH  0x03  /* Line cap on both ends of the vector only */

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_drawcircletoolbar(NXTKWINDOW hfwnd, FAR const struct nxgl_point_s *center, \
                           nxgl_coord_t radius, nxgl_coord_t 宽度, \
                           nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES]);

  Draw a circular outline using the specified line
  thickness and 颜色.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param center:
     A 指针 to the point that is the center of the circle.
  :param radius:
     The radius of the circle in 像素s.
  :param 宽度:
     The 宽度 of the line
  :param 颜色:
     The 颜色 to use to fill the line

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_fillcircletoolbar(NXWINDOW hfwnd, FAR const struct nxgl_point_s *center, \
                           nxgl_coord_t radius, nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES]);

  Fill a circular region using the specified 颜色.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param center:
     A 指针 to the point that is the center of the circle.
  :param radius:
     The 宽度 of the line
  :param 颜色:
     The 颜色 to use to fill the circle

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_movetoolbar(NXTKWINDOW hfwnd, FAR const struct nxgl_rect_s *rect, \
                     FAR const struct nxgl_point_s *off设置);

  Move a rectangular region within the toolbar sub-窗口
  of a framed 窗口.

  :param hfwnd:
     A 句柄 identifying sub-窗口 containing the toolbar within which
     the move is to be done. This 句柄 must have previously been
     返回ed by ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param rect:
     Describes the rectangular region relative to the toolbar sub-窗口
     to move.
  :param off设置:
     The off设置 to move the region

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nxtk_bitmaptoolbar(NXTKWINDOW hfwnd, \
                       FAR const struct nxgl_rect_s *dest, \
                       FAR const void *src[CONFIG_NX_NPLANES], \
                       FAR const struct nxgl_point_s *origin, \
                       unsigned int stride);

  Copy a rectangular region of a larger 图像 into the
  rectangle in the specified toolbar sub-窗口.

  :param hfwnd:
     A 句柄 previously 返回ed by
     ```nxtk_打开窗口()`` <#nxtk打开窗口>`__.
  :param dest:
     Describes the rectangular region on in the toolbar sub-窗口 will
     接收 the 位 map.
  :param src:
     The 启动 of the source 图像.
  :param origin:
     The origin of the upper, left-most corner of the full 位map. Both
     dest and origin are in sub-窗口 coordinates, however, the origin
     may lie outside of the sub-窗口 显示.
  :param stride:
     The 宽度 of the full source 图像 in 字节s.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. _nx-fonts-support-nxfonts-1:

