====================
M25P/MT25Q NOR Flash
====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 为 M25P/MT25Q 系列的基于 SPI 的 NOR Flash 提供支持。
支持的容量最高可达 1 Gbit（128 MB）。

可以通过 ``CONFIG_MTD_M25P`` 选项启用驱动程序。可以通过
``CONFIG_M25P_SPIMODE`` 选项选择 SPI 模式，并通过
``CONFIG_M25P_SPIFREQUENCY`` 选项选择通信频率。

不同制造商可能生产这些部件。``0x20`` 是 STMicro 制造的部件的
制造商 ID。这是由 ``CONFIG_M25P_MANUFACTURER`` 设置的默认选项。
例如，如果您使用的是 Macronix International MX25 系列 FLASH，
正确的制造商 ID 应为 ``0xC2``。配置选项 ``CONFIG_M25P_MEMORY_TYPE``
设置存储器类型值。M25 P 系列的存储器类型为 ``0x20``，但驱动程序
也支持 F 系列设备，例如 EON EN25F80 部件，它增加了 4K 扇区
擦除功能。EON 的 F 系列部件的存储器类型为 ``0x31``。当启用可以
使用 4K 扇区擦除大小的文件系统（如 SMART）时，将自动启用该功能。

某些设备（如 EON EN25F80）支持较小的擦除块大小（4K 对比 64K）。
选项 ``CONFIG_M25P_SUBSECTOR_ERASE`` 启用对子扇区擦除的支持。
如果启用此选项，SMART 文件系统可以利用此功能。

Flash 的大小在设备初始化期间自动设置。

闪存在使用前必须初始化。这通常在板卡启动阶段从板级支持包层完成。
此操作由以下函数执行。

.. code-block:: C

   #include <nuttx/mtd/mtd.h>

   FAR struct mtd_dev_s *m25p_initialize(FAR struct spi_dev_s *dev)
