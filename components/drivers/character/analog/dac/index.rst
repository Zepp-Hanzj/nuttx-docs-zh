===========
DAC 驱动
===========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

-  ``include/nuttx/analog/dac.h``。此头文件提供了使用 DAC 驱动程序所需的所有结构体和 API。此头文件包括：

   #. 开发底层、特定于架构的 DAC 驱动程序所需的结构体和接口描述。
   #. 将 DAC 驱动程序注册到通用 DAC 字符驱动程序。
   #. 用户程序与通用 DAC 字符驱动程序交互所需的接口。

-  ``drivers/analog/dac.c``。通用 DAC 字符驱动程序的实现。

应用程序编程接口
=================================

要从应用程序使用 DAC 驱动程序，首先需要包含正确的头文件。它包含了 PWM 驱动程序的应用程序编程接口。为此，请包含

.. code-block:: c

  #include <nuttx/analog/dac.h>

DAC 驱动程序作为 POSIX 字符设备驱动程序注册到 ``/dev`` 命名空间。需要打开设备以获取文件描述符进行后续操作。这可以通过标准 POSIX ``open()`` 调用完成。

标准 POSIX ``write()`` 调用用于从应用程序向控制器发送数据。结构 ``dac_msg_s`` 用于传递数据/采样值。

.. c:struct:: dac_msg_s
.. code-block:: c

  begin_packed_struct struct dac_msg_s
  {
    /* 8 位 DAC 通道 */
    uint8_t      am_channel;
    /* DAC 转换结果（4 字节） */
    int32_t      am_data;
  } end_packed_struct;

应用程序示例
~~~~~~~~~~~~~~~~~~~

示例应用程序可以在 ``nuttx-apps`` 仓库的 ``examples/dac`` 路径下找到。它提供了向 DAC 通道写入数据的命令行界面。

配置
=============

本节描述 ``Kconfig`` 中的 DAC 驱动程序配置。读者应参考目标文档了解目标特定配置。

外设分别由 ``CONFIG_ANALOG`` 和 ``CONFIG_DAC`` 选项启用。FIFO 队列大小可通过 ``CONFIG_DAC_FIFOSIZE`` 配置。此大小限制为 ``255`` 以适应 ``uint8_t``。

支持的外部 DAC（I2C/SPI）
=================================

NuttX 还提供对各种外部 DAC 设备的支持。这些设备通常通过 I2C 或 SPI 接口与 MCU 通信。

基于 I2C 的 DAC：

.. toctree::
  :maxdepth: 1

  dac7571/index.rst
  mcp47x6/index.rst

基于 SPI 的 DAC：

.. toctree::
  :maxdepth: 1

  dac7554/index.rst
  mcp48xx/index.rst
