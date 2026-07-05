======================================================================================
``configure.sh``, ``configure.bat``, ``configure.c``, ``cfgparser.c``, ``cfgparser.h``
======================================================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``configure.sh`` is a bash script that 用于 to configure NuttX for a given
tar获取 board in a environment that 支持s POSIX 路径s (Linux, Cygwin, macOS,
or similar).  See :doc:`/components/boards` or
Documentation/NuttXPortingGuide.html for a description of how to configure NuttX
with this script.

configure.c, cfgparser.c, and cfgparser.h 可用于 to 构建 a work-alike
program as a replacement for configure.sh.  This work-alike program would be
used in environments that do not 支持 Bash scripting (such as the 窗口s
native environment).

configure.bat is a small 窗口s batch 文件 that 可用于 as a replacement
for configure.sh in a 窗口s native environment.  configure.bat is actually
just a thin layer that 执行s configure.exe if it 可用. If
configure.exe is not available, then configure.bat will attempt to 构建 it
first.

In order to 构建 configure.exe from configure.c in the 窗口s native
environment, two assumptions are made:

1) You have installed the MinGW GCC toolchain.  This toolchain can be
   downloaded from http://www.mingw.org/.  It is recommended that you not
   install the 选项al MSYS components as there may be conflicts.
2) That 路径 to the bin/ 目录 containing mingw-gcc.exe must be
   included in the PATH 变量.
