===============
分区表
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

基于文本的分区表
==========================

**摘要**

TXTABLE - 存储在最后一个擦除块中（或在 romdisk 中作为备份）的基于文本的分区表。

1. 第一行必须是"魔术字+版本"，当前为 "TXTABLE0"。
#. 第二行及后续行是分区条目（最少：一个），格式为："%s %zx %zx"（表示名称、大小和偏移量（字节）（十六进制））。
#. 大小或偏移量可以默认为零（表示零（对于第 1 个条目）或计算值（对于其他条目）），将由解析器参考前一个和下一个条目来计算。
#. 最后一个擦除块将被注册为名为 "txtable" 的伪分区。如果最后一个擦除块包含在最后一个实际分区中，它将被排除在外。

为避免 PTABLE 的问题：在多个 NuttX 二进制文件的情况下，分区表可能不同步。

而且它更简单：

1. 带有简单规则的文本格式（名称 + 大小 + 偏移量）。
#. 大小或偏移量可以是默认值（参考前一个和下一个条目计算）。
#. 支持备份表（例如 ROMFS 中的 /etc/txtable.txt）

大小/偏移量可以自动计算，情况：

1. 第一个条目的偏移量为零，其他条目的偏移量为零：自动计算；
#. 最后一个条目的大小为零：填充到整个 Flash 的末尾（保留最后一个擦除块）；其他条目的大小为零：自动计算（next.offset - current.offset）；
#. 典型情况 1：所有条目的大小为零（自动计算），偏移量非零；
#. 典型情况 2：某个条目的大小和偏移量都为零，但两个相邻条目的大小和偏移量都非零；

**示例**

"partition6" 的大小和偏移量都为零，"partition7" 和 "data" 之间存在间隙，并且不保留最后一个擦除块。

* txtable.txt

  ::

    TXTABLE0
    partition1 0x6C000 0x4000
    partition2 0x10000 0x70000
    partition3 0x80000 0x80000
    partition4 0x80000 0x100000
    partition5 0x280000 0x180000
    partition6 0 0
    partition7 0x10000 0x480000
    data 0 0x500000



* 解析结果

  | 保留了最后一个擦除块，partition7 和 data 之间的间隙被保留。
  | 格式：名称、偏移量、大小

  ::

    /dev/partition1   offset 0x00004000, size 0x0006c000
    /dev/partition2   offset 0x00070000, size 0x00010000
    /dev/partition3   offset 0x00080000, size 0x00080000
    /dev/partition4   offset 0x00100000, size 0x00080000
    /dev/partition5   offset 0x00180000, size 0x00280000
    /dev/partition6   offset 0x00400000, size 0x00080000
    /dev/partition7   offset 0x00480000, size 0x00010000
    /dev/data         offset 0x00500000, size 0x00aff000
    /dev/txtable      offset 0x00fff000, size 0x00001000

多个未设置大小或偏移量

* txtable.txt

  ::

    TXTABLE0
    partition1 0 0x4000
    partition2 0 0x70000
    partition3 0 0x80000
    partition4 0x80000 0x100000
    partition5 0x280000 0
    partition6 0 0
    partition7 0x10000 0x480000
    data 0 0x500000

* 解析结果

  | partition[2,3,4,6] 和 data 的大小被计算，partition7 和 data 之间的间隙被保留。

  ::

    /dev/partition1   offset 0x00004000, size 0x0006c000
    /dev/partition2   offset 0x00070000, size 0x00010000
    /dev/partition3   offset 0x00080000, size 0x00080000
    /dev/partition4   offset 0x00100000, size 0x00080000
    /dev/partition5   offset 0x00180000, size 0x00280000
    /dev/partition6   offset 0x00400000, size 0x00080000
    /dev/partition7   offset 0x00480000, size 0x00010000
    /dev/data         offset 0x00500000, size 0x00aff000
    /dev/txtable      offset 0x00fff000, size 0x00001000

仅一个分区条目且未指定大小

* txtable.txt

  ::

    TXTABLE0
    partition1 0x0 0x4000

* 解析结果

  | 保留了最后一个擦除块，大小正确。

  ::

    /dev/partition1   offset 0x00004000, size 0x00ffb000
    /dev/txtable      offset 0x00fff000, size 0x00001000

空行和换行符分隔

* txtable.txt

  | 换行：CR + LF / LF。
  | 在 "%s %zx %zx" 之后的额外字符/字符串。

  ::

    TXTABLE0
    partition1 0x6C000 0x4000
    partition2 0 0x70000
    partition3 0 0x80000
    partition4 0 0x100000
    partition5 0x280000 0x180000
    partition6 0x80000 0x400000   # String between "%s %zx %zx" and "LF" will be ignored.
    partition7 0x10000 0x480000   # Comments: This is the 7th partition.
    data 0 0x500000
    
    
    
    EOF

* 解析结果

  | 空行被忽略，"LF" 或 "CRLF" 的换行都被解析。
    "%s %zx %zx" 和 "LF" 之间的字符串将被忽略（例如 CR 或某些注释）。

  ::

    /dev/partition1   offset 0x00004000, size 0x0006c000
    /dev/partition2   offset 0x00070000, size 0x00010000
    /dev/partition3   offset 0x00080000, size 0x00080000
    /dev/partition4   offset 0x00100000, size 0x00080000
    /dev/partition5   offset 0x00180000, size 0x00280000
    /dev/partition6   offset 0x00400000, size 0x00080000
    /dev/partition7   offset 0x00480000, size 0x00010000
    /dev/data         offset 0x00500000, size 0x00aff000
    /dev/txtable      offset 0x00fff000, size 0x00001000