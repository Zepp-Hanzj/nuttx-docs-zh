===============
MX25R NOR Flash
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 为 MX25R 系列的基于 QSPI 的 NOR Flash 提供支持。
支持的容量最高可达 256 Mbit（32 MB）。

可以通过 ``CONFIG_MTD_MX25RXX`` 选项启用驱动程序。可以通过
``CONFIG_MX25RXX_QSPIMODE`` 选项选择 QSPI 模式，并通过
``CONFIG_MX25RXX_QSPI_FREQUENCY`` 选项选择通信频率。此频率
用于除读取命令以外的所有命令。读取命令的速度由
``CONFIG_MX25RXX_QSPI_READ_FREQUENCY`` 选项配置。

如果启用了 ``CONFIG_MX25RXX_SECTOR512`` 选项，该 Flash 允许
模拟 512 字节的大擦除块；如果设置了 ``CONFIG_MX25RXX_PAGE128``，
则允许 128 字节的大页面。

还可以通过启用 ``CONFIG_MX25RXX_LXX`` 选项以 MX25LXX 模式
运行驱动程序。

Flash 的大小在设备初始化期间自动设置。

闪存在使用前必须初始化。这通常在板卡启动阶段从板级支持包层完成。
此操作由以下函数执行。

.. code-block:: C

   #include <nuttx/mtd/mtd.h>

   FAR struct mtd_dev_s *mx25rxx_initialize(FAR struct qspi_dev_s *qspi,
                                            bool unprotect)
