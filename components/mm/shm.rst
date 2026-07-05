=====================
Shared Memory Support
=====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

前提条件
-------------

在提供共享内存支持之前，必须启用以下功能：

- ``CONFIG_ARCH_ADDRENV=y`` - 使用 MMU 支持每个任务的地址环境。
- ``CONFIG_BUILD_KERNEL=y`` - MMU 必须提供受保护的内核/用户空间内存区域支持。
- ``CONFIG_GRAN=y`` - 颗粒分配是所有分页分配的底层分配。
- ``CONFIG_MM_PGALLOC=y`` - 启用物理页分配器
- ``CONFIG_MM_PGSIZE`` - 确定 MMU 可映射的一个页面的大小。

最后：

- ``CONFIG_MM_SHM=y`` - 启用共享内存支持
- ``CONFIG_ARCH_SHM_VBASE`` - 共享内存区域起始的虚拟地址。
- ``CONFIG_ARCH_SHM_MAXREGIONS`` - 可为共享内存空间分配的最大区域数。此硬编码值允许静态分配共享内存数据结构，没有其他目的。默认为 1。
- ``CONFIG_ARCH_SHM_NPAGES`` - 可为共享内存区域分配的最大页数。默认为 1。

虚拟共享内存地址空间的大小由最大区域数、每区域最大页数和每页配置大小的乘积决定。

概念
--------

每个进程都有一个任务组结构 struct task_group_s，它保存组中所有线程共有的信息。如果 ``CONFIG_MM_SHM=y``，则这包括每进程共享内存虚拟页分配器的数据结构。

内存区域使用以下方式访问：

.. code-block:: C

    int shmget(key_t key, size_t size, int shmflg);

通过使用内部共享内存数据集以 key 作为查找匹配值进行查找。成功时，shmget 返回匹配的共享内存标识符 -- 在此实现中，该标识符就是匹配的表索引。

如果内存区域不存在，也可以由 shmget 创建（如果 shmflag 中设置了 IPC_CREAT 位）。创建共享内存区域时，会发生以下情况：

- 在内部数据集中保留一个新条目。键值被分配给条目，表索引就是新的共享内存标识符。

- 请求的大小被向上舍入到完整页面，每页大小为 ``CONFIG_MM_PGSIZE``。

- 分配一组物理页，这些页的物理地址保存在内部数据集中。

现在键映射到共享内存标识符（表索引），表索引提供对组成共享内存区域的物理页列表的访问。

注意：改进的实现可能会执行物理内存的"延迟"备份，即在需要内存时才分配物理内存，例如当应用程序尝试分配内存时发生页面错误。

共享内存区域通过以下方式销毁：

.. code-block:: C

    int shmctl(int shmid, int cmd, struct shmid_ds *buf);

为了使进程能够使用内存区域，必须使用以下方式将内存区域"附加"到进程：

.. code-block:: C

    FAR void *shmat(int shmid, FAR const void *shmaddr, int shmflg);

``shmat()`` 返回共享内存可在用户进程中找到的虚拟地址。附加共享内存区域涉及以下步骤：

- 使用 shmid 作为表索引在共享内存内部数据结构中查找映射。

- 使用可在调用进程的任务组结构中找到的每进程虚拟共享内存虚拟页分配器，分配与物理地址空间相同大小的虚拟地址空间。

- 使用平台特定接口将物理内存映射到选定的虚拟地址空间，以及

- 将分配的虚拟基地址返回给调用者。

内存区域可以使用以下方式从用户进程分离：

.. code-block:: C

    int shmdt(FAR const void *shmaddr);

相关头文件
---------------------

- ``include/sys/shm.h`` - 共享内存接口声明
- ``include/sys/ipc.h`` - 提供共享内存接口使用的额外定义
- ``include/nuttx/addrenv.h`` - 定义进程的虚拟地址空间。
- ``include/nuttx/pgalloc.h`` - 页分配器接口
- ``mm/shm/shm.h`` - 内部共享内存定义。这包括内部共享内存数据结构的定义。
