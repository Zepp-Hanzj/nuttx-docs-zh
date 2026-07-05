======
EEPROM
======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

.. warning::

   本页描述使用字符驱动程序进行 EEPROM 连接。有关更标准的 MTD 接口，请参考 :doc:`MTD 文档 <../special/mtd/index>`。
   参见 `MTD 与字符驱动程序 <mtd_vs_char_>`_ 了解何时使用哪种接口。

EEPROM 是一种存储技术设备（MTD）。

EEPROM 是像 FLASH 一样的非易失性存储器，但在底层存储技术和使用方面有许多不同：它们可能不会组织成块（至少从用户的角度来看），并且在重新写入之前不需要擦除 EEPROM 存储器。

此外，EEPROM 往往比 FLASH 部件小得多，通常只有几千字节，而 FLASH 则有几兆字节。EEPROM 往往用于保留少量设备配置信息；FLASH 往往用于程序或大量数据存储。因此，使用更复杂的 MTD 接口可能不太方便，而可以使用 EEPROM 驱动程序提供的简单字符接口。

.. _mtd_vs_char:

MTD 驱动与字符驱动
==============================

MTD 驱动
  当 EEPROM 应作为块设备（`/dev/mtdX`）出现并打算挂载文件系统时使用。MTD 层处理擦除、读取和写入粒度。

字符驱动
  当需要直接、随机访问原始 EEPROM 的读写操作时使用，无需文件系统的开销。这适用于存储少量配置参数、校准数据或任何不需要完整文件系统的小型数据块。

EEPROM 设备支持
=====================

drivers/eeprom/spi_xx25xx.c
---------------------------

这是一个用于 SPI EEPROM 的驱动程序，使用与 25AA160 相同的命令::

    Manufacturer Device     Bytes PgSize SecSize AddrLen
    Microchip
                 25xx010A     128     16      16       1
                 25xx020A     256     16      16       1
                 25AA02UID    256     16      16       1
                 25AA02E48    256     16      16       1
                 25AA02E64    256     16      16       1
                 25xx040      512     16      16       1+bit
                 25xx040A     512     16      16       1+bit
                 25xx080     1024     16      16       1
                 25xx080A    1024     16      16       2
                 25xx080B    1024     32      32       2
                 25xx080C    1024     16      16       x
                 25xx080D    1024     32      32       x
                 25xx160     2048     16      16       2
                 25xx160A/C  2048     16      16       2
                 25xx160B/D  2048     32      32       2
                 25xx160C    2048     16      16       2
                 25xx160D    2048     32      32       2
                 25xx320     4096     32      32       2
                 25xx320A    4096     32      32       2
                 25xx640     8192     32      32       2
                 25xx640A    8192     32      32       2
                 25xx128    16384     64      64       2
                 25xx256    32768     64      64       2
                 25xx512    65536    128   16384       2
                 25xx1024  131072    256   32768       3
    Atmel
                 AT25010B     128      8       8       1
                 AT25020B     256      8       8       1
                 AT25040B     512      8       8       1+bit
                 AT25080B    1024     32      32       2
                 AT25160B    2048     32      32       2
                 AT25320B    4096     32      32       2
                 AT25640B    8192     32      32       2
                 AT25128B   16384     64      64       2
                 AT25256B   32768     64      64       2
                 AT25512    65536    128     128       2
                 AT25M01   131072    256     256       3
    ST Microelectronics
                 M95010       128     16      16       1
                 M95020       256     16      16       1
                 M95040       512     16      16       1+bit
                 M95080      1024     32      32       2
                 M95160      2048     32      32       2
                 M95320      4096     32      32       2
                 M95640      8192     32      32       2
                 M95128     16384     64      64       2
                 M95256     32768     64      64       2
                 M95512     65536    128     128       2
                 M95M01    131072    256     256       3
                 M95M02    262144    256     256       3

drivers/eeprom/i2c_xx24xx.c
---------------------------

这是一个用于 I2C EEPROM 的驱动程序，使用与 xx24xx 相同的命令::

    Manufacturer Device     Bytes PgSize AddrLen DevAddr
    Microchip
                 24xx00        16     1    1     1010000 Special case
                 24xx01       128     8    1     1010000
                 24xx02       256     8    1     1010000
                 24xx04       512     16   1     101000P
                 24xx08      1024     16   1     10100PP
                 24xx16      2048     16   1     1010PPP
                 24xx32      4096     32   2     1010AAA
                 24xx64      8192     32   2     1010AAA
                 24xx128    16384     64   2     1010AAA
                 24xx256    32768     64   2     1010AAA
                 24xx512    65536    128   2     1010AAA
                 24xx1025  131072    128   2     1010PAA Special case: address
                                                         bit is shifted.
                 24xx1026  131072    128   2     1010AAP
    Atmel
                 AT24C01      128     8    1     1010AAA
                 AT24C02      256     8    1     1010AAA
                 AT24C04      512    16    1     1010AAP P bits = word address
                 AT24C08     1024    16    1     1010APP
                 AT24C16     2048    16    1     1010PPP
                 AT24C32     4096    32    2     1010AAA
                 AT24C64     8192    32    2     1010AAA
                 AT24C128   16384    64    2     10100AA
                 AT24C256   32768    64    2     10100AA
                 AT24C512   65536   128    2     10100AA
                 AT24C1024 131072   256    2     10100AP
    ST Microelectronics
                 M24C01       128    16    1     1010AAA
                 M24C02       256    16    1     1010AAA
                 M24C04       512    16    1     1010AAP
                 M24C08      1024    16    1     1010APP
                 M24C16      2048    16    1     1010PPP
                 M24C32      4096    32    2     1010AAA ID pages supported
                                                         as a separate device
                 M24C64      8192    32    2     1010AAA
                 M24128     16384    64    2     1010AAA
                 M24256     32768    64    2     1010AAA
                 M24512     65536   128    2     1010AAA
                 M24M01    131072   256    2     1010AAP
                 M24M02    262144   256    2     1010APP

IOCTL 命令
==============

完整的 ``ioctl()`` 命令列表可在 ``include/nuttx/eeprom/eeprom.h`` 中找到。

- ``EEPIOC_GEOMETRY``
    *参数：* ``struct eeprom_geometry_s *``

    获取 EEPROM 几何信息

- ``EEPIOC_SETSPEED``
    *参数：* ``uint32_t``

    设置 SPI/I2C 总线频率

- ``EEPIOC_PAGEERASE``
    *参数：* ``unsigned long``

    根据索引擦除 EEPROM 页面，如果设备支持则使用专用命令。

- ``EEPIOC_SECTORERASE``
    *参数：* ``unsigned long``

    根据索引擦除 EEPROM 扇区，如果设备支持则使用专用命令。对于没有扇区的设备，等同于页面擦除。

- ``EEPIOC_CHIPERASE``
    *参数：* ``void``

    擦除整个 EEPROM，如果设备支持则使用专用命令。

- ``EEPIOC_BLOCKPROTECT``
    *参数：* ``uint8_t``

    设置 EEPROM 的块保护位。对于状态寄存器中有两个块保护位的 25AA160 兼容 EEPROM，参数可以是：

    - ``0`` 表示无写保护，
    - ``1`` 设置状态寄存器的块保护位 0，
    - ``2`` 设置状态寄存器的块保护位 1，
    - ``3`` 同时设置块保护位 0 和 1。

文件系统
============

大多数 EEPROM 部件太小，不适合使用文件系统。字符驱动程序接口对于这些小部件是最优的，因为您可以像打开和访问单个固定大小文件一样打开和访问 EEPROM 部件。

要将它们与文件系统一起使用，最好使用 :doc:`MTD 驱动 <../special/mtd/index>`。
