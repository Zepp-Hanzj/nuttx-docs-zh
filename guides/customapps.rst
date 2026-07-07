======================
自定义应用程序操作指南
======================

NuttX 自带大量应用程序，但您很可能想要添加自己的应用程序。

根据您的需求，有多种不同的选择。

  #. 完全替换 apps/ 目录
  #. 扩展 apps/ 目录以包含新的自定义目录
  #. 在主源码树外包含额外的自定义目录

以下各节使用 ``CustomHello.c`` 应用程序和 ``CustomApps`` 目录作为示例来解释这 3 种方法。

.. Tip::
  如果您在设置过程中出现错误且构建失败，您很可能需要在重新构建之前运行 ``make clean``，甚至可能需要运行 ``make distclean``，以确保正确运行。

1. 完全替换 Apps/ 目录
=========================================

CustomApps 目录只需包含最少的三个文件：

  * ``Makefile``
  * ``Kconfig``
  * ``CustomHello.c``


1.1 Makefile
------------

自定义应用程序目录必须包含一个 Makefile 来构建 NuttX 期望的所有目标，并且必须在自定义目录结构的顶层生成名为 libapps.a 的归档。

Makefile 只有那些最低要求的目标：

    .. code-block:: console

      APPDIR = ${shell pwd}

      -include $(TOPDIR)/Make.defs

      # files

      CSRCS = CustomHello.c
      COBJS = CustomHello.o

      ROOTDEPPATH = --dep-path .

      # Build targets

      all: libapps.a
      .PHONY: dirlinks context preconfig depend clean clean_context distclean
      .PRECIOUS: libapps$(LIBEXT)

      # Compile C Files

      $(COBJS): %$(OBJEXT): %.c
      $(call COMPILE, $<, $@)

      # Add object files to the apps archive

      libapps.a: $(COBJS)
        $(call ARCHIVE, libapps.a, $(COBJS))

      # Create directory links

      dirlinks:

      # Setup any special pre-build context

      context:

      # Setup any special pre-configuration context

      preconfig:

      # Make the dependency file, Make.deps

      depend: Makefile $(CSRCS)
        $(Q) $(MKDEP) $(ROOTDEPPATH) "$(CC)" -- $(CFLAGS) -- $(SRCS) > Make.dep

      # Clean the results of the last build

      clean:
        $(call CLEAN)

      # Remove the build context and directory links

      clean_context:

      # Restore the directory to its original state

      distclean: clean clean_context
        $(call DELFILE, Make.dep)

      # Include dependencies

      -include Make.dep

1.2 Kconfig
-----------

必须包含 Kconfig 文件，但不需要填充任何有意义的选项。这是一个可以添加设置以生成自定义应用程序的自定义构建和/或选择要包含哪些应用程序的地方。

在最小情况下，Kconfig 只是：

    .. code-block:: console

      # For a description of the syntax of this configuration file,
      # see the file kconfig-language.txt in the NuttX tools repository.
      #

但通常会包含任何 NuttX 应用程序所需的基本信息，以及您的应用程序可能需要的任何其他内容：

    .. code-block:: console

      # For a description of the syntax of this configuration file,
      # see the file kconfig-language.txt in the NuttX tools repository.
      #

      config CUSTOM_APPS_MY_APP
	        tristate "My App"
	        default n
	        ---help---
		      Enable My App
		
      if CUSTOM_APPS_MY_APP

      config CUSTOM_APPS_MY_APP_PROGNAME
    	  string "Program name"
    	  default "myapp"
    	  ---help--- This is the name of the program that will be used when the NSH ELF
    	    program is installed.
    	
      config CUSTOM_APPS_MY_APP_PRIORITY
    	  int "My App task priority"
    	  default 100

      config CUSTOM_APPS_MY_APP_STACKSIZE
    	  int "My App stack size"
    	  default DEFAULT_TASK_STACKSIZE

      endif

1.3 CustomHello.c
-----------------

自定义应用程序必须实际编译一些源文件以生成所需的 libapps.a 归档。其中一个源文件必须包含应用程序的 ``main()`` 入口点。

此 main() 入口点的功能只是启动完整的应用程序。它在 OS 初始化完成时被调用。

此应用程序初始化入口点做什么、如何与应用程序的其余部分交互、以及应用程序代码的其余部分位于何处，都与 OS 无关。只需要这一个入口点。

对于此 "Hello, Custom World!" 应用程序，``custom_hello()`` 是应用程序入口点：

    .. code-block:: console

      #include <stdio.h>

      int main(int argc, char *argv[])
      {
        printf("Hello, Custom World!!\n");
        return 0;
      }

1.4 使用 CustomApps 目录构建
------------------------------------------

要使用新的自定义配置进行构建，您需要在配置中包含以下内容：

:menuselection:`CONFIG_APPS_DIR="../CustomApps"`

:menuselection:`CONFIG_INIT_ENTRYPOINT="custom_hello_main"`

请注意，只有在执行 ``make menuconfig`` 之前将 ``CONFIG_APPS_DIR`` 设置为 ``../CustomApps``，才能访问 ``../CustomApps/Kconfig`` 配置文件。

可以通过以下方式完成

* 在运行 make menuconfig 之前手动编辑 .config 文件，这很少是个好主意
* 使用 ``kconfig-tweak --set-str CONFIG_APPS_DIR ../CustomApps``
* 在配置板时将 CustomApps 目录选为命令行选项：

      .. code-block:: console

        ./tools/configure.sh -a ../CustomApps <board>:<config>

  或

      .. code-block:: console

        .tools/configure.sh -l ../CustomBoards/MyCustomBoardName/MyCustomConfig

然后像平常一样构建。当您执行 custom_hello 应用程序时，您应该看到：

  .. code-block:: console

    Hello, Custom World!!

2. 扩展 apps/ 目录以包含新的自定义目录
===============================================================

nuttx-apps 中提供的应用程序集合可能很有用，此方法只是扩展目录结构以包含您自己的目录结构。

现有的 /apps makefile 自动检查包含 ``Makefile`` 和 ``Make.defs`` 文件的子目录是否存在。此示例假设可能有多个自定义应用程序，并包含应用程序本身的 ``Kconfig``。包含 ``Kconfig`` 允许将自定义应用程序选项包含在 NuttX 配置系统中，但这是可选的。

2.1 自定义应用程序目录
-------------------------

只需在现有 apps 目录下创建一个名称自选的新目录。此示例使用目录名 ``CustomApps``。

2.2 Make.defs
-------------

在 ``CustomApps`` 目录中创建此文件，添加以下行：

  .. code-block:: console

    include $(wildcard $(APPDIR)/CustomApps/*/Make.defs)

2.3 Makefile
------------

在 ``CustomApps`` 目录中创建一个 Makefile，添加以下行：

  .. code-block:: console

    MENUDESC = "Custom Apps"

    include $(APPDIR)/Directory.mk

2.4 CustomHello 应用程序
--------------------

在 ``CustomApps`` 目录下创建一个名为 ``CustomHello`` 的子目录。

应在此处创建与上述相同的 ``CustomHello.c`` 文件。

2.5 CustomHello Make.defs
-------------------------

在 ``CustomApps/CustomHello`` 目录中创建一个 Make.defs，包含以下行：

  .. code-block:: console

    ifneq ($(CONFIG_CUSTOM_APPS_CUSTOM_HELLO),)
    CONFIGURED_APPS += $(APPDIR)/CustomApps/CustomHello
    endif


2.6 CustomHello Makefile
------------------------

在 ``CustomApps/CustomHello`` 目录中创建一个 Makefile，包含以下行：

  .. code-block:: console

    include $(APPDIR)/Make.defs

    # Custom Hello built-in application info

    PROGNAME = $(CONFIG_CUSTOM_APPS_CUSTOM_HELLO_PROGNAME)
    PRIORITY = $(CONFIG_CUSTOM_APPS_CUSTOM_HELLO_PRIORITY)
    STACKSIZE = $(CONFIG_CUSTOM_APPS_CUSTOM_HELLO_STACKSIZE)
    MODULE = $(CONFIG_CUSTOM_APPS_CUSTOM_HELLO)

    # Custom Hello

    MAINSRC = CustomHello.c

    include $(APPDIR)/Application.mk


2.7 CustomHello Kconfig
-----------------------

在 ``CustomApps/CustomHello`` 目录中创建一个 Kconfig 文件，包含以下行。对于本示例，Kconfig 仅涵盖我们的单个应用程序）：

  .. code-block:: console

    #
    # For a description of the syntax of this configuration file,
    # see the file kconfig-language.txt in the NuttX tools repository.
    #

    config CUSTOM_APPS_CUSTOM_HELLO
	    tristate "Custom Hello App"
	    default n
	    ---help---
		    Enable the Custom Hello App

    if CUSTOM_APPS_CUSTOM_HELLO

    config CUSTOM_APPS_CUSTOM_HELLO_PROGNAME
	    string "Program name"
	    default "custom_hello"
	    ---help--- This is the name of the program that will be used when the NSH ELF
		    program is installed.

    config CUSTOM_APPS_CUSTOM_HELLO_PRIORITY
	    int "Custom Hello task priority"
	    default 100

    config CUSTOM_APPS_CUSTOM_HELLO_STACKSIZE
	    int "Custom Hello stack size"
	    default DEFAULT_TASK_STACKSIZE

    endif

2.8 构建和运行
-----------------

创建这些文件后，运行 ``make clean``（您可能需要运行 ``make distclean``），然后运行 ``make menuconfig``。如果成功，将出现新的 Kconfig 条目。

:menuselection:`Application Configuraration --> Custom Apps --> Custom Hello App`

选择 ``Custom Hello App`` 并运行常规构建过程。如果成功，您可以运行新包含的 ``custom_hello`` 应用程序。

3. 在主源码树外包含额外的自定义目录
==========================================================================

这与前面的方法类似，但将 ``CustomApps`` 目录放在默认树之外。

3.1 创建自定义应用程序目录和符号链接
----------------------------------------------------

在您选择的位置创建自定义应用程序目录。然后在主 nuttx/apps 目录中创建符号链接。

此示例假设已将其放在顶层 NuttX 文件夹下方，默认 ``apps`` 目录旁边，即 ``nuttx/CustomApps``

  .. code-block:: console

    $ pwd
    /home/nuttx
    $ ls -1
    apps
    CustomBoards
    nuttx
    $ mkdir CustomApps
    $ ls -1
    apps
    CustomApps
    CustomBoards
    nuttx
    $ cd apps
    $ ln -s ../CustomApps CustomApps

3.2 Make.defs 等
------------------

按照上面第 2.2 到 2.7 节中的所有步骤操作，创建完全相同的文件，但将其放在此处描述创建的新 ``CustomApps`` 目录位置。
