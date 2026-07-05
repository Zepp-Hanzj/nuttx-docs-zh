.. todo::
  根据需要创建新的子章节。

===
FAQ
===

NSH 技巧
==========

如何在 NSH 中使用一个应用程序？
-----------------------------------------------

您需要在 NuttX menuconfig 中至少启用三个选项
才能看到一个应用程序显示在那里：
BUILTIN、NSH_BUILTIN_APPS 以及应用程序本身。
启用 BUILTIN::

    Library Routines  --->
            [*] Support Builtin Applications

启用 NSH_BUILTIN_APPS::

    Application Configuration  --->
            NSH Library  --->
                [*]   Enable built-in applications

启用 Hello World 应用程序::

    Application Configuration  --->
            Examples  --->
                [*]   "Hello, World!" example

编译后您应该能在 NSH 中看到 hello：

.. code-block:: shell

  NuttShell (NSH) NuttX-12.5.1
  nsh> ?
  help usage:  help [-v] [<cmd>]
    .           cp          exit        mkdir       set         unset
    [           cmp         expr        mkrd        sleep       uptime
    ?           dirname     false       mount       source      usleep
    alias       dd          fdinfo      mv          test        xd
    unalias     df          free        pidof       time
    basename    dmesg       help        printf      true
    break       echo        hexdump     pwd         truncate
    cat         env         kill        rm          uname
    cd          exec        ls          rmdir       umount
  Builtin Apps:
    hello        nsh          sh
  nsh>

注意：如果您想在 /bin 目录下物理地看到这些应用程序，可以
启用 BINFS::

    File Systems  --->
            [*] BINFS File System

如何增加命令行长度？
----------------------------------------

您可以将最大命令行长度从 64 增加到其他值，
方法如下::

    Application Configuration  --->
            NSH Library  --->
                Command Line Configuration  --->
                    (64) Max command line length

如何在命令行上启用编辑支持？
----------------------------------------------------

您需要将命令行编辑器从"Minimal readline"更改为
"Command Line Editor"，方法如下::

    Application Configuration  --->
        NSH Library  --->
            Command Line Configuration  --->
                Command Line Editor (Command Line Editor) --->

如何启用命令行历史？
-----------------------------------

您需要在 menuconfig 中启用以下选项::

    Application Configuration  --->
        System Libraries and NSH Add-Ons  --->
            -*- readline() Support  --->
                [*]     Command line history
                (80)      Command line history length
                (16)      Command line history records

注意：如果您使用的是"Command Line Editor"而不是"readline"，
那么您需要使用以下另一个选项::

    Application Configuration  --->
        System Libraries and NSH Add-Ons  --->
            -*- EMACS-like Command Line Editor  --->
                [*]   Command line history
                (80)    Command line history length
                (16)    Command line history records

如何在命令行上启用自动补全？
-----------------------------------------------

您需要在 menuconfig 中启用以下选项::

    Application Configuration  --->
        System Libraries and NSH Add-Ons  --->
            -*- readline() Support  --->
                [*]     Tab completion
                (64)      Maximum built-in matches
                (64)      Maximum external command matches

注意：当使用"Command Line Editor"而不是"readline"时，
自动补全不会启用。

如何使用 Ctrl^C 中断 NSH 应用程序？
--------------------------------------------------

您需要在 menuconfig 中启用以下选项::

    RTOS Features --->
        Signal Configuration --->
            [*] Default signal actions --->
                [*] SIGINT and SIGKILL
    Device Drivers --->
        Serial Driver Support --->
            [*] Serial TERMIOS support
            [*]   Support SIGINT
            (0x03)  Serial parse SIGINT characters

板级初始化
====================

如何直接启动我的应用程序而不是启动 NSH？
----------------------------------------------------------

您可以直接启动您的应用程序，而不是启动默认的
NSH 终端。假设您的应用程序名为"hello"，那么您
需要修改 ENTRYPOINT 来调用"hello_main"而不是"nsh_main"::

    RTOS Features --->
        Tasks and Scheduling  --->
            (hello_main) Application entry point

为什么将我的应用程序放在 ENTRYPOINT 后它就停止工作了？
----------------------------------------------------------------

当您将 ENTRYPOINT 从"nsh_main"替换为您的应用程序时，一些
初始化流程会发生变化。

您可以通过启用 Board Late Initialization 来修复这个问题，它将
执行驱动程序初始化。只需启用它::

    RTOS Features --->
        RTOS hooks --->
            [*] Custom board late initialization

此外，您还需要禁用特定于架构的初始化::

    Application Configuration --->
        NSH Library --->
            [ ] Have architecture-specific initialization

为什么使用 USB 控制台时 /dev/ttySx 没有创建，即使 UART 已启用？
------------------------------------------------------------------------------

如果您不使用串行控制台，那么 /dev/ttyS0 将不会被创建，
即使您在"System Type"中启用了 UART 外设。

您可以通过启用 Serial Upper-Half Driver 来修复这个问题::

    Device Drivers --->
        Serial Driver Support --->
            [*]   Enable standard "upper-half" serial driver

网络
=======

如何检测以太网电缆连接/断开？
------------------------------------------------------

NuttX 支持来自以太网 PHY 的以太网连接/断开事件，
使用信号（参见 ``nuttx/drivers/net/phy_notify.c``）。
apps/netutils/netinit 中的网络监控线程（参见
``CONFIG_NETINIT_MONITOR``）将处理在电缆拔出时关闭网络，
并在电缆恢复时重新启动网络。
需要注意的是，您的 MCU 的以太网控制器驱动程序需要
支持 CONFIG_ARCH_PHY_INTERRUPT（并实现
``arch_phy_irq()``）。

如何定义网络数据包的 MTU 和 MSS？
------------------------------------------------------

正如您可能知道的，"MSS = MTU - 40"，所以您只需要设置 MTU。
如果您在 menuconfig 中搜索 MTU，您将找不到它，但您可以
使用 ``CONFIG_NET_ETH_PKTSIZE`` 来设置 MTU::

    Networking Support  --->
        Driver buffer configuration  --->
            (590) Ethernet packet buffer size

然后使用以下公式计算：

  MTU = NET_ETH_PKTSIZE - 14

  MSS = MTU - 40

在这种情况下，MTU = 590 - 14 => MTU = 576！

而 MSS = 576 - 40 => MSS = 536。
