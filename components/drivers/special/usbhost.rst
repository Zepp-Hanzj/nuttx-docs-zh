=====================
USB 主机端驱动
=====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

-  **USB 主机控制器驱动** 抽象目标芯片中的主机控制器设备。
   每个 USB 主机控制器驱动必须实现 ``struct usbhost_driver_s`` 和
   ``struct usbhost_connection_s`` 的实例，定义在
   ``include/nuttx/usb/usbhost.h`` 中。

   -  ``struct usbhost_driver_s`` 提供 USB 主机驱动和 USB 主机类驱动之间的接口。

   -  ``struct usbhost_connection_s`` 提供 USB 主机驱动和平台特定连接管理及设备枚举逻辑之间的接口。


   **示例**：``arch/arm/src/lpc17xx_40xx/lpc17_40_usbhost.c``、
   ``arch/arm/src/stm32/stm32_otgfshost.c``、
   ``arch/arm/src/sama5/sam_ohci.c`` 和
   ``arch/arm/src/sama5/sam_ehci.c``。

-  **USB 主机类驱动** 抽象连接到 USB 主机控制器的 USB 外设。
   每个 USB 主机类驱动必须实现 ``struct usbhost_class_s`` 的实例，
   同样定义在 ``include/nuttx/usb/usbhost.h`` 中。

   **示例**：``drivers/usbhost/usbhost_storage.c``

-  **USB 主机类驱动注册表**。NuttX USB 主机基础设施包含一个 *注册表*。
   在初始化期间，每个 USB 主机类驱动必须调用接口 ``usbhost_registerclass()``
   以将其接口添加到注册表中。稍后，当 USB 设备连接时，USB 主机控制器
   将在此注册表中查找支持已连接设备所需的 USB 主机类驱动。

   **示例**：``drivers/usbhost/usbhost_registry.c``、
   ``drivers/usbhost/usbhost_registerclass.c`` 和
   ``drivers/usbhost/usbhost_findclass.c``。

-  **已连接设备的检测和枚举**。每个 USB 主机设备控制器支持两种方法，
   用于检测和枚举新连接的设备（以及检测断开的设备）：

   -  ``int (*wait)(FAR struct usbhost_connection_s *drvr, FAR const bool *connected);``

      等待设备连接或断开。

   -  ``int (*enumerate)(FAR struct usbhost_connection_s *drvr, int rhpndx);``

      枚举连接到根集线器端口的设备。作为此枚举过程的一部分，
      驱动将 (1) 获取设备的配置描述符，(2) 从配置描述符中提取类 ID 信息，
      (3) 调用 ``usbhost_findclass()`` 查找支持此设备的类，
      (4) 调用 ``struct usbhost_registry_s interface`` 上的 ``create()`` 方法
      获取类实例，最后 (5) 调用 ``struct usbhost_class_s`` 接口的 ``connect()``
      方法。之后，类负责操作序列。

-  **绑定 USB 主机端驱动**。USB 主机端控制器驱动通常不由用户代码直接
   访问，而是绑定到另一个更高级别的 USB 主机类驱动。类驱动导出标准
   NuttX 设备接口，使得已连接的 USB 设备可以像其他类似的板载设备一样
   访问。例如，USB 主机大容量存储类驱动
   (``drivers/usbhost/usbhost_storage.c``) 将注册标准的 NuttX 块驱动
   接口（如 ``/dev/sda``），可用于挂载文件系统，就像其他块驱动实例一样。
   通常的绑定顺序是：

   #. 每个 USB 主机类驱动包含一个初始化入口点，在初始化时从应用程序调用。
      此驱动在此初始化期间调用 ``usbhost_registerclass()`` 以使其在支持的
      设备连接时可用。

      **示例**：``drivers/usbhost/usbhost_storage.c`` 中的函数
      ``usbhost_msc_initialize()``

   #. 每个应用程序必须包含一个 *等待* 线程，该线程 (1) 调用 USB 主机控制器
      驱动的 ``wait()`` 检测设备连接，然后 (2) 调用 USB 主机控制器驱动的
      ``enumerate`` 方法将已注册的 USB 主机类驱动绑定到 USB 主机控制器驱动。

   #. 作为绑定操作期间的一部分，USB 主机类驱动将在 ``/dev`` 目录下注册
      标准 NuttX 驱动的实例。重复上述示例，USB 主机大容量存储类驱动
      (``drivers/usbhost/usbhost_storage.c``) 将注册标准的 NuttX 块驱动
      接口（如 ``/dev/sda``），可用于挂载文件系统，就像其他块驱动实例一样。

      **示例**：参见 ``drivers/usbhost/usbhost_storage.c`` 中函数
      ``usbhost_initvolume()`` 中对 ``register_blockdriver()`` 的调用。

CDC-ECM 主机类驱动
=========================

CDC-ECM（以太网控制模型）主机类驱动
(``drivers/usbhost/usbhost_cdcecm.c``) 支持使用 USB 通信设备类以太网控制模型
暴露网络接口的 USB 设备。常见的设备类型包括：

-  **USB 转以太网适配器**，实现 CDC-ECM，通过 USB 端口提供有线以太网连接。

-  **蜂窝调制解调器和类似设备**，暴露 CDC-ECM 接口用于 IP 连接，
   例如在 USB 共享模式下运行的 LTE 调制解调器。

当兼容设备连接并枚举后，驱动注册标准的 NuttX 以太网网络接口 — 例如
``eth0`` — 并以与任何板载以太网驱动完全相同的方式集成到 NuttX 网络栈中。
然后可以使用标准 NSH 命令对接口应用正常的网络配置::

    ifup eth0
    ifconfig eth0 192.168.1.10 netmask 255.255.255.0

或者在选择 ``CONFIG_NETINIT_DHCPC=y`` 时通过 ``netinit`` 守护进程使用 DHCP。

驱动通过在板初始化期间调用 ``usbhost_cdcecm_initialize()`` 注册，
在 USB 主机等待线程开始枚举设备之前。

**示例**：``drivers/usbhost/usbhost_cdcecm.c``、
``boards/arm/stm32h5/nucleo-h563zi/configs/nshusbnet/defconfig``。
