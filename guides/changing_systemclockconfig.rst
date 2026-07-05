=======================================
更改系统时钟配置
=======================================

.. warning:: 
    迁移自: 
    https://cwiki.apache.org/confluence/display/NUTTX/Changing+the+System+Clock+Configuration


问题
========
`STM32 配置是否可以使用内部 16 MHz 时钟启动，然后稍后（按命令）切换到外部 25 MHz 晶振？我认为不行，但您能确认一下吗？`

答案
======

当然可以，这始终是这样发生的：STM32 使用内部时钟启动，在启动后切换到外部晶振源。但我假设您指的是初始化之后很久。

是的，这也是可以做到的。只有几个问题和需要注意的事项：

自定义时钟配置
--------------------------

``configs/vsn/`` 配置做了类似您所说的事情。它通过定义 ``CONFIG_ARCH_BOARD_STM32_CUSTOM_CLOCKCONFIG=y`` 来跳过初始时钟配置。然后 ``arch/arm/src/stm32/stm32_rcc.c`` 中的正常时钟配置逻辑不会执行。取而代之的是调用 ``configs/vsn/src/sysclock.c`` 中的"自定义"时钟初始化：

.. code-block:: c

    void stm32_clockconfig(void)
    {
      /* Make sure that we are starting in the reset state */

      rcc_reset();

    #if defined(CONFIG_ARCH_BOARD_STM32_CUSTOM_CLOCKCONFIG)

      /* Invoke Board Custom Clock Configuration */

      stm32_board_clockconfig();

    #else

      /* Invoke standard, fixed clock configuration based on definitions in board.h */

      stm32_stdclockconfig();

    #endif

      /* Enable peripheral clocking */

      rcc_enableperipherals();
    }

通过这种方式，您可以完全控制何时使用晶振时钟源。初始"自定义"时钟配置可以使用内部源，然后其他自定义时钟配置逻辑可以在稍后更改时钟源。

注意：自本文最初编写以来，VSN 配置已被弃用，不再位于 config/vsn。弃用的代码仍可在 `Obsoleted 仓库 <https://bitbucket.org/patacongo/obsoleted/src/master/nuttx/configs/vsn>`_ 中找到。

外设时钟
-----------------

许多设备使用外设时钟来设置 SPI 频率和 UART 波特率等。目前，这些外设时钟频率在 board.h 头文件中硬编码。因此您有两个选择：

1. **固定外设时钟。** 理想情况下，您希望在两种情况下保持外设时钟频率相同。这样生活就简单了。您可能可以使用内部 RC 时钟源作为 PLL 的输入，并设置分频器以获得相同的外设时钟。那么，我认为，从外设的角度来看，什么都没发生。

2. **可变外设时钟。** 您可以使外设时钟可变。我不得不为 SAMA5Dx 系列这样做。参见 ``boards/arm/stm32/sama5d4-ek/include/board_sdram.h`` 示例。请注意，频率不是常量，而是函数调用：

.. code-block:: c

    #define BOARD_MAINCK_FREQUENCY     BOARD_MAINOSC_FREQUENCY
    #define BOARD_PLLA_FREQUENCY       (sam_pllack_frequency(BOARD_MAINOSC_FREQUENCY))
    #define BOARD_PLLADIV2_FREQUENCY   (sam_plladiv2_frequency(BOARD_MAINOSC_FREQUENCY))
    #define BOARD_PCK_FREQUENCY        (sam_pck_frequency(BOARD_MAINOSC_FREQUENCY))
    #define BOARD_MCK_FREQUENCY        (sam_mck_frequency(BOARD_MAINOSC_FREQUENCY))

鉴于我知道 XTAL 振荡器频率，我可以推导出其他时钟的频率。然而，这实际上比您想象的工作量要大，因为可能有一些 C 预处理器测试现在会失败。例如：

.. code-block:: c

    #if BOARD_MCK_FREQUENCY > 16000000
    ... do something ...
    #endif

此类逻辑必须从编译时决策转换为运行时决策，可能如下所示：

.. code-block:: c

    if (BOARD_MCK_FREQUENCY > 16000000)
    {
      ... do something ...
    }

SAMA5D4-EK 的情况适用于软件从 SDRAM 运行且无法重新配置时钟的情况。相反，它必须推导出引导加载程序留下的时钟配置。但您也可以在更改频率时做类似于 SAMA5D4-EK 的事情。您也可以使外设时钟可变。

重新初始化外设
--------------------------

可变外设时钟
----------------------------

如果您在更改频率时做了类似于 SAMA5D4-EK 的事情，那么外设时钟将是可变的。主要问题将是您必须在外设时钟更改时重新初始化外设。例如，如果 UART 在初始外设时钟下初始化，那么如果外设时钟更改，您将需要重新计算波特率分频器。

但这并不是一个大问题。您可以使用 TERMIOS ioctl 调用强制 UART 重新计算波特率分频器。您可以使用 setfrequency() 方法重新计算 I2C 和 SPI 波特率分频器。但还有存储卡频率等。

Systick 定时器
-------------

如果 CPU 频率更改，您需要更改 Systick 定时器配置：它始终由 CPU 时钟驱动

up_mdelay
---------

up_mdelay() 提供低级定时循环，必须对任何导致该定时循环执行速率变化的因素重新校准。此校准不是关键的，相当大的校准误差是可以容忍的。希望您可以保持执行速率足够接近，使 up_mdelay() 不会有严重错误。

电源管理
----------------

如果您想因电源管理原因切换时钟，这也是您需要做的同类事情。NuttX 确实有电源管理系统，也许利用电源管理系统来管理系统时钟更改是可能的。例如，当时钟更改时，您可以强制某些电源管理状态更改。该状态更改将通知所有驱动程序，作为响应，驱动程序可以重新计算其频率相关设置。

以下是一些电源管理文档：

.. toctree::
  :maxdepth: 1

  /components/drivers/special/power/pm/index.rst
