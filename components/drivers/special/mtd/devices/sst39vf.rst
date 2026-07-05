=================
SST39VF NOR Flash
=================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 为 SST39VF 系列的 NOR Flash 提供支持。
支持的容量最高可达 32 Mbit（4 MB）。

驱动程序假定设备位于配置的内存地址。此地址可通过
``CONFIG_SST39VF_BASE_ADDRESS`` 配置。驱动程序本身通过
``CONFIG_SST39FV`` 启用，注意选项名称中的拼写错误。

Flash 的大小在设备初始化期间自动设置。

闪存在使用前必须初始化。这通常在板卡启动阶段从板级支持包层完成。
此操作由以下函数执行。

.. code-block:: C

   #include <nuttx/mtd/mtd.h>

   FAR struct mtd_dev_s *sst39vf_initialize(void)
