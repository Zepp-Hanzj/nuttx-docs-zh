=============================
从 NSH 运行应用程序
=============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本页描述了 NuttX NuttShell (NSH) 的当前和计划功能。
请将此页视为路线图。大多数功能已经实现并整合到 NSH 中；
其他功能只是正在讨论的想法（标注为未实现）。随着新功能的加入，NSH 文档将被更新。

目前有三种方式可以从 NSH 执行应用程序：

#. 执行内置应用程序

   **内置应用程序**
   NSH 的当前实现允许执行"命名的"或"内置"应用程序。这些应用程序只是共同 FLASH 映像中
   分配了名称的任务入口点。只需从 NSH 命令行输入该名称，就会导致相关应用程序运行。

   有关更多详细信息，请参阅 NSH 文档。

   **示例**

   例如：

     .. code-block:: bash

        NuttShell (NSH) NuttX-6.24
        nsh> hello
        Hello, World!!
        nsh>

   **配置设置**

   此功能依赖于以下配置设置：

     * ``CONFIG_BUILTIN=y`` 启用 NuttX 对内置应用程序的支持，以及
     * ``CONFIG_NSH_BUILTIN_APPS=y`` 启用 NSH 对内置应用程序的支持，以及
     * ``CONFIG_NSH_BUILTIN_AS_COMMAND``：启用 NSH 直接运行内置应用程序而不创建
       单独的线程（可选）。

   除了 NSH 所需的其他配置之外。

#. 从文件系统执行应用程序

   **操作系统接口**

   NuttX 也支持运行驻留在文件系统上的应用程序。用于此目的的标准接口包括：

     * ``execv()``
     * ``execl()``
     * ``posix_spawn()``


   **配置设置**

   文件系统上的应用程序执行目前由 NuttX 支持。此功能通过以下方式启用：

     * ``CONFIG_LIBC_EXECFUNCS=y`` 启用对 ``execv()``、``execl()`` 和 ``posix_spawn()`` 的支持，以及
     * ``CONFIG_NSH_FILE_APPS=y`` 启用 NSH 在文件系统中执行程序。

   **示例**

   启用此功能后，您将能够执行以下操作：

   .. code-block:: bash

      NuttShell (NSH) NuttX-6.24
      nsh> mount -t vfat /dev/mmcsd0 /mnt/sdcard
      nsh> ls -l /mnt/sdcard
      /mnt/sdcard:
      -rw-r--r--  198 hello
      nsh> /mnt/sdcard/hello
      Hello, World!!
      nsh>

   **PATH 变量**

   请注意使用了 hello 程序的绝对路径。这可以通过在配置中设置以下内容来简化：

     * ``CONFIG_BINFMT_EXEPATH=y`` 启用使用路径变量查找可执行程序。

   **示例**

   然后，示例变为：

   .. code-block:: bash

      NuttShell (NSH) NuttX-6.24
      nsh> mount -t vfat /dev/mmcsd0 /mnt/sdcard
      nsh> ls -l /mnt/sdcard
      /mnt/sdcard:
        -rw-r--r--  198 hello
      nsh> set PATH /mnt/sdcard
      nsh> hello
      Hello, World!!
      nsh>

   **预初始化 PATH 变量**

   最后一个简化：可以配置初始 PATH 变量，以便在 NSH 启动时已定义可执行程序的 PATH。
   这通过以下方式完成：

     * ``CONFIG_PATH_INITIAL="/mnt/sdcard"``

   此功能已经就位。

#. 从文件系统执行内置应用程序

   **命名空间管理**

   NuttX 支持可用于管理命名空间的虚拟文件系统 (VFS)。Linux 使用其 VFS 管理几乎所有
   命名对象（管道、锁、消息队列等）。NuttX 这样做也是一个好策略。NuttX 已经对驱动程序
   和挂载点等这样做了。为什么不将此机制扩展到处理命名的内置应用程序呢？

   **建议的配置选项**

   计划以下配置选项：

     * ``CONFIG_BUILTIN=y`` 仍将需要以启用 NuttX 对内置应用程序的支持，以及
     * ``CONFIG_NSH_BUILTIN_APPS=y`` 仍将需要以激励程序将自己注册为内置应用程序。

   此外：

     * ``CONFIG_FS_BINFS=y`` 启用用于将内置应用程序作为文件访问的 BINFS 文件系统，
     * ``CONFIG_LIBC_EXECFUNCS=y`` 启用对 ``execv()``、``execl()`` 和 ``posix_spawn()`` 的支持，
     * ``CONFIG_NSH_FILE_APPS=y`` 启用 NSH 在文件系统中执行程序，
     * ``CONFIG_BINFMT_EXEPATH=y`` 启用（可选）使用路径变量查找可执行程序，以及
     * ``CONFIG_PATH_INITIAL="/mnt/sdcard:/bin"`` PATH 变量的可选初始值。

   **示例**

   启用此功能后，您将能够执行此操作（其中 myapplication 是某个任意"内置"应用程序的名称）：

   .. code-block:: bash

      NuttShell (NSH) NuttX-6.24
      nsh> mount -t binfs /bin
      nsh> ls -l /bin
      /bin:
        -rw-r--r--  0 myapplication
      nsh> echo $PATH
      /mnt/sdcard:/bin
      nsh> myapplication
      ... 您基于 FLASH 的应用程序运行 ...
      nsh>

   **自动挂载 BINFS**

   BINFS 与任何文件系统一样，可以由 ``/etc/init.d/rcS`` 的启动脚本挂载。

   但由于 BINFS 可能在许多不需要启动脚本的配置中使用，也许一些配置会有所帮助：

     * ``CONFIG_NSH_AUTOMOUNT_BINFS=y`` 启动时自动挂载 BINFS 文件系统（**未实现**）
     * ``CONFIG_NSH_BINFS_MOUNTPOINT="/bin"`` BINFS 挂载点（未实现）。

   或者更好的做法是使添加启动脚本更容易？

   **后续步骤**

   从长远来看，最好可以选择性地将大多数较大的 NSH 命令移出 RAM，并将它们构建为
   可以驻留在 SD 卡上的独立程序（**未实现**）。
