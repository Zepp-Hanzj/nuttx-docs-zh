===============
SST26 NOR Flash
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 为 SST26 系列的基于 QSPI/SPI 的 NOR Flash 提供支持。
支持的容量最高可达 64 Mbit（8 MB）。

目前仅支持 SPI 接口。

可以通过 ``CONFIG_MTD_SST26`` 选项启用驱动程序。可以通过
``CONFIG_SST26_SPIMODE`` 选项选择 SPI 模式，并通过
``CONFIG_SST26_SPIFREQUENCY`` 选项选择通信频率。

不同制造商可能生产这些部件。``0xBF`` 是 SST 制造的部件的
制造商 ID。这是由 ``CONFIG_SST26_MANUFACTURER`` 设置的默认选项。
存储器类型同理，由 ``CONFIG_SST26_MEMORY_TYPE`` 设置的默认值为
``0x26``。

Flash 的大小在设备初始化期间自动设置。

闪存在使用前必须初始化。这通常在板卡启动阶段从板级支持包层完成。
此操作由以下函数执行。

.. code-block:: C

   #include <nuttx/mtd/mtd.h>

   FAR struct mtd_dev_s *sst26_initialize_spi(FAR struct spi_dev_s *dev,
                                              uint16_t spi_devid)
