========
命令
========

.. _cmdtest:

\`\`test\`\` 求值表达式
=============================

**命令语法：**

.. code-block:: fish

  [ <expression> ]
  test <expression>

**概述**。这是同一命令的两种替代形式。
它们支持求值布尔表达式，结果设置到 ``$?``。此命令最常用于 ``if-then[-else]-fi`` 中 ``if`` 之后的条件命令。

**表达式语法：**

::

    expression = simple-expression | !expression | expression -o expression | expression -a expression

    simple-expression = unary-expression | binary-expression

    unary-expression = string-unary | file-unary

    string-unary = -n string | -z string

    file-unary = -b file | -c file | -d file | -e file | -f file | -r file | -s file | -w file

    binary-expression = string-binary | numeric-binary

    string-binary = string = string | string == string | string != string

    numeric-binary = integer -eq integer | integer -ge integer | integer -gt integer | integer -le integer | integer -lt integer | integer -ne integer

.. _cmdaddroute:

\`\`addroute\`\` 添加路由表条目
======================================

**命令语法：**

::

  addroute <target> [<netmask>] <router>
  addroute default <ipaddr> <interface>

**概述**。此命令在路由表中添加一个条目。新条目将本地网络上的路由器 IP 地址（<router>）映射到由 <target> IP 地址和网络掩码 <netmask> 标识的外部网络。

网络掩码也可以使用 IPv4 CIDR 或 IPv6 斜杠表示法来表示。在这种情况下，不需要提供网络掩码。

**示例：**

::

  nsh> addroute 11.0.0.0 255.255.255.0 10.0.0.2

等价于

::

  nsh> addroute 11.0.0.0/24 10.0.0.2

addroute 命令的第二种形式可用于设置默认网关。

.. _cmdarp:

\`\`arp\`\` 访问 ARP 表
============================

**命令语法：**::

  arp [-t|-a <ipaddr> |-d <ipaddr> |-s <ipaddr> <hwaddr>]

**概述**：访问操作系统 ARP 表。

  -a <ipaddr>           显示 IP 地址 <ipaddr> 映射到的硬件地址。
  -d <ipaddr>           从 ARP 表中删除 IP 地址 <ipaddr> 的映射。
  -s <ipaddr hwaddr>    设置（或替换）IP 地址 <ipaddr> 到硬件地址 <hwaddr> 的映射。
  -t                    转储 ARP 表的全部内容。此选项仅在启用 ``CONFIG_NETLINK_ROUTE`` 时可用。

**示例：**::

  nsh> arp -a 10.0.0.1
  nsh: arp: no such ARP entry: 10.0.0.1

  nsh> arp -s 10.0.0.1 00:13:3b:12:73:e6
  nsh> arp -a 10.0.0.1
  HWAddr: 00:13:3b:12:73:e6

  nsh> arp -d 10.0.0.1
  nsh> arp -a 10.0.0.1
  nsh: arp: no such ARP entry: 10.0.0.1

.. _cmdbase64dec:

\`\`base64dec\`\` Base64 解码
===========================

**命令语法：**::

  base64dec [-w] [-f] <string or filepath>

**概述**。*待提供。*

.. _cmdbase64enc:

\`\`base64enc\`\` Base64 编码
===========================

**命令语法：**::

  base64enc [-w] [-f] <string or filepath>

**概述**。*待提供。*

.. _cmdbasename:

\`\`basename\`\` 提取基础文件/目录名
=============================================

**命令语法：**::

  basename <path> [<suffix>]

**概述**。从 ``<path>`` 中提取最终字符串，方法是删除前面的路径段，并（可选地）删除尾部的 ``<suffix>``。

.. _cmdbreak:

\`\`break\`\` 终止循环
==========================

**命令语法：**::

  break

**概述**。``break`` 命令仅在 ``while`` 或 ``until`` 循环体内的 ``do`` 和 ``done`` 标记之间有意义。在循环外部，``break`` 命令不执行任何操作。如果在循环体内执行 ``break`` 命令，循环将立即终止，执行将继续到 ``done`` 标记之后的下一条命令。

.. _cmdcat:

\`\`cat\`\` 连接文件
=========================

**命令语法：**::

  cat <path> [<path> [<path> ...]]

**概述**。此命令将 ``<path>`` 处的所有文件复制并连接到控制台（如果输出被重定向则到另一个文件）。

.. _cmdcd:

\`\`cd\`\` 切换当前工作目录
=======================================

**命令语法：**::

  cd [<dir-path>|-|~|..]

**概述**。更改当前工作目录（``PWD``）。同时设置上一个工作目录环境变量（``OLDPWD``）。

**形式：**

==================  =====================================
``cd <dir-path>``   将当前工作目录设置为 <dir-path>。
``cd -``            将当前工作目录设置为上一个工作目录（$OLDPWD）。等同于 cd $OLDPWD。
``cd`` 或 ``cd ~``  将当前工作目录设置为"主"目录。主目录可通过在配置文件中设置 CONFIG_LIBC_HOMEDIR 来配置。默认主目录为 /。
``cd ..`` \t        将当前工作目录设置为父目录。
==================  =====================================

.. _cmdchmod:

\`\`chmod\`\` 更改文件权限
==================================

**命令语法：**::

  chmod <octal-mode> <path>

**概述**。更改 ``<path>`` 的权限位。仅支持数字（八进制）模式。

**示例：**::

  nsh> chmod 600 /tmp/secret
  nsh> chmod 755 /usr/bin/app

.. _cmdchown:

\`\`chown\`\` 更改文件所有者和组
======================================

**命令语法：**::

  chown <uid>[:gid] <path>

**概述**。更改 ``<path>`` 的所有者和/或组。只接受数字 uid 和 gid 值。省略的 uid 或 gid 字段保持不变。

**形式：**

===================  ===============================================================
``chown uid:gid``    设置所有者为 uid，组为 gid。
``chown uid``        设置所有者为 uid；组不变。
``chown uid:``       设置所有者为 uid；组不变。
``chown :gid``       设置组为 gid；所有者不变。
===================  ===============================================================

**示例：**::

  nsh> chown 1000:1000 /tmp/file
  nsh> chown 0: /tmp/file
  nsh> chown :100 /tmp/file

.. _cmdcmp:

\`\`cmp\`\` 比较文件
=====================

**命令语法：**::

  cmp <path1> <path2>

**概述**。比较 ``<path1>`` 处文件与 ``<path2>`` 处文件的内容。仅在文件不同时返回指示。

.. _cmdcp:

\`\`cp\`\` 复制文件
=================

**命令语法：**::

  cp <source-path> <dest-path>

**概述**。将 ``<source-path>`` 处文件的内容复制到 ``<dest-path>`` 指定的位置。

.. _cmddate:

\`\`date\`\` 显示或设置日期和时间
======================================

**命令语法：**::

  date [-s "MMM DD HH:MM:SS YYYY"] [-u] [+%format]

**概述**。显示或设置当前日期和时间，使用 ``-u`` 选项可设置 UTC，支持 ``+%format`` 格式化输出。

要显示当前系统时间和日期，输入 ``date`` 命令。输出显示星期几、月份中的天数、月份、年份、当前时间。使用 24 小时制。
只使用一种格式，显示和设置日期/时间时均如此。
要手动更改系统时钟，输入 ``date -s MMM DD HH:MM:SS YYYY``。

  -  ``MMM``  月份缩写（如 Sep）。
  -           空格分隔符。
  -  ``DD``   月份中的天数（如 01）。
  -           空格分隔符。
  -  ``HH``   小时（00-23）。
  -  ``:``    冒号分隔符。
  -  ``MM``   分钟（00-59）。
  -  ``:``    冒号分隔符。
  -  ``SS``   秒（00-60）。
  -           空格分隔符。
  -  ``YYYY`` 年份（如 2023）。

**示例：**::

  nsh> date
  Thu, Jan 01 00:00:17 1970
  nsh> date -s "Sep 15 11:30:00 2023"
  nsh> date
  Fri, Sep 15 11:30:03 2023

.. _cmddd:

\`\`dd\`\` 复制和转换文件
=============================

**命令语法：**::

  dd if=<infile> of=<outfile> [bs=<sectsize>] [count=<sectors>] [skip=<sectors>]

**概述**。从 <infile> 复制块到 <outfile>。<infile> 或 <outfile> 可以是标准文件、字符设备或块设备的路径。示例如下：

从字符设备读取，写入常规文件。这将创建一个指定大小、用零填充的新文件：::

  nsh> ls -l /dev
  /dev:
   crw-rw-rw-       0 zero
  nsh> dd if=/dev/zero of=/tmp/zeros bs=64 count=16
  nsh> ls -l /tmp
  /tmp:
   -rw-rw-rw-    1024 ZEROS

从字符设备读取，写入块设备。这将用零填充整个块设备：::

  nsh> ls -l /dev
  /dev:
   brw-rw-rw-       0 ram0
   crw-rw-rw-       0 zero
  nsh> dd if=/dev/zero of=/dev/ram0

从块设备读取，写入字符设备。这将读取整个块设备并将内容转储到位桶中：::

  nsh> ls -l /dev
  /dev:
   crw-rw-rw-       0 null
   brw-rw-rw-       0 ram0
  nsh> dd if=/dev/ram0 of=/dev/null

.. _cmddelroute:

\`\`delroute\`\` 删除路由表条目
=========================================

**命令语法：**::

  delroute <target> [<netmask>]

**概述**。删除的条目将是路由表中第一个匹配由 <target> IP 地址和网络掩码 <netmask> 标识的外部网络的条目。

网络掩码也可以使用 IPv4 CIDR 或 IPv6 斜杠表示法来表示。在这种情况下，不需要提供网络掩码。

**示例：**::

  nsh> delroute 11.0.0.0 255.255.255.0

等价于：::

  nsh> delroute 11.0.0.0/24

.. _cmddf:

\`\`df\`\` 显示卷状态
=========================

**命令语法：**::

  df [-h]

**概述**。显示每个已挂载卷的状态。示例：::

  nsh> mount
    /etc type romfs
    /tmp type vfat
  nsh> df
    Block  Number
    Size   Blocks     Used Available Mounted on
      64        6        6         0 /etc
     512      985        2       983 /tmp
  nsh>

如果在 NuttX 配置中定义了 ``CONFIG_NSH_CMDOPT_DF_H``，则 ``df`` 还将支持 ``-h`` 选项，可用于以人类可读的格式显示卷信息。

.. _cmddirname:

\`\`dirname\`\` 提取文件/目录的路径
============================================

**命令语法：**::

  dirname <path>

**概述**。通过删除最终的目录或文件名，提取指向完整 ``<path>`` 的路径字符串。

.. _cmddmesg:

\`\`dmesg\`\` 转储缓冲的 SYSLOG 输出
=====================================

**命令语法：**::

  dmesg

**概述**。此命令可用于转储（并清除）任何缓冲的 syslog 输出消息的内容。此命令仅在启用 ``CONFIG_RAMLOG_SYSLOG`` 时可用。在这种情况下，syslog 输出将收集到内存中的循环缓冲区中。输入 ``dmesg`` 命令将把该内存循环缓冲区的内容转储到 NSH 控制台输出。``dmesg`` 会清除缓冲数据，因此再次输入 ``dmesg`` 将只显示新缓冲的数据。

.. _cmdecho:

\`\`echo\`\` 回显字符串和变量
===================================

**命令语法：**::

  echo [-n] [<string|$name> [<string|$name>...]]

**概述**。将字符串序列和展开的环境变量复制到控制台输出（如果输出被重定向则到文件）。

``-n`` 选项抑制尾部的换行符。

.. _cmdenv:

\`\`env\`\` 显示环境变量
==================================

**命令语法：**::

  env

**概述**。显示环境中的当前名称-值对。示例：::

  nsh> env
  PATH=/bin

  nsh> set foo bar
  nsh> env
  PATH=/bin
  foo=bar

  nsh> unset PATH
  nsh> env
  foo=bar

  nsh>

.. note::NSH 本地变量\ *不会*\ 由 ``env`` 命令显示。

.. _cmdexec:

\`\`exec\`\` 执行用户代码
==========================

**命令语法：**::

  exec <hex-address>

**概述**。执行地址 ``<hex-address>`` 处的用户逻辑。NSH 将暂停直到执行完成，除非通过 ``exec <hex-address> &`` 在后台执行用户逻辑。

.. _cmdexit:

\`\`exit\`\` 退出 NSH
=================

**命令语法：**::

  exit

**概述**。退出 NSH。对于串口前端，仅在你已启动其他任务（可能使用 ``exec`` 命令）且希望 NSH 不再占用时有用。对于 telnet 前端，``exit`` 终止 telnet 会话。

.. _cmdexport:

\`\`export\`\` 设置环境变量
======================================

**命令语法：**::

  export <name> [<value>]

**概述**。``export`` 命令设置环境变量，或将 NSH 变量提升为环境变量。示例如下：

  #. 使用 ``export`` 将 NSH 变量提升为环境变量：::

        nsh> env
        PATH=/bin

        nsh> set foo bar
        nsh> env
        PATH=/bin

        nsh> export foo
        nsh> env
        PATH=/bin
        foo=bar

     创建了一个与本地 NSH 变量具有相同值的组级环境变量；本地 NSH 变量被删除。

        .. note::此行为与 Bash shell 不同。Bash 会保留本地 Bash 变量，该变量将遮蔽同名同值的环境变量。

  #. 使用 ``export`` 设置环境变量：::

      nsh> export dog poop
      nsh> env
      PATH=/bin
      foo=bar
      dog=poop

除非同时设置 ``CONFIG_NSH_VARS=y`` 且 ``CONFIG_DISABLE_ENVIRON`` 未设置，否则 NSH 不支持 ``export`` 命令。

.. _cmdexpr:

\`\`expr\`\` 求值表达式
=============================

**命令语法：**::

  expr <operand1> <operator> <operand2>

**概述**。这是 expr 命令的迷你版本，实现了加、减、乘、除和取模功能。

**示例：**

  nsh> expr 5 - 2
  3
  nsh> set hello 10
  nsh> expr $hello - 2
  8
  nsh> expr 8 a 9
  Unknown operator
  nsh> expr 20 / 5
  4
  nsh> expr 10 % 4
  2
  nsh> expr 100 + 0
  100

.. _cmdfree:

\`\`free\`\` 显示内存管理器状态
===================================

**命令语法：**::

  free

**概述**。显示内存分配器的当前状态。示例：::

  nsh> free
               total       used       free    largest  nused  nfree
  Mem:       5583024    1614784    3968240    3967792    244      4

  nsh>

**各列含义：**

=======  ======================================
total \t 为 malloc 分配使用的总内存大小（字节）。
used     malloc 分配出去的已占用内存块总大小（字节）。
free     空闲（未使用）内存块的总大小（字节）。
largest  最大空闲（未使用）内存块的大小。
nused    已分配内存块的数量。
nfree    空闲内存块的数量。
=======  ======================================

.. _cmdget:

\`\`get\`\` 通过 TFTP 获取文件
=========================

**命令语法：**::

  get [-b|-n] [-f <local-path>] -h <ip-address> <remote-path>

**概述**。从 IP 地址由 ``<ip-address>`` 标识的主机复制 ``<remote-address>`` 处的文件。

**其他选项**

===================  ============================================
``-f <local-path>``  除非提供 <local-path>，否则文件将保存到当前工作目录。
``-n``               选择文本（"netascii"）传输模式（默认）。
``-b``               选择二进制（"octet"）传输模式。
===================  ============================================

.. _cmdhelp:

\`\`help\`\` 显示命令用法
=================================

**命令语法：**::

  help [-v] [<cmd>]

**概述**。在控制台显示 NSH 命令的摘要信息。

**选项**

========= ====================
``-v``    显示完整命令用法的详细输出。
``<cmd>`` 仅显示此命令的完整用法。
========= ====================

.. _cmdhexdump:

\`\`hexdump\`\` 文件或设备的十六进制转储
==============================================

**命令语法：**::

  hexdump <file or device> [skip=<bytes>] [count=<bytes>]

**概述**。以十六进制格式从文件或字符设备转储数据。

================= ==================================
``skip=<bytes>``  将从开头跳过 <bytes> 字节。
``count=<bytes>`` 转储 <bytes> 字节后停止。
================= ==================================

``skip`` 和 ``count`` 选项仅在 NuttX 配置中定义了 ``CONFIG_NSH_CMDOPT_HEXDUMP`` 时可用。

.. _cmdifconfig:

\`\`ifconfig\`\` 管理网络配置
=========================================

**命令语法：**::

  ifconfig [nic_name [<ip-address>|dhcp]] [dr|gw|gateway <dr-address>] [netmask <net-mask>] [dns <dns-address>] [hw <hw-mac>]]

**概述**。``ifconfig`` 命令支持多种形式：

  #. 带一个或不带参数时，``ifconfig`` 将显示网络的当前配置，以及可能的以太网设备状态：::

       ifconfig
       ifconfig [nic_name]

     示例：::

       nsh> ifconfig
       eth0    HWaddr 00:18:11:80:10:06
               IPaddr:10.0.0.2 DRaddr:10.0.0.1 Mask:255.255.255.0

     如果启用了网络统计（``CONFIG_NET_STATISTICS``），此命令还将显示网络的详细状态。

  #. 如果同时提供了网络接口名称和 IP 地址作为参数，``ifconfig`` 将设置以太网设备的地址：::

      ifconfig nic_name ip_address

  #. 其他形式\ *待提供*\

.. note::此命令依赖于系统中配置了 *procfs* 文件系统。*procfs* 文件系统还必须通过以下命令挂载：::

    nsh> mount -t procfs /proc

.. _cmdifdown:

\`\`ifdown\`\` 关闭网络
==============================

**命令语法：**::

  ifdown <interface>

**概述**。关闭由 <interface> 名称标识的接口。

**示例：**::

  ifdown eth0

.. _cmdifup:

\`\`ifup\`\` 启动网络
===========================

**命令语法：**::

  ifup <interface>

**概述**。启动由 <interface> 名称标识的接口。

**示例：**::

  ifup eth0

.. _cmdinsmod:

\`\`insmod\`\` 安装操作系统模块
===============================

**命令语法：**::

  insmod <file-path> <module-name>

**概述**。将 <file-path> 处的可加载操作系统模块安装为 <module-name> 模块。

**示例：**::

  nsh> ls -l /mnt/romfs
  /mnt/romfs:
   dr-xr-xr-x       0 .
   -r-xr-xr-x    9153 chardev
  nsh> ls -l /dev
  /dev:
   crw-rw-rw-       0 console
   crw-rw-rw-       0 null
   brw-rw-rw-       0 ram0
   crw-rw-rw-       0 ttyS0
  nsh> lsmod
  NAME                 INIT   UNINIT      ARG     TEXT     SIZE     DATA     SIZE
  nsh> insmod /mnt/romfs/chardev mydriver
  nsh> ls -l /dev
  /dev:
   crw-rw-rw-       0 chardev
   crw-rw-rw-       0 console
   crw-rw-rw-       0 null
   brw-rw-rw-       0 ram0
   crw-rw-rw-       0 ttyS0
  nsh> lsmod
  NAME                 INIT   UNINIT      ARG     TEXT     SIZE     DATA     SIZE
  mydriver         20404659 20404625        0 20404580      552 204047a8        0

.. _cmdirqinfo:

\`\`irqinfo\`\` 显示中断状态
=================================

**命令语法：**::

  irqinfo

**概述**。显示所有已连接中断的当前中断计数。

**示例：**::

  nsh> irqinfo
  IRQ HANDLER  ARGUMENT    COUNT    RATE
    3 00001b3d 00000000        156   19.122
   15 0000800d 00000000        817  100.000
   30 00000fd5 20000018         20    2.490

.. _cmdcritmon:

\`\`critmon\`\` 显示临界区监控状态
========================================

**命令语法：**::

  critmon

**概述**。显示系统中每个线程的抢占时间、临界区时间、最长单次运行时间、总运行时间、进程 ID（PID）和线程描述。

**示例：**::

  nsh> critmon
  PRE-EMPTION   CSECTION      RUN         TIME         PID   DESCRIPTION
  0.010265000   0.000037000   ----------- ------------ ----  CPU 0
  0.000000000   0.000000000   0.001237000 28.421047000 0     Idle Task
  0.000011000   0.000037000   0.000046000 0.034211000  1     loop_task
  0.000000000   0.000028000   0.000067000 0.236657000  2     hpwork

在此示例中，输出显示了系统中每个线程的抢占时间、临界区时间、最长单次运行时间、总运行时间和线程描述。

``critmon`` 命令的输出显示以下列：

- PRE-EMPTION：抢占时间
- CSECTION：临界区时间
- RUN：线程的最长单次运行时间
- TIME：线程的总运行时间
- PID：线程的进程 ID
- DESCRIPTION：线程描述（名称）

.. _cmdkill:

\`\`kill\`\` 向任务发送信号
================================

**命令语法：**::

  kill -<signal> <pid>

**概述**。向由 <pid> 标识的任务发送 <signal> 信号。

**示例：**::

  nsh> mkfifo /dev/fifo
  nsh> cat /dev/fifo &
  cat [2:128]
  nsh> ps
  PID PRI POLICY   TYPE    NPX STATE    EVENT     SIGMASK  COMMAND
    0   0 FIFO     Kthread --- Ready              00000000 Idle Task
    1 128 RR       Task    --- Running            00000000 init
    2 128 FIFO     pthread --- Waiting  Semaphore 00000000 <pthread>(51ea50)
  nsh> kill -9 2
  nsh> ps
  PID PRI POLICY   TYPE    NPX STATE    EVENT     SIGMASK  COMMAND
    0   0 FIFO     Kthread --- Ready              00000000 Idle Task
    1 128 RR       Task    --- Running            00000000 init
  nsh>

.. note::NuttX 不支持完整的 POSIX 信号系统。系统中存在一些标准信号名称，如 ``SIGCHLD``、``SIGUSR1``、``SIGUSR2``、``SIGALRM`` 和 ``SIGPOLL``。但它们不具有你可能期望的默认操作。NuttX 仅支持所谓的 POSIX 实时信号。这些信号可用于与运行中的任务通信、可用于等待中的任务等。

  如果启用了配置选项 ``CONFIG_SIG_DEFAULT``，则将支持 ``SIGINT`` 和 ``SIGKILL`` 信号（仅此两个）的默认操作。在这种情况下，``kill -9``（SIGKILL）确实会终止任务。但应谨慎使用，因为在某些构建配置中清理不足，可能会导致内存泄漏和资源悬空。

.. _cmdlosetup:

\`\`losetup\`\` 设置/拆除回环设备
==========================================

**命令语法 1：**::

  losetup [-o <offset>] [-r] <dev-path> <file-path>

**概述**。设置 <dev-path> 处的回环设备，以将 <file-path> 处的文件作为块设备访问。在以下示例中，创建了一个 256K 的文件（``dd``），并使用 ``losetup`` 使该文件可作为块设备访问。创建了 FAT 文件系统（``mkfatfs``）并挂载（``mount``）。然后可以在回环挂载的文件上管理文件：::

  nsh> dd if=/dev/zero of=/tmp/image bs=512 count=512
  nsh> ls -l /tmp
  /tmp:
   -rw-rw-rw-   262144 IMAGE
  nsh> losetup /dev/loop0 /tmp/image
  nsh> ls -l /dev
  /dev:
   brw-rw-rw-       0 loop0
  nsh> mkfatfs /dev/loop0
  nsh> mount -t vfat /dev/loop0 /mnt/example
  nsh> ls -l /mnt
  ls -l /mnt
  /mnt:
   drw-rw-rw-       0 example/
  nsh> echo "This is a test" >/mnt/example/atest.txt
  nsh> ls -l /mnt/example
  /mnt/example:
   -rw-rw-rw-      16 ATEST.TXT
  nsh> cat /mnt/example/atest.txt
  This is a test
  nsh>

**命令语法 2：**::

  losetup d <dev-path>

**概述**。拆除 <dev-path> 处回环设备的设置。

.. _cmdln:

\`\`ln\`\` 创建文件或目录链接
==================================

**命令语法：**::

  ln [-s] <target> <link>

**概述**。``ln`` 命令将在 <link> 处为已存在的文件或目录 <target> 创建新的符号链接。此实现针对 NuttX 进行了简化：

  -  链接只能在 NuttX 顶层:ref:`伪文件系统 <file_system_overview>` 中创建。NuttX 目前支持的文件系统不提供符号链接。
  -  出于相同原因，仅实现了软链接。
  -  文件权限被忽略。
  -  ``c_time`` 不会更新。

.. _cmdls:

\`\`ls\`\` 列出目录内容
==============================

**命令语法：**::

  ls [-lRsh] <dir-path>

**概述**。显示 ``<dir-path>`` 处目录的内容。注意：``<dir-path>`` 必须指向目录，而非其他文件系统对象。

**选项**

======  ================================
``-R`` \t显示指定目录及其所有子目录的内容。
``-s`` \t在列表中显示文件的大小和文件名。
``-l`` \t在列表中显示大小和模式信息以及文件名。
``-h`` \t以人类可读的格式在列表中显示大小和模式信息以及文件名。
======  ================================

.. _cmdlsmod:

\`\`lsmod\`\` 显示已安装的操作系统模块信息
=====================================================

**命令语法：**::

  lsmod

**概述**。显示当前已安装的操作系统模块信息。此信息包括：

  -  安装时分配给模块的模块名称（``NAME``，字符串）。
  -  模块初始化函数的地址（``INIT``，十六进制）。
  -  模块反初始化函数的地址（``UNINIT``，十六进制）。
  -  将传递给模块反初始化函数的参数（``ARG``，十六进制）。
  -  .text 内存区域的起始地址（``TEXT``，十六进制）。
  -  .text 内存区域的大小（``SIZE``，十进制）。
  -  .bss/.data 内存区域的起始地址（``DATA``，十六进制）。
  -  .bss/.data 内存区域的大小（``SIZE``，十进制）。

**示例：**::

  nsh> lsmod
  NAME                 INIT   UNINIT      ARG     TEXT     SIZE     DATA     SIZE
  mydriver         20404659 20404625        0 20404580      552 204047a8        0

.. _cmdmd5:

\`\`md5\`\` 计算 MD5
=====================

**命令语法：**::

  md5 [-f] <string or filepath>

**概述**。*待提供。*

.. _cmdmx:

\`\`mb\`\`、\`\`mh\`\` 和 \`\`mw\`\` 访问内存
============================================

**命令语法：**::

  mb <hex-address>[=<hex-value>][ <hex-byte-count>]
  mh <hex-address>[=<hex-value>][ <hex-byte-count>]
  mw <hex-address>[=<hex-value>][ <hex-byte-count>]

**概述**。使用字节大小访问（mb）、16 位访问（mh）或 32 位访问（mw）来访问内存。在每种情况下，

=============================  ==============================================
``<hex-address>``              指定要访问的地址。始终读取并显示该地址的当前值。
``<hex-address>=<hex-value>``  读取值，然后将 <hex-value> 写入该位置。
``<hex-byte-count>``           对总共 <hex-byte-count> 字节执行 mb、mh 或 mw 操作，每次访问后适当地递增 <hex-address>。
=============================  ==============================================

**示例：**::

  nsh> mh 0 16
    0 = 0x0c1e
    2 = 0x0100
    4 = 0x0c1e
    6 = 0x0110
    8 = 0x0c1e
    a = 0x0120
    c = 0x0c1e
    e = 0x0130
    10 = 0x0c1e
    12 = 0x0140
    14 = 0x0c1e
  nsh>

.. _cmdps:

\`\`ps\`\` 显示当前任务和线程
=====================================

**命令语法：**::

  ps

**概述**。显示当前活动的线程和任务。示例：::

  nsh> ps
  PID PRI POLICY   TYPE    NPX STATE    EVENT     SIGMASK  COMMAND
    0   0 FIFO     Kthread --- Ready              00000000 Idle Task
    1 128 RR       Task    --- Running            00000000 init
    2 128 FIFO     Task    --- Waiting  Semaphore 00000000 nsh_telnetmain()
    3 100 RR       pthread --- Waiting  Semaphore 00000000 <pthread>(21)
  nsh>

注意：此命令依赖于系统中配置了 *procfs* 文件系统。*procfs* 文件系统还必须通过以下命令挂载：::

  nsh> mount -t procfs /proc

.. _cmdmkdir:

\`\`mkdir\`\` 创建目录
============================

**命令语法：**::

  mkdir <path>

**概述**。在 ``<path>`` 处创建目录。除最终目录名外，``<path>`` 的所有组成部分必须已存在于已挂载的文件系统中；最终目录必须不存在。

**仅限于已挂载的文件系统**。回想一下，NuttX 使用:ref:`伪文件系统 <file_system_overview>` 作为其根文件系统。``mkdir`` 命令只能用于在通过:ref:`mount <cmdmount>` 命令设置的卷中创建目录；不能用于在*伪*文件系统中创建目录。

**示例：**::

  nsh> mkdir /mnt/fs/tmp
  nsh> ls -l /mnt/fs
  /mnt/fs:
   drw-rw-rw-       0 TESTDIR/
   drw-rw-rw-       0 TMP/
  nsh>

.. _cmdmkfatfs:

\`\`mkfatfs\`\` 创建 FAT 文件系统
====================================

**命令语法**

  mkfatfs [-F <fatsize>] [-r <rootdirentries>] <block-driver>

**概述**。在 ``<block-driver>`` 路径指定的块设备上格式化 FAT 文件系统。FAT 大小可作为选项提供。不使用 ``<fatsize>`` 选项时，``mkfatfs`` 将选择 FAT12 或 FAT16 格式。由于历史原因，如果需要 FAT32 格式，必须在命令行中明确指定。

``-r`` 选项可用于选择 FAT12 和 FAT16 文件系统根目录中的条目数。小卷的典型值为 112 或 224；大卷（如硬盘或非常大的 SD 卡）应使用 512。所有情况下默认为 512 个条目。

FAT32 报告的根目录条目数为零，因为 FAT32 根目录是一个簇链。

NSH 提供此命令以访问 ``mkfatfs()`` NuttX API。此块设备必须位于 NuttX :ref:`伪文件系统 <file_system_overview>` 中，并且必须已通过 ``register_blockdriver()`` 的调用创建（参见 ``include/nuttx/fs/fs.h``）。

.. _cmdmkfifo:

\`\`mkfifo\`\` 创建 FIFO
========================

**命令语法：**::

  mkfifo <path>

**概述**。在伪文件系统中的任意位置创建 FIFO 字符设备，创建完成 ``<path>`` 所需的任何伪目录。但按照惯例，设备驱动程序放置在标准的 ``/dev`` 目录中。创建后，FIFO 设备可像其他设备驱动程序一样使用。NSH 提供此命令以访问 ``mkfifo()`` NuttX API。

**示例：**::

  nsh> ls -l /dev
  /dev:
   crw-rw-rw-       0 console
   crw-rw-rw-       0 null
   brw-rw-rw-       0 ram0
  nsh> mkfifo /dev/fifo
  nsh> ls -l /dev
  ls -l /dev
  /dev:
   crw-rw-rw-       0 console
   crw-rw-rw-       0 fifo
   crw-rw-rw-       0 null
   brw-rw-rw-       0 ram0
  nsh>

.. _cmdmkrd:

\`\`mkrd\`\` 创建 RAMDISK
=========================

**命令语法：**::

  mkrd [-m <minor>] [-s <sector-size>] <nsectors>

**概述**。创建由 ``<nsectors>`` 个扇区组成的 ramdisk，每个扇区大小为 ``<sector-size>``（如果未指定 ``<sector-size>`` 则为 512 字节）。ramdisk 将注册为 ``/dev/ram<minor>``。如果未指定 ``<minor>``，``mkrd`` 将尝试将 ramdisk 注册为 ``/dev/ram0``。

**示例：**::

  nsh> ls /dev
  /dev:
   console
   null
   ttyS0
   ttyS1
  nsh> mkrd 1024
  nsh> ls /dev
  /dev:
   console
   null
   ram0
   ttyS0
   ttyS1
  nsh>

创建 ramdisk 后，可以使用 ``mkfatfs`` 命令格式化，使用 ``mount`` 命令挂载。

**示例：**::

  nsh> mkrd 1024
  nsh> mkfatfs /dev/ram0
  nsh> mount -t vfat /dev/ram0 /tmp
  nsh> ls /tmp
  /tmp:
  nsh>

.. _cmdmount:

\`\`mount\`\` 挂载文件系统
=============================

**命令语法：**::

  mount -t <fstype> [-o <options>] <block-device> <dir-path>

**概述**。``mount`` 命令执行两种不同操作之一。如果 ``mount`` 命令后没有参数，则 ``mount`` 命令将在控制台枚举所有当前挂载点。

如果在 ``mount`` 命令后提供了挂载参数，则 ``mount`` 命令将在 NuttX 伪文件系统中挂载文件系统。``mount`` 执行三向关联，绑定：

  #. **文件系统。**'-t ``<fstype>``' 选项标识 ``<block-device>`` 上已格式化的文件系统类型。截至目前，``vfat`` 是 ``<fstype>`` 的唯一支持值。
  #. **块设备。**``<block-device>`` 参数是:ref:`伪文件系统 <file_system_overview>` 中块驱动 inode 的完整或相对路径。按照惯例，这是 ``/dev`` 子目录下的名称。此 ``<block-device>`` 必须已预先格式化为 ``<fstype>`` 指定的相同文件系统类型。
  #. **挂载点。**挂载点 ``<dir-path>`` 是:ref:`伪文件系统 <file_system_overview>` 中已挂载卷将出现的位置。此挂载点只能位于 NuttX:ref:`伪文件系统 <file_system_overview>` 中。按照惯例，此挂载点是 ``/mnt`` 下的子目录。mount 命令将创建完成完整路径所需的任何伪目录，但完整路径不能已存在。

卷挂载到 NuttX:ref:`伪文件系统 <file_system_overview>` 后，可以像访问文件系统中的其他对象一样访问它。

**示例：**

使用 ``mount`` 挂载文件系统：::

  nsh> ls -l /dev
  /dev:
   crw-rw-rw-       0 console
   crw-rw-rw-       0 null
   brw-rw-rw-       0 ram0
  nsh> ls /mnt
  nsh: ls: no such directory: /mnt
  nsh> mount -t vfat /dev/ram0 /mnt/fs
  nsh> ls -l /mnt/fs/testdir
  /mnt/fs/testdir:
   -rw-rw-rw-      15 TESTFILE.TXT
  nsh> echo "This is a test" >/mnt/fs/testdir/example.txt
  nsh> ls -l /mnt/fs/testdir
  /mnt/fs/testdir:
  -rw-rw-rw-      15 TESTFILE.TXT
   -rw-rw-rw-      16 EXAMPLE.TXT
  nsh> cat /mnt/fs/testdir/example.txt
  This is a test
  nsh>

使用 ``mount`` 枚举挂载点：::

  nsh> mount
    /etc type romfs
    /mnt/fs type vfat
    /tmp type vfat

.. _cmdmv:

\`\`mv\`\` 重命名文件
====================

**命令语法：**::

  mv <old-path> <new-path>

**概述**。将 ``<old-path>`` 处的文件对象重命名为 ``<new-path>``。两个路径必须位于同一已挂载的文件系统中。

.. _cmdnfsmount:

\`\`nfsmount\`\` 挂载 NFS 文件系统
=====================================

**命令语法：**::

  nfsmount <server-address> <mount-point> <remote-path>

**概述**。将远程 NFS 服务器目录 <remote-path> 挂载到目标机器的 <mount-point>。<server-address> 是远程服务器的 IP 地址。

.. _cmdnslookup:

\`\`nslookup\`\` 查询网络地址
=====================================

**命令语法：**::

  nslookup <host-name>

**概述**。查询并打印与 ``<host-name>`` 关联的 IP 地址。

.. _cmdpasswd:

\`\`passwd\`\` 更改用户密码
===================================

**命令语法：**::

  passwd <username> <password>

**概述**。将已有用户 <username> 的密码设置为 <password>。

.. _cmdpmconfig:

\`\`pmconfig\`\` 管理电源管理子系统
==============================================

**命令语法：**::

  pmconfig [stay|relax] [normal|idle|standby|sleep]

**概述**。控制电源管理子系统。

.. _cmdpoweroff:

\`\`poweroff\`\` 关闭系统
=================================

**命令语法：**::

  poweroff [<n>]

**概述**。立即关闭系统并断电。此命令依赖于板级特定的硬件支持来关闭系统。可选的十进制数字参数可用于向板级特定的关机逻辑提供关机模式。

注意：同时支持 ``poweroff`` 和 ``shutdown`` 命令是冗余的。

.. _cmdput:

\`\`put\`\` 通过 TFTP 发送文件
==========================

**命令语法：**::

  put [-b|-n] [-f <remote-path>] -h <ip-address> <local-path>

**概述**。将 ``<local-address>`` 处的文件复制到 IP 地址由 ``<ip-address>`` 标识的主机。

**其他选项：**

====================  =============================================
``-f <remote-path>``  除非提供 <remote-path>，否则文件将以相同名称保存到主机上。
``-b|-n``             选择二进制（"octet"）或文本（"netascii"）传输模式。默认：文本。
====================  =============================================

.. _cmdpwd:

\`\`pwd\`\` 显示当前工作目录
======================================

**命令语法：**::

  pwd

**概述**。显示当前工作目录：::

  nsh> cd /dev
  nsh> pwd
  /dev
  nsh>

等同于 ``echo $PWD``：::

  nsh> echo $PWD
  /dev
  nsh>

.. _cmdreadlink:

\`\`readlink\`\` 显示链接目标
==================================

**命令语法：**::

  readlink <link>

**概述**。显示 ``<link>`` 路径处软链接的目标。

.. _cmdreboot:

\`\`reboot\`\` 重启系统
============================

**命令语法：**::

  reboot [<n>]

**概述**。立即重置并重启系统。此命令依赖于硬件支持来重置系统。可选的十进制数字参数 <n> 可用于向板级特定的重启逻辑提供重启模式。

注意：同时支持 ``reboot`` 和 ``shutdown`` 命令是冗余的。

.. _cmdrm:

\`\`rm\`\` 删除文件
====================

**命令语法：**::

  rm <file-path>

**概述**。从已挂载的文件系统中删除指定的 ``<file-path>`` 名称。回想一下，NuttX 使用:ref:`伪文件系统 <file_system_overview>` 作为其根文件系统。``rm`` 命令只能用于删除（取消链接）通过:ref:`mount <cmdmount>` 命令设置的卷中的文件；不能用于删除*伪*文件系统中的名称。

**示例：**::

  nsh> ls /mnt/fs/testdir
  /mnt/fs/testdir:
   TESTFILE.TXT
   EXAMPLE.TXT
  nsh> rm /mnt/fs/testdir/example.txt
  nsh> ls /mnt/fs/testdir
  /mnt/fs/testdir:
   TESTFILE.TXT
  nsh>

.. _cmdrmdir:

\`\`rmdir\`\` 删除目录
============================

**命令语法：**::

  rmdir <dir-path>

**概述**。从已挂载的文件系统中删除指定的 ``<dir-path>`` 目录。回想一下，NuttX 使用:ref:`伪文件系统 <file_system_overview>` 作为其根文件系统。``rmdir`` 命令只能用于删除通过:ref:`mount <cmdmount>` 命令设置的卷中的目录；不能用于删除*伪*文件系统中的目录。

**示例：**::

  nsh> mkdir /mnt/fs/tmp
  nsh> ls -l /mnt/fs
  /mnt/fs:
   drw-rw-rw-       0 TESTDIR/
   drw-rw-rw-       0 TMP/
  nsh> rmdir /mnt/fs/tmp
  nsh> ls -l /mnt/fs
  /mnt/fs:
   drw-rw-rw-       0 TESTDIR/
  nsh>

.. _cmdrmmod:

\`\`rmmod\`\` 移除操作系统模块
=============================

**命令语法：**::

  rmmod <module-name>

**概述**。移除名为 <module-name> 的可加载操作系统模块。注意：操作系统模块只能在不忙时移除。

**示例：**::

  nsh> lsmod
  NAME                 INIT   UNINIT      ARG     TEXT     SIZE     DATA     SIZE
  mydriver         20404659 20404625        0 20404580      552 204047a8        0
  nsh> rmmod mydriver
  nsh> lsmod
  NAME                 INIT   UNINIT      ARG     TEXT     SIZE     DATA     SIZE
  nsh>

.. _cmdroute:

\`\`route\`\` 显示路由表
============================

**命令语法：**::

  route ipv4|ipv6

**概述**。显示 IPv4 或 IPv6 的路由表内容。

如果仅启用了 IPv4 或 IPv6，则参数是可选的，但如果提供，必须匹配已启用的互联网协议版本。

.. _cmdrptun:

\`\`rptun\`\` 启动/停止 OpenAMP RPC 隧道
===========================================

**命令语法：**::

  rptun start|stop <dev-path>

**概述**。启动或停止 <dev-path> 处的 OpenAMP RPC 隧道设备。

.. _cmdset:

\`\`set\`\` 设置变量
======================

**命令语法：**::

  set [{+|-}{e|x|xe|ex}] [<name> <value>]

**概述**。将变量 ``<name>`` 设置为字符串 ``<value>``，和/或设置 NSH 解析器控制选项。

例如，可以这样设置变量：::

  nsh> echo $foobar

  nsh> set foobar foovalue
  nsh> echo $foobar
  foovalue
  nsh>

如果选择了 ``CONFIG_NSH_VARS``，此 ``set`` 命令的效果是设置本地 NSH 变量。否则，将设置组级环境变量。

如果本地 NSH 变量已通过:ref:`export <cmdexport>` *提升*为环境变量，则 ``set`` 命令将设置环境变量的值，而非本地 NSH 变量。

.. note::Bash shell 的工作方式不同。Bash 会将本地 Bash 变量和同名环境变量的值都设置为相同值。

如果选择了 ``CONFIG_NSH_VARS=y`` 且未提供参数，则 ``set`` 命令将列出所有本地 NSH 变量：::

  nsh> set
  foolbar=foovalue

设置在 NSH 中解析脚本时的*出错退出控制*和/或*打印命令跟踪*。设置从执行点开始生效，直到再次更改，或者对于初始化脚本，设置在退出时恢复为默认设置。包含的子脚本将使用父级的设置运行，在子脚本中所做的更改在返回时会影响父级。

  -  使用 ``set -e`` 启用，``set +e`` 禁用（忽略）命令的退出条件。默认为 -e。错误会导致脚本退出。

  -  使用 ``set -x`` 启用，``set +x`` 禁用（静默）在执行脚本命令时打印跟踪。默认为 ``+x``：不打印脚本命令的执行跟踪。

示例 1 - 命令未找到时不退出：::

  set +e
  notacommand

示例 2 - 命令未找到时退出：::

  set -e
  notacommand

示例 3 - 命令未找到时退出，并打印脚本命令的跟踪：::

  set -ex

示例 4 - 命令未找到时退出，打印脚本命令的跟踪，并将 foobar 设置为 foovalue：::

  set -ex foobar foovalue
  nsh> echo $foobar
  foovalue

.. _cmdsh:

\`\`sh\`\` 执行 NSH 脚本
============================

**命令语法：**::

  sh <script-path>

**概述**。执行 ``<script-path>`` 所指向文件中的 NSH 命令序列。

.. _cmdshutdown:

\`\`shutdown\`\` 关闭系统
=================================

**命令语法：**::

  shutdown [--reboot]

**概述**。关闭系统并断电，或者可选地重置并立即重启系统。此命令依赖于硬件支持来关闭或重置系统；可能支持其中一种、两种或都不支持。

注意：``shutdown`` 命令复制了 ``poweroff`` 和 ``reboot`` 命令的行为。

.. _cmdsleep:

\`\`sleep\`\` 等待秒数
==========================

**命令语法：**::

  sleep <sec>

**概述**。暂停执行（休眠）``<sec>`` 秒。

.. _cmdtelnetd:

\`\`telnetd\`\` 启动 Telnet 守护进程
========================================

**命令语法：**::

  telnetd

**概述**。如果 Telnet 守护进程尚未运行，则启动它。

Telnet 守护进程可以通过编程方式调用 ``nsh_telnetstart()`` 启动，也可以使用此 ``telnetd`` 命令从 NSH 命令行启动。

通常，如果没有 ``CONFIG_SYSTEM_TELNETD``，此命令将被抑制，因为 Telnet 守护进程在 ``nsh_main.c`` 中自动启动。例外情况是选择了 ``CONFIG_NSH_NETLOCAL`` 时。在这种情况下，网络不会在初始化时启用，而必须从 NSH 命令行或通过其他应用程序启用。

在这种情况下，当在网络初始化之前调用 ``nsh_telnetstart()`` 时，它将失败。

.. _cmdtime:

\`\`time\`\` 计时执行另一个命令
==========================================

**命令语法：**::

  time "<command>"

**概述**。执行命令计时。此命令将执行后面的 <command> 字符串，然后显示执行该命令所需的时间。时间显示分辨率为 100 微秒，这可能超出许多配置的分辨率。注意，如果 <command> 包含空格或其他分隔符，必须用引号括起来。

**示例：**::

  nsh> time "sleep 2"

  2.0100 sec
  nsh>

此示例中额外的 10 毫秒是由于 sleep 命令的工作方式：它总是比请求的多等待一个系统时钟节拍，而此测试设置使用了 10 毫秒的周期系统定时器。误差来源可能包括各种量化误差、CPU 竞争使用，以及 time 命令执行本身的额外开销（已包含在总计中）。

报告的时间是从命令开始到命令完成的经过时间。此经过时间不一定只是命令的处理时间。例如，它可能包括中断级处理。在繁忙的系统中，如果被其他更高优先级的线程抢占 CPU 时间，命令处理可能会被延迟。因此，报告的时间包括从命令开始到结束的所有 CPU 处理，可能包括该时间间隔内不相关的处理时间。

注意：::

  nsh> time "sleep 2 &"
  sleep [3:100]

  0.0000 sec
  nsh>

由于 sleep 命令在后台执行，sleep 命令几乎立即完成。与以下在后台运行 time 命令和 sleep 命令的情况相反：::

  nsh> time "sleep 2" &
  time [3:100]
  nsh>
  2.0100 sec

.. _cmdtruncate:

\`\`truncate\`\` 设置文件大小
===================================

**命令语法：**::

  truncate -s <length> <file-path>

**概述**。将 <file-path> 处常规文件的大小缩小或扩展到指定的 <length>。

不存在的 <file-path> 参数将被创建。<length> 选项不是可选的。

如果 <file-path> 大于指定大小，多余的数据将丢失。如果 <file-path> 较短，将被扩展，扩展部分读取为零字节。

.. _cmdumount:

\`\`umount\`\` 卸载文件系统
================================

**命令语法：**::

  umount [-f] <dir-path>

**概述**。卸载挂载点 ``<dir-path>`` 处的文件系统。``umount`` 命令只能用于卸载先前使用:ref:`mount <cmdmount>` 命令挂载的卷。

**选项**

======  ======================================================
``-f``  即使文件系统繁忙也强制卸载。
======  ======================================================

**示例：**::

  nsh> ls /mnt/fs
  /mnt/fs:
   TESTDIR/
  nsh> umount /mnt/fs
  nsh> ls /mnt/fs
  /mnt/fs:
  nsh: ls: no such directory: /mnt/fs
  nsh>

.. _cmduname:

\`\`uname\`\` 打印系统信息
==================================

**命令语法：**::

  uname [-a | -imnoprsv]

**概述**。打印某些系统信息。不带选项时，输出与 -s 相同。

==========  ========================================
``-a``      打印所有信息，按以下顺序，如果未知则省略 -p 和 -i：
``-s, -o``  打印操作系统名称（NuttX）
``-n``      打印网络节点主机名（仅在 CONFIG_NET=y 时可用）
``-r``      打印内核发行版本
``-v``      打印内核版本
``-m``      打印机器硬件名称
``-i``      打印机器平台名称
``-p``      打印 "unknown"
==========  ========================================

.. _cmdunset:

\`\`unset\`\` 取消设置环境变量
=======================================

**命令语法：**

  unset <name>

**概述**。删除与变量 ``<name>`` 关联的值。这将从 NSH 本地变量和组级环境变量中删除名称-值对。例如：::

  nsh> echo $foobar
  foovalue
  nsh> unset foobar
  nsh> echo $foobar

  nsh>

.. _cmduptime:

\`\`uptime\`\` 显示系统运行时间
====================================================

**命令语法：**

  uptime [-sph]

**概述**。显示以下信息：当前时间、系统已运行时间，以及过去 1、5 和 15 分钟的平均负载。

**选项**

======  ================================
``-p`` \t以美观格式显示运行时间。
``-s`` \t系统自何时起运行。
``-h`` \t显示此帮助并退出。
======  ================================

.. _cmdurldecode:

\`\`urldecode\`\` URL 解码
========================

**命令语法：**::

  urldecode [-f] <string or filepath>

**概述**。*待提供。*

.. _cmdurlencode:

\`\`urlencode\`\` URL 编码
========================

**命令语法：**::

  urlencode [-f] <string or filepath>

**概述**。*待提供。*

.. _cmduseradd:

\`\`useradd\`\` 添加新用户
==========================

**命令语法：**::

  useradd <username> <password>

**概述**。添加具有 <username> 和 <password> 的新用户。

.. _cmduserdel:

\`\`userdel\`\` 删除用户
=========================

**命令语法：**::

  userdel <username>

**概述**。删除名为 <username> 的用户。

.. _cmdusleep:

\`\`usleep\`\` 等待微秒
================================

**命令语法：**::

  usleep <usec>

**概述**。暂停执行（休眠）``<usec>`` 微秒。

.. _cmdwget:

\`\`wget\`\` 通过 HTTP 获取文件
==========================

**命令语法**

  wget [-o <local-path>] <url>

**概述**。使用 HTTP 将 ``<url>`` 处的文件复制到当前目录。

**选项**

===================  =================================================
``-o <local-path>``  除非提供 <local-path>，否则文件将保存到当前工作目录，并使用与 HTTP 服务器上相同的名称。
===================  =================================================

.. _cmdxd:

\`\`xd\`\` 内存的十六进制转储
=================================

**命令语法：**::

  xd <hex-address> <byte-count>

**概述**。从地址 ``<hex-address>`` 转储 ``<byte-count>`` 字节的数据。

**示例：**::

  nsh> xd 410e0 512
  Hex dump:
  0000: 00 00 00 00 9c 9d 03 00 00 00 00 01 11 01 10 06 ................
  0010: 12 01 11 01 25 08 13 0b 03 08 1b 08 00 00 02 24 ....%..........$
  ...
  01f0: 08 3a 0b 3b 0b 49 13 00 00 04 13 01 01 13 03 08 .:.;.I..........
  nsh>

内置命令
=================

除了上面列出的属于 NSH 的命令外，还可以有额外的外部*内置*应用程序添加到 NSH 中。这些是独立的可执行程序，但看起来就像 NSH 的一部分命令。从用户角度来看，主要区别在于内置应用程序的帮助信息不能直接从 NSH 获取。你需要使用 ``-h`` 选项执行应用程序来获取有关使用内置应用程序的帮助。

``apps/`` 仓库中有几个内置应用程序。这里不打算枚举所有这些。但下面列出了一些更常见、更有用的内置应用程序。

.. _cmdping:

\`\`ping\`\` 和 \`\`ping6\`\` 检查网络对等体
=========================================

**命令语法：**::

  ping  [-c <count>] [-i <interval>] <ip-address>
  ping6 [-c <count>] [-i <interval>] <ip-address>

**概述**。测试与远程对等体的网络通信。示例：::

  nsh> ping 10.0.0.1
  PING 10.0.0.1 56 bytes of data
  56 bytes from 10.0.0.1: icmp_seq=1 time=0 ms
  56 bytes from 10.0.0.1: icmp_seq=2 time=0 ms
  56 bytes from 10.0.0.1: icmp_seq=3 time=0 ms
  56 bytes from 10.0.0.1: icmp_seq=4 time=0 ms
  56 bytes from 10.0.0.1: icmp_seq=5 time=0 ms
  56 bytes from 10.0.0.1: icmp_seq=6 time=0 ms
  56 bytes from 10.0.0.1: icmp_seq=7 time=0 ms
  56 bytes from 10.0.0.1: icmp_seq=8 time=0 ms
  56 bytes from 10.0.0.1: icmp_seq=9 time=0 ms
  56 bytes from 10.0.0.1: icmp_seq=10 time=0 ms
  10 packets transmitted, 10 received, 0% packet loss, time 10190 ms
  nsh>

``ping6`` 与 ``ping`` 的不同之处在于它使用 IPv6 寻址。
