==============
Regmap 驱动
==============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 drivers/regmap/ 的文档页面。

Regmap 头文件
===================

- ``include/nuttx/regmap/regmap.h``

  regmap 中使用的结构和 API 在此头文件中。

- ``struct regmap_bus_s``

  每个总线必须实现 struct regmap_bus_s 的一个实例。该结构定义了包含以下方法的调用表：

    - 寄存器的单字节读取（8 位）

      .. code-block:: C
         typedef CODE int (*reg_read_t)(FAR struct regmap_bus_s *bus,
                                        unsigned int reg,
                                        FAR void *val);

    - 寄存器的单字节写入（8 位）

      .. code-block:: C
         typedef CODE int (*reg_write_t)(FAR struct regmap_bus_s *bus,
                                         unsigned int reg,
                                         unsigned int val);

    - 批量寄存器数据读取。

      .. code-block:: C
         typedef CODE int (*read_t)(FAR struct regmap_bus_s *bus,
                                   FAR const void *reg_buf, unsigned int reg_size,
                                   FAR void *val_buf, unsigned int val_size);

    - 批量寄存器数据写入。

      .. code-block:: C
         typedef CODE int (*write_t)(FAR struct regmap_bus_s *bus,
                                     FAR const void *data,
                                     unsigned int count);

    - 初始化 regmap 的内部配置。第一个参数必须是总线的句柄，第二个参数是总线的配置参数。最后，这两个参数将透明地传递给相应的总线。如果您想自己实现总线接口，需要实现相应的总线初始化函数，请参考 regmap_i2c.c 和 regmap_spi.c。

      .. code-block:: C
         FAR struct regmap_s *regmap_init(FAR struct regmap_bus_s *bus,
                                     FAR const struct regmap_config_s *config);

    - Regmap 初始化 I2C 总线。

      .. code-block:: C
         FAR struct regmap_s *regmap_init_i2c(FAR struct i2c_master_s *i2c,
                                              FAR struct i2c_config_s *i2c_config,
                                              FAR const struct regmap_config_s *config);

    - Regmap 初始化 SPI 总线。

      .. code-block:: C
         FAR struct regmap_s *regmap_init_spi(FAR struct spi_dev_s *spi, uint32_t freq,
                                              uint32_t devid, enum spi_mode_e mode,
                                              FAR const struct regmap_config_s *config);

    - 退出并销毁 regmap。

      .. code-block:: C
         void regmap_exit(FAR struct regmap_s *map);

    - Regmap 的 write()、bulk_write()、read()、bulk_read()，在初始化 regmap 总线设备后调用。第一个参数是 regmap_s 指针。

      .. code-block:: C
         int regmap_write(FAR struct regmap_s *map, unsigned int reg,
                          unsigned int val);
         int regmap_bulk_write(FAR struct regmap_s *map, unsigned int reg,
                               FAR const void *val, unsigned int val_count);
         int regmap_read(FAR struct regmap_s *map, unsigned int reg,
                         FAR void *val);
         int regmap_bulk_read(FAR struct regmap_s *map, unsigned int reg,
                              FAR void *val, unsigned int val_count);

示例
========

以 BMI160 传感器为例：
- 头文件

.. code-block:: C

    #include <nuttx/i2c/i2c_master.h>
    #include <nuttx/sensors/bmi160.h>
    #include <nuttx/regmap/regmap.h>

    #include <stdlib.h>


- 在驱动生命周期中定义 regmap_s 句柄

.. code-block:: C

   struct bmi160_dev_s
   {
   #ifdef CONFIG_SENSORS_BMI160_I2C
   FAR struct regmap_s * regmap;     /* Regmap 接口 */
   #else /* CONFIG_SENSORS_BMI160_SPI */
   FAR struct spi_dev_s *spi;       /* SPI 接口 */
   #endif
   };


- 初始化 regmap

.. code-block:: C

   int bmi160_i2c_regmap_init(FAR struct bmi160_dev_s *priv,
                              FAR struct i2c_master_s *i2c)
    {
      struct regmap_config_s config;
      struct i2c_config_s dev_config;

      config.reg_bits = 8;
      config.val_bits = 8;
      config.disable_locking = true;

      dev_config.frequency = BMI160_I2C_FREQ;
      dev_config.address   = BMI160_I2C_ADDR;
      dev_config.addrlen   = 7;

      priv->regmap = regmap_init_i2c(i2c, &dev_config, &config);
      if (priv->regmap == NULL)
        {
          snerr("bmi160 Initialize regmap configuration failed!");
          return -ENXIO;
        }

      return OK;
    }

- 使用：

.. code-block:: C

  int ret;

  ret = regmap_read(priv->regmap, regaddr, &regval);
  if (ret < 0)
    {
      snerr("regmap read address[%2X] failed: %d!\n", regaddr, ret);
    }
   

  ret = regmap_write(priv->regmap, regaddr, regval);
  if (ret < 0)
    {
      snerr("regmap write address[%2X] failed: %d!\n", regaddr, ret);
    }

  ret = regmap_bulk_read(priv->regmap, regaddr, regval, len);
  if (ret < 0)
    {
      snerr("regmap read bulk address[%2X] failed: %d!\n", regaddr, ret);
    }
