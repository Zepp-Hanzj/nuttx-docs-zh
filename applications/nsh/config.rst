.. |br| raw:: html

   <br/>

======================
配置设置
======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

上述命令的可用性取决于 NuttX 配置文件中可能启用或未启用的功能。
以下 :ref:`cmdtable <cmddependencies>` 指示了每个命令对 NuttX 配置设置的依赖关系。
一般配置设置在 NuttX 移植指南中讨论。
NSH 特定的配置设置在本文档的 :ref:`cmdbottom <nshconfiguration>` 部分讨论。

请注意，除了通用的 NuttX 配置设置之外，每个 NSH 命令都可以通过最右边列中的设置
单独禁用。所有这些设置使 NSH 的配置可能变得复杂，但也允许其压缩到非常小的内存占用中。

.. _cmddependencies:

命令对配置设置的依赖关系
==============================================

====================== =========================================== ======================
命令                   依赖的配置                                  可通过以下方式禁用
====================== =========================================== ======================
``[``                  ! ``CONFIG_NSH_DISABLESCRIPT``              ``CONFIG_NSH_DISABLE_TEST``
:ref:`cmdaddroute`     ``CONFIG_NET`` && ``CONFIG_NET_ROUTE``      ``CONFIG_NSH_DISABLE_ADDROUTE``
:ref:`cmdarp`          ``CONFIG_NET`` && ``CONFIG_NET_ARP``        ``CONFIG_NSH_DISABLE_ARP``
:ref:`cmdbase64dec`    ``CONFIG_NETUTILS_CODECS`` &&               ``CONFIG_NSH_DISABLE_BASE64DEC``
                       ``CONFIG_CODECS_BASE64``
:ref:`cmdbase64enc`    ``CONFIG_NETUTILS_CODECS`` &&               ``CONFIG_NSH_DISABLE_BASE64ENC``
                       ``CONFIG_CODECS_BASE64``
:ref:`cmdbasename`     .                                           ``CONFIG_NSH_DISABLE_BASENAME``
:ref:`cmdbreak`        ! ``CONFIG_NSH_DISABLESCRIPT`` &&           .
                       ! ``CONFIG_NSH_DISABLE_LOOPS``  
:ref:`cmdcat`          ``CONFIG_NSH_DISABLE_CAT``                  .
:ref:`cmdcd`           ! ``CONFIG_DISABLE_ENVIRON``                ``CONFIG_NSH_DISABLE_CD``
:ref:`cmdcmp`          ``CONFIG_NSH_DISABLE_CMP``                  .
:ref:`cmdcp`           ``CONFIG_NSH_DISABLE_CP``                   .
:ref:`cmddate`         ``CONFIG_NSH_DISABLE_DATE``                 .
:ref:`cmddelroute`     ``CONFIG_NET`` && ``CONFIG_NET_ROUTE``      ``CONFIG_NSH_DISABLE_DELROUTE``
:ref:`cmddf`           ! ``CONFIG_DISABLE_MOUNTPOINT``             ``CONFIG_NSH_DISABLE_DF``
:ref:`cmddirname`      ``CONFIG_NSH_DISABLE_DIRNAME``              .
:ref:`cmddmesg`        ``CONFIG_RAMLOG_SYSLOG``                    ``CONFIG_NSH_DISABLE_DMESG``
:ref:`cmdecho`         ``CONFIG_NSH_DISABLE_ECHO``                 .
:ref:`cmdenv`          ``CONFIG_FS_PROCFS`` &&                     ``CONFIG_NSH_DISABLE_ENV``
                       ! ``CONFIG_DISABLE_ENVIRON`` && |br|
                       ! ``CONFIG_PROCFS_EXCLUDE_ENVIRON``
:ref:`cmdexec`         ``CONFIG_NSH_DISABLE_EXEC``                 .
:ref:`cmdexit`         ``CONFIG_NSH_DISABLE_EXIT``                 .
:ref:`cmdexport`       ``CONFIG_NSH_VARS`` &&
                       ! ``CONFIG_DISABLE_ENVIRON``                ``CONFIG_NSH_DISABLE_EXPORT``
:ref:`cmdfree`         ``CONFIG_NSH_DISABLE_FREE``                 .
:ref:`cmdget`          ``CONFIG_NET`` && ``CONFIG_NET_UDP`` &&      ``CONFIG_NSH_DISABLE_GET``
                       *MTU* >= 58\ [#1]_
:ref:`cmdhelp`  [#3]_  ``CONFIG_NSH_DISABLE_HELP``                 .
:ref:`cmdhexdump`      ``CONFIG_NSH_DISABLE_HEXDUMP``              .
:ref:`cmdifconfig`     ``CONFIG_NET`` && ``CONFIG_FS_PROCFS`` &&    ``CONFIG_NSH_DISABLE_IFCONFIG``
                       ! ``CONFIG_FS_PROCFS_EXCLUDE_NET``
:ref:`cmdifdown`       ``CONFIG_NET`` && ``CONFIG_FS_PROCFS`` &&   ``CONFIG_NSH_DISABLE_IFUPDOWN``
                       ! ``CONFIG_FS_PROCFS_EXCLUDE_NET``
:ref:`cmdifup`         ``CONFIG_NET`` && ``CONFIG_FS_PROCFS`` &&
                       ! ``CONFIG_FS_PROCFS_EXCLUDE_NET``          ``CONFIG_NSH_DISABLE_IFUPDOWN``
:ref:`cmdinsmod`       ``CONFIG_MODULE``                           ``CONFIG_NSH_DISABLE_MODCMDS``
:ref:`cmdirqinfo`      ! ``CONFIG_DISABLE_MOUNTPOINT`` &&          .
                       ``CONFIG_FS_PROCFS`` && |br|
                       ``CONFIG_SCHED_IRQMONITOR``
:ref:`cmdkill`         ``CONFIG_NSH_DISABLE_KILL``                 .
:ref:`cmdlosetup`      ! ``CONFIG_DISABLE_MOUNTPOINT`` &&          ``CONFIG_NSH_DISABLE_LOSETUP``
                       ``CONFIG_DEV_LOOP``
:ref:`cmdln`           ``CONFIG_PSEUDOFS_SOFTLINKS``               ``CONFIG_NSH_DISABLE_LN``
:ref:`cmdls`           ``CONFIG_NSH_DISABLE_LS``                   .
:ref:`cmdlsmod`        ``CONFIG_MODULE`` && ``CONFIG_FS_PROCFS``   ``CONFIG_NSH_DISABLE_MODCMDS``
                       && |br|
                       ! ``CONFIG_FS_PROCFS_EXCLUDE_MODULE``
:ref:`cmdmd5`          ``CONFIG_NETUTILS_CODECS`` &&               ``CONFIG_NSH_DISABLE_MD5``
                       ``CONFIG_CODECS_HASH_MD5``
:ref:`cmdmx`           .                                           ``CONFIG_NSH_DISABLE_MB``, |br|
                                                                   ``CONFIG_NSH_DISABLE_MH``, |br|
                                                                   ``CONFIG_NSH_DISABLE_MW``
:ref:`cmdmkdir`        (! ``CONFIG_DISABLE_MOUNTPOINT`` \|\|       ``CONFIG_NSH_DISABLE_MKDIR``
                       ! ``CONFIG_DISABLE_PSEUDOFS_OPERATIONS``)
:ref:`cmdmkfatfs`      ! ``CONFIG_DISABLE_MOUNTPOINT`` &&          ``CONFIG_NSH_DISABLE_MKFATFS``
                       ``CONFIG_FSUTILS_MKFATFS``
:ref:`cmdmkfifo`       ``CONFIG_PIPES`` &&                         ``CONFIG_NSH_DISABLE_MKFIFO``
                       ``CONFIG_DEV_FIFO_SIZE`` > 0
:ref:`cmdmkrd`         ! ``CONFIG_DISABLE_MOUNTPOINT``             ``CONFIG_NSH_DISABLE_MKRD``
:ref:`cmdmount`        ! ``CONFIG_DISABLE_MOUNTPOINT``             ``CONFIG_NSH_DISABLE_MOUNT``
:ref:`cmdmv`           ! ``CONFIG_DISABLE_MOUNTPOINT`` \|\|        ``CONFIG_NSH_DISABLE_MV``
                       ! ``CONFIG_DISABLE_PSEUDOFS_OPERATIONS``
:ref:`cmdnfsmount`     ! ``CONFIG_DISABLE_MOUNTPOINT`` &&          ``CONFIG_NSH_DISABLE_NFSMOUNT``
                       ``CONFIG_NET`` && ``CONFIG_NFS``
:ref:`cmdnslookup`     ``CONFIG_LIBC_NETDB`` &&                    ``CONFIG_NSH_DISABLE_NSLOOKUP``
                       ``CONFIG_NETDB_DNSCLIENT``
:ref:`cmdpasswd`       ! ``CONFIG_DISABLE_MOUNTPOINT`` &&          ``CONFIG_NSH_DISABLE_PASSWD``
                       ``CONFIG_NSH_LOGIN_PASSWD``
:ref:`cmdpmconfig`     ``CONFIG_PM``                               ``CONFIG_NSH_DISABLE_PMCONFIG``
:ref:`cmdpoweroff`     ``CONFIG_BOARDCTL_POWEROFF``                ``CONFIG_NSH_DISABLE_POWEROFF``
:ref:`cmdps`           ``CONFIG_FS_PROCFS`` &&                     ``CONFIG_NSH_DISABLE_PS``
                       ! ``CONFIG_FS_PROCFS_EXCLUDE_PROC``
:ref:`cmdput`          ``CONFIG_NET`` && ``CONFIG_NET_UDP`` &&     ``CONFIG_NSH_DISABLE_PUT``
                       ``MTU >= 558`` [#1]_, [#2]_
:ref:`cmdpwd`          !  ``CONFIG_DISABLE_ENVIRON``               ``CONFIG_NSH_DISABLE_PWD``
:ref:`cmdreadlink`     ``CONFIG_PSEUDOFS_SOFTLINKS``               ``CONFIG_NSH_DISABLE_READLINK``
:ref:`cmdreboot`       ``CONFIG_BOARD_RESET``                      ``CONFIG_NSH_DISABLE_REBOOT``
:ref:`cmdrm`           ! ``CONFIG_DISABLE_MOUNTPOINT`` \|\|        ``CONFIG_NSH_DISABLE_RM``
                       ! ``CONFIG_DISABLE_PSEUDOFS_OPERATIONS``
:ref:`cmdrmdir`        ! ``CONFIG_DISABLE_MOUNTPOINT`` \|
                       ! ``CONFIG_DISABLE_PSEUDOFS_OPERATIONS``    ``CONFIG_NSH_DISABLE_RMDIR``
:ref:`cmdrmmod`        ``CONFIG_MODULE``                           ``CONFIG_NSH_DISABLE_MODCMDS``
:ref:`cmdroute`        ``CONFIG_FS_PROCFS`` &&                     ``CONFIG_NSH_DISABLE_ROUTE``
                       ``CONFIG_FS_PROCFS_EXCLUDE_NET`` && |br|
                       ! ``CONFIG_FS_PROCFS_EXCLUDE_ROUTE`` &&
                       ``CONFIG_NET_ROUTE`` && |br|
                       ! ``CONFIG_NSH_DISABLE_ROUTE`` && |br|
                       (``CONFIG_NET_IPv4`` \|
                       ``CONFIG_NET_IPv6``)
:ref:`cmdrptun`        ``CONFIG_RPTUN``                            ``CONFIG_NSH_DISABLE_RPTUN``
:ref:`cmdset`          ``CONFIG_NSH_VARS`` \|\|                    ``CONFIG_NSH_DISABLE_SET``
                       ! ``CONFIG_DISABLE_ENVIRON``
:ref:`cmdshutdown`     ``CONFIG_BOARDCTL_POWEROFF`` \|\|           ``CONFIG_NSH_DISABLE_SHUTDOWN``
                       ``CONFIG_BOARD_RESET``
:ref:`cmdsleep`        .                                           ``CONFIG_NSH_DISABLE_SLEEP``
``cmdsource``          ``CONFIG_FILE_STREAM`` &&                   ``CONFIG_NSH_DISABLE_SOURCE``
                       ! ``CONFIG_NSH_DISABLESCRIPT``
:ref:`cmdtelnetd`      ``CONFIG_NSH_TELNET`` &&
                       ``CONFIG_SYSTEM_TELNETD``
:ref:`cmdtest`         !  ``CONFIG_NSH_DISABLESCRIPT``             ``CONFIG_NSH_DISABLE_TEST``
:ref:`cmdtime`         .                                           ``CONFIG_NSH_DISABLE_TIME``
:ref:`cmdtruncate`     ! ``CONFIG_DISABLE_MOUNTPOINT``             ``CONFIG_NSH_DISABLE_TRUNCATE``
:ref:`cmdumount`       !  ``CONFIG_DISABLE_MOUNTPOINT``            ``CONFIG_NSH_DISABLE_UMOUNT``
:ref:`cmduname`        .                                           ``CONFIG_NSH_DISABLE_UNAME``
:ref:`cmdunset`        ``CONFIG_NSH_VARS`` \|\|                    ``CONFIG_NSH_DISABLE_UNSET``
                       !  ``CONFIG_DISABLE_ENVIRON``
:ref:`cmdurldecode`    ! ``CONFIG_NETUTILS_CODECS`` &&             ``CONFIG_NSH_DISABLE_URLDECODE``
                       ``CONFIG_CODECS_URLCODE``
:ref:`cmdurlencode`    ! ``CONFIG_NETUTILS_CODECS`` &&             ``CONFIG_NSH_DISABLE_URLENCODE``
                       ``CONFIG_CODECS_URLCODE``
:ref:`cmduseradd`      ! ``CONFIG_DISABLE_MOUNTPOINT`` &&          ``CONFIG_NSH_DISABLE_USERADD``
                       ``CONFIG_NSH_LOGIN_PASSWD``
:ref:`cmduserdel`      ! ``CONFIG_DISABLE_MOUNTPOINT`` &&          ``CONFIG_NSH_DISABLE_USERDEL``
                       ``CONFIG_NSH_LOGIN_PASSWD``
:ref:`cmdusleep`       .                                           ``CONFIG_NSH_DISABLE_USLEEP``
:ref:`cmdwget`         ``CONFIG_NET`` && ``CONFIG_NET_TCP``        ``CONFIG_NSH_DISABLE_WGET``
:ref:`cmdxd`           .                                           ``CONFIG_NSH_DISABLE_XD``
====================== =========================================== ======================

.. [#1] 由于硬件填充，实际所需的数据包大小可能更大
.. [#2] 可能需要特殊的 TFTP 服务器启动选项以允许创建文件，以便 ``put`` 命令正确操作。
.. [#3] 通过定义 ``CONFIG_NSH_HELP_TERSE`` 可以抑制详细的帮助输出。在这种情况下，help 命令仍然可用，但会稍微小一些。

内置命令对配置设置的依赖关系
=======================================================

所有内置应用程序都需要启用 NSH 内置应用程序的支持。此支持通过
``CONFIG_BUILTIN=y`` 和 ``CONFIG_NSH_BUILTIN_APPS=y`` 启用。

=============  ==================================================================================================
命令           依赖的配置
=============  ==================================================================================================
``ping``       ``CONFIG_NET`` && ``CONFIG_NET_ICMP`` && ``CONFIG_NET_ICMP_SOCKET`` && ``CONFIG_SYSTEM_PING``
``ping6``      ``CONFIG_NET`` && ``CONFIG_NET_ICMPv6`` && ``CONFIG_NET_ICMPv6_SOCKET`` && ``CONFIG_SYSTEM_PING6``
=============  ==================================================================================================

.. _nshconfiguration:

NSH 特定配置设置
===================================

NSH 的行为可以通过 ``boards/<arch>/<chip>/<board>/defconfig`` 文件中的以下设置进行修改：

===================================  ==================================
配置                                 描述
===================================  ==================================
 ``CONFIG_NSH_READLINE``             选择 ``readline()`` 的最小实现。
                                     此最小实现仅提供退格键进行命令行编辑。
                                     它期望终端提供一些最小的 VT100 命令支持。

 ``CONFIG_NSH_CLE``                  选择更广泛的类似 EMACS 的命令行编辑器。
                                     仅在以下情况下选择此选项：(1) 您不介意 FLASH
                                     占用适度增加，(2) 您使用支持广泛 VT100 编辑
                                     命令的终端。选择此选项可能会增加约 1.5-2KB
                                     的 FLASH 占用。

 ``CONFIG_NSH_BUILTIN_APPS``         支持外部注册的"内置"应用程序，可从 NSH 命令行
                                     执行（有关更多信息，请参阅 apps/README.txt）。
                                     这需要 ``CONFIG_BUILTIN`` 以启用 NuttX 对
                                     "内置"应用程序的支持。

 ``CONFIG_NSH_BUILTIN_AS_COMMAND``   如果启用，则"内置"应用程序将直接从 NSH 命令行
                                     执行而不创建单独的线程。优点是更简单、更快的执行。
                                     缺点是不支持后台执行。这需要 ``CONFIG_BUILTIN``
                                     和 ``CONFIG_NSH_BUILTIN_APPS`` 以启用 NuttX 对
                                     "内置"应用程序的支持。

 ``CONFIG_NSH_FILEIOSIZE``           用于文件访问的静态 I/O 缓冲区大小（如果没有文件
                                     系统则忽略）。默认值为 1024。

 ``CONFIG_NSH_STRERROR``             ``strerror(errno)`` 产生更可读的输出，但
                                     ``strerror()`` 非常大，除非此设置为 *y*，
                                     否则不会使用。此设置依赖于 ``strerror()``
                                     已通过 ``CONFIG_LIBC_STRERROR`` 启用。

 ``CONFIG_NSH_DISABLE_SEMICOLON``    默认情况下，您可以在一行上输入多个 NSH 命令，
                                     每个命令之间用分号分隔。您可以禁用此功能以在
                                     FLASH 受限的平台上节省一些内存。
                                     默认值：n

 ``CONFIG_NSH_CMDPARMS``             如果选中，则命令、文件应用程序和 NSH 内置命令
                                     的输出可以用作其他命令的参数。要执行的实体通过
                                     将命令行括在反引号中来标识。例如::

                                       set FOO `myprogram $BAR`

                                     将执行名为 ``myprogram`` 的程序，将环境变量
                                     ``BAR`` 的值传递给它。环境变量 ``FOO`` 的值
                                     随后被设置为 ``myprogram`` 在 ``stdout`` 上的
                                     输出。由于此功能占用大量资源，因此默认禁用。
                                     ``CONFIG_NSH_CMDPARMS`` 中间输出将保留在临时
                                     文件中。临时文件目录的完整路径取自
                                     ``CONFIG_LIBC_TMPDIR``，如果未设置
                                     ``CONFIG_LIBC_TMPDIR``，则默认为 ``/tmp``。

 ``CONFIG_NSH_MAXARGUMENTS``         NSH 命令参数的最大数量。默认值：6

 ``CONFIG_NSH_ARGCAT``               支持将字符串与环境变量或命令输出连接。例如::

                                       set FOO XYZ
                                       set BAR 123
                                       set FOOBAR ABC_${FOO}_${BAR}

                                     将把环境变量 ``FOO`` 设置为 ``XYZ``，``BAR``
                                     设置为 ``123``，``FOOBAR`` 设置为 ``ABC_XYZ_123``。
                                     如果未选中 ``CONFIG_NSH_ARGCAT``，则 FLASH 占用
                                     会略微减小，但命令行上只能使用简单的环境变量如 ``$FOO``。

 ``CONFIG_NSH_VARS``                 默认情况下，没有内部 NSH 变量。NSH 将使用操作系统
                                     环境变量进行所有变量存储。如果选中此选项，NSH 还
                                     将支持本地 NSH 变量。这些变量在很大程度上是透明的，
                                     工作方式与操作系统环境变量相同。区别在于当您创建
                                     新任务时，所有环境变量都会被创建的任务继承。NSH
                                     本地变量则不会。如果启用此选项（且未设置
                                     ``CONFIG_DISABLE_ENVIRON``），则将启用名为 'export'
                                     的新命令。export 命令的工作方式与 set 命令非常相似，
                                     只是它操作环境变量。当启用 CONFIG_NSH_VARS 时，
                                     某些命令的行为会发生变化。
                                     参见以下 :ref:`cmdtable <nsh_vars_table>`。

 ``CONFIG_NSH_QUOTE``                启用命令中某些字符的反斜杠引用。此选项适用于使用
                                     NSH 脚本动态生成新 NSH 脚本的情况。在这种情况下，
                                     命令必须被视为简单文本字符串，不解释任何特殊字符。
                                     ``$``、:literal:`\\`、``"`` 等特殊字符必须作为测试
                                     字符串的一部分保持完整。此选项当前仅在同时选中了
                                     ``CONFIG_NSH_ARGCAT`` 时可用。

 ``CONFIG_NSH_NESTDEPTH``            允许的最大嵌套 ``if-then[-else]-fi`` <#conditional>`__
                                     序列数。默认值：3

 ``CONFIG_NSH_DISABLESCRIPT``        可以设置为 *y* 以抑制脚本支持。此设置禁用
                                     ```sh`` <#cmdsh>`__、```test`` <#cmdtest>`__ 和
                                     ```[`` <#cmtest>`__ 命令以及
                                     ```if-then[-else]-fi`` <#conditional>`__ 构造。
                                     这仅在最小占用是必需的且脚本不是的系统上设置。

 ``CONFIG_NSH_DISABLE_ITEF``         如果启用了脚本，则可以选择此选项以抑制脚本中
                                     ``if-then-else-fi`` 序列的支持。这仅在需要一些
                                     最小脚本但不需要 ``if-then-else-fi`` 的系统上设置。

 ``CONFIG_NSH_DISABLE_LOOPS``        如果启用了脚本，则可以选择此选项以抑制脚本中
                                     ``for while-do-done`` 和 ``until-do-done`` 序列
                                     的支持。这仅在需要一些最小脚本但不需要循环的
                                     系统上设置。

 ``CONFIG_NSH_DISABLEBG``            可以设置为 *y* 以抑制后台命令的支持。此设置禁用
                                     ```nice`` <#cmdoverview>`__ 命令前缀和
                                     ```&`` <#cmdoverview>`__ 命令后缀。这仅在最小占用
                                     是必需的且不需要后台命令执行的系统上设置。

 ``CONFIG_NSH_MMCSDMINOR``           如果架构支持 MMC/SD 插槽且存在 NSH 架构特定逻辑，
                                     此选项将提供 MMC/SD 次设备号，即 MMC/SD 块驱动程序
                                     将注册为 ``/dev/mmcsd``\\ *N*，其中 *N* 是次设备号。
                                     默认值为零。

 ``CONFIG_NSH_CONSOLE``              如果 ``CONFIG_NSH_CONSOLE`` 设置为 *y*，则选择串口
                                     控制台前端。

                                     通常，串口控制台设备是 UART 和 RS-232 接口。但是，
                                     如果定义了 ``CONFIG_USBDEV``，则可以使用 USB 串口
                                     设备替代，前提是定义了以下之一：

                                     -  ``CONFIG_PL2303`` 和 ``CONFIG_PL2303_CONSOLE``。
                                        将 Prolifics PL2303 仿真设置为 ``/dev/console``
                                        处的控制台设备。
                                     -  ``CONFIG_CDCACM`` 和 ``CONFIG_CDCACM_CONSOLE``。
                                        将 CDC/ACM 串口设备设置为 ``/dev/console`` 处的
                                        控制台设备。
                                     -  ``CONFIG_NSH_USBCONSOLE``。如果定义，则可以使用
                                        任意 USB 设备作为 NSH 控制台。在这种情况下，
                                        必须定义 ``CONFIG_NSH_USBCONDEV`` 以指示使用
                                        哪个 USB 设备作为控制台。使用 ``/dev/console``
                                        以外的设备的优点是，正常的调试输出可以使用
                                        ``/dev/console``，而 NSH 使用
                                        ``CONFIG_NSH_USBCONDEV``。

                                        ``CONFIG_NSH_USBCONDEV``。如果
                                        ``CONFIG_NSH_USBCONSOLE`` 设置为 'y'，
                                        则还必须设置 ``CONFIG_NSH_USBCONDEV``
                                        以选择用于支持 NSH 控制台的 USB 设备。这应设置为
                                        可读/可写 USB 驱动程序的带引号名称，例如：
                                        ``CONFIG_NSH_USBCONDEV="/dev/ttyACM0"``。

                                     如果有多个 USB 插槽，则可能还需要提供 USB 设备次设备号：

                                     -  ``CONFIG_NSH_UBSDEV_MINOR``：USB 设备的次设备号。默认值：0

                                     如果启用了 USB 跟踪（``CONFIG_USBDEV_TRACE``），则 NSH 将
                                     按以下请求初始化 USB 跟踪。默认值：仅跟踪 USB 错误。

                                     - ``CONFIG_NSH_USBDEV_TRACEINIT``：显示初始化事件
                                     -  ``CONFIG_NSH_USBDEV_TRACECLASS``：显示类驱动程序事件
                                     -  ``CONFIG_NSH_USBDEV_TRACETRANSFERS``：显示数据传输事件
                                     -  ``CONFIG_NSH_USBDEV_TRACECONTROLLER``：显示控制器事件
                                     -  ``CONFIG_NSH_USBDEV_TRACEINTERRUPTS``：显示中断相关事件。

 ``CONFIG_NSH_ALTCONDEV`` 和        如果 ``CONFIG_NSH_CONSOLE`` 设置 ``CONFIG_NSH_CONDEV``
                                     为 *y*，则还可以选择 ``CONFIG_NSH_ALTCONDEV``
                                     以启用使用备用字符设备来支持 NSH 控制台。如果选择了
                                     ``CONFIG_NSH_ALTCONDEV``，则 ``CONFIG_NSH_CONDEV``
                                     持有可读/可写字符驱动程序的带引号名称，例如：
                                     ``CONFIG_NSH_CONDEV="/dev/ttyS1"``。这在例如将 NSH
                                     命令行与系统控制台分离（当系统控制台用于提供调试输出时）
                                     很有用。默认值：``stdin`` 和 ``stdout``（可能是
                                     "``/dev/console``"）

                                     -  **注意 1：** 当使用 ``/dev/console`` 以外的任何其他设备
                                        作为用户界面时，(1) 换行符（``\n``）不会扩展为回车/换行
                                        （``\r\n``）。您需要配置终端程序以解决此问题。
                                        (2) 输入不会自动回显，因此您需要打开本地回显。
                                     -  **注意 2：** 此选项强制所有会话的控制台使用 NSH_CONDEV。
                                        因此，此选项仅适用于仅支持单个会话的系统。此选项特别
                                        与 Telnet 会话不兼容，因为每个 Telnet 会话必须使用
                                        不同的控制台设备。

 ``CONFIG_NSH_TELNET``               如果 ``CONFIG_NSH_TELNET`` 设置为 *y*，则选择 TELNET
                                     服务器前端。提供此选项时，您可以使用 telnet 远程登录到
                                     NuttX 以访问 NSH。
===================================  ==================================

.. _nsh_vars_table:

==================  ===================================   =============================================
CMD                 无 ``CONFIG_NSH_VARS``                有 ``CONFIG_NSH_VARS``
==================  ===================================   =============================================
``set <a> <b>``     设置环境变量 <a> 为 <b>               设置 NSH 变量 <a> 为 <b>（除非 NSH 变量已
                                                          通过 ``export`` *提升*，在这种情况下设置同名
                                                          的环境变量为 <b>）。
``set``             导致错误。                             列出所有 NSH 变量。
``unset <a>``       取消设置环境变量 <a>                   同时取消设置名称为 <a> 的环境变量和 NSH 变量
``export <a> <b>``  导致错误，                              取消设置 NSH 变量 <a>。设置环境变量 <a> 为 <b>。
``export <a>``      导致错误。                              将环境变量 <a> 设置为 NSH 变量 <a> 的值
                                                          （如果 NSH 变量未设置则为 ""）。取消设置
                                                          NSH 本地变量 <a>。
``env``             列出所有环境变量                       列出所有环境变量（*仅*环境变量）
==================  ===================================   =============================================

如果选择 Telnet 作为 NSH 控制台，则必须配置 Telnet 守护程序和 Telnet 客户端使用的资源。

===========================================  ================================
配置                                         描述
===========================================  ================================
``CONFIG_SYSTEM_TELNETD_PORT``               Telnet 守护程序将在此 TCP 端口号上监听连接。默认值：23
``CONFIG_SYSTEM_TELNETD_PRIORITY``           Telnet 守护程序的优先级。默认值：``SCHED_PRIORITY_DEFAULT``
``CONFIG_SYSTEM_TELNETD_STACKSIZE``          为 Telnet 守护程序分配的栈大小。默认值：2048
``CONFIG_SYSTEM_TELNETD_SESSION_PRIORITY``   Telnet 客户端的优先级。默认值：``SCHED_PRIORITY_DEFAULT``
``CONFIG_SYSTEM_TELNETD_SESSION_STACKSIZE``  为 Telnet 客户端分配的栈大小。默认值：2048
===========================================  ================================

必须定义 ``CONFIG_NSH_CONSOLE`` 和 ``CONFIG_NSH_TELNET`` 中的一个或两个。
如果选择了 ``CONFIG_NSH_TELNET``，则以下是一些适用的其他配置设置：

======================================  ================================
配置                                    描述
======================================  ================================
``CONFIG_NET=y``                        当然，必须启用网络。
``CONFIG_NET_TCP=y``                    Telnet 需要 TCP/IP 支持（以及各种其他
                                        TCP 相关的配置设置）。
``CONFIG_NSH_DHCPC``                    通过 DHCP 获取 IP 地址。
``CONFIG_NSH_IPADDR``                   如果未设置 ``CONFIG_NSH_DHCPC``，则必须提供静态 IP 地址。
``CONFIG_NSH_DRIPADDR``                 默认路由器 IP 地址
``CONFIG_NSH_NETMASK``                  网络掩码
``CONFIG_NSH_NOMAC``                    如果您的以太网硬件没有内置 MAC 地址则设置。如果设置，
                                        将分配一个伪造的 MAC。
``CONFIG_NSH_MAX_ROUNDTRIP``            这是 ICMP ECHO 请求响应的最大往返时间。单位为十分之一秒。
                                        默认值为 20（2 秒）。
======================================  ================================

如果您使用 DHCPC，则需要一些特殊的网络配置选项。这些包括：

============================================== ============================================================
配置                                           描述
============================================== ============================================================
``CONFIG_NET=y``                               当然，必须启用网络。
``CONFIG_NET_UDP=y``                           DHCP 需要 UDP 支持（以及各种其他
                                               UDP 相关的配置设置）。
``CONFIG_NET_BROADCAST=y``                     需要 UDP 广播支持。
``CONFIG_NET_ETH_PKTSIZE=650``（或更大）       根据 RFC2131（第 9 页），DHCP 客户端必须准备好接收
                                               最大 576 字节的 DHCP 消息（不包括以太网、IP 或 UDP
                                               头和 FCS）。注意：实际 MTU 设置将取决于具体的链路
                                               协议。这里指示的是以太网。
============================================== ============================================================

如果选择了 ``CONFIG_ETC_ROMFS``，则以下是一些适用的额外配置设置：

============================== =============================================================
配置                           描述
============================== =============================================================
``CONFIG_NSH_SYSINITSCRIPT``   这是挂载点内系统初始化脚本的相对路径。默认值是
                               ``"init.d/rc.sysinit"``。这是相对路径，不能以 '``/``'
                               开头，但必须用引号括起来。
``CONFIG_NSH_INITSCRIPT``      这是挂载点内启动脚本的相对路径。默认值是 ``"init.d/rcS"``。
                               这是相对路径，不能以 '``/``' 开头，但必须用引号括起来。
============================== =============================================================

常见问题
===============

问题::

  函数 'readline' 未定义。

常见原因：

* 您的 `defconfig` 文件中缺少以下内容::

    CONFIG_SYSTEM_READLINE=y
