============================
通过轻量级链路的控制台
============================

LWL 是目标板与调试主机之间的一种轻量级双向通信方式，
无需任何额外硬件。

它可与 OpenOCD 以及其他能够在目标板运行时读写内存的调试器配合使用……
例如，如果你拥有 JLink SDK 并相应修改了此文件，它也应该可以与 JLink 一起运行。

工作原理很简单：一个 32 位的 `'上行字'` 从目标板向主机通信，
一个相同大小的 `'下行字'` 则沿相反方向传输。这两个字可以位于
目标板和调试主机均可读写的任意内存中。通过这两个字上的简单
乒乓握手协议即可实现上下行通信。
优点是不需要额外的集成工作。缺点是根据使用场景，可能需要
向 lwl 提供周期来轮询下行字的变化。
对于简单的控制台场景，这并不是必需的。

为方便起见，通信位置会通过搜索 RAM 自动发现。
如果你希望使用固定位置，只需定义 downwordaddr 和 upwordaddr 即可。

位配置
-----------------

下行字（主机到目标板）
^^^^^^^^^^^^^^^^^^^^^^^^^

A D U VV XXX O2 O1 O0

A   31    1 - 服务激活（由主机设置）
D   30    1 - 下行感知（有数据时翻转）
U   29    1 - 上行感知确认（翻转以确认收到上行数据）
VV  28-27 2 - 有效字节数（消息中有效八位字节的数量）
XXX 26-24 3 - 使用的端口（消息类型）
O2  23-16 8 - 八位字节 2
O1  15-08 8 - 八位字节 1
O0  07-00 8 - 八位字节 0

上行字（目标板到主机）
^^^^^^^^^^^^^^^^^^^^^^^

A   31    1 - 服务激活（由设备设置）
D   30    1 - 下行感知确认（翻转以确认收到下行数据）
U   29    1 - 上行感知（有数据时翻转）
VV  28-27 2 - 上行字有效字节数
XXX 26-24 3 - 使用的端口（消息类型）
O2  23-16 8 - 八位字节 2
O1  15-08 8 - 八位字节 1
O0  07-00 8 - 八位字节 0

端口 1 用于控制台。目前没有定义其他端口。

用法
=====

不需要特殊的 Python 模块，只需按如下方式即可运行该应用程序：

在第一个终端中执行 openocd 命令以连接到目标板。
假设你已经将支持 LWL 控制台的固件（nuttx.bin）烧录完成。
对于 stm32f4discovery 开发板，我使用以下命令：

.. code-block:: console

  $ sudo openocd -f board/stm32f4discovery.cfg
  Open On-Chip Debugger  v0.10.0-esp32-20200526-6-g4c41a632 (2020-06-23-10:12)
  Licensed under GNU GPL v2
  For bug reports, read
  \thttp://openocd.org/doc/doxygen/bugs.html
  Info : The selected transport took over low-level target control. The results might differ compared to plain JTAG/SWD
  srst_only separate srst_nogate srst_open_drain connect_deassert_srst
  
  Info : Listening on port 6666 for tcl connections
  Info : Listening on port 4444 for telnet connections
  Info : clock speed 2000 kHz
  Info : STLINK V2J17S0 (API v2) VID:PID 0483:3748
  Info : Target voltage: 3.216252
  Info : stm32f4x.cpu: hardware has 6 breakpoints, 4 watchpoints
  Info : Listening on port 3333 for gdb connections
  Info : accepting 'tcl' connection on tcp/6666
  invalid command name "ocd_mdw"
  0x20000000: 000000ff

  0x20000000: 000000ff
  
  0x20000004: 7216a318
  
  0x2000000c: 994b5b1b
  
  0x2000000c: 994b5b1b
  
  0x2000000c: 994b5b1b

  ...

然后在另一个终端中执行：

.. code-block:: console

  $ ./ocdconsole.py
  ==Link Activated
  
  nsh>
  nsh> help
  help usage:  help [-v] [<cmd>]
  
   ?        echo     exit     hexdump  ls       mh       sleep    xd
   cat      exec     help     kill     mb       mw       usleep
  nsh>

此代码设计为 `'健壮的'`，能够在 openocd 进程关闭和重启后继续工作。
当你的目标应用程序发生变化时，上行字和下行字的位置可能会改变，
因此会重新搜索它们。为了加快启动过程，
建议将这些字放在固定位置（例如通过链接器文件）并直接引用它们。

后续工作/改进
========================

目前 NuttX 端的 lwl 驱动采用轮询方式，但为了获得更好的性能，
可以使用中断来检测内存位置被修改以读取数据。

它还将避免在驱动中使用忙等待，更多信息请参阅
``nuttx/arch/arm/src/common/arm_lwl_console.c``。
