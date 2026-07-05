===========================
Microchip MCP4706/4716/4726
===========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Microchip MCP4706/4716/4726 DAC。

此数模转换器通过 I2C 总线通信。

-  ``include/nuttx/analog/mcp47x6.h``。此头文件提供了使用 DAC 驱动程序所需的所有结构体和 API。

以下功能可通过设备的 ``ioctl`` 接口配置：

- 增益
- 掉电模式
- 电压参考


使用示例
-------------

.. code-block:: c

   #include <nuttx/analog/dac.h>
   #include <nuttx/analog/mcp47x6.h>

   struct dac_dev_s *dac;
   unsigned int const i2c_bus = 0;
   unsigned int const i2c_address = 0x63;

   /* 创建并注册设备 */

   dac = mcp47x6_initialize(i2c_bus, i2c_address);
   dac_register("/dev/dac0", dac);

   /* 配置 DAC */

   int fd = open("/dev/dac0", O_WRONLY | O_NONBLOCK);
   ioctl(fd, ANIOC_MCP47X6_DAC_SET_REFERENCE, MCP47X6_REFERENCE_VREF_BUFFERED);

   /* 设置 DAC 输出值 */

   struct dac_msg_s dac_message = {
     .am_channel = 0,
     .am_data = 1234
   };
   write(fd, &dac_message, sizeof(dac_message));

   /* 清理 */

   close(fd);
