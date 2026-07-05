=========================
共享内存文件系统
=========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这支持 POSIX shm_open() API，用于不相关应用程序之间的共享内存。

可以通过 ``CONFIG_FS_SHMFS=y`` 来启用。要查看其工作原理，还请通过 ``CONFIG_EXMAPLE_SHM=y`` 启用示例应用程序，并从 NSH 命令行运行 ``shm_test``。

但是，此文件系统不支持挂载操作。

如果在示例应用程序中注释掉使用 ``shm_unlink()`` 的行，运行示例后可以从 NSH 命令行看到 ``/var/shm/`` 下的文件。我们也可以从命令行删除该文件。
