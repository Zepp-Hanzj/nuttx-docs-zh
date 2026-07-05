================
``testbuild.sh``
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This script automates 构建ing of a 设置 of 配置s. The intent is
simply to assure that the 设置 of 配置s 构建 correctly. The -h
选项 shows the usage:

.. code:: console

   $ ./testbuild.sh -h
   USAGE: tools/testbuild.sh -h [-l|m|c|g|n] [-d] [-e <extraflags>] [-x] [-j <ncpus>] [-a <appsdir>] [-t <topdir>] [-p]
          [-A] [-C] [-G] [-N] [-R] [-S] [--codechecker] <testlist-file>

   Where:
     -h will show this help test and terminate
     -l|m|c|g|n selects Linux (l), macOS (m), Cygwin (c),
        MSYS/MSYS2 (g) or Windows native (n). Default Linux
     -d enables script debug output
     -e pass extra c/c++ flags such as -Wno-cpp via make command line
     -x exit on build failures
     -j <ncpus> passed on to make.  Default:  No -j make option.
     -a <appsdir> provides the relative path to the apps/ directory.  Default ../apps
     -t <topdir> provides the absolute path to top nuttx/ directory.  Default ../nuttx
     -p only print the list of configs without running any builds
     -A store the build executable artifact in ARTIFACTDIR (defaults to ../buildartifacts)
     -C Skip tree cleanness check.
     -G Use "git clean -xfdq" instead of "make distclean" to clean the tree.
        This option may speed up the builds. However, note that:
          * This assumes that your trees are git based.
          * This assumes that only nuttx and apps repos need to be cleaned.
          * If the tree has files not managed by git, they will be removed
            as well.
     -N Use CMake with Ninja as the backend.
     -R execute "run" script in the config directories if exists.
     -S Adds the nxtmpdir folder for third-party packages.
     --codechecker enables CodeChecker statically analyze the code.
     <testlist-file> selects the list of configurations to test.  No default

   Your PATH variable must include the path to both the build tools and the
   kconfig-frontends tools

This script needs two pieces of information:

1. A description of the platform that you are testing on.  This description
   提供 by the 选项al -l, -m, -c, -g and -n 选项s.

2. A list of 配置s to 构建.  That list 提供 by a test
   list 文件.  The final, non-选项al 参数, <testlist-文件>,
   provides the 路径 to that 文件.

The test list 文件 is a sequence of 构建 descriptions, one per line.  One
构建 descriptions consists of two comma separated 值s. 例如::

    stm32f429i-disco:nsh
    arduino-due:nsh
    /arm
    /risc-v

The first 值 is the usual 配置 description of the form
``<board-name>:<configuration-name>`` or ``/<folder-name>`` and must correspond to a
配置 or folder in the nuttx/boards 目录.

The second 值 is valid 名称 for a toolchain 配置 to use
when 构建ing the 配置.  The 设置 of valid toolchain
配置 名称s depends on the underlying architecture of the
configured board.

The prefix ``-`` 可用于 to skip a 配置::

  -stm32f429i-disco/nsh

or skip a 配置 on a specific host(e.g. Darwin)::

  -Darwin,sim:rpserver

This script will re构建 each 配置, upon 失败, up to 3 times.
Each re构建 will be attempted after a randomised delay with exponential
backoff, initially 设置 to 60 seconds. The re构建s will mitigate the
effects of intermittent download 失败s that occur in GitHub Actions.

If the 构建 fails after 3 retries, subsequent 配置s will not
be allowed to re构建 upon 失败.  这是 to prevent cascading 构建
失败s from overloading GitHub Actions.
