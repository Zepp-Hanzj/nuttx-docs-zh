=====
TMPFS
=====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX TMPFS 文件系统是一个基于动态 RAM 的小型文件系统。

可以通过在构建时向配置添加 ``CONFIG_FS_TMPFS=y`` 来启用。

在运行时，只需使用 ``mount -t tmpfs /tmp`` 即可获得由 TMPFS 支持的 ``/tmp`` 文件夹，然后可以在该文件夹下创建文件和文件夹。

请注意，TMPFS 由内核内存支持，因此不要期望在其上存储大文件，其大小受空闲内核内存限制。

我们可以使用 ``df -h`` 命令查看 TMPFS 的大小，特别是当文件在 TMPFS 文件夹中添加或删除时，可以看到 TMPFS 的 ``Size`` 列会变化。TMPFS 大小的变化总是反映在空闲内核内存大小的反向变化上。