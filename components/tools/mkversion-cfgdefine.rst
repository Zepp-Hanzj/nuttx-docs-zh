=================================================
``mkversion.c``, ``cfgdefine.c``, ``cfgdefine.h``
=================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是一个 C 文件，用于构建 mkversion 程序。mkversion
程序在 NuttX 初始构建期间使用。

当你构建 NuttX 时，NuttX 顶层目录中应该有一个名为 .version 的版本文件
（参见 Documentation/NuttXPortingGuide.html）。第一次构建 NuttX 时，
顶层 Makefile 将从 mkversion.c（使用 Makefile.host）构建 mkversion
可执行文件。然后顶层 Makefile 将执行 mkversion 程序，将
顶层目录中的 .version 文件转换为 include/nuttx/version.h。
version.h 提供了可被 C 文件包含的版本信息。
