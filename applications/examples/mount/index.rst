==========================
``mount`` 挂载文件系统
==========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

包含一个简单的文件系统挂载点测试。

- ``CONFIG_EXAMPLES_MOUNT_DEVNAME`` – 用户提供的要挂载的块设备名称。
  如果未提供 ``CONFIG_EXAMPLES_MOUNT_DEVNAME``，则将配置 RAM 磁盘。

- ``CONFIG_EXAMPLES_MOUNT_NSECTORS`` – 当未定义 ``CONFIG_EXAMPLES_MOUNT_DEVNAME`` 时，
  RAM 磁盘中的扇区数。

- ``CONFIG_EXAMPLES_MOUNT_SECTORSIZE`` – 当未定义 ``CONFIG_EXAMPLES_MOUNT_DEVNAME`` 时，
  RAM 磁盘中每个扇区的大小。

- ``CONFIG_EXAMPLES_MOUNT_RAMDEVNO`` – 用于挂载 RAM 磁盘的 RAM 设备次设备号，
  当未定义 ``CONFIG_EXAMPLES_MOUNT_DEVNAME`` 时使用。默认为零（表示将使用 ``/dev/ram0``）。
