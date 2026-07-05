======
PROCFS
======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是一个小型 procfs 文件系统，允许对任务或线程的少数属性进行只读访问。此小型 procfs 文件系统可以通过启用以下选项来构建到系统中::

    CONFIG_FS_PROCFS=y

然后可以通过 NSH 命令行挂载::

    nsh> mount -t procfs /proc

示例::

  NuttShell (NSH) NuttX-6.31
  nsh> mount -t procfs /proc

  nsh> ls /proc
  /proc:
   0/
   1/

  nsh> ls /proc/1
  /proc/1:
   status
   cmdline

  nsh> cat /proc/1/status
  Name:       init
  Type:       Task
  State:      Running
  Priority:   100
  Scheduler:  SCHED_FIFO
  SigMask:    00000000

  nsh> cat /proc/1/cmdline
  init

  nsh> sleep 100 &
  sleep [2:100]
  nsh> ls /proc
  ls /proc
  /proc:
   0/
   1/
   2/

  nsh> cat /proc/2/cmdline
  <pthread> 0x527420