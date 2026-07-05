===================================================================
使用硬件调试器 (JTAG/SWD) 在 ARM 上调试/烧录 NuttX
===================================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

.. warning:: 
    迁移自： 
    https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=139629444


注意：如果你遇到本页描述的问题，可以启用下面的配置选项来解决。

.. code-block:: makefile

    CONFIG_STM32_DISABLE_IDLE_SLEEP_DURING_DEBUG=y

问题是什么？
===================

在某些架构上（如 ARM Cortex-M3），空闲线程会使用 WFI（等待中断）汇编指令使核心停止。这实际上停止了核心的时钟，只有某些启用的中断才能恢复。这导致硬件调试器认为它们已与目标断开连接，因为它们失去了与已停止核心的连接。例如 OpenOCD 在你启动目标时就会显示如下错误：

.. code-block:: console

    Error: jtag status contains invalid mode value - communication failure
    Polling target failed, GDB will be halted. Polling again in 100ms
    Error: jtag status contains invalid mode value - communication failure
    Polling target failed, GDB will be halted. Polling again in 300ms
    Error: jtag status contains invalid mode value - communication failure
    Polling target failed, GDB will be halted. Polling again in 700ms
    Error: jtag status contains invalid mode value - communication failure
    Polling target failed, GDB will be halted. Polling again in 1500ms
    Error: jtag status contains invalid mode value - communication failure
    Polling target failed, GDB will be halted. Polling again in 3100ms
    Error: jtag status contains invalid mode value - communication failure
    Polling target failed, GDB will be halted. Polling again in 6300ms
    Error: jtag status contains invalid mode value - communication failure
    Polling target failed, GDB will be halted. Polling again in 6300ms


这使得调试代码变得不可能，烧录芯片也更加困难——你必须在正确的时刻连接到芯片（当它没有因 WFI 而禁用时）——这样做的机会与系统负载成反比（如果你的芯片 99% 的时间处于空闲模式，你只有 1% 的机会连接并暂停它）。

解决方案
========

一些支持在 WFI 指令后禁用时钟的 ARM 核心有特殊的配置选项来使调试成为可能。STM32 系列就是一个例子——通过其 ``DBGMCU->CR`` 寄存器，可以在掉电模式下保持核心时钟。如果你的芯片支持这种配置，你应该在初始化的早期阶段放置它，例如在 ``stm32_boardinitialize()`` 函数中。以下代码演示了 STM32 的更改：

.. code-block:: c

    uint32_t cr = getreg32(STM32_DBGMCU_CR);
    cr |= DBGMCU_CR_STANDBY | DBGMCU_CR_STOP | DBGMCU_CR_SLEEP;
    putreg32(cr, STM32_DBGMCU_CR);

如果你的芯片不提供这样的选项，除了不在 up_idle() 函数中使用 WFI 指令外别无他法。

应该注意，这种修改只应在开发阶段进行，因为在掉电模式下保持核心时钟与使用它们的主要目的——降低功耗——相矛盾。

在极少数情况下，如果你仍然有连接目标的问题（尤其是在电源循环后），你应该尝试在复位状态下连接和暂停芯片（新版本的 OpenOCD 支持此功能），通过在启动 OpenOCD 时按住复位按钮，或配置 OpenOCD 为你执行此操作。

变通方法
-----------

如果你按住 RESET 按钮并运行 OpenOCD 命令连接它，那么它将成功连接。连接后，你需要保持复位按钮按下，直到你打开 telnet 连接（telnet 127.0.0.1 4444）并执行 "reset halt"：

.. code-block:: console

    > reset halt
    timed out while waiting for target halted
    TARGET: stm32f1x.cpu - Not halted
      
    in procedure 'reset'
    target state: halted
    target halted due to debug-request, current mode: Thread
    xPSR: 0x01000000 pc: 0x080003d0 msp: 0x20001278

然后释放 RESET 按钮，它将正确复位。

此变通方法已在 viewtool-stm32f107 板上测试，并绕过了 OpenOCD 报告的上述错误。SWD 编程器是 STLink-V2，连接命令是：

.. code-block:: console

    openocd -f interface/stlink-v2.cfg -f target/stm32f1x_stlink.cfg

使用的 OpenOCD 版本是：Open On-Chip Debugger 0.8.0-dev-00307-g215c41c 
(git commit 215c41c)
