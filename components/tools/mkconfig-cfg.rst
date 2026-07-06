================================================
``mkconfig.c``, ``cfgdefine.c``, ``cfgdefine.h``
================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这些是用于构建 mkconfig 程序的 C 文件。mkconfig
程序在 NuttX 初始构建期间使用。

当你配置 NuttX 时，你将在 NuttX 顶层目录中复制一个名为 .config 的
配置文件（参见 :doc:`/components/boards` 或
Documentation/NuttXPortingGuide.html）。第一次构建 NuttX 时，
顶层 Makefile 将从 mkconfig.c（使用 Makefile.host）构建 mkconfig
可执行文件。然后顶层 Makefile 将执行 mkconfig 程序，将
顶层目录中的 .config 文件转换为 include/nuttx/config.h。
config.h 是 NuttX 配置的另一个版本，可被 C 文件包含。
