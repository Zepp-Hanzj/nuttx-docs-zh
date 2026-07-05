===========================================
``incdir.sh``, ``incdir.bat``, ``incdir.c``
===========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Different 编译rs have different conventions for specifying lists
of include 文件 路径s on the 编译r command line. This incdir.sh
bash script allows the 构建 system to 创建 include 文件 路径s without
concern for the particular 编译r in use.

The incdir.bat script is a counterpart for use in the native 窗口s
构建.  However, there is currently only one 编译r 支持ed in
that con文本:  MinGW-GCC.

incdir.c is a higher performance version of incdir.sh, converted to C.
