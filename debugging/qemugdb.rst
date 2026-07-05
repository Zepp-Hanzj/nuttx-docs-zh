.. include:: /substitutions.rst
.. _qemugdb:

=====================================
如何使用 QEMU 和 GDB 调试 NuttX
=====================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本指南解释了使用 QEMU 和 GDB 调试 ARM 板卡（lm3s6965-ek）所需的步骤，但可以修改为适用于 QEMU 支持的其他板卡或架构。

开始配置和编译 lm3s6965-ek 板卡的 qemu-flat 配置。

编译
=========

#. 配置 lm3s6965-ek

   有一个在 QEMU 上使用 lm3s6965-ek 的示例配置。

   只需使用 ``lm3s6965-ek:qemu-flat`` 板卡配置即可。

    .. code-block:: console

       $ cd nuttx
       $ ./tools/configure.sh lm3s6965-ek:qemu-flat

#. 编译

    .. code-block:: console

       $ make -j

启动 QEMU
==========

#. 你需要使用上面创建的 NuttX ELF 文件启动 QEMU：

    .. code-block:: console

       $ qemu-system-arm -M lm3s6965evb -device loader,file=nuttx -serial mon:stdio -nographic -s
       Timer with period zero, disabling
       ABCDF
       telnetd [4:100]

       NuttShell (NSH) NuttX-12.0.0
       nsh>

启动 GDB 连接到 QEMU
============================

   以下步骤展示了如何将 GDB 连接到运行 NuttX 的 QEMU：

    .. code-block:: console

      $ gdb-multiarch nuttx -ex "source tools/pynuttx/gdbinit.py" -ex "target remote 127.0.0.1:1234"
      Reading symbols from nuttx...
      Registering NuttX GDB commands from ~/nuttx/nuttx/tools/gdb/nuttxgdb
      set pagination off
      set python print-stack full
      "handle SIGUSR1 "nostop" "pass" "noprint"
      Load macro: ~/nuttx/nuttx/b73e7dbb3d3bbd6ff2eb9be4e5f01d5e.json
      readelf took 0.1 seconds
      Parse macro took 0.1 seconds
      Cache macro info to ~/nuttx/nuttx/b73e7dbb3d3bbd6ff2eb9be4e5f01d5e.json

      if use thread command, please don't use 'continue', use 'c' instead !!!
      if use thread command, please don't use 'step', use 's' instead !!!
      Build version:  "86868a9e194-dirty Nov 26 2024 00:14:53"

      Remote debugging using :1234
      0x0000b78a in up_idle () at chip/common/tiva_idle.c:62
      62      }
      (gdb)

#. 从 (gdb) 提示符可以运行命令来检查 NuttX：

    .. code-block:: console

        (gdb) info threads
        Id   Thread                Info                                                                             Frame
        *0   Thread 0x2000168c     (Name: Idle_Task, State: Running, Priority: 0, Stack: 1008)                      0xa45a up_idle() at chip/common/tiva_idle.c:62
        1    Thread 0x20005270     (Name: hpwork, State: Waiting,Semaphore, Priority: 224, Stack: 1984)             0xa68c up_switch_context() at common/arm_switchcontext.c:95
        2    Thread 0x20005e30     (Name: nsh_main, State: Waiting,Semaphore, Priority: 100, Stack: 2008)           0xa68c up_switch_context() at common/arm_switchcontext.c:95
        3    Thread 0x20006d48     (Name: NTP_daemon, State: Waiting,Signal, Priority: 100, Stack: 1960)            0xa68c up_switch_context() at common/arm_switchcontext.c:95
        4    Thread 0x20008b60     (Name: telnetd, State: Waiting,Semaphore, Priority: 100, Stack: 2016)            0xa68c up_switch_context() at common/arm_switchcontext.c:95
       (gdb)

如你所见，QEMU 和 GDB 是强大的工具，无需使用外部板卡或昂贵的调试硬件即可调试 NuttX。
