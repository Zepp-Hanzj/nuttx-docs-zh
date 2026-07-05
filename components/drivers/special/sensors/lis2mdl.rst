=======
LIS2MDL
=======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

由 Matteo Golin 贡献。

LIS2MDL 是 ST Microelectronics 生产的低功耗、高性能 3 轴磁力计。
它具有 I2C 和 SPI 接口，但此驱动程序目前仅支持 I2C。

驱动程序使用 :doc:`uorb
</components/drivers/special/sensors/sensors_uorb>` 接口。它支持
自检功能。

应用编程接口
=================================

.. code-block:: c

   #include <nuttx/sensors/lis2mdl.h>

LIS2MDL 注册函数允许将驱动程序注册为 UORB 驱动程序。注册此驱动
程序将导致 ``/dev/uorb/sensor_mag<n>`` 主题出现，其中 ``n`` 是
``devno`` 的值。

驱动程序可以以轮询模式或中断驱动模式注册。轮询模式将创建一个内核
线程，根据设置的间隔定期轮询传感器。轮询模式通过将 ``attach`` 参数
设置为 ``NULL`` 而不是实际的函数指针来注册，如下所示：

.. code-block:: c

   int err;

   /* 以轮询模式创建 /dev/uorb/mag0 */

   err = lis2mdl_register(i2c_master, 0, 0x1e, NULL);
   if (err < 0)
   {
     syslog(LOG_ERR, "Could not register LIS2MDL driver at 0x1E: %d\n", err);
   }

要以中断驱动模式注册，调用代码必须提供一个函数来正确注册 LIS2MDL
中断处理程序。此函数应接受中断处理程序和 ``arg`` 引用作为参数，
成功时返回 0，失败时返回负的错误代码。此函数还必须在成功注册后
启用中断。

.. warning::
   要使用中断驱动模式，必须启用 ``CONFIG_SCHED_HPWORK``。

以下示例显示了基于 RP2040 的板卡的示例流程，但在其他架构上类似：

.. code-block:: c

   /* RP2040 板卡的 IRQ 附加函数示例 */

   static int board_lis2mdl_attach(xcpt_t handler, FAR void *arg)
   {
     int err;
     err = rp2040_gpio_irq_attach(GPIO_MAG_INT, RP2040_GPIO_INTR_EDGE_HIGH,
                                  handler, arg);
     if (err < 0)
       {
         return err;
       }

     rp2040_gpio_enable_irq(GPIO_MAG_INT);
     return err;
   }

   /* 稍后，在板卡启动代码中 ... */

   int err;
   err = lis2mdl_register(i2c_master, 0, 0x1e, board_lis2mdl_attach);
   if (err < 0)
   {
     syslog(LOG_ERR, "Couldn't register LIS2MDL driver: %d\n", err);
   }

要调试此设备，您可以在构建中包含 ``uorb_listener`` 并启用调试。
运行它将显示传感器测量值。

.. warning::
   默认情况下，当通过 UORB 接口停用传感器时，它会进入低功耗模式
   并设置为空闲。当重新激活时，它会进入高分辨率模式并设置为连续
   测量。如果您想在低功耗模式下连续测量，需要使用下面说明的
   ``SNIOC_SET_POWER_MODE`` 命令。

此传感器的 ``set_calibvalue`` 接口接受三个 `float` 类型的数组，
表示以微特斯拉为单位的硬铁偏移。此偏移设置在传感器上，并从测量值
中减去以补偿环境影响。

LIS2MDL 的一些附加控制命令如下所列。

``SNIOC_WHO_AM_I``
------------------

此命令读取 LIS2MDL 的 ``WHOAMI`` 寄存器。应始终返回 ``0x40``。
参数是指向 8 位无符号整数的指针。

.. code-block:: c

   uint8_t id; /* 应始终包含 0x40 */
   err = orb_ioctl(sensor, SNIOC_WHO_AM_I, &id);

``SNIOC_SET_POWER_MODE``
------------------------

此命令选择 LIS2MDL 传感器的电源模式。参数为 ``true`` 时将传感器
置于低功耗模式，``false`` 时将传感器置于高分辨率模式。

.. code-block:: c

   /* 将 LIS2MDL 置于低功耗模式 */
   err = orb_ioctl(sensor, SNIOC_WHO_AM_I, true);

``SNIOC_RESET``
----------------

执行 LIS2MDL 的软复位，重置用户寄存器。此命令不接受参数。
发出此命令后，必须经过 5 微秒传感器才能再次运行。

.. code-block:: c

   err = orb_ioctl(sensor, SNIOC_RESET, NULL);

``SNIOC_SENSOR_OFF``
--------------------

执行 LIS2MDL 内存内容的重启。此命令不接受参数。发出命令后，
必须经过 20ms 传感器才能再次运行。

.. code-block:: c

   err = orb_ioctl(sensor, SNIOC_SENSOR_OFF, NULL);

``SNIOC_SET_TEMP_OFFSET``
--------------------------

启用或禁用磁力计的温度补偿。参数为 ``true`` 时启用补偿，
``false`` 时禁用。默认情况下启用。

.. code-block:: c

   err = orb_ioctl(sensor, SNIOC_SET_TEMP_OFFSET, true);

``SNIOC_LPF``
-------------

启用或禁用磁力计低通滤波器。参数为 ``true`` 时启用滤波器，
``false`` 时禁用。默认情况下禁用。

.. code-block:: c

   err = orb_ioctl(sensor, SNIOC_LPF, true);
