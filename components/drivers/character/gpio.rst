============
GPIO 驱动
============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

-  ``include/nuttx/ioexpander/gpio.h``。此头文件提供了将 GPIO 引脚作为驱动程序使用所需的所有结构体和 API。此头文件包括：

   #. 开发底层、特定于板卡的 GPIO 驱动程序所需的结构体和接口描述。
   #. 将 GPIO 驱动程序注册到通用 GPIO 字符驱动程序。
   #. 用户程序与通用 GPIO 字符驱动程序交互所需的接口。

-  ``drivers/ioexpander/gpio.c``。通用 GPIO 字符驱动程序的实现。

应用程序编程接口
=================================

应用程序编程接口通过以下头文件包含到应用程序中。

.. code-block:: c

  #include <nuttx/ioexpander/gpio.h>

GPIO 引脚可以是输入引脚或输出引脚。

一个 GPIO 引脚作为 POSIX 字符设备文件注册到 ``/dev`` 命名空间中。需要打开设备以获取文件描述符进行后续操作。这可以通过标准 POSIX ``open()`` 调用完成。每个驱动程序只支持一个引脚。

GPIO 驱动程序不允许标准 POSIX ``read()`` 和 ``write()`` 操作。所有接口都通过 IOCTL 调用路由。支持以下命令：

 * :c:macro:`GPIOC_WRITE`
 * :c:macro:`GPIOC_READ`
 * :c:macro:`GPIOC_PINTYPE`
 * :c:macro:`GPIOC_REGISTER`
 * :c:macro:`GPIOC_UNREGISTER`
 * :c:macro:`GPIOC_SETPINTYPE`
 * :c:macro:`GPIOC_SETDEBOUNCE`
 * :c:macro:`GPIOC_IRQ_SETMASK`


.. c:macro:: GPIOC_WRITE

``GPIOC_WRITE`` 命令设置输出 GPIO 的值。参数为 0（设置低电平）或 1（设置高电平）。只能写入输出引脚。典型用例是：

.. code-block:: c

  bool value = true;
  int ret = ioctl(fd, GPIOC_WRITE, value);


.. c:macro:: GPIOC_READ

``GPIOC_READ`` 命令读取 GPIO 的值。参数是指向 bool 值的指针，用于接收结果。结果为 0（低电平）或 1（高电平）。可以从输入和输出引脚读取。如果引脚是输出引脚，则返回当前设置的值。典型用例是：

.. code-block:: c

  bool value;
  int ret = ioctl(fd, GPIOC_READ, (unsigned long)(uintptr_t)&value);

.. c:macro:: GPIOC_PINTYPE

``GPIOC_PINTYPE`` 命令获取 GPIO 引脚的类型。参数是指向 :c:enum:`gpio_pintype_e` 类型实例的指针。

.. code-block:: c

  enum gpio_pintype_e
  {
    GPIO_INPUT_PIN = 0, /* 浮空 */
    GPIO_INPUT_PIN_PULLUP,
    GPIO_INPUT_PIN_PULLDOWN,
    GPIO_OUTPUT_PIN, /* 推挽 */
    GPIO_OUTPUT_PIN_OPENDRAIN,
    GPIO_INTERRUPT_PIN,
    GPIO_INTERRUPT_HIGH_PIN,
    GPIO_INTERRUPT_LOW_PIN,
    GPIO_INTERRUPT_RISING_PIN,
    GPIO_INTERRUPT_FALLING_PIN,
    GPIO_INTERRUPT_BOTH_PIN,
    GPIO_INTERRUPT_PIN_WAKEUP,
    GPIO_INTERRUPT_HIGH_PIN_WAKEUP,
    GPIO_INTERRUPT_LOW_PIN_WAKEUP,
    GPIO_INTERRUPT_RISING_PIN_WAKEUP,
    GPIO_INTERRUPT_FALLING_PIN_WAKEUP,
    GPIO_INTERRUPT_BOTH_PIN_WAKEUP,
    GPIO_NPINTYPES
  };

.. c:macro:: GPIOC_REGISTER

``GPIOC_REGISTER`` 命令注册一个引脚，以便在输入 GPIO 引脚上接收到中断时接收信号。当然，此功能取决于平台特定代码中的中断 GPIO 支持。有关更多信息，请参考描述目标平台的文档。参数是指向 :c:type:`sigevent` 值的指针，即中断发生时要生成的信号。

典型用例如下：

.. code-block:: c

  struct sigevent notify;

  notify.sigev_notify = SIGEV_SIGNAL;
  notify.sigev_signo = SIGUSR1;

  int ret = ioctl(fd, GPIOC_REGISTER, (unsigned long)&notify);

.. c:macro:: GPIOC_UNREGISTER

``GPIOC_UNREGISTER`` 命令注销一个引脚并停止接收引脚中断的信号。

.. c:macro:: GPIOC_SETPINTYPE

``GPIOC_SETPINTYPE`` 命令可用于更改 GPIO 引脚类型（从输入引脚更改为输出引脚、更改中断边沿等）。可设置的类型列在 :c:enum:`gpio_pintype_e` 中。

.. c:macro:: GPIOC_SETDEBOUNCE

``GPIOC_SETDEBOUNCE`` 命令设置 GPIO 输入引脚的去抖动时间。参数是指向整数值的指针，指定去抖动时间（以毫秒为单位）。这有助于过滤输入引脚上的虚假跳变（噪声）。

典型用例：

.. code-block:: c

  int debounce_ms = 10;
  int ret = ioctl(fd, GPIOC_SETDEBOUNCE, (unsigned long)(uintptr_t)&debounce_ms);

.. c:macro:: GPIOC_IRQ_SETMASK

``GPIOC_IRQ_SETMASK`` 命令设置 GPIO 引脚的中断掩码。参数是指向整数值的指针，指定用于启用或禁用特定中断类型（如上升/下降沿、电平等）的掩码。掩码的确切含义取决于平台实现。

典型用例：

.. code-block:: c

  int irq_mask = /* 平台特定的掩码值 */;
  int ret = ioctl(fd, GPIOC_IRQ_SETMASK, (unsigned long)(uintptr_t)&irq_mask);

应用程序示例
~~~~~~~~~~~~~~~~~~~

示例应用程序可以在 ``nuttx-apps`` 仓库的 ``examples/gpio`` 路径下找到。这是一个允许您读取、写入或配置 GPIO 引脚的示例应用程序。

配置
=============

本节描述 ``Kconfig`` 中的 GPIO 驱动程序配置。读者应参考目标文档了解目标特定配置。

GPIO 外设由 ``CONFIG_DEV_GPIO`` 启用。选项 ``CONFIG_DEV_NPOLLWAITERS`` 用于指定可以在轮询上等待的最大线程数，默认设置为一。还可以向 GPIO 驱动程序注册信号。允许的信号数量由 ``CONFIG_DEV_NSIGNALS`` 配置。

IO 扩展器设备驱动
==========================

IO 扩展器设备驱动是提供更多 GPIO 引脚的芯片，通常通过 SPI 或 I2C 总线连接到 MCU。如果需要，可以将扩展器的单个 GPIO 引脚注册为单独的引脚。此选项由 ``CONFIG_GPIO_LOWER_HALF`` 选项启用。有关更多描述，请参考 `ioexpander 文档 <https://nuttx.apache.org/docs/latest/components/drivers/special/ioexpander.html>`_。
