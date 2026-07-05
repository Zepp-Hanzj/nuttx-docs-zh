=================
NFS 客户端指南
=================

将 NFS 添加到 NuttX 配置
=====================================

NFS 客户端可以轻松添加到你的配置中：你只需在 ``nuttx/.config`` 文件中
添加 ``CONFIG_NFS``。但是，对其他系统设置有一些依赖：

首先，你必须配置一些内容才能使用任何文件系统：

  -  ``CONFIG_DISABLE_MOUNTPOINT=n``。你必须在伪文件系统中包含对挂载点的支持。

并且对网络配置有几个依赖。至少，你需要选择以下内容：

  -  ``CONFIG_NET=y``。通用网络支持。
  -  ``CONFIG_NET_UDP=y``。UDP 支持。

挂载接口
===============

提供了一个低级的、C 可调用的接口来挂载文件系统。
该接口称为 ``mount()``，在移植指南中有提及，
并在头文件 ``include/sys/mount.h`` 中声明原型：

.. c:function:: int mount(const char *source, const char *target, const char *filesystemtype, unsigned long mountflags, const void *data)

  ``mount()`` 将 ``source`` 块设备名称指定的文件系统
  附加到 ``target`` 指定的路径上的根文件系统中。

  :param source: 以空字符结尾的字符串，提供 NuttX 伪文件系统中
     块驱动的完整路径。
  :param target: NuttX 伪文件系统中要挂载卷的位置。
  :param filesystemtype: 标识要使用的文件系统类型的字符串。
  :param mountflags: 可用于限定文件系统挂载方式的各种标志。
  :param data: 挂载时传递给文件系统的不透明数据。

  :return: 成功时返回零；错误时返回 -1，并适当设置 ``errno``：

    -  ``EACCES``。路径的某个组件不可搜索，或者尝试挂载只读文件系统
       而未给出 ``MS_RDONLY`` 标志。
    -  ``EBUSY``。``source`` 已经被挂载。
    -  ``EFAULT``。某个指针参数指向用户地址空间之外。
    -  ``EINVAL``。``source`` 具有无效的超级块。
    -  ``ENODEV``。``filesystemtype`` 未配置。
    -  ``ENOENT``。路径名为空或包含不存在的组件。
    -  ``ENOMEM``。无法分配内存来复制文件名或数据。
    -  ``ENOTBLK``。``source`` 不是块设备。

此相同接口可用于使用一些特殊参数挂载远程 NFS 文件系统。
NFS 挂载与 *普通* 文件系统挂载的不同之处在于：
(1) NFS 文件系统没有块驱动，(2) 必须将特殊参数作为 ``data`` 传递
以描述远程 NFS 服务器。因此以下代码片段可以表示如何挂载 NFS 文件系统：

.. code-block:: c

  #include <sys/mount.h>
  #include <nuttx/fs/nfs.h>

  struct nfs_args data;
  char *mountpoint;

  ret = mount(NULL, mountpoint, string "nfs", 0, (FAR void *)&data);

注意：(1) 块驱动参数为 ``NULL``。``mount()`` 足够智能，知道 NFS 文件系统
不需要块驱动。(2) NFS 文件系统用简单字符串 "nfs" 标识。
(3) ``struct nfs_args`` 的引用作为 NFS 特定参数传递。

NFS 特定接口在文件 ``include/nuttx/fs/nfs.h`` 中描述。
在那里你可以看到 ``struct nfs_args`` 定义如下：

.. code-block:: c

  struct nfs_args
  {
    uint8_t  addrlen;               /* Length of address */
    uint8_t  sotype;                /* Socket type */
    uint8_t  flags;                 /* Flags, determines if following are valid: */
    uint8_t  timeo;                 /* Time value in deciseconds (with NFSMNT_TIMEO) */
    uint8_t  retrans;               /* Times to retry send (with NFSMNT_RETRANS) */
    uint16_t wsize;                 /* Write size in bytes (with NFSMNT_WSIZE) */
    uint16_t rsize;                 /* Read size in bytes (with NFSMNT_RSIZE) */
    uint16_t readdirsize;           /* readdir size in bytes (with NFSMNT_READDIRSIZE) */
    char    *path;                  /* Server's path of the directory being mount */
    struct   sockaddr_storage addr; /* File server address (requires 32-bit alignment) */
  };

NFS 挂载命令
=================

:NuttShell (NSH) <nsh>` 也支持名为 ``nfsmount`` 的命令，
可用于通过 NSH 命令行挂载远程文件系统。

**命令语法：**

.. code-block::

  nfsmount <server-address> <mount-point> <remote-path> [udp]

**概述**。``nfsmount`` 命令在 NuttX 伪文件系统中挂载网络文件系统。
``nfsmount`` 将使用 NFSv3 UDP 协议挂载远程文件系统。

**命令行参数**。``nfsmount`` 接受三个参数：

  #. ``<server-address>`` 是导出你希望挂载的文件系统的服务器的 IP 地址。
     此 NuttX RTOS 的 NFS 实现仅适用于局域网，因此服务器和客户端
     必须在同一网络中。
  #. ``<mount-point>`` 是 NuttX 伪文件系统中挂载卷将出现的位置。
     此挂载点只能位于 NuttX 伪文件系统中。按照惯例，此挂载点是
     ``/mnt`` 下的子目录。挂载命令将创建完成完整路径所需的
     任何伪目录（但完整路径不能已存在）。
  #. ``<remote-path>`` 是从服务器导出的文件系统 ``/`` 目录。
     此 ``/`` 目录必须在设置 NFS 服务器时已在服务器上配置为可导出。

卷挂载到 NuttX 伪文件系统后，可以像访问文件系统中的其他对象一样访问它。

**示例**。假设 NFS 服务器已配置为导出目录 ``/export/shared``。
以下命令将挂载该文件系统（假设目标板也有权限挂载该文件系统）。

.. code-block:: fish

  NuttShell (NSH)
  nsh> ls /mnt
  /mnt:
  nsh: ls: no such directory: /mnt
  nsh> nfsmount 10.0.0.1 /mnt/nfs /export/shared
  nsh> ls -l /mnt/nfs
  /mnt/nfs:
   drwxrwxrwx   4096 ..
   drwxrwxrwx   4096 testdir/
   -rw-rw-rw-      6 ctest.txt
   -rw-r--r--     15 btest.txt
   drwxrwxrwx   4096 .
  nsh> echo "This is a test" >/mnt/nfs/testdir/testfile.txt
  nsh> ls -l /mnt/nfs/testdir
  /mnt/nfs/testdir:
   -rw-rw-rw-     21 another.txt
   drwxrwxrwx   4096 ..
   drwxrwxrwx   4096 .
   -rw-rw-rw-     16 testfile.txt
  nsh> cat /mnt/nfs/testdir/testfile.txt
  This is a test

配置 NFS 服务器（Ubuntu）
===================================

服务器的设置将分两步完成：首先，设置 NFS 的配置文件，
然后启动 NFS 服务。但首先，你需要使用以下两个命令
在 Ubuntu 上安装 NFS 服务器：

.. code-block:: console

  $ sudo apt-get install nfs-common
  $ sudo apt-get install nfs-kernel-server

之后，我们需要创建或选择要从 NFS 服务器导出的目录。
在我们的例子中，我们将创建一个名为 ``/export`` 的新目录。

.. code-block:: console

  # sudo mkdir /export

重要的是 ``/export`` 目录允许所有人访问（777 权限），
因为我们将从客户端无认证地访问 NFS 共享。

.. code-block:: console

  # sudo chmod 777 /export

完成所有这些后，我们将需要编辑配置文件以设置 NFS 服务器：
``/etc/exports``。此文件包含条目列表；每个条目指示一个共享的卷
以及如何共享。有关此文件所有设置选项的完整描述，
请查看 man 页面（``man export``）。

``/etc/exports`` 中的条目通常如下所示：

.. code-block::

  directory machine1(option11,option12)

因此对于我们的示例，我们将 ``/export`` 导出到客户端 10.0.0.2，
添加条目：

.. code-block::

  /export 10.0.0.2(rw)

在我们的例子中，我们使用了所有默认选项，只是将 ``ro`` 替换为 ``rw``，
以便我们的客户端对我们正在导出的目录具有读写权限。

完成所有必要的配置后，我们就可以使用以下命令启动服务器：

.. code-block:: console

  # sudo /etc/init.d/nfs-kernel-server start

注意：如果你以后决定向 /etc/exports 文件添加更多 NFS 导出，
你需要重启 NFS 守护进程或运行 exportfs 命令。

.. code-block:: console

  # sudo /etc/init.d/nfs-kernel-server start

或

.. code-block:: console

  # exportfs -ra

现在我们可以检查导出目录和挂载点是否正确设置。

.. code-block:: console

  # sudo showmount -e
  # sudo showmount -a

我们还可以验证 NFS 是否在系统中运行：

.. code-block:: console

    # rpcinfo –p
    program vers proto   port
       100000   2   tcp    111  portmapper
       100000   2   udp    111  portmapper
       100011   1   udp   749  rquotad
       100011   2   udp   749  rquotad
       100005   1   udp    759  mountd
       100005   1   tcp    761  mountd
       100005   2   udp    764  mountd
       100005   2   tcp    766  mountd
       100005   3   udp    769  mountd
       100005   3   tcp    771  mountd
       100003   2   udp   2049  nfs
       100003   3   udp   2049  nfs
       300019   1   tcp    830  amd
       300019   1   udp    831  amd
       100024   1   udp    944  status
       100024   1   tcp    946  status
       100021   1   udp   1042  nlockmgr
       100021   3   udp   1042  nlockmgr
       100021   4   udp   1042  nlockmgr
       100021   1   tcp   1629  nlockmgr
       100021   3   tcp   1629  nlockmgr
       100021   4   tcp   1629  nlockmgr

现在你的 NFS 服务器正在共享 ``/export`` 目录以供访问。
