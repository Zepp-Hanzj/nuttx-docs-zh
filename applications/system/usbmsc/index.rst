===========================================
``usbmsc`` USB 大容量存储设备命令
===========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此附加组件注册一个块设备驱动程序，然后使用 USB 存储类驱动程序导出该块设备。要使用此附加组件，您的板级逻辑必须提供以下函数：

::

  void board_usbmsc_initialize(void);

此函数将由 ``system/usbmsc`` 通过 ``boardctl`` 的 ``BOARDIOC_USBDEV_CONTROL`` 命令间接调用，以完成块设备驱动程序的实际注册。有关 ``board_usbmsc_initialize()`` 的实现示例，请参阅 ``boards/arm/lpc214x/mcu123-lpc214x/src/up_usbmsc.c`` 或 ``boards/arm/stm32/stm3210e-eval/src/usbmsc.c``。

配置选项：

- ``CONFIG_NSH_BUILTIN_APPS`` – 如果选择此选项，此附加组件可以构建为两个 NSH "内置"命令：``msconn`` 将连接 USB 大容量存储设备；``msdis`` 将断开 USB 存储设备连接。

- ``CONFIG_BOARDCTL`` – 启用 ``boardctl()`` 接口。

- ``CONFIG_BOARDCTL_USBDEVCTRL`` – 启用 ``BOARDIOC_USBDEV_CONTROL`` 的 ``boardctl()`` 命令。

- ``CONFIG_SYSTEM_USBMSC_NLUNS`` – 定义 USB 存储驱动程序导出的逻辑单元数（LUN）。每个 LUN 对应一个导出的块驱动程序（或块驱动程序的分区）。可以是 ``1``、``2`` 或 ``3``。默认值为 ``1``。

- ``CONFIG_SYSTEM_USBMSC_DEVMINOR1`` – 第一个 LUN 的块驱动程序次设备号。例如，``/dev/mmcsdN`` 中的 ``N``。用于注册块驱动程序。默认值为零。

- ``CONFIG_SYSTEM_USBMSC_DEVPATH1`` – 注册的块驱动程序的完整路径。默认值为 ``/dev/mmcsd0``

- ``CONFIG_SYSTEM_USBMSC_DEVMINOR2`` 和 ``CONFIG_SYSTEM_USBMSC_DEVPATH2`` 如果 ``CONFIG_SYSTEM_USBMSC_NLUNS`` 为 ``2`` 或 ``3``，则需要提供的类似参数。无默认值。

- ``CONFIG_SYSTEM_USBMSC_DEVMINOR3`` 和 ``CONFIG_SYSTEM_USBMSC_DEVPATH3`` 如果 ``CONFIG_SYSTEM_USBMSC_NLUNS`` 为 ``3``，则需要提供的类似参数。无默认值。

- ``CONFIG_SYSTEM_USBMSC_DEBUGMM`` – 启用一些调试测试以检查内存使用情况和内存泄漏。

如果启用了 ``CONFIG_USBDEV_TRACE``（或 ``CONFIG_DEBUG_FEATURES`` 和 ``CONFIG_DEBUG_USB``），则代码还将管理 USB 跟踪输出。跟踪输出量可以使用以下选项控制：

- ``CONFIG_SYSTEM_USBMSC_TRACEINIT`` – 显示初始化事件。
- ``CONFIG_SYSTEM_USBMSC_TRACECLASS`` – 显示类驱动程序事件。
- ``CONFIG_SYSTEM_USBMSC_TRACETRANSFERS`` – 显示数据传输事件。
- ``CONFIG_SYSTEM_USBMSC_TRACECONTROLLER`` – 显示控制器事件。
- ``CONFIG_SYSTEM_USBMSC_TRACEINTERRUPTS`` – 显示中断相关事件。

错误结果始终在跟踪输出中显示。

**注意 1**：当构建为 NSH 附加命令（``CONFIG_NSH_BUILTIN_APPS=y``）时，应注意确保 SD 驱动器（或其他存储设备）在配置 USB 存储设备时未被使用。具体来说，应像下面这样卸载 SD 驱动器：

::

  nsh> mount -t vfat /dev/mmcsd0 /mnt/sdcard  # Card is mounted in NSH
  ...
  nsh> umount /mnd/sdcard                     # Unmount before connecting USB!!!
  nsh> msconn                                 # Connect the USB storage device
  ...
  nsh> msdis                                  # Disconnect USB storate device
  nsh> mount -t vfat /dev/mmcsd0 /mnt/sdcard  # Restore the mount

不这样做可能会导致 SD 卡格式损坏。

**注意 2**：此附加组件使用了内部 USB 设备驱动程序接口。因此，它依赖于通常不提供给用户空间程序的内部操作系统接口。所以，如果 NuttX 构建为保护模式或内核模式（``CONFIG_BUILD_PROTECTED`` 或 ``CONFIG_BUILD_KERNEL``），则无法使用此附加组件。
