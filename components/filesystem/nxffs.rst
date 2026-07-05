=====
NXFFS
=====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本页面包含有关 NuttX 磨损均衡 FLASH 文件系统 NXFFS 实现的信息。

NXFFS 总体组织
==========================

以下示例假设每个 FLASH 擦除块有 4 个逻辑块。实际关系由 MTD 驱动程序报告的 FLASH 几何结构决定::

  ERASE LOGICAL                   Inodes begin with a inode header.  inode may
  BLOCK BLOCK       CONTENTS      be marked as "deleted," pending re-packing.
    n   4*n     --+--------------+
                  |BBBBBBBBBBBBBB| Logic block header
                  |IIIIIIIIIIIIII| Inodes begin with a inode header
                  |DDDDDDDDDDDDDD| Data block containing inode data block
                  | (Inode Data) |
        4*n+1   --+--------------+
                  |BBBBBBBBBBBBBB| Logic block header
                  |DDDDDDDDDDDDDD| Inodes may consist of multiple data blocks
                  | (Inode Data) |
                  |IIIIIIIIIIIIII| Next inode header
                  |              | Possibly a few unused bytes at the end of a block
        4*n+2   --+--------------+
                  |BBBBBBBBBBBBBB| Logic block header
                  |DDDDDDDDDDDDDD|
                  | (Inode Data) |
        4*n+3   --+--------------+
                  |BBBBBBBBBBBBBB| Logic block header
                  |IIIIIIIIIIIIII| Next inode header
                  |DDDDDDDDDDDDDD|
                  | (Inode Data) |
   n+1  4*(n+1) --+--------------+
                  |BBBBBBBBBBBBBB| Logic block header
                  |              | All FLASH is unused after the end of the final
                  |              | inode.
                --+--------------+

总体操作
=================

Inode 从 FLASH 的开头开始写入。当 inode 被删除时，它们被标记为已删除但不被移除。当写入新 inode 时，分配向 FLASH 的末尾进行——从而通过均等地使用所有 FLASH 块来支持磨损均衡。

当 FLASH 变满（FLASH 末尾没有更多空间）时，必须执行重新打包操作：所有标记为删除的 inode 最终被移除，剩余的 inode 被打包到 FLASH 的开头。然后分配继续在 FLASH 末尾释放的 FLASH 内存中进行。

头部
=======

``BLOCK HEADER``
    块头用于确定该块是否已被格式化，也指示永远不应使用的坏块。

``INODE HEADER``
    每个 inode 以一个 inode 头开始，包含 inode 的名称、指向第一个数据块的偏移量以及 inode 数据的长度等信息。

    目前，唯一支持的 inode 类型是文件。所以目前，术语文件和 inode 是可互换的。

``INODE DATA HEADER``
    Inode 数据包含在数据头中。对于给定的 inode，每个逻辑块最多有一个 inode 数据块。如果 inode 数据跨越多个逻辑块，则 inode 数据可能包含在多个数据块中，每个逻辑块一个。

NXFFS 限制
=================

此实现非常简单，因此在选择使用 NXFFS 之前，您应该了解以下几个限制：

1. 由于文件在 FLASH 中是连续的，并且分配总是向 FLASH 末尾进行，因此一次只能打开一个文件进行写入。可以打开多个文件进行读取。

2. 文件在关闭后不能增加大小。不支持 O_APPEND 打开标志。

3. 文件总是按顺序写入。在以写入方式打开的文件中进行 seek 将不起作用。

4. 没有目录，但是可以在文件名字符串中使用 '/' 来提供一些目录的错觉。

5. 文件可以打开进行读取或写入，但不能同时进行两者：不支持 O_RDWR 打开标志。

6. 重新打包过程仅在写入期间当 FLASH 末尾的空闲 FLASH 内存耗尽时发生。因此，偶尔文件写入可能需要很长时间。

7. 另一个限制是一次只能挂载一个 NXFFS 卷。这与我们绑定到 MTD 驱动程序（而不是块驱动程序）并绕过所有正常挂载操作的事实有关。

多个写入者
================

如上面的限制中所述，一次只能打开一个文件进行写入。如果一个线程已打开一个文件进行写入，而另一个线程尝试打开一个文件进行写入，则该第二个线程将被阻塞，必须等待第一个线程关闭文件。

这种行为对您的应用程序来说可能是也可能不是问题，取决于（1）第一个线程保持文件打开进行写入的时间长短，以及（2）第二个线程的行为有多关键。请注意，写入 FLASH 始终可以触发主要的 FLASH 重组，因此无法保证第一个条件：即使第一个线程只打算写入少量数据，它也可能长时间保持文件打开。

另请注意，如果同一线程尝试打开两个文件进行写入，将发生死锁条件。该线程将被阻塞等待自己关闭第一个文件。

ioctls
======

文件系统支持两个 ioctl：

``FIOC_REFORMAT``
  将强制擦除闪存并在其上写入一个全新的空 NXFFS 文件系统。

``FIOC_OPTIMIZE``
  将强制立即重新打包文件系统。这将避免在所有 FLASH 内存都已用尽的紧急情况下重新打包文件系统的延迟。相反，您可以将垃圾收集推迟到系统不忙的时候。在频繁抖动的文件系统上调用此函数将增加 FLASH 的磨损量！

待办事项
============

- statfs() 实现是最小的。它应该对 f_bfree、f_bavail、f_files、f_ffree 返回值进行一些计算。
- 有太多的分配和释放操作。可能需要预分配更多的结构。
- 文件名总是被提取并保存在分配的可变长度内存中。在读取期间不使用文件名，消除条目结构中的文件名将提高性能。
- 读取中存在很大的低效性。在每次读取时，逻辑每次都从文件开头搜索读取位置。每当执行 lseek() 时这可能是必要的，但通常不是。通过在读取打开文件结构中保留 FLASH 偏移量和读取位置信息可以提高读取性能。
- 容错性必须改进。我们需要绝对确保任何 FLASH 错误不会导致文件系统行为不正确。
- 磨损均衡可能需要改进（？）。文件在清理操作中被重新打包到 FLASH 的前端。然而，这意味着不经常修改的文件固定在 FLASH 的开头。这减小了在 FLASH 末尾移动文件的池的大小。随着文件系统中设备前端的固定文件越来越多，FLASH 末尾的块的磨损程度会增加。
- 当需要重组 FLASH 时，系统可能会长时间不可用。这是一个不好的行为。我认为需要的是一个定期运行的垃圾收集任务，这样当大型重组事件发生时，大部分工作已经完成。垃圾收集应搜索不再包含有效数据的有效块。它应该预先擦除它们，将它们置于良好但空的状态……全部准备好进行文件系统重组。注意：有 FIOC_OPTIMIZE IOCTL 命令，应用程序可以在系统不忙时使用它来强制垃圾收集。如果应用程序明智地使用，这可以消除问题。
- 更糟的是，当 NXFSS 重组 FLASH 时，如果电源循环发生在错误的时间，可能会损坏文件系统内容。
- 当前设计不允许以写入方式重新打开文件，除非将文件截断为零长度。这有效地禁止了实现正确的 truncate() 方法，该方法应更改先前写入的文件的大小。有一些零散的逻辑可用，但即使这些也被 __NO_TRUNCATE_SUPPORT__ 条件排除。

进一步参考
=================

.. toctree::
  how_nxffs_works.rst