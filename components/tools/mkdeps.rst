.. _mkdeps:

===================================================================
``mkdeps.c``, ``cnvwindeps.c``, ``mkwindeps.sh``, ``mknulldeps.sh``
===================================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 使用 GCC 编译器的功能来创建 Makefile 依赖关系。
mkdeps 程序用于运行 GCC 以创建依赖关系。如果 NuttX 配置使用
GCC 工具链，其 Make.defs 文件（参见 :doc:`/components/boards`）
将包含如下行::

    MKDEP = $(TOPDIR)/tools/mkdeps[.exe] (See NOTE below)

如果 NuttX 配置不使用 GCC 兼容工具链，则无法使用依赖关系，
而是使用 mknulldeps.sh::

    MKDEP = $(TOPDIR)/tools/mknulldeps.sh

mknulldeps.sh 是一个本质上什么都不做的存根脚本。

mkwindeps.sh 是使用 Windows 原生工具链创建依赖关系的版本。
它在依赖文件中生成 Windows 原生路径。但 mkwindeps.sh 使用
cnvwindeps.c 将 Windows 路径转换为 POSIX 路径。这为 Windows
依赖生成增加了一些时间，但对于 Cygwin 配合原生 Windows GCC
工具链的混合环境来说，通常是最佳选择。

mkdeps.c 生成 mkdeps（在 Linux 上）或 mkdeps.exe（在 Windows 上）。
但是，此版本仍在开发中。它在全 POSIX 环境或全 Windows 环境中
工作良好，但在混合 POSIX 环境与 Windows 工具链的情况下
不能很好地工作。在这种情况下，bash 将 'c:\\Program Files' 转换为
'c:program files' 等问题仍然存在。这些问题最终可能是可解决的，
但目前在该混合环境中继续使用 mkwindeps.sh。
