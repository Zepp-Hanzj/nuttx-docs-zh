.. _chardev:

========================
字符设备驱动
========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

字符设备驱动程序具有以下属性：

-  ``include/nuttx/fs/fs.h``。此头文件提供了使用字符驱动程序所需的所有结构体和 API。

-  ``struct file_operations``。每个字符设备驱动程序必须实现一个 ``struct file_operations`` 实例。该结构定义了一个包含以下方法的调用表：

-  ``int register_driver(const char *path, const struct file_operations *fops, mode_t mode, void *priv);``。每个字符驱动程序通过调用 ``register_driver()`` 注册自身，传递其在 :ref:`伪文件系统 <file_system_overview>` 中出现的 ``path`` 以及已初始化的 ``struct file_operations`` 实例。

-  **用户访问**。注册后，用户代码可以使用标准驱动程序操作访问字符驱动程序，包括 ``open()``、``close()``、``read()``、``write()`` 等。

-  **专用字符驱动程序**。在通用字符驱动程序框架内，有不同种类的*专用*字符驱动程序。底层设备硬件的独特要求通常需要对字符驱动程序进行一些定制。这些定制通常采用以下形式：

   -  用于在设备上执行专用操作的设备特定 ``ioctl()`` 命令。这些 ``ioctl()`` 将在 ``include/nuttx`` 下的头文件中记录，详细说明特定设备接口。
   -  专用 I/O 格式。某些设备要求 ``read()`` 和/或 ``write()`` 操作使用符合特定格式的数据，而不是简单的字节流。这些专用 I/O 格式将在 ``include/nuttx`` 下的头文件中记录，详细说明特定设备接口。I/O 格式的典型表示是 C 结构定义。

   NuttX 支持的专用字符驱动程序将在以下段落中记录。

-  **示例**：``drivers/dev_null.c``、``drivers/fifo.c``、``drivers/serial.c`` 等。

.. toctree::
  :caption: 支持的驱动程序
  :maxdepth: 2

  1wire.rst
  analog/index.rst
  bch.rst
  can.rst
  contactless.rst
  crypto/index.rst
  eeprom.rst
  efuse.rst
  gpio.rst
  i2s.rst
  input/index.rst
  ipcc.rst
  leds/index.rst
  loop.rst
  math.rst
  modem.rst
  motor/index.rst
  note.rst
  nullzero.rst
  quadrature.rst
  rc.rst
  rf.rst
  serial.rst
  timers/index.rst
  touchscreen.rst
  wireless/index.rst
