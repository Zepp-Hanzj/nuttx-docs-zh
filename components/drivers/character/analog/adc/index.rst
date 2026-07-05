===========
ADC 驱动
===========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

-  ``include/nuttx/analog/adc.h``。此头文件提供了使用 ADC 驱动程序所需的所有结构体和 API。此头文件包括：

   #. 开发底层、特定于架构的 ADC 驱动程序所需的结构体和接口描述。
   #. 将 ADC 驱动程序注册到通用 ADC 字符驱动程序。
   #. 用户程序与通用 ADC 字符驱动程序交互所需的接口。

-  ``drivers/analog/adc.c``。通用 ADC 字符驱动程序的实现。

应用程序编程接口
=================================

要从应用程序使用 ADC 驱动程序，首先需要包含正确的头文件。它包含了 ADC 驱动程序的应用程序编程接口。为此，请包含：

.. code-block:: c

  #include <nuttx/analog/adc.h>

ADC 驱动程序作为 POSIX 字符设备文件注册到 ``/dev`` 命名空间。需要打开设备以获取文件描述符进行后续操作。这可以通过标准 POSIX ``open()`` 调用完成。

标准 POSIX ``read()`` 操作可用于从控制器读取测量数据。驱动程序对接收到的测量数据使用 FIFO 队列，``read()`` 操作从此队列获取数据。结构 ``adc_msg_s``（或这些结构的数组）应传递给 ``read()`` 调用的缓冲区参数。此结构表示一次 ADC 测量。

.. c:struct:: adc_msg_s
.. code-block:: c

  begin_packed_struct struct adc_msg_s
  {
    /* 8 位 ADC 通道 */
    uint8_t      am_channel;
    /* ADC 转换结果（4 字节） */
    int32_t      am_data;
  } end_packed_struct;

用户可以使用 ``poll()`` 调用对驱动程序执行轮询操作。控制器也可以在运行时通过众多 ``ioctl()`` 调用进行配置/控制。支持以下命令：

 * :c:macro:`ANIOC_TRIGGER`
 * :c:macro:`ANIOC_WDOG_UPPER`
 * :c:macro:`ANIOC_WDOG_LOWER`
 * :c:macro:`ANIOC_GET_NCHANNELS`
 * :c:macro:`ANIOC_RESET_FIFO`
 * :c:macro:`ANIOC_SAMPLES_ON_READ`

.. c:macro:: ANIOC_TRIGGER

``ANIOC_TRIGGER`` 命令触发一次转换。此调用在配置了软件触发转换时使用。与软件触发相对的是硬件触发，例如某个定时器驱动程序。

.. c:macro:: ANIOC_WDOG_UPPER

此命令用于设置看门狗的上限阈值。

.. c:macro:: ANIOC_WDOG_LOWER

此命令用于设置看门狗的下限阈值。

.. c:macro:: ANIOC_GET_NCHANNELS

``ANIOC_GET_NCHANNELS`` 获取给定已打开实例使用的/配置的通道数。这是从驱动程序获取通道数的唯一可移植方式。

.. c:macro:: ANIOC_RESET_FIFO

此 ``ioctl`` 命令清除存储测量数据的 FIFO 队列。

.. c:macro:: ANIOC_SAMPLES_ON_READ

``ANIOC_SAMPLES_ON_READ`` 返回等待在 FIFO 队列中被读取的采样/测量数据数量。

控制器可以支持其特定的 ioctl 命令。这些应在控制器特定文档中描述。

应用程序示例
~~~~~~~~~~~~~~~~~~~

示例应用程序可以在 ``nuttx-apps`` 仓库的 ``examples/adc`` 路径下找到。这是一个从定义数量的通道读取数据的示例应用程序。

.. code-block :: bash

   nsh> adc
   Sample:
   1: channel: 0 value 951
   2: channel: 1 value 1879
   Sample:
   1: channel: 0 value 952
   2: channel: 1 value 1880
   Sample:
   1: channel: 0 value 942
   2: channel: 1 value 1800

配置
=============

本节描述 ``Kconfig`` 中的 ADC 驱动程序配置。读者应参考目标文档了解目标特定配置。

ADC 外设分别由 ``CONFIG_ANALOG`` 和 ``CONFIG_ADC`` 选项启用。用户可以使用配置选项 ``CONFIG_ADC_FIFOSIZE`` 配置 FIFO 队列大小。此变量定义 ADC 环形缓冲区的大小，用于在应用程序通过从 ADC 字符设备读取来检索数据之前排队接收到的 ADC 数据。由于这是一个环形缓冲区，缓冲区中可以保留的实际字节数为（``CONFIG_ADC_FIFOSIZE - 1``）。

配置选项 ``CONFIG_ADC_NPOLLWAITERS`` 定义可以在轮询上等待的线程数量。

外部设备
================

NuttX 还提供对各种外部 ADC 设备的支持。这些设备通常通过 I2C 或 SPI 外设与 MCU 通信。

.. toctree::
  :maxdepth: 1
  :glob:

  */*
