#!/usr/bin/env python3
"""Translate remaining NuttX system application RST files (batch 3)."""

import os

DST_DIR = "/home/hanzj-mi/workspace/nuttx-docs-zh/applications/system"
NOTE = ".. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/"

def write(rel, content):
    path = os.path.join(DST_DIR, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Wrote: {rel}")

def main():
    print("Translating remaining content files (batch 3)...")
    
    # nxcamera/index.rst
    write("nxcamera/index.rst", f"""\
=============================================
``nxcamera`` 摄像头/视频流测试命令
=============================================

{NOTE}

简介
============

``nxcamera`` 是一个用于测试 NuttX 中摄像头设备和视频流捕获的命令行工具。
它构建在 NuttX 视频子系统之上（使用 V4L2 风格的接口），通常用于：

- 枚举和打开视频设备节点，如 ``/dev/video0`` 和 ``/dev/video1``
- 配置捕获参数，包括分辨率和像素格式
- 根据平台支持和构建配置，捕获视频帧进行验证、调试或简单数据转储

用法
=====

``nxcamera`` 是一个交互式命令行程序。从 NSH 启动它，然后在 ``nxcamera>`` 提示符
下输入命令：

.. code-block:: console

   nsh> nxcamera
   nxcamera>

提示：执行 NSH 命令（隐藏功能）
==================================

在 ``nxcamera>`` 提示符下，您可以通过在命令前加上 ``!`` 来运行 NSH 命令。
这对于快速检查系统状态或调用其他工具而无需退出 ``nxcamera`` 非常有用。

.. code-block:: console

   nxcamera> !ls /dev
   /dev:
    console
    fb0
    gpio0
    gpio1
    gpio2
    gpio3
    loop
    null
    oneshot
    ram0
    ram1
    ram2
    video0
    video1
    zero
   nxcamera> !poweroff
   bash>

提示符下的典型工作流程是：

- ``input /dev/video0`` 设置输入视频节点。
- ``output /dev/fb0`` 设置输出节点，例如帧缓冲区。
- ``stream 640 480 30 NV12`` 开始流式传输，参数为 ``宽度 高度 帧率 格式``。
- ``stop`` 停止流式传输。

您可以复制粘贴以下命令来开始使用：

.. code-block:: console

  nxcamera
  input /dev/video0
  output /dev/fb0
  stream 640 480 30 YUYV # 或在 macOS 上使用 NV12

像素格式
============

对于 ``stream`` 命令，像素格式取决于平台。在 macOS ``sim`` 平台上可以使用 ``NV12``，
而在 Linux 系统上 ``YUYV`` 更常用。

示例
========

1. 启动 ``nxcamera`` 并配置典型的交互式捕获会话：

.. code-block:: console

   nsh> nxcamera
   nxcamera> input /dev/video0
   nxcamera> output /dev/fb0
   nxcamera> stream 640 480 30 NV12
   nxcamera> stop

.. figure:: nxcamera_macos_sim.png
   :alt: nxcamera 在 macOS SIM 平台上运行
   :align: center

   ``nxcamera`` 在 SIM 平台上使用 macOS AVFoundation 后端。

功能和更新
====================

- 支持多个摄像头实例，允许多个摄像头作为不同的设备节点暴露，
  如 ``/dev/video0`` 和 ``/dev/video1``。这使得在同一系统上选择和验证
  不同的视频输入源更加容易。
- 在 ``sim`` 平台上，已添加对 macOS AVFoundation 后端的支持。
  这使得在 macOS 主机上进行摄像头捕获和功能验证成为可能，
  取决于构建配置和主机权限设置。
""")

    # nxmbclient/index.rst
    write("nxmbclient/index.rst", f"""\
===================================
``nxmbclient`` NxModbus 客户端工具
===================================

{NOTE}

``nxmbclient`` 命令行工具提供了一种便捷的方式，从 NuttX shell 执行 Modbus
客户端（主站）操作。它支持 RTU、ASCII 和 TCP 传输，并提供完整的命令行配置。

支持的命令
==================

读操作：

- ``read-coils ADDR COUNT`` – 读取线圈状态 (FC01)
- ``read-discrete ADDR COUNT`` – 读取离散输入状态 (FC02)
- ``read-input ADDR COUNT`` – 读取输入寄存器 (FC04)
- ``read-holding ADDR COUNT`` – 读取保持寄存器 (FC03)

写操作：

- ``write-coil ADDR VALUE`` – 写单个线圈 (FC05)
- ``write-holding ADDR VALUE`` – 写单个保持寄存器 (FC06)
- ``write-coils ADDR VALUE...`` – 写多个线圈 (FC15)
- ``write-holdings ADDR VALUE...`` – 写多个保持寄存器 (FC16)

命令行选项
====================

传输选择（必需）：

- ``-t TYPE`` – 传输类型：``rtu``、``ascii`` 或 ``tcp``

串口传输选项（RTU/ASCII）：

- ``-d DEVICE`` – 串口设备路径（例如 ``/dev/ttyS1``）
- ``-b BAUD`` – 波特率（默认：115200）
- ``-p PARITY`` – 校验位：``none``、``even`` 或 ``odd``（默认：none）

TCP 传输选项：

- ``-h HOST`` – TCP 主机地址（例如 ``192.168.1.100``）
- ``-P PORT`` – TCP 端口（默认：502）

Modbus 选项：

- ``-u UNIT`` – 单元 ID / 从站地址（默认：1）
- ``-T TIMEOUT`` – 超时时间，单位毫秒（默认：1000）
- ``--poll MS`` – 轮询间隔，单位毫秒（0 = 单次模式）

用法示例
==============

RTU 客户端 - 读取保持寄存器::

    nsh> nxmbclient -t rtu -d /dev/ttyS1 -b 115200 read-holding 0 10
    从地址 0 读取 10 个保持寄存器：
    [0]: 0x0000
    [1]: 0x0064
    [2]: 0x00C8
    ...

TCP 客户端 - 写单个寄存器::

    nsh> nxmbclient -t tcp -h 192.168.1.100 -P 502 write-holding 0 1234
    写入地址 0 的保持寄存器：1234

RTU 客户端 - 持续轮询::

    nsh> nxmbclient -t rtu -d /dev/ttyS1 --poll 1000 read-holding 0 5
    从地址 0 读取 5 个保持寄存器：
    [0]: 0x0000
    [1]: 0x0064
    [2]: 0x00C8
    [3]: 0x012C
    [4]: 0x0190
    
    （每 1000ms 重复一次，直到 Ctrl+C）

ASCII 客户端 - 写多个线圈::

    nsh> nxmbclient -t ascii -d /dev/ttyS1 -b 9600 -p even write-coils 0 1 0 1 1
    从地址 0 开始写入 5 个线圈

配置
=============

在 NuttX 配置中启用该工具::

    CONFIG_SYSTEM_NXMBCLIENT=y
    CONFIG_INDUSTRY_NXMODBUS=y
    CONFIG_NXMODBUS_RTU=y      # 用于 RTU 支持
    CONFIG_NXMODBUS_ASCII=y    # 用于 ASCII 支持
    CONFIG_NXMODBUS_TCP=y      # 用于 TCP 支持

Kconfig 选项：

- ``CONFIG_SYSTEM_NXMBCLIENT`` – 启用 nxmbclient 工具
- ``CONFIG_INDUSTRY_NXMBCLIENT_PROGNAME`` – 程序名称（默认："nxmbclient"）
- ``CONFIG_NXMBCLIENT_PRIORITY`` – 任务优先级（默认：100）
- ``CONFIG_NXMBCLIENT_STACKSIZE`` – 栈大小（默认：DEFAULT_TASK_STACKSIZE）

另请参阅
========

- :doc:`/applications/industry/nxmodbus/index` – NxModbus 协议栈
- :doc:`/applications/examples/nxmbserver/index` – NxModbus 服务器示例
""")

    # psmq/index.rst
    write("psmq/index.rst", f"""\
========================================
``psmq`` 发布订阅消息队列
========================================

{NOTE}

``psmq`` 是发布订阅消息队列。它是一组程序和库，用于在 POSIX 消息队列之上实现
发布/订阅方式的进程间通信。

手册、源代码和更多信息请访问：https://psmq.bofc.pl

使用 ``psmqd`` 代理、``psmq_pub`` 和 ``psmq_sub`` 的简单演示：

启动代理并使其记录到文件::

  nsh> psmqd -b/brok -p/sd/psmqd/psmqd.log &

启动订阅线程，读取 ``/can/*`` 和 ``/adc/*`` 主题上发送的所有消息，
并将所有读数转储到文件::

  nsh> psmq_sub -n/sub -b/brok -t/can/* -t/adc/* -o/sd/psmq-sub/can.log &
  n/connected to broker /brok
  n/subscribed to: /can/*
  n/subscribed to: /adc/*
  n/start receiving data
  n/reply timeout set 100

发布一些消息::

  nsh> psmq_pub -b/brok -t/can/engine/rpm -m50
  nsh> psmq_pub -b/brok -t/adc/volt -m30
  nsh> psmq_pub -b/brok -t/can/room/10/temp -m23
  nsh> psmq_pub -b/brok -t/pwm/fan1/speed -m300

查看订阅线程日志::

  nsh> cat /sd/psmq-sub/can.log

  [2021-05-23 17:53:59] p:0 l:   3  /can/engine/rpm  50
  [2021-05-23 17:53:59] p:0 l:   3  /adc/volt  30
  [2021-05-23 17:53:59] p:0 l:   3  /can/room/10/temp  23

如您所见，``/pwm/fan1/speed`` 没有被订阅线程接收到，因为我们没有订阅它。

内容：

- ``psmqd`` – 代理，在客户端之间转发消息。
- ``psmq_sub`` – 监听指定主题，可用作通信记录器（可选）。
- ``psmq_pub`` – 直接从 shell 发布消息。可以发送二进制数据，但需要管道，
  因此在 NuttX 上只能发送 ASCII 数据。
- ``libpsmq`` – 用于与代理通信以及发送/接收消息的库。
""")

    # termcurses/index.rst
    write("termcurses/index.rst", f"""\
==============================================
``termcurses`` 终端 Curses 控制支持
==============================================

{NOTE}

NuttX 终端模拟库

Termcurses 库提供终端模拟支持，用于执行常见的屏幕操作，如光标移动、前景/背景
颜色控制和键盘转义序列映射。初始版本仅支持 ``vt100`` / ``ansi`` 终端类型，
但库架构具有可扩展的接口，允许在需要时支持其他模拟类型。

该库可以单独使用，也可以与 ``apps/graphics/pdcurses`` 库配合使用。pdcurses 库
已更新了 _termcurses_ 配置选项，可自动完全集成 termcurses 库。

用法
-----

要使用 termcurses 库，必须通过调用 ``termcurses_initterm()`` 函数来初始化例程。
此例程接受一个终端类型字符串，标识请求的终端模拟支持类型。如果传递 ``NULL`` 指针，
则例程将检查 ``TERM`` 环境变量并根据该字符串设置终端类型。如果仍然无法确定模拟类型，
例程将默认使用 ``vt100`` 模拟类型。

成功初始化后，``termcurses_initterm()`` 函数将分配一个新的终端上下文，
该上下文必须与所有后续的 termcurses 库函数一起传递。当不再需要此上下文时，
应调用 ``termcurses_deinitterm()`` 例程以进行正确的释放和终端清理。

与 ``telnetd`` 一起使用
--------------------------

将 termcurses 与 telnet 守护进程一起使用时，应启用 telnet 配置选项
``CONFIG_TELNET_SUPPORT_NAWS``。此选项向 telnet 库添加终端大小协商代码。
没有此选项，telnet 例程无法了解终端大小，因此 termcurses 例程必须默认使用
``80x24`` 屏幕模式。

与 ``pdcurses`` 一起使用
--------------------------

使用 pdcurses termcurses 支持时（即同时启用了 ``CONFIG_PDCURSES`` 和
``CONFIG_TERMCURSES`` 选项），pdcurses 输入设备应选择为 ``TERMINPUT``
（即设置 ``CONFIG_PDCURSES_TERMINPUT=y``）。这将使 pdcurses 键盘输入逻辑
使用 ``termcurses_getkeycode()`` 例程进行 curses 输入。


作者：Ken Pettit
日期：2018-2019
""")

    # vncviewer/index.rst
    write("vncviewer/index.rst", f"""\
===========================
``vncviewer`` VNC 查看器
===========================

{NOTE}

一个轻量级的 VNC 查看器，通过 NuttX LCD 字符设备接口 (``/dev/lcd0``) 在 LCD
显示屏上渲染远程桌面。

特性：

- RFB 3.8 协议，支持 VNC 认证（纯软件 DES，无外部库）
- 从 LCD 驱动程序自动检测像素格式
- 原始编码，逐行渲染 – 最小 RAM 使用
- 断开连接时自动重连

准备工作
==========================

- 启用 VNC 查看器应用程序（设备端）：

  .. code-block:: bash

     CONFIG_NET_TCP=y
     CONFIG_LCD=y
     CONFIG_SYSTEM_VNCVIEWER=y

- 确保设备有可用的 LCD 驱动程序 (``/dev/lcd0``) 和 TCP/IP 网络连接。

- 在主机上安装 VNC 服务器。例如，在 Ubuntu 上：

  .. code-block:: bash

     sudo apt install x11vnc xvfb openbox xterm

用法
==========================

.. code-block:: bash

   vncviewer [options] <host> [port]

选项：

- ``-p <password>`` – VNC 密码
- ``-d <devno>`` – LCD 设备号（默认：0）
- ``-h`` – 显示帮助

默认端口：5900

主机 VNC 服务器配置
==============================

支持三种服务器模式：

1. Xvfb 虚拟桌面（像素精确 1:1）
---------------------------------------------

创建与 LCD 分辨率匹配的虚拟帧缓冲区（例如 320×240）：

.. code-block:: bash

   # 启动虚拟显示
   Xvfb :1 -screen 0 320x240x16 &
   DISPLAY=:1 openbox &
   DISPLAY=:1 xterm -geometry 38x11+0+0 -fa Monospace -fs 10 &

   # 启动 VNC 服务器
   x11vnc -display :1 -rfbport 5901 -passwd mypasswd -shared -forever -xkb -add_keysyms -bg

在设备上：

.. code-block:: bash

   vncviewer -p mypasswd <host_ip> 5901

.. figure:: vncviewer_xvfb.png
   :align: center

   Xvfb 虚拟桌面 – 主机端（320×240 xterm 在 VNC 查看器中）

.. figure:: vncviewer_xvfb_lcd.jpg
   :align: center

   Xvfb 虚拟桌面 – 设备端（在 ST7789 LCD 上渲染）

2. 物理桌面裁剪（左上角区域）
-------------------------------------------

裁剪与 LCD 分辨率匹配的物理桌面区域：

.. code-block:: bash

   x11vnc -display :0 -rfbport 5901 -passwd mypasswd -shared -forever -xkb -add_keysyms -bg -clip 320x240+0+0

在设备上：

.. code-block:: bash

   vncviewer -p mypasswd <host_ip> 5901

3. 物理桌面缩放
-------------------------------------------

将完整桌面缩小到 LCD 分辨率：

.. code-block:: bash

   x11vnc -display :0 -rfbport 5901 -passwd mypasswd -shared -forever -xkb -add_keysyms -bg -scale 320x240

在设备上：

.. code-block:: bash

   vncviewer -p mypasswd <host_ip> 5901

示例
==========================

使用密码连接到 VNC 服务器：

.. code-block:: bash

   vncviewer -p mypasswd 192.168.1.100 5901

使用不同的 LCD 设备连接：

.. code-block:: bash

   vncviewer -d 1 -p mypasswd 192.168.1.100 5900
""")

    # ymodem/index.rst
    write("ymodem/index.rst", f"""\
=================
``ymodem`` YMODEM
=================

{NOTE}

这是 `ymodem 协议 <http://pauillac.inria.fr/~doligez/zmodem/ymodem.txt>`_。
根据该协议实现了 sb rb 应用程序，分别用于发送文件和接收文件。

用法
-----

常见用法
~~~~~~~~~~~~

在 Ubuntu 系统中，需要安装 lszrz，可以使用 ``sudo apt install lszrz``。
使用 minicom 与开发板通信。

高级用法
~~~~~~~~~~~~~~

为了实现更快的传输速度，在 YMODEM 协议中添加了特定的 HEADER ``STC``
来表示自定义长度。在开发板上使用 ``sb`` 和 ``rb`` 命令时，可以使用 ``-k``
选项设置自定义数据包的长度，单位为 KB。因此，需要使用 ``sbrb.py`` 进行文件传输，
并且需要 ``sbrb.py`` -k 设置与开发板相同的长度。根据测试，使用 -k 32 时，
可以达到波特率的 93%，并且完全兼容原始 ymodem 协议。

首先，需要为 sbrb.py 添加软链接，例如
``sudo ln -s /home/<name>/.../<nuttxwork>/apps/system/ymodem/sbrb.py /usr/bin``
然后可以将 sbrb.py 配置到 minicom 中。``<Ctrl + a> z o`` 然后选择
``File transfer protocols`` 并创建两个选项，命令为 'sbrb.py -k 32'。如下所示

=========== ============= ==== === ======= ======= =====
名称        程序          名称 U/D 全屏    IO重定向 多文件
=========== ============= ==== === ======= ======= =====
ymodem-k    sbrb.py -k 32 Y    U   N       Y       Y 
ymodem-k    sbrb.py -k 32 N    D   N       Y       Y 
=========== ============= ==== === ======= ======= =====

在开发板上使用 ``sb -k 32`` 或 ``rb -k 32`` 进行文件传输。

发送文件到 PC
--------------

使用 sb 命令，如 ``nsh> sb /tmp/test.c ...``，此命令支持同时发送多个文件。
然后使用 ``<Ctrl + a> , r`` 选择 ``ymodem`` 接收开发板文件。

发送文件到开发板
-----------------

使用 rb 命令，如 ``nsh> rb``，此命令支持同时接收多个文件。
然后使用 ``<Ctrl + a> , s`` 选择 ``ymodem``，然后选择要发送的文件。

帮助
~~~~

可以使用 ``sb -h`` 或 ``rb -h`` 获取帮助。

调试
-----

由于使用串口进行通信，日志会打印到调试文件。
可以使用 ``CONFIG_SYSTEM_YMODEM_DEBUGFILE_PATH`` 设置调试文件路径。
""")

    # zmodem/index.rst
    write("zmodem/index.rst", f"""\
==========================
``zmodem`` Zmodem 命令
==========================

{NOTE}

目录
--------

- 缓冲注意事项

  * 硬件流控
  * 接收缓冲区大小
  * 缓冲区建议

- 在 Linux 主机上使用 NuttX ZModem

  * 从目标设备发送文件到 Linux 主机 PC
  * 在目标设备上接收来自 Linux 主机 PC 的文件

- 构建在 Linux 下运行的 ZModem 工具

- 状态

缓冲注意事项
---------------

硬件流控
~~~~~~~~~~~~~~~~~~~~~

串口驱动程序中必须启用硬件流控以防止数据溢出。然而，在大多数 NuttX 串口驱动程序中，
硬件流控仅保护硬件 RX FIFO：数据不会在硬件 FIFO 中丢失，但在从 FIFO 中取出时仍可能丢失。
即使启用了硬件流控，我们仍然可能溢出串口驱动程序的 RX 缓冲区！这可能是一个 bug。
但目前的解决方案是使用较低的数据速率和较大的串口驱动程序 RX 缓冲区。

如果缓冲和硬件流控设置正确且工作正常，这些措施应该是不必要的。

软件流控
~~~~~~~~~~~~~~~~~~~~~

ZModem 协议内置了 ``XON/XOFF`` 流控。协议允许在消息的某些部分放置 ``XON`` 或 ``XOFF``
字符。如果接收端启用了软件流控，它将消耗这些 ``XON`` 和 ``XOFF``。否则，ZModem 逻辑
将在数据中忽略它们。

然而，NuttX 不实现 ``XON/XOFF`` 流控，因此这些不起作用。在 NuttX 上，大多数情况下
必须使用硬件流控。

如果您在主机上启用了软件流控，可以使用 ZModem 内置的 ``XON`` / ``XOFF`` 控制。
但这只能在一个方向上工作：它可以防止主机溢出目标接收缓冲区。因此您应该能够实现
主机到目标的软件流控。但仍然没有目标到主机的流控。这可能不是问题，因为主机通常
比目标快得多。

接收缓冲区大小
~~~~~~~~~~~~~~

ZModem 协议支持一个消息 (``ZRINIT``)，通知文件发送方您可以缓冲的最大数据大小。
然而，根据经验，Linux 的 sz 会忽略此设置，无论您报告的缓冲区大小如何，始终以最大大小
(``1024``) 发送文件数据。这是不幸的，因为结合数据溢出的可能性，意味着您必须使用
相当大的缓冲区才能使 ZModem 文件接收可靠（这些问题都不影响文件发送）。

缓冲区建议
~~~~~~~~~~~~~~~~~~~~~~

基于 NuttX 硬件流控和 Linux sz 行为的限制，使用以下配置进行了测试
（假设 ``UART1`` 是 ZModem 设备）：

1) 此设置决定数据包帧的最大大小::

     CONFIG_SYSTEM_ZMODEM_PKTBUFSIZE=1024

2) 输入缓冲。如果输入缓冲设置为完整的帧，则数据溢出的可能性较小::

     CONFIG_UART1_RXBUFSIZE=1024

3) 使用较大的驱动输入缓冲区，ZModem 接收 I/O 缓冲区可以较小::

     CONFIG_SYSTEM_ZMODEM_RCVBUFSIZE=256

4) 输出缓冲。输出端（NuttX 侧）不会发生溢出，因此不需要如此小心::

     CONFIG_SYSTEM_ZMODEM_SNDBUFSIZE=512
     CONFIG_UART1_TXBUFSIZE=256

在 Linux 主机上使用 NuttX ZModem
------------------------------------

从目标设备发送文件到 Linux 主机 PC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NuttX ZModem 命令已在运行 rzsz 程序的 Linux PC 上验证。要将文件发送到 PC，
首先确保串口已配置为与开发板配合工作（假设您使用 9600 波特进行数据传输 -
高速率可能导致数据溢出）::

  $ sudo stty -F /dev/ttyS0 9600     # 选择 9600 波特
  $ sudo stty -F /dev/ttyS0 crtscts  # 启用 CTS/RTS 握手 *
  $ sudo stty -F /dev/ttyS0 raw      # 将 TTY 设置为原始模式
  $ sudo stty -F /dev/ttyS0          # 显示 TTY 配置

* 仅在启用硬件流控时。

在 Linux 主机上启动 ``rz``（以 ``/dev/ttyS0`` 为例）::

  $ sudo rz < /dev/ttyS0 > /dev/ttyS0

您可以多次添加 ``rz -v`` 选项，每次都会增加调试输出级别。如果您想捕获 Linux ``rz``
输出，请通过在 ``rz`` 命令末尾添加 ``2>rz.log`` 将 ``stderr`` 重定向到日志文件。

**注意**：NuttX ZModem 启动时会按照 ZModem 规范发送 ``rz\\n``。然而在 Linux 上，
这似乎会启动其他不兼容版本的 ``rz``。您需要手动启动 ``rz`` 以确保选择了正确的版本。
当这个有问题的 ``rz``/``sz`` 插入时，您会在二进制数据流中看到 ``^`` (``0x5e``) 字符
替换了标准的 ZModem ``ZDLE`` 字符 (``0x19``)。

如果您的 Linux 系统上没有 ``rz`` 命令，需要安装的软件包是 ``rzsz``
（或可能是 ``lrzsz``）。

然后在目标设备上（以 ``/dev/ttyS1`` 为例）::

  nsh> sz -d /dev/ttyS1 <filename>

其中 filename 是要发送的文件的完整路径（即以 ``/`` 字符开头）。``/dev/ttyS1``
或您选择的任何设备 **必须** 支持硬件流控，以便节制数据传输速率以适应分配的缓冲区。

在目标设备上接收来自 Linux 主机 PC 的文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**注意**：使用 Linux ``sz`` 命令与 NuttX ``rz`` 命令时存在问题。请参阅下面的 _状态_。
建议您在 Linux 上使用 NuttX ``sz`` 命令，如下一段所述。

要将文件发送到目标设备，首先确保主机上的串口已配置为与开发板配合工作
（假设您使用 ``9600`` 波特进行数据传输 - 高速率可能导致数据溢出）::

  $ sudo stty -F /dev/ttyS0 9600     # 选择 9600（或其他）波特
  $ sudo stty -F /dev/ttyS0 crtscts  # 启用 CTS/RTS 握手 *
  $ sudo stty -F /dev/ttyS0 raw      # 将 TTY 设置为原始模式
  $ sudo stty -F /dev/ttyS0          # 显示 TTY 配置

* 仅在启用硬件流控时。

在目标设备上启动 ``rz``。在此示例中，我们使用 ``/dev/ttyS1`` 执行传输::

  nsh> rz -d /dev/ttyS1

``/dev/ttyS1`` 或您选择的任何设备 **必须** 支持硬件流控，以便节制数据传输速率
以适应分配的缓冲区。

然后在 Linux 上使用 ``sz`` 命令将文件发送到目标设备::

  $ sudo sz <filename> [-l nnnn] [-w nnnn] </dev/ttyS0 >/dev/ttyS0

其中 ``<filename>`` 是您要发送的文件。如果未指定 ``-l nnnn`` 和 ``-w nnnn``，
则可能会出现数据包缓冲区溢出错误。``nnnn`` 应设置为小于或等于
``CONFIG_SYSTEM_ZMODEM_PKTBUFSIZE`` 的值。

生成的文件将在您通过 ``CONFIG_SYSTEM_ZMODEM_MOUNTPOINT`` 配置的 ZModem
**沙箱** 中找到。

您可以多次添加 ``sz -v`` 选项，每次都会增加调试输出级别。如果您想捕获 Linux ``sz``
输出，请通过在 ``sz`` 命令末尾添加 ``2>sz.log`` 将 ``stderr`` 重定向到日志文件。

如果您的 Linux 系统上没有 sz 命令，需要安装的软件包是 ``rzsz``（或可能是 ``lrzsz``）。

构建在 Linux 下运行的 ZModem 工具
--------------------------------------------

已添加构建支持，使 NuttX ZModem 实现可以在 Linux 主机 PC 上执行。可以通过以下方式完成：

- 切换到 ``apps/systems/zmodem`` 目录
- 使用特殊的 makefile ``Makefile.host`` 进行构建

**注意事项**：

1. ``TOPDIR`` 和 ``APPDIR`` 必须在 make 命令行上定义：``TOPDIR`` 是 ``nuttx/`` 目录的
   完整路径；``APPDIR`` 是 ``apps/`` 目录的完整路径。例如，如果您将 nuttx 安装在
   ``/home/me/projects/nuttx``，apps 安装在 ``/home/me/projects/apps``，则正确的
   make 命令行应为::

     make -f Makefile.host TOPDIR=/home/me/projects/nuttx APPDIR=/home/me/projects/apps

2. 在 make 命令行上添加 ``CONFIG_DEBUG_FEATURES=1`` 以启用调试输出
3. 在构建新的主机 ``.o`` 文件之前，请确保清理旧的目标 ``.o`` 文件。

此构建已在 ``2013-7-16`` 使用 Linux 与 Olimex LPC1766STK 开发板传输文件进行了验证。
它工作得很好，似乎解决了 Linux ``sz``/``rz`` 实现中发现的所有问题。

状态
------

- ``2013-7-15``：针对 Linux ``rz``/``sz`` 命令进行测试。

  使用 ``boards/arm/lpc17xx_40xx/olimex-lpc1766stk`` 配置进行了测试。
  使用目标 ``sz`` 命令传输了大文件和小文件。可以接收小文件，但使用 Linux ``sz``
  命令接收大文件时存在问题：Linux ``sz`` 不遵守缓冲限制，在 ``rz`` 将先前接收的
  数据写入文件时继续发送数据，串口驱动程序的 RX 缓冲区在写入过程中溢出了几个字节。
  结果，当读取下一个缓冲区数据时，可能会缺少几个字节。这些缺失数据的症状是 CRC 校验失败。

  要么 (1) 我们需要一个更礼貌的主机应用程序，要么 (2) 我们需要大大改善目标端的缓冲能力！

  我现在的想法是在 PC 端也实现 NuttX ``sz`` 和 ``rz`` 命令。匹配两端并遵守握手将解决这些问题。
  另一个选择可能是以某种方式修复串口驱动程序的硬件流控。

- ``2013-7-16``。针对 Linux ``rz``/``sz`` 命令进行更多测试。

  验证了在关闭调试和较低串口波特率 (``2400``) 下，大文件传输成功无错误。
  这被认为是问题的 _解决方案_。此外，LPC17xx 硬件流控导致奇怪的挂起；
  在 LPC17xx 上禁用硬件流控时 ZModem 工作得更好。

  在此较低波特率下，RX 缓冲区大小可能可以减小；或者波特率可能可以提高。
  然而，我的想法是，在这种不健康的情况下进行调整不是正确的方法：
  最好的做法是在 Linux 主机端使用匹配的 NuttX sz。

- ``2013-7-16``。在两端使用 NuttX ``rz``/``sz`` 进行更多测试。

  NuttX ``sz``/``rz`` 命令已修改，使其可以在 Linux 下构建和执行。
  在这种情况下，双向传输都没有任何问题，无论是大文件还是小文件。
  此配置可能可以以更高的串口速率和更小的缓冲区运行（尽管截至撰写本文时尚未验证）。

- ``2018-5-27``

  更新了校验和计算。使用 ``olimex-stm32-p407/zmodem`` 配置验证了硬件流控下的正确操作。
  仅验证了主机到目标的传输。

  使用的是 Linux ``sz`` 工具。使用在 Linux 上运行的 NuttX ``sz`` 工具似乎仍然存在问题。

- ``2018-5-27``

  使用 ``olimex-stm32-p407/zmodem`` 配置验证了硬件流控下目标到主机传输的正确操作。
  同样，使用在 Linux 上运行的 NuttX ``rz`` 工具时仍存在问题。

- ``2018-6-26``

  使用 ``-w nnnn`` 选项，主机到目标的传输可以在没有硬件流控的情况下可靠工作。
""")

    print("Batch 3 done.")
    return True

if __name__ == '__main__':
    main()
