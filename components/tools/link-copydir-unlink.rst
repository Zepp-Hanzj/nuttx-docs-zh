.. _build_system_linking:

============================================================
.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``link.[sh|bat]``, ``copydir.[sh|bat]``, ``unlink.[sh|bat]``
============================================================

不同的文件系统对符号链接的支持能力各不相同。某些 Windows 文件系统不原生支持
符号链接。在 Windows 下运行的 Cygwin 内置了适用于所有 Cygwin 工具的特殊链接
机制。然而，当 Windows 原生工具与 Cygwin 一起使用时，这些链接将无法工作。
在这种情况下，必须采取不同的方法。

如果你在 Linux 下或在使用 Cygwin 工具链的 Cygwin 下进行构建，那么你的
Make.defs 文件中可能会有如下定义::

    DIRLINK = $(TOPDIR)/tools/link.sh
    DIRUNLINK = (TOPDIR)/tools/unlink.sh

第一个定义并不总是存在，因为 link.sh 是默认值。link.sh 是一个执行常规
Linux 风格符号链接的 bash 脚本；unlink.sh 是一个处理所有取消链接操作的脚本。

但如果你在 Cygwin 下使用 Windows 原生工具链，并在 POSIX 框架（如 Cygwin）
内进行构建，那么你需要在 Make.defs 文件中添加如下内容::

    DIRLINK = $(TOPDIR)/tools/copydir.sh
    DIRUNLINK = (TOPDIR)/tools/unlink.sh

copydir.sh 将复制整个目录，而不是创建链接。

最后，如果你在纯 Windows 原生环境中使用 CMD.exe shell 运行，
那么你需要如下配置::

    DIRLINK = $(TOPDIR)/tools/copydir.bat
    DIRUNLINK = (TOPDIR)/tools/unlink.bat

请注意，这将会复制目录。在这种情况下也可以使用 link.bat。
link.bat 将尝试使用 NTFS mklink.exe 命令创建符号链接，而不是复制文件。
但截至本文编写时，该逻辑尚未经过验证。
