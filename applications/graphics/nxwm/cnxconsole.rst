=========================
CNxConsole 键盘输入
=========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**参与者**

让我们来看看键盘数据传输中的主要参与者。这比您最初想象的要复杂得多：

**特殊驱动程序**
NxConsole 设备。NX 控制台输入通过一个在早期初始化时注册为 ``/dev/nxcon0`` 的特殊设备驱动程序进行。

**内核线程**

* **NX 服务器线程** NX 服务器是图形服务器命令。它接收来自各种来源的消息，执行图形操作，并将图形事件消息转发到正确的窗口。大多数时候，NX 服务器线程在消息队列上等待接收下一个图形事件。

* **NxConsole 线程** 每个 NxConsole 都有一个线程，在每个 ``NxWM::CNxConsole`` 实例被 NxWM 创建时启动。每个 ``NxWM::CNxConsole`` 线程打开 ``/dev/nxcon0`` 处的 NxConsole 驱动程序，并将 stdin、stdout 和 stderr 重定向到/来自该特殊设备。通常，``NxWM::CNxConsole`` 线程停止，仅在 read 上等待键盘输入完成。

**应用程序线程**

* **NxWidgets 窗口事件处理线程** ``CNxServer::listener()`` 是 NxWidgets 每次打开新窗口时启动的应用程序线程。它接收来自 NX 服务器的窗口消息并相应地分派消息。

* **键盘监听线程** ``CKeyboard::listener()`` 是由 NxWM 启动的应用程序线程。它仅监听键盘输入并通过图形路由系统转发。

以下是将键盘输入从 stdin 设备传递到正确 NxConsole 的事件序列：

#. 应用程序空间 / NxWidgets 窗口事件处理线程
   让我们从 NX 服务器线程的初始状态开始。最初，它只是等待来自 NX 服务器的消息。

     * ``NxWidgets/libnxwidgets/src/cnxserver.cxx``
       ``CNxServer::listener()`` 是其窗口监听线程。它仅调用 ``nx_eventhandler()`` 来接收和处理服务器事件。每个窗口都有一个这样的监听线程。

     * ``nuttx/libnx/nxwm/nx_eventhandler``
       ``nx_eventhandler()`` 等待接收来自 NX 服务器的消息。每个窗口都有自己的消息队列；每个窗口实例都有自己的 ``nx_eventhandler()`` 等待消息。

#. 应用程序空间 / 键盘监听线程

   以下是键盘数据输入时发生的即时事件。键盘监听线程唤醒并将键盘数据转发到 NX 服务器。只有 NX 服务器知道哪个窗口应该获得键盘输入。

     * ``NxWidgets\\nxwm\\src\\ckeyboard.cxx``
       ``CKeyboard::listener()`` 是由 NxWM 启动的微小线程，仅监听键盘输入。它打开键盘设备并等待 ``read()`` 以接收下一个键盘输入。当从键盘设备读取返回数据时，``CKeyboard::listener()`` 调用 ``nx_kbdin()``。

     * ``nuttx\\libnx\\nxmu\\nx_kbdin.c``
       此库函数仅隐藏 NX 服务器消息实现。它将 ``NX_SVRMSG_KBDIN`` 发送到 NX 服务器线程。

#. 内核空间 / NX 服务器

   NX 服务器唤醒，接收键盘消息，并将其转发到相应的窗口。

     * ``nuttx/graphics/nxmu/nxmu/nxmu_server.c``
       ``NX_SVRMSG_KBDIN`` 消息的接收唤醒了 NX 服务器线程。NX 服务器线程解码消息并调用 ``nxmu_kbdin()``。

     * ``nuttx/graphics/nxconsole/nxmu_kbdin.c``
       ``nxmu_kbdin()`` 通过与窗口关联的客户端消息队列，简单地将 ``NX_CLIMSG_KBDIN`` 发送到相应的窗口客户端。

#. 应用程序空间 / NxWidgets 窗口事件处理线程

   当接收到键盘消息时，窗口客户端唤醒。它将键盘数据转发到 ``/dev/nxcon0/``，使其可用于 NxConsole 窗口。

     * ``nuttx/libnx/nxwm/nx_eventhandler``
       在 ``CNxServer::listener()`` 线程中运行的 ``nx_eventhandler()`` 逻辑接收 ``NX_CLIMSG_KBDIN`` 消息并将其分派到键盘输入回调方法。在本例中，该回调方法映射到 ``CCallback::newKeyboardEvent()``。

     * ``NxWidgets/libnxwidgets/src/ccallback.cxx``
       对于普通键盘输入，``CCallback::newKeyboardEvent()`` 通过 ``CWidgetControl::newKeyboardEvent()`` 方法将键盘定向到获得焦点的部件。但对于 NxConsole 窗口，情况不同。在这种情况下，``CCallback::newKeyboardEvent()`` 调用 ``nxcon_kbdin()``。

     * ``nuttx/graphics/nxconsole/nxcon_kbdin.c``
       ``nxcon_kbdin()`` 将键盘数据添加到循环缓冲区，并唤醒任何在 ``/dev/nxcon0`` 输入设备上的读取操作。


   注意：此处存在应用程序和内核空间边界的违规。``nxcon_kbdin.c`` 构建在内核空间中，但从应用程序空间调用。解决方案是 (1) 将 ``nxcon_kbdin()`` 移到 ``libnx/``，然后 (2) 它应通过 ioctl 调用与 ``/dev/nxcon9`` 驱动程序通信。这将来会成为问题。

#. 内核空间 / NxConsole 线程

   最后，
     * ``nuttx/graphics/nxconsole/nxcon_kbdin.c``
       ``nxcon_kbdin()`` 对键盘数据的接收和入队唤醒了在 ``nxcon_read()`` 方法中等待的所有线程。这就是 NxConsole 获取键盘输入的方式。


**鼠标输入**
此处所述的几乎所有内容同样适用于鼠标/触摸屏输入。如果我们将键盘替换为鼠标、kbdin 替换为 mousein 等，您就得到了关于鼠标/触摸屏输入如何工作的相当好的描述。

不过，鼠标/触摸屏输入稍微简单一些：主要简化在于 NxConsole 及其特殊输入设备的额外复杂性不适用。鼠标/触摸屏输入在 ``CCallback::newMouseEvent`` 中接收到回调时，总是通过无条件调用 ``CWidgetControl::newMouseEvent`` 转向部件。在 ``CCallback::newKeyboardEvent`` 的逻辑中，在对应的位置存在一个"分支"。
