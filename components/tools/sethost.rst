==============
``sethost.sh``
==============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

保存的配置可以在 Linux、Cygwin（32 位或 64 位）或其他平台上运行。
平台特性可以通过 'make menuconfig' 进行更改。
由于平台之间的差异，有时可能会令人困惑。
sethost.sh 应运而生。

sethost.sh 是一个简单的脚本，用于将配置更改为你的主机平台。
如果你使用许多不同的配置，这可以大大简化工作。
例如，如果你在 Linux 上运行并像这样配置：

.. code:: console

   $ tools/configure.sh board:configuration

那么你可以使用以下命令同时完成以下两项操作：(1) 确保配置是最新的，
(2) 正确配置为 Linux：

.. code:: console

   $ tools/sethost.sh -l

或者，如果你在 Windows/Cygwin 64 位平台上：

.. code:: console

   $ tools/sethost.sh -c

其他可用选项：

.. code:: console

   $ ./sethost.sh -h

   USAGE: ./sethost.sh [-l|m|c|g|n] [make-opts]
          ./sethost.sh -h

   Where:
     -l|m|c|g|n selects Linux (l), macOS (m), Cygwin (c),
        MSYS/MSYS2 (g) or Windows native (n). Default Linux
     make-opts directly pass to make
     -h will show this help test and terminate
