============
RTC 驱动程序
============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 支持一个低级的两部分实时时钟（RTC）驱动程序。

#. "上半部分"，通用驱动程序，为应用程序代码提供通用 RTC 接口，
#. "下半部分"，平台特定的驱动程序，实现底层定时器控制以实现 RTC 功能。

支持 RTC 驱动程序的文件可以在以下位置找到：

-  **接口定义**。NuttX RTC 驱动程序的头文件位于 ``include/nuttx/timers/rtc.h``。此头文件包含 RTC 驱动程序的应用程序级别接口以及"上半部分"和"下半部分"驱动程序之间的接口。RTC 驱动程序使用标准字符驱动程序框架。
-  **"上半部分"驱动程序**。通用的"上半部分" RTC 驱动程序位于 ``drivers/timers/rtc.c``。
-  **"下半部分"驱动程序**。平台特定的 RTC 驱动程序位于 ``arch/<architecture>/src/<hardware>`` 目录，针对特定处理器 ``<architecture>`` 和特定 ``<chip>`` RTC 外设设备。
