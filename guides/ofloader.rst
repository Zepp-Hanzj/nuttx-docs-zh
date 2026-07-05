=================
Open Flash Loader
=================

介绍
=========

Open Flash Loader 是 NuttX 中的一个实现，它在 NuttX 中的设备驱动与
J-Link 中的 flash loader 编程方法之间架起了桥梁。
它允许 J-Link 编程任何受支持的 NuttX 设备驱动。

配置
===============

.. code-block:: c

    CONFIG_DISABLE_IDLE_LOOP=y
    CONFIG_SYSTEM_OFLOADER=y
    CONFIG_SYSTEM_OFLOADER_TABLE="/dev/flash,0x08000000,0x20000",0

``CONFIG_DISABLE_IDLE_LOOP`` 用于禁用 NuttX 中的空闲循环。
``CONFIG_SYSTEM_OFLOADER`` 用于启用 Open Flash Loader。
``CONFIG_SYSTEM_OFLOADER_TABLE`` 用于配置 flash 设备，
第一个参数是设备名称，第二个参数是起始地址。

参考配置 "stm32f429i-disco:ofloader" 设计用于 NuttX 中的 STM32F429I-DISCO 开发板，
启用 Open Flash Loader 功能。此配置允许 J-Link flash loader 将 NuttX 镜像
编程到 STM32F429I-DISCO 开发板上。

用法
=====
1. 使用 Open Flash Loader 构建 NuttX。
2. 配置 JLink xml 文件。例如

.. code-block:: xml

    <Database>
        <Device>
            <ChipInfo Vendor="STM32NUTTX" Name="NuttX" Core="JLINK_CORE_CORTEX_M4" WorkRAMAddr="0x20000000" WorkRAMSize="0x10000000" />
            <FlashBankInfo Name="Storage" BaseAddr="0x00000000" MaxSize="0xffffffff" Loader="/home/ajh/work/vela_all/nuttx/nuttx" LoaderType="FLASH_ALGO_TYPE_OPEN" AlwaysPresent="1"/>
        </Device>
    </Database>

3. 使用 ``JLinkExe -if SWD -speed 4000 -device STM32NUTTX``，
   然后 ``loadbin /home/ajh/work/nuttx.bin 0x08000000``，
   我们就可以将 nuttx.bin 烧录到 /dev/flash

注意事项
===========

1. 如果你需要在不同的板子上实现 ofloader，
你需要阅读 `wiki <https://wiki.segger.com/SEGGER_Flash_Loader>`_
并参考 "boards/arm/stm32/stm32f429i-disco/scripts" 目录中的
"ofloader.ld" 链接器脚本的实现。
此链接器脚本定义了 NuttX 镜像的不同部分如何在内存中布局。
你应该配置相应的部分位于 RAM 中，
以便 J-Link 可以正确地写入镜像。

2. 运行 ofloader 时，J-Link 默认禁用任何中断。
因此，目前不支持使用中断驱动驱动的编程设备。

3. 由于 J-Link 的限制，ofloader 镜像文件不能超过 64KB。
在编程过程中必须注意此限制。

