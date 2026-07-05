================
AT45DB NOR Flash
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 为基于 SPI 的 NOR Flash AT45DB 提供支持。支持的容量为
16 Mbit（2 MB）。

驱动程序通过选项 ``CONFIG_MTD_AT64DB`` 启用。可以通过
``CONFIG_AT64DB_FREQUENCY`` 选项设置通信频率。

选项 ``CONFIG_AT64DB_PREWAIT`` 启用高性能写入逻辑，
选项 ``CONFIG_AT64DB_PRWSAVE`` 允许设备进入省电模式。

闪存在使用前必须初始化。这通常在板卡启动阶段从板级支持包层完成。
此操作由以下函数执行。

.. code-block:: C

   #include <nuttx/mtd/mtd.h>

   FAR struct mtd_dev_s *at45db_initialize(FAR struct spi_dev_s *spi)
