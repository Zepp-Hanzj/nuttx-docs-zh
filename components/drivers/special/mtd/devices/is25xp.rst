================
IS25XP NOR Flash
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 为 IS25XP 系列的基于 SPI 的 NOR Flash 提供支持。
支持的容量最高可达 512 Mbit（64 MB）。

可以通过 ``CONFIG_MTD_IS25PX`` 选项启用驱动程序。可以通过
``CONFIG_IS25PX_SPIMODE`` 选项选择 SPI 模式，并通过
``CONFIG_IS25PX_SPIFREQUENCY`` 选项选择通信频率。

Flash 的大小在设备初始化期间自动设置。

闪存在使用前必须初始化。这通常在板卡启动阶段从板级支持包层完成。
此操作由以下函数执行。

.. code-block:: C

   #include <nuttx/mtd/mtd.h>

   FAR struct mtd_dev_s *is25xp_initialize(FAR struct spi_dev_s *dev,
                                           uint16_t spi_devid)
