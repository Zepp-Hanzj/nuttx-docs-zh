================
单总线驱动
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

---------------------------------------------------------------
在同一总线上连接同系列的多个设备
---------------------------------------------------------------

单总线（1Wire）是一种总线，因此驱动程序应允许指定应用程序需要连接的设备。此外，驱动程序还应允许扫描整个总线以发现可用设备。正确的方式应该是使用一个后台线程持续扫描总线，并可能将设备注册到文件系统中。

但这可能过于复杂，因此一个更简单的解决方案是调用扫描 ``ioctl``，获取可用设备，选择我们需要的设备，并将其告知驱动程序。

.. c:macro:: ONEWIREIOC_GETFAMILYROMS

    一个 ``ioctl`` 调用，返回所有已扫描到的同系列设备的 ROM（系列取决于驱动程序）。所有记录都存储到应用程序提供的 ``struct onewire_availroms_s`` 对象中。
    用法：``ioctl(fd, ONEWIREIOC_GETFAMILYROMS, (unsigned long *)&query)``

.. c:struct:: onewire_availroms_s
.. code-block:: c

    struct onewire_availroms_s
    {
        uint64_t *roms;
        int maxroms;
        int actual;
    };

驱动程序能提供的最大记录数由用户在 ``maxroms`` 字段中指定。用户还必须在 ``roms`` 字段中指定一个 ``uint64_t`` 缓冲区，供驱动程序存储扫描到的设备。扫描到的设备数量由驱动程序设置在 ``actual`` 字段中。

.. c:macro:: ONEWIREIOC_SETROM

设置驱动程序应连接的设备的 ROM。请注意，ROM 参数是一个指向 ``uint64_t`` 变量的指针，而不是 ``uint64_t`` 值，原因是 ``ioctl`` 中的 ``arg`` 是 ``unsigned long``，在许多架构上是 32 位。
用法：``ioctl(fd, ONEWIREIOC_SETROM, (unsigned long *)&romcode)``

-----------------------------------------
Maxim/Analog Devices DS2XXX EEPROM 驱动
-----------------------------------------

此驱动程序可用于连接以下带暂存器的 EEPROM（也在 ``include/nuttx/1wire/1wire_ds2xxx.h`` 中的 ``enum ds2xxx_eeproms_e`` 中指定）：

- DS2430：32 字节，8 字节暂存器，
- DS2431：128 字节，8 字节暂存器，
- DS2432：128 字节，8 字节暂存器，
- DS2433：512 字节，32 字节暂存器，
- DS28E04：512 字节，32 字节暂存器，
- DS28E07：128 字节，8 字节暂存器，
- DS28EC20：2560 字节，32 字节暂存器。

每个驱动程序实例只能连接一种 EEPROM 类型。如果要在同一总线上连接多个 EEPROM，需要使用两个驱动程序（例如两个 ``/dev`` 文件）。

目前，仅实现了 EEPROM 的基本读写操作。锁定相应页面的特殊 ioctl 调用（或可能的其他 EEPROM 功能）尚未实现。
由于 EEPROM 驱动程序是基于字符的，您可以使用 ``lseek`` 在 EEPROM 中移动。暂存器的非对齐读写是可能的。

驱动程序的 API
============

.. c:enum:: ds2xxx_eeproms_e
.. code-block:: c

    enum ds2xxx_eeproms_e
    {
        EEPROM_DS2430 = 0,
        EEPROM_DS2431,
        EEPROM_DS2432,
        EEPROM_DS2433,
        EEPROM_DS28E04,
        EEPROM_DS28E07,
        EEPROM_DS28EC20,
        EEPROM_DS_COUNT
    };

所有支持的 EEPROM 的枚举（``EEPROM_DS_COUNT`` 除外）。

.. c:function:: int ds2xxx_initialize(FAR struct onewire_dev_s *dev, enum ds2xxx_eeproms_e devtype, FAR char *devname)

    将 ``onewire_dev_s`` 结构体绑定到此驱动程序，使其能够连接 DS2XXX 单总线 EEPROM。用户必须指定设备类型以及设备名称（例如 ``/dev/ds2xxx``）。

    :param dev: 指向底层结构体的指针
    :param devtype: 要连接的 EEPROM 类型
    :param devname: 注册的文件名

    :return: 成功返回 0 并注册驱动程序，失败返回取负的 errno 值

示例用法
-------------

注册驱动程序（STM32 BSP，DS2431 存储器）：

.. code-block:: c

    struct onewire_dev_s *lwhalf;
    lwhalf = stm32_1wireinitialize(0);
    ds2xxx_initialize(lwhalf, EEPROM_DS2431, "/dev/ds2431");

应用程序用法（假设所有调用都成功）：

.. code-block:: c

    /* 写入特定的 EEPROM */

    int fd = open("/dev/ds2xxx", O_RDWR);
    struct onewire_availroms_s query;
    uint64_t romarr[8];
    query.roms = romarr;
    query.maxroms = 8;
    ioctl(fd, ONEWIREIOC_GETFAMILYROMS, (unsigned long *)&query);

    /* 假设驱动程序在 query.actual 中返回 3。我们要访问最后一个设备。 */

    ioctl(fd, ONEWIREIOC_SETROM, (unsigned long *)&query.roms[query.actual - 1]);

    lseek(fd, 10, SEEK_SET);
    write(fd, "HELLO", 5);
