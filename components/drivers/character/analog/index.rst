========================
模拟（ADC/DAC）驱动
========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 模拟驱动程序分为两部分：

#. "上半部分"，通用驱动程序，为应用程序级代码提供通用模拟接口，以及
#. "下半部分"，特定于平台的驱动程序，实现底层控制以实现模拟功能。

-  NuttX 模拟驱动程序的通用头文件位于 ``include/nuttx/analog/``。这些头文件包括模拟驱动程序的应用程序级接口以及"上半部分"和"下半部分"驱动程序之间的接口。
-  通用模拟逻辑和可共享的模拟驱动程序位于 ``drivers/analog/``。
-  特定于平台的驱动程序位于 ``arch/<architecture>/src/<hardware>`` 目录，针对特定处理器 ``<architecture>`` 和特定 ``<chip>`` 模拟外设设备。

.. toctree::
  :caption: 支持的驱动程序
  :maxdepth: 1

  adc/index.rst
  dac/index.rst
