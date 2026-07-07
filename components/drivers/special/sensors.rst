==============
传感器驱动
==============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

目前在 NuttX 中，我们有 3 种不同的传感器接口方法：

.. toctree::
    :maxdepth: 1

    sensors/sensors_uorb
    sensors/sensors_legacy
    sensors/sensors_cluster
    sensors/sensor_monitor

实现新传感器的首选方式是 :ref:`新传感器框架 <new_sensor_framework>`，它提供了最通用的接口。

:doc:`传感器监控器 <sensors/sensor_monitor>` 提供了一个动态调试工具，用于在运行时监控传感器活动。

.. attach files to avoid warnings, but don't show them here !

.. toctree::
    :hidden:

    sensors/adt7320
    sensors/adxl345
    sensors/adxl362
    sensors/adxl372
    sensors/aht10
    sensors/ak09912
    sensors/lsm330
    sensors/mcp9600
    sensors/mpl115a
    sensors/nau7802
    sensors/qmi8658
    sensors/sht4x
    sensors/lsm6dso32
    sensors/lis2mdl
    sensors/l86xxx
    sensors/gnss_lowerhalf
