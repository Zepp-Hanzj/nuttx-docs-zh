=============
AT24XX EEPROM
=============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 为基于 I2C 的 AT24XX EEPROM 提供支持。这些包括 AT24C32、
AT24C64、AT24C128 和 AT24C256。

驱动程序通过选项 ``CONFIG_MTD_AT24XX` 启用。可以通过启用
``CONFIG_AT24XX_MULTI`` 来支持多个 AT25XX 设备。这将为多个
AT24XX 设备构建额外的支持，每个设备具有动态分配的设备结构和
独立的 I2C 地址（但其他方面相同——尚不支持多个不同的 AT24xx
设备）。

EEPROM 的大小由 ``CONFIG_AT24XX_SIZE`` 配置。这是 AT24Cxx
部件号中的 XX。例如，如果您有 AT24C64，则正确的值为 64。
此值也是部件的容量（以千位为单位）。例如，64 支持 64 Kbit
或 64/8 = 8 KiB。

使用单个 EEPROM 时的静态 I2C 地址可以通过 ``CONFIG_AT24XX_ADDR``
选项配置。

如果设备支持扩展存储器，则可以设置 ``CONFIG_AT24XX_EXTENDED``
以启用 ``MTDIOC_EXTENDED`` ioctl() 操作。当选择扩展操作时，
对驱动程序读取方法的调用将从扩展存储器区域返回数据。扩展存储器
区域大小由 ``CONFIG_AT24XX_EXTSIZE`` 配置。

I2C 通信频率可以通过 ``CONFIG_AT24XX_FREQUENCY`` 设置。
此值必须表示有效的 I2C 速度（通常小于 400,000），否则驱动
程序可能失败。

存储器在使用前必须初始化。这通常在板卡启动阶段从板级支持包层
完成。此操作由以下函数执行。

.. code-block:: C

   #include <nuttx/mtd/mtd.h>

   #ifdef CONFIG_AT24XX_MULTI
   FAR struct mtd_dev_s *at24c_initialize(FAR struct i2c_master_s *dev,
                                          uint8_t address)
   #else
   FAR struct mtd_dev_s *at24c_initialize(FAR struct i2c_master_s *dev)
   #endif
