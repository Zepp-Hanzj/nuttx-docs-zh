===============
GD5F NAND Flash
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 为 GD5F 系列的 NAND Flash 提供支持。目前唯一支持的变体
是 4 Gbit（512 MB）的大容量 Flash。

该 Flash 通过选项 ``CONFIG_MTD_GD5F`` 启用。可以通过
``CONFIG_GD5F_SPIMODE`` 选项选择 SPI 模式，并通过
``CONFIG_GD5F_SPIFREQUENCY`` 选项选择通信频率。

闪存在使用前必须初始化。这通常在板卡启动阶段从板级支持包层完成。
此操作由以下函数执行。

.. code-block:: C

   #include <nuttx/mtd/mtd.h>

   FAR struct mtd_dev_s *gd5f_initialize(FAR struct spi_dev_s *dev,
                                         uint32_t spi_devid)
