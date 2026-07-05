===========================
NSH 网络链路管理
===========================

.. warning:: 
    迁移自： 
    https://cwiki.apache.org/confluence/display/NUTTX/NSH+Network+Link+Management

过去，如果 NuttX 启动时网络未连接，可能会出现两个问题：

1. 由于顺序初始化，NSH 提示符可能需要很长时间才能出现
   （例如，当网络电缆未连接时）。
2. NuttX 启动后，插入网络电缆不会启用网络；
   恢复网络的唯一方法是连接电缆并重置目标板。

现在已向 NSH 添加了网络链路管理功能以解决这些问题。

配置选项
=====================

可以启用一个简单的功能，将网络初始化移到单独的线程中，
使其不再顺序执行。有了这个功能，网络启动异步发生，
NSH 提示符立即出现（尽管网络可能在一段时间后才可用）。
该功能通过以下设置启用，是完整 NSH 链路管理功能的第一个前提条件：

- ``CONFIG_NSH_NETINIT_THREAD``。请参阅此选项的 Kconfig 文件
  （``apps/nshlib/Kconfig``）中的帮助文本。那里包含了有关此设置的
  附加信息。

实现 NSH 网络管理的逻辑在 ``apps/nshlib/nsh_netinit.c`` 中提供。
该逻辑的行为取决于多个配置设置。首先，必须满足一些额外的前提条件：

- ``CONFIG_NETDEV_PHY_IOCTL``  
  在以太网设备驱动中启用 PHY IOCTL 命令。以太网驱动必须提供特殊的
  IOCTL 命令以支持链路管理所需的某些 PHY 操作。这些操作并不复杂，
  已为 Atmel SAM4/4、SAMA5 系列以及 STMicro STM32 实现。
  参见 ``nuttx/arch/arm/src/sam34/sam_emac.c``、
  ``nuttx/arch/arm/src/sam34/sam_emaca.c``、``sam_emacb.c`` 和 ``sam_gmac.c``，
  以及 ``nuttx/arch/arm/src/stm32/stm32_eth.c``。
- ``CONFIG_ARCH_PHY_INTERRUPT``  
  这不是用户可选择的选项。而是在选择支持 PHY 中断的板子时设置的。
  在大多数架构中，PHY 中断不直接与以太网驱动关联。相反，PHY 中断
  通过某些板特定的 GPIO 提供，板特定逻辑必须为该 GPIO 中断提供支持。
  具体来说，板逻辑必须：
  
  1. 提供 ``nuttx/include/nuttx/arch.h`` 中描述和声明原型的
     ``arch_phy_irq()`` 函数。
  2. 在板配置文件中选择 ``CONFIG_ARCH_PHY_INTERRUPT`` 以声明
     支持 ``arch_phy_irq()``。
  
  示例可以在以下位置找到：
  
  - ``nuttx/boards/arm/sama5/sama5d3x-ek/src/sam_ethernet.c``
  - ``nuttx/boards/arm/sama5/sama5d3-xplained/src/sam_ethernet.c``
  - ``nuttx/boards/arm/sama5/sama5d4-ek/src/sam_ethernet.c``
- 其他要求：必须启用 UDP 支持（``CONFIG_NET_UDP``），
  且不得禁用信号（``CONFIG_DISABLE_SIGNALS``）。

满足所有这些前提条件后，可以通过选择以下附加选项
在 NSH 网络初始化线程上启用 NSH 网络管理：

- ``CONFIG_NSH_NETINIT_MONITOR``  
  默认情况下，网络初始化线程启动网络（或在尝试时失败）然后退出，
  释放其使用的所有资源。但是，如果选择此选项，网络初始化线程
  将无限期持续以监控网络状态。如果网络断开（例如，电缆被拔出），
  该线程将监控链路状态并尝试重新启动网络。在此场景中，
  网络初始化所需的资源永远不会被释放。

如果选择了网络监视器，附加选项控制其行为：

- ``CONFIG_NSH_NETINIT_SIGNO``  
  网络监视器逻辑在链路状态发生变化时接收信号。
  此设置可用于自定义信号编号以避免冲突。
- ``CONFIG_NSH_NETINIT_RETRYMSEC``  
  当网络断开时，初始化线程将定期尝试重新启动网络。
  由于这可能很耗时，重试操作仅在此值指定的间隔（以毫秒为单位）执行。
- ``CONFIG_NSH_NETINIT_THREAD_STACKSIZE``  
  网络初始化线程的栈大小。
- ``CONFIG_NSH_NETINIT_THREAD_PRIORITY``  
  网络初始化线程的优先级。

操作概述
=========================

以下是 NSH 管理线程操作方式的摘要：

1. 初始化期间，线程打开用于 IOCTL 操作的 UDP 套接字并连接信号处理程序。
2. 进入循环。在每次循环迭代开始时，线程使用 IOCTL 命令向以太网设备
   注册（或重新注册），以便在 PHY 报告链路启动或链路中断中断时接收信号。
   重新注册是必要的，因为每次 PHY 中断后通知会解除。
3. 线程从 PHY 和以太网设备读取链路状态。如果它们不一致，
   网络监视器使用 IOCTL 命令将以太网驱动启动或关闭以匹配当前网络状态。
   如果网络丢失，监视器将以太网驱动关闭；如果网络恢复，
   监视器将重新启动以太网驱动并重新建立连接。
4. 如果 PHY 和以太网驱动对链路状态达成一致，则不执行任何操作。
5. 在循环结束时，网络监视器等待 PHY 中断或超时。当其中任何一个发生时，
   控制返回到循环顶部，过程重复。
6. 如果发生 PHY 中断，信号被传递到任务并由网络监视器的信号处理程序处理，
   该处理程序发送信号量以立即从等待中重新唤醒网络监视器。
