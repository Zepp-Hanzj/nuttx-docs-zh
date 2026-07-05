==================
伪文件系统
==================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

.. warning::
    迁移自:
    https://cwiki.apache.org/confluence/display/NUTTX/Pseudo+File+System

概述
========

伪根文件系统
-----------------------

NuttX 包含一个可选的、可扩展的文件系统。至少，它可以是一个简单的内存中伪文件系统。这是一个内存中的文件系统，因为它不需要任何存储介质或块驱动程序支持。相反，文件系统内容在通过标准文件系统操作（open、close、read、write 等）引用时即时生成。从这个意义上说，文件系统是一个伪文件系统（与 Linux ``/proc`` 文件系统也被称为伪文件系统相同的意义）。

任何用户提供的数据或逻辑都可以通过伪文件系统访问。在 ``/dev`` 伪文件系统目录中提供了对字符、块和 MTD（内存技术设备）驱动程序的内置支持。

特殊文件
-------------

NuttX 不像 Linux 那样支持特殊文件。事实上，更正确的说法是 NuttX 文件系统根本不支持特殊文件。

然而，NuttX 支持类似 Linux 的特殊 `设备节点`、字符驱动程序和块驱动程序文件（以及 NuttX 特定的挂载点、命名信号量、消息队列和共享内存特殊文件）。但是，这些不是 POSIX 环境中使用的特殊文件：在 NuttX 中，这些特殊文件只能在根伪文件系统中创建。有关设备节点的情况，请参阅 `设备节点 <https://cwiki.apache.org/confluence/display/NUTTX/Device+Nodes>`_ 获取更多信息。

在 NuttX 中，基本原则是所有 `命名资源` 都作为特殊文件出现在根伪文件系统中，并由 VFS 管理。

已挂载的卷
---------------

简单的内存中文件系统可以通过挂载提供访问某些大容量存储设备支持的真正文件系统的块设备来扩展。NuttX 支持标准的 mount() 命令，允许将块驱动程序绑定到伪文件系统中的挂载点和文件系统。目前，NuttX 支持标准的 VFAT 和 ROMFS 文件系统、特殊的磨损均衡 NuttX FLASH 文件系统（NXFFS），以及网络文件系统客户端（NFS 版本 3，UDP）。

与 Linux 的比较
-------------------

从编程角度来看，NuttX 文件系统看起来与 Linux 文件系统非常相似。然而，有一个根本区别：NuttX 根文件系统是一个伪文件系统，真正的文件系统可以挂载在伪文件系统中。相比之下，在典型的 Linux 安装中，Linux 根文件系统是一个真正的文件系统，伪文件系统可以挂载在真正的根文件系统中。NuttX 选择的方法旨在支持从非常小的平台到中等平台的更大可扩展性。

FAQ
===

**问题**：我想知道为什么我不能创建目录。如果我尝试创建一个目录。

.. code-block:: bash

    mkdir /mnt

我得到这个错误，

.. code-block:: bash

    nsh: mkdir: mkdir failed: 2

但如果我这样做，它会创建两个目录 mnt 和 sda

.. code-block:: bash

    mount -t vfat /dev/mmcsd0 /mnt/sda

**回答**：这是因为顶层目录是 `伪文件系统` 的一部分——就像 Linux 的 ``proc/`` 或 ``sys/`` 文件系统一样。但 NuttX 伪文件系统从顶层 ``/`` 开始。

这真正意味着您一定选择了 ``CONFIG_DISABLE_PSEUDOFS_OPERATIONS``。因为您通常可以在伪文件系统中正常创建目录：

.. code-block:: bash

    NuttShell (NSH) NuttX-9.0.0
    nsh> mkdir /mnt
    nsh> ls
    /:
    dev/
    etc/
    mnt/
    proc/
    tmp/
    nsh> ls mnt
    /mnt:
    nsh>

但假设您确实禁用了伪文件系统上的操作。为什么它不起作用？那里没有真正的媒体，因此您不能在那里创建文件或创建任何目录。``mount`` 命令是特殊的，它知道如何在伪文件系统中创建挂载点。

伪文件系统只是 RAM 中的树结构。它有两个目的：（1）您不需要有真正的文件系统来使用 NuttX。它开箱即用，具有可用（但有限）的伪文件系统。这允许即使在资源非常有限的 MCU 上也能有更文明的编程环境。（2）这个伪文件系统是所有 NuttX 特殊文件保留的地方：字符驱动程序、块驱动程序和挂载点。

NuttX 顶层伪文件系统创建了目录的 `错觉`，并提供了一致的、无缝的语义来与挂载的文件系统交互。如果在您挂载在 ``/mnt/sda`` 的卷中有一个名为 ``hello.txt`` 的文件，那么：

``/mnt`` - 是伪文件系统中的一个 `节点`，它只包含名称 mnt 并提供指向 mnt `下` 内容的链接。

``/mnt/sda`` - 这指的是一个包含名称 sda 的节点，可以在名称为 mnt 的节点 `下` 找到。此节点是伪文件系统中的特殊 `挂载点节点`。它包含与真正文件系统交互所需的方法。``/mnt/sda`` `下` 的所有内容都在物理媒体中。

``/mnt/sda/hello.txt`` - 这然后指的是挂载媒体上相对路径 ``hello.txt`` 处的文件 ``hello.txt``。从伪文件系统到真正媒体的过渡是无缝的。

这与 Linux 有些不同：Linux 必须始终用 `真正的` 文件系统启动——即使它只是一个 initrd RAM 磁盘。在 Linux 中，这些特殊文件（链接、驱动程序、管道等）驻留在真正的媒体上，可以驻留在任何兼容 Linux 的文件系统中。

普通的 ``mkdir`` 只能在有 `真正` 文件系统的位置工作。伪文件系统中没有真正的目录。伪文件系统支持看起来像目录并具有某些目录属性的 `节点`（如上面提到的 ``/mnt`` 节点）。但这实际上是一种错觉。

如果未启用 ``CONFIG_DISABLE_PSEUDOFS_OPERATIONS``，则 NuttX 添加了使用 ``mkdir`` 在伪文件系统中创建新的空 `节点` 的能力，完善了这种错觉。

[另一方面，所有目录在某种意义上都是一种 `错觉`，我想从这个意义上说，伪文件系统中的这些节点与任何其他目录一样"真实"。]

在您将 SD 卡挂载到 ``/mnt/sda`` 后，您可以执行：

.. code-block:: bash

    mkdir /mnt/sda/newdir

这应该可以正常工作，并在挂载卷的相对路径 ``newdir`` 处创建一个目录。

还有一些其他特殊的 NSH 命令（如 mount）可以更改伪文件系统。如 ``losetup``、``mkfifo``、``mkrd``、``umount`` 等。事实上，这些命令 `只` 在伪文件系统中工作。在 ``/mnt/sda`` 中尝试它们……它们不会工作。

但是任何修改文件或目录的 `普通` 命令都不会在伪文件系统中工作：``mkdir``、``mv``、``rm``、``rmdir``。这些都需要真正的媒体。它们不会在伪文件系统中工作，但会在 ``/mnt/sda`` 中工作。

尝试管道到伪文件系统中的内容也会失败。例如，您不能这样做：

.. code-block:: bash

    NuttShell (NSH) NuttX-6.20
    nsh> cat "Hello, World!" >/hello.text
    nsh> cat: open failed: 22
    nsh>

另请参见 `移植指南 <https://cwiki.apache.org/confluence/display/NUTTX/Porting+Guide>`_ 中的 NxFileSystem