====================
使用 CMake 编译
====================

使用 CMake 初始化配置
===================================

第一步是为给定的开发板初始化 NuttX 配置，基于
一个预先存在的配置。要列出所有支持的配置，可以执行：

    .. code-block:: console

       $ cd nuttx
       $ ./tools/configure.sh -L | less

输出格式为 ``<board name>:<board configuration>``。您会发现
通常所有开发板都支持 ``nsh`` 配置，这是一个很好的起点，
因为它可以启动进入交互式命令行
:doc:`/applications/nsh/index`。

要选择一个配置，传递 ``<board name>:<board configuration>``，例如：

    .. code-block:: console

       $ cd nuttx
       $ cmake -B build -DBOARD_CONFIG=stm32f4discovery:nsh -GNinja

``-B build`` 指定了构建目录。

然后您可以使用基于菜单的配置系统自定义此配置：

.. code-block:: console

   $ cd nuttx
   $ cmake --build build -t menuconfig 

修改配置在 :doc:`configuring` 中介绍。

使用 CMake 构建 NuttX
======================

现在我们可以构建 NuttX。为此，您只需运行：

  .. code-block:: console

     $ cd nuttx
     $ cmake --build build 

构建完成后将在 ``build/`` 目录中生成二进制输出文件。
通常包括 ``nuttx`` ELF 文件（适合使用 ``gdb`` 调试）和
``nuttx.bin`` 文件（可烧录到开发板上）。

要清理构建，可以执行：

  .. code-block:: console

     $ cmake --build build -t clean

源码外构建
====================

CMake 的一个关键优势是源码外构建，允许为不同的配置使用不同的构建文件夹，
非常适合需要对同一代码库检查多个配置的场景。源码外意味着上述 ``build`` 文件夹
可以在 NuttX 源码树之外。

假设 ``$NUTTX_DIR`` 是 NuttX 源码树，我们可以使用临时文件夹
作为特定目标配置的构建目录，如下所示。

  .. code-block:: console

    $ echo $NUTTX_DIR
    /home/user/Projects/Nuttx/nuttx
    $ mkdir -p ~/tmp/rv32/nsh
    $ cd ~/tmp/rv32/nsh
    # 确保适当的工具链在您的 $PATH 中
    $ riscv64-unknown-elf-gcc -v
    $ cmake $NUTTX_DIR -DBOARD_CONFIG=rv-virt:nsh -GNinja
    -- Initializing NuttX
    --   Board:  rv-virt
    --   Config: nsh
    --   Appdir: /home/yf/Projects/Nuttx/apps
    -- The C compiler identification is GNU 10.2.0
    -- The CXX compiler identification is GNU 10.2.0
    -- The ASM compiler identification is GNU
    -- Found assembler: /usr/bin/riscv64-unknown-elf-gcc
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /home/yf/tmp/rv32/nsh
    $ ninja
    $ size nuttx
       text    data      bss      dec      hex  filename
     167411      365    11568   179344    2bc90  nuttx

此方法目前适用于 FLAT 配置，如果需要的 CMake 脚本已经就绪，
很快也将支持 PROTECTED 配置。

构建 KERNEL 配置
=======================

我们现在可以使用 CMake 来为 KERNEL 配置构建内核镜像，
前提是 apps ROMFS 已通过 Makefile 系统准备好。如果开发重点在内核侧
且 apps 不经常更改，那么 CMake 可以帮助我们实现源码外构建
——前提是你设备的 CMake 脚本已准备就绪。让我们以 ``canm230`` 设备为例：

  .. code-block:: console

    $ echo $NUTTX_DIR
    /home/user/Projects/Nuttx/nuttx
    $ mkdir -p ~/tmp/k230/nsbi
    # 将 romfs_boot.c 复制到构建文件夹
    $ cp romfs_boot.c ~/tmp/k230/nsbi
    $ cd ~/tmp/k230/nsbi
    $ ls -l
    total 976
    -rw-rw-r-- 1 yf yf 997843 Jul 15 06:23 romfs_boot.c
    $ cmake $NUTTX_DIR -DBOARD_CONFIG=canmv230:nsbi -GNinja
    -- Initializing NuttX
    --   Board:  canmv230
    --   Config: nsbi
    --   Appdir: /home/yf/Projects/Nuttx/apps
    -- The C compiler identification is GNU 10.2.0
    -- The CXX compiler identification is GNU 10.2.0
    -- The ASM compiler identification is GNU
    -- Found assembler: /usr/bin/riscv64-unknown-elf-gcc
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /home/yf/tmp/k230/nsbi
    $ ninja
    $ size nuttx
      text     data      bss      dec      hex  filename
    281671      609    37496   319776    4e120  nuttx

请注意，对于 QEMU 目标，我们可以通过 QEMU 中的 ``hostfs``
直接使用主机文件夹上的 apps 二进制文件。

因此，即使 apps 侧的 CMake 支持尚未就绪，我们仍然可以
在 KERNEL 配置中使用 CMake 进行内核构建。
