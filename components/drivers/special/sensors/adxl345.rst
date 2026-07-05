ADXL345
=======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

由 Alan Carvalho de Assis 贡献

ADXL345 加速度计可以在 I2C 或 SPI 模式下工作。要在 I2C 模式下
工作，只需将 CS 引脚连接到 Vddi/o。

要在 SPI 模式下工作，CS 需要连接到微控制器，不能悬空。

在 SPI 模式下，它使用时钟极性 (CPOL) = 1 和时钟相位 (CPHA) = 1。
