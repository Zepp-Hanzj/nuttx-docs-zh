==========================
正交编码器驱动程序
==========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

正交编码器（QE）是一种通常用于读取电机或其他旋转设备角位移的传感器。

NuttX 支持某些微控制器中存在的内部 QE 外设，如 ESP32、iMXRT、STM32、nRF5x、TIVA 等，同时也支持磁旋转编码器，如 AS5048、MT6816 等。

内部外设正交编码器
======================================

NuttX 支持一个低级的两部分正交编码器驱动程序。

#. "上半部分"，通用驱动程序，为应用程序代码提供通用的正交编码器接口，
#. "下半部分"，平台特定的驱动程序，实现底层定时器控制以实现正交编码器功能。

支持正交编码器的文件可以在以下位置找到：

-  **接口定义**。NuttX 正交编码器驱动程序的头文件位于 ``include/nuttx/sensors/qencoder.h``。此头文件包含正交编码器驱动程序的应用程序级别接口以及"上半部分"和"下半部分"驱动程序之间的接口。正交编码器模块使用标准字符驱动程序框架。
-  **"上半部分"驱动程序**。通用的"上半部分"正交编码器驱动程序位于 ``drivers/sensors/qencoder.c``。
-  **"下半部分"驱动程序**。平台特定的正交编码器驱动程序位于 ``arch/<architecture>/src/<hardware>`` 目录，针对特定处理器 ``<architecture>`` 和特定 ``<chip>`` 正交编码器外设设备。

磁旋转编码器
=======================

虽然从技术上讲磁旋转编码器不是正交编码器，但通常使用 QE 下半部分驱动程序来导出与正交编码器兼容的设备。这样，使用普通 QE 编码器的应用程序可以无需任何修改即可使用磁旋转编码器，只需在其板上启用和初始化磁旋转编码器即可。

以下是基于 STM32 的板如何初始化 MT6816 磁旋转编码器：

.. code-block:: c

   /* 初始化连接到 MT6816 的 SPI 总线 */

   spi = stm32_spibus_initialize(spi_busno);
   if (spi == NULL)
     {
       return -ENODEV;
     }

   /* 使用 `spi` 和从 0 开始的 `device number` 初始化 MT6816 */

   dev = mt6816_initialize(spi, (uint16_t) devno);
   if (dev == NULL)
     {
       return -ENODEV;
     }

   /* 使用返回的 qe 下半部分注册 /dev/qe# (# => devno) */

   ret = qe_register(qe_path, dev);
   if (ret < 0)
     {
       snerr("ERROR: Failed to register MT6816 qe%d driver: %d\n",
             devno, ret);
       ret = -ENODEV;
     }

应用程序编程接口
=================================

要在应用程序中使用正交编码器驱动程序，首先需要包含正确的头文件。它包含驱动程序的应用程序编程接口。为此，包含

.. code-block:: c

  #include <nuttx/sensors/qencoder.h>

正交编码器驱动程序注册为 ``/dev`` 命名空间中的 POSIX 字符设备文件。需要打开设备以获取文件描述符以进行后续操作。这可以通过标准的 POSIX ``open()`` 调用完成。

驱动程序仅通过 ``ioctl`` 接口访问，``read`` 和 ``write`` 函数没有任何效果。以下 ``ioctl`` 命令可用：

 * :c:macro:`QEIOC_POSITION`
 * :c:macro:`QEIOC_RESET`
 * :c:macro:`QEIOC_SETPOSMAX`
 * :c:macro:`QEIOC_SETINDEX`
 * :c:macro:`QEIOC_GETINDEX`

.. c:macro:: QEIOC_POSITION

此调用从编码器驱动程序获取当前位置。调用的参数是指向 ``int32_t`` 变量的指针。

.. c:macro:: QEIOC_RESET

此命令将当前编码器位置重置为零。

.. c:macro:: QEIOC_SETPOSMAX

``QEIOC_SETPOSMAX`` 调用设置编码器的最大位置。参数是一个 ``uint32_t`` 变量，包含最大位置值。

.. c:macro:: QEIOC_SETINDEX

此 ioctl 设置编码器的索引位置。参数是一个 ``uint32_t`` 变量，包含最大位置值。

.. c:macro:: QEIOC_GETINDEX

此 ioctl 获取编码器的索引位置。参数是指向 ``qe_index_s`` 结构体的指针。

.. c:struct:: qe_index_s
.. code-block:: c

   struct qe_index_s
   {
      /* 编码器实际位置 */
      int32_t qenc_pos;
      /* 索引上次位置 */
      int32_t indx_pos;
      /* 索引出现次数 */
      int16_t indx_cnt
   };

指向此结构体的指针用作 ``QEIOC_GETINDEX`` ioctl 命令的参数。它获取当前编码器位置、索引的最后位置和索引出现次数。

应用示例
~~~~~~~~~~~~~~~~~~~

示例应用程序可以在 ``nuttx-apps`` 仓库的 ``examples/qencoder`` 路径下找到。它演示了从编码器设备读取基本数据。

.. code-block:: console

    nsh> qe
    1.  0
    2.  0
    3.  0
    4.  1
    5.  1
    6.  1
    7.  2
    8.  2
    9.  3

配置
=============

本节描述 ``Kconfig`` 中的 qencoder 驱动程序配置。读者应参考目标文档以获取目标特定配置。

需要启用 ``CONFIG_SENSORS`` 选项才能使用 qencoder 外设。外设本身由 ``CONFIG_SENSORS_QENCODER`` 选项启用。
