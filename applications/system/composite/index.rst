===========================================
``composite`` USB 复合设备命令
===========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此逻辑添加了一个 NSH 命令来控制 USB 复合设备。复合设备中唯一支持的设备是
CDC/ACM 串口和 USB 大容量存储设备。复合设备中包含哪些设备通过配置结构体数组
传递给 ``composite_initialize()`` 函数来配置。

必需的总体配置：

启用硬件/处理器的 USB 支持，例如 ``SAMV7_USBDEVHS=y``

- ``CONFIG_USBDEV=y`` – USB 设备支持。
- ``CONFIG_USBDEV_COMPOSITE=y`` – USB 复合设备支持。
- ``CONFIG_COMPOSITE_IAD=y`` – 需要接口关联描述符。
- ``CONFIG_CDCACM=y`` – USB CDC/ACM 串口设备支持。
- ``CONFIG_CDCACM_COMPOSITE=y`` – USB CDC/ACM 串口复合设备支持。

接口、字符串描述符和端点编号通过上述配置结构体进行配置。CDC/ACM 串口设备
需要三个端点：一个中断驱动端点和两个批量端点。

- ``CONFIG_USBMSC=y`` – USB 大容量存储设备支持。
- ``CONFIG_USBMSC_COMPOSITE=y`` – USB 大容量存储复合设备支持。

与 CDC/ACM 的配置类似，描述符和端点编号通过配置结构体进行配置。

根据配置结构体，您需要配置不同的供应商 ID 和产品 ID。每个 ``VID``/``PID`` 对
设备而言是唯一的，因此对应于特定的配置。

Linux 会尝试检测设备类型，如果 ``VID``/``PID`` 对未知，则安装默认驱动程序。

Windows 要求已知且已安装的配置。使用 Atmel 硬件并安装了 Atmel-Studio 或
Atmel-USB 驱动程序后，您可以使用 Atmel 示例供应商 ID 和产品 ID 测试您的配置。

如果您的组合中配置了 USBMSC 和 CDC/ACM，则可以尝试使用：

- ``VID = 0x03EB`` (ATMEL)
- ``PID = 0x2424`` (ASF 示例，包含 MSC 和 CDC)

例如，如果您尝试测试最多七个 CDC 的配置，则：

- ``VID = 0x03EB`` (ATMEL)
- ``PID = 0x2426`` (ASF 示例，最多七个 CDC)

此附加组件可以构建为两个 NSH "内置" 命令：

- ``CONFIG_NSH_BUILTIN_APPS`` – 如果选择此选项：``conn`` 将连接 USB 复合设备；
  ``disconn`` 将断开 USB 复合设备。

此附加组件特有的配置选项：

- ``CONFIG_SYSTEM_COMPOSITE_DEBUGMM`` – 启用一些调试测试以检查内存使用和内存泄漏。

如果启用了 ``CONFIG_USBDEV_TRACE``（或 ``CONFIG_DEBUG_FEATURES`` 和
``CONFIG_DEBUG_USB``），则附加组件代码还将管理 USB 跟踪输出。跟踪输出量
可以使用以下选项控制：

- ``CONFIG_SYSTEM_COMPOSITE_TRACEINIT`` – 显示初始化事件。
- ``CONFIG_SYSTEM_COMPOSITE_TRACECLASS`` – 显示类驱动程序事件。
- ``CONFIG_SYSTEM_COMPOSITE_TRACETRANSFERS`` – 显示数据传输事件。
- ``CONFIG_SYSTEM_COMPOSITE_TRACECONTROLLER`` – 显示控制器事件。
- ``CONFIG_SYSTEM_COMPOSITE_TRACEINTERRUPTS`` – 显示中断相关事件。
