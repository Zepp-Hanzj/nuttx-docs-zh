=====================
Sensor Legacy Drivers
=====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

旧的传感器实现，其中字符设备接口未以任何方式标准化。

不建议新驱动程序使用此方法，因为没有标准化接口，创建可移植的应用
程序是不可能的。

已实现的驱动程序
===================

在新传感器框架中也可用的驱动程序标记为 ``[*]``。

- :doc:`adt7320`
- adxl345
- :doc:`aht10`
- :doc:`ak09912`
- amg88xx
- apds9922
- apds9960
- as5048a
- as5048b
- as726x
- bh1749nuc [*]
- bh1750fvi
- bmg160
- bmi088 [*]
- bmi160 [*]
- bmi270 [*]
- bmp180 [*]
- dhtxx
- fxos8700cq
- hall3ph
- hc_sr04
- hdc1008
- hts221
- ina219
- ina226
- ina3221
- isl29023
- kxtj9
- lis2dh
- lis331dl
- lis3dh
- lis3dsh
- lis3mdl
- lm75
- lm92
- lps25h
- lsm303agr
- lsm6dsl
- lsm9ds1
- ltc4151
- max31855
- max31865
- max44009
- max6675
- mb7040
- :doc:`mcp9600`
- mcp9844
- mlx90393
- mlx90614
- :doc:`mpl115a`
- mpu60x0
- ms58xx
- msa301
- qencoder
- scd30
- scd41
- sgp30
- sht21
- sht3x
- sps30
- t67xx
- veml6070
- vl53l1x
- xen1210
- zerocross
