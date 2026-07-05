==================
关于 Apache NuttX
==================

NuttX 是一个实时嵌入式操作系统 (RTOS)。其目标是：

* **小体积**
  可用于除最严格的微控制器环境之外的所有环境，重点面向小型到微型的深度嵌入式环境。

* **丰富的功能集**
  目标是提供大多数标准 POSIX 操作系统接口的实现，以支持深度嵌入式处理器的丰富多线程开发环境。

  非目标：提供类似 Linux 那样级别的操作系统功能并非本项目的目标。为了适配更小的 MCU，小体积必须比丰富的功能集更重要。但标准兼容性比小体积更重要。当然，忽略标准可以制造出更小的 RTOS。可以把 NuttX 想象成一个功能集大幅缩减的微型 Linux 兼容系统。

* **高度可扩展**
  从小型（8 位）到中等规模嵌入式（64 位）完全可扩展。通过以下方式实现功能丰富与可扩展性的平衡：众多小型源文件、从静态库链接、高度可配置、在可用时使用弱符号。

* **标准兼容**
  NuttX 致力于实现高度的标准兼容性。主要遵循的标准是 POSIX 和 ANSI 标准。对于这些标准未涵盖的功能或不适合深度嵌入式 RTOS 的功能（如 ``fork()``），采用了来自 Unix 和其他常见 RTOS 的附加标准 API。

  由于这种标准兼容性，在其他标准操作系统（如 Linux）下开发的软件应能轻松移植到 NuttX。

* **实时性**
  完全可抢占；支持固定优先级、轮询和"零星"调度。

* **完全开放**
  无限制的 Apache 许可证。

* **GNU 工具链**
  基于 `buildroot <http://buildroot.uclibc.org/>`__ 的兼容 GNU 工具链可供 `下载 <https://bitbucket.org/nuttx/buildroot/downloads/>`__，为多种架构提供完整的开发环境。

特性集
===========

NuttX 的主要特性包括：

* **符合标准的核心任务管理**

  * 完全可抢占。
  * 自然可扩展。
  * 高度可配置。
  * 易于扩展到新的处理器架构、SoC 架构或板级架构。 :doc:`/reference/os/index` 可用。
  * FIFO 和轮询调度。
  * 实时、确定性，支持优先级继承
  * 无滴答操作
  * 类 POSIX/ANSI 任务控制、命名消息队列、计数信号量、时钟/定时器、信号、线程、健壮互斥锁、取消点、环境变量、文件系统。
  * 标准默认信号操作（可选）。
  * 类 VxWorks 任务管理和看门狗定时器。
  * BSD 套接字接口。
  * 预抢占管理扩展。
  * 带地址环境的可选任务（*进程*）。
  * 可加载内核模块；轻量级嵌入式共享库。
  * 内存配置：（1）平铺嵌入式构建，（2）带 MPU 的保护构建，（3）带 MMU 的内核构建。
  * 内存分配器：（1）标准堆内存分配，（2）粒度分配器，（3）共享内存，（4）动态大小的进程堆。
  * 可继承的"控制终端"和 I/O 重定向。
  * 伪终端
  * 按需分页。
  * 系统日志。
  * 可构建为开放的平铺嵌入式 RTOS，或构建为独立构建的、安全的、带有系统调用接口的单体内核。
  * 内置的逐线程 CPU 负载测量。
  * 在 NuttX 用户指南中有详细文档。

* **文件系统**

  * 小型内存中的根伪文件系统。
  * 虚拟文件系统 (VFS) 支持驱动程序和挂载点。
  * 可挂载卷。绑定挂载点、文件系统和块设备驱动程序。
  * 通用系统日志 (SYSLOG) 支持。
  * FAT12/16/32 文件系统支持，可选 FAT 长文件名支持1。
  * NFS 客户端。网络文件系统 (NFS, 版本 3, UDP) 客户端支持。
  * NXFFS。NuttX 小型磨损均衡 FLASH 文件系统。
  * SMART。Ken Pettit 的 FLASH 文件系统。
  * SPIFFS。FLASH 文件系统，最初由 Peter Anderson 开发。
  * LittleFS。ARM mbed 的 FLASH 文件系统。
  * ROMFS 文件系统支持（支持 XIP）。
  * CROMFS（压缩 ROMFS）文件系统支持。
  * TMPFS RAM 文件系统支持。
  * BINFS 伪文件系统支持。
  * HOSTFS 文件系统支持（仅仿真模式）。
  * 联合文件系统 - 支持文件系统的组合和覆盖。
  * UserFS - 用户应用程序文件系统。
  * ``procfs/`` 伪文件系统支持。
  * :doc:`/components/binfmt` 支持以下格式：

    - 独立链接的 ELF 模块。
    - 独立链接的 :doc:`/components/nxflat` 模块。NXFLAT 是一种可以从文件系统 XIP 的二进制格式。
    - "内置"应用程序。

  * PATH 变量支持。
  * 通过 TFTP 和 FTP（``get`` 和 ``put``）、HTML（``wget``）和 Zmodem（``sz`` 和 ``rz``）进行文件传输。Intel HEX 文件转换。

    * FAT 长文件名支持可能受某些 Microsoft 专利限制。详见顶层 ``NOTICE`` 文件。

* **设备驱动程序**

  * 支持字符和块驱动程序以及专用驱动程序接口。
  * 完整 VFS 集成。异步 I/O (AIO)
  * 网络、USB（主机）、USB（设备）、串口、I2C、I2S、NAND、CAN、ADC、DAC、PWM、正交编码器、I/O 扩展器、无线、通用定时器和看门狗定时器驱动架构。
  * RAMDISK、管道、FIFO、``/dev/null``、``/dev/zero``、``/dev/random`` 和循环驱动程序。
  * 基于 SPI 或 SDIO 的 MMC/SD/SDH 卡通用驱动程序。
  * 图形：帧缓冲驱动程序、图形和段式 LCD 驱动程序。VNC 服务器。
  * 音频子系统：CODEC、音频输入输出驱动程序。命令行和图形媒体播放器应用程序。
  * 加密子系统。
  * :doc:`/components/drivers/special/power/pm/index` 子系统。
  * 内置 `FreeModBus <https://www.embedded-experts.at/en/freemodbus/>`__ 1.5.0 版本提供 ModBus 支持。

* **C/C++ 库**

  * 标准 C 库完全集成到操作系统中。
  * 通过标准数学库提供浮点支持。
  * 附加 `uClibc++ <http://cxx.uclibc.org/>`__ 模块提供标准 C++ 库 (LGPL)。

* **网络**

  * 多网络接口支持；多网络链路层支持。
  * IPv4、IPv6、TCP/IP、UDP、ICMP、ICMPv6、IGMPv2 和 MLDv1/v2（客户端）协议栈。
  * IP 转发（路由）支持。
  * 用户空间协议栈。
  * 流和数据报套接字。
  * 地址族：IPv4/IPv6（``AF_INET``/``AF_INET6``）、原始套接字（``AF_PACKET``）、原始 IEEE 802.15.4（``AF_IEEE802154``）、原始蓝牙（``AF_BLUETOOTH``）、本地 Unix 域套接字支持（``AF_LOCAL``）。
  * 特殊 ``INET`` 协议套接字：原始 ICMP 和 ICMPv6 协议 ping 套接字（``IPPROTO_ICMP``/``IPPROTO_ICMP6``）。
  * 自定义用户套接字。
  * IP 转发。
  * DNS 名称解析 / NetDB
  * IEEE 802.11 FullMac
  * 无线网络驱动程序：IEEE 802.15.4 MAC、通用分组无线电、蓝牙 LE
  * 无线网络驱动程序的 6LoWPAN（IEEE 802.15.4 MAC 和通用分组无线电）
  * SLIP、TUN/PPP、本地回环设备
  * cJSON 移植
  * 小体积。
  * BSD 兼容的套接字层。
  * 网络实用程序（DHCP 服务器和客户端、SMTP 客户端、Telnet 服务器和客户端、FTP 服务器和客户端、TFTP 客户端、HTTP 服务器和客户端、PPPD、NTP 客户端）。可继承的 TELNET 服务器会话（作为"控制终端"）。VNC 服务器。
  * ICMPv6 自主自动配置
  * NFS 客户端。网络文件系统 (NFS, 版本 3, UDP) 客户端支持。
  * Jeff Poskanzer 的 `THTTPD <http://acme.com/software/thttpd>`__ HTTP 服务器的 NuttX 移植，与 NuttX :doc:`/components/binfmt` 集成，提供真正的嵌入式 CGI。
  * PHY 链路状态管理。
  * UDP 网络发现（由 Richard Cochran 贡献）。
  * XML RPC 服务器（由 Richard Cochran 贡献）。
  * 支持网络模块（例如 ESP8266）。

* **FLASH 支持**

  * *MTD* 启发的 *M* emory *T* echnology *D* evices 接口。
  * NAND 支持。
  * *FTL*。简单的 *F* lash *T* ranslation *L* ayer 支持 FLASH 上的文件系统。
  * 磨损均衡 FLASH 文件系统：NXFFS、SmartFS、SPIFFS。
  * 支持基于 SPI 的 FLASH 和 FRAM 设备。

* **USB 主机支持**

  * 用于 USB 主机控制器驱动程序和设备相关 USB 类驱动程序的 USB 主机架构。
  * Atmel SAMA5Dx、NXP LPC17xx、LPC31xx 和 STmicro STM32 的 USB 主机控制器驱动程序。
  * 适用于 USB 大容量存储、CDC/ACM 串口、HID 键盘和 HID 鼠标的设备相关 USB 类驱动程序。
  * 无缝支持 USB 集线器。

* **USB 设备支持**

  * 类 *Gadget* 架构，用于 USB 设备控制器驱动程序和设备相关 USB 类驱动程序。
  * 适用于大多数 MCU 架构的 USB 设备控制器驱动程序，包括 PIC32、Atmel AVR、SAM3、SAM4、SAMv7、SAMA5Dx、NXP/Freescale LPC17xx、LPC214x、LPC313x、LPC43xx、Kinetis、Silicon Laboratories EFM32、STMicro STM32 F1/F2/F3/F4/F7、TI DM320 等。
  * 适用于 USB 串口（CDC/ACM 和 PL2303 模拟）、USB 大容量存储、USB 网络（RNDIS 和 CDC/ECM）、DFU 和动态可配置复合 USB 设备的设备相关 USB 类驱动程序。
  * 内置 :doc:`/guides/usbtrace` 和 USB 主机跟踪功能，用于非侵入式 USB 调试。

* **图形支持**

  * 帧缓冲驱动程序。
  * 适用于并行和 SPI LCD 及 OLED 的图形 LCD 驱动程序。
  * 段式 LCD 驱动程序。
  * VNC 服务器。
  * 可 ``mmap`` 的帧缓冲字符驱动程序。
  * NX：图形库、小型窗口系统和小型字体支持，可与帧缓冲或 LCD 驱动程序配合使用。详见 :doc:`/components/nxgraphics/index` 手册。
  * 字体管理子系统。
  * :doc:`/applications/graphics/nxwidgets/index`：NXWidgets 是图形对象或"小部件"库（标签、按钮、文本框、图像、滑块、进度条等）。NXWidgets 使用 C++ 编写，与 NuttX NX 图形和字体管理子系统无缝集成。
  * NxWM 是基于 NX 和 NxWidgets 的小型 NuttX 窗口管理器。

* **输入设备**

  * 触摸屏、USB 键盘、基于 GPIO 的按钮和键盘。

* **模拟设备**

  * 支持模数转换 (ADC)、数模转换 (DAC)、多路复用器和放大器。

* **电机控制**

  * 脉宽调制 (PWM) / 脉冲计数调制。

* **NuttX 附加组件**
  以下软件包可用于扩展基本 NuttX 功能集：

  * **NuttShell (NSH)**
    一个小型、可扩展、类似 bash 的 NuttX shell，功能丰富且体积小巧。详见 :doc:`/applications/nsh/index`。
  * **BAS 2.4**
    Michael Haardt 的 BAS 2.4 无缝集成："Bas 是经典 BASIC 编程语言方言的解释器。它与 1980 年代的典型 BASIC 解释器非常兼容，不像其他 UNIX BASIC 解释器那样实现不同的语法，破坏了与现有程序的兼容性。Bas 提供了许多用于结构化编程的 ANSI BASIC 语句，如过程、局部变量和各种循环类型。此外还有矩阵操作、自动 LIST 缩进以及许多在特定经典方言中出现的语句和函数。行号不是必需的。"

看看所有这些文件和功能……它怎么能是一个小型操作系统？
================================================================

NuttX 的功能列表（如上）相当长，如果你查看 NuttX 源代码树，你会看到有数百个源文件构成了 NuttX。NuttX 怎么能拥有所有这些却仍然是一个小型操作系统呢？

  * **功能丰富——更多可以更小！**

    NuttX 的理念是功能丰富很好……*但*如果你不使用这些功能，就不应该为未使用的功能付出代价。在 NuttX 中，你不需要！如果你不使用某个功能，它就不会被包含在最终的可执行二进制文件中。你只需为你实际使用的功能付出体积增加的代价。

    使用多种技术，NuttX 可以从非常小的系统扩展到中等规模的系统。NuttX 曾在仅 32K *总*内存（代码和数据）中运行一些简单应用程序。另一方面，典型的、功能丰富的 NuttX 构建需要大约 64K（如果使用所有功能，可能会达到 100K）。

  * **许许多多文件——更多真的更小！**

   你可能会被 NuttX 源代码树的规模吓到。有数百个源文件！这怎么能是一个小型操作系统呢？实际上，大量的文件是保持 NuttX 尽可能小且可扩展的技巧之一。大多数文件只包含一个函数。有时只是一个只有几行代码的小函数。为什么？

     - **静态库**。
       因为在 NuttX 构建过程中，目标文件被编译并保存到*静态库*（*归档*）中。然后，在链接可执行文件时，只有需要的目标文件才会从归档中提取并添加到最终的可执行文件中。通过拥有众多的小型源文件，可以确保不会执行的代码永远不会被包含在链接中。通过拥有众多的小型源文件，你有更好的粒度——如果你不使用那个只有几行代码的小函数，它就不会被包含在二进制文件中。

* **其他技巧**

  如上所述，使用众多的小型源文件和从静态库链接可以保持 NuttX 的大小。NuttX 中使用的其他技巧包括：

  - **配置文件**。

    在构建 NuttX 之前，你必须提供一个配置文件，指定你计划使用哪些功能，不使用哪些功能。此配置文件包含一长串设置，控制哪些内容被构建到 NuttX 中，哪些不被构建。有数百个这样的设置（参见 `配置变量文档 <https://cwiki.apache.org/confluence/display/NUTTX/Configuration+Variables?src=contextnavpagetreemode>`__ 获取不包括平台特定设置的部分列表）。这些众多的配置选项允许 NuttX 高度调优以满足尺寸要求。所有这些配置选项的缺点是它大大复杂化了 NuttX 的维护——但这是我的问题，不是你的。-

  - **弱符号**
    GNU 工具链支持*弱*符号，这也有助于保持 NuttX 的大小。弱符号可以防止目标文件被拉入链接，即使它们被源代码访问。仔细使用弱符号是将未使用的代码排除在最终二进制文件之外的另一个技巧。

