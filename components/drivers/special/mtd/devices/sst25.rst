===============
SST25 NOR Flash
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 为 SST25 系列的基于 SPI 的 NOR Flash 提供支持。
支持的容量最高可达 64 Mbit（8 MB）。

-----
SST25
-----

标准 SST25 驱动程序可以通过 ``CONFIG_MTD_SST25`` 选项启用。
此驱动程序支持最高 32 Mbit（4 MB）的容量。可以通过
``CONFIG_SST25_SPIMODE`` 选项选择 SPI 模式，并通过
``CONFIG_SST25_SPIFREQUENCY`` 选项选择通信频率。

如果启用了 ``CONFIG_SST25_SECTOR512`` 选项，该 Flash 允许模拟
512 字节的大擦除块。如果设置了 ``CONFIG_SST25_READONLY``，
还可以将 Flash 配置为只读。

Flash 的大小在设备初始化期间自动设置。

闪存在使用前必须初始化。这通常在板卡启动阶段从板级支持包层完成。
此操作由以下函数执行。

.. code-block:: C

   #include <nuttx/mtd/mtd.h>

   FAR struct mtd_dev_s *sst25_initialize(FAR struct spi_dev_s *dev)

-------
SST25XX
-------

此驱动程序支持 64 Mbit 及更大容量的 SST25 Flash。在 64 MBit
及更大的部件中，SST 将写入机制更改为支持页面写入，而不是像
较小部件那样的字节/字写入。因此，SST25 驱动程序与较大密度的
部件不兼容，必须改用 SST25XX 驱动程序。

此驱动程序通过 ``CONFIG_MTD_SST25XX`` 选项启用。可以通过
``CONFIG_SST25XX_SPIMODE`` 选项选择 SPI 模式，并通过
``CONFIG_SST25XX_SPIFREQUENCY`` 选项选择通信频率。

不同制造商可能生产这些部件。``0xBF`` 是 SST 制造的部件的
制造商 ID。这是由 ``CONFIG_SST25XX_MANUFACTURER`` 设置的默认
选项。存储器类型同理，由 ``CONFIG_SST25XX_MEMORY_TYPE`` 设置的
默认值为 ``0x25``。

Flash 的大小在设备初始化期间自动设置。

闪存在使用前必须初始化。这通常在板卡启动阶段从板级支持包层完成。
此操作由以下函数执行。

.. code-block:: C

   #include <nuttx/mtd/mtd.h>

   FAR struct mtd_dev_s *sst25xx_initialize(FAR struct spi_dev_s *dev)
