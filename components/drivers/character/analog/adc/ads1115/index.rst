==========
TI ADS1115
==========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

由 Jia Lin 贡献

ADS1115 是一款由 Texas Instruments 生产的 16 位、4 通道 ADC，通过 I2C 总线通信。它可以单独测量每个通道的电压，也可以测量不同通道对之间的电压。ADS1115 还支持可编程增益放大器（PGA）和数字比较器。


.. list-table:: 通道号与对应源
   :widths: auto

   * - 通道号
     - AINP
     - AINN
   * - 0
     - AIN0
     - AIN1
   * - 1
     - AIN0
     - AIN3
   * - 2
     - AIN1
     - AIN3
   * - 3
     - AIN2
     - AIN3
   * - 4
     - AIN0
     - GND
   * - 5
     - AIN1
     - GND
   * - 6
     - AIN2
     - GND
   * - 7
     - AIN3
     - GND

驱动程序接口
---------------------

要将 ADS1115 设备驱动程序注册为标准 NuttX 模拟设备，可以使用类似以下适用于 RP2040 的代码。

.. code-block:: c

  #include <nuttx/analog/ads1115.h>
  #include <nuttx/analog/adc.h>

  /* 注册 ADS1115 ADC */

  struct adc_dev_s *ads1115 = ads1115_initialize(rp2040_i2cbus_initialize(0),
                                                 CONFIG_ADC_ADS1115_ADDR);
  if (ads1115 == NULL)
    {
      syslog(LOG_ERR, "Failed to initialize ADS1115\n");
    }

  ret = adc_register("/dev/adc1", ads1115);
  if (ret < 0)
    {
      syslog(LOG_ERR, "Failed to register ADS1115 device driver: %d\n", ret);
    }

如果从 ADS1115 获取了测量值，可以按如下方式将其转换为电压：

.. code-block:: c

   #define FSR (2.048)

   struct adc_msg_s msg;

   /* 读取 ADC 设备的代码，可以参考 ADC 驱动程序文档 */

   double voltage = ((double)msg.am_data  * FSR) / (32768.0);

注册后，此驱动程序可以使用 ADC 示例（:ref:`adc-example`）进行交互。请确保启用软件触发，因为 ADS1115 驱动程序不支持硬件触发（中断）。您还可以将每组采样数更改为最多 8 个，覆盖 ADC 的所有 8 个通道。

您可能需要将 `CONFIG_ADC_FIFOSIZE` 值增加到大于 8 的值，以便在测量触发后能够存储所有 ADC 测量值（例如 9）。

配置
---------------------

.. list-table:: 配置选项
   :widths: auto

   * - 名称
     - 描述
   * - CONFING_ADC_ADS1115_I2C_FREQUENCY
     - ADS1115 的 I2C 频率
   * - CONFIG_ADC_ADS1115_ADDR
     - ADS1115 的 I2C 地址
   * - CONFIG_ADC_ADS1115_CHANNEL
     - 默认读取的 ADC 通道
   * - CONFIG_ADC_ADS1115_PGA
     - ADS1115 的增益
   * - CONFIG_ADC_ADS1115_CONTINOUS
     - ADS1115 的连续模式
   * - CONFIG_ADC_ADS1115_DR
     - ADS1115 的数据速率
   * - CONFIG_ADC_ADS1115_COMP_MODE
     - ADS1115 比较器模式，传统或窗口模式
   * - CONFIG_ADC_ADS1115_COMP_POL
     - ADS1115 比较器极性，高电平有效或低电平有效
   * - CONFIG_ADC_ADS1115_COMP_LAT
     - ADS1115 比较器锁存模式，传统或锁存模式
   * - CONFIG_ADC_ADS1115_COMP_QUE
     - ADS1115 比较器队列，决定 ALRT/RDY 引脚何时被置位
   * - CONFIG_ADC_ADS1115_HI_THRESH
     - ADS1115 的 HIGH_THRESH 寄存器
   * - CONFIG_ADC_ADS1115_LO_THRESH
     - ADS1115 的 LOW_THRESH 寄存器

.. list-table:: 数据速率
   :widths: auto

   * - Kconfig 中的值
     - 数据速率
   * - 0
     - 8 SPS
   * - 1
     - 16 SPS
   * - 2
     - 32 SPS
   * - 3
     - 64 SPS
   * - 4
     - 128 SPS
   * - 5
     - 250 SPS
   * - 6
     - 475 SPS
   * - 7
     - 860 SPS


.. list-table:: PGA 值
   :widths: auto

   * - Kconfig 中的值
     - 满量程范围（FSR）
   * - 0
     - ±6.144V
   * - 1
     - ±4.096V
   * - 2
     - ±2.048V
   * - 3
     - ±1.024V
   * - 4
     - ±0.512V
   * - 5
     - ±0.256V
   * - 6
     - ±0.256V
   * - 7
     - ±0.256V


.. list-table:: 比较器队列值
   :widths: auto

   * - Kconfig 中的值
     - 比较器队列
   * - 0
     - 一次转换后置位
   * - 1
     - 两次转换后置位
   * - 2
     - 四次转换后置位
   * - 3
     - 禁用比较器



其他 ioctl 命令
--------------------------------

ADS1115 驱动程序支持各种额外的 ioctl() 命令。
这些命令主要用于在运行时更改配置。

.. c:macro:: ANIOC_ADS1115_SET_PGA

此命令更改 ADS1115 驱动程序的增益。传递的参数应为 ads1115_pga_e 类型，对应于上述增益值。

.. c:macro:: ANIOC_ADS1115_SET_MODE

此命令将 ADS1115 切换为连续或单次转换模式。

.. c:macro:: ANIOC_ADS1115_SET_DR

此命令更改 ADS1115 驱动程序的数据速率。传递的参数应为 ads1115_dr_e 类型，对应于上述数据速率值。

.. c:macro:: ANIOC_ADS1115_SET_COMP_MODE

此命令将 ADS1115 切换为传统或窗口比较器模式。

.. c:macro:: ANIOC_ADS1115_SET_COMP_POL

此命令将 ADS1115 切换为高电平有效或低电平有效模式。

.. c:macro:: ANIOC_ADS1115_SET_COMP_LAT

此命令将 ADS1115 切换为传统或锁存比较器模式。

.. c:macro:: ANOIC_ADS1115_SET_COMP_QUEUE

此命令更改 ADS1115 的比较器队列功能。传递的参数应为 ads1115_comp_queue_e 类型，对应于上述比较器队列值。

.. c:macro:: ANOIC_ADS1115_SET_HI_THRESH

此命令更改 ADS1115 的 HIGH_THRESH 寄存器。传递的参数应为 uint16_t 类型，对应于 HIGH_THRESH 寄存器值。

.. c:macro:: ANOIC_ADS1115_SET_LO_THRESH

此命令更改 ADS1115 的 LOW_THRESH 寄存器。传递的参数应为 uint16_t 类型，对应于 LOW_THRESH 寄存器值。

.. c:macro:: ANIOC_ADS1115_READ_CHANNEL

此命令从 ADS1115 的特定通道读取值。传递的参数应为指向 struct adc_msg_s 的指针。

.. c:macro:: ANIOC_ADS1115_TRIGGER_CONVERSION

此命令触发 ADS1115 的模拟转换。传递的参数应为指向 ``struct adc_msg_s`` 的指针，其中 ``am_channel`` 成员应初始化为要开始转换的通道号。

.. c:macro:: ANIOC_ADS1115_READ_CHANNEL_NO_CONVERSION

此命令读取 ADS1115 上次转换的结果。传递的参数应为指向 ``struct adc_msg_s`` 的指针，转换结果将存储在其中。
