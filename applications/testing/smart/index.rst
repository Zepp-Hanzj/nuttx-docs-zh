===========================
``smart`` SMART File System
===========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 SMART 文件系统的测试，源自 ``testing/nxffs``。

- ``CONFIG_TESTING_SMART`` – 启用 SMART 文件系统示例。

- ``CONFIG_TESTING_SMART_ARCHINIT`` – 默认使用 ``drivers/mtd/rammtd.c`` 中的 RAM MTD 设备。但可以通过定义 ``CONFIG_TESTING_SMART_ARCHINIT`` 来使用架构特定的 MTD 驱动程序。在这种情况下，初始化逻辑将调用 ``smart_archinitialize()`` 来获取 MTD 驱动程序实例。

- ``CONFIG_TESTING_SMART_NEBLOCKS`` – 当未定义 ``CONFIG_TESTING_SMART_ARCHINIT`` 时，此测试将使用 ``drivers/mtd/rammtd.c`` 中的 RAM MTD 设备来模拟 FLASH。在这种情况下，必须提供此值以给出 MTD RAM 设备中的擦除块数量。分配的 RAM 驱动器大小为：``CONFIG_RAMMTD_ERASESIZE * CONFIG_TESTING_SMART_NEBLOCKS``。

- ``CONFIG_TESTING_SMART_MAXNAME`` – 确定文件系统中使用的名称的最大大小。

- ``CONFIG_TESTING_SMART_MAXFILE`` – 确定文件的最大大小。
- ``CONFIG_TESTING_SMART_MAXIO`` – 最大 I/O，默认 ``347``。
- ``CONFIG_TESTING_SMART_MAXOPEN`` – 最大打开文件数。
- ``CONFIG_TESTING_SMART_MOUNTPT`` – SMART 挂载点。
- ``CONFIG_TESTING_SMART_NLOOPS`` – 测试循环次数，默认 ``100``。
- ``CONFIG_TESTING_SMART_VERBOSE`` – 详细输出。
