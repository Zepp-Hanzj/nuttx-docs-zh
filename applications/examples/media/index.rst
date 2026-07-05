====================
``media`` 媒体测试
====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

媒体测试简单地将值写入字符驱动背后的媒体，并验证媒体是否可以成功写入和读取。
这个低级测试在新块驱动或 MTD 驱动的启动初期阶段非常有用，因为它避免了文件系统的复杂性。

此测试使用字符驱动，不能直接访问块或 MTD 驱动。
此测试适用于 EEPROM 字符驱动（参见 ``nuttx/drivers/eeprom``），
或用作字符驱动包装的块驱动（参见 ``nuttx/drivers/bch``）

.. code-block:: C

  int ret = bchdev_register(<path-to-block-driver>, <path-to-character-driver>,
                            false);

MTD 驱动需要额外的包装层，必须首先使用 FTL 包装将 MTD 驱动转换为块设备：

.. code-block:: C

  int ret = ftl_initialize(<N>, mtd);
  ret = bchdev_register(/dev/mtdblock<N>, <path-to-character-driver>, false);
