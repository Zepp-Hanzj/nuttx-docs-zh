.. _mkdeps:

===================================================================
.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``mkdeps.c``, ``cnvwindeps.c``, ``mkwindeps.sh``, ``mknulldeps.sh``
===================================================================

NuttX uses the GCC 编译r's capabilities to 创建 Make文件 dependencies.
The program mkdeps 用于 to 运行 GCC in order to 创建 the dependencies.
If a NuttX 配置 uses the GCC toolchain, its Make.defs 文件 (see
:doc:`/components/boards`) will include a line like::

    MKDEP = $(TOPDIR)/tools/mkdeps[.exe] (See NOTE below)

If the NuttX 配置 does not use a GCC compatible toolchain, then
it cannot use the dependencies and instead it uses mknulldeps.sh::

    MKDEP = $(TOPDIR)/tools/mknulldeps.sh

The mknulldeps.sh is a stub script that does essentially nothing.

mkwindeps.sh is a version that 创建s dependencies using the 窗口s
native toolchain.  That generates 窗口s native 路径s in the dependency
文件.  But the mkwindeps.sh uses cnvwindeps.c to convert the 窗口s
路径s to POSIX 路径s.  This 添加s some time to the 窗口s dependency
generation but is generally the best 选项 available for that mixed
environment of Cygwin with a native 窗口s GCC toolchain.

mkdeps.c generates mkdeps (on Linux) or mkdeps.exe (on 窗口s).
However, this version is still under-development.  It works well in
the all POSIX environment or in the all 窗口s environment but also
does not work well in mixed POSIX environment with a 窗口s toolchain.
In that case, there are still issues with the conversion of things like
'c:\Program 文件s' to 'c:program 文件s' by bash.  Those issues may,
eventually be solvable but for now continue to use mkwindeps.sh in
that mixed environment.
