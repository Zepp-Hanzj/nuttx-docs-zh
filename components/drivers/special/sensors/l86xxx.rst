=======
L86-XXX
=======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

.. tags:: experimental

此驱动程序通过 :doc:`uorb </components/drivers/special/sensors/sensors_uorb>`
接口为 Quectel 的 L86-XXX 系列 GNSS 模块提供支持。此驱动程序的功能
使用 Quectel L86-M33 进行了测试。

.. warning::
   此驱动程序仅包含对少量专有 'PMTK' 命令的初步支持。尚不支持整个
   命令套件。此驱动程序也不使用标准的 uORD GNSS 上半部分驱动程序，
   最终应进行修改以使其使用。将此驱动程序视为实验性的。

应用编程接口
=================================

要注册设备以供使用，您需要启用标准上半部分串行驱动程序
（``CONFIG_STANDARD_SERIAL``），因为 L86-XXX 驱动程序需要模块
连接到的 UART 接口的路径。您还需要确保 UART 接口的波特率设置为
9600，这是 L86-XXX 系列 GNSS 模块的默认波特率。

驱动程序支持更改 GNSS 模块的默认波特率和更新速率。因此，您还需要
启用串行 TERMIOS 支持（``CONFIG_SERIAL_TERMIOS``）。GNSS 模块的
波特率和更新速率可以分别使用 ``L86_XXX_BAUD`` 和 ``L86_XXX_FIX_INT``
选项配置。请注意，更快的更新速率需要更高的波特率来支持，L86-XXX
系列 GNSS 模块支持的波特率为：

* 4800
* 9600
* 14400
* 19200
* 38400
* 57600
* 115200

模块的波特率和更新速率在注册时更改。

.. code-block:: c

   #if defined(CONFIG_SENSORS_L86_XXX)
      #include <nuttx/sensors/l86xxx.h>

      /* 在 USART2 上注册 L86xxx 设备 */

      ret = l86xxx_register("/dev/ttyS2", 0);
      if (ret < 0) {
         syslog(LOG_ERR, "Failed to register L86-M33: %d\n", ret);
      }
   #endif

驱动程序注册后，它会启动一个线程，持续从指定的 UART 设备读取原始
输出，并根据 `NMEA
<https://en.wikipedia.org/wiki/NMEA_0183>`_ 标准使用 NuttX 中包含的
`minmea <https://github.com/kosma/minmea>`_ 库解析输出。驱动程序
填充 ``sensor_gnss`` 结构体，并在其序列中的所有 NMEA 消息读取完成后
将数据推送到适当的事件。


**uORB 命令**
-----------------

驱动程序实现 ``orb_activate``、``orb_set_interval`` 和 ``orb_ioctl``
操作以与设备交互。后者用于发送专有的 'PMTK' 命令，下面将详细记录。

**激活**

L86-XXX GNSS 模块可以处于 4 种模式：

* 全开模式
* 待机模式
* 备份模式
* 周期模式
* AlwaysLocateTM 模式

调用 ``orb_activate`` 并将 ``enable`` 设置为 false 将使模块进入
"待机模式"。在"待机模式"下，模块不会输出任何 NMEA 消息，但内部
核心和 I/O 电源域仍然处于活动状态。

可以通过调用 ``orb_activate`` 并将 ``enable`` 设置为 true 来重新
启用模块，这将热启动模块，或者通过发送任何 'PMTK' 命令。

**设置间隔**

L86-XXX GNSS 模块支持 1Hz 到 10Hz（100ms - 10000ms）的间隔速率。
使用 ``orb_set_interval`` 时，请注意增加模块的间隔可能还需要增加
波特率。有关如何执行此操作的示例可以在源代码中找到。

超出支持范围的任何间隔速率都将导致此函数调用失败。

**控制**

``orb_ioctl`` 接口允许向 L86-XXX GNSS 模块发送专有的 'PMTK' 命令。
它实际上是 Quectel 概述的命令框架的包装器。``orb_ioctl`` 调用的
返回值遵循以下模式：

* ``EINVAL`` - 无效数据包
* ``ENOSYS`` - 不支持的数据包类型
* ``EIO`` - 有效数据包，但操作失败
* ``0`` - 有效数据包，操作成功
* 其他 - 写入期间命令失败

支持的命令及其参数如下所列。

``SNIOC_HOT_START``
-------------------

用于"热启动"GNSS 模块。通常热启动意味着 GNSS 模块断电时间少于
3 小时（RTC 必须保持活动状态），并且其星历仍然有效。由于无需下载
星历，这是最快的启动方法。

.. code-block:: c

   orb_ioctl(sensor, SNIOC_HOT_START);

``SNIOC_WARM_START``
--------------------

用于"温启动"GNSS 模块。温启动意味着 GNSS 模块具有大致的时间、
位置和卫星位置的粗略数据信息，但需要下载星历才能获得定位。

.. code-block:: c

   orb_ioctl(sensor, SNIOC_WARM_START);

``SNIOC_COLD_START``
--------------------

用于"冷启动"GNSS 模块。使用此消息将强制 GNSS 模块在没有任何先前
位置信息（包括时间、位置、历书和星历数据）的情况下重新启动。

.. code-block:: c

   orb_ioctl(sensor, SNIOC_COLD_START);

``SNIOC_FULL_COLD_START``
-------------------------

用于"完全冷启动"GNSS 模块。这实际上与冷重启相同，但额外清除系统
和用户配置。换句话说，这将 GNSS 模块重置为出厂设置。完全冷启动时，
GNSS 模块没有其上次位置的信息。

.. code-block:: c

   orb_ioctl(sensor, SNIOC_FULL_COLD_START);

``SNIOC_SET_INTERVAL``
----------------------

用于修改 GNSS 模块的定位间隔。参数为 100 到 10000 之间的整数，
默认值为 1000。

.. code-block:: c

   orb_ioctl(sensor, SNIOC_SET_INTERVAL, 1000);

``SNIOC_SET_BAUD``
------------------
.. note::

   此功能需要启用 termios 支持（``CONFIG_SERIAL_TERMIOS``）

用于修改 GNSS 模块的波特率。参数为表示支持的波特率的整数，
默认值为 9600。发送此命令后，用于与模块通信的 UART 接口的波特率
也会被修改。L86-XXX 系列 GNSS 模块支持的波特率为：

* 4800
* 9600
* 14400
* 19200
* 38400
* 57600
* 115200

.. code-block:: c

   orb_ioctl(sensor, SNIOC_SET_BAUD, 9600);

``SNIOC_SET_OPERATIONAL_MODE``
------------------------------

用于设置 GNSS 模块的导航模式。参数为 ``L86XXX_OPERATIONAL_MODE``
枚举：

* NORMAL - 通用目的
* FITNESS - 低速移动（<5 m/s>）会影响计算的情况
* AVIATION - 高动态目的，大加速度移动对位置计算有更大影响
* BALLOON - 高空气球目的，垂直移动对位置计算有更大影响
* STANDBY - 用于进入待机模式以节省功耗

默认模式为 NORMAL

.. code-block:: c

   orb_ioctl(sensor, SNIOC_SET_OPERATIONAL_MODE, NORMAL);
