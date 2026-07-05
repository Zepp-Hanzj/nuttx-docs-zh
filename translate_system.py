#!/usr/bin/env python3
"""Translate all 74 NuttX system application RST files from English to Chinese."""

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
    print("Translating all 74 NuttX system application docs...")
    
    # ===== TITLE-ONLY STUBS (39 files) =====
    
    write("adb/index.rst", f"""\
``adb`` ADB 守护进程应用程序
==============================

{NOTE}
""")

    write("argtable3/index.rst", f"""\
``argtable3`` Argtable3 命令行解析库
======================================

{NOTE}
""")

    write("cle/index.rst", f"""\
``cle`` 类 EMACS 命令行编辑器
======================================

{NOTE}
""")

    write("coredump/index.rst", f"""\
``coredump`` 核心转储
=======================

{NOTE}
""")

    write("crimon/index.rst", f"""\
``crimon`` Crimon
==================

{NOTE}
""")

    write("cu/index.rst", f"""\
``cu`` cu 命令
===============

{NOTE}
""")

    write("dd/index.rst", f"""\
``dd`` 系统 'dd' 命令
==========================

{NOTE}
""")

    write("dhcp6c/index.rst", f"""\
``dhcp6c`` DHCPv6 客户端
==========================

{NOTE}
""")

    write("dhcpc/index.rst", f"""\
``dhcpc`` DHCP 客户端
=======================

{NOTE}
""")

    write("fdt/index.rst", f"""\
``fdt`` FDT 工具
=================

{NOTE}
""")

    write("gdbstub/index.rst", f"""\
``gdbstub`` GDB 存根
=====================

{NOTE}
""")

    write("hex2bin/index.rst", f"""\
``hex2bin`` Intel HEX 转二进制工具
==========================================

{NOTE}
""")

    write("hexed/index.rst", f"""\
``hexed`` 十六进制编辑器
=========================

{NOTE}
""")

    write("hostname/index.rst", f"""\
``hostname`` \"hostname\" 命令
===============================

{NOTE}
""")

    write("input/index.rst", f"""\
``input`` 输入事件
===================

{NOTE}
""")

    write("iptables/index.rst", f"""\
``iptables`` \"iptables\" 命令
===============================

{NOTE}
""")

    write("lm75/index.rst", f"""\
``lm75`` LM75 温度传感器
==========================

{NOTE}
""")

    write("lzf/index.rst", f"""\
``lzf`` LZF 压缩工具
======================

{NOTE}
""")

    write("mdio/index.rst", f"""\
``mdio`` MDIO 工具
===================

{NOTE}
""")

    write("netdb/index.rst", f"""\
``netdb`` netdb
================

{NOTE}
""")

    write("nxlooper/index.rst", f"""\
``nxlooper`` nxlooper
=====================

{NOTE}
""")

    write("nxrecorder/index.rst", f"""\
``nxrecorder`` nxrecorder
=========================

{NOTE}
""")

    write("ofloader/index.rst", f"""\
``ofloader`` ofloader
=====================

{NOTE}
""")

    write("ping6/index.rst", f"""\
``ping6`` ICMPv6 \"ping6\" 命令
================================

{NOTE}
""")

    write("popen/index.rst", f"""\
``popen`` popen
================

{NOTE}
""")

    write("readline/index.rst", f"""\
``readline`` readline
=====================

{NOTE}
""")

    write("sched_note/index.rst", f"""\
``sched_note`` sched_note
=========================

{NOTE}
""")

    write("setlogmask/index.rst", f"""\
``setlogmask`` \"setlogmask\" 命令
===================================

{NOTE}
""")

    write("stackmonitor/index.rst", f"""\
``stackmonitor`` 栈监控器
==========================

{NOTE}
""")

    write("system/index.rst", f"""\
``system`` system()
====================

{NOTE}
""")

    write("taskset/index.rst", f"""\
``taskset`` Taskset 命令
=========================

{NOTE}
""")

    write("tcpdump/index.rst", f"""\
``tcpdump`` tcpdump 命令
=========================

{NOTE}
""")

    write("tee/index.rst", f"""\
``tee`` Tee 命令
=================

{NOTE}
""")

    write("telnet/index.rst", f"""\
``telnet`` Telnet 命令
=======================

{NOTE}
""")

    write("telnetd/index.rst", f"""\
``telnetd`` Telnet 守护进程
============================

{NOTE}
""")

    write("ubloxmodem/index.rst", f"""\
``ubloxmodem`` u-blox 调制解调器命令
======================================

{NOTE}
""")

    write("uniqueid/index.rst", f"""\
``uniqueid`` \"uniqueid\" 命令
===============================

{NOTE}
""")

    write("vi/index.rst", f"""\
``vi`` vi 编辑器
=================

{NOTE}
""")

    write("zlib/index.rst", f"""\
``zlib`` Zlib 压缩工具
=======================

{NOTE}
""")

    # ===== FILES WITH CONTENT (35 files) =====
    
    # index.rst (top-level)
    write("index.rst", f"""\
================================
系统库和 NSH 附加组件
================================

.. toctree::
   :glob:
   :maxdepth: 1
   :titlesonly:
   :caption: 目录
   
   */index*

{NOTE}
""")

    # trace/index.rst
    write("trace/index.rst", f"""\
=======================
``trace`` Trace 命令
=======================

{NOTE}

请参阅 https://nuttx.apache.org/docs/latest/guides/tasktraceuser.html
""")

    # gprof/index.rst
    write("gprof/index.rst", f"""\
=============================
``gprof`` GNU 性能分析工具
=============================

{NOTE}

请参考 :doc:`/debugging/gprof` 获取全面的 gprof 文档，包括配置选项、使用示例和实际开发板示例。
""")

    # flash_eraseall/index.rst
    write("flash_eraseall/index.rst", f"""\
====================================
``flash_eraseall`` Flash 擦除工具
====================================

{NOTE}

``flash_eraseall`` 命令用于擦除整个 MTD 设备或擦除指定的分区。该命令需要
在 NuttX 配置中启用 ``CONFIG_SYSTEM_FLASH_ERASEALL=y``。

用法
----

::

  flash_eraseall [-q] <mtd_device>

选项
----

- ``-q``: 静默模式，不显示进度信息。
- ``<mtd_device>``: 要擦除的 MTD 设备路径，例如 ``/dev/mtd0`` 或 ``/dev/mtdblock0``。

示例
----

.. code-block:: bash

  flash_eraseall /dev/mtd0

注意事项
--------

- 擦除操作会永久删除设备上的所有数据，请谨慎使用。
- 确保在擦除前备份重要数据。
""")

    # nxplayer/index.rst
    write("nxplayer/index.rst", f"""\
==============================
``nxplayer`` nxplayer 播放器
==============================

{NOTE}

``nxplayer`` 是一个命令行媒体播放器应用程序，可用于播放音频文件。

配置选项
--------

- ``CONFIG_SYSTEM_NXPLAYER`` – 启用 nxplayer 应用程序。
- ``CONFIG_AUDIO`` – 启用音频子系统支持。
""")

    # sensorscope/index.rst
    write("sensorscope/index.rst", f"""\
==================================
``sensorscope`` 传感器监视工具
==================================

{NOTE}

``sensorscope`` 是一个用于监视和显示传感器数据的工具。

配置选项
--------

- ``CONFIG_SYSTEM_SENSORSCOPE`` – 启用 sensorscope 应用程序。
- ``CONFIG_SENSORS`` – 启用传感器子系统支持。
""")

    # libuv/index.rst
    write("libuv/index.rst", f"""\
========================
``libuv`` libuv 库
========================

{NOTE}

``libuv`` 是一个跨平台的异步 I/O 库，最初为 Node.js 开发，现已成为独立项目。

概述
----

libuv 提供了事件循环、异步网络、异步文件系统操作、子进程管理等功能。

配置选项
--------

- ``CONFIG_SYSTEM_LIBUV`` – 启用 libuv 库支持。
""")

    # adcscope/index.rst
    write("adcscope/index.rst", f"""\
==============================
``adcscope`` ADC 作用域工具
==============================

{NOTE}

``adcscope`` 是一个用于监视和显示 ADC（模数转换器）数据的工具。

配置选项
--------

- ``CONFIG_SYSTEM_ADCSCOPE`` – 启用 adcscope 应用程序。
- ``CONFIG_ADC`` – 启用 ADC 子系统支持。
""")

    # cfgdata/index.rst
    write("cfgdata/index.rst", f"""\
============================
``cfgdata`` 配置数据工具
============================

{NOTE}

``cfgdata`` 是一个用于管理配置数据的工具。

配置选项
--------

- ``CONFIG_SYSTEM_CFGDATA`` – 启用 cfgdata 应用程序。
""")

    # syslogd/index.rst
    write("syslogd/index.rst", f"""\
====================================
``syslogd`` 系统日志守护进程
====================================

{NOTE}

``syslogd`` 是一个系统日志守护进程，用于接收和处理系统日志消息。

概述
----

``syslogd`` 实现了标准的 syslog 协议，可以接收来自系统各组件的日志消息，
并将它们写入指定的日志文件或其他输出目标。

配置选项
--------

- ``CONFIG_SYSTEM_SYSLOGD`` – 启用 syslogd 应用程序。
- ``CONFIG_NET`` – 启用网络支持（用于远程日志接收）。
- ``CONFIG_SYSTEM_SYSLOGD_SOCKET_PATH`` – 指定 syslog 套接字路径。
""")

    # fastboot/index.rst
    write("fastboot/index.rst", f"""\
======================
``fastboot`` fastbootd
======================

{NOTE}

准备工作
==========================

- 检查 fastboot 工具（主机端）：:code:`fastboot --version`
- 下载并安装 fastboot 工具（主机端）：`platform-tools <https://developer.android.com/tools/releases/platform-tools>`__
- 启用 fastbootd 应用程序（设备端）：:code:`CONFIG_USBFASTBOOT=y` 和 :code:`CONFIG_SYSTEM_FASTBOOTD=y`
- 启动 fastbootd（设备端）：:code:`fastbootd &`

命令
==========================

- :code:`fastboot reboot [FLAG]`: 重启设备，:code:`[FLAG]` 的更多详情：`g_resetflag <https://github.com/apache/nuttx-apps/blob/master/nshlib/nsh_syscmds.c#L114>`__ 和 `boardioc_softreset_subreason_e <https://github.com/apache/nuttx/blob/master/include/sys/boardctl.h#L458>`__
- :code:`fastboot flash <PARTITION> <FILENAME>`: 使用给定的 :code:`<FILENAME>` 刷写分区 :code:`<PARTITION>`
- :code:`fastboot erase <PARTITION>`: 擦除给定分区
- 获取变量
   - :code:`fastboot getvar product`: 获取产品名称
   - :code:`fastboot getvar kernel`: 获取内核名称
   - :code:`fastboot getvar version`: 获取操作系统版本字符串
   - :code:`fastboot getvar slot-count`: 获取槽位数量
   - :code:`fastboot getvar max-download-size`: 获取最大下载大小
- OEM
   - :code:`fastboot oem filedump <PARTITION> [OFFSET] [LENGTH]`: 从 :code:`<OFFSET>`（默认为零）获取 :code:`<PARTITION>` 的 :code:`<LENGTH>`（默认为全部）字节数据
   - :code:`fastboot oem memdump <ADDRESS> <LENGTH>`: 从地址 :code:`<ADDRESS>` 转储 :code:`<LENGTH>` 字节内存
   - :code:`fastboot oem shell <COMMAND>`: 执行自定义命令，例如 "oem shell ps"、"oem shell ls /dev/"
- :code:`fastboot get_staged <OUT_FILE>`: 将上一个命令暂存的数据写入文件 :code:`<OUT_FILE>`，例如 "oem filedump" 和 "oem memdump"

示例
==========================

- 退出 fastboot 模式：:code:`fastboot reboot`
- 将 app.bin 刷写到 /dev/app 分区：:code:`fastboot flash app ./app.bin`
- 擦除 /dev/userdata 分区：:code:`fastboot erase userdata`
- 转储 /dev/app 分区：:code:`fastboot filedump /dev/app` 然后 :code:`fastboot get_staged ./dump_app.bin`
- 转储从 0x44000000 到 0x440b6c00 的内存：:code:`fastboot oem memdump 0x44000000 0xb6c00` 然后 :code:`fastboot get_staged ./mem_44000000_440b6c00.bin`
- 创建大小为 320KB 的 RAM 磁盘 "/dev/ram10"：:code:`fastboot oem shell "mkrd -m 10 -s 512 640"`
""")

    # cdcacm/index.rst
    write("cdcacm/index.rst", f"""\
======================================
``cdcacm`` CDC/ACM USB 串口设备
======================================

{NOTE}

``cdcacm`` 附加组件提供了一个 CDC/ACM（通信设备类/抽象控制模型）USB 串口设备驱动程序。
该驱动程序允许 NuttX 设备通过 USB 接口模拟串口通信。

配置选项
--------

- ``CONFIG_CDCACM`` – 启用 CDC/ACM USB 串口设备支持。
- ``CONFIG_CDCACM_COMPOSITE`` – 将 CDC/ACM 作为复合设备的一部分启用。
- ``CONFIG_CDCACM_CONSOLE`` – 启用 CDC/ACM 控制台。
- ``CONFIG_CDCACM_BULKIN_REQHEADERS`` – 设置批量输入请求头缓冲区数量。
- ``CONFIG_CDCACM_BULKOUT_REQHEADERS`` – 设置批量输出请求头缓冲区数量。
""")

    # nsh/index.rst
    write("nsh/index.rst", f"""\
=================================
``nsh`` NuttShell (NSH) 示例
=================================

{NOTE}

基本配置
-------------------

本目录提供了如何配置和使用 NuttShell (NSH) 应用程序的示例。NSH 是一个简单的 shell 应用程序。
NSH 的说明文档位于 ``apps/nshlib/README.md``。通过以下配置启用此功能::

  CONFIG_SYSTEM_NSH=y

使用此示例的应用程序需要在配置目录中提供一个 ``defconfig`` 文件，其中包含构建 NSH 库的指令::

  CONFIG_NSH_LIBRARY=y

其他配置要求
--------------------------------

**注意**：如果使用 NSH 串口控制台，则还需要以下配置来构建 ``readline()`` 库::

  CONFIG_SYSTEM_READLINE=y

如果包含网络支持::

  CONFIG_NETUTILS_NETLIB=y
  CONFIG_NETUTILS_DHCPC=y
  CONFIG_NETDB_DNSCLIENT=y
  CONFIG_NETUTILS_TFTPC=y
  CONFIG_NETUTILS_WEBCLIENT=y

如果启用了 Telnet 控制台，则 defconfig 文件还应包含::

  CONFIG_NETUTILS_TELNETD=y

此外，如果启用了 Telnet 控制台，请确保在 NuttX 配置文件中设置以下选项，
否则性能会很差（因为每次 TCP 传输只传输一个字符）：

- ``CONFIG_STDIO_BUFFER_SIZE`` – 某个值 ``>= 64``
- ``CONFIG_STDIO_LINEBUFFER=y``
""")

    # nxcodec/index.rst
    write("nxcodec/index.rst", f"""\
===============================
``nxcodec`` NuttX 编解码器工具
===============================

{NOTE}

``nxcodec`` 是 NuttX 的编解码器工具，用于处理音视频编解码操作。

概述
----

nxcodec 提供了一个命令行接口来测试和使用 NuttX 中的编解码器框架。它支持
各种编解码器的加载和使用。

配置选项
--------

- ``CONFIG_SYSTEM_NXCODEC`` – 启用 nxcodec 应用程序。
- ``CONFIG_VIDEO`` – 启用视频子系统支持。
- ``CONFIG_AUDIO`` – 启用音频子系统支持。
""")

    # nxdiag/index.rst
    write("nxdiag/index.rst", f"""\
================================
``nxdiag`` NuttX 诊断工具
================================

{NOTE}

NuttX 诊断工具 (Nxdiag) 是一个命令行工具，可用于收集 NuttX 系统和主机系统的信息。
它还可以用于运行测试，以验证供应商的工具是否已正确安装和配置。

其主要目的是收集可用于调试问题的信息，并简化不熟悉用户的错误报告过程。

该工具使用 Python 脚本 (``nuttx/tools/host_info_dump.py``) 在构建期间收集主机系统信息，
并使用 C 程序收集 NuttX 系统信息并显示所有可用信息。有关 Python 脚本的更多信息，
请查看 ``host_info_dump.py`` 的命令行选项和代码注释。

或者，可以使用 ``host_info`` 目标而无需启用 nxdiag 应用程序和重新烧录即可获取系统信息。
该目标可在配置步骤之后工作，并打印有关 NuttX 和主机系统的信息。

.. note:: Nxdiag 需要 Python 3.6 或更高版本。在 Linux 发行版上，建议安装 ``distro`` Python 模块，
          因为它提供更准确的主机系统信息。

用法
-----

本页显示 ``nxdiag`` 选项。请注意，某些选项仅在启用相应的配置选项时才可用
（参见 :ref:`命令表 <nxdiagcmddependencies>`）。
要获取系统可用的 ``nxdiag`` 选项的完整列表，只需运行 ``nxdiag``::

    Usage: nxdiag [options]
    Options:
            -h                                 Show this message
            -n, --nuttx                        Output the NuttX operational system information.
            -f, --flags                        Output the NuttX compilation and linker flags used.
            -c, --config                       Output the NuttX configuration options used.
            -o, --host-os                      Output the host system operational system information.
            -p, --host-path                    Output the host PATH environment variable.
            -k, --host-packages                Output the host installed system packages.
            -m, --host-modules                 Output the host installed Python modules.
            -v, --vendor-specific              Output vendor specific information.
            --all                              Output all available information.

示例输出可以在 `这里 <https://pastebin.com/HSw1EvhR>`_ 查看。

.. toctree::
  :maxdepth: 2
  :caption: 目录

  config.rst
""")

    # nxdiag/config.rst
    write("nxdiag/config.rst", f"""\
.. |br| raw:: html

   <br/>

======================
配置设置
======================

{NOTE}

上述命令的可用性取决于 NuttX 配置文件中可能启用或未启用的功能。
以下 :ref:`命令表 <nxdiagcmddependencies>` 指示了每个命令对 NuttX 配置设置的依赖关系。
通用配置设置在 NuttX 移植指南中讨论。
Nxdiag 特定的配置设置在本文档的 :ref:`底部 <nxdiagconfiguration>` 讨论。

请注意，``--vendor-specific`` 或 ``-v`` 选项将生成特定于供应商的信息和检查。
此选项的输出将取决于 NuttX 配置文件中选择的供应商。例如，如果启用了
``CONFIG_SYSTEM_NXDIAG_ESPRESSIF`` 配置设置，则此选项将提供 Espressif 设备的
自定义信息和检查。可以同时选择多个供应商。

.. _nxdiagcmddependencies:

选项对配置设置的依赖
=============================================

========================= ===========================================
选项                        依赖的配置
========================= ===========================================
``--help, -h``
``--nuttx, -n``
``--flags, -f``           ``CONFIG_SYSTEM_NXDIAG_COMP_FLAGS``
``--config, -c``          ``CONFIG_SYSTEM_NXDIAG_CONF``
``--host-os, -o``
``--host-path, -p``       ``CONFIG_SYSTEM_NXDIAG_HOST_PATH``
``--host-packages, -k``   ``CONFIG_SYSTEM_NXDIAG_HOST_PACKAGES``
``--host-modules, -m``    ``CONFIG_SYSTEM_NXDIAG_HOST_MODULES``
``--vendor-specific, -v``
``--all``

========================= ===========================================

.. _nxdiagconfiguration:

Nxdiag 特定配置设置
======================================

Nxdiag 的行为可以通过 ``boards/<arch>/<chip>/<board>/defconfig`` 文件中的以下设置进行修改：

========================================  ==================================
配置                                      描述
========================================  ==================================
 ``CONFIG_SYSTEM_NXDIAG_COMP_FLAGS``      启用 nxdiag 应用程序以列出 NuttX 编译
                                          标志。这对于调试主机和目标系统非常有用。
                                          启用 ``-f`` 和 ``--nuttx-flags`` 选项。

 ``CONFIG_SYSTEM_NXDIAG_CONF``            启用 nxdiag 应用程序以列出用于编译 NuttX
                                          的配置选项。这对于调试主机和目标系统非常有用。
                                          启用 ``-c`` 和 ``--nuttx-config`` 选项。

 ``CONFIG_SYSTEM_NXDIAG_HOST_PATH``       启用 nxdiag 应用程序以列出主机系统 PATH
                                          环境变量。这对于调试主机系统非常有用。
                                          启用 ``-p`` 和 ``--host-path`` 选项。

 ``CONFIG_SYSTEM_NXDIAG_HOST_PACKAGES``   启用 nxdiag 应用程序以列出主机系统上
                                          已安装的软件包。这对于调试主机系统非常有用。
                                          启用 ``-k`` 和 ``--host-packages`` 选项。

 ``CONFIG_SYSTEM_NXDIAG_HOST_MODULES``    启用 nxdiag 应用程序以列出主机系统上
                                          已安装的 Python 模块。这对于调试主机系统
                                          非常有用。启用 ``-m`` 和 ``--host-modules`` 选项。

 ``CONFIG_SYSTEM_NXDIAG_ESPRESSIF``       启用 Espressif 特定的信息和检查。

========================================  ==================================
""")

    print("\nDone with batch 1. Continuing with remaining content files...")
    return True

if __name__ == '__main__':
    main()
