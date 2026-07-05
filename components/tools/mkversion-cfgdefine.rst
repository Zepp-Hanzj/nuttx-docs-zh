=================================================
``mkversion.c``, ``cfgdefine.c``, ``cfgdefine.h``
=================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 C 文件 that 用于 to 构建 mkversion program.  The mkversion
program 用于 during the initial NuttX 构建.

When you 构建 NuttX there should be a version 文件 called .version in
the top level NuttX 目录 (See Documentation/NuttXPortingGuide.html).
The first time you make NuttX, the top-level make文件 will 构建 the
mkversion executable from mkversion.c (using Make文件.host).  The top-level
Make文件 will then 执行 the mkversion program to convert the
.version 文件 in the top level 目录 into include/nuttx/version.h.
version.h provides version information that can be included by C 文件s.

