.. _adc-example:

=====================
``adc`` 从 ADC 读取
=====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

一个非常简单的 ADC 设备测试。它只是从 ADC 设备读取数据，并将数据不断输出到控制台。

此测试依赖于以下特定的 ADC/NSH 配置设置（您特定的 ADC 设置可能需要额外的配置）。

- ``CONFIG_ADC`` – 启用 ADC 支持。
- ``CONFIG_NSH_BUILTIN_APPS`` – 将 ADC 测试构建为 NSH 内置函数。
  默认：构建为独立程序。

此示例的特定配置选项包括：

- ``CONFIG_EXAMPLES_ADC_DEVPATH`` – ADC 设备的默认路径。默认：
  ``/dev/adc0``。
- ``CONFIG_EXAMPLES_ADC_NSAMPLES`` – 采集此数量的样本后程序终止。
  默认：无限期采集样本。
- ``CONFIG_EXAMPLES_ADC_GROUPSIZE`` – 一次读取的样本数量。
  默认：``4``。
