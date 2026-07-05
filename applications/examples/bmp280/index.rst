==========================================
``bmp280`` BMP280 气压传感器示例
==========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此示例用于测试 BMP280 气压传感器。它通过从设备读取单次测量结果（假设注册在 ``/dev/uorb/sensor_baro0``）并将结果打印到屏幕来工作。程序不带任何命令行参数运行。

以下是控制台输出示例：

.. code-block:: console

   nsh> bmp280
   Absolute pressure [hPa] = 983.099976
   Temperature [C] = 24.129999
