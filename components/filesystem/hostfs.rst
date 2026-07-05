================
宿主文件系统
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

宿主文件系统提供了一种在模拟模式下挂载宿主操作系统目录的机制。要"挂载"的宿主目录在挂载命令中使用 ``-o`` 命令行开关指定，例如::

			mount -t hostfs -o fs=/home/user/nuttx_root /host

对于非 NSH 操作，选项 ``fs=home/user/nuttx_root`` 将通过可选的 ``void *data`` 参数传递给 ``mount()`` 例程。
