==
NX
==

概述
========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NX provides a tiny 窗口ing system in the spirit of X, but greatly scaled
down and appropriate for most resource-limited embedded environments.
The current NX implementation 支持s the general following, high-level
特性s:

* **Virtual Vertical Graphics Space** 窗口s that reside in a virtual,
  vertical space so that it makes sense to talk about one 窗口 being
  on top of another and obscuring the 窗口 below it.

* **Client/Server Model** A standard client server/model was adopted.
  NX may be considered a server and other logic that presents the 窗口s
  are NX clients.

* **Multi-User 支持** NX includes front-end logic to an NX server
  daemon that can serve multiple NX client th读取s. The NX sever
  th读取/daemon serializes graphics 操作s from multiple clients.
  
* **Minimal Graphics Tool设置** The actual implementation of the graphics
  操作s is performed by common, back-end logic. This back-end 支持s
  only a primitive 设置 of graphic and rendering 操作s.

* **设备 接口** NX 支持s any graphics 设备 either of two
  设备 接口s:

  #. Any 设备 with random access video 内存 using the NuttX frame缓冲区
     驱动 接口 (see include/nuttx/video/fb.h).
  #. Any LCD-like 设备 than can accept raster line 运行s through a parallel
     or serial 接口 (see include/nuttx/lcd/lcd.h). By 默认, NX is
     configured to use the frame 缓冲区 驱动 unless CONFIG_NX_LCDDRIVER
     定义 =y in your NuttX 配置 文件.

* **Transparent to NX Client** The 窗口 client on "sees" the sub-窗口
  that is operates in and does not need to be concerned with the virtual,
  vertical space (other that to respond to redraw requests from NX when needed).

* **Framed 窗口s and Toolbars** NX also 添加s the capability to 支持
  窗口s with frames and toolbars on top of the basic 窗口ing 支持.
  These are 窗口s such as those shown in the 屏幕shot above. These framed
  窗口s sub-divide one one 窗口 into three relatively independent
  sub窗口s: A frame, the contained 窗口 and an (选项al) toolbar 窗口.

* **Mouse 支持** NX provides 支持 for a mouse or other X/Y pointing
  设备s. APIs 提供 to allow external 设备s to give X/Y position
  information and mouse button presses to NX. NX will then provide the mouse
  输入 to the relevant 窗口 clients via callbacks. Client 窗口s only
  接收 the mouse 输入 callback if the mouse is positioned over a visible
  portion of the client 窗口; X/Y position 提供 to the client in the
  relative coordinate system of the client 窗口.

* **Keyboard 输入** NX also 支持s keyboard/keypad 设备s. APIs 提供
  to allow external 设备s to give keypad information to NX. NX will then
  provide the mouse 输入 to the top 窗口 on the 显示 (the 窗口 that
  has the focus) via a callback 函数.

预处理器定义
=========================

The 默认 server message queue 名称 used by the :c:macro:`nx_运行` macro:

.. code-block:: c

  #define NX_DEFAULT_SERVER_MQNAME "/dev/nxs"

Mouse button 位s:

.. code-block:: c

  #define NX_MOUSE_NOBUTTONS    0x00
  #define NX_MOUSE_LEFTBUTTON   0x01
  #define NX_MOUSE_CENTERBUTTON 0x02
  #define NX_MOUSE_RIGHTBUTTON  0x04

NX 类型
========

The 接口 to the NX server is managed using a opaque 句柄:

.. c:type:: FAR void *NXHANDLE

The 接口 to a specific 窗口 is managed using an opaque 句柄:

.. c:type:: FAR void *NXWINDOW

These define callbacks that must be provided to :c:func:`nx_打开窗口`.
These callbacks will be invoked as part of the processing performed by
:c:func:`nx_event句柄r`.

.. c:struct:: nx_callback_s

  .. code-block:: c

    struct nx_callback_s
    {
      void (*redraw)(NXWINDOW hwnd, FAR const struct nxgl_rect_s *rect,
                     bool more, FAR void *arg);
      void (*position)(NXWINDOW hwnd, FAR const struct nxgl_大小_s *大小,
                       FAR const struct nxgl_point_s *pos,
                       FAR const struct nxgl_rect_s *bounds,
                       FAR void *arg);
    #ifdef CONFIG_NX_XYINPUT
      void (*mousein)(NXWINDOW hwnd, FAR const struct nxgl_point_s *pos,
                      uint8_t buttons, FAR void *arg);
    #endif
    #ifdef CONFIG_NX_KBD
      void (*kbdin)(NXWINDOW hwnd, uint8_t nch, FAR const uint8_t *ch, FAR void *arg);
    #endif
    };

Starting the NX Server
======================

The *NX Server* is a kernel daemon that 接收s and serializes graphic
commands. Before you can use the NX graphics system, you must first
启动 this daemon. There are two ways that this can be done:

#. The NX server may be 启动ed in your board 启动up logic by simply
   calling the 函数 ``nxmu_启动()``. The board 启动up logic
   usually resides the ``boards/arch/chip/board/src`` 目录. The
   board 启动up logic can 运行 automatically during the early system if
   ``CONFIG_BOARD_LATE_INITIALIZE`` 定义 in the 配置. Or,
   the board 启动up logic can 执行 under control of the application
   by calling :c:func:`boardctl` as:

   .. code-block:: c

     boardctl(BOARDIOC_INIT, arg)

   The board initialization logic will 运行 in either case and the simple
   call to ``nxmu_启动()`` will 启动 the NX server.

#. The NX server may also be 启动ed later by the application via
   :c:func:`boardctl` as:

   .. code-block:: c

     boardctl(BOARDIOC_NX_START, arg)

.. c:function:: int nxmu_start(int display, int plane);

  Provides a wrapper 函数 to
  simplify and standardize the 启动ing of the NX server.

  :param 显示: The 显示 数量 to be served by this new NXMU instance.
  :param plane: The plane 数量 to use to 获取 information about the 显示 geometry and 颜色 format.

  :返回: Zero (``OK``) is 返回ed on 成功. This indicates
    that the NX server has been 成功fully 启动ed, is 运行ning, and
    waiting to accept 连接ions from NX clients.
    A negated ``errno`` value is returned on failure. The ``errno`` value
    indicates the nature of the 失败.

NX Server Callbacks
===================

.. c:function:: void redraw(NXWINDOW hwnd, FAR const struct nxgl_rect_s *rect, bool more, FAR void *arg);

  NX requests that the client re-draw the portion of the
  窗口 within with rectangle.

  :param hwnd:
     The 句柄 创建d by :c:func:`nx_打开窗口` or :c:func:`nx_requestbkgd`
  :param rect:
     The rectangle that needs to be re-drawn (in 窗口 relative
     coordinates)
  :param more:
     true: More re-draw requests will follow
  :param arg:
     User provided 参数 (see :c:func:`nx_打开窗口`)

.. c:function:: void position(NXWINDOW hwnd, FAR const struct nxgl_size_s *size, \
              FAR const struct nxgl_point_s *pos, \
              FAR const struct nxgl_rect_s *bounds, \
              FAR void *arg);

  The 大小 or position of the 窗口 has changed (or the
  窗口 was just 创建d with zero 大小.

  :param hwnd:
     The 句柄 创建d by :c:func:`nx_打开窗口` or :c:func:`nx_requestbkgd`
  :param 大小:
     The 大小 of the 窗口
  :param pos:
     The position of the upper left hand corner of the 窗口 on the
     overall 显示
  :param bounds:
     The bounding rectangle that the describes the entire 显示
  :param arg:
     User provided 参数 (see :c:func:`nx_打开窗口`)

.. c:function:: void mousein(NXWINDOW hwnd, FAR const struct nxgl_point_s *pos, \
             uint8_t buttons, FAR void *arg);

  New mouse 数据 可用 for the 窗口

  :param hwnd:
     The 句柄 创建d by :c:func:`nx_打开窗口` or :c:func:`nx_requestbkgd`
  :param pos:
     The (x,y) position of the mouse
  :param buttons:
     See ``NX_MOUSE_*`` definitions
  :param arg:
     User provided 参数 (see :c:func:`nx_打开窗口`)

.. c:var:: void (*kbdin)(NXWINDOW hwnd, uint8_t nch, FAR const uint8_t *ch, FAR void *arg);

  New keyboard/keypad 数据 可用 for the 窗口.

  :param hwnd:
       The 句柄 创建d by :c:func:`nx_打开窗口` or :c:func:`nx_requestbkgd`
  :param nch:
     The 数量 of characters that 可用 in ch[]
  :param ch:
     The array of characters
  :param arg:
     User provided 参数 (see :c:func:`nx_打开窗口`)

.. c:var:: void (*event)(NXWINDOW hwnd, enum nx_event_e event, FAR void *arg1, FAR void *arg2);

  This callback 用于 to communicate server events to the 窗口 listener.

  - ``NXEVENT_BLOCKED``: Window messages are blocked.
     This callback is the response from :c:func:`nx_block`,
     :c:func:`nxtk_block`. Those blocking 接口s 用于
     to assure that no further messages are directed to the 窗口.
     Receipt of the blocked callback signifies that (1) there are no
     further pending callbacks and (2) that the 窗口 is now *defunct*
     and will 接收 no further callbacks. This callback 支持s
     coordinated destruction of a 窗口. In the multi-user mode, the
     client 窗口 logic must stay intact until all of the queued
     callbacks are processed. Then the 窗口 may be safely 关闭d.
     Closing the 窗口 prior with pending callbacks can lead to bad
     behavior when the callback is 执行d.
  - ``NXEVENT_SYNCHED``: Synchronization handshake
     This completes the handshake 启动ed by
     :c:func:`nx_synch`, or :c:func:`nxtk_synch`.
     Those 接口s 发送 a synchronization messages to the NX server
     which responds with this event. The sleeping client is awakened and
     continues graphics processing, completing the handshake. Due to the
     highly asynchronous nature of client-server communications,
     synchronization is sometimes necessary to assure that the client and
     server are working to获取her properly.

  :param hwnd:
     T窗口 句柄 of 窗口 receiving the event
  :param event:
     The server event
  :param arg1:
     User provided 参数 (see :c:func:`nx_打开窗口`,
     :c:func:`nx_requestbkgd`, or :c:func:`nxtk_打开toolbar`)
  :param arg2:
     TUser provided 参数 (see :c:func:`nx_block`, :c:func:`nxtk_block`,
     :c:func:`nx_synch`, or :c:func:`nxtk_synch`)

.. c:macro:: nx_run(fb)

  .. code-block:: c

    #define nx_运行(fb) nx_运行instance(NX_DEFAULT_SERVER_MQNAME, dev)

.. c:function:: int nx_runinstance(FAR const char *mqname, FAR struct fb_vtable_s *fb)

  这是 the server entry point. It does not 返回; the
  calling th读取 is dedicated to 支持ing NX server.

  NOTE that multiple instances of the NX server may 运行 at the same time,
  with different callback and message queue 名称s. ``nx_运行()`` is simply
  a macro that 可用于 when only one server instance 需要. In
  that case, a 默认 server 名称 用于.

  :param mq名称: The 名称 for the server incoming message queue
  :param dev: Frame缓冲区 or LCD 驱动 "object" to be used

  :返回: This 函数 usually does not 返回. If it does
    return, it will return ``ERROR`` and ``errno`` will be set
    appropriately.

.. c:macro:: nx_connect(cb)

  .. code-block:: c

    #define nx_连接(cb) nx_连接instance(NX_DEFAULT_SERVER_MQNAME)

.. c:function:: NXHANDLE nx_connectinstance(FAR const char *svrmqname);

  打开 a 连接ion from a client to the NX server. One
  one client 连接ion is normally needed per th读取 as each 连接ion
  can host multiple 窗口s.

  NOTES:

  -  This 函数 返回 before the 连接ion is fully instantiated. it
     is necessary to wait for the 连接ion event before using the
     返回ed 句柄.
  -  Multiple instances of the NX server may 运行 at the same time, each
     with different message queue 名称s.
  -  ``nx_连接()`` is simply a macro that 可用于 when only one
     server instance 需要. In that case, a 默认 server 名称 is
     used.

  :param svrmq名称: The 名称 for the server incoming message queue

  :返回: Success: A non-NULL 句柄 used with subsequent NX accesses
    Failure: NULL is 返回ed and errno is 设置 appropriately.

.. c:function:: void nx_disconnect(NXHANDLE handle)

  Dis连接 a client from the NX server and/or 释放
  resources reserved by :c:func:`nx_连接`/c:func:`nx_连接instance`.

  :param 句柄: The 句柄 返回ed by :c:func:`nx_连接instance`.

.. c:function:: int nx_eventhandler(NXHANDLE handle);

  The client code must call this 函数 periodically to
  process incoming messages from the server. If ``CONFIG_NX_BLOCKING`` is
  defined, then this 函数 not 返回 until a server message is
  接收d.

  When ``CONFIG_NX_BLOCKING`` is not defined, the client must exercise
  caution in the looping to assure that it does not eat up all of the CPU
  band宽度 calling nx_event句柄r repeatedly.
  ```nx_eventnotify()`` <#nxeventnotify>`__ may be called to 获取 a signal
  event whenever a new incoming server event 可用.

  :param 句柄: The 句柄 返回ed by ```nx_连接()`` <#nx连接instance>`__.

  :返回:
    -  ``OK``: No errors occurred. If ``CONFIG_NX_BLOCKING`` is defined,
       then one or more server messages were processed.
    -  ``ERROR``: An error occurred and ``errno`` has been set
       appropriately. Of particular interest, it will 返回
       ``errno == EHOSTDOWN`` when the server is dis连接ed. After that
       event, the 句柄 can no longer be used.

.. c:function:: int nx_eventnotify(NXHANDLE handle, int signo);

  Rather than calling :c:func:`nx_event句柄r` periodically, the client may
  注册 to 接收 a signal when a server event 可用. The
  client can then call :c:func:nx_event句柄r` only
  when incoming events 可用.

  The underlying implementation used ``mq_notifiy()`` and, as a result,
  the client must observe the rules for using ``mq_notifiy()``:

  -  Only one event is signalled. Upon receipt of the signal, if the
     client wishes further notifications, it must call
     ``nx_eventnotify()`` again.
  -  The signal will only be issued when the message queue transitions
     from empty to not empty.

  :param 句柄: The 句柄 返回ed by ```nx_连接()`` <#nx连接instance>`__.
  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nx_block(NXWINDOW hwnd, FAR void *arg);

  The response to this 函数 call is two things: (1)
  any queued callback messages to the 窗口 are 'blocked' and then (2)
  also subsequent 窗口 messaging is blocked.

  The ``event`` callback with the ``NXEVENT_BLOCKED`` event is the
  response from ``nx_block()``. This blocking 接口 用于 to assure
  that no further messages are are directed to the 窗口. Receipt of the
  ``NXEVENT_BLOCKED`` event signifies that (1) there are no further
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

.. c:function:: int nx_synch(NXWINDOW hwnd, FAR void *arg);

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
    ret = nx_synch(hwnd, 句柄);
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

  :param wnd: The 窗口 to be synched
  :param arg: An 参数 that will accompany the synch messages (这是 ``arg2`` in the event callback).

  :返回: OK on 成功; ERROR on 失败 with errno 设置
    appropriately

.. c:function:: NXWINDOW nx_openwindow(NXHANDLE handle, uint8_t flags, \
                       FAR const struct nx_callback_s *cb, \
                       FAR void *arg);

  创建 a new 窗口.

  :param 句柄: The 句柄 返回ed by ```nx_连接()`` <#nx连接instance>`__.
  :param flags: 选项al flags. These include:
    - ``NXBE_WINDOW_RAMBACKED``: Creates a RAM backed window. This option is only valid if ``CONFIG_NX_RAMBACKED`` is enabled.
    - ``NXBE_WINDOW_HIDDEN``: The window is create in the HIDDEN state and can be made visible later with ``nx_setvisibility()``.

  :param cb: Callbacks used to process 窗口 events
  :param arg: User provided 值 that will be 返回ed with NX callbacks.

  :返回: Success: A non-NULL 句柄 used with subsequent NX accesses
    Failure: NULL is 返回ed and errno is 设置 appropriately.

.. c:function:: int nx_closewindow(NXWINDOW hwnd)

  Destroy a 窗口 创建d by :c:func:`nx_打开窗口` 窗口.

  :param hwnd: The 句柄 返回ed by ```nx_打开窗口()`` <#nx打开窗口>`__ that
    identifies the 窗口 to be destroyed. This 句柄 must not have been
    one 返回ed by ```nx_requestbkgd()`` <#nxrequestbkgd>`__.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nx_requestbkgd(NXHANDLE handle, \
                   FAR const struct nx_callback_s *cb, \
                   FAR void *arg);

  NX normally controls a separate 窗口 called the
  background 窗口. It repaints the 窗口 as necessary using only a
  solid 颜色 fill. The background 窗口 always represents the entire
  屏幕 and is always below other 窗口s. It is useful for an
  application to control the background 窗口 in 以下
  conditions:

  -  If you want to implement a 窗口less solution. The single 屏幕 can
     be used to 创建 a truly simple graphic environment.
  -  When you want more on the background than a solid 颜色. 例如,
     if you want an 图像 in the background, or animations in the
     background, or live video, etc.

  This API only requests the 句柄 of the background 窗口. That 句柄
  will be 返回ed asynchronously in a subsequent position and redraw
  callbacks.

  Cautions:

  -  以下 should never be called using the background 窗口.
     They are guaranteed to cause severe crashes: :c:func:`nx_设置position`,
     :c:func:`nx_设置大小`, :c:func:`nx_raise`, or :c:func:`nx_lower`,
     :c:func:`nx_modal`, :c:func:`nx_设置visibility`.
  -  Neither :c:func:`nx_requestbkgd` nor :c:func:`nx_releasebkgd`
     should be called more than once. Multiple instances of the
     background 窗口 are not 支持ed.

  :param 句柄: The 句柄 返回ed by ```nx_连接()`` <#nx连接instance>`__.
  :param cb: Callbacks to use for processing background 窗口 events
  :param arg: User provided 参数 (see ```nx_打开窗口()`` <#nx打开窗口>`__)

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nx_releasebkgd(NXWINDOW hwnd)

  Release the background 窗口 previously acquired using
  :c:func:`nx_requestbkgd` and 返回 control of the background to NX.

  :param 句柄: The 句柄 返回ed indirectly by :c:func:`nx_requestbkgd`.
    This 句柄 must not have been one 创建d by :c:func:`nx_打开窗口`.

  :return: ``OK`` on success; ``ERROR`` on failure with ``errno`` set appropriately

.. c:function:: int nx_getposition(NXWINDOW hwnd)

  Request the position and 大小 information for the
  selected 窗口. The 值s will be 返回 asynchronously through the
  client callback 函数 指针.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口` or
    :c:func:`nx_requestbkgd`.

  :return: ``OK`` on success; ``ERROR`` on failure with ``errno`` set appropriately

.. c:function:: int nx_setposition(NXWINDOW hwnd, FAR struct nxgl_point_s *pos)

  设置 the position and 大小 for the selected 窗口.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口`. This
    句柄 must not have been 创建d by :c:func:`nx_requestbkgd`.
  :param pos: The new position of the 窗口

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nx_setsize(NXWINDOW hwnd, FAR struct nxgl_size_s *size)

  设置 the 大小 of the selected 窗口.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口`. This
    句柄 must not have been 创建d by :c:func:`nx_requestbkgd`.
  :param 大小: The new 大小 of the 窗口 (in 像素s).

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nx_raise(NXWINDOW hwnd)

  Bring the specified 窗口 to the top of the 显示.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口`. This
    句柄 must not have been 创建d by :c:func:`nx_requestbkgd`.

  :return: ``OK`` on success; ``ERROR`` on failure with ``errno`` set appropriately

.. c:function:: int nx_lower(NXWINDOW hwnd);

  Lower the specified 窗口 to the bottom of the 显示.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口`. This
    句柄 must not have been 创建d by :c:func:`nx_requestbkgd`.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nx_modal(NXWINDOW hwnd, bool modal)

  May be used to either (1) raise a 窗口 to the top of
  the 显示 and select modal behavior, or (2) 禁用 modal behavior.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口`. This
    句柄 must not have been 创建d by :c:func:`nx_requestbkgd`.
  :param modal: True: enter modal state; False: leave modal state

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nx_setvisibility(NXWINDOW hwnd, bool hide);

  Select if the 窗口 is visible or hidden. A hidden
  窗口 is still present and will update normally, but will not be
  visible on the 显示 until it is unhidden.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口`. This
    句柄 must not have been 创建d by :c:func:`nx_requestbkgd`.
  :param hide: True: 窗口 will be hidden; false: 窗口 will be visible

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: bool nx_ishidden(NXWINDOW hwnd);

  返回 true if the 窗口 is hidden.

  **NOTE**: There will be a delay between the time that the visibility of
  the 窗口 is changed via :c:func:`nx_设置visibily`
  before that new 设置 is reported by :c:func:`nx_ishidden`. ``nx_synch()``
  may be used if temporal synchronization 需要.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口` that
    identifies the 窗口 to be queried.

  :返回: *True*: the 窗口 is hidden, *false*: the 窗口 is
    visible

.. c:function:: int nx_fill(NXWINDOW hwnd, FAR const struct nxgl_rect_s *rect, \
                   nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES]);

  Fill the specified rectangle in the 窗口 with the
  specified 颜色.

  :param hwnd: The 句柄 返回ed by ```nx_打开窗口()`` <#nx打开窗口>`__ or
    ```nx_requestbkgd()`` <#nxrequestbkgd>`__
  :param rect: The location to be filled
  :param 颜色: The 颜色 to use in the fill

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: void nx_getrectangle(NXWINDOW hwnd, FAR const struct nxgl_rect_s *rect, \
                     unsigned int plane, FAR uint8_t *dest, \
                     unsigned int deststride);

  获取 the raw contents of graphic 内存 within a
  rectangular region. 注意： Since raw graphic 内存 is 返回ed, the
  返回ed 内存 content may be the 内存 of 窗口s above this one and
  may not necessarily belong to this 窗口 unless you assure that this is
  the top 窗口.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口` or
    :c:func:`nx_requestbkgd`
  :param rect: The location to be copied
  :param plane: Specifies the 颜色 plane to 获取 from
  :param dest: The location to copy the 内存 region
  :param deststride: The 宽度, in 字节s, of the dest 内存

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nx_filltrapezoid(NXWINDOW hwnd, FAR const struct nxgl_rect_s *clip, \
                            FAR const struct nxgl_trapezoid_s *trap, \
                            nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES]);

  Fill the specified trapezoidal region in the 窗口
  with the specified 颜色.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口` or
    :c:func:`nx_requestbkgd`
  :param clip: Clipping rectangle relative to 窗口 (may be null)
  :param trap: The trapezoidal region to be filled
  :param 颜色: The 颜色 to use in the fill

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nx_drawline(NXWINDOW hwnd, FAR struct nxgl_vector_s *vector, \
               nxgl_coord_t 宽度, nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES], \
               uint8_t caps);

  Fill the specified trapezoidal region in the 窗口
  with the specified 颜色. Fill the specified line in the 窗口 with the
  specified 颜色. 这是 simply a wrapper that uses :c:func:`nxgl_splitline`
  to break the line into trapezoids and then calls :c:func:`nx_filltrapezoid`
  to render the line.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口` or
    :c:func:`nx_requestbkgd`
  :param vector: Describes the line to be drawn.
  :param 宽度: The 宽度 of the line
  :param 颜色: The 颜色 to use to fill the line
  :param caps: Draw a circular cap on the ends of the line to 支持 better line
    joins. One of::

      /* Line caps */

      #define NX_LINECAP_NONE  0x00, /* No line caps */
      #define NX_LINECAP_PT1   0x01  /* Line cap on pt1 on of the vector only */
      #define NX_LINECAP_PT2   0x02  /* Line cap on pt2 on of the vector only */
      #define NX_LINECAP_BOTH  0x03  /* Line cap on both ends of the vector only */

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nx_drawcircle(NXWINDOW hwnd, FAR const struct nxgl_point_s *center, \
                  nxgl_coord_t radius, nxgl_coord_t 宽度, \
                  nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES]);

  Draw a circular outline using the specified line
  thickness and 颜色.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口` or
    :c:func:`nx_requestbkgd`
  :param center: A 指针 to the point that is the center of the circle.
  :param radius: The radius of the circle in 像素s.
  :param 宽度: The 宽度 of the line
  :param 颜色: The 颜色 to use to fill the line

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nx_fillcircle(NXWINDOW hwnd, FAR const struct nxgl_point_s *center, \
                  nxgl_coord_t radius, nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES]);

  Fill a circular region using the specified 颜色.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口` or
    :c:func:`nx_requestbkgd`
  :param center: A 指针 to the point that is the center of the circle.
  :param radius: The 宽度 of the line
  :param 颜色: The 颜色 to use to fill the circle

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nx_setbgcolor(NXHANDLE handle, \
                  nxgl_mx像素_t 颜色[CONFIG_NX_NPLANES]);

设置 the 颜色 of the background.

:param 句柄: The 句柄 创建d by :c:func:`nx_打开窗口` or
  :c:func:`nx_requestbkgd`
:param 颜色: The 颜色 to use in the background

:return: ``OK`` on success; ``ERROR`` on failure with
  ``errno`` 设置 appropriately

.. c:function:: int nx_move(NXWINDOW hwnd, FAR const struct nxgl_rect_s *rect,  \
                           FAR const struct nxgl_point_s *off设置);

Move a rectangular region within the 窗口.

:param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口` or
  :c:func:`nx_requestbkgd` that specifies the 窗口 within which the move is to be done
:param rect: Describes the (source) rectangular region to move
:param off设置: The off设置 to move the region

:return: ``OK`` on success; ``ERROR`` on failure with ``errno`` set appropriately

.. c:function:: int nx_bitmap(NXWINDOW hwnd, FAR const struct nxgl_rect_s *dest, \
                     FAR const void *src[CONFIG_NX_NPLANES], \
                     FAR const struct nxgl_point_s *origin, \
                     unsigned int stride);

  Copy a rectangular region of a larger 图像 into the
  rectangle in the specified 窗口.

  :param hwnd: The 句柄 返回ed by :c:func:`nx_打开窗口` or
    :c:func:`nx_requestbkgd` that specifies the 窗口 that will 接收 the 位map 图像.
  :param dest: Describes the rectangular on the 显示 that will 接收 the 位 map.
  :param src: The 启动 of the source 图像. 这是 an array source 图像s of 大小 ``CONFIG_NX_NPLANES`` (probably 1).
  :param origin: The origin of the upper, left-most corner of the full 位map. Both
    dest and origin are in 窗口 coordinates, however, the origin may
    lie outside of the 显示.
  :param stride: The 宽度 of the full source 图像 in 字节s.

  :return: ``OK`` on success; ``ERROR`` on failure with ``errno`` set appropriately

.. c:function:: int nx_kbdchin(NXHANDLE handle, uint8_t ch);
.. c:function:: int nx_kbdin(NXHANDLE handle, uint8_t nch, FAR const uint8_t *ch);

  Used by a th读取 or interrupt 句柄r that manages some
  kind of keypad hardware to report 文本 information to the NX server.
  That 文本 数据 will be routed by the NX server to the appropriate 窗口
  client.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. c:function:: int nx_mousein(NXHANDLE handle, nxgl_coord_t x, nxgl_coord_t y, uint8_t buttons)

  Used by a th读取 or interrupt 句柄r that manages some
  kind of pointing hardware to report new positional 数据 to the NX
  server. That positional 数据 will be routed by the NX server to the
  appropriate 窗口 client.

  :return: ``OK`` on success; ``ERROR`` on failure with
    ``errno`` 设置 appropriately

.. _nx-tool-kit-nxtk-1:

