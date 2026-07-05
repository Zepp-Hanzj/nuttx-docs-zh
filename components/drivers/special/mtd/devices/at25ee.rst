=============
AT25EE EEPROM
=============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 为基于 SPI 的 EEPROM AT25EE 提供支持。支持的容量为
16 Mbit（2 MB）。EEPROM 上的 MTD 性能可能较差，因此仅在
EEPROM 时钟速度为 10MHz 或更高时才可能可用。使用与 25AA160
相同命令的 EEPROM 应该可以正常工作。

驱动程序通过选项 ``CONFIG_MTD_AT25EE`` 启用。

对于在 AT25 EEPROM 上使用文件系统的应用，极小的页面大小将导致
EEPROM 使用效率非常低。在这种情况下，最好将块由页面的"簇"组成，
使文件系统块大小为 128、256 或 512 字节。无论如何，块大小*必须*
是页面数量的整数倍，并且通常需要是 2 的因数。这需要用户自行检查！

您可以通过选择 ``CONFIG_USE_NATIVE_AT25EE_BLOCK_SIZE`` 将 EEPROM
配置为使用原生块，或使用 ``CONFIG_MANUALLY_SET_AT25EE_BLOCK_SIZE``
选项手动设置。如果设置了后者，则选项
``CONFIG_MANUAL_AT25EE_BLOCK_SIZE`` 将变为可用。

EEPROM 在写入前不需要擦除。但是，在某些应用中（例如需要擦除验证，
或特定文件系统要求），可以通过 ``CONFIG_AT25EE_ENABLE_BLOCK_ERASE``
启用块擦除（即将每个字节写入 0xff）。

存储器在使用前必须初始化。这通常在板卡启动阶段从板级支持包层
完成。此操作由以下函数执行。

.. code-block:: C

   #include <nuttx/mtd/mtd.h>

   FAR struct mtd_dev_s *at25ee_initialize(FAR struct spi_dev_s *dev,
                                           uint16_t spi_devid,
                                           enum eeprom_25xx_e devtype,
                                           int readonly)
