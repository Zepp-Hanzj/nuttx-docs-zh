======================================================================================
``configure.sh``, ``configure.bat``, ``configure.c``, ``cfgparser.c``, ``cfgparser.h``
======================================================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``configure.sh`` 是一个 bash 脚本，用于在支持 POSIX 路径的环境（Linux、Cygwin、macOS
或类似环境）中为给定目标板配置 NuttX。有关如何使用此脚本配置 NuttX 的说明，
请参阅 :doc:`/components/boards` 或 Documentation/NuttXPortingGuide.html。

configure.c、cfgparser.c 和 cfgparser.h 可用于构建一个功能相同的程序
作为 configure.sh 的替代品。此替代程序可用于
不支持 Bash 脚本的环境（如 Windows 原生环境）。

configure.bat 是一个小型 Windows 批处理文件，可在 Windows 原生环境中
用作 configure.sh 的替代品。configure.bat 实际上
只是一个薄层，如果 configure.exe 可用则执行它。如果
configure.exe 不可用，configure.bat 将尝试先构建它。

为了在 Windows 原生环境中从 configure.c 构建 configure.exe，
需要满足两个假设：

1) 你已安装 MinGW GCC 工具链。该工具链可从
   http://www.mingw.org/ 下载。建议不要安装可选的 MSYS 组件，
   因为可能会有冲突。
2) 包含 mingw-gcc.exe 的 bin/ 目录路径必须
   包含在 PATH 变量中。
