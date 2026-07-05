==========
TI ADS1242
==========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

ADS1242 是一款 24 位 SPI 供电的 ADC。此驱动程序支持读取 ADC 转换结果以及配置 ADC、设置输入通道等，这些功能通过 ioctl 调用实现。但是，它尚未实现标准 ADC 接口。

-  ``include/nuttx/analog/ads1242.h``。此头文件提供了使用 ADC 驱动程序所需的所有结构体和 API。
