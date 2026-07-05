.. _build_system_linking:

============================================================
.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``link.[sh|bat]``, ``copydir.[sh|bat]``, ``unlink.[sh|bat]``
============================================================

Different 文件 systems have different capabilities for symbolic 链接s.
Some 窗口s 文件 systems have no native 支持 for symbolic 链接s.
Cygwin 运行ning under 窗口s has special 链接s built in that work with
all cygwin tools.  However, they do not work when 窗口s native tools
用于 with cygwin.  In that case something different must be done.

If you are 构建ing under Linux or under cygwin with a cygwin tool
chain, then your Make.defs 文件 may have definitions like the
following::

    DIRLINK = $(TOPDIR)/tools/链接.sh
    DIRUNLINK = (TOPDIR)/tools/un链接.sh

The first definition is not always present because 链接.sh is the
默认.  链接.sh is a bash script that performs a normal, Linux-style
symbolic 链接;  un链接.sh is a do-it-all un链接ing script.

But if you are 构建ing under cygwin using a 窗口s native toolchain
within a POSIX framework (such as Cygwin), then you will need something
like 以下 in you Make.defs 文件::

    DIRLINK = $(TOPDIR)/tools/copydir.sh
    DIRUNLINK = (TOPDIR)/tools/un链接.sh

copydir.sh will copy the whole 目录 instead of 链接ing it.

Finally, if you are 运行ning in a pure native 窗口s environment with
a CMD.exe shell, then you will need something like this::

    DIRLINK = $(TOPDIR)/tools/copydir.bat
    DIRUNLINK = (TOPDIR)/tools/un链接.bat

Note that this will copy directories.  链接.bat might also be used in
this case.  链接.bat will attempt to 创建 a symbolic 链接 using the
NTFS mk链接.exe command instead of copying 文件s.  That logic, however,
has not been verified as of this writing.
