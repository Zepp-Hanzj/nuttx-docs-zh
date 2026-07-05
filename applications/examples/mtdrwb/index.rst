=============================================
``mtdrwb`` MTD 预读和写缓冲
=============================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本示例提供了一个简单的 MTD 预读/写缓冲逻辑测试。

- ``CONFIG_EXAMPLES_MTDRWB`` – 启用 MTD R/W 缓冲测试示例。

- ``CONFIG_EXAMPLES_MTDRWB_ARCHINIT`` – 默认使用 ``drivers/mtd/rammtd.c`` 中的
  RAM MTD 设备。但可以通过定义 ``CONFIG_EXAMPLES_MTDRWB_ARCHINIT`` 来使用
  特定于架构的 MTD 驱动。在这种情况下，初始化逻辑将调用
  ``mtdrwb_archinitialize()`` 来获取 MTD 驱动实例。

当未定义 ``CONFIG_EXAMPLES_MTDRWB_ARCHINIT`` 时，此测试将使用
``drivers/mtd/rammtd.c`` 中的 RAM MTD 设备来模拟 FLASH。
分配的 RAM 驱动大小为：``CONFIG_EXMPLES_RAMMTD_ERASESIZE *
CONFIG_EXAMPLES_MTDRWB_NEBLOCKS``

- ``CONFIG_EXAMPLES_MTDRWB_ERASESIZE`` – 此值给出 MTD RAM 设备中一个擦除块的大小。
  这必须与 ``drivers/mtd/rammtd.c`` 中的默认配置完全匹配！

- ``CONFIG_EXAMPLES_MTDRWB_NEBLOCKS`` – 此值给出 MTD RAM 设备中的擦除块数。
