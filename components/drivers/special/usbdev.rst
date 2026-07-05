=======================
USB 设备端驱动
=======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

-  ``include/nuttx/usb/usbdev.h``。使用 USB 设备端驱动所需的
   所有结构和 API 都在此头文件中提供。

-  ``include/nuttx/usb/usbdev_trace.h``。使用 NuttX USB 设备驱动
   跟踪功能所需的声明。该 USB 跟踪功能详见
   :ref:`单独文档 <usbtrace>`。

-  ``struct usbdev_s``。每个 USB 设备控制器驱动必须实现
   ``struct usbdev_s`` 的一个实例。此结构定义在
   ``include/nuttx/usb/usbdev.h`` 中。

   **示例**：``arch/arm/src/dm320/dm320_usbdev.c``、
   ``arch/arm/src/lpc17xx_40xx/lpc17_40_usbdev.c``、
   ``arch/arm/src/lpc214x/lpc214x_usbdev.c``、
   ``arch/arm/src/lpc313x/lpc313x_usbdev.c`` 和
   ``arch/arm/src/stm32/stm32_usbdev.c``。

-  ``struct usbdevclass_driver_s``。每个 USB 设备类驱动必须实现
   ``struct usbdevclass_driver_s`` 的一个实例。此结构也定义在
   ``include/nuttx/usb/usbdev.h`` 中。

   **示例**：``drivers/usbdev/pl2303.c`` 和
   ``drivers/usbdev/usbmsc.c``

-  **绑定 USB 设备端驱动**。USB 设备端控制器驱动通常不由用户代码
   直接访问，而是绑定到另一个更高级别的 USB 设备类驱动。类驱动
   随后被配置以导出 USB 设备功能。通常的绑定顺序是：

   #. 每个 USB 设备类驱动包含一个初始化入口点，在初始化时从
      应用程序调用。

      **示例**：``drivers/usbdev/pl2303.c`` 中的函数
      ``usbdev_serialinitialize()`` 和
      ``drivers/usbdev/usbmsc.c`` 中的函数

   #. 这些初始化函数调用驱动 API ``usbdev_register()``。此驱动函数
      将 USB 类驱动 *绑定* 到 USB 设备控制器驱动，完成初始化。

