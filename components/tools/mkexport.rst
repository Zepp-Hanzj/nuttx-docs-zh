==============================
``mkexport.sh``, ``Export.mk``
==============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这些实现了顶层 Makefile 的 'export' 目标的一部分。该目标将把所有的 NuttX
库、头文件和启动对象打包成一个可导出的二进制 NuttX 发行包。
Export.mk 仅由 mkexport.sh 脚本使用，用于从顶层 Make.defs 文件中解析选项。

USAGE: tools/mkexport.sh [-d] [-z] [-u] -t <top-dir> [-x <lib-ext>] -l "lib1 [lib2 [lib3 ...]]"

此脚本还依赖于环境变量 MAKE，该变量在启动 mkexport.sh 之前在顶层
Makefile 中设置。如果未定义 MAKE，脚本将将其设置为 `which make`。
