========================*
自定义 NuttShell
========================*

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**概述。** NuttShell (NSH) 是一个简单的 shell 应用程序，可与 NuttX 一起使用。
它支持各种命令，并且（非常）松散地基于 Bash shell 和 Bash shell 编程中使用的
通用实用程序。本附录中的段落将重点介绍自定义 NSH：添加新命令、更改初始化序列等。

NSH 库和 NSH 初始化
======================================

**概述。** NSH 作为库实现，可以在 ``apps/nshlib`` 中找到。作为库，它可以被
自定义构建到遵循下面描述的 NSH 初始化序列的任何应用程序中。例如，
``apps/examples/nsh/nsh_main.c`` 中的代码说明了如何启动 NSH，其中的逻辑旨在
整合到您自己的自定义代码中。虽然代码只是作为示例生成的，但最终大多数人只是将
此示例代码用作应用程序的 ``main()`` 函数。该示例执行的初始化将在以下段落中讨论。

NSH 初始化序列
---------------------------

NSH 启动序列非常简单。例如，``apps/system/nsh/nsh_main.c`` 中的代码说明了如何
启动 NSH。它简单地执行以下操作：

  #. 此函数调用 ``nsh_initialize()``，该函数初始化 NSH 库。``nsh_initialize()``
     将在下面更详细地描述。

  #. 如果启用了 Telnet 控制台，它将调用位于 NSH 库中的 ``nsh_telnetstart()``。
     ``nsh_telnetstart()`` 将启动 Telnet 守护程序，该守护程序将监听 Telnet 连接
     并启动远程 NSH 会话。

  #. 如果启用了本地控制台（可能在串口上），则调用 ``nsh_consolemain()``。
     ``nsh_consolemain()`` 也位于 NSH 库中。``nsh_consolemain()`` 不会返回，
     因此完成了整个 NSH 初始化序列。

``nsh_initialize()``
--------------------

NSH 初始化函数 ``nsh_initialize()`` 可以在 ``apps/nshlib/nsh_init.c`` 中找到。
它只做四件事：

  #. ``nsh_romfsetc()``：如果配置如此，它将执行 NSH 系统初始化和启动脚本，
     可以在目标文件系统的 ``/etc/init.d/rc.sysinit`` 和 ``/etc/init.d/rcS`` 中找到。
     ``nsh_romfsetc()`` 函数可以在 ``apps/nshlib/nsh_romfsetc.c`` 中找到。
     此函数将 (1) 注册 ROMFS 文件系统，然后 (2) 挂载 ROMFS 文件系统。
     ``/etc`` 是 ``nsh_romfsetc()`` 挂载只读 ROMFS 文件系统的默认位置。

     ROMFS 映像本身只是构建到固件中。默认情况下，此 ``rc.sysinit`` 系统初始化脚本
     包含优先使用 TMPFS 挂载 ``/tmp`` 的逻辑，并在失败时回退到 FAT RAMDISK::

        # 在 TMPFS 上挂载 /tmp
        mount -t tmpfs XXXRDMOUNTPOINTXXX

        # 否则创建 RAMDISK 并将其挂载到 XXXRDMOUNTPOINTXXX
        mkrd -m XXXMKRDMINORXXX -s XXMKRDSECTORSIZEXXX XXMKRDBLOCKSXXX
        mkfatfs /dev/ramXXXMKRDMINORXXX
        mount -t vfat /dev/ramXXXMKRDMINORXXX XXXRDMOUNTPOINTXXX

     其中 ``XXXX*XXXX`` 字符串在创建 ROMFS 映像时在模板中被替换：

     -  ``XXXMKRDMINORXXX`` 将成为 RAM 设备次设备号。默认值：0

     -  ``XXMKRDSECTORSIZEXXX`` 将成为 RAM 设备扇区大小

     -  ``XXMKRDBLOCKSXXX`` 将成为设备中的扇区数。

     -  ``XXXRDMOUNTPOINTXXX`` 将成为配置的挂载点。默认值：``/etc``

     默认情况下，使用 FAT 回退值替换后，``rc.sysinit`` 看起来像::

        # 在 TMPFS 上挂载 /tmp
        mount -t tmpfs /tmp

        # 否则创建 RAMDISK 并将其挂载到 /tmp
        mkrd -m 1 -s 512 1024
        mkfatfs /dev/ram1
        mount -t vfat /dev/ram1 /tmp

     此脚本将：

     -  在可用时将 ``/tmp`` 挂载为 TMPFS，否则：

     -  在 ``/dev/ram1`` 创建大小为 512*1024 字节的 RAMDISK，

     -  在 ``/dev/ram1`` 的 RAM 磁盘上格式化 FAT 文件系统，然后

     -  将 FAT 文件系统挂载到配置的挂载点 ``/tmp``。

     此 ``rc.sysinit.template`` 模板文件可以在 ``apps/nshlib/rc.sysinit.template`` 中找到。
     生成的 ROMFS 文件系统可以在 ``apps/nshlib/nsh_romfsimg.h`` 中找到。

  #. ``nsh_netinit()``：``nsh_netinit()`` 函数可以在 ``apps/nshlib/nsh_netinit.c`` 中找到。

  #. 启动脚本 ``rcS`` 在系统初始化脚本之后执行，以启动一些应用程序和其他系统服务。

     此 ``rcS`` 模板文件可以在 ``apps/nshlib/rcS.template`` 中找到。
     生成的 ROMFS 文件系统可以在 ``apps/nshlib/nsh_romfsimg.h`` 中找到。

NSH 命令
============

**概述。** NSH 支持各种命令作为 NSH 程序的一部分。所有 NSH 命令都在上面
`NSH 文档 <#cmdoverview>`__ 中列出。然而，并非所有这些命令在任何时候都可用。
许多命令依赖于某些 NuttX 配置选项。您可以在 NSH 提示符下输入 help 命令来查看
实际可用的命令：

例如，如果禁用了网络支持，那么所有与网络相关的命令将不会出现在
'``nsh> help``' 列出的命令列表中。您可以在上面 `命令依赖关系表 <#cmddependencies>`__
中查看具体的命令依赖关系。

添加新 NSH 命令
-----------------------

可以非常容易地向 NSH 添加新命令。您只需添加两样东西：

  #. 您的命令的实现，以及

  #. NSH 命令表中的新条目

**命令的实现。** 例如，如果您想向 NSH 添加一个名为 ``mycmd`` 的新命令，
您需要首先使用以下原型在函数中实现 ``mycmd`` 代码：

.. code-block:: c

  int cmd_mycmd(FAR struct nsh_vtbl_s *vtbl, int argc, char **argv);

``argc`` 和 ``argv`` 用于将命令行参数传递给 NSH 命令。命令行参数以非常标准的方式
传递：``argv[0]`` 将是命令的名称，``argv[1]`` 到 ``argv[argc-1]`` 是 NSH 命令行上
提供的额外参数。

第一个参数 ``vtbl`` 是特殊的。这是指向特定于会话的状态信息的指针。您不需要知道
状态信息的内容，但当您与 NSH 逻辑交互时，确实需要传递此 ``vtbl`` 参数。
您对 ``vtbl`` 参数的唯一用途将是向控制台输出数据。您不在 NSH 命令中使用 ``printf()``。
相反，您将使用：

.. code-block:: c

  void nsh_output(FAR struct nsh_vtbl_s *vtbl, const char *fmt, ...);

因此，如果您只想在控制台上输出"Hello, World!"，那么您的整个命令实现可能是：

.. code-block:: c

  int cmd_mycmd(FAR struct nsh_vtbl_s *vtbl, int argc, char **argv)
  {
    nsh_output(vtbl, "Hello, World!");
    return 0;
  }

新命令的原型应放在 ``apps/examples/nshlib/nsh.h`` 中。

**将您的命令添加到 NSH 命令表**。NSH 支持的所有命令都出现在一个名为的单一表中：

.. code-block:: c

  const struct cmdmap_s g_cmdmap[]

该表可以在文件 ``apps/examples/nshlib/nsh_parse.c`` 中找到。结构 ``cmdmap_s``
也在 ``apps/nshlib/nsh_parse.c`` 中定义：

.. code-block:: c

  struct cmdmap_s
  {
    const char *cmd;        /* 命令名称 */
    cmd_t       handler;    /* 处理命令的函数 */
    uint8_t     minargs;    /* 最小参数数量（包括命令） */
    uint8_t     maxargs;    /* 最大参数数量（包括命令） */
    const char *usage;      /* 'help' 命令的用法说明 */
  };

此结构提供了描述命令所需的一切：其名称（``cmd``）、处理命令的函数
（``cmd_mycmd()``）、命令所需的最小和最大参数数量，以及描述命令行参数的字符串。
最后那个字符串是在输入"``nsh> help``"时打印的内容。

因此，对于您的示例命令，您将向 ``g_cmdmap[]`` 表添加以下内容：

.. code-block:: c

  { "mycmd", cmd_mycmd, 1, 1, NULL },

此条目特别简单，因为 ``mycmd`` 非常简单。请查看 ``g_cmdmap[]`` 中的其他命令
以获取更复杂的示例。
