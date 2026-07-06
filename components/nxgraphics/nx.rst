==
NX
==

概述
========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NX 提供了一个精简的窗口系统，其设计思路源自 X Window，但做了大幅裁剪，
适用于大多数资源受限的嵌入式环境。当前 NX 实现支持以下高层特性：

* **虚拟垂直图形空间** 窗口存在于一个虚拟的垂直空间中，因此可以讨论一个
  窗口位于另一个窗口之上并遮挡下方窗口这样的概念。

* **客户端/服务器模型** 采用标准的客户端/服务器模型。NX 可被视为服务器，
  而负责呈现窗口的其他逻辑则为 NX 客户端。

* **多用户支持** NX 包含面向 NX 服务器守护进程的前端逻辑，该守护进程可以
  为多个 NX 客户端线程提供服务。NX 服务器线程/守护进程负责将来自多个客户端
  的图形操作进行序列化处理。

* **精简图形工具集** 图形操作的实际实现由通用的后端逻辑完成。该后端仅支持
  一组基础的图形和渲染操作。

* **设备接口** NX 支持任意图形设备，可通过以下两种设备接口之一进行访问：

  #. 任何具有随机访问显存的设备，使用 NuttX 帧缓冲驱动接口
     （参见 include/nuttx/video/fb.h）。
  #. 任何可通过并行或串行接口接收光栅行数据的类 LCD 设备
     （参见 include/nuttx/lcd/lcd.h）。默认情况下，NX 使用帧缓冲驱动，
     除非在 NuttX 配置文件中将 CONFIG_NX_LCDDRIVER 定义为 =y。

* **对 NX 客户端透明** 窗口客户端只能"看到"其操作所在的子窗口，
  无需关心虚拟垂直空间的问题（仅在需要时响应 NX 发来的重绘请求即可）。

* **带边框的窗口和工具栏** NX 还在基本窗口功能之上，增加了对带边框和工具栏
  窗口的支持。这些窗口即为上图截图中所示的类型。这类带边框的窗口会将一个窗口
  划分为三个相对独立的子窗口：边框、所包含的窗口以及（可选的）工具栏窗口。

* **鼠标支持** NX 支持鼠标或其他 X/Y 指点设备。提供了相应的 API，允许外部
  设备向 NX 报告 X/Y 位置信息和鼠标按键事件。NX 随后会通过回调函数将鼠标
  输入传递给相关的窗口客户端。客户端窗口仅在鼠标位于其可见区域内时才会收到
  鼠标输入回调；X/Y 位置会以客户端窗口的相对坐标系提供给客户端。

* **键盘输入** NX 还支持键盘/小键盘设备。提供了相应的 API，允许外部设备向
  NX 报告键盘信息。NX 随后会通过回调函数将键盘输入传递给显示顶层窗口（即
  拥有焦点的窗口）。

预处理器定义
=========================

:c:macro:`nx_run` 宏使用的默认服务器消息队列名称：

.. code-block:: c

  #define NX_DEFAULT_SERVER_MQNAME "/dev/nxs"

鼠标按键位定义：

.. code-block:: c

  #define NX_MOUSE_NOBUTTONS    0x00
  #define NX_MOUSE_LEFTBUTTON   0x01
  #define NX_MOUSE_CENTERBUTTON 0x02
  #define NX_MOUSE_RIGHTBUTTON  0x04

NX 类型
========

NX 服务器的接口通过一个不透明句柄来管理：

.. c:type:: FAR void *NXHANDLE

特定窗口的接口同样通过一个不透明句柄来管理：

.. c:type:: FAR void *NXWINDOW

以下定义了必须提供给 :c:func:`nx_openwindow` 的回调函数。这些回调会在
:c:func:`nx_eventhandler` 的处理过程中被调用。

.. c:struct:: nx_callback_s

  .. code-block:: c

    struct nx_callback_s
    {
      void (*redraw)(NXWINDOW hwnd, FAR const struct nxgl_rect_s *rect,
                     bool more, FAR void *arg);
      void (*position)(NXWINDOW hwnd, FAR const struct nxgl_size_s *size,
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

启动 NX 服务器
======================

*NX 服务器*是一个内核守护进程，负责接收和序列化图形命令。在使用 NX 图形系统
之前，必须先启动该守护进程。有两种方式可以完成此操作：

#. 可以在板级启动逻辑中通过简单地调用函数 ``nxmu_start()`` 来启动 NX 服务器。
   板级启动逻辑通常位于 ``boards/arch/chip/board/src`` 目录中。如果配置中定义了
   ``CONFIG_BOARD_LATE_INITIALIZE``，则板级启动逻辑会在系统启动早期自动运行。
   或者，板级启动逻辑也可以由应用程序通过以下方式调用 :c:func:`boardctl` 来执行：

   .. code-block:: c

     boardctl(BOARDIOC_INIT, arg)

   无论哪种情况，板级初始化逻辑都会运行，简单地调用 ``nxmu_start()`` 即可启动
   NX 服务器。

#. NX 服务器也可以由应用程序稍后通过 :c:func:`boardctl` 来启动：

   .. code-block:: c

     boardctl(BOARDIOC_NX_START, arg)

.. c:function:: int nxmu_start(int display, int plane);

  提供一个包装函数，用于简化和标准化 NX 服务器的启动过程。

  :param display: 此新 NXMU 实例所服务的显示器编号。
  :param plane: 用于获取显示器几何信息和颜色格式的平面编号。

  :return: 成功时返回零（``OK``）。这表示 NX 服务器已成功启动、正在运行，
    并等待接受来自 NX 客户端的连接。失败时返回取负的 ``errno`` 值，该值
    指示了失败的原因。

NX 服务器回调
===================

.. c:function:: void redraw(NXWINDOW hwnd, FAR const struct nxgl_rect_s *rect, bool more, FAR void *arg);

  NX 请求客户端重绘窗口中指定矩形区域的内容。

  :param hwnd:
     由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd` 创建的句柄
  :param rect:
     需要重绘的矩形区域（使用窗口相对坐标）
  :param more:
     true：后续还有更多重绘请求
  :param arg:
     用户提供的参数（参见 :c:func:`nx_openwindow`）

.. c:function:: void position(NXWINDOW hwnd, FAR const struct nxgl_size_s *size, \
              FAR const struct nxgl_point_s *pos, \
              FAR const struct nxgl_rect_s *bounds, \
              FAR void *arg);

  窗口的大小或位置发生了变化（或者窗口刚以零大小创建）。

  :param hwnd:
     由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd` 创建的句柄
  :param size:
     窗口的大小
  :param pos:
     窗口左上角在整个显示器上的位置
  :param bounds:
     描述整个显示器的边界矩形
  :param arg:
     用户提供的参数（参见 :c:func:`nx_openwindow`）

.. c:function:: void mousein(NXWINDOW hwnd, FAR const struct nxgl_point_s *pos, \
             uint8_t buttons, FAR void *arg);

  窗口收到了新的鼠标数据

  :param hwnd:
     由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd` 创建的句柄
  :param pos:
     鼠标的 (x,y) 位置
  :param buttons:
     参见 ``NX_MOUSE_*`` 定义
  :param arg:
     用户提供的参数（参见 :c:func:`nx_openwindow`）

.. c:var:: void (*kbdin)(NXWINDOW hwnd, uint8_t nch, FAR const uint8_t *ch, FAR void *arg);

  窗口收到了新的键盘/小键盘数据。

  :param hwnd:
       由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd` 创建的句柄
  :param nch:
     ch[] 中可用的字符数量
  :param ch:
     字符数组
  :param arg:
     用户提供的参数（参见 :c:func:`nx_openwindow`）

.. c:var:: void (*event)(NXWINDOW hwnd, enum nx_event_e event, FAR void *arg1, FAR void *arg2);

  此回调用于将服务器事件通知给窗口监听器。

  - ``NXEVENT_BLOCKED``：窗口消息被阻塞。
     此回调是对 :c:func:`nx_block` 或 :c:func:`nxtk_block` 的响应。
     这些阻塞接口用于确保不再有消息被发送到该窗口。收到阻塞回调表示
     （1）没有更多的待处理回调，且（2）该窗口现已失效，不会再收到任何
     回调。此回调支持窗口的协调销毁。在多用户模式下，客户端窗口逻辑
     必须保持完整，直到所有排队的回调都被处理完毕。之后窗口才能被安全
     关闭。在有待处理回调的情况下关闭窗口，可能会在回调执行时导致异常
     行为。
  - ``NXEVENT_SYNCHED``：同步握手
     此事件完成了由 :c:func:`nx_synch` 或 :c:func:`nxtk_synch` 发起的
     握手过程。这些接口向 NX 服务器发送同步消息，服务器随即响应该事件。
     处于等待状态的客户端被唤醒后继续图形处理，从而完成握手。由于客户端
     与服务器之间的通信具有高度异步性，有时需要进行同步以确保客户端和
     服务器能够正确协调工作。

  :param hwnd:
     接收事件的窗口句柄
  :param event:
     服务器事件
  :param arg1:
     用户提供的参数（参见 :c:func:`nx_openwindow`、
     :c:func:`nx_requestbkgd` 或 :c:func:`nxtk_opentoolbar`）
  :param arg2:
     用户提供的参数（参见 :c:func:`nx_block`、:c:func:`nxtk_block`、
     :c:func:`nx_synch` 或 :c:func:`nxtk_synch`）

.. c:macro:: nx_run(fb)

  .. code-block:: c

    #define nx_run(fb) nx_runinstance(NX_DEFAULT_SERVER_MQNAME, dev)

.. c:function:: int nx_runinstance(FAR const char *mqname, FAR struct fb_vtable_s *fb)

  这是服务器的入口点。该函数不会返回；调用线程将专用于支持 NX 服务器。

  注意：NX 服务器可以同时运行多个实例，每个实例使用不同的回调和消息队列
  名称。``nx_run()`` 仅是一个宏，可在只需要一个服务器实例时使用。在这种
  情况下，将使用默认的服务器名称。

  :param mqname: 服务器接收消息队列的名称
  :param dev: 要使用的帧缓冲或 LCD 驱动"对象"

  :return: 该函数通常不会返回。如果确实返回，将返回 ``ERROR``，并适当
    设置 ``errno``。

.. c:macro:: nx_connect(cb)

  .. code-block:: c

    #define nx_connect(cb) nx_connectinstance(NX_DEFAULT_SERVER_MQNAME)

.. c:function:: NXHANDLE nx_connectinstance(FAR const char *svrmqname);

  打开从客户端到 NX 服务器的连接。通常每个线程只需要一个客户端连接，
  因为每个连接可以承载多个窗口。

  注意：

  - 该函数在连接完全建立之前就会返回。在使用返回的句柄之前，必须等待
    连接事件。
  - NX 服务器可以同时运行多个实例，每个实例使用不同的消息队列名称。
  - ``nx_connect()`` 仅是一个宏，可在只需要一个服务器实例时使用。在这种
    情况下，将使用默认的服务器名称。

  :param svrmqname: 服务器接收消息队列的名称

  :return: 成功：返回一个非 NULL 的句柄，用于后续的 NX 访问。
    失败：返回 NULL，errno 被适当设置。

.. c:function:: void nx_disconnect(NXHANDLE handle)

  断开客户端与 NX 服务器的连接，并/或释放由
  :c:func:`nx_connect`/:c:func:`nx_connectinstance` 保留的资源。

  :param handle: 由 :c:func:`nx_connectinstance` 返回的句柄。

.. c:function:: int nx_eventhandler(NXHANDLE handle);

  客户端代码必须周期性地调用此函数来处理来自服务器的传入消息。如果定义了
  ``CONFIG_NX_BLOCKING``，则此函数在收到服务器消息之前不会返回。

  当未定义 ``CONFIG_NX_BLOCKING`` 时，客户端在循环调用时必须谨慎，以确保
  不会因反复调用 nx_eventhandler 而耗尽所有 CPU 带宽。可以调用
  :c:func:`nx_eventnotify` 来注册信号事件，以便在有新的服务器事件到来时
  获得通知。

  :param handle: 由 :c:func:`nx_connectinstance` 返回的句柄。

  :return:
    - ``OK``：没有发生错误。如果定义了 ``CONFIG_NX_BLOCKING``，则表示
      已处理了一个或多个服务器消息。
    - ``ERROR``：发生了错误，``errno`` 已被适当设置。特别需要注意的是，
      当服务器断开连接时，将返回 ``errno == EHOSTDOWN``。此后该句柄
      将不再可用。

.. c:function:: int nx_eventnotify(NXHANDLE handle, int signo);

  客户端可以注册接收信号通知，而不是周期性地调用 :c:func:`nx_eventhandler`。
  这样客户端只在有传入事件可用时才调用 :c:func:`nx_eventhandler`。

  底层实现使用了 ``mq_notifiy()``，因此客户端必须遵守 ``mq_notifiy()`` 的
  使用规则：

  - 每次仅发送一个信号通知。收到信号后，如果客户端希望继续接收通知，
    必须再次调用 ``nx_eventnotify()``。
  - 信号仅在消息队列从空变为非空时才会发出。

  :param handle: 由 :c:func:`nx_connectinstance` 返回的句柄。
  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_block(NXWINDOW hwnd, FAR void *arg);

  调用此函数后会得到两个结果：（1）所有已排队的窗口回调消息被"阻塞"，
  （2）后续的窗口消息也被阻塞。

  带有 ``NXEVENT_BLOCKED`` 事件的 ``event`` 回调是 ``nx_block()`` 的响应。
  此阻塞接口用于确保不再有消息被发送到该窗口。收到 ``NXEVENT_BLOCKED``
  事件表示（1）没有更多的待处理回调，且（2）该窗口现已失效，不会再收到
  任何回调。

  此回调支持窗口的协调销毁。客户端窗口逻辑必须保持完整，直到所有排队的
  回调都被处理完毕。之后窗口才能被安全关闭。在有待处理回调的情况下关闭
  窗口，可能会在回调执行时导致异常行为。

  :param wnd: 要被阻塞的窗口
  :param arg: 将伴随阻塞消息传递的参数（即事件回调中的 ``arg2``）

  :return: 成功返回 OK；失败返回 ERROR，errno 被适当设置。

.. c:function:: int nx_synch(NXWINDOW hwnd, FAR void *arg);

  此接口可用于同步窗口客户端与 NX 服务器。它实际上实现了一个"回声"机制：
  窗口客户端向服务器发送同步消息，服务器随即立即将 ``NXEVENT_SYNCHED``
  事件发送回窗口客户端。

  由于客户端与服务器之间的通信具有高度异步性，``nx_synch()`` 有时是必要的，
  以确保客户端和服务器在时间上完全同步。

  窗口客户端的使用方式可能如下：

  .. code-block:: c

    extern bool g_synched;
    extern sem_t g_synch_sem;

    g_synched = false;
    ret = nx_synch(hwnd, handle);
    if (ret < 0)
      {
         -- 处理错误 --
      }

    while (!g_synched)
      {
        ret = sem_wait(&g_sync_sem);
        if (ret < 0)
          {
             -- 处理错误 --
          }
      }

  当窗口监听器线程收到 ``NXEVENT_SYNCHED`` 事件时，会将 ``g_synched``
  设置为 ``true`` 并发送 ``g_synch_sem`` 信号，从而唤醒上述循环。

  :param wnd: 要同步的窗口
  :param arg: 将伴随同步消息传递的参数（即事件回调中的 ``arg2``）

  :return: 成功返回 OK；失败返回 ERROR，errno 被适当设置

.. c:function:: NXWINDOW nx_openwindow(NXHANDLE handle, uint8_t flags, \
                       FAR const struct nx_callback_s *cb, \
                       FAR void *arg);

  创建一个新窗口。

  :param handle: 由 :c:func:`nx_connectinstance` 返回的句柄。
  :param flags: 可选标志。包括：
    - ``NXBE_WINDOW_RAMBACKED``：创建一个 RAM 支持的窗口。此选项仅在启用 ``CONFIG_NX_RAMBACKED`` 时有效。
    - ``NXBE_WINDOW_HIDDEN``：窗口创建时处于隐藏状态，之后可通过 ``nx_setvisibility()`` 使其可见。

  :param cb: 用于处理窗口事件的回调函数
  :param arg: 用户提供的值，将在 NX 回调中返回。

  :return: 成功：返回一个非 NULL 的句柄，用于后续的 NX 访问。
    失败：返回 NULL，errno 被适当设置。

.. c:function:: int nx_closewindow(NXWINDOW hwnd)

  销毁由 :c:func:`nx_openwindow` 创建的窗口。

  :param hwnd: 由 :c:func:`nx_openwindow` 返回的句柄，用于标识要销毁的窗口。
    此句柄不能是由 :c:func:`nx_requestbkgd` 返回的句柄。

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_requestbkgd(NXHANDLE handle, \
                   FAR const struct nx_callback_s *cb, \
                   FAR void *arg);

  NX 通常会控制一个名为背景窗口的独立窗口。NX 使用纯色填充来重绘该窗口。
  背景窗口始终代表整个屏幕，且始终位于其他窗口之下。在以下情况下，应用程序
  控制背景窗口会很有用：

  - 当您希望实现无窗口方案时。单一屏幕可用于创建一个真正简单的图形环境。
  - 当您希望背景不仅仅是纯色时。例如，如果您想要背景图片、背景动画或
    实时视频等。

  此 API 仅请求背景窗口的句柄。该句柄会在后续的 position 和 redraw 回调中
  异步返回。

  注意事项：

  - 绝对不能对背景窗口调用以下函数，否则会导致严重崩溃：
    :c:func:`nx_setposition`、:c:func:`nx_setsize`、:c:func:`nx_raise`、
    :c:func:`nx_lower`、:c:func:`nx_modal`、:c:func:`nx_setvisibility`。
  - :c:func:`nx_requestbkgd` 和 :c:func:`nx_releasebkgd` 都不应被多次调用。
    不支持多个背景窗口实例。

  :param handle: 由 :c:func:`nx_connectinstance` 返回的句柄。
  :param cb: 用于处理背景窗口事件的回调函数
  :param arg: 用户提供的参数（参见 :c:func:`nx_openwindow`）

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_releasebkgd(NXWINDOW hwnd)

  释放之前通过 :c:func:`nx_requestbkgd` 获取的背景窗口，并将背景的控制权
  交还给 NX。

  :param handle: 由 :c:func:`nx_requestbkgd` 间接返回的句柄。
    此句柄不能是由 :c:func:`nx_openwindow` 创建的句柄。

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_getposition(NXWINDOW hwnd)

  请求指定窗口的位置和大小信息。这些值将通过客户端回调函数指针异步返回。

  :param hwnd: 由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd`
    返回的句柄。

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_setposition(NXWINDOW hwnd, FAR struct nxgl_point_s *pos)

  设置指定窗口的位置和大小。

  :param hwnd: 由 :c:func:`nx_openwindow` 返回的句柄。此句柄不能是由
    :c:func:`nx_requestbkgd` 创建的句柄。
  :param pos: 窗口的新位置

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_setsize(NXWINDOW hwnd, FAR struct nxgl_size_s *size)

  设置指定窗口的大小。

  :param hwnd: 由 :c:func:`nx_openwindow` 返回的句柄。此句柄不能是由
    :c:func:`nx_requestbkgd` 创建的句柄。
  :param size: 窗口的新大小（以像素为单位）。

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_raise(NXWINDOW hwnd)

  将指定窗口提升到显示器的最顶层。

  :param hwnd: 由 :c:func:`nx_openwindow` 返回的句柄。此句柄不能是由
    :c:func:`nx_requestbkgd` 创建的句柄。

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_lower(NXWINDOW hwnd);

  将指定窗口降低到显示器的最底层。

  :param hwnd: 由 :c:func:`nx_openwindow` 返回的句柄。此句柄不能是由
    :c:func:`nx_requestbkgd` 创建的句柄。

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_modal(NXWINDOW hwnd, bool modal)

  可用于（1）将窗口提升到显示器最顶层并选择模态行为，或（2）禁用模态行为。

  :param hwnd: 由 :c:func:`nx_openwindow` 返回的句柄。此句柄不能是由
    :c:func:`nx_requestbkgd` 创建的句柄。
  :param modal: True：进入模态状态；False：退出模态状态

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_setvisibility(NXWINDOW hwnd, bool hide);

  设置窗口是否可见。隐藏的窗口仍然存在并会正常更新，但在取消隐藏之前
  不会在显示器上显示。

  :param hwnd: 由 :c:func:`nx_openwindow` 返回的句柄。此句柄不能是由
    :c:func:`nx_requestbkgd` 创建的句柄。
  :param hide: True：窗口将被隐藏；false：窗口将可见

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: bool nx_ishidden(NXWINDOW hwnd);

  如果窗口处于隐藏状态则返回 true。

  **注意**：通过 :c:func:`nx_setvisibily` 更改窗口可见性后，到
  :c:func:`nx_ishidden` 报告新设置之间会存在延迟。如果需要时间同步，
  可以使用 ``nx_synch()``。

  :param hwnd: 由 :c:func:`nx_openwindow` 返回的句柄，用于标识要查询的窗口。

  :return: *True*：窗口已隐藏，*false*：窗口可见

.. c:function:: int nx_fill(NXWINDOW hwnd, FAR const struct nxgl_rect_s *rect, \
                   nxgl_mxpixel_t color[CONFIG_NX_NPLANES]);

  使用指定颜色填充窗口中的指定矩形区域。

  :param hwnd: 由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd`
    返回的句柄
  :param rect: 要填充的位置
  :param color: 填充使用的颜色

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: void nx_getrectangle(NXWINDOW hwnd, FAR const struct nxgl_rect_s *rect, \
                     unsigned int plane, FAR uint8_t *dest, \
                     unsigned int deststride);

  获取矩形区域内图形内存的原始内容。注意：由于返回的是原始图形内存，
  返回的内存内容可能是该窗口上方其他窗口的内存，不一定属于当前窗口，
  除非确保当前窗口位于最顶层。

  :param hwnd: 由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd`
    返回的句柄
  :param rect: 要复制的位置
  :param plane: 指定要获取的颜色平面
  :param dest: 复制内存区域的目标位置
  :param deststride: 目标内存的宽度（以字节为单位）

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_filltrapezoid(NXWINDOW hwnd, FAR const struct nxgl_rect_s *clip, \
                            FAR const struct nxgl_trapezoid_s *trap, \
                            nxgl_mxpixel_t color[CONFIG_NX_NPLANES]);

  使用指定颜色填充窗口中的指定梯形区域。

  :param hwnd: 由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd`
    返回的句柄
  :param clip: 相对于窗口的裁剪矩形（可以为 null）
  :param trap: 要填充的梯形区域
  :param color: 填充使用的颜色

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_drawline(NXWINDOW hwnd, FAR struct nxgl_vector_s *vector, \
               nxgl_coord_t width, nxgl_mxpixel_t color[CONFIG_NX_NPLANES], \
               uint8_t caps);

  使用指定颜色在窗口中绘制指定线条。这是一个包装函数，使用
  :c:func:`nxgl_splitline` 将线条分解为梯形，然后调用
  :c:func:`nx_filltrapezoid` 来渲染线条。

  :param hwnd: 由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd`
    返回的句柄
  :param vector: 描述要绘制的线条。
  :param width: 线条宽度
  :param color: 填充线条使用的颜色
  :param caps: 在线条端点绘制圆形端帽以支持更好的线条连接。取值为::

      /* Line caps */

      #define NX_LINECAP_NONE  0x00, /* No line caps */
      #define NX_LINECAP_PT1   0x01  /* Line cap on pt1 on of the vector only */
      #define NX_LINECAP_PT2   0x02  /* Line cap on pt2 on of the vector only */
      #define NX_LINECAP_BOTH  0x03  /* Line cap on both ends of the vector only */

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_drawcircle(NXWINDOW hwnd, FAR const struct nxgl_point_s *center, \
                  nxgl_coord_t radius, nxgl_coord_t width, \
                  nxgl_mxpixel_t color[CONFIG_NX_NPLANES]);

  使用指定的线条宽度和颜色绘制圆形轮廓。

  :param hwnd: 由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd`
    返回的句柄
  :param center: 指向圆心的指针。
  :param radius: 圆的半径（以像素为单位）。
  :param width: 线条宽度
  :param color: 填充线条使用的颜色

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_fillcircle(NXWINDOW hwnd, FAR const struct nxgl_point_s *center, \
                  nxgl_coord_t radius, nxgl_mxpixel_t color[CONFIG_NX_NPLANES]);

  使用指定颜色填充圆形区域。

  :param hwnd: 由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd`
    返回的句柄
  :param center: 指向圆心的指针。
  :param radius: 圆的半径（以像素为单位）
  :param color: 填充圆使用的颜色

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_setbgcolor(NXHANDLE handle, \
                  nxgl_mxpixel_t color[CONFIG_NX_NPLANES]);

  设置背景颜色。

  :param handle: 由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd`
    创建的句柄
  :param color: 背景使用的颜色

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_move(NXWINDOW hwnd, FAR const struct nxgl_rect_s *rect,  \
                           FAR const struct nxgl_point_s *offset);

  移动窗口内的一个矩形区域。

  :param hwnd: 由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd`
    返回的句柄，指定要执行移动操作的窗口
  :param rect: 描述要移动的（源）矩形区域
  :param offset: 移动区域的偏移量

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_bitmap(NXWINDOW hwnd, FAR const struct nxgl_rect_s *dest, \
                     FAR const void *src[CONFIG_NX_NPLANES], \
                     FAR const struct nxgl_point_s *origin, \
                     unsigned int stride);

  将较大图像中的一个矩形区域复制到指定窗口中的矩形区域。

  :param hwnd: 由 :c:func:`nx_openwindow` 或 :c:func:`nx_requestbkgd`
    返回的句柄，指定接收位图图像的窗口。
  :param dest: 描述显示器上接收位图的矩形区域。
  :param src: 源图像的起始位置。这是一个大小为 ``CONFIG_NX_NPLANES``（通常为 1）
    的源图像数组。
  :param origin: 完整位图最左上角的原点。dest 和 origin 均使用窗口坐标，
    但 origin 可能位于显示器范围之外。
  :param stride: 完整源图像的宽度（以字节为单位）。

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_kbdchin(NXHANDLE handle, uint8_t ch);
.. c:function:: int nx_kbdin(NXHANDLE handle, uint8_t nch, FAR const uint8_t *ch);

  由管理某种键盘硬件的线程或中断处理程序使用，用于向 NX 服务器报告文本信息。
  NX 服务器会将该文本数据路由到相应的窗口客户端。

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. c:function:: int nx_mousein(NXHANDLE handle, nxgl_coord_t x, nxgl_coord_t y, uint8_t buttons)

  由管理某种指点设备硬件的线程或中断处理程序使用，用于向 NX 服务器报告新的
  位置数据。NX 服务器会将该位置数据路由到相应的窗口客户端。

  :return: 成功返回 ``OK``；失败返回 ``ERROR``，并适当设置 ``errno``

.. _nx-tool-kit-nxtk-1:
