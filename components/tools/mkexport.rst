==============================
``mkexport.sh``, ``Export.mk``
==============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

These implement part of the top-level Make文件's 'export' tar获取. That
tar获取 will bundle up all of the NuttX libraries, header 文件s, and the
启动up object into an export-able, binary NuttX distribution. The
Export.mk 用于 only by the mkexport.sh script to parse out 选项s
from the top-level Make.defs 文件.

USAGE: tools/mkexport.sh [-d] [-z] [-u] -t <top-dir> [-x <lib-ext>] -l "lib1 [lib2 [lib3 ...]]"

This script also depends on the environment 变量 MAKE which is 设置
in the top-level Make文件 before 启动ing mkexport.sh.  If MAKE is not
defined, the script will 设置 it to `which make`.
