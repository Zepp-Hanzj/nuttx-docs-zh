.. include:: /substitutions.rst
.. _drivers:

=======
驱动程序
=======

一些 NuttX 开发板对所有片上外设没有完全支持。如果您需要支持这些硬件，您将需要从另一个芯片移植驱动程序，或者自己编写一个。本节讨论如何做到这一点。

.. _drivers-porting:

移植驱动程序
================

通常，片上外设的支持存在于密切相关的芯片中，甚至是不同的系列或不同的制造商。许多芯片由来自 Cadence、Synopsys 等供应商许可的不同知识产权 (IP) 块组成。IP 块可能足够相似，可以使用另一个芯片的驱动程序而只需少量修改。

* 在 NuttX 源代码中找到类似的驱动程序：

  * 查看外设数据手册中列出的寄存器名称。
  * 在 NuttX 代码库中搜索寄存器名称（尝试几个不同的）。
  * 请注意，您需要将数据手册与头文件和代码文件进行比较，看看是否有差异；架构之间通常会有一些差异，而且可能很显著。

* 在 U-Boot、Zephyr 或 BSD Unix（OpenBSD、FreeBSD、NetBSD）源代码中找到类似的驱动程序：

  * 仅用于参考，您不能复制代码，因为许可证不兼容和 Apache 基金会的限制。
    （Apache License 2.0 和 BSD 代码可以通过原始作者的软件许可协议引入；这有时很难获得。如果不确定，请在邮件列表中询问。）
  * 但您可以调试以了解驱动程序的工作原理。
  * `U-Boot <https://www.denx.de/wiki/U-Boot>`_ 驱动程序通常比 BSD Unix 驱动程序更容易理解，因为 U-Boot 更简单。

* 理解驱动程序的工作原理

  以下是一些对我有帮助的技术。

    * printf 调试

      * 在代码中散布 ``custinfo()`` 日志语句以查看执行路径并在代码运行时查看变量。
        使用 ``custinfo()`` 而不是其他日志快捷方式（``mcinfo()`` 等）的原因是，您可以打开和关闭其他日志，同时仍然可以看到自定义调试日志。有时，静默来自特定调试日志快捷方式的大量日志很有用。
      * 请注意，将信息打印到控制台会影响时序。
      * 保留一个仅包含调试设置的文件，如下所示（``debugsettings``）：

        .. code-block:: c

           CONFIG_DEBUG_CUSTOM_INFO=y
           (etc..)

      * 在运行 ``make menuconfig`` 后将设置添加到 ``.config`` 文件末尾（该操作会重新排序文件，如果需要，会使查看和更改调试设置变得更加困难）。

        .. code-block:: bash

           $ cat .config debugsettings > .config1 ; mv .config1 .config

      * 如果您使用中断和线程（NuttX 中的许多操作作为对中断的响应在不同线程中运行），您可以使用 printf 调试来查看重叠执行。

        * 中断 - 以下是检查 C 堆栈帧以查看当前正在运行的执行环境的方法：

          .. code-block:: c
            uint32_t frame = 0;  /* MUST be the very first thing in the function */
            uint32_t p_frame;
            frame++;             /* make sure that frame doesn't get optimized out */
            p_frame = (uint32_t)(&frame);
            custinfo("p_frame: %08x\n", p_frame);

        * 线程 - 以下是获取线程标识符以查看当前正在执行哪个线程的方法：

          .. code-block:: c
            pthread_t thread_id = pthread_self();
            custinfo("pthread_id: %08x\n", thread_id);

      * 堆栈帧 printf
      * 线程 printf

    * `GDB — GNU 调试器 <https://www.gnu.org/software/gdb/>`_

      GDB 是一个很好的工具。在本指南中，我们已经用它来加载和运行程序。但它可以做更多的事情。您可以单步执行代码、检查变量和内存、设置断点等。我通常从命令行使用它，但也从 JetBrains 的 Clion 等 IDE 中使用过，在那里更容易看到代码上下文。

      我发现一个必不可少的附加功能是检查内存块的能力，例如 NuttX 用于读写存储介质或网络适配器的缓冲区。这个 `Stack Overflow 上关于使用 GDB 检查内存的问题 <https://stackoverflow.com/a/54784260/431222>`_ 包含一个非常方便的 GDB 命令。将其添加到您的 ``.gdbinit`` 文件中，然后使用 ``xxd`` 命令以易于阅读的格式转储内存：

      .. code-block::

         define xxd
           if $argc < 2
             set $size = sizeof(*$arg0)
           else
             set $size = $arg1
           end
           dump binary memory dump.bin $arg0 ((void *)$arg0)+$size
           eval "shell xxd -o %d dump.bin; rm dump.bin", ((void *)$arg0)
         end
         document xxd
           Dump memory with xxd command (keep the address as offset)

           xxd addr [size]
             addr -- expression resolvable as an address
             size -- size (in byte) of memory to dump
                     sizeof(*addr) is used by default end

      以下是简短的 GDB 会话，显示了实际效果。请注意，正在检查的内存位置（此处为 ``0x200aa9eo``）是传递给 ``mmcsd_readsingle`` 的缓冲区：

      .. code-block::
        Program received signal SIGTRAP, Trace/breakpoint trap.
        0x200166e8 in up_idle () at common/arm_idle.c:78
        78	}
        (gdb) b mmcsd_readsingle
        Breakpoint 1 at 0x2006ea70: file mmcsd/mmcsd_sdio.c, line 1371.
        (gdb) c
        Continuing.

        Breakpoint 1, mmcsd_readsingle (priv=0x200aa8c0, buffer=0x200aa9e0 "WRTEST  TXT \030", startblock=2432) at mmcsd/mmcsd_sdio.c:1371
        1371	  finfo("startblock=%d\n", startblock);
        (gdb) xxd 0x200aa9e0 200
        200aa9e0: 5752 5445 5354 2020 5458 5420 1800 0000  WRTEST  TXT ....
        200aa9f0: 0000 0000 0000 0000 0000 5500 1100 0000  ..........U.....
        200aaa00: 5752 5445 5354 3520 5458 5420 1800 0000  WRTEST5 TXT ....
        200aaa10: 0000 0000 0000 0000 0000 5800 1500 0000  ..........X.....
        200aaa20: e552 5445 5854 3620 5458 5420 1800 0000  .RTEXT6 TXT ....
        200aaa30: 0000 0000 0000 0000 0000 5600 1200 0000  ..........V.....
        200aaa40: 5752 5445 5354 3620 5458 5420 1800 0000  WRTEST6 TXT ....
        200aaa50: 0000 0000 0000 0000 0000 5600 1200 0000  ..........V.....
        200aaa60: 0000 0000 0000 0000 0000 0000 0000 0000  ................
        200aaa70: 0000 0000 0000 0000 0000 0000 0000 0000  ................
        200aaa80: 0000 0000 0000 0000 0000 0000 0000 0000  ................
        200aaa90: 0000 0000 0000 0000 0000 0000 0000 0000  ................
        200aaaa0: 0000 0000 0000 0000                      ........

NuttX 驱动程序作为参考
============================

如果您不是从另一个架构移植 NuttX 驱动程序，查看其他类似的 NuttX 驱动程序（如果有的话）仍然有帮助。例如，在实现以太网驱动程序时，查看其他 NuttX 以太网驱动程序；对于 SD 卡驱动程序，查看其他 NuttX SD 卡驱动程序。即使特定芯片的代码不同，与 NuttX 接口的结构也可以使用。

使用芯片数据手册
=====================

要移植或编写驱动程序，您需要熟悉芯片数据手册中的信息。一定要找到您的芯片数据手册，并阅读与您正在处理的外设相关的部分。提前这样做将节省很多时间。

另一个通常有帮助的是参考制造商提供的示例代码，或在参考数据手册的同时参考另一个操作系统（如 U-Boot、Zephyr 或 FreeBSD）的驱动程序代码——查看工作代码如何实现必要的算法通常有助于理解驱动程序需要如何工作。

* 如何使用数据手册

  片上系统 (SoC) 数据手册中的关键信息通常是：

  * 芯片架构图 - 显示芯片的子部分（CPU、系统总线、外设、I/O 等）如何相互连接。
  * 内存映射 - 显示外设寄存器在内存中的位置。此信息通常写入头文件。
  * DMA 引擎 - 如果使用直接内存访问 (DMA)，此处可能有使用说明。
  * 外设 - 数据手册通常有关于外设工作原理的章节。关键部分包括：

    * 寄存器列表 - 名称和外设基地址的偏移量。这需要写入头文件。
    * 寄存器映射 - 每个寄存器的大小是多少，位的含义是什么？您需要在头文件中创建 ``#defines``，您的代码将使用它们来操作寄存器。参考其他驱动程序头文件获取示例。

逻辑分析仪
===============

对于涉及输入和输出 (I/O) 的驱动程序，特别是涉及 SD 卡、SPI、I2C 等复杂协议的驱动程序，实际查看进出芯片引脚的波形非常有帮助。`逻辑分析仪 <https://en.wikipedia.org/wiki/Logic_analyzer>`_ 可以捕获该信息并以图形方式显示，让您查看驱动程序是否在总线上执行了正确的操作。

DMA 调试
=============

* 在传输之前、期间和之后转储寄存器。一些 NuttX 驱动程序（例如 ``sam_sdmmc.c`` 或 ``imxrt_sdmmc.c``）内置了调试寄存器状态的代码，可以在 DMA 传输之前、期间和之后立即采样寄存器，以及可以将外设寄存器以格式良好的方式转储到控制台设备（可以是串行控制台、网络控制台或内存）的代码。如果您尝试调试 DMA 传输代码，考虑使用类似的功能来查看芯片内部发生了什么。
* 将寄存器设置与从数据手册或从另一个操作系统（U-Boot、Zephyr、FreeBSD 等）中转储的工作代码确定的预期设置进行比较。
* 使用上面提到的 ``xxd`` GDB 工具在传输之前、期间和之后转储 NuttX 内存缓冲区，以查看数据是否正确传输、是否存在溢出或欠载，或诊断数据是否存储在错误的位置。
* printf 调试寄存器状态在此处也可能有帮助。
* 请记住，日志记录可能会更改您可能使用的任何算法的时序，因此在添加或删除日志记录时，功能可能会开始或停止工作。务必在禁用日志记录的情况下进行测试。

