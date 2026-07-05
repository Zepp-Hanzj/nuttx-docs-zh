=======================
将日志记录到 RAM 缓冲区
=======================

.. warning:: 
    迁移自: 
    https://cwiki.apache.org/confluence/display/NUTTX/Logging+to+a+RAM+Buffer 


默认调试输出
====================

默认情况下，当您启用调试输出时，该输出会发送到系统控制台，并与正常控制台输出混合在一起。通常，这已经足够。然而，在某些情况下，您可能希望以不同的方式做事。例如，如果有时间关键的调试输出干扰了设备的操作。或者，如果您希望将正常控制台输出与调试输出分开。

一个特别棘手的情况是在 Telnet 会话中将网络调试输出到控制台。由于 telnet 会话将控制台输出重映射到 Telnet 连接，网络调试输出可能会产生无限循环，因为网络操作生成调试输出到控制台，这又生成更多调试输出，……如此循环往复。

通过 NuttX 系统日志 (SYSLOG) 功能的一些创造性配置，这些问题都可以消除。

syslog 设备
=================

调试输出发送到 `syslog` 设备。如上所述，默认的 syslog 设备是系统控制台。然而，有许多选项可以控制 syslog 的行为——实际上太多了。有如此多的选项，您可能需要进行实验才能使 syslog 按照您希望的方式工作。

RAMLOG 设备
=================

RAMLOG 设备是一个特殊的字符设备，几乎可以用于任何目的。然而，RAMLOG 设备具有一些特殊属性，使其非常适合作为系统日志设备。

* 它支持系统日志所需的 ``syslog_write`` 接口
* 它的行为类似于管道：它实现了一个队列。向 RAMLOG 设备写入数据会将数据添加到队列头部；从 RAMLOG 设备读取数据会从队列尾部移除数据。
* 可以配置为在您尝试读取但 RAMLOG 中没有可用内容时返回 EOF。


使用 RAMLOG 作为 syslog 设备
=====================================

此 Wiki 页面介绍了一种配置的设置：使用 `RAMLOG` 作为 syslog 设备。RAMLOG 是内存中的循环缓冲区。在此配置中，所有调试输出都发送到此循环缓冲区，稍后可以使用 NSH ``dmesg`` 命令检索。

以下是使 RAMLOG 作为 syslog 设备工作所需做的事情的摘要。我使用仿真配置，但对于此功能来说这并不重要。

.. code-block:: bash

    tools/configure.sh sim:nsh
    make menuconfig

我添加了以下设置。首先，这些只是为了给我一些调试输出来进行测试：

.. code-block:: c

    CONFIG_DEBUG=y
    CONFIG_DEBUG_FS=y
    CONFIG_DEBUG_SCHED=y

这配置虚拟文件系统以支持 syslog 设备，是其他设置的必要前提条件：

.. code-block:: c

    CONFIG_SYSLOG=y

这些启用 RAMLOG 并将其配置为用作 syslog 设备

.. code-block:: c

    CONFIG_RAMLOG=y
    CONFIG_RAMLOG_CONSOLE_BUFSIZE=8192
    CONFIG_RAMLOG_NONBLOCKING=y
    CONFIG_RAMLOG_SYSLOG=y
    #CONFIG_SYSLOG_CHAR undefined, else duplicate output with syslog_write()

现在当我运行 NuttX 时，我得到如下输出。``dmesg`` 命令现在作为 NSH 命令出现：

.. code-block:: bash

    NuttShell (NSH) NuttX-7.1
    nsh> help
    help usage:  help [-v] [<cmd>]
    [           dd          free        mkdir       mw          sleep      
    ?           df          help        mkfatfs     ps          test       
    break       dmesg       hexdump     mkfifo      pwd         true       
    cat         echo        kill        mkrd        rm          umount     
    cd          exec        losetup     mh          rmdir       unset      
    cp          exit        ls          mount       set         usleep     
    cmp         false       mb          mv          sh          xd     
    Builtin Apps:
    hello

``dmesg`` 命令转储内容并清除 RAMLOG：

.. code-block:: bash

    nsh> dmesg
    nx_start: Entry
    up_unblock_task: Unblocking TCB=52bc70
    up_unblock_task: New Active Task TCB=52bc70
    posix_spawn_exec: ERROR: exec failed: 22
    cmd_mkrd: RAMDISK at 52d4f0
    posix_spawn_exec: ERROR: exec failed: 22
    mkfatfs_tryfat16: Too few or too many clusters for FAT16: 4081 < 983 < 1022
    mkfatfs_clustersearch: Cannot format FAT16 at 1 sectors/cluster
    mkfatfs_configfatfs: Sector size:          512 bytes
    mkfatfs_configfatfs: Number of sectors:    1024 sectors
    mkfatfs_configfatfs: FAT size:             12 bits
    mkfatfs_configfatfs: Number FATs:          2
    mkfatfs_configfatfs: Sectors per cluster:  1 sectors
    mkfatfs_configfatfs: FS size:              3 sectors
    mkfatfs_configfatfs:                       985 clusters
    mkfatfs_configfatfs: Root directory slots: 512
    mkfatfs_configfatfs: Volume ID:            00000000
    mkfatfs_configfatfs: Volume Label:         "           "
    posix_spawn_exec: ERROR: exec failed: 22
    fat_mount: FAT12:
    fat_mount:      HW  sector size:     512
    fat_mount:          sectors:         1024
    fat_mount:      FAT reserved:        1
    fat_mount:          sectors:         1024
    fat_mount:          start sector:    1
    fat_mount:          root sector:     7
    fat_mount:          root entries:    512
    fat_mount:          data sector:     39
    fat_mount:          FSINFO sector:   0
    fat_mount:          Num FATs:        2
    fat_mount:          FAT sectors:     3
    fat_mount:          sectors/cluster: 1
    fat_mount:          max clusters:    985
    fat_mount:      FSI free count       -1
    fat_mount:          next free        0
    posix_spawn_exec: ERROR: exec failed: 22
    posix_spawn_exec: ERROR: exec failed: 22
    nsh> 

如前所述，dmesg 命令会清除 RAMLOG。因此再次使用时，只会显示新的调试输出：

.. code-block:: bash

    nsh> dmesg
    posix_spawn_exec: ERROR: exec failed: 22

附带说明，此配置中的 ``posix_spawn_exec`` 错误会在每个命令上发生。这是因为 NSH 首先尝试从 ``PATH`` 变量中文件系统上找到的命令执行。除非您在配置中定义了 ``CONFIG_NSH_FILE_APPS=y``，否则您不会在系统中看到此错误。
