=======
MCP3008
=======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

由 Matteo Golin 贡献

MCP3008 是一款由 Microchip 生产的 10 位、8 通道 ADC，通过 SPI 总线通信。

可以选择在单端模式下运行，该模式单独测量每个通道的电压，或在差分模式下运行，该模式测量通道对之间的电压差。

在差分模式下运行时，以下通道号对应列出的差分对：

.. list-table:: 差分对通道号
   :widths: auto

   * - 通道号
     - 源
   * - 0
     - CH0+, CH1-
   * - 1
     - CH0-, CH1+
   * - 2
     - CH2+, CH3-
   * - 3
     - CH2-, CH3+
   * - 4
     - CH4+, CH5-
   * - 5
     - CH4-, CH5+
   * - 6
     - CH6+, CH7-
   * - 7
     - CH6-, CH7+

驱动程序接口
---------------------

要将 MCP3008 设备驱动程序注册为标准 NuttX 模拟设备，可以使用类似以下适用于 RP2040 的代码。

.. code-block:: c

  #include <nuttx/analog/mcp3008.h>
  #include <nuttx/analog/adc.h>

  /* 注册 MCP3008 ADC */

  struct spi_dev_s *spi = rp2040_spibus_initialize(0);
  if (spi == NULL)
    {
      syslog(LOG_ERR, "Failed to initialize SPI bus 0\n");
    }

  struct adc_dev_s *mcp3008 = mcp3008_initialize(spi);
  if (mcp3008 == NULL)
  {
    syslog(LOG_ERR, "Failed to initialize MCP3008\n");
  }

  int ret = adc_register("/dev/adc1", mcp3008);
  if (ret < 0)
  {
    syslog(LOG_ERR, "Failed to register MCP3008 device driver: %d\n", ret);
  }

注册后，此驱动程序可以使用 ADC 示例（:ref:`adc-example`）进行交互。请确保启用软件触发，因为 MCP3008 驱动程序不支持硬件触发（中断）。您还可以将每组采样数更改为最多 8 个，覆盖 ADC 的所有 8 个通道。

您可能需要将 `CONFIG_ADC_FIFOSIZE` 值增加到大于 8 的值，以便在测量触发后能够存储所有 ADC 测量值（例如 9）。

您可以使用 `CONFIG_ADC_MCP3008_DIFFERENTIAL` 配置选项将驱动程序默认配置为差分模式。

您还可以使用 `CONFIG_ADC_MCP3008_SPI_FREQUENCY` 配置选项配置与 MCP3008 的 SPI 通信速度。此速度应根据为 MCP3008 供电的电压来选择：

.. list-table:: 供电电压对应的 SPI 频率
   :widths: auto
   :header-rows: 1

   * - 供电电压
     - 频率
   * - VDD >= 4V
     - 3.6MHz
   * - VDD >= 3.3V
     - 2.34MHz
   * - VDD = 2.7V
     - 1.35MHz

如果从 MCP3008 获取了测量值，可以按如下方式将其转换为电压：

.. code-block:: c

   #define VREF (3.3) /* VREF 引脚上使用的电压 */

   struct adc_msg_s msg;

   /* 读取 ADC 设备的代码，可以参考 ADC 驱动程序文档 */

   double voltage = ((double)msg.am_data * VREF) / (1023.0);

MCP3008 还支持一个额外的 `ioctl()` 命令，允许您在运行时从差分模式切换到单端模式：

.. c:macro:: ANIOC_MCP3008_DIFF

此命令更改 MCP3008 驱动程序的模式。传递的参数应为 0 以禁用差分模式（即使用单端模式），为 1 以启用差分模式。不允许其他值。
