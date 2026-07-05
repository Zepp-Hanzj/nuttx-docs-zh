=========
LSM6DSO32
=========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

LSM6DSO32 是 STMicroelectronics 生产的高性能 IMU，具有 3 轴陀螺仪
和 3 轴加速度计。它具有 I2C 和 SPI 接口，但此驱动程序仅支持 I2C。

此驱动程序使用 :doc:`uorb
</components/drivers/special/sensors/sensors_uorb>` 接口。它支持
加速度计和陀螺仪的自检功能。

.. warning::
   LSM6DSO32 是功能丰富的传感器，此驱动程序未实现其许多功能，
   如点击检测、唤醒、作为其他传感器的主设备等。

应用编程接口
=================================

.. code-block:: c

   #include <nuttx/sensors/lsm6dso32.h>

LSM6DSO32 注册函数允许将驱动程序注册为 uORB 驱动程序。注册此驱动
程序将导致在 ``/dev/uorb/`` 下注册两个 uORB 主题：``sensor_accel<n>``
和 ``sensor_gyro<n>``，其中 ``n`` 是 ``devno`` 的值。

驱动程序可以以轮询模式或中断驱动模式注册。轮询模式将创建一个内核
线程，根据设置的间隔定期轮询传感器。轮询模式通过将 ``config`` 参数
中的 ``attach`` 函数留为 ``NULL`` 来注册。

.. warning::
   要使用中断驱动模式，必须启用 ``CONFIG_SCHED_HPWORK``。

以下代码段显示了如何以轮询模式注册驱动程序。在此模式下，可以安全
忽略 ``gy_int`` 和 ``xl_int`` 的值。

.. code-block:: c

   /* RP2040 MCU 的示例 */

    struct lsm6dso32_config_s lsm6dso32_config = {
      .gy_int = 0,
      .xl_int = 0,
      .gy_attach = NULL,
      .xl_attach = NULL,
    };

    ret = lsm6dso32_register(rp2040_i2cbus_initialize(0), 0x6b, 0,
                             &lsm6dso32_config);
    if (ret < 0)
      {
        syslog(LOG_ERR, "Couldn't register LSM6DSO32 at 0x6b: %d\n", ret);
      }

以下代码段显示了如何以中断驱动模式注册驱动程序。在这里，您必须
指定哪个中断引脚是陀螺仪中断处理程序的 DRDY 信号，哪个中断引脚
是加速度计中断处理程序的 DRDY 信号。

.. code-block:: c

   /* RP2040 MCU 的示例 */

   /* 此函数注册陀螺仪中断处理程序并立即启用它 */

   static int board_lsm6dso32_gy_attach(xcpt_t handler, FAR void *arg)
   {
     int err;
     err = rp2040_gpio_irq_attach(GPIO_GYRO_INT, RP2040_GPIO_INTR_EDGE_HIGH,
                                  handler, arg);
     if (err < 0)
       {
         return err;
       }

     rp2040_gpio_enable_irq(GPIO_GYRO_INT);
     return err;
   }

   /* 此函数注册加速度计中断处理程序并立即启用它 */

   static int board_lsm6dso32_xl_attach(xcpt_t handler, FAR void *arg)
   {
     int err;
     err = rp2040_gpio_irq_attach(GPIO_XL_INT, RP2040_GPIO_INTR_EDGE_HIGH,
                                  handler, arg);
     if (err < 0)
       {
         return err;
       }

     rp2040_gpio_enable_irq(GPIO_XL_INT);
     return err;
   }

   /* 驱动程序注册 */

   struct lsm6dso32_config_s lsm6dso32_config = {
    .gy_int = LSM6DSO32_INT1, /* 陀螺仪使用 INT1 引脚 */
    .xl_int = LSM6DSO32_INT2, /* 加速度计使用 INT2 引脚 */
    .gy_attach = board_lsm6dso32_gy_attach;
    .xl_attach = board_lsm6dso32_xl_attach;
   };

   ret = lsm6dso32_register(rp2040_i2cbus_initialize(0), 0x6b, 0,
                            &lsm6dso32_config);
   if (ret < 0)
     {
       syslog(LOG_ERR, "Couldn't register LSM6DSO32 at 0x6b: %d\n", ret);
     }

要调试此设备，您可以在构建中包含 ``uorb_listener`` 应用程序并启用
调试。运行它将显示传感器测量值。

此设备驱动程序的自检功能基于 STMicroelectronics 的 AN5473 信息，
为加速度计和陀螺仪提供自检。因此它只执行正向自检。被测传感器取决
于自检调用的主题：陀螺仪或加速度计。两个传感器的自检都不接受参数。

.. warning::
   自检功能必须在传感器静止时执行。

.. code-block:: c

   err = orb_ioctl(gyro, SNIOC_SELFTEST, 0);
   if (err < 0)
     {
       fprintf(stderr, "Gyroscope self-test failed: %d\n", errno);
     }

此设备的 ``SNIOC_SET_CALIBVALUE`` 命令也根据调用的传感器主题而
有所不同。

对于加速度计，参数是一个包含 3 个浮点数的数组，表示要从测量值中
减去的 X、Y 和 Z 偏移量（以米每秒平方为单位），按此顺序。

对于陀螺仪，参数是一个包含 3 个浮点数的数组，表示要从测量值中
减去的 X、Y 和 Z 偏移量（以弧度每秒为单位），按此顺序。

.. code-block:: c

   /* 加速度计偏移示例 */

   float offsets[3] = {0.0f, 0.0f, 9.81f};
   err = orb_ioctl(accel, SNIOC_SET_CALIBVALUE, (unsigned long)(offsets));

设置测量间隔的接口对陀螺仪和加速度计单独操作。也就是说，它们可以
有不同的采样率。

.. warning::
   此驱动程序不实现加速度计在 1.6Hz 的低功耗模式采样，仅支持
   12.5Hz 及以上。

加速度计和陀螺仪数据中包含的温度测量值来自同一板载温度传感器。此
温度传感器的输出数据速率始终为 52Hz。仅当加速度计处于低功耗或
超低功耗模式时才会改变，此时温度 ODR 与加速度计匹配。但是，此驱动
程序目前不实现这些电源模式。

.. code-block:: c

   unsigned freq = 50;
   err = orb_set_frequency(accel, freq);
   if (err)
     {
       fprintf(stderr, "Wasn't able to set frequency to %uHz: %d\n", freq, err);
       return EXIT_FAILURE;
     }

此传感器还有用于访问额外功能的附加命令。

``SNIOC_WHO_AM_I``
------------------

此命令读取 LSM6DSO32 的 ``WHOAMI`` 寄存器。应始终返回 `0x6c`。
参数是指向 8 位无符号整数的指针。此命令在加速度计或陀螺仪主题上
调用时结果相同。

.. code-block:: c

   uint8_t id;
   err = orb_ioctl(accel, SNIOC_WHO_AM_I, (unsigned long)&id);

``SNIOC_SETFULLSCALE``
----------------------

此命令允许用户设置加速度计或陀螺仪的满量程范围。

在加速度计上调用时，参数应为以 'g' 为单位的所需 FSR。可用选项为
4、8、16 和 32g。

在陀螺仪上调用时，参数应为以度每秒为单位的所需 FSR。可用选项为
125、250、500、1000 和 2000 dps。

请注意，默认情况下，加速度计的满量程范围为 +/-4g，陀螺仪的满量程
范围为 +/-125dps。

.. code-block:: c

   err = orb_ioctl(accel, SNIOC_SETFULLSCALE, 16);
   err = orb_ioctl(gyro, SNIOC_SETFULLSCALE, 150);

要检查 FSR，您可以获取传感器信息并检查 ``max_range`` 字段。此值
对于加速度计以 m/s^2 为单位，对于陀螺仪以 rad/s 为单位，因此必须
转换为 g 或度每秒的单位才能直接与设置值进行比较。

.. code-block:: c

   struct sensor_device_info_s info;
   err = orb_ioctl(accel, SNIOC_GET_INFO, (unsigned long)&info);
   if (err < 0)
     {
       fprintf(stderr, "Could not get sensor information: %d", errno);
       return EXIT_FAILURE;
     }

   printf("Sensor: %s\n", info.name);
   printf("Manufacturer: %s\n", info.vendor);
   printf("Max range: %.2f m/s^2\n", info.max_range);
