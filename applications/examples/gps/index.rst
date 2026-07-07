===================
\`\`gps\`\` GPS 示例
===================

本示例可用于在 NuttX 中与 GPS 设备进行交互。它使用
`MINMEA <https://github.com/kosma/minmea>`_ 库来解析标准 NMEA
消息，并将 GPS 数据打印到控制台。

使用该程序时，将 GPS 串口连接的字符设备路径作为唯一参数传入。如果未提供路径，程序将默认使用 ``/dev/ttyS1``。

如果你希望看到本程序的浮点输出，请确保启用 ``CONFIG_LIBC_FLOATINGPOINT``。

程序会持续循环解析串口设备中的 NMEA 数据。

等待 GPS 定位
-------------------

.. code:: console

   nsh> gps /dev/ttyS3
   Fixed-point Latitude...........: 0
   Fixed-point Longitude..........: 0
   Fixed-point Speed..............: 0
   Floating point degree latitude.: nan
   Floating point degree longitude: nan
   Floating point speed...........: nan
   Fix quality....................: 0
   Altitude.......................: 0
   Tracked satellites.............: 0

在等待获取定位期间，输出将显示 ``nan`` 和 ``0``，获取到定位后将开始显示真实值。

获取到 GPS 定位后
------------

.. code:: console

   nsh> gps /dev/ttyS3
   Altitude.......................: 73172                                         
   Tracked satellites.............: 5                                             
   Fixed-point Latitude...........: 4628356                                       
   Fixed-point Longitude..........: -8058408                                      
   Fixed-point Speed..............: 110                                           
   Floating point degree latitude.: 46.476547                                     
   Floating point degree longitude: -80.977995                                    
   Floating point speed...........: 0.001833                                      
   Fix quality....................: 1                

现在可以看到 GPS 数据已填充到信息中。

.. note::

   定点读数可能与浮点读数具有不同的比例。例如，上面的高度是定点表示，但实际上是浮点的 73.172 米。
