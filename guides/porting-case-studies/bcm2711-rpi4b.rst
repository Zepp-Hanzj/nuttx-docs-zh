移植到 BCM2711 (Raspberry Pi 4B)
========================================

此次移植是在 NuttX 内核 12.7.0 版本上完成的，由 Matteo Golin 贡献。

初始支持的 Pull Request 可在 `apache/nuttx/pull/15188
<https://github.com/apache/nuttx/pull/15188>`_ 找到。

该移植需要为新的芯片（BCM2711）和新的开发板编写支持代码。Matteo 在进行初始移植的过程中撰写了日志条目，
可在 `他的博客 <https://linguini1.github.io/blog/2024/12/25/nuttx-bcm2711.html>`_ 上找到。
以下内容是对移植过程的更简洁总结。

研究阶段
-----------

将开发板移植到 NuttX 的第一步是研究开发板以及 NuttX 的工作原理。

BCM2711 是一款基于四核 ARM Cortex A72 的 SoC，它同时支持 aarch64 和 32 位 ARM 架构。在此次移植中，
我只专注于 aarch64 的实现。我的第一步是确定 NuttX 内核中已经有哪些使用 aarch64 架构的开发板，
因为这为我移植这个新芯片和新开发板提供了一个起点。

我主要参考了 Lup Yuen Lee 撰写的关于将 NuttX 移植到 PinePhone（另一款基于 ARM Cortex-A 的设备）的博客文章。
这些文章列在 `这里 <https://github.com/lupyuen/pinephone-nuttx>`_。Lup 的文章让我了解了 NuttX 的启动过程，
以及 NuttX 中 aarch64 支持的哪些文件被引入了启动的构建过程。他还展示了如何使用 NuttX 的 UART 驱动结构
创建初始的 UART 驱动程序，从而使 NSH 能够在控制台上显示。

最后，我当然还需要 BCM2711 的数据手册，以便了解哪些寄存器可用于创建外设驱动程序。BCM2711 的数据手册
对 SoC 上的许多功能描述得并不十分详细，但它确实提供了足够的细节来设置中断并使 UART 正常工作。

添加到源代码树
-------------------------

为了使用 NuttX 构建系统编译我的代码，我需要将开发板和 BCM2711 芯片添加到 NuttX 的源代码树中。
这样，它就会作为可用配置出现在 ``tools/configure.sh`` 脚本中，我就可以通过 ``make menuconfig``
为其选择选项。

首先要做的是添加芯片，它位于 ``arch/arm64`` 目录下，因为它是一个 64 位 ARM SoC。
芯片目录必须在两个位置添加：``arch/arm/include/cxd32xx`` 和 ``arch/arm64/src/bcm2711``。
C 文件连同一些头文件放在 ``src`` 目录中，一些特定的头文件放在 ``include`` 目录中。

此外，为了使 BCM2711 作为受支持的芯片可见，我必须在 ``arch/arm64/Kconfig`` 中将其添加为一个选项。
为此，我复制了 Allwinner A64 的条目，因为这两个芯片非常相似。我需要更改一些字段
（例如，选择 ``ARCH_CORTEX_A72`` 而不是 ``ARCH_CORTEX_A53``），但根据 SoC 的相关信息，
这相对简单地完成了。我还需要指定 ``ARMV8A_HAVE_GICv2``，因为 BCM2711 使用的是该中断控制器。
``ARCH_HAVE_MULTICPU`` 因为它是四核的，``ARCH_USE_MMU`` 因为它有内存管理单元。

我现在还需要将 Raspberry Pi 4B 开发板添加到源代码树中。为此，我复制了 PinePhone 的开发板文件夹
（``boards/arm64/a64/pinephone``）并将其重命名为 ``raspberrypi-4b``。我还删除了该文件夹中
许多不适用于 Pi 4B 的文件，并将所有提到 PinePhone 的地方替换为 Raspberry Pi 4B
（在路径名和头文件包含保护中）。

然后我在 ``boards/Kconfig`` 中将 Pi 4B 添加到受支持的开发板列表中。为此，我只需要创建一个
名为 ``ARCH_BOARD_RASPBERRYPI_4B`` 的条目，并写明它依赖于 ``ARCH_CHIP_BCM2711``。
不需要额外的选项！在该文件的其他两个地方，我还必须添加一些指令以确保开发板的 Kconfig 能被正确找到。
这些指令在选择 Pi 4B 时将 ``ARCH_BOARD`` 设置为开发板目录名 \"raspberrypi-4b\"，
并在选择时 ``source`` 了 ``boards/arm64/bcm2711/raspberrypi-4b`` 下的 Kconfig。

该开发板的默认配置是从 PinePhone 的 NSH 配置复制而来的，我将其修改为使用正确的开发板名称、
芯片和硬件特定设置。它仍然是不完整的，因为还没有实际引导进入 NSH 的代码，但这是一个起点。

这基本上就是我让开发板在源代码树中显示为可用配置所需要的全部内容！

映射芯片
--------------------

要开始为 BCM2711 编写代码，我需要映射芯片。这包括寄存器地址和内存映射，这些都可以在 BCM2711 的
数据手册中找到。通过查看其他实现，寄存器地址通常被定义为 C 宏，并保存在
``arch/<architecture>/src/<chip>/hardware`` 下的头文件中。我也把它们放在了那里，
将不同组的所有寄存器映射定义在单独的文件中（即 ``bmc2711_i2c.h``、``bcm2711_spi.h`` 等）。

许多外设都有内存映射寄存器的分组，使用基地址加上从该地址到不同字段的偏移量来定义。
例如，两个 mini-SPI 外设具有相同的结构，每个有 12 个寄存器。我常见的这些宏的实现方式类似于：

.. code-block:: c

   #define BCM_AUX_SPI1_BASEADDR (BCM_AUX_BASEADDR + BCM_AUX_SPI1_OFFSET)

   #define BCM_AUX_SPI_CNTL0_REG_OFFSET (0x00) /* SPI control register 0 */
   /* ... more register offsets */

   /* This allows you to choose which SPI interface base address to get the register for. */

   #define BCM_AUX_SPI_CNTL0(base) ((base) + BCM_AUX_SPI_CNTL0_REG_OFFSET)

除了寄存器本身之外，我还包含了用于屏蔽寄存器中某些字段或设置某些值的宏。这使得代码在后续使用中
更不容易出错，因为从数据手册中复制长列表的字段和寄存器时产生的任何错误都可以在一个地方修改。

.. code-block:: c

   #define BCM_SPI_CNTL0_EN (1 << 11) /* Enable SPI interface */

除了寄存器之外，我还必须映射中断。这在 ``include/bcm2711/irq.h`` 中完成。我从数据手册中复制了
IRQ 编号，并将它们全部列为带名称的宏。我还必须定义 IRQ 的数量，在本例中为 216。
``MPID_TO_CORE(mpid)`` 宏是从另一个 arm64 实现中复制的。

.. code-block:: c

   #define NR_IRQS 216
   #define MPID_TO_CORE(mpid) (((mpid) >> MPIDR_AFF0_SHIFT) & MPIDR_AFFLVL_MASK)

   /* VideoCore interrupts */

   #define BCM_IRQ_VC_BASE 96
   #define BCM_IRQ_VC(n) (BCM_IRQ_VC_BASE + n)

   #define BCM_IRQ_VC_TIMER0 BCM_IRQ_VC(0)
   #define BCM_IRQ_VC_TIMER1 BCM_IRQ_VC(1)
   /* More interrupts ... */

最后是在 ``include/bcm2711/chip.h`` 文件中定义内存映射。我简单地完成了这项工作，因为我只在 4GB
版本的 BCM2711 上进行测试。RAM 从地址 0 开始，大约为 4GB 大小。其中 64 MB 保留用于内存映射 I/O，
所以我必须确保将其移除。我还为芯片定义了内核在内存中的加载地址。

.. code-block:: c

   #define CONFIG_RAMBANK1_ADDR (0x000000000)

   /* Both the 4GB and 8GB ram variants use all the size in RAMBANK1 */

   #if defined(CONFIG_RPI4B_RAM_4GB) || defined(CONFIG_RPI4B_RAM_8GB)
   #define CONFIG_RAMBANK1_SIZE GB(4) - MB(64)
   #endif /* defined(CONFIG_RPI4B_RAM_4GB) || defined(CONFIG_RPI4B_RAM_8GB) */

   /* Raspberry Pi 4B loads NuttX at this address */

   #define CONFIG_LOAD_BASE 0x480000

相同的加载地址必须在 Raspberry Pi 4B 内核的链接脚本中指定。该脚本告诉编译器如何在内存中布局内核代码
以及使用什么地址。我能够从 PinePhone 复制它，只需将加载地址更改为 ``0x480000``。

解决启动问题
---------------------

我想做的第一件事是确定 aarch64 已经完成了多少工作，以便我能更轻松地完成移植。在 Lup 的博客中，
他通过使用该核心启动 QEMU 的 aarch64 实例来测试对其核心类型（PinePhone 上的 ARM Cortex-A53）的支持。
我决定采用相同的方法，并能够在他的博客指导下成功使用 QEMU 在 ARM Cortex-A72 上启动。
这是一个很好的确认，表明我使用的硬件已经在 NuttX 中得到了支持，可以启动操作系统并使 NSH
通过 PL011 UART 接口正常工作。

我怎么强调都不为过，移植到这个芯片之所以变得如此容易，是因为我站在了巨人的肩膀上。
NuttX 的贡献者们已经编写了用汇编语言编写的启动脚本、定时器配置、中断处理程序以及
aarch64 架构中许多标准功能的驱动程序。由于他们，我不需要处理这些中的任何一个，
这确实减少了我需要阅读和理解的汇编代码量。除了在调试启动过程中写了一点汇编之外，
我几乎不需要编写任何汇编（我们稍后会讲到）。更不用说我有 Lup 写得很好的文章来指导我了。

为了编译和启动开发板，我必须为 ``g_mmu_config`` 添加定义，我对此感到困惑，最初只是留空
以便通过编译阶段。我还通过从使用相同控制器的 Allwinner 芯片复制来定义 GICv2 中断控制器的
``GICR_OFFSET`` 和 ``GICR_BASE`` 宏。在进一步阅读 Lup 的博客后，我了解到启动脚本有一个
``PRINT`` 宏，在启动过程的早期被调用，并且需要实现 ``up_lowputc`` 来向控制台打印输出。
这将是我需要实现的第一个功能。代码编译通过了，但当我启动 Pi 时，什么也没发生。

在尝试了各种方法并查看其他实现相当长一段时间后，我注意到许多人在早期打印函数中直接使用寄存器操作。
我决定也这样做，但不是打印（一个更复杂的操作），而是将一个 GPIO 引脚拉高。我能够用万用表测量并
确认 GPIO 确实被设置了，所以我知道 ``arm64_earlyprint_init`` 函数被调用了。
我的 UART 配置出了问题。

然后我尝试直接操作寄存器将文本 \"hi\" 放入 UART FIFO。当我再次启动时，这打印出来了，
但随后是一些乱码输出。看起来传递给打印函数的 ``char *`` 指针出现了乱码。通过在汇编启动脚本中
调用我的 ``arm64_lowputc`` 直接打印字符进行故障排除后，我发现如果将字符串声明为 static，
就可以从 C 定义中打印字符串。我还检查了构建生成的 ELF 文件，确认字符串位于 ``.rodata`` 中。
我怀疑我没有正确地将内核加载到内存中，某些地址出现了混乱。果然，我在链接脚本中将加载地址
定义为 ``0x80000`` 而不是 ``0x480000``。修复这个问题后，我就能正确看到启动消息了！

我在控制台中收到了以下消息：

.. code-block:: console

   ----gic_validate_dist_version: No GIC version detect
   arm64_gic_initialize: no distributor detected, giving up ret=-19
   _assert: Current Version: NuttX  12.6.0-RC0 6791d4a1c4-dirty Aug  4 2024 00:38:21 arm64
   _assert: Assertion failed panic: at file: common/arm64_fatal.c:375 task: Idle_Task process: Kernel 0x481418

我在从其他开发板复制内容时，不小心在配置文件中保留了 GICv3，将其更改为 GICv2 后解决了这个问题，
但又出现了一个新问题：

.. code-block:: console

   MESS:00:00:06.144520:0:----_assert: Current Version: NuttX  12.6.0-RC0 f81fb7a076-dirty Aug  4 2024 16:16:30 arm64
   _assert: Assertion failed panic: at file: common/arm64_fatal.c:375 task: Idle_Task process: Kernel 0x4811e4

在构建选项中启用所有调试输出后，变成了这样：

.. code-block:: console

   arm64_oneshot_initialize: cycle_per_tick 54000
   arm64_fatal_error: reason = 0
   arm64_fatal_error: CurrentEL: MODE_EL1
   arm64_fatal_error: ESR_ELn: 0xbf000002
   arm64_fatal_error: FAR_ELn: 0x0
   arm64_fatal_error: ELR_ELn: 0x48a458
   print_ec_cause: SError interrupt

这看起来像是一个未处理的中断，通过在内核代码中添加日志语句来缩小出错的行后，我发现这是由于自旋锁代码
导致的。``ldaxr`` 指令引发了异常，ARM 文档指出该指令只能在 MMU 启用后使用。然后我启用了 MMU
及其调试信息，得到了这个可爱的错误：

.. code-block:: console

   MESS:00:00:06.174977:0:----arm64_mmu_init: xlat tables:
   arm64_mmu_init: base table(L1): 0x4cb000, 64 entries
   arm64_mmu_init: 0: 0x4c4000
   arm64_mmu_init: 1: 0x4c5000
   arm64_mmu_init: 2: 0x4c6000
   arm64_mmu_init: 3: 0x4c7000
   arm64_mmu_init: 4: 0x4c8000
   arm64_mmu_init: 5: 0x4c9000
   arm64_mmu_init: 6: 0x4ca000
   init_xlat_tables: mmap: virt 4227858432x phys 4227858432x size 67108864x
   set_pte_table_desc:   
   set_pte_table_desc: 0x4cb018: [Table] 0x4c4000
   init_xlat_tables: mmap: virt 0x phys 0x size 1006632960x
   set_pte_table_desc:   
   set_pte_table_desc: 0x4cb000: [Table] 0x4c5000
   init_xlat_tables: mmap: virt 4718592x phys 4718592x size 192512x
   split_pte_block_desc: Splitting existing PTE 0x4c5010(L2)
   set_pte_table_desc:     
   set_pte_table_desc: 0x4c5010: [Table] 0x4c6000
   init_xlat_tables: mmap: virt 4911104x phys 4911104x size 81920x
   init_xlat_tables: mmap: virt 4993024x phys 4993024x size 65536x
   enable_mmu_el1: MMU enabled with dcache
   nx_start: Entry
   up_allocate_heap: heap_start=0x0x4d3000, heap_size=0x47b2d000
   mm_initialize: Heap: name=Umem, start=0x4d3000 size=1202900992
   mm_addregion: [Umem] Region 1: base=0x4d32a8 size=1202900304
   arm64_fatal_error: reason = 0
   arm64_fatal_error: CurrentEL: MODE_EL1
   arm64_fatal_error: ESR_ELn: 0x96000045
   arm64_fatal_error: FAR_ELn: 0x47fffff8
   arm64_fatal_error: ELR_ELn: 0x489d28
   print_ec_cause: Data Abort taken without a change in Exception level
   _assert: Current Version: NuttX  12.6.0-RC0 96be557b64-dirty Aug  5 2024 14:56:42 arm64
   _assert: Assertion failed panic: at file: common/arm64_fatal.c:375 task: Idle_Task process: Kernel 0x481a34
   up_dump_register: stack = 0x4d2e10
   up_dump_register: x0:   0x13                x1:   0x4d32c0
   up_dump_register: x2:   0xfe215040          x3:   0xfe215040
   up_dump_register: x4:   0x0                 x5:   0x0
   up_dump_register: x6:   0x1                 x7:   0xdba53f65cc808a8
   up_dump_register: x8:   0xc4276feb17c016ba  x9:   0xecbcfeb328124450
   up_dump_register: x10:  0xb7989dd7d34a1280  x11:  0x5ebf5f572386fdee
   up_dump_register: x12:  0x6f7c07d067f6e38   x13:  0x3f7b5adaf798b4d5
   up_dump_register: x14:  0xf3dffbe2e4cff736  x15:  0xd76b1c050c964ea0
   up_dump_register: x16:  0x6d6fa9cfeeb0eff8  x17:  0x1a051d808a830286
   up_dump_register: x18:  0x3f7b5adaf798b4bf  x19:  0x4d3000
   up_dump_register: x20:  0x47fffff0          x21:  0x4d32d0
   up_dump_register: x22:  0x47b2cd30          x23:  0x4d32a8
   up_dump_register: x24:  0x4d32b0            x25:  0x4806f4
   up_dump_register: x26:  0x2f56f66b2df71556  x27:  0x74ee6bbfb5d438f4
   up_dump_register: x28:  0x7ef57ab47b85f74f  x29:  0x9a7fa1cb06923003
   up_dump_register: x30:  0x489cf8          
   up_dump_register: 
   up_dump_register: STATUS Registers:
   up_dump_register: SPSR:      0x600002c5        
   up_dump_register: ELR:       0x489d28          
   up_dump_register: SP_EL0:    0x4d3000          
   up_dump_register: SP_ELX:    0x4d2f40          
   up_dump_register: TPIDR_EL0: 0x0               
   up_dump_register: TPIDR_EL1: 0x0               
   up_dump_register: EXE_DEPTH: 0x1                 

经过进一步调试，我确定 nsh 配置的 defconfig 中的 ``CONFIG_RAM_START`` 和 ``CONFIG_RAM_SIZE`` 宏
仍然是我从 PinePhone 复制时的值。我将它们设置为 Raspberry Pi 4B 的正确值，然后进展更大了！

.. code-block:: console

   MESS:00:00:06.211786:0:----irq_attach: In irq_attach
   irq_attach: before spin_lock_irqsave
   spin_lock_irqsave: me: 0
   spin_lock_irqsave: before spin_lock
   spin_lock: about to enter loop
   spin_lock: loop over
   spin_lock_irqsave: after spin_lock
   irq_attach: after spin_lock_irqsave
   irq_attach: before spin_unlock_irqrestore
   irq_attach: after spin_unlock_irqrestore
   arm64_serialinit: arm64_serialinit not implemented
   group_setupidlefiles: ERROR: Failed to open stdin: -38
   _assert: Current Version: NuttX  12.6.0-RC0 be262c7ad3-dirty Aug  5 2024 17:16:27 arm64
   _assert: Assertion failed : at file: init/nx_start.c:728 task: Idle_Task process: Kernel 0x48162c
   up_dump_register: stack = 0x4c0170
   up_dump_register: x0:   0x4c0170            x1:   0x0
   up_dump_register: x2:   0x0                 x3:   0x0
   up_dump_register: x4:   0x0                 x5:   0x0
   up_dump_register: x6:   0x3                 x7:   0x0
   up_dump_register: x8:   0x4c7468            x9:   0x0
   up_dump_register: x10:  0x4c7000            x11:  0x4
   up_dump_register: x12:  0x4b8000            x13:  0x4b7000
   up_dump_register: x14:  0x1                 x15:  0xfffffff7
   up_dump_register: x16:  0x48a654            x17:  0x0
   up_dump_register: x18:  0x1                 x19:  0x0
   up_dump_register: x20:  0x4ac181            x21:  0x4bf430
   up_dump_register: x22:  0x0                 x23:  0x4c0170
   up_dump_register: x24:  0x4c0170            x25:  0x2d8
   up_dump_register: x26:  0x240               x27:  0x4b7000
   up_dump_register: x28:  0xfdc3ed41d6862df6  x29:  0xbf8e8f7280a0100
   up_dump_register: x30:  0x481bf8          
   up_dump_register: 
   up_dump_register: STATUS Registers:
   up_dump_register: SPSR:      0x20000245        
   up_dump_register: ELR:       0x480230          
   up_dump_register: SP_EL0:    0x4c7000          
   up_dump_register: SP_ELX:    0x4c6e90          
   up_dump_register: TPIDR_EL0: 0x4bf430          
   up_dump_register: TPIDR_EL1: 0x4bf430          
   up_dump_register: EXE_DEPTH: 0x0               
   dump_tasks:    PID GROUP PRI POLICY   TYPE    NPX STATE   EVENT      SIGMASK          STACKBASE  STACKSIZE      USED   FILLED    COMMAND
   dump_tasks:   ----   --- --- -------- ------- --- ------- ---------- ---------------- 0x4c4000      4096       144     3.5%    irq
   dump_task:       0     0   0 FIFO     Kthread - Running            0000000000000000 0x4c5010      8176      1200    14.6%    Idle_Task
   
   CTRL-A Z for help | 115200 8N1 | NOR | Minicom 2.9 | VT102 | Offline | ttyUSB0

我们现在实际上进入了任务阶段！看起来 stdin 打开失败了，因为在我的 Mini-UART 驱动实现中，
``attach`` 和 ``ioctl`` 函数返回了 ``-ENOSYS``。暂时将其更改为 0 表示成功，让我们能够走得更远，
我可以看到 NSH 开始启动的迹象。

.. code-block:: console

   mm_initialize: Heap: name=Umem, start=0x4cc000 size=4222828544
   mm_addregion: [Umem] Region 1: base=0x4cc2a8 size=4222827856
   mm_malloc: Allocated 0x4cc2d0, size 144
   mm_malloc: Allocated 0x4cc360, size 80
   gic_validate_dist_version: GICv2 detected
   up_timer_initialize: up_timer_initialize: cp15 timer(s) running at 54.0MHz
   arm64_oneshot_initialize: oneshot_initialize
   mm_malloc: Allocated 0x4cc3b0, size 48
   arm64_oneshot_initialize: cycle_per_tick 54000
   uart_register: Registering /dev/console
   mm_malloc: Allocated 0x4cc3e0, size 80
   mm_malloc: Allocated 0x4cc430, size 80
   uart_register: Registering /dev/ttys0
   mm_malloc: Allocated 0x4cc480, size 80
   mm_malloc: Allocated 0x4cc4d0, size 80
   mm_malloc: Allocated 0x4cc520, size 80
   mm_malloc: Allocated 0x4cc570, size 32
   mm_malloc: Allocated 0x4cc590, size 64
   work_start_highpri: Starting high-priority kernel worker thread(s)
   mm_malloc: Allocated 0x4cc5d0, size 336
   mm_malloc: Allocated 0x4cc720, size 8208
   nxtask_activate: hpwork pid=1,TCB=0x4cc5d0
   nx_start_application: Starting init thread
   task_spawn: name=nsh_main entry=0x48b24c file_actions=0 attr=0x4cbfa0 argv=0x4cbf98
   mm_malloc: Allocated 0x4ce730, size 1536
   mm_malloc: Allocated 0x4ced30, size 64
   mm_malloc: Allocated 0x4ced70, size 32
   mm_malloc: Allocated 0x4ced90, size 8208
   nxtask_activate: nsh_main pid=2,TCB=0x4ce730
   lib_cxx_initialize: _sinit: 0x4ad000 _einit: 0x4ad000
   mm_malloc: Allocated 0x4d0da0, size 848
   mm_free: Freeing 0x4d0da0
   mm_free: Freeing 0x4ced70
   mm_free: Freeing 0x4ced30
   nxtask_exit: nsh_main pid=2,TCB=0x4ce730
   mm_free: Freeing 0x4ced90
   mm_free: Freeing 0x4ce730
   nx_start: CPU0: Beginning Idle Loop

看起来我们在等待一个从未发生的中断。这很奇怪，因为我的 Mini-UART 驱动有中断实现，而且看起来写得没有问题。
这花了几个小时的调试、从中断处理程序记录日志和转储寄存器值，但最终我确定 BCM2711 的数据手册实际上有一个错误，
TX 和 RX 中断字段在数据手册中是交换的。网上有一篇博客文章提到了 BCM2835 的这个问题，但看起来这个芯片也有同样的问题。
现在我们成功启动进入了 NSH！

到此时，移植被认为取得了成功，因为我能够启动进入 NSH 并成功运行 ``ostest`` 基准测试。
我继续编写了几个更多驱动程序的开始部分，比如 GPIO 驱动程序，但这完成了初始移植的要求，
也是最终提交的初始 Pull Request 中的大部分内容。
