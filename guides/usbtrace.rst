.. _usbtrace:

================
USB 设备跟踪
================

**USB 设备跟踪控制**。NuttX USB 设备子系统支持相当复杂的跟踪功能。基本跟踪能力由以下 NuttX 配置设置控制：

  -  ``CONFIG_USBDEV_TRACE``：启用 USB 跟踪
  -  ``CONFIG_USBDEV_TRACE_NRECORDS``：要记住的跟踪条目数量

**跟踪 ID**。跟踪功能的工作方式如下：启用后，USB 设备驱动或 USB 类驱动中发生的 USB 事件会被记录。这些事件在 ``include/nuttx/usb/usbdev_trace.h`` 中描述。记录的事件由一组事件 ID 标识：

=========================  ==================================
``TRACE_INIT_ID`` \t       初始化事件
``TRACE_EP_ID`` \t         端点 API 调用
``TRACE_DEV_ID`` \t         USB 设备 API 调用
``TRACE_CLASS_ID`` \t       USB 类驱动 API 调用
``TRACE_CLASSAPI_ID`` \t   其他类驱动系统 API 调用
``TRACE_CLASSSTATE_ID``    跟踪类驱动状态变化
``TRACE_INTENTRY_ID`` \t   中断处理程序入口
``TRACE_INTDECODE_ID`` \t   解码的中断事件
``TRACE_INTEXIT_ID`` \t     中断处理程序退出
``TRACE_OUTREQQUEUED_ID``  OUT 端点排队的请求
``TRACE_INREQQUEUED_ID``   IN 端点排队的请求
``TRACE_READ_ID``          读取 (OUT) 操作
``TRACE_WRITE_ID``         写入 (IN) 操作
``TRACE_COMPLETE_ID``      请求完成
``TRACE_DEVERROR_ID``      USB 控制器驱动错误事件
``TRACE_CLSERROR_ID``      USB 类驱动错误事件
=========================  ==================================

**记录的事件**。每个记录的事件为 32 位大小，包括

  #. 8 位跟踪 ID（与上述关联的值）
  #. 8 位附加跟踪 ID 数据，以及
  #. 16 位附加数据。

**8 位跟踪数据** 8 位跟踪数据取决于特定的事件 ID。例如，

  -  对于 USB 串口和大容量存储类，8 位事件数据在 ``include/nuttx/usb/usbdev_trace.h`` 中提供。
  -  对于 USB 设备驱动，8 位事件数据在 USB 设备驱动本身中提供。例如，LPC1768 USB 设备驱动的 8 位事件数据在 ``arch/arm/src/lpc17xx_40xx/lpc17_40_usbdev.c`` 中。

**16 位跟踪数据**。16 位跟踪数据提供与特定记录事件相关的附加上下文数据。

**跟踪控制接口**。可以使用 ``include/nuttx/usb/usbdev_trace.h`` 中描述的接口启用或禁用每种事件的日志记录。

**启用 USB 设备跟踪**。如果在 NuttX 配置文件中设置了 ``CONFIG_USBDEV`` 和以下任一项，则将配置 USB 设备跟踪：

  -  ``CONFIG_USBDEV_TRACE``，或
  -  ``CONFIG_DEBUG_FEATURES and CONFIG_DEBUG_USB``

**日志数据接收器**。记录的数据本身可以发送到 (1) 内部循环缓冲区，或 (2) 控制台。如果定义了 ``CONFIG_USBDEV_TRACE``，则跟踪数据将发送到循环缓冲区。循环缓冲区的大小由 ``CONFIG_USBDEV_TRACE_NRECORDS`` 确定。否则，跟踪数据发送到控制台。

**示例**。以下是使用 ``apps/examples/usbserial`` 在 LPC1768 平台上使用以下 NuttX 配置设置的 USB 跟踪输出示例：

  -  ``CONFIG_DEBUG_FEATURES``, ``CONFIG_DEBUG_INFO``, ``CONFIG_USB``
  -  ``CONFIG_EXAMPLES_USBSERIAL_TRACEINIT``,
     ``CONFIG_EXAMPLES_USBSERIAL_TRACECLASS``,
     ``CONFIG_EXAMPLES_USBSERIAL_TRACETRANSFERS``,
     ``CONFIG_EXAMPLES_USBSERIAL_TRACECONTROLLER``,
     ``CONFIG_EXAMPLES_USBSERIAL_TRACEINTERRUPTS``

控制台输出::

    \tABDE
    \tusbserial_main: Registering USB serial driver
    \tuart_register: Registering /dev/ttyUSB0
    \tusbserial_main: Successfully registered the serial driver
  1 \tClass API call 1: 0000
  2 \tClass error: 19:0000
    \tusbserial_main: ERROR: Failed to open /dev/ttyUSB0 for reading: 107
    \tusbserial_main: Not connected. Wait and try again.
  3 \tInterrupt 1 entry: 0039
  4 \tInterrupt decode 7: 0019
  5 \tInterrupt decode 32: 0019
  6 \tInterrupt decode 6: 0019
  7 \tClass disconnect(): 0000
  8 \tDevice pullup(): 0001
  9 \tInterrupt 1 exit: 0000

带编号的项目是 USB 跟踪输出。你可以查看 ``drivers/usbdev/usbdev_trprintf.c`` 文件以了解每行输出的确切格式。以下是如何解释每一行：

==  ====================  ================  ==================================  =================
N.  USB 事件 ID          8 位事件数据      含义                                16 位事件数据
1   TRACE_CLASSAPI_ID1 \t  1                 USBSER_TRACECLASSAPI_SETUP1         0000
2   TRACE_CLSERROR_ID1 \t  19                USBSER_TRACEERR_SETUPNOTCONNECTED1  0000
3   TRACE_INTENTRY_ID1 \t  1                 LPC17_40_TRACEINTID_USB2            0039
4   TRACE_INTDECODE_ID2   7                 LPC17_40_TRACEINTID_DEVSTAT2        0019
5   TRACE_INTDECODE_ID2   32                LPC17_40_TRACEINTID_SUSPENDCHG2     0019
6   TRACE_INTDECODE_ID2   6                 LPC17_40_TRACEINTID_DEVRESET2       0019
7   TRACE_CLASS_ID1       3                 (参见 TRACE_CLASSDISCONNECT1)        0000
8   TRACE_DEV_ID1         6                 (参见 TRACE_DEVPULLUP1)              0001
9   TRACE_INTEXIT_ID1     1                 LPC17_40_TRACEINTID_USB2            0000
==  ====================  ================  ==================================  =================

注意：

  1. 参见 include/nuttx/usb/usbdev_trace.h
  2. 参见 arch/arm/src/lpc17xx_40xx/lpc17_40_usbdev.c

在上面的示例中你可以看到：

  -  **1**. 为 USB 串口类调用了串口类 USB setup 方法。这对应于 ``drivers/usbdev/pl2303.c`` 中的以下逻辑：

     .. code-block:: c

       static int pl2303_setup(FAR struct uart_dev_s *dev)
       {
         ...
         usbtrace(PL2303_CLASSAPI_SETUP, 0);
         ...

  -  **2**. 处理 setup 命令时发生错误，因为主机尚未选择配置。这对应于 ``drivers/usbdev/pl2303.c`` 中的以下逻辑：

      .. code-block:: c

        static int pl2303_setup(FAR struct uart_dev_s *dev)
        {
          ...
          /* Check if we have been configured */

          if (priv->config == PL2303_CONFIGIDNONE)
            {
              usbtrace(TRACE_CLSERROR(USBSER_TRACEERR_SETUPNOTCONNECTED), 0);
              return -ENOTCONN;
            }
          ...

  -  **3-6**. 这是一个挂起并重置设备的 USB 中断。
  -  **7-8**. 在中断处理期间，串口类被断开连接。
  -  **9**. 中断返回。

**USB 监视器**。*USB 监视器* 是 ``apps/system/usbmonitor`` 中的一个应用程序，提供了一种方便的方式来获取调试跟踪输出。如果启用了跟踪，USB 设备将保存编码的跟踪输出到内存缓冲区；如果 USB 监视器也被启用，该跟踪缓冲区将定期清空并转储到系统日志设备（大多数配置中为串口控制台）。以下是一些相关配置选项：

===========================================  ===================================================
设备驱动 -> USB 设备驱动支持                 .
``CONFIG_USBDEV_TRACE=y`` \t                 启用 USB 跟踪功能
``CONFIG_USBDEV_TRACE_NRECORDS=nnnn`` \t     在内存中缓冲 nnnn 条记录。如果你丢失了跟踪数据，
.                                            那么你需要增加此缓冲区的大小
.                                            （或增加跟踪缓冲区清空的速率）。
``CONFIG_USBDEV_TRACE_STRINGS=y`` \t         可选地，将跟踪 ID 编号转换为字符串。
.                                            此功能可能不是所有驱动都支持。
===========================================  ===================================================

===========================================  ===================================================
应用程序配置 -> NSH 库                        .
``CONFIG_NSH_USBDEV_TRACE=n`` \t             确保禁用 NSH 的任何内置跟踪。
===========================================  ===================================================

===============================================   ============================================
应用程序配置 -> 系统 NSH 附加组件                  .
``CONFIG_USBMONITOR=y`` \t                        启用 USB 监视器守护进程
``CONFIG_USBMONITOR_STACKSIZE=nnnn`` \t            设置 USB 监视器守护进程栈大小为 nnnn。默认为 2KiB。
``CONFIG_USBMONITOR_PRIORITY=50`` \t              设置 USB 监视器守护进程优先级为 nnnn。
.                                                 此优先级应该较低，以免
.                                                 干扰其他操作，但不能太低以至于
.                                                 无法足够快地转储缓冲的 USB 数据。默认为 50。
``CONFIG_USBMONITOR_INTERVAL=nnnn`` \t            每 nnnn 秒转储缓冲的 USB 数据。
.                                                 如果你丢失了缓冲的 USB 跟踪数据，那么降低
.                                                 此值将有助于提高 USB 跟踪缓冲区清空的速率。
``CONFIG_USBMONITOR_TRACEINIT=y``                 选择你想要跟踪的 USB 事件。
``CONFIG_USBMONITOR_TRACECLASS=y``                .
``CONFIG_USBMONITOR_TRACETRANSFERS=y``            .
``CONFIG_USBMONITOR_TRACECONTROLLER=y``           .
``CONFIG_USBMONITOR_TRACEINTERRUPTS=y``           .
===============================================   ============================================

注意：如果还启用了 USB 调试输出，两种输出都将出现在串口控制台。但是，调试输出将与跟踪输出异步，因此难以解释。
