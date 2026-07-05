=====
SHT4X
=====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

由 Matteo Golin 贡献。

SHT4x 是 Sensirion 创建的温度和湿度传感器系列，通过 I2C 操作。
它们包含一个小型加热元件。

提供的驱动程序允许通过 I2C 与传感器进行接口。它已针对 SHT41 进行
了测试。此驱动程序使用 :doc:`uorb
</components/drivers/special/sensors/sensors_uorb>` 接口。

应用编程接口
=================================

SHT4X 驱动程序接口的头文件可以使用以下方式包含：

.. code-block:: c

   #include <nuttx/sensors/sht4x.h>

SHT4x 注册函数允许将驱动程序注册为 UORB 驱动程序。

SHT4x 测量环境温度和湿度，因此注册此驱动程序将导致两个新的 UORB
主题出现：``sensor_humi<n>`` 和 ``sensor_temp<n>``。

.. code-block:: c

   int err;
   err = sht4x_register(i2c_master, 0, 0x44);
   if (err < 0)
   {
     syslog(LOG_ERR, "Couldn't register SHT4X driver at 0x44: %d\n", err);
   }

要调试此设备，您可以在构建中包含 ``uorb_listener`` 并启用调试。
运行它将显示传感器测量值。

此传感器还提供一些附加控制命令，用于使用板载加热器和检查序列号。
这些控制命令可以在任一主题（湿度或温度）上使用，因为它们控制整个
设备。

``SNIOC_RESET``
----------------

这将执行 SHT4X 的软复位命令。

.. code-block:: c

  err = orb_ioctl(sensor, SNIOC_RESET);
  if (err) {
    fprintf(stderr, "SNIOC_RESET: %s\n", strerror(errno));
  } else {
    puts("RESET success!");
  }

``SNIOC_WHO_AM_I``
------------------

此命令读取 SHT4X 传感器的序列号。序列号在命令的参数中返回，
参数必须是 `uint32_t` 指针。

.. code-block:: c

  uint32_t serialno = 0;
  err = orb_ioctl(sensor, SNIOC_WHO_AM_I, &serialno);

``SNIOC_HEAT``
--------------

此命令将指示 SHT4X 在指定时间打开其加热器单元。

此命令的参数必须是 `enum sht4x_heater_e` 类型，它将指示加热器
开启的持续时间和使用的功率。

加热命令不允许每秒超过一次，以避免损坏传感器。如果在此一秒冷却
期结束前发出命令，将返回 `EAGAIN`。

.. code-block:: c

  err = orb_ioctl(sensor, SNIOC_HEAT, SHT4X_HEATER_200MW_1);

``SNIOC_CONFIGURE``
-------------------

此命令允许调用者配置后续测量命令使用的 SHT4X 传感器精度。
默认情况下，传感器以高精度启动。

此命令的参数是 `enum sht4x_precision_e` 中的值之一。

.. code-block:: c

  err = orb_ioctl(sensor, SNIOC_CONFIGURE, SHT4X_PREC_LOW);
