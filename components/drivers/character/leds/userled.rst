===============
USERLED 驱动程序
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

USERLED 是 NuttX 中用于控制用户板上 LED 的子系统。使用它，应用程序可以单独或成组控制每个 LED。

有一个名为 "leds" 的应用程序可以测试板上的所有 LED（以二进制计数方式，逐个开启和关闭每个 LED）。

.. code-block:: bash

  NuttShell (NSH)
  nsh> leds
  nsh>
  leds_main: Starting the led_daemon
  leds main: led daemon started
  led_daemon: Running
  led_daemon: Opening /dev/userleds
  led_daemon: Supported LEDs 0xff
  led daemon: LED set 0x01
  led daemon: LED set 0x02
  led daemon: LED set 0x03
  led daemon: LED set 0x04
  led daemon: LED set 0x05

用户还可以使用 "nsh>" 中的 "printf" 命令以十六进制代码向 LED 发送数据来控制 LED：

.. code-block:: bash

  NuttShell (NSH)
  nsh> printf \\x000000a5 > /dev/userleds

此命令将开启映射到第 0、2、5 和 7 位的 LED。

需要注意的是，USERLED 和 ARCH_LEDS 不能同时工作，因此要使用 USERLED，请禁用 CONFIG_ARCH_LEDS。

NuttX USERLED 驱动程序分为两部分：

#. "上半部分"（userled_upper.c），通用驱动程序，提供应用程序级别的通用接口，
#. "下半部分"（userled_lower.c），调用平台特定的板级函数（board_userled_initialize()、board_userled()、board_userled_all() 等）来实现 LED 的底层控制。

支持 USERLED 的文件可以在以下位置找到：

-  **接口定义**。NuttX USERLED 驱动程序的头文件位于 ``include/nuttx/leds/userled.h``。此头文件包含 USERLED 驱动程序的应用程序级别接口以及"上半部分"和"下半部分"驱动程序之间的接口。USERLED 模块使用标准字符驱动程序框架。
-  **"上半部分"驱动程序**。通用的"上半部分" USERLED 驱动程序位于 ``drivers/leds/userled_upper.c``。
-  **"下半部分"驱动程序**。USERLED 驱动程序的下半部分位于 ``drivers/leds/userled_lower.c``，板级特定函数的目录位于 ``boards/<arch>/<family>/<boardname>/src/<arch>_userleds.c``。

需要注意的重要一点是，您的板初始化代码（通常命名为 ``<arch>_bringup.c``）应调用注册驱动程序的函数。

对于 stm32f4discovery 板，此初始化代码位于 ``boards/arm/stm32/stm32f4discovery/src/stm32_bringup.c``，以下是负责初始化子系统的代码块：

.. code-block:: C

  #ifdef CONFIG_USERLED
    /* 注册 LED 驱动程序 */

    ret = userled_lower_initialize("/dev/userleds");
    if (ret < 0)
      {
        syslog(LOG_ERR, "ERROR: userled_lower_initialize() failed: %d\n", ret);
      }
  #endif


