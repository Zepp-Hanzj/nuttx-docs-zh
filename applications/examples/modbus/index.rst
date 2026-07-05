==================================
``modbus`` FreeModbus 演示示例
==================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 FreeModbus Linux 演示的移植版本。它源自 FreeModBus 版本 ``1.5.0``
（2010 年 6 月 6 日）的 demos/LINUX 目录，完整内容可从以下地址下载：
http://developer.berlios.de/project/showfiles.php?group_id=6120。

- ``CONFIG_EXAMPLES_MODBUS_PORT``，默认 ``0``（对应 ``/dev/ttyS0``）。
- ``CONFIG_EXAMPLES_MODBUS_BAUD``，默认 ``38400``。
- ``CONFIG_EXAMPLES_MODBUS_PARITY``，默认 ``MB_PAR_EVEN``。
- ``CONFIG_EXAMPLES_MODBUS_REG_INPUT_START``，默认 ``1000``。
- ``CONFIG_EXAMPLES_MODBUS_REG_INPUT_NREGS``，默认 ``4``。
- ``CONFIG_EXAMPLES_MODBUS_REG_HOLDING_START``，默认 ``2000``。
- ``CONFIG_EXAMPLES_MODBUS_REG_HOLDING_NREGS``，默认 ``130``。

FreeModBus 库位于 ``apps/modbus``。
有关其他配置信息，请参见 :doc:`/applications/industry/modbus/index`。
