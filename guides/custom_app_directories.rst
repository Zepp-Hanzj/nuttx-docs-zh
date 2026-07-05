===========================================
自定义应用程序目录
===========================================

.. warning:: 
    迁移自: 
    https://cwiki.apache.org/confluence/display/NUTTX/Custom+Application+Directories

大多数人使用 NuttX 的通用 ``apps/`` 目录。这很方便且文档齐全。然而，应始终记住 NuttX 是一个独立的通用操作系统，对该"罐装"应用程序目录 **没有依赖**。

本页面展示如何从头创建自己的自定义应用程序目录。

创建自定义应用程序目录
=========================================

下面是一个 **最小** 自定义应用程序目录的简单示例。它只包含三个文件：``Makefile``、``Kconfig`` 和 ``hello.c``。

Makefile
--------

自定义应用程序目录必须包含一个 ``Makefile``，支持 NuttX 构建系统期望的所有 make 目标，**并且** 必须在自定义目录结构的顶层生成名为 ``libapps.a`` 的归档。``Makefile`` 的最低要求目标如下：

.. code-block:: shell

    APPDIR = ${shell pwd}
    
    -include $(TOPDIR)/Make.defs
    
    # files
    
    CSRCS = hello.c
    COBJS = hello.o
    
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
    $(Q) $(MKDEP) $(ROOTDEPPATH) "$(CC)" -- $(CFLAGS) -- $(SRCS) >Make.dep
    
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
    

Kconfig
-------

必须包含 ``Kconfig`` 文件，但不需要包含任何有意义的配置选项。此文件可用于添加应用程序特定的配置设置。最小 ``Kconfig`` 可能如下所示：

.. code-block:: shell

   # For a description of the syntax of this configuration file,
   # see the file kconfig-language.txt in the NuttX tools repository.
   #

hello.c
-------

您的自定义应用程序必须编译至少一个源文件以生成所需的 ``libapps.a`` 归档。其中一个源文件必须包含应用程序的 ``main()`` 入口点。该主函数（或类似命名的入口点）在 OS 初始化完成后被调用。

此应用程序初始化入口点做什么、如何与应用程序的其余部分交互、以及应用程序代码的其余部分位于何处，都与 OS 无关。只需要这一个入口点。

下面是一个小的 "Hello, World!" 示例，其中 ``custom_main()`` 是应用程序入口点：

.. code-block:: c

    #include <stdio.h>
    
    int custom_main(int argc, char *argv[])
    {
    printf("Hello, World!!\n");
    return 0;
    }

使用自定义应用程序目录构建
==============================================

要使用新的自定义应用程序目录进行构建，需要在 NuttX 配置中包含以下内容：

.. code-block:: shell

   CONFIG_APPS_DIR="../custom-apps"
   CONFIG_USER_ENTRYPOINT="custom_main"

.. note::

   只有在运行 ``make menuconfig`` **之前** 将 ``CONFIG_APPS_DIR`` 设置为 ``../custom-apps``，才能访问 ``../custom-apps/Kconfig`` 文件。如果您从现有配置开始，可能会面临"先有鸡还是先有蛋"的情况。一种变通方法是在运行 ``make menuconfig`` 之前手动编辑 ``.config`` 文件。

或者，如果您使用 ``tools/configure.sh`` 脚本，可以从命令行指定 custom-apps 目录：

.. code-block:: shell

   tools/configure.sh -a ../custom_apps <board>:<config>

之后，只需像平常一样构建 NuttX。当您运行使用自定义应用程序目录构建的程序时，您应该看到：

.. code-block:: shell

   Hello, World!!
