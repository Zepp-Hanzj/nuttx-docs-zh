======================================
Sim GPIO 芯片驱动（Linux 主机 GPIO）
============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
==

Sim GPIO 芯片驱动为 NuttX 模拟器（sim）提供了一种访问
Linux 主机 GPIO 芯片设备（``/dev/gpiochipN``）的机制。这使得
在模拟模式下运行的 NuttX 应用程序能够与连接到 Linux 主机系统的真实硬件 GPIO 引脚进行交互。

此驱动特别适用于：

- 在带有真实硬件的模拟环境中测试基于 GPIO 的应用程序
- 从 NuttX 模拟器与 USB 转 GPIO 适配器（如 CH341A）进行接口
- 无需专用嵌入式硬件即可开发和调试 GPIO 驱动

主机准备
====

主机端需要的准备工作：

- 所需硬件模块：USB-CH341A 模块
- Refer to https://github.com/frank-zago/ch341-i2c-spi-gpio, and install the driver
- 验证 /dev/gpiochipN 设备文件是否存在

架构
==

驱动由两层组成：

1. **NuttX Layer** (``sim_gpiochip.c``): Implements the NuttX ``ioexpander_dev_s``
      接口，为上层 NuttX 驱动提供标准 GPIO 操作。

2. **Host Layer** (``sim_linux_gpiochip.c``): Interfaces directly with Linux kernel's
      GPIO 字符设备（``/dev/gpiochipN``）使用 GPIO v2 ABI 进行接口。

::

    +---------------------+
    |  NuttX Application  |
    +---------------------+
            |
            v
    +---------------------+
    |  GPIO Lower Half    |
    |  (gpio_lower_half)  |
    +---------------------+
            |
            v
    +---------------------+
    |   sim_gpiochip.c    |  <-- NuttX ioexpander interface
    | (ioexpander_dev_s)  |
    +---------------------+
            |
            v
    +---------------------+
    | sim_linux_gpiochip.c|  <-- Linux host GPIO interface
    |  (GPIO v2 ABI)      |
    +---------------------+
            |
            v
    +---------------------+
    |  /dev/gpiochipN     |  <-- Linux GPIO character device
    +---------------------+

头文件
===

-  ``arch/sim/src/sim/sim_hostgpiochip.h``: Host GPIO chip interface definitions
      和函数原型。

-  ``include/nuttx/ioexpander/ioexpander.h``: Standard NuttX IO expander interface.

-  ``include/nuttx/ioexpander/gpio.h``: NuttX GPIO interface definitions.

配置选项
====

以下配置选项与此驱动相关：

- ``CONFIG_SIM_GPIOCHIP``：启用 sim GPIO 芯片驱动。
- ``CONFIG_IOEXPANDER_NPINS``：支持的最大 GPIO 引脚数（默认：64）。
- ``CONFIG_IOEXPANDER_INT_ENABLE``：启用 GPIO 引脚的中断支持。

支持的操作
=====

驱动支持以下 GPIO 操作：

方向控制
----

.. code-block:: c

   int sim_gpiochip_direction(struct ioexpander_dev_s *dev,
                              uint8_t pin, int direction);

设置 GPIO 引脚方向。支持的方向：

- ``IOEXPANDER_DIRECTION_IN``：配置为输入
- ``IOEXPANDER_DIRECTION_OUT``：配置为输出
- ``IOEXPANDER_DIRECTION_OUT_OPENDRAIN``：配置为开漏输出

读取/写入引脚
-------

.. code-block:: c

   int sim_gpiochip_readpin(struct ioexpander_dev_s *dev, uint8_t pin,
                            bool *value);
   int sim_gpiochip_writepin(struct ioexpander_dev_s *dev, uint8_t pin,
                             bool value);

读取或写入 GPIO 引脚的值。

中断配置
----

.. code-block:: c

   int sim_gpiochip_option(struct ioexpander_dev_s *dev, uint8_t pin,
                           int option, void *val);

配置 GPIO 引脚选项。支持的中断边沿配置：

- ``IOEXPANDER_VAL_RISING``：上升沿触发
- ``IOEXPANDER_VAL_FALLING``：下降沿触发
- ``IOEXPANDER_VAL_BOTH``：双沿触发
- ``IOEXPANDER_VAL_DISABLE``：禁用中断

中断回调
----

.. code-block:: c

   void *sim_gpiochip_attach(struct ioexpander_dev_s *dev,
                             ioe_pinset_t pinset,
                             ioe_callback_t callback,
                             void *arg);
   int sim_gpiochip_detach(struct ioexpander_dev_s *dev, void *handle);

附加或分离 GPIO 引脚的中断回调函数。

主机层 API
=======

主机层（``sim_linux_gpiochip.c``）提供以下功能：

.. code-block:: c

   /* Allocate and initialize a host GPIO chip device */
   struct host_gpiochip_dev *host_gpiochip_alloc(const char *filename);

   /* Free a host GPIO chip device */
   void host_gpiochip_free(struct host_gpiochip_dev *dev);

   /* Set GPIO pin direction */
   int host_gpiochip_direction(struct host_gpiochip_dev *dev,
                               uint8_t pin, bool input);

   /* Read GPIO pin value */
   int host_gpiochip_readpin(struct host_gpiochip_dev *dev,
                             uint8_t pin, bool *value);

   /* Write GPIO pin value */
   int host_gpiochip_writepin(struct host_gpiochip_dev *dev,
                              uint8_t pin, bool value);

   /* Request GPIO interrupt */
   int host_gpiochip_irq_request(struct host_gpiochip_dev *dev,
                                 uint8_t pin, uint16_t cfgset);

   /* Check if GPIO interrupt is active */
   bool host_gpiochip_irq_active(struct host_gpiochip_dev *dev, uint8_t pin);

   /* Get GPIO line information */
   int host_gpiochip_get_line(struct host_gpiochip_dev *priv,
                              uint8_t pin, bool *input);

Linux 内核版本要求
============

驱动使用 Linux GPIO v2 ABI，要求：

- **Linux 内核 >= 6.8.0**：具有 GPIO v2 API 支持的完整功能。
- **Linux 内核 < 6.8.0**：驱动可以编译但提供存根实现
    返回 0 或 NULL。

使用示例
====

初始化
---

.. code-block:: c

   #include <nuttx/ioexpander/gpio.h>
   #include "sim_internal.h"

   int board_gpio_initialize(void)
   {
     struct ioexpander_dev_s *ioe;
     int ret;

     /* Initialize the GPIO chip device */
     ioe = sim_gpiochip_initialize("/dev/gpiochip0");
     if (ioe == NULL)
       {
         return -ENODEV;
       }

     /* Register GPIO pins using gpio_lower_half */
     ret = gpio_lower_half(ioe, 0, GPIO_INPUT_PIN, 60);  /* Pin 0 as input, minor 60 */
     if (ret < 0)
       {
         return ret;
       }

     ret = gpio_lower_half(ioe, 1, GPIO_OUTPUT_PIN, 61); /* Pin 1 as output, minor 61 */
     if (ret < 0)
       {
         return ret;
       }

     return OK;
   }

应用使用
----

初始化后，可以通过标准 NuttX GPIO 接口访问 GPIO 引脚：

.. code-block:: c

   #include <fcntl.h>
   #include <sys/ioctl.h>
   #include <nuttx/ioexpander/gpio.h>

   int main(void)
   {
     int fd;
     bool value;

     /* Open GPIO device */
     fd = open("/dev/gpio60", O_RDWR);
     if (fd < 0)
       {
         return -1;
       }

     /* Read GPIO value */
     ioctl(fd, GPIOC_READ, &value);
     printf("GPIO value: %d\n", value);

     close(fd);
     return 0;
   }

中断处理
====

驱动使用工作队列来轮询 GPIO 事件。轮询间隔
由 ``SIM_GPIOCHIP_WORK_DELAY`` 定义（默认：500 微秒）。

当在 GPIO 引脚上检测到中断事件时，已注册的回调
函数将使用引脚号和用户提供的参数被调用。

.. code-block:: c

   static int gpio_interrupt_handler(struct ioexpander_dev_s *dev,
                                     ioe_pinset_t pinset, void *arg)
   {
     printf("GPIO interrupt on pin %d\n", pinset);
     return OK;
   }

   /* Attach interrupt handler */
   void *handle = IOEP_ATTACH(ioe, (1 << pin), gpio_interrupt_handler, NULL);

   /* Configure interrupt edge */
   IOEP_SETOPTION(ioe, pin, IOEXPANDER_OPTION_INTCFG,
                  (void *)IOEXPANDER_VAL_RISING);

文件
==

-  ``arch/sim/src/sim/sim_gpiochip.c``：NuttX IO 扩展器实现
-  ``arch/sim/src/sim/posix/sim_linux_gpiochip.c``：Linux 主机 GPIO 接口
-  ``arch/sim/src/sim/sim_hostgpiochip.h``：主机 GPIO 芯片头文件

限制
==

1. **基于轮询的中断**：由于模拟限制，中断
      使用轮询而非真正的硬件中断来实现。

2. **Linux 内核版本**：完整功能需要 Linux 内核 >= 6.8.0。

3. **引脚数量**：受 ``CONFIG_IOEXPANDER_NPINS`` 配置限制。

4. **反转选项**：``IOEXPANDER_OPTION_INVERT`` 选项尚未实现。

另请参阅
====

-  Linux GPIO documentation: https://www.kernel.org/doc/html/latest/driver-api/gpio/
