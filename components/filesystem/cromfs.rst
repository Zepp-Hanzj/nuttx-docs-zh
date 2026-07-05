======
CROMFS
======

概述
========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此目录包含 CROMFS 文件系统。这是一个内存中（不需要块驱动）的只读（可以存放在 FLASH 中）文件系统。它仅对数据使用 LZF 解压缩（元数据不压缩）。

它通过目录内存读取来访问内存中的文件系统，因此只能存在于随机访问的 NOR 类型 FLASH 中。它旨在用于大多数 MCU 上的片上 FLASH（该设计也可以扩展为访问非随机访问 FLASH，但这些扩展尚未实现）。

目前还没有很好的方法来测量使用 LZF 获得的压缩率。我在其他应用中看到过 37% 的压缩率报告，所以暂时接受这个数据。这意味着，例如，一个包含 512Kb 数据的文件系统可以仅占用 322Kb 的 FLASH 空间，从而为您腾出 190Kb 的空间做其他事情。

LZF 压缩以其快速解压缩而非高压缩率而闻名。根据 LZF 解压缩例程作者的说法，它几乎和 memcpy 一样快！

还有一个新工具 ``/tools/gencromfs.c``，它将为 NuttX CROMFS 文件系统生成二进制镜像，以及一个位于 ``apps/examples/cromfs`` 的示例 CROMFS 文件系统镜像。该示例包含一个如下所示的测试文件系统::

  $ ls -Rl ../apps/examples/cromfs/cromfs
  ../apps/examples/cromfs/cromfs:
  total 2
  -rwxr--r--+ 1 spuda spuda 171 Mar 20 08:02 BaaBaaBlackSheep.txt
  drwxrwxr-x+ 1 spuda spuda   0 Mar 20 08:11 emptydir
  -rwxr--r--+ 1 spuda spuda 118 Mar 20 08:05 JackSprat.txt
  drwxrwxr-x+ 1 spuda spuda   0 Mar 20 08:06 testdir1
  drwxrwxr-x+ 1 spuda spuda   0 Mar 20 08:10 testdir2
  drwxrwxr-x+ 1 spuda spuda   0 Mar 20 08:05 testdir3
  ../apps/examples/cromfs/cromfs/emptydir:
  total 0
  ../apps/examples/cromfs/cromfs/testdir1:
  total 2
  -rwxr--r--+ 1 spuda spuda 249 Mar 20 08:03 DingDongDell.txt
  -rwxr--r--+ 1 spuda spuda 247 Mar 20 08:06 SeeSawMargorieDaw.txt
  ../apps/examples/cromfs/cromfs/testdir2:
  total 5
  -rwxr--r--+ 1 spuda spuda  118 Mar 20 08:04 HickoryDickoryDock.txt
  -rwxr--r--+ 1 spuda spuda 2082 Mar 20 08:10 TheThreeLittlePigs.txt
  ../apps/examples/cromfs/cromfs/testdir3:
  total 1
  -rwxr--r--+ 1 spuda spuda 138 Mar 20 08:05 JackBeNimble.txt

当构建到 NuttX 中并部署到目标设备时，它看起来像::

  NuttShell (NSH) NuttX-7.24
  nsh> mount -t cromfs /mnt/cromfs
  nsh> ls -Rl /mnt/cromfs
  /mnt/cromfs:
   dr-xr-xr-x       0 .
   -rwxr--r--     171 BaaBaaBlackSheep.txt
   dr-xr-xr-x       0 emptydir/
   -rwxr--r--     118 JackSprat.txt
   dr-xr-xr-x       0 testdir1/
   dr-xr-xr-x       0 testdir2/
   dr-xr-xr-x       0 testdir3/
  /mnt/cromfs/emptydir:
   drwxrwxr-x       0 .
   dr-xr-xr-x       0 ..
  /mnt/cromfs/testdir1:
   drwxrwxr-x       0 .
   dr-xr-xr-x       0 ..
   -rwxr--r--     249 DingDongDell.txt
   -rwxr--r--     247 SeeSawMargorieDaw.txt
  /mnt/cromfs/testdir2:
   drwxrwxr-x       0 .
   dr-xr-xr-x       0 ..
   -rwxr--r--     118 HickoryDickoryDock.txt
   -rwxr--r--    2082 TheThreeLittlePigs.txt
  /mnt/cromfs/testdir3:
   drwxrwxr-x       0 .
   dr-xr-xr-x       0 ..
   -rwxr--r--     138 JackBeNimble.txt
  nsh>

我尝试的所有操作都正常工作：查看目录、cat 文件等。"."" 和 ".." 硬链接也正常工作::

  nsh> cd /mnt/cromfs
  nsh> cat emptydir/../testdir1/DingDongDell.txt
  Ding, dong, bell,
  Pussy's in the well.
  Who put her in?
  Little Johnny Green.

  Who pulled her out?
  Little Tommy Stout.
  What a naughty boy was that,
  To try to drown poor pussy cat,
  Who never did him any harm,
  And killed the mice in his father's barn.

  nsh>

gencromfs
=========

genromfs 程序可以在 tools/ 目录中找到。它是一个名为 gencromfs.c 的单个 C 文件。可以通过以下方式构建::

    cd tools
    make -f Makefile.host gencromfs

genromfs 工具用于生成 CROMFS 文件系统镜像。使用方法很简单::

    gencromfs <dir-path> <out-file>

其中::

    <dir-path> 是将成为新 CROMFS 文件系统镜像根目录的目录路径。
    <out-file> 是生成的输出 C 文件的名称。必须编译此文件才能生成二进制 CROMFS 文件系统镜像。

所有这些步骤都已在 ``apps/examples/cromfs/Makefile`` 中自动完成。请参考该 Makefile 作为参考。

架构
============

CROMFS 文件系统由内存中的数据结构表示。该结构是一棵"树"。树的根是一个"卷节点"，描述整个操作系统。文件系统中的其他实体由其他类型的节点表示：硬链接、目录和文件。这些节点都在 ``fs/cromfs/cromfs.h`` 中描述。

除了常规的卷信息外，卷节点还提供到"根目录"的偏移量。根目录与所有其他 CROMFS 目录一样，只是其他节点的单链表：硬链接节点、目录节点和文件。该列表由"同级偏移量"管理：目录中的每个节点都包含指向同一目录中下一个同级节点的偏移量。该目录列表以零偏移量终止。

卷头位于偏移量零处。因此，任何节点或数据块的偏移量都可以通过将该偏移量加上卷头的已知地址来转换为内存中 CROMFS 镜像的绝对地址。

目录列表中的每个硬链接、目录和文件节点都包含指向列表中下一个节点的这样一个"同级偏移量"。每个节点后面跟着以 NUL 结尾的节点名称。每个节点还持有一个额外的偏移量。目录节点包含一个"子偏移量"，即指向构成子目录的另一个单链表节点中第一个条目的偏移量。

硬链接节点持有指向链接目标节点的"链接偏移量"。链接偏移量可以是另一个硬链接节点、目录或文件节点的偏移量。目录链接偏移量将引用表示该目录的单链目录列表中的第一个节点。

文件节点提供文件数据。文件名字符串后面跟着一个可变长度的压缩数据块列表。在这种情况下，每个压缩数据块以 ``include/lzf.h`` 中描述的 LZF 头开始。

因此，根据这个描述，我们可以用以下节点来说明上面的示例 CROMFS 文件系统（其中 V=卷节点，H=硬链接节点，D=目录节点，F=文件节点，D=数据块)::

  V
  `- +- H: .
     |
     +- F: BaaBaaBlackSheep.txt
     |  `- D,D,D,...D
     +- D: emptydir
     |  |- H: .
     |  `- H: ..
     +- F: JackSprat.txt
     |  `- D,D,D,...D
     +- D: testdir1
     |  |- H: .
     |  |- H: ..
     |  |- F: DingDongDell.txt
     |  |  `- D,D,D,...D
     |  `- F: SeeSawMargorieDaw.txt
     |     `- D,D,D,...D
     +- D: testdir2
     |  |- H: .
     |  |- H: ..
     |  |- F: HickoryDickoryDock.txt
     |  |  `- D,D,D,...D
     |  `- F: TheThreeLittlePigs.txt
     |     `- D,D,D,...D
     +- D: testdir3
        |- H: .
        |- H: ..
        `- F: JackBeNimble.txt
           `- D,D,D,...D

其中，例如::

  H: ..

    表示一个名为 ".." 的硬链接节点

  |
  +- D: testdir1
  |  |- H: .

    表示一个名为 "testdir1" 的目录节点。该目录列表的第一个节点是名为 "." 的硬链接

  |
  +- F: JackSprat.txt
  |  `- D,D,D,...D

    表示一个名为 "JackSprat.txt" 的文件节点，后面跟着一些压缩数据块序列 D。

配置
=============

要构建 CROMFS 文件系统，您需要在配置中添加以下内容：

1. 启用 LZF（其他 LZF 设置仅适用于压缩，因此对只进行解压缩的 CROMFS 没有影响)::

     CONFIG_LIBC_LZF=y

   注意：当启用 CONFIG_FS_CROMFS 时，这应该会自动被选中。

2. 启用 CROMFS 文件系统::

     CONFIG_FS_CROMFS=y

3. 启用 ``apps/examples/cromfs`` 示例::

     CONFIG_EXAMPLES_CROMFS=y

   或者如果您喜欢，可以使用 ``apps/examples/elf`` 示例::

     CONFIG_ELF=y
     # CONFIG_BINFMT_DISABLE is not set
     CONFIG_EXAMPLES_ELF=y
     CONFIG_EXAMPLES_ELF_CROMFS=y

   或者以该示例为指导实现您自己的自定义 CROMFS 文件系统。
