=========
gdbserver
=========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

简介
============

此工具可以利用 PC 上的崩溃日志来模拟一组 GDB 服务器功能，从而使用 GDB 来调试 NuttX 崩溃的上下文。脚本目录位于 ``tools/gdbserver.py``。

用法
=====

我们可以使用 ``-h`` 获取帮助信息：

.. code-block:: bash

   $ usage: gdbserver.py [-h] -e ELFFILE [-l LOGFILE] [-a {arm,arm-a,arm-t,riscv,esp32s3,xtensa}] [-p PORT] [-g GDB] [-i [INIT_CMD]]
                    [-r [RAWFILE ...]] [-c [COREDUMP]] [--debug]

    options:
      -h, --help            show this help message and exit
      -e ELFFILE, --elffile ELFFILE
                            elffile
      -l LOGFILE, --logfile LOGFILE
                            logfile
      -a {arm,arm-a,arm-t,riscv,esp32s3,xtensa}, --arch {arm,arm-a,arm-t,riscv,esp32s3,xtensa}
                            Only use if can't be learnt from ELFFILE.
      -p PORT, --port PORT  gdbport
      -g GDB, --gdb GDB     provided a custom GDB path, automatically start GDB session and exit gdbserver when exit GDB.
      -i [INIT_CMD], --init-cmd [INIT_CMD]
                            provided a custom GDB init command, automatically start GDB sessions and input what you provide. if you don't
                            provide any command, it will use default command [-ex 'bt full' -ex 'info reg' -ex 'display /40i $pc-40'].
      -r [RAWFILE ...], --rawfile [RAWFILE ...]
                            rawfile is a binary file, args format like ram.bin:0x10000 ...
      -c [COREDUMP], --coredump [COREDUMP]
                            coredump file, will prase memory in this file
      --debug               if enabled, it will show more logs.


日志示例
===========
1. 使用 ./tools/configure.sh esp32s3-devkit:nsh 并禁用 `CONFIG_NSH_DISABLE_MW`。
2. `make -j`
3. 将镜像烧录到 esp32s3-devkit。
4. 运行 `minicom -D /dev/ttyUSB0 -b 115200` 并复位 esp32s3-devkit。
5. 在 nsh 中使用 `mw -1` 触发崩溃。
6. 从 minicom 获取崩溃日志并保存到 `crash.log`。

.. code-block:: bash

    up_dump_register:    PC: 42009cd8    PS: 00060820
    up_dump_register:    A0: 82007d71    A1: 3fc8b6d0    A2: 3fc8b8e0    A3: 00000000
    up_dump_register:    A4: ffffffff    A5: 00000000    A6: 00000001    A7: 00000000
    up_dump_register:    A8: ffffffff    A9: 3fc8b690   A10: ffffffff   A11: 00000000
    up_dump_register:   A12: 0000002d   A13: 0000002d   A14: 3fc8bb6d   A15: 0fffffff
    up_dump_register:   SAR: 00000000 CAUSE: 0000001c VADDR: ffffffff
    up_dump_register:  LBEG: 40055499  LEND: 400554a9  LCNT: fffffffc
    dump_stack: User Stack:
    dump_stack:   base: 0x3fc8b0e0
    dump_stack:   size: 00002000
    dump_stack:     sp: 0x3fc8b6d0
    stack_dump: 0x3fc8b6c0: 82007770 3fc8b700 3fc8b8e0 00000002 ffffffff 3fc89f54 00060e20 00000000
    stack_dump: 0x3fc8b6e0: 3fc8b8e0 3fc8b778 00000000 3fc8b750 82007850 3fc8b720 3fc8b8e0 00000002
    stack_dump: 0x3fc8b700: 3fc8b720 42009c84 3fc8bb68 3fc8b8e0 82006b04 3fc8b7d0 3fc8b8e0 3fc8bb68
    stack_dump: 0x3fc8b720: 3fc8bb68 3fc8bb6b 00000000 00000000 00000000 00000000 00000000 00000000
    stack_dump: 0x3fc8b740: 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
    stack_dump: 0x3fc8b760: 00000000 00000000 00000000 00000000 00000000 00000000 00000000 3fc8bb69
    stack_dump: 0x3fc8b780: 82006ad5 00000000 00000000 00000040 00000040 3fc8bb6e 3fc8adf8 0000002c
    stack_dump: 0x3fc8b7a0: ffffffff 00000005 00000000 00000000 3fc8bae0 00000000 00000000 00000000
    stack_dump: 0x3fc8b7c0: 820068a2 3fc8b800 3fc8b8e0 3c020837 00000001 3fc8b800 3fc8b8e0 3c020837
    stack_dump: 0x3fc8b7e0: 0000000a 3fc8bae0 00000001 3fc8bb68 82006865 3fc8b820 00000001 3fc8b0c0
    stack_dump: 0x3fc8b800: 00000001 3fc8bb68 00000000 3fc8ae1c 82003618 3fc8b840 00000001 3fc8b0c0
    stack_dump: 0x3fc8b820: 3fc8b8e0 00000000 00000000 00000000 820019dc 3fc8b870 42006834 00000001
    stack_dump: 0x3fc8b840: 00000064 00000000 00000000 00000000 3c0225d8 3fc89590 00000000 3fc880cc
    stack_dump: 0x3fc8b860: 00000000 3fc8b890 00000000 00000000 3fc8b0c0 00000002 00000000 3fc8ad98
    stack_dump: 0x3fc8b880: 00000000 3fc8b8b0 00000000 00000000 00000000 00000000 00000000 00000000

7. 运行 `./tools/gdbserver.py -e nuttx -l crash.log -p 1234 -a esp32s3`
8. 运行 `xtensa-esp32s3-elf-gdb nuttx -ex "target remote 127.0.0.1:1234"`

.. code-block:: bash

    GNU gdb (esp-gdb) 12.1_20221002
    Copyright (C) 2022 Free Software Foundation, Inc.
    License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.
    Type "show copying" and "show warranty" for details.
    This GDB was configured as "--host=x86_64-linux-gnu --target=xtensa-esp-elf".
    Type "show configuration" for configuration details.
    For bug reporting instructions, please see:
    <https://www.gnu.org/software/gdb/bugs/>.
    Find the GDB manual and other documentation resources online at:
        <http://www.gnu.org/software/gdb/documentation/>.

    For help, type "help".
    Type "apropos word" to search for commands related to "word"...
    Reading symbols from nuttx...
    Remote debugging using 127.0.0.1:1234
    0x42009cd8 in cmd_mw (vtbl=0x3fc8b8e0, argc=<optimized out>, argv=<optimized out>) at nsh_dbgcmds.c:259
    259               nsh_output(vtbl, "  %p = 0x%08" PRIx32, ptr, *ptr);
    (gdb) bt
    #0  0x42009cd8 in cmd_mw (vtbl=0x3fc8b8e0, argc=<optimized out>, argv=<optimized out>) at nsh_dbgcmds.c:259
    #1  0x42007d71 in nsh_command (vtbl=0x3fc8b8e0, argc=2, argv=0x3fc8b720) at nsh_command.c:1154
    #2  0x42007770 in nsh_execute (oflags=<optimized out>, redirfile=0x0, argv=0x3fc8b720, argc=2, vtbl=0x3fc8b8e0)
        at nsh_parse.c:845
    #3  nsh_parse_command (vtbl=0x3fc8b8e0, cmdline=<optimized out>) at nsh_parse.c:2744
    #4  0x42007850 in nsh_parse (vtbl=0x3fc8b8e0,
        cmdline=0x3fc8bb68 <error: Cannot access memory at address 0x3fc8bb68>) at nsh_parse.c:2828
    #5  0x42006b04 in nsh_session (pstate=0x3fc8b8e0, login=<optimized out>, argc=1, argv=<optimized out>)
        at nsh_session.c:245
    #6  0x420068a2 in nsh_consolemain (argc=1, argv=0x3fc8b0c0) at nsh_consolemain.c:71
    #7  0x42006865 in nsh_main (argc=1, argv=0x3fc8b0c0) at nsh_main.c:74
    #8  0x42003618 in nxtask_startup (entrypt=0x42006834 <nsh_main>, argc=1, argv=0x3fc8b0c0)
        at sched/task_startup.c:70
    #9  0x420019dc in nxtask_start () at task/task_start.c:134
    (gdb)

原始文件示例
================
1. 如果你从板卡获取了内存文件，你也可以使用 gdbserver.py 重建现场。获取原始文件最常见的方法是使用 GDB 中的 dump memory 命令转储内存并保存为文件。

2. 运行 `./tools/gdbserver.py -e nuttx -r rawfile:0x1000 -a arm`
3. 使用 target remote 运行 gdb。

核心转储示例
================
1. 如果你有 coredump，也可以运行 `./tools/gdbserver.py -e nuttx -c coredump -a arm`
2. 使用 target remote 运行 gdb。

这种方法的好处是，在多核 AMP 系统中，单个 coredump 可能包含来自其他核心的内存信息。通过分析此 coredump 以及其他核心对应的 ELF 文件，你可以重建其他核心的崩溃现场。

线程感知
===============

`gdbserver.py` 基于 NuttX 中的 `g_pidhash`、`g_npidhash` 和 `g_tcbinfo` 实现线程调试。如果你提供的日志、原始文件或 coredump 可以读取这些变量，这意味着你可以在 GDB 中使用线程相关命令，例如 `info thread` 或 `thread`

如何添加新架构
===========================

主要目标是在 GDB 中建立寄存器序列，将崩溃日志中的寄存器名称与 GDB 中的寄存器顺序对齐。这种对齐将有助于创建新架构的 GDB 服务器。
