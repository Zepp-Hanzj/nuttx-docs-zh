==================
SPI 设备驱动
==================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

-  ``include/nuttx/spi/spi.h``。使用 SPI 驱动所需的
   所有结构和 API 都在此头文件中提供。

-  ``struct spi_ops_s``。每个 SPI 设备驱动必须实现
   ``struct spi_ops_s`` 的一个实例。该结构定义了包含以下方法的调用表：

-  **绑定 SPI 驱动**。SPI 驱动通常不由用户代码直接
   访问，而是绑定到另一个更高级别的设备驱动。例如参见
   ``drivers/mmcsd/mmcsd_spi.c`` 中的
   ``int mmcsd_spislotinitialize(int minor, int slotno, FAR struct spi_dev_s *spi)``。
   通常的绑定顺序是：

   #. 从硬件特定的 SPI 设备驱动获取 ``struct spi_dev_s`` 的
      实例，然后
   #. 将该实例提供给更高级别设备驱动的初始化方法。

-  **示例**：``drivers/loop.c``、
   ``drivers/mmcsd/mmcsd_spi.c``、``drivers/ramdisk.c`` 等。
