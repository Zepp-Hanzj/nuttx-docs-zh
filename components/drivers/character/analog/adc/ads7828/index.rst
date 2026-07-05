==========
TI ADS7828
==========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

ADS7828 是一款 12 位 I2C 供电的 ADC。此驱动程序支持通过 ioctl 调用读取单个或多个 ADC 转换结果以及配置 ADC。

-  ``include/nuttx/analog/ads7828.h``。此头文件提供了使用 ADC 驱动程序所需的所有结构体和 API。
