==========================
IO 扩展器设备驱动
==========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

IO 扩展器子系统定义在以下头文件中：

- ``include/nuttx/ioexpander/ioexpander.h`` — 定义了公共 IO 扩展器接口：驱动和消费者使用的宏、类型和辅助访问宏。
- ``include/nuttx/ioexpander/gpio.h`` — 提供了"gpio 下半部分"辅助工具，允许将 IO 扩展器引脚注册为标准 GPIO 字符设备（参见 ``gpio_lower_half`` 和 ``gpio_lower_half_byname``）。

每个 IO 扩展器驱动必须实现 ``struct ioexpander_ops_s`` 的一个实例。该结构定义了下半部分调用表和驱动必须提供的操作；公共头文件还包含分派到下半部分操作表的辅助宏。

辅助工具 ``gpio_lower_half`` 可用于将单个扩展器引脚注册为标准 GPIO 设备，以便上半部分 GPIO 消费者可以通过通用 GPIO 字符驱动访问扩展器引脚。

**绑定 IO 扩展器驱动**

IO 扩展器驱动通常由板级特定代码绑定，而不是从应用程序代码直接访问。对于 I2C 或 SPI 连接的扩展器，典型顺序是：

#. 从硬件特定的总线驱动获取总线实例（例如 ``struct i2c_master_s *``）。
#. 使用总线实例和设备特定配置调用扩展器驱动的初始化例程；初始化例程返回 ``struct ioexpander_dev_s *`` 实例。
#. 直接使用返回的 ``ioe`` 实例，或通过 ``gpio_lower_half`` 将单个扩展器引脚注册到上半部分 GPIO 驱动。


-  **示例**：``drivers/ioexpander/pca9555.c``、
   ``drivers/input/aw86225.c``、
   ``drivers/analog/lmp92001.c``、
   ``drivers/ioexpander/ioe_rpmsg.c``、
   ``boards/sim/sim/sim/src/sim_ioexpander.c``、
   ``boards/arm/nrf52/thingy52/src/nrf52_sx1509.c`` 等。

更多信息
===============

头文件
------------

相关头文件为：

- ``include/nuttx/ioexpander/ioexpander.h`` — 定义了用于与 IO 扩展器交互的宏、类型和访问宏。
- ``include/nuttx/ioexpander/gpio.h`` — 提供了"gpio 下半部分"辅助工具，允许将 IO 扩展器引脚注册为标准 GPIO 设备。

关键宏和选项概述
----------------------------------

以下是头文件中定义的重要宏的简明参考。这些是通常通过 ``IOEXP_SETOPTION`` 和各种访问宏使用的选项。主要预处理器定义如下（C 语法）：

.. code-block:: c

   /* 方向定义 */
   #define IOEXPANDER_DIRECTION_IN            0  /* float */
   #define IOEXPANDER_DIRECTION_IN_PULLUP     1
   #define IOEXPANDER_DIRECTION_IN_PULLDOWN   2
   #define IOEXPANDER_DIRECTION_OUT           3  /* push-pull */
   #define IOEXPANDER_DIRECTION_OUT_OPENDRAIN 4
   #define IOEXPANDER_DIRECTION_OUT_LED       5  /* LED output */

   /* 引脚集掩码辅助宏 */
   #define IOEXPANDER_PINMASK  (((ioe_pinset_t)1 << CONFIG_IOEXPANDER_NPINS) - 1)
   #define PINSET_ALL          (~((ioe_pinset_t)0))

   /* 通用选项值（与 IOEXP_SETOPTION 一起使用） */
   /* 反转（有效电平） */
   #define IOEXPANDER_OPTION_INVERT      1
   #define IOEXPANDER_VAL_NORMAL         0  /* 正常极性 */
   #define IOEXPANDER_VAL_INVERT         1  /* 反转极性 */

   /* 中断配置（电平/边沿 和 高/低/上升/下降/双沿） */
   #define IOEXPANDER_OPTION_INTCFG      2
   #define IOEXPANDER_VAL_DISABLE        0  /* 0000 禁用中断 */
   #define IOEXPANDER_VAL_LEVEL          1  /* xx01: 电平触发 */
   #define IOEXPANDER_VAL_EDGE           2  /* xx10: 边沿触发 */
   #define IOEXPANDER_VAL_HIGH           5  /* 0101: 高电平 */
   #define IOEXPANDER_VAL_LOW            9  /* 1001: 低电平 */
   #define IOEXPANDER_VAL_RISING         6  /* 0110: 上升沿 */
   #define IOEXPANDER_VAL_FALLING        10 /* 1010: 下降沿 */
   #define IOEXPANDER_VAL_BOTH           14 /* 1110: 双沿 */

   /* LED 配置 */
   #define IOEXPANDER_OPTION_LEDCFG      3  /* 为引脚分配 LED 编号 */

   /* 非通用（驱动特定）选项 */
   #define IOEXPANDER_OPTION_NONGENERIC  4  /* 传递驱动特定结构 */

   /* 唤醒配置（将引脚配置为 SoC 唤醒源） */
   #define IOEXPANDER_OPTION_WAKEUPCFG   5
   #define IOEXPANDER_WAKEUP_DISABLE     0
   #define IOEXPANDER_WAKEUP_ENABLE      1

   /* 去抖和中断掩码（最近添加） */
   #define IOEXPANDER_OPTION_SETDEBOUNCE 6  /* 配置去抖 */
   #define IOEXPANDER_DEBOUNCE_DISABLE  0
   #define IOEXPANDER_DEBOUNCE_ENABLE   1

   #define IOEXPANDER_OPTION_SETMASK     7  /* 控制中断掩码 */
   #define IOEXPANDER_MASK_DISABLE       0  /* 取消屏蔽（启用）中断 */
   #define IOEXPANDER_MASK_ENABLE        1  /* 屏蔽（抑制）中断 */

访问宏（API）
-------------------

头文件暴露了一组辅助宏，分派到底层驱动操作表（``struct ioexpander_ops_s``）：

.. c:macro:: IOEXP_SETDIRECTION(dev, pin, dir)

   设置引脚方向（输入、输出、开漏、LED、上拉/下拉）。
   成功返回 0，失败返回负的 errno。

.. c:macro:: IOEXP_SETOPTION(dev, pin, opt, val)

   通用选项设置接口，用于配置上述列出的选项。注意 ``val`` 是 ``void *``；驱动可能接受强制转换为指针的整数或指向驱动特定结构的指针。

   示例::

     /* 反转引脚极性 */
     IOEXP_SETOPTION(dev, 3, IOEXPANDER_OPTION_INVERT,
                     (FAR void *)IOEXPANDER_VAL_INVERT);

     /* 在引脚 2 上启用去抖 */
     IOEXP_SETOPTION(dev, 2, IOEXPANDER_OPTION_SETDEBOUNCE,
                     (FAR void *)IOEXPANDER_DEBOUNCE_ENABLE);

     /* 屏蔽引脚 5 的中断 */
     IOEXP_SETOPTION(dev, 5, IOEXPANDER_OPTION_SETMASK,
                     (FAR void *)IOEXPANDER_MASK_ENABLE);

.. c:macro:: IOEXP_WRITEPIN(dev, pin, val)

   设置引脚电平。成功返回 0，错误返回负的 errno。

.. c:macro:: IOEXP_READPIN(dev, pin, valptr)

   读取实际物理引脚电平。值通过 ``valptr`` 返回。

.. c:macro:: IOEXP_READBUF(dev, pin, valptr)

   读取扩展器缓存的缓冲/寄存器值。

   - ``IOEXP_WRITEPIN`` 设置引脚电平（TRUE 通常表示高电平）。
     如果配置了极性反转，驱动会处理。
   - ``IOEXP_READPIN`` 读取实际物理引脚电平。
   - ``IOEXP_READBUF`` 读取扩展器缓存的缓冲/寄存器值。

多引脚操作
--------------------

当启用 ``CONFIG_IOEXPANDER_MULTIPIN`` 时，批处理操作可用，可能比重复的单引脚调用更高效：

- ``IOEXP_MULTIWRITEPIN(dev, pins, vals, count)``
- ``IOEXP_MULTIREADPIN(dev, pins, vals, count)``
- ``IOEXP_MULTIREADBUF(dev, pins, vals, count)``

中断和回调
--------------------

如果启用了 ``CONFIG_IOEXPANDER_INT_ENABLE``，头文件定义了回调类型和附加/分离辅助宏。回调签名为::

   typedef CODE int (*ioe_callback_t)(FAR struct ioexpander_dev_s *dev,
                                                       ioe_pinset_t pinset, FAR void *arg);

当监控的引脚集发生事件时调用回调。当 ``CONFIG_IOEXPANDER_INT_ENABLE`` 启用时，附加/分离辅助宏作为宏提供，分派到下半部分驱动：

.. c:macro:: IOEP_ATTACH(dev, pinset, callback, arg)

   附加并启用引脚中断回调。成功返回非 NULL 的不透明句柄。``pinset`` 选择哪些引脚将产生回调；``callback`` 是 ``ioe_callback_t`` 类型的函数，``arg`` 传递给回调。

.. c:macro:: IOEP_DETACH(dev, handle)

   分离并禁用先前通过 ``handle`` 引用的已附加回调。

注意：当 ``CONFIG_IOEXPANDER_NPINS`` > 64 时，``ioe_pinset_t`` 表示单个中断引脚编号而不是位掩码。

驱动接口（下半部分）
-----------------------------

每个 IO 扩展器驱动必须实现操作表 ``struct ioexpander_ops_s``。驱动至少应提供：

- ``ioe_direction``
- ``ioe_option``
- ``ioe_writepin``
- ``ioe_readpin``
- ``ioe_readbuf``

当启用相应的配置选项时，应提供可选的多引脚和中断附加/分离方法。

绑定到上层（gpio_lower_half）
--------------------------------------------

应用程序通常不直接访问 IO 扩展器驱动。典型的绑定步骤是：

1. 从硬件特定的总线驱动获取总线实例（例如 ``struct i2c_master_s *``）。
2. 使用总线实例和设备配置调用扩展器驱动的初始化例程以获取 ``struct ioexpander_dev_s *``。
3. 直接使用返回的 ``ioe`` 实例，或通过 ``gpio_lower_half`` 或 ``gpio_lower_half_byname`` 将单个扩展器引脚注册为标准 GPIO 设备。

示例（伪代码）::

   /* 获取 I2C 总线 */
   struct i2c_master_s *i2c = up_i2cinitialize(0);

   /* 初始化扩展器（驱动特定初始化） */
   struct ioexpander_dev_s *ioe = pca9555_initialize(i2c, CONFIG_PCA9555_ADDR);

   /* 配置引脚 0 为带上拉的输入并启用去抖 */
   IOEXP_SETDIRECTION(ioe, 0, IOEXPANDER_DIRECTION_IN_PULLUP);
   IOEXP_SETOPTION(ioe, 0, IOEXPANDER_OPTION_SETDEBOUNCE,
                           (FAR void *)IOEXPANDER_DEBOUNCE_ENABLE);

示例和参考
-----------------------

参见以下驱动和板级示例了解具体用法：

- ``drivers/ioexpander/pca9555.c`` — I2C IO 扩展器实现。
- ``drivers/ioexpander/ioe_rpmsg.c`` — 基于 RPMSG 的 IO 扩展器。
- ``boards/arm/nrf52/thingy52/src/nrf52_sx1509.c`` — 绑定示例。
