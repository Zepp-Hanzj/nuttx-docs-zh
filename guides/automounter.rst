============
自动挂载器
============

概述
===================
NuttX 实现了一个自动挂载器，可以更方便地使用 SD 卡或其他可移动介质。使用自动挂载器时，文件系统会在插入介质时自动挂载，在移除介质时自动卸载。

通过在 NuttX 配置中选择以下选项来启用自动挂载器::

  CONFIG_FS_AUTOMOUNTER=y


警告：SD 卡绝不应在未先卸载的情况下移除。这是为了避免数据和可能的文件系统损坏。如果您在移除时正在写入 SD 卡，情况确实如此。但是，如果您将 SD 卡用于只读访问，那么我想不出任何理由说明在未挂载的情况下移除卡会造成损害。

对于写入可移动介质的应用程序，自动卸载仍然是有益的（与保留损坏的挂载相比），尽管不应将其作为正确的解决方案来依赖。

板级特定支持
======================

与 NuttX 的许多组件一样，自动挂载器具有上层/下层架构：

* **上层** 上层是文件 ``fs/fs_automount.c``。该上层执行基本的自动挂载活动。它通过挂载和卸载介质上的文件系统来响应介质插入和移除事件。这包括处理卸载重试的逻辑：当应用程序在介质上有打开的文件时无法执行卸载。在这种情况下，自动挂载器将定期重试卸载，直到所有应用程序关闭对不存在介质上文件的引用。

* **下层** 下层由标准接口定义。该接口定义在头文件 ``include/nuttx/fs/automount.h`` 中。下层接口提供：(1) 挂载信息，包括文件系统类型、块驱动路径和挂载点路径，(2) 挂载和卸载重试延迟，以及 (3) 用于附加和管理介质插入/移除中断的回调。

示例实现
======================

该下层接口的示例实现位于 ``boards/arm/sama5/sama5d4-ek/src/sam_automount.c``。``boards/arm/sama5/sama5d4-ek/Kconfig`` 作为自动挂载器的板级特定配置。您可以在 ``boards/arm/sama5/sama5d4-ek/configs/nsh/defconfig`` 和 ``boards/arm/sama5/sama5d4-ek/configs/nxwm/defconfig`` 配置文件中查看配置设置::

  CONFIG_SAMA5D4EK_HSMCI0_AUTOMOUNT=y
  CONFIG_SAMA5D4EK_HSMCI0_AUTOMOUNT_FSTYPE="vfat"
  CONFIG_SAMA5D4EK_HSMCI0_AUTOMOUNT_BLKDEV="/dev/mmcsd0"
  CONFIG_SAMA5D4EK_HSMCI0_AUTOMOUNT_MOUNTPOINT="/mnt/sdcard"
  CONFIG_SAMA5D4EK_HSMCI0_AUTOMOUNT_DDELAY=1000
  CONFIG_SAMA5D4EK_HSMCI0_AUTOMOUNT_UDELAY=2000

这些设置决定了下层接口中的值。中断由 ``boards/arm/sama5/sama5d4-ek/src/sama5e4-ek.h`` 中定义的 PIO 引脚提供，接口和回调的实现在 ``boards/arm/sama5/sama5d4-ek/src/sam_automount.c`` 中。


