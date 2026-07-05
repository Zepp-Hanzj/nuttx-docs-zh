#!/usr/bin/env python3
"""Translate remaining NuttX system application RST files (batch 4 - ping and i2c)."""

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
    print("Translating remaining content files (batch 4)...")
    
    # ping/index.rst
    write("ping/index.rst", f"""\
============================
``ping`` ICMP "ping" 命令
============================

{NOTE}

概述
--------
``ping`` 应用程序向目标主机发送 ICMPv4 Echo Request 数据包，并报告回复、
丢包率、往返时间 (RTT) 统计和基本错误。它对于验证 IP 连通性和测量延迟非常有用。

系统要求
------------
- 启用网络：``CONFIG_NET=y``
- 操作系统中的 ICMP 和原始套接字支持
- 构建应用程序：``CONFIG_SYSTEM_PING=y``
- 可选 DNS 解析：``CONFIG_LIBC_NETDB`` 和 ``CONFIG_NETDB_DNSCLIENT``
- 可选设备绑定支持（``-I``）：``CONFIG_NET_BINDTODEVICE``

命令格式
--------

::

\tping [-c <count>] [-i <interval>] [-W <timeout>] [-s <size>] [-I <interface>] <hostname|ip-address>

其中 ``<hostname>`` 可以是 DNS 名称（启用 DNS 客户端时）或 IPv4 地址。
没有 DNS 时，需要 IPv4 地址。

选项
-------

- ``-c <count>``：要发送的 echo 请求数量（默认：实现定义，通常为 10）。
- ``-i <interval>``：请求之间的延迟，单位毫秒（默认：1000 ms）。
- ``-W <timeout>``：每个回复的超时时间，单位毫秒（默认：1000 ms）。
- ``-s <size>``：要发送的 ICMP 负载字节数（默认：56）。
- ``-I <interface>``：将套接字流量绑定到特定网络设备名称（需要 ``CONFIG_NET_BINDTODEVICE``）。
- ``-h``：显示帮助并退出。

输出
------

对于每个回复，``ping`` 打印类似以下的行：

::

\t56 bytes from 10.0.2.2: icmp_seq=3 time=6.0 ms

超时时：

::

\tNo response from 10.0.2.2: icmp_seq=3 time=1000 ms

完成时，打印摘要统计信息，包括发送的数据包数、接收的数据包数、丢包率、
总时间和 RTT 最小/平均/最大/标准差：

::

\t10 packets transmitted, 10 received, 0% packet loss, time 10011 ms
\trtt min/avg/max/mdev = 0.000/0.600/6.000/1.800 ms

退出状态
-----------

- 成功 (0)：完成且无致命错误。
- 失败 (!=0)：报告了致命错误（例如套接字/DNS 错误、无效参数）。

示例
--------

基本 IP 连通性测试：

.. code-block:: bash

\tping 1.1.1.1

使用自定义请求数和负载大小 ping 主机名：

.. code-block:: bash

\tping -c 3 -s 100 example.com

减小间隔和超时以加快探测：

.. code-block:: bash

\tping -i 500 -W 500 10.0.2.2

将流量绑定到特定接口（需要 ``CONFIG_NET_BINDTODEVICE``）：

.. code-block:: bash

\tping -I wlan0 10.0.2.2

如果设备名称无效，``ping`` 报告绑定错误并终止。

注意事项
--------

- 设备绑定 (``-I``) 在存在多个接口或路由不明确的早期网络设置时非常有用。
  它强制流量使用指定的设备。
- ``<hostname>`` 的 DNS 解析需要 DNS 客户端配置；否则请提供 IPv4 地址。
- ICMPv6 支持由单独的 ``ping6`` 应用程序提供（启用时，
  ``CONFIG_NETUTILS_PING6``），具有类似的选项和输出。

故障排除
---------------

- ``ERROR: ping_gethostip(...) failed``：DNS 查找失败或地址无效。
- ``ERROR: socket() failed: <errno>``：原始套接字创建失败。
- ``ERROR: setsockopt error: <errno>``：设备绑定 (``-I``) 失败；检查接口名称和 ``CONFIG_NET_BINDTODEVICE``。
- ``ERROR: poll/recvfrom failed``：链路问题或网络栈错误。

实现细节
----------------------

内部实现中，应用程序使用 ``apps/netutils/ping/icmp_ping.c`` 驱动 ICMP Echo
请求和解析回复。命令行界面和打印逻辑在 ``apps/system/ping/ping.c`` 中实现。
""")

    # i2c/index.rst
    write("i2c/index.rst", f"""\
================
``i2c`` I2C 工具
================

{NOTE}

I2C 工具提供了一种调试 I2C 相关问题的方法。本 README 文件将提供 I2C 工具的用法信息。

目录
--------

- 系统要求
  - I2C 驱动程序
  - 配置选项
- 帮助
- 命令行格式
- 通用命令选项
  - "粘性" 选项
  - 环境变量
  - 通用选项摘要
- 命令摘要
  - ``bus``
  - ``dev``
  - ``get``
  - ``set``
  - ``verf``
- I2C 构建配置
  - NuttX 配置要求
  - I2C 工具配置选项

系统要求
-------------------

I2C 工具设计为 NuttShell (NSH) 附加组件。请阅读 ``apps/nshlib/README.md``
文件了解附加组件的信息。

配置选项
~~~~~~~~~~~~~~~~~~~~~

- ``CONFIG_NSH_BUILTIN_APPS`` – 将工具构建为 NSH 内置命令。
- ``CONFIG_I2CTOOL_MINBUS`` – 硬件支持的最小总线索引（默认 ``0``）。
- ``CONFIG_I2CTOOL_MAXBUS`` – 硬件支持的最大总线索引（默认 ``3``）。
- ``CONFIG_I2CTOOL_MINADDR`` – 最小设备地址（默认：``0x03``）。
- ``CONFIG_I2CTOOL_MAXADDR`` – 最大设备地址（默认：``0x77``）。
- ``CONFIG_I2CTOOL_MAXREGADDR`` – 最大寄存器地址（默认：``0xff``）。
- ``CONFIG_I2CTOOL_DEFFREQ`` – 默认频率（默认：``4000000``）。

帮助
----

首先，I2C 工具支持非常丰富的帮助输出。可以通过输入以下任一方式查看帮助输出::

  nsh> i2c help

或::

  nsh> i2c ?

以下是帮助输出的示例。它显示了命令行的一般形式、支持的各种 I2C 命令及其
特有的命令行选项，以及 I2C 命令选项的更详细摘要::

  nsh> i2c help

  Usage: i2c <cmd> [arguments]
  Where <cmd> is one of:

    Show help     : ?
    List buses    : bus
    List devices  : dev [OPTIONS] <first> <last>
    Read register : get [OPTIONS] [<repetitions>]
    Show help     : help
    Write register: set [OPTIONS] <value> [<repetitions>]
    Verify access : verf [OPTIONS] <value> [<repetitions>]

    Where common _sticky_ OPTIONS include:
      [-a addr] is the I2C device address (hex).  Default: 03 Current: 03
      [-b bus] is the I2C bus number (decimal).  Default: 1 Current: 1
      [-r regaddr] is the I2C device register address (hex).  Default: 00 Current: 00
      [-w width] is the data width (8 or 16 decimal).  Default: 8 Current: 8
      [-s|n], send/don't send start between command and data.  Default: -n Current: -n
      [-i|j], Auto increment|don't increment regaddr on repetitions.  Default: NO Current: NO
      [-f freq] I2C frequency.  Default: 100000 Current: 100000

**注意事项**：

- 环境变量如 ``$PATH`` 可用于任何参数。
- 参数是 _粘性_ 的。例如，一旦指定了 I2C 地址，该地址将一直使用直到被更改。

**警告**：

- I2C dev 命令可能对您的 I2C 设备产生不良副作用。使用风险自负。

命令行格式
-----------------

I2C 通过从 NSH 命令行调用 ``i2c`` 命令来启动。``i2c`` 命令的一般形式是::

  i2c <cmd> [arguments]

其中 ``<cmd>`` 是子命令，标识工具支持的 I2C 操作之一。``[arguments]`` 表示执行
I2C 操作所需的参数列表。这些参数因命令而异，如下所述。但是，所有命令都支持
一组核心的通用 ``OPTIONS``。因此，通用 I2C 命令的更好表示可能是::

  i2c <cmd> [OPTIONS] [arguments]

其中 ``[OPTIONS]`` 表示通用选项，arguments 表示特定于操作的参数。

通用命令选项
----------------------

"粘性" 选项
~~~~~~~~~~~~~~~~

为了与 I2C 设备交互，必须正确设置许多 I2C 参数。一种方法是为每个 I2C 参数
在每个单独的命令中设置值。I2C 工具采用了不同的方法：I2C 配置可以指定为
（可能很长的）命令行参数序列。

然而，这些参数是 _粘性_ 的。它们是粘性的，因为一旦您设置了 I2C 参数，
该值将保持不变，直到被新值重置（或直到您重置开发板）。

环境变量
~~~~~~~~~~~~~~~~~~~~~

**注意**：如果环境变量未被禁用（通过 ``CONFIG_DISABLE_ENVIRON=y``），
则这些选项也可以是环境变量。环境变量必须以特殊字符 ``$`` 开头。
例如，``PWD`` 是保存当前工作目录的变量，因此 ``$PWD`` 可以用作命令行参数。
在 I2C 工具命令中使用环境变量实际上仅在您希望编写 NSH 脚本来执行更长、
更复杂的 I2C 命令序列时才有用。

通用选项摘要
~~~~~~~~~~~~~~~~~~~~~

- ``[-a addr]`` 是 I2C 设备地址（十六进制）。默认：``03`` 当前：``03``

  ``[-a addr]`` 设置 I2C 设备地址。有效范围是 ``0x03`` 到 ``0x77``
  （此有效范围由配置设置 ``CONFIG_I2CTOOL_MINADDR`` 和 ``CONFIG_I2CTOOL_MAXADDR`` 控制）。
  如果您使用同一设备，地址只需设置一次。

  所有 I2C 地址都是 7 位十六进制值。

  **注意 1**：请注意上面的 ``help`` 输出同时显示了 I2C 地址的默认值（``03`` 十六进制）
  和当前地址值（也是 ``03`` 十六进制）。

  **注意 2**：有时 I2C 地址表示为 8 位值（第 0 位指示读或写操作）。I2C 工具使用
  7 位地址表示，第 7 位未使用，第 0 位没有读/写指示。本质上，7 位地址就像
  8 位地址右移 1 位。

  **注意 3**：大多数 I2C 总线控制器也支持 10 位寻址。截至撰写本文时，
  该功能尚未集成到 I2C 工具中。

- ``[-b bus]`` 是 I2C 总线号（十进制）。默认：``1`` 当前：``1``

  大多数设备支持多个 I2C 设备，也有唯一的总线编号。此选项标识您正在使用的总线。
  总线号的有效范围由配置设置 ``CONFIG_I2CTOOL_MINBUS`` 和 ``CONFIG_I2CTOOL_MAXBUS`` 控制。

  总线号是小的十进制数。

- ``[-r regaddr]`` 是 I2C 设备寄存器地址（十六进制）。默认：``00`` 当前：``00``

  I2C set 和 get 命令将访问 I2C 设备上的寄存器。此选项选择设备寄存器地址
  （有时称为子地址）。这是一个 8 位十六进制值。最大值由配置设置
  ``CONFIG_I2CTOOL_MAXREGADDR`` 确定。

- ``[-w width]`` 是数据宽度（8 或 16 十进制）。默认：``8`` 当前：``8``

  设备寄存器数据可以是 8 位或 16 位。此选项选择这两种数据宽度之一。

- ``[-s|n]``，在命令和数据之间发送/不发送起始信号。默认：``-n`` 当前：``-n``

  这决定在发送寄存器地址和发送/接收寄存器数据之间是否应有新的 I2C START。

- ``[-i|j]``，重复时自动递增/不递增 ``regaddr``。默认：``NO`` 当前：``NO``

  在接受可选重复次数的命令中，此选项可用于在每次重复时临时将 ``regaddr`` 值递增一。

- ``[-f freq]`` I2C 频率。默认：``400000`` 当前：``400000``

  ``[-f freq]`` 设置 I2C 设备的频率。

命令摘要
---------------

我们已经在上面看到了 I2C 帮助（或 ``?``）命令。本节将讨论其余命令。

列出总线：``bus [OPTIONS]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

此命令将简单列出所有已配置的 I2C 总线，并指示哪些受驱动程序支持，哪些不受::

  BUS   EXISTS?
  Bus 1: YES
  Bus 2: NO

总线号的有效范围由配置设置 ``CONFIG_I2CTOOL_MINBUS`` 和 ``CONFIG_I2CTOOL_MAXBUS`` 控制。

列出设备：``dev [OPTIONS] <first> <last>``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``dev`` 命令将尝试识别所选总线上的所有 I2C 设备。``<first>`` 和 ``<last>`` 参数是
7 位十六进制 I2C 地址。此命令将检查从 ``<first>`` 开始到 ``<last>`` 结束的地址范围。
它将从每个设备请求寄存器地址零的值。

默认始终使用零的寄存器地址。先前的 _粘性_ 寄存器地址被忽略。然而，某些设备
可能不响应寄存器地址零。为了解决这个问题，您可以在命令上提供新的 _粘性_
寄存器地址作为 'dev' 命令的选项。然后将使用该新的 _粘性_ 寄存器地址代替地址零。

如果 I2C 地址处的设备响应读取请求，则 ``dev`` 命令将显示设备的 I2C 地址。
如果设备不响应，此命令将显示 ``--``。结果显示如下::

  nsh> i2c dev 03 77

       0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
  00:         -- -- -- -- -- -- -- -- -- -- -- -- --
  10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  40: -- -- -- -- -- -- -- -- -- 49 -- -- -- -- -- --
  50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  70: -- -- -- -- -- -- -- --

警告：

- I2C dev 命令可能对某些 I2C 设备产生不良副作用。例如，它可能导致 EEPROM 设备中的数据丢失。

- I2C dev 命令还依赖于 I2C 驱动程序的底层行为。驱动程序如何响应寻址失败？

读取寄存器：``get [OPTIONS]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

此命令将使用通用选项中选定的 I2C 参数读取 I2C 寄存器的值。不需要其他参数。

此命令将写入 8 位地址值，然后从设备读取 8 位或 16 位数据值。可选地，
它可以在获取数据之前重新启动传输。

可以提供可选的 ``<repetitions>`` 参数来重复读取操作任意次数（最多 20 亿次）。
如果选择了自动递增 (``-i``)，则寄存器地址将在每次重复时临时递增。递增是临时的，
因为它不会改变寄存器地址的 _粘性_ 值。

成功时，输出将如下所示（如果选择了 16 位数据宽度选项，读取的数据值将显示为
4 个字符的十六进制数）::

  READ Bus: 1 Addr: 49 Subaddr: 04 Value: 96

所有值（总线号除外）都是十六进制的。

写入寄存器：``set [OPTIONS] <value>``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

此命令将使用通用选项中选定的 I2C 参数向 I2C 寄存器写入值。要写入的值必须
作为最终的十六进制值提供。根据选定的数据宽度，此值可以是 8 位值
（范围 ``00``-``ff``）或 16 位值（范围 ``0000``-``ffff``）。

此命令将写入 8 位地址值，然后向设备写入 8 位或 16 位数据值。可选地，
它可以在写入数据之前重新启动传输。

可以提供可选的 ``<repetitions>`` 参数来重复写入操作任意次数（最多 20 亿次）。
如果选择了自动递增 (``-i``)，则寄存器地址将在每次重复时临时递增。递增是临时的，
因为它不会改变寄存器地址的 _粘性_ 值。

成功时，输出将如下所示（如果选择了 16 位数据宽度选项，写入的数据值将显示为
4 个字符的十六进制数）::

  WROTE Bus: 1 Addr: 49 Subaddr: 04 Value: 96

所有值（总线号除外）都是十六进制的。

验证访问：``verf [OPTIONS] <value> [<repetitions>]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

此命令组合了对 I2C 设备寄存器的写入和读取。它将使用通用选项中选定的 I2C 参数
向 I2C 寄存器写入值，就像 ``set`` 命令中描述的那样。然后此命令将读回值，
就像 ``get`` 命令中描述的那样。最后，此命令将比较读取的值和写入的值，
如果不匹配则发出错误消息。

如果未提供值，则此命令将使用寄存器地址本身作为数据，提供地址中的地址测试。

可以提供可选的 ``<repetitions>`` 参数来重复验证操作任意次数（最多 20 亿次）。
如果选择了自动递增 (``-i``)，则寄存器地址将在每次重复时临时递增。递增是临时的，
因为它不会改变寄存器地址的 ``sticky`` 值。

成功时，输出将如下所示（如果选择了 16 位数据宽度选项，写入的数据值将显示为
4 个字符的十六进制数）::

  VERIFY Bus: 1 Addr: 49 Subaddr: 04 Wrote: 96 Read: 92 FAILURE

所有值（总线号除外）都是十六进制的。

I2C 构建配置
-----------------------

NuttX 配置要求
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I2C 工具需要在您的 NuttX 配置中进行以下设置：

1. 应用程序配置。

   使用 ``make menuconfig`` 选择 i2c 工具。以下定义应出现在您的 ``.config`` 文件中::

     CONFIG_SYSTEM_I2C=y

2. 必须启用设备特定的 I2C 驱动程序支持::

     CONFIG_I2C_DRIVER=y

   I2C 工具将使用 I2C 字符驱动程序访问 I2C 总线。这些设备将位于 ``/dev/i2cN``,
   其中 ``N`` 是 I2C 总线号。

   **注意**：I2C 驱动程序 ``ioctl`` 接口定义在 ``include/nuttx/i2c/i2c_master.h`` 中。

I2C 工具配置选项
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I2C 工具的默认行为可以通过 NuttX 配置中的设置进行修改。此配置是配置目录中的
``defconfig`` 文件，在配置 NuttX 时复制到 NuttX 顶层目录作为 ``.config``。

- ``CONFIG_NSH_BUILTIN_APPS`` – 将工具构建为 NSH 内置命令。
- ``CONFIG_I2CTOOL_MINBUS`` – 硬件支持的最小总线索引（默认 ``0``）。
- ``CONFIG_I2CTOOL_MAXBUS`` – 硬件支持的最大总线索引（默认 ``3``）。
- ``CONFIG_I2CTOOL_MINADDR`` – 最小设备地址（默认：``0x03``）。
- ``CONFIG_I2CTOOL_MAXADDR`` – 最大设备地址（默认：``0x77``）。
- ``CONFIG_I2CTOOL_MAXREGADDR`` – 最大寄存器地址（默认：``0xff``）。
- ``CONFIG_I2CTOOL_DEFFREQ`` – 默认频率（默认：``4000000``）。
""")

    print("Batch 4 done.")
    return True

if __name__ == '__main__':
    main()
