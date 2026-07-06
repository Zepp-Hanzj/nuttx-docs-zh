================
``testbuild.sh``
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此脚本自动构建一组配置。目的只是确保
这组配置能正确构建。-h 选项显示用法：

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

此脚本需要两条信息：

1. 你正在测试的平台的描述。此描述由可选的 -l、-m、-c、-g 和 -n 选项提供。

2. 要构建的配置列表。该列表由测试列表文件提供。最后的非可选参数
   <testlist-file> 提供了该文件的路径。

测试列表文件是一个构建描述序列，每行一个。一个构建描述
由两个逗号分隔的值组成。例如::

    stm32f429i-disco:nsh
    arduino-due:nsh
    /arm
    /risc-v

第一个值是通常的 ``<board-name>:<configuration-name>`` 或 ``/<folder-name>`` 格式的
配置描述，必须对应 nuttx/boards 目录中的一个配置或文件夹。

第二个值是构建配置时使用的有效工具链配置名称。
有效工具链配置名称的集合取决于
所配置板的底层架构。

前缀 ``-`` 可用于跳过某个配置::

  -stm32f429i-disco/nsh

或在特定主机上（如 Darwin）跳过某个配置::

  -Darwin,sim:rpserver

此脚本将在失败时重新构建每个配置，最多 3 次。每次重新构建
将在随机的指数退避延迟后尝试，初始设置为 60 秒。重新构建将
缓解 GitHub Actions 中发生的间歇性下载失败的影响。

如果 3 次重试后构建仍然失败，后续配置将不被允许
在失败时重新构建。这是为了防止级联构建失败
导致 GitHub Actions 过载。
