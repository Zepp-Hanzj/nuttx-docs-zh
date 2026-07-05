===========
Semihosting
===========

概述
========

NuttX 支持多种类型的 semihosting（syslog、文件主机共享、poweroff 等）。本文档的重点是 syslog 和文件共享，因为这些是将 NuttX 移植到新平台或测试需要主机文件（例如播放音频文件）时最常用的功能。

Semihosting SYSLOG
------------------

此功能非常有价值，特别是在移植到新芯片的过程中。它允许开发人员在早期初始化阶段跟踪事件和诊断问题，即使 UART 驱动支持尚未实现。此外，当没有可用的物理串口进行监控时，它可作为关键的调试工具。

以下是在 stm32f4discovery 板上使 semihost syslog 工作的步骤，但也可以适用于其他板子：

1. 使用 nsh 配置文件选择 stm32f4discovery 板：

.. code-block:: console

    $ ./tools/configure.sh stm32f4discovery:nsh
      Copy files
      Select CONFIG_HOST_LINUX=y
      Refreshing...

2. 运行 menuconfig 以选择必要的选项：

.. code-block:: console

    $ make menuconfig

3. 启用通过 syslog semihost 显示的调试选项（我们希望查看内存分配）：

.. code-block:: text

    Build Setup  --->
        Debug Options  --->
            [*] Enable Debug Features
            [*]   Enable Error Output (NEW)
            [*]     Enable Warnings Output (NEW)
            [*]       Enable Informational Debug Output (NEW)
            ...
            [*]   Memory Manager Debug Features
            [*]     Memory Manager Error Output 
            [*]     Memory Manager Warnings Output 
            [*]     Memory Manager Informational Output 

4. 启用 semihost syslog 支持：

.. code-block:: text

    System Type  --->
        [*] Semihosting SYSLOG support

5. 我们需要禁用 /dev/console，否则将调用串口初始化：

.. code-block:: text

    RTOS Features  --->
        Files and I/O  --->
            [ ] Enable /dev/console (disable the /dev/console)

6. 禁用串口驱动并启用 syslog 缓冲区以加速输出：

.. code-block:: text

    Device Drivers  --->
        [ ] Serial Driver Support  ---- (disable serial driver)
    
        System Logging  ---> 
            [*] Use buffered output

7. 保存并退出 menuconfig。

8. 编译固件：

.. code-block:: console

    $ make -j

9. 将固件烧录到板子：

.. code-block:: console

    $ sudo openocd -f interface/stlink.cfg -f target/stm32f4x.cfg -c init -c "reset halt" -c "flash write_image erase nuttx.bin 0x08000000"

10. 启动 openocd 服务器以等待 GDB 连接：

.. code-block:: console

    $ sudo openocd -f interface/stlink.cfg -f target/stm32f4x.cfg -c init -c "reset halt"
    Open On-Chip Debugger 0.12.0
    Licensed under GNU GPL v2
    For bug reports, read
      http://openocd.org/doc/doxygen/bugs.html
    Info : auto-selecting first available session transport "hla_swd". To override use 'transport select <transport>'.
    Info : The selected transport took over low-level target control. The results might differ compared to plain JTAG/SWD
    Info : clock speed 2000 kHz
    Info : STLINK V2J14S0 (API v2) VID:PID 0483:3748
    Info : Target voltage: 3.202097
    Info : [stm32f4x.cpu] Cortex-M4 r0p1 processor detected
    Info : [stm32f4x.cpu] target has 6 breakpoints, 4 watchpoints
    Info : starting gdb server for stm32f4x.cpu on 3333
    Info : Listening on port 3333 for gdb connections
    [stm32f4x.cpu] halted due to breakpoint, current mode: Thread 
    xPSR: 0x01000000 pc: 0x08004b68 msp: 0x200016b0
    [stm32f4x.cpu] halted due to debug-request, current mode: Thread 
    xPSR: 0x01000000 pc: 0x0800052c msp: 0x200017f0
    Info : Listening on port 6666 for tcl connections
    Info : Listening on port 4444 for telnet connections

11. 打开另一个终端，进入你编译 nuttx 的同一目录，运行 GDB 并传入 ELF 文件 (nuttx)

.. code-block:: console

    $ gdb-multiarch -ex "set architecture arm" nuttx
    GNU gdb (Ubuntu 15.0.50.20240403-0ubuntu1) 15.0.50.20240403-git
    Copyright (C) 2024 Free Software Foundation, Inc.
    ...
    Reading symbols from nuttx...
    The target architecture is set to "arm".
    
    (gdb) target extended-remote 127.0.0.1:3333
    Remote debugging using 127.0.0.1:3333
    0x0800052c in start ()
    
    (gdb) monitor arm semihosting enable
    semihosting is enabled
    
    (gdb) monitor arm semihosting_fileio enable
    semihosting fileio is enabled
    
    (gdb) monitor reset halt
    [stm32f4x.cpu] halted due to debug-request, current mode: Thread 
    xPSR: 0x01000000 pc: 0x0800052c msp: 0x200017f0, semihosting fileio
    
    (gdb) c
    Continuing.
    mm_initialize: Heap: name=Umem, start=0x200017f0 size=124944
    mm_addregion: [Umem] Region 1: base=0x20001960 size=124576
    mm_malloc: Allocated 0x20001970, size 72
    mm_malloc: Allocated 0x200019b8, size 40
    mm_addregion: [Umem] Region 2: base=0x10000000 size=65536
    mm_malloc: Allocated 0x10000010, size 48
    mm_malloc: Allocated 0x10000040, size 48
    mm_malloc: Allocated 0x10000070, size 48
    mm_malloc: Allocated 0x100000a0, size 24
    mm_malloc: Allocated 0x100000b8, size 16
    mm_malloc: Allocated 0x100000c8, size 32
    mm_malloc: Allocated 0x100000e8, size 208
    mm_malloc: Allocated 0x100001b8, size 2056
    mm_malloc: Allocated 0x100009c0, size 48
    mm_malloc: Allocated 0x100009f0, size 896
    mm_malloc: Allocated 0x10000d70, size 32
    mm_malloc: Allocated 0x10000d90, size 16
    mm_malloc: Allocated 0x10000da0, size 2056
    mm_free: Freeing 0x100001b8
    mm_free: Freeing 0x100000e8
    mm_malloc: Allocated 0x100000e8, size 768
    mm_free: Freeing 0x100000e8
    mm_free: Freeing 0x10000d90
    mm_free: Freeing 0x10000d70
    mm_free: Freeing 0x10000da0
    mm_free: Freeing 0x100009f0

Semihosting 文件
-----------------

相关文件：

.. code-block:: bash

    fs/hostfs/
    arch/arm/include/armv7-m/syscall.h
    arch/arm/src/common/up_hostfs.c

挂载：

.. code-block:: bash

    mount -t hostfs -o fs=/host/path /local/path
