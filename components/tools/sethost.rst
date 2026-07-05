==============
``sethost.sh``
==============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Saved 配置s may 运行 on Linux, Cygwin (32- or 64-位), or other
platforms.  The platform characteristics can be changed use 'make menuconfig'.
Sometimes this can be confusing due to the differences between the platforms.
Enter 设置host.sh

设置host.sh is a simple script that changes a 配置 to your host
platform. This can greatly simplify life if you use many different
配置s. 例如, if you are 运行ning on Linux and you configure like
this:

.. code:: console

   $ tools/configure.sh board:configuration

The you can use 以下 command to both (1) make sure that the
配置 is up to date, AND (2) the 配置 is 设置 up
correctly for Linux:

.. code:: console

   $ tools/sethost.sh -l

Or, if you are on a 窗口s/Cygwin 64-位 platform:

.. code:: console

   $ tools/sethost.sh -c

Other 选项s 可用:

.. code:: console

   $ ./sethost.sh -h

   USAGE: ./sethost.sh [-l|m|c|g|n] [make-opts]
          ./sethost.sh -h

   Where:
     -l|m|c|g|n selects Linux (l), macOS (m), Cygwin (c),
        MSYS/MSYS2 (g) or Windows native (n). Default Linux
     make-opts directly pass to make
     -h will show this help test and terminate
