================================================
``mkconfig.c``, ``cfgdefine.c``, ``cfgdefine.h``
================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

These are C 文件s that 用于 to 构建 mkconfig program.  The mkconfig
program 用于 during the initial NuttX 构建.

When you configure NuttX, you will copy a 配置 文件 called .config
in the top level NuttX 目录 (See :doc:`/components/boards` or
Documentation/NuttXPortingGuide.html).  The first time you make NuttX,
the top-level make文件 will 构建 the mkconfig executable from mkconfig.c
(using Make文件.host).  The top-level Make文件 will then 执行 the mkconfig
program to convert the .config 文件 in the top level 目录 into
include/nuttx/config.h.  config.h is a another version of the NuttX
配置 that can be included by C 文件s.
