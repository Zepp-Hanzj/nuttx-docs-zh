===================
``mcuboot`` MCUboot
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

描述
-----------

MCUboot 安全引导库的 NuttX 移植版本期望平台提供具有以下分区的 Flash 存储：

- ``CONFIG_MCUBOOT_PRIMARY_SLOT_PATH``：应用固件镜像主插槽的 MTD 分区；
- ``CONFIG_MCUBOOT_SECONDARY_SLOT_PATH``：应用固件镜像次插槽的 MTD 分区；
- ``CONFIG_MCUBOOT_SCRATCH_PATH``：Scratch 区域的 MTD 分区；

此外，这些是可选功能，可以启用：

- ``CONFIG_MCUBOOT_WATCHDOG``：如果启用了 ``CONFIG_WATCHDOG``，MCUboot 将重置由 ``CONFIG_MCUBOOT_WATCHDOG_DEVPATH`` 指示的看门狗定时器为当前超时值，防止任何即将到来的看门狗超时。

MCUboot 库的移植层由以下接口组成：

- ``<flash_map_backend/flash_map_backend.h>``，用于使 MCUboot 能够管理设备存储中的应用固件镜像插槽。
- ``<mcuboot_config/mcuboot_config.h>``，用于配置 MCUboot 的功能。
- ``<mcuboot_config/mcuboot_logging.h>``，用于提供日志记录功能。
- ``<os/os_malloc.h>``，用于使 MCUboot 能够访问操作系统内存管理接口。
- ``<sysflash/sysflash.h>``，用于配置系统闪存区域组织。

MCUboot 的 NuttX 移植版本在应用层实现，只需最少的底层存储设备特性知识。
这是通过 ``BCH`` 和 ``FTL`` 子系统实现的，它们使 MCUboot 能够通过字符设备驱动程序
使用标准 POSIX 文件系统操作（例如 ``open()`` / ``close()`` / ``read()`` / ``write()``）来管理 MTD 分区。

创建兼容 MCUboot 的应用固件镜像
-------------------------------------------------------

MCUboot 的一个常见用例是将其集成到固件更新代理中，这是安全固件更新子系统的重要组成部分。
通过 MCUboot API，应用程序能够安装新接收的应用固件镜像，并且一旦确认该应用固件镜像有效，
应用程序可以将其确认为稳定镜像。如果该应用固件镜像被认为是伪造的，MCUboot 提供了一个用于
使该更新无效的 API，这将触发回滚到最近的稳定应用固件镜像的程序。

``CONFIG_EXAMPLES_MCUBOOT_UPDATE_AGENT`` 示例演示了此工作流程，通过从 Web 服务器下载应用固件镜像，
安装它并在系统重置后触发下次启动的固件更新过程。还有 ``CONFIG_EXAMPLES_MCUBOOT_SLOT_CONFIRM``，
这是一个相当简单的示例，只是调用 MCUboot API 来确认正在执行的应用固件镜像为稳定镜像。

有关所有 MCUboot 示例的更多信息，请参阅 ``examples/mcuboot`` 目录。

在 NuttX 上使用 MCUboot 作为安全引导解决方案
------------------------------------------------

MCUboot 的 NuttX 移植还支持创建安全引导加载程序应用，只需最少的特定平台实现。
安全引导的逻辑实现在应用层由 MCUboot 库执行。一旦 MCUboot 验证了应用固件镜像，
它将应用固件镜像的加载和执行委托给特定平台的例程，通过 ``boardctl(BOARDIOC_BOOT_IMAGE)`` 调用访问。
然后每个平台必须提供 ``board_boot_image()`` 的实现，以执行引导新应用固件镜像所需的操作
（例如，反初始化外设，将程序计数器寄存器加载为应用固件镜像入口点地址）。

可以通过选择 ``CONFIG_MCUBOOT_BOOTLOADER`` 选项来启用 MCUboot 引导加载程序应用。

假设
-----------

IOCTL MTD 命令
~~~~~~~~~~~~~~~~~~

``<flash_map_backend/flash_map_backend.h>`` 的实现期望给定镜像分区的 MTD 驱动程序处理以下 ``ioctl`` 命令：

- ``MTDIOC_GEOMETRY``，用于检索有关 MTD 几何结构的信息，这是配置每个闪存区域大小所必需的。
- ``MTDIOC_ERASESTATE``，用于检索 MTD 擦除单元的字节值，这是实现 ``flash_area_erased_val()`` 接口所必需的。

写入访问对齐
~~~~~~~~~~~~~~~~~~~~~~

通过 ``flash_area_align()`` 接口，MCUboot 期望实现提供可通过 ``flash_area_write()`` 接口写入的最短数据长度。
NuttX 实现通过 ``BCH`` 和 ``FTL`` 层传递，它们适当处理底层 MTD 的写入对齐限制。
因此，NuttX 的 ``flash_area_align()`` 实现能够返回固定的 1 字节值，即使 MTD 不支持字节操作。

限制
-----------

``<flash_map_backend/flash_map_backend.h>`` 函数不是多任务安全的
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MCUboot 的文档对其公共接口的使用没有施加限制，但这并不意味着它们是线程安全的。
但是，关于 ``<flash_map_backend/flash_map_backend.h>`` 的 NuttX 实现，可以安全地声明它们**不是**多任务安全的。
NuttX 实现通过字符设备驱动程序管理 MTD 分区。由于文件描述符不能在不同任务之间共享，
如果一个任务调用 ``flash_area_open`` 而另一个任务调用 ``flash_area_<read/write/close>`` 并传递相同的
``struct flash_area`` 实例，将导致失败。
