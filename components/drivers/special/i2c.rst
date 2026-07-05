==================
I2C 设备驱动
==================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

-  ``include/nuttx/i2c/i2c_master.h``
   使用 I2C 驱动所需的所有结构和 API 都在此头文件中提供。

-  ``struct i2c_ops_s``。每个 I2C 设备驱动必须实现
   ``struct i2c_ops_s`` 的一个实例。该结构定义了包含以下方法的调用表：

-  **绑定 I2C 驱动**。I2C 驱动通常不由用户代码直接
   访问，而是绑定到另一个更高级别的设备驱动。通常的绑定顺序是：

   #. 从硬件特定的 I2C 设备驱动获取 ``struct i2c_master_s`` 的
      实例，然后
   #. 将该实例提供给更高级别设备驱动的初始化方法。

-  **示例**：``arch/z80/src/ez80/ez80_i2c.c``、
   ``arch/z80/src/z8/z8_i2c.c`` 等。


=======================
I2C 位操作驱动
=======================

I2C 位操作驱动提供了一种使用 GPIO 引脚的 I2C 协议软件实现。当硬件 I2C 外设不可用或需要额外的 I2C 总线时，这非常有用。

概述
--------

-  ``include/nuttx/i2c/i2c_bitbang.h``
   通用上半部分 I2C 位操作驱动接口。

-  ``drivers/i2c/i2c_bitbang.c``
   处理 I2C 协议时序的通用上半部分实现。

-  平台特定的下半部分驱动控制 GPIO 引脚（SDA 和 SCL）。

基于 IO 扩展器的 I2C 位操作
-------------------------------

为使用 IO 扩展器控制 GPIO 引脚的系统提供了通用下半部分实现。这消除了通过 IO 扩展器引脚实现 I2C 位操作时对平台特定代码的需求。

配置
~~~~~~~~~~~~~

-  ``CONFIG_I2C_BITBANG`` - 启用 I2C 位操作驱动框架
-  ``CONFIG_I2C_BITBANG_IOEXPANDER`` - 启用基于 IO 扩展器的下半部分
   （依赖于 ``CONFIG_IOEXPANDER``）

头文件
~~~~~~~~~~~~

-  ``include/nuttx/i2c/i2c_bitbang_ioexpander.h``
   基于 IO 扩展器的下半部分驱动接口。

API
~~~

.. c:function:: FAR struct i2c_master_s *i2c_bitbang_ioexpander_initialize(FAR struct ioexpander_dev_s *ioe, int scl_pin, int sda_pin, int busnum);

   使用 IO 扩展器引脚初始化 I2C 位操作驱动。

   :param ioe: IO 扩展器设备的指针
   :param scl_pin: SCL（时钟线）的 IO 扩展器引脚编号
   :param sda_pin: SDA（数据线）的 IO 扩展器引脚编号
   :param busnum: 要注册的 I2C 总线编号（使用负值跳过注册）
   
   :return: 成功时返回 ``struct i2c_master_s`` 的指针，失败时返回 NULL

   引脚将被配置为开漏输出，这对于正确的 I2C 操作是必需的。如果 busnum >= 0，I2C 总线将自动注册并可通过标准 I2C API 访问。

使用示例
~~~~~~~~~~~~~

.. code-block:: c

   #include <nuttx/ioexpander/ioexpander.h>
   #include <nuttx/i2c/i2c_bitbang_ioexpander.h>
   #include <nuttx/i2c/i2c_master.h>

   /* 假设我们有一个 IO 扩展器设备 */
   FAR struct ioexpander_dev_s *ioe = /* ... 获取 IO 扩展器 ... */;
   FAR struct i2c_master_s *i2c;

   /* 使用 IO 扩展器引脚 10 (SCL) 和 11 (SDA) 初始化 I2C 位操作 */
   /* 注册为 I2C 总线 0 */
   i2c = i2c_bitbang_ioexpander_initialize(ioe, 10, 11, 0);
   if (i2c == NULL)
     {
       /* 初始化失败 */
       return -1;
     }

   /* 现在可以正常使用 I2C 主设备 */
   /* 例如，使用 I2C 字符驱动或直接使用 */

   /* 如果已注册 (busnum >= 0)，也可以通过 /dev/i2c0 访问 */

使用场景
~~~~~~~~~

-  **GPIO 扩展**：当使用 I2C 或 SPI IO 扩展器进行 GPIO 扩展时，
   需要使用这些扩展引脚实现额外的 I2C 总线。

-  **多主控场景**：软件位操作在硬件 I2C 有限制的多主控配置中可能有用。

-  **引脚灵活性**：在任何 GPIO 引脚上实现 I2C，不限于
   硬件 I2C 外设引脚。

-  **测试和调试**：在原型设计和调试期间使用 IO 扩展器引脚进行 I2C 通信。

-  **硬件 I2C 不可用**：当硬件 I2C 外设已用尽
   或在特定引脚上不可用时。

特性
~~~~~~~~

-  使用标准 IO 扩展器 API (``IOEXP_WRITEPIN``、``IOEXP_READPIN``)
-  自动开漏配置
-  支持时钟拉伸（通过引脚读取）
-  平台无关的实现
-  适用于任何实现标准接口的 IO 扩展器
-  自动 I2C 总线注册

限制
~~~~~~~~~~~

-  软件时序（比硬件 I2C 慢）
-  时序精度取决于系统负载和 IO 扩展器响应时间
-  限于标准 I2C 速度（快速模式和高速模式可能不可靠）

实现细节
~~~~~~~~~~~~~~~~~~~~~~

基于 IO 扩展器的实现提供以下回调：

-  ``initialize``：将 SCL 和 SDA 引脚配置为开漏输出
-  ``set_scl/set_sda``：控制引脚输出值
-  ``get_scl/get_sda``：读取当前引脚状态（用于时钟拉伸检测）

驱动自动管理 IO 扩展器引脚状态，并根据 I2C 规范处理位操作协议时序。


========================
I2C 从设备驱动
========================

-  ``include/nuttx/i2c/i2c_slave.h``
   声明所有宏、操作和 ``int i2c_slave_register``，用于将下半部分驱动绑定到上半部分驱动并注册 I2C 从设备。

-  **绑定 I2C 从设备驱动**。在您的 BSP 中使用 ``int i2c_slave_register`` 注册从设备。在此之前，您需要从硬件特定的 I2C 从设备驱动获取 ``struct i2c_slave_s`` 的实例。

-  **在应用程序中使用 I2C 从设备**。I2C 从设备驱动通常由用户代码直接访问，我们可以使用 POSIX 接口对设备节点进行读写操作。设备注册为 ``/dev/i2cslv%d``，其中 ``%d`` 是在 BSP 初始化阶段提供的编号。

-  **BSP 初始化示例 (STM32 I2C Slave)**：

.. code-block:: c

   int stm32_i2cs_setup(void)
   {
      i2cs = stm32_i2cbus_slaveinitialize(1);
      if (i2cs != NULL)
        {
          return -ENOENT;
        }
      return i2c_slave_register(i2cs, 1, 0x01, 7);
   }

I2C 从设备驱动 API
--------------------

.. c:function:: int i2c_slave_register(FAR struct i2c_slave_s *dev, int bus, int addr, int nbit);

   将下半部分 ``dev`` 驱动绑定到上半部分驱动并注册设备。设备名称为 ``/dev/i2cslv%d``，其中 ``%d`` 是总线编号。I2C 从设备的地址在 ``addr`` 中指定。
   ``nbit`` 为 7 或 10，指定地址格式。


-  ``struct i2c_slaveops_s``。每个 I2C 从设备下半部分驱动必须实现
   ``struct i2c_slaveops_s`` 的一个实例。该结构定义了包含以下方法的调用表：

   - ``setownaddress``：从设备响应的地址，
   - ``write``：设置发送缓冲区指针，
   - ``read``：设置接收缓冲区指针，
   - ``registercallback``：注册回调函数，该函数应从服务例程中调用。发出接收到的或已完全传输的 I2C 数据包信号。
   - ``setup``：初始化外设，
   - ``shutdown``：关闭外设。
