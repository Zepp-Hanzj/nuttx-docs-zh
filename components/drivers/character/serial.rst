=====================
串行设备驱动程序
=====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

-  ``include/nuttx/serial/serial.h``。此头文件提供了使用串行驱动程序所需的所有结构和 API。

-  ``struct uart_ops_s``。每个串行设备驱动程序必须实现一个 ``struct uart_ops_s`` 实例。该结构体定义了一个包含以下方法的调用表：

-  ``int uart_register(FAR const char *path, FAR uart_dev_t *dev);``。串行驱动程序可以通过调用 ``uart_register()`` 注册自身，传入其在 :ref:`伪文件系统 <file_system_overview>` 中出现的 ``path`` 和已初始化的 ``struct uart_ops_s`` 实例。按照惯例，串行设备驱动程序注册在 ``/dev/ttyS0``、``/dev/ttyS1`` 等路径。参见 ``drivers/serial.c`` 中的 ``uart_register()`` 实现。

-  **TTY_LAUNCH** 这取决于 ``CONFIG_TTY_LAUNCH``，此功能允许用户通过特殊字符输入启动新程序。

   例如：使用 ctrl+R 启动 NuttX shell。
   例如：使用 ctrl+E 启动用户条目。

   您可以使用 ``TTY_LAUNCH_CHAR`` 自定义特殊字符。

   您可以选择启动方式：
   ``TTY_LAUNCH_ENTRY`` 或 ``TTY_LAUNCH_FILE``，
   如果使用 ``TTY_LAUNCH_ENTRY``，您可以通过 ``TTY_LAUNCH_ENTRYPOINT`` 设置程序入口。
   如果使用 ``TTY_LAUNCH_FILE``，您可以通过 ``TTY_LAUNCH_FILEPATH`` 设置文件路径。

   此外，您可以自定义：
   ``TTY_LAUNCH_ARGS`` ``TTY_LAUNCH_PRIORITY`` ``TTY_LAUNCH_STACKSIZE``

-  **用户访问**。串行驱动程序本质上是普通的 `字符驱动程序 <#chardrivers>`__，与其他字符驱动程序的访问方式相同。

-  **示例**：``arch/arm/src/stm32/stm32_serial.c``、``arch/arm/src/lpc214x/lpc214x_serial.c``、``arch/z16/src/z16f/z16f_serial.c`` 等。

串行错误报告
----------------------

可以使用 TIOCGICOUNT ioctl 检查是否存在帧错误、奇偶校验错误、溢出错误、中断错误或其他错误，就像在 Linux 中一样。

串行调试结构体 (TIOCSERGSTRUCT)
---------------------------------------

.. note::
   这是一个**仅用于调试**的 ioctl。它暴露的内部结构体是驱动程序特定的，可能随时更改，不能作为稳定的 ABI 使用。

``TIOCSERGSTRUCT`` ioctl 允许开发人员检索串行驱动程序内部状态结构体的副本，用于诊断和调试目的。它定义在 ``include/nuttx/serial/tioctl.h`` 中：

   #define TIOCSERGSTRUCT  _TIOC(0x0032)  /* Get device TTY structure */

启用 ``TIOCSERGSTRUCT``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

支持由 Kconfig 选项 ``CONFIG_SERIAL_TIOCSERGSTRUCT`` 控制。要启用它：

1. 必须启用 ``CONFIG_DEBUG_FEATURES``（该选项依赖于它）。
2. ``CONFIG_MCU_SERIAL`` 或 ``CONFIG_16550_UART`` 必须处于活动状态（即板必须使用 MCU 串行驱动程序或通用 16550 UART 驱动程序）。
3. 您硬件的特定低级串行驱动程序必须在其 ``ioctl`` 方法中实现 ``TIOCSERGSTRUCT`` 情况。树中的大多数串行驱动程序已经实现了（跨 ARM、ARM64、RISC-V、Xtensa 和 MIPS 架构的 63+ 个驱动程序）。

通过 ``menuconfig``，导航到：

.. code-block:: text

   Device Drivers  --->
     Serial Driver Support  --->
       [*] Support TIOCSERGSTRUCT

如果该选项不可见，请先确保已启用 ``CONFIG_DEBUG_FEATURES``。

工作原理
~~~~~~~~~~~~

由于确切的布局取决于为您的板选择的串行驱动程序，因此没有单一的可移植结构体定义。调用者必须查阅驱动程序源代码以获取结构体定义并相应地调整缓冲区大小。

如果 ``arg`` 为 ``NULL``，ioctl 返回 ``-EINVAL``。

使用示例
~~~~~~~~~~~~~

以下示例展示了应用程序如何使用 ``TIOCSERGSTRUCT`` 与 16550 UART 驱动程序来检查内部状态。请根据您板上使用的串行驱动程序调整结构体类型和头文件。

.. code-block:: c

   #include <stdio.h>
   #include <fcntl.h>
   #include <unistd.h>
   #include <sys/ioctl.h>
   #include <nuttx/serial/tioctl.h>

   /* 包含驱动程序特定的头文件以获取结构体定义。
    * 此示例使用 16550 UART；请替换为定义您的板
    * 串行驱动程序状态结构体的头文件。
    */

   #include <nuttx/serial/uart_16550.h>

   int main(int argc, char *argv[])
   {
     struct u16550_s devstate;
     int fd;
     int ret;

     fd = open("/dev/ttyS0", O_RDONLY);
     if (fd < 0)
       {
         perror("open");
         return 1;
       }

     ret = ioctl(fd, TIOCSERGSTRUCT, (unsigned long)&devstate);
     if (ret < 0)
       {
         perror("ioctl TIOCSERGSTRUCT");
         close(fd);
         return 1;
       }

     /* 检查驱动程序内部字段以进行调试。字段名称
      * 特定于驱动程序；请查阅驱动程序源代码以获取
      * 结构体定义。
      */

     printf("UART base address: 0x%08lx\n",
            (unsigned long)devstate.uartbase);

     close(fd);
     return 0;
   }

.. warning::
   结构体布局和字段名称是每个驱动程序实现的内部细节，**可能在 NuttX 版本之间发生变化**。仅将此 ioctl 用于交互式调试和诊断——永远不要在生产应用程序逻辑中使用。
