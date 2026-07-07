==============
Device Drivers
==============

NuttX 支持多种设备驱动，大致可分为三类：

.. toctree::
  :maxdepth: 1

  character/index.rst
  block/index.rst
  special/index.rst
  thermal/index.rst

.. note::
  设备驱动支持依赖于默认启用的 *内存中*、*伪* 文件系统。

Lower-half and upper-half
=========================

NuttX 中的驱动通常分为两个不同的层次工作：

  * *上半部* 通过诸如 :c:func:`register_driver` 或 :c:func:`register_blockdriver` 之类的调用向 NuttX 注册自身，并实现相应的高级接口（`read`、`write`、`close` 等）。*上半部* 通过回调调用 *下半部*。
  * *下半部* 通常是硬件特定的。它通常在架构或板级实现。

有关驱动实现的详细信息，请参阅 :doc:`../../implementation/drivers_design` 和 :doc:`../../implementation/device_drivers`。

Subdirectories of ``nuttx/drivers``
===================================

* ``1wire/`` :doc:`character/1wire`

  1wire 设备驱动。

* ``analog/`` :doc:`character/analog/index`

  此目录包含模拟设备驱动的实现。包括模数转换 (ADC) 驱动和数模转换 (DAC) 驱动。

* ``audio/`` :doc:`special/audio`

  音频设备驱动。

* ``bch/`` :doc:`character/bch`

  包含可用于将块驱动转换为字符驱动的逻辑。这是 loop.c 执行的补充转换。

* ``can/`` :doc:`character/can`

  CAN 驱动和逻辑支持。

* ``clk/``:doc:`special/clk`

  时钟管理 (CLK) 设备驱动。

* ``contactless/`` :doc:`character/contactless`

  非接触式设备与无线设备相关。它们不是与其他同类对等设备通信的设备，而是与非接触式卡和标签的耦合器/接口。

* ``crypto/`` :doc:`character/crypto/index`

  包含加密驱动和支持逻辑，包括 ``/dev/urandom`` 设备。

* ``devicetree/`` :doc:`special/devicetree`

  设备树支持。

* ``dma/`` :doc:`special/dma`

  DMA 驱动支持。

* ``eeprom/`` :doc:`character/eeprom`

  以字符驱动方式支持 EEPROM。作为内存技术设备 (MTD) 的支持位于 ``mtd/`` 目录中。

* ``efuse/`` :doc:`character/efuse`

  EFUSE 驱动支持。

* ``i2c/`` :doc:`special/i2c`

  I2C 驱动和逻辑支持。

* ``i2s/`` :doc:`character/i2s`

  I2S 驱动和逻辑支持。

* ``i3c/`` :doc:`special/i3c`

  I3C 驱动和逻辑支持。

* ``input/`` :doc:`character/input/index`

  此目录包含人机输入设备 (HID) 驱动的实现。包括鼠标、触摸屏、操纵杆、键盘和键盘驱动等。

  请注意，USB HID 设备的处理方式不同。这些可以在 ``usbdev/`` 或 ``usbhost/`` 下找到。

* ``ioexpander/`` :doc:`special/ioexpander`

  IO 扩展器驱动。

* ``ipcc/`` :doc:`character/ipcc`

  IPCC（处理器间通信控制器）驱动。

* ``lcd/`` :doc:`special/lcd`

  并行和串行 LCD 及 OLED 类型设备的驱动。

* ``leds/`` :doc:`character/leds/index`

  各种 LED 相关驱动，包括离散 LED 和 PWM 驱动的 LED。

* ``loop/`` :doc:`character/loop`

  支持标准 loop 设备，可用于将文件（或字符设备）导出为块设备。

  参见 ``include/nuttx/fs/fs.h`` 中的 ``losetup()`` 和 ``loteardown()``。

* ``math/`` :doc:`character/math`

  MATH 加速驱动。

* ``misc/`` :doc:`character/nullzero` :doc:`special/rwbuffer` :doc:`block/ramdisk`

  其他不适合放在别处的各种驱动。

* ``mmcsd/`` :doc:`special/sdio` :doc:`special/mmcsd`

  MMC/SD 块驱动支持。支持基于 SPI 和 SDIO/MCI 接口的 MMC/SD 块驱动。

* ``modem/`` :doc:`character/modem`

  调制解调器支持。

* ``motor/`` :doc:`character/motor/index`

  电机控制驱动。

* ``mtd/`` :doc:`special/mtd/index`

  内存技术设备 (MTD) 驱动。一些用于 FLASH、EEPROM、NVRAM 等内存技术的简单驱动。

  （注意：这是一个简单的内存接口，不应与 infradead.org 开发的"真正的" MTD 混淆。该逻辑是无关的；我只是使用了 MTD 这个名称，因为我不知道还有其他通用方式来称呼这类设备）。

* ``net/`` :doc:`special/net/index`

  网络接口驱动。

* ``notes/`` :doc:`character/note`

  Note 驱动支持。

* ``pinctrl/`` :doc:`special/pinctrl`

  配置和管理引脚。

* ``pipes/`` :doc:`special/pipes`

  FIFO 和命名管道驱动。标准接口在 ``include/unistd.h`` 中声明。

* ``power/`` :doc:`special/power/index`

  与电源管理相关的各种驱动。

* ``rc/`` :doc:`character/rc`

  遥控设备支持。

* ``regmap/`` :doc:`special/regmap`

  Regmap 子系统支持。

* ``reset/`` :doc:`special/reset`

  复位驱动支持。

* ``rf/`` :doc:`character/rf`

  RF 设备支持。

* ``rptun/`` :doc:`special/rptun/index`

  远程处理器隧道驱动支持。

* ``segger/`` :doc:`special/segger`

  Segger RTT 驱动。

* ``sensors/`` :doc:`special/sensors`

  各种传感器的驱动。传感器驱动与其他类型的驱动差别不大，只是它们用于提供环境中事物的测量，如温度、方向、加速度、高度、方向、位置等。

  DAC 也可能符合传感器驱动的定义，因为它们测量和转换电压电平。但是，DAC 保留在 ``analog/`` 子目录中。

* ``serial/``:doc:`character/serial`

  芯片特定 UART 的前端字符驱动。提供类似 TTY 的功能，通常用于（但不是必须的）NuttX 系统控制台。

* ``spi/`` :doc:`special/spi`

  SPI 驱动和逻辑支持。

* ``syslog/`` :doc:`special/syslog`

  系统日志设备。

* ``timers/`` :doc:`character/timers/index`

  包括对各种定时器设备的支持。

* ``usbdev/`` :doc:`special/usbdev`

  USB 设备驱动。

* ``usbhost/`` :doc:`special/usbhost`

  USB 主机驱动。

* ``usbmisc/`` :doc:`special/usbmisc`

  USB 杂项驱动。

* ``usbmonitor/`` :doc:`special/usbmonitor`

  USB 监控支持。

* ``usrsock/`` :doc:`special/usrsock`

  Usrsock 驱动支持。

* ``video/`` :doc:`special/video`

  视频相关驱动。

* ``virtio/`` :doc:`special/virtio/index`

  Virtio 设备支持。

* ``wireless/`` :doc:`special/wireless`

  各种无线设备的驱动。

Skeleton Files
==============

Skeleton 文件是 NuttX 驱动的"空"框架。如果你想创建新的 NuttX 驱动，它们为你提供了一个良好的起点。以下 skeleton 文件可用：

* ``drivers/lcd/skeleton.c`` Skeleton LCD 驱动
* ``drivers/mtd/skeleton.c`` Skeleton 内存技术设备驱动
* ``drivers/net/skeleton.c`` Skeleton 网络/以太网驱动
* ``drivers/usbhost/usbhost_skeleton.c`` Skeleton USB 主机类驱动

Drivers Early Initialization
============================

为了在启动过程早期初始化驱动，引入了 :c:func:`drivers_early_initialize` 函数。这对某些驱动特别有益，例如 SEGGER SystemView，或其他在系统完全运行之前需要初始化的驱动。

需要注意的是，在此早期初始化阶段，系统资源尚不可使用。这包括内存分配、文件系统和任何其他系统资源。
