===========================
NSH 内置应用程序
===========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**概述。** 除了作为 NSH 一部分的这些命令之外，外部程序也可以作为 NSH 命令执行。
由于历史原因，这些外部程序被称为"内置"应用程序。这个术语有些令人困惑，因为上面
描述的实际 NSH 命令才是真正"内置"到 NSH 中的，而这些应用程序实际上是在 NuttX 外部的。

这些应用程序在某种意义上是"内置"到 NSH 中的，即只需在 NSH 提示符下输入应用程序
名称即可执行。内置应用程序支持通过以下配置选项启用：

  -  ``CONFIG_BUILTIN``：启用 NuttX 对内置应用程序的支持。
  -  ``CONFIG_NSH_BUILTIN_APPS``：启用 NSH 对内置应用程序的支持。
  -  ``CONFIG_NSH_BUILTIN_AS_COMMAND``：启用 NSH 直接运行内置应用程序而不创建
     单独的线程（可选）。

当这些配置选项被设置时，您还可以通过输入"nsh> help"来查看内置应用程序。
它们将出现在 NSH 命令列表的底部，在以下标题下::

  Builtin Apps:

请注意，除了内置应用程序的名称之外，不提供详细的帮助信息。

内置应用程序
=====================

**概述。** 支持 NSH 内置应用程序的底层逻辑被称为"内置应用程序"。
内置应用程序逻辑可以在 ``apps/builtin`` 中找到。该逻辑仅执行以下操作：

  #. 它支持注册机制，以便内置应用程序可以在构建时动态注册自己，以及

  #. 用于查找、列出和执行内置应用程序的实用函数。

**内置应用程序实用函数**。内置应用程序逻辑导出的实用函数原型在
``nuttx/include/nuttx/lib/builtin.h`` 和 ``apps/include/builtin.h`` 中。
这些实用函数包括：

  -  ``int builtin_isavail(FAR const char *appname);`` 检查在构建期间
     注册为 ``appname`` 的应用程序是否可用。

  -  ``const char *builtin_getname(int index);`` 返回由 ``index`` 指向的
     内置应用程序名称的指针。这是 NSH 用于在输入"``nsh> help``"时列出可用
     内置应用程序的实用函数。

  -  ``int exec_builtin(FAR const char *appname, FAR const char **argv);``
     执行在编译期间注册的内置应用程序。这是 NSH 用于执行内置应用程序的实用函数。

**自动生成的头文件**。应用程序入口点及其需求在 NuttX 首次构建时收集到两个文件中：

  #. ``apps/builtin/builtin_proto.h``：应用程序任务入口点的原型。

  #. ``apps/builtin/builtin_list.h``：应用程序特定信息和启动需求。

**内置应用程序的注册**。NuttX 构建在多个阶段进行，不同的构建目标被执行：
(1) *context* 阶段建立配置，(2) *depend* 阶段生成目标依赖关系，(3) *default*
（``all``）阶段执行正常的编译和链接操作。内置应用程序信息在 make *context*
构建阶段收集。

可以在 ``apps/examples/hello directory`` 中找到一个可以"内置"的示例应用程序。
让我们通过这个具体案例来说明创建内置应用程序以及它们如何注册以便从 NSH 使用的一般方式。

``apps/examples/hello``。apps/examples/hello 的主例程可以在
``apps/examples/hello/main.c`` 中找到。主例程是：

.. code-block:: c

  int hello_main(int argc, char *argv[])
  {
    printf("Hello, World!!\n");
    return 0;
  }

这是将在 NuttX 构建的 *context* 阶段注册的内置函数。该注册由
``apps/examples/hello/Makefile`` 中的逻辑执行。但构建系统通过相当曲折的
路径到达该逻辑：

  #. 顶层 context make 目标在 ``nuttx/Makefile`` 中。所有构建目标都依赖于
     *context* 构建目标。对于 ``apps/`` 目录，此构建目标将在 ``apps/Makefile``
     中执行 *context* 目标。

  #. ``apps/Makefile`` 将依次在所有已配置的子目录中执行 *context* 目标。
     在我们的案例中将包括 ``apps/examples`` 中的 ``Makefile``。

  #. 最后，``apps/examples/Makefile`` 将在所有已配置的 ``example`` 子目录中
     执行 *context* 目标，最终到达 ``apps/examples/Makefile``，下面将进行介绍。

**注意**：由于此 context 构建阶段只能执行一次，因此您之后进行的任何后续配置
更改都不会反映在构建序列中。这是一个常见的困惑点。在您实例化新配置之前，
您必须先摆脱旧配置。最彻底的方法是::

  make distclean

但这样您将不得不从头开始重新配置 NuttX。但如果您只想重建 ``apps/`` 子目录中
的配置，那么有一种工作量较小的方法。以下 NuttX make 命令将仅从 ``apps/``
目录中移除配置，并让您继续而无需重新配置所有内容::

  make apps_distclean

``apps/examples/hello/Makefile`` 中 ``context`` 目标的逻辑在 ``builtin`` 的
``builtin_proto.h`` 和 ``builtin_list.h`` 文件中注册 ``hello_main()`` 应用程序。
``apps/examples/hello/Makefile`` 中执行此操作的逻辑如下所示：

  #. 首先，``Makefile`` 包含 ``apps/Make.defs``::

      include $(APPDIR)/Make.defs

     这定义了一个名为 ``REGISTER`` 的宏，用于向 *builtin* 头文件添加数据::

        define REGISTER
            @echo "Register: $1"
            @echo "{ \"$1\", $2, $3, $4 }," >> "$(APPDIR)/builtin/builtin_list.h"
            @echo "EXTERN int $4(int argc, char *argv[]);" >> "$(APPDIR)/builtin/builtin_proto.h"
        endef

     当此宏运行时，您将在构建输出中看到"``Register: hello``"，这是注册成功的
     可靠标志。

  #. 然后 make 文件定义应用程序名称（``hello``）、任务优先级（默认）以及任务运行时
     将分配的栈大小（2K）::

      APPNAME         = hello
      PRIORITY        = SCHED_PRIORITY_DEFAULT
      STACKSIZE       = 2048

  #. 最后，``Makefile`` 调用 ``REGISTER`` 宏来添加 ``hello_main()`` 内置应用程序。
     然后，当系统构建完成后，``hello`` 命令就可以从 NSH 命令行执行。当 ``hello``
     命令被执行时，它将以默认优先级和 2K 的栈大小启动入口点为 ``hello_main()`` 的任务::

      context:
        $(call REGISTER,$(APPNAME),$(PRIORITY),$(STACKSIZE),$(APPNAME)_main)

**内置应用程序的其他用途。** 内置应用程序的主要目的是支持从 NSH 命令行执行
应用程序。然而，还应该提及内置应用程序的另一种用途。

  #. **binfs**。*binfs* 是一个位于 ``apps/builtin/binfs.c`` 的小型文件系统。
     这提供了一种查看已安装内置应用程序的替代方式。没有 *binfs* 时，您可以
     使用 NSH help 命令查看已安装的内置应用程序。*binfs* 将创建一个挂载在
     ``/bin`` 的小型伪文件系统。使用 *binfs*，您可以通过列出 ``/bin`` 目录的
     内容来查看可用的内置应用程序。这提供了一些表面上的 Unix 兼容性，但并不
     真正增加任何新功能。

同步内置应用程序
=================================

默认情况下，从 NSH 命令行启动的内置命令将与 NSH 异步运行。如果您想强制 NSH
执行命令后等待命令执行完成，可以通过在 NuttX 配置文件中添加以下内容来启用该功能::

  CONFIG_SCHED_WAITPID=y

此配置选项启用对标准 ``waitpid()`` RTOS 接口的支持。当该接口被启用时，NSH
将使用它来等待，休眠直到内置应用程序执行完成。

当然，即使定义了 ``CONFIG_SCHED_WAITPID=y``，仍然可以通过在 NSH 命令后添加
与号 (&) 来强制特定应用程序异步运行。
