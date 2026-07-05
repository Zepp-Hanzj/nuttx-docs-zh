#!/usr/bin/env python3
"""Translate remaining NuttX system application RST files (batch 5 - spi)."""

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
    print("Translating SPI tool...")
    
    write("spi/index.rst", f"""\
================
``spi`` SPI 工具
================

{NOTE}

SPI 工具提供了一种调试 SPI 相关问题的方法。本 README 文件将提供 SPI 工具的用法信息。

目录
--------

- 系统要求

  * SPI 驱动程序
  * 配置选项

- 帮助
- 命令行格式
- 通用命令选项

  * "粘性" 选项
  * 环境变量
  * 通用选项摘要

- 命令摘要
  
  * ``bus``
  * ``dev``
  * ``get``
  * ``set``
  * ``verf``

- SPI 构建配置

  * NuttX 配置要求
  * SPI 工具配置选项

系统要求
-------------------

SPI 工具设计为 NuttShell (NSH) 附加组件。请阅读 ``apps/nshlib/README.md``
文件了解附加组件的信息。

配置选项
~~~~~~~~~~~~~~~~~~~~~

- ``CONFIG_NSH_BUILTIN_APPS`` – 将工具构建为 NSH 内置命令。
- ``CONFIG_SPITOOL_MINBUS`` – 硬件支持的最小总线索引（默认 ``0``）。
- ``CONFIG_SPITOOL_MAXBUS`` – 硬件支持的最大总线索引（默认 ``3``）。
- ``CONFIG_SPITOOL_DEFFREQ`` – 默认频率（默认：``40000000``）。
- ``CONFIG_SPITOOL_DEFMODE`` – 默认模式，其中::

    0 = CPOL=0, CPHA=0
    1 = CPOL=0, CPHA=1
    2 = CPOL=1, CPHA=0
    3 = CPOL=1, CPHA=1

- ``CONFIG_SPITOOL_DEFWIDTH`` – 默认位宽（默认 ``8``）。
- ``CONFIG_SPITOOL_DEFWORDS`` – 默认交换字数（默认 ``1``）。

帮助
----

SPI 工具支持一些帮助输出。可以通过输入以下任一方式查看帮助输出::

  nsh> spi help

或::

  nsh> spi ?

以下是帮助输出的示例。它显示了命令行的一般形式、支持的各种 SPI 命令及其
特有的命令行选项，以及 SPI 命令选项的更详细摘要::

  nsh> Usage: spi <cmd> [arguments]

  Where <cmd> is one of:

    Show help     : ?
    List buses    : bus
    SPI Exchange  : exch [OPTIONS] [<hex senddata>]
    Show help     : help

  Where common _sticky_ OPTIONS include:
    [-b bus] is the SPI bus number (decimal).  Default: 0 Current: 2
       [-f freq] SPI frequency.  Default: 4000000 Current: 4000000
    [-m mode] Mode for transfer.  Default: 0 Current: 0
    [-u udelay] Delay after transfer in uS.  Default: 0 Current: 0
    [-w width] Width of bus.  Default: 8 Current: 8
    [-x count] Words to exchange.  Default: 1 Current: 4

**注意事项**：

- 环境变量如 $PATH 可用于任何参数。
- 参数是 _粘性_ 的。例如，一旦指定了 SPI 总线，该总线将一直使用直到被更改。

**警告**：

- SPI 命令可能对您的 SPI 设备产生不良副作用。使用风险自负。

命令行格式
-----------------

SPI 通过从 NSH 命令行调用 ``spi`` 命令来启动。``spi`` 命令的一般形式是::

  spi <cmd> [arguments]

其中 ``<cmd>`` 是"子命令"，标识工具支持的 SPI 操作之一。``[arguments]`` 表示执行
SPI 操作所需的参数列表。这些参数因命令而异，如下所述。但是，所有命令都支持
一组核心的通用 ``OPTIONS``。因此，通用 SPI 命令的更好表示可能是::

  spi <cmd> [OPTIONS] [arguments]

其中 ``[OPTIONS]`` 表示通用选项，arguments 表示特定于操作的参数。

通用命令选项
-----------------------

"粘性" 选项
~~~~~~~~~~~~~~~~

为了与 SPI 设备交互，必须正确设置许多 SPI 参数。一种方法是为每个 SPI 参数
在每个单独的命令中设置值。SPI 工具采用了不同的方法：SPI 配置可以指定为
（可能很长的）命令行参数序列。

然而，这些参数是 _粘性_ 的。它们是粘性的，因为一旦您设置了 SPI 参数，
该值将保持不变，直到被新值重置（或直到您重置开发板）。

环境变量
~~~~~~~~~~~~~~~~~~~~~

**注意**：如果环境变量未被禁用（通过 ``CONFIG_DISABLE_ENVIRON=y``），
则这些选项也可以是环境变量。环境变量必须以特殊字符 ``$`` 开头。
例如，``PWD`` 是保存当前工作目录的变量，因此 ``$PWD`` 可以用作命令行参数。
在 SPI 工具命令中使用环境变量实际上仅在您希望编写 NSH 脚本来执行更长、
更复杂的 SPI 命令序列时才有用。

通用选项摘要
~~~~~~~~~~~~~~~~~~~~~

- ``[-b bus]`` 是 SPI 总线号（十进制）。默认：``0``

  要在哪个 SPI 总线上通信。该总线必须已在配置中初始化为字符设备，
  格式为 ``/dev/spiX``（例如 ``/dev/spi2``）。

  总线号的有效范围由配置设置 ``CONFIG_SPITOOL_MINBUS`` 和 ``CONFIG_SPITOOL_MAXBUS`` 控制。

  总线号是小的十进制数。

- ``[-m mode]`` SPI 传输模式。

  使用哪个可用的 SPI 模式。选项为::

    0 = CPOL=0, CPHA=0
    1 = CPOL=0, CPHA=1
    2 = CPOL=1, CPHA=0
    3 = CPOL=1, CPHA=1

- ``[-u udelay]`` 传输后延迟，单位微秒。默认：``0``

  传输后提供的额外延迟。通常不需要从命令行设置。

- ``[-x count]`` 交换字数。默认：``1``

  通过总线传输的字数。为了安全起见，这被限制为相对较小的数字（默认 ``40``）。
  命令行上的任何数据首先发送，不足部分用 ``0xFF`` 填充，同时接收任何剩余数据。

- ``[-w width]`` 是数据宽度（根据目标而异）。默认：``8``

  各种 SPI 设备支持不同的数据宽度。此选项未经测试。

- ``[-f freq]`` SPI 频率。默认：``4000000`` 当前：``4000000``

  ``[-f freq]`` 设置 SPI 设备的频率。默认值非常保守。

命令摘要
---------------

列出总线：``bus [OPTIONS]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

此命令将简单列出所有已配置的 SPI 总线，并指示哪些受驱动程序支持，哪些不受::

  BUS   EXISTS?
  Bus 1: YES
  Bus 2: NO

总线号的有效范围由配置设置 ``CONFIG_SPITOOL_MINBUS`` 和 ``CONFIG_SPITOOL_MAXBUS`` 控制。

交换数据：``exch [OPTIONS] <Optional TX Data>``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

此命令触发 SPI 传输，返回来自远端的数据。

例如，您可以使用以下命令在 SPI2 (-b 2) 上交换（发送和接收）4 个字节 (-x 4)，
使用 ``loopback`` 方法。此方法要求您将 MOSI 引脚直接连接到 MISO 引脚
（注意：SCLK 和 CS 不直接参与，但如果您决定使用示波器或更恰当地使用逻辑分析仪
来分析这些引脚，仍然可以看到时钟和片选波形）::

  nsh> spi exch -b 2 -x 4 aabbccdd

  Received: AA BB CC DD

请注意，``TX Data`` 始终以十六进制指定，每个值始终为两位数，不区分大小写。

SPI 构建配置
-----------------------

NuttX 配置要求
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SPI 工具需要在您的 NuttX 配置中进行以下设置：

1. 应用程序配置。

   使用 ``make menuconfig`` 选择 SPI 工具。以下定义应出现在您的 ``.config`` 文件中::

     CONFIG_SYSTEM_SPI=y

2. 必须启用设备特定的 SPI 驱动程序支持::

     CONFIG_SPI_DRIVER=y

   SPI 工具将使用 SPI 字符驱动程序访问 SPI 总线。这些设备将位于 ``/dev/spiN``,
   其中 ``N`` 是 SPI 总线号。

   **注意**：SPI 驱动程序 ``ioctl`` 接口定义在 ``include/nuttx/spi/spi.h`` 中。
""")

    print("Batch 5 done.")

if __name__ == '__main__':
    main()
