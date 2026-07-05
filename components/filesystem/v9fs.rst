V9FS
====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

V9FS 是基于 9P2000.L 协议的远程文件系统。

将 V9FS 添加到 NuttX 配置
======================================

V9FS 客户端很容易添加到您的配置中。只需将 ``CONFIG_FS_V9FS`` 添加到 ``nuttx/.config``。

为了完整运行 V9FS，您还需要选择传输层驱动程序。目前可用的两种是：

  - **VIRTIO** -> ``CONFIG_V9FS_VIRTIO_9P=y``
  - **SOCKET** -> ``CONFIG_V9FS_SOCKET_9P=y``

NFS 挂载命令
=================

在 V9FS 中，我们有一些特殊参数

  - ``uname``. 用于指示客户端的用户身份
  - ``aname``. 可选，指定客户端请求访问的文件树
  - ``trans``. 选择传输层（virtio/socket）
  - ``msize``. 消息的最大大小
  - ``tag``. 挂载点的标签

不同的传输层对参数传递有不同的要求。以下是一些示例：

Qemu + VIRTIO
--------------

.. code-block:: console

  mount -t v9fs -o trans=virtio,tag=<mount_tag> /dir

同样，我们需要在 qemu 中带入相应的参数

.. code-block:: console

  -fsdev local,security_model=none,id=fsdev1,path=<share-path> \
  -device virtio-9p-device,id=fs1,fsdev=fsdev1,mount_tag=<mount_tag>

有关如何在 QEMU 中启动 virtio-9p，请参考文档：

  - https://wiki.qemu.org/Documentation/9psetup


Socket
-------

.. code-block:: console

  mount -t v9fs -o trans=socket,tag=<IP Address>:[Port Default 563],aname=[path] /dir

有多种类型的 9P 套接字服务器。这里我们使用 R9-fileserver
（一个基于 Rust 的跨平台 9p 服务器
https://github.com/crafcat7/R9-fileserver）

.. code-block:: console

  sudo ./ya-vm-file-server --network-address <IP Address>:<Server Port> --mount-point <share-path>


结果
------

.. code-block:: fish

  NuttShell (NSH)
  nsh> mkdir mnt
  nsh> 
  nsh> ls mnt
  /mnt:
  nsh> mount -t v9fs -o trans=virtio,tag=hostshare /mnt/v9fs
  nsh> 
  nsh> ls /mnt/v9fs
  /mnt/v9fs:
  sdcard/
  mnt/
  nsh> 
  nsh> echo "This is a test" >/mnt/v9fs/testfile.txt
  nsh> ls -l /mnt/v9fs
  /mnt/v9fs:
  drwxrwxrwx    1000    1000        4096 sdcard/
  -rw-rw-rw-    1000    1000          15 testfile.txt
  drwxrwxrwx    1000    1000        4096 mnt/
  nsh> 
  nsh> cat /mnt/v9fs/testfile.txt
  This is a test
  nsh> 