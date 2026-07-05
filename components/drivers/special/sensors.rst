==============
传感器驱动
==============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

目前在 NuttX 中，我们有 3 种不同的传感器接口方法：

.. toctree::
    :maxdepth: 1

    sensors/sensors_uorb.rst
    sensors/sensors_legacy.rst
    sensors/sensors_cluster.rst
    sensors/sensor_monitor.rst

实现新传感器的首选方式是 :ref:`新传感器框架 <new_sensor_framework>`，它提供了最通用的接口。

:doc:`传感器监控器 <sensors/sensor_monitor>` 提供了一个动态调试工具，用于在运行时监控传感器活动。

.. attach files to avoid warnings, but don't show them here !

.. toctree::
    :hidden:

    sensors/adt7320.rst
    sensors/adxl345.rst
    sensors/adxl362.rst
    sensors/adxl372.rst
    sensors/aht10.rst
    sensors/ak09912.rst
    sensors/lsm330.rst
    sensors/mcp9600.rst
    sensors/mpl115a.rst
    sensors/nau7802.rst
    sensors/qmi8658.rst
    sensors/sht4x.rst
    sensors/lsm6dso32.rst
    sensors/lis2mdl.rst
    sensors/l86xxx.rst
    sensors/gnss_lowerhalf.rst
