=========================
运行时栈统计
=========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

介绍
=========
调试代码时，通常需要关注如何跟踪调用函数的最大栈使用量，以优化代码结构并减少栈使用。本文将介绍一种基于运行状态跟踪所有任务最深调用栈的方法。

配置
=============
   .. code-block:: c

      CONFIG_SCHED_STACKRECORD=32
      CONFIG_ARCH_INSTRUMENT_ALL=y

```CONFIG_SCHED_STACKRECORD``` 用于记录所有任务的最大栈使用量。
```CONFIG_ARCH_INSTRUMENT_ALL``` 用于对所有代码进行插桩。

请注意，CONFIG_ARCH_INSTRUMENT_ALL 不是必需的。此配置选项会对所有代码进行插桩，但如果你只想对特定函数进行插桩，可以在相应的 makefile 中添加 '-finstrument-functions'。

示例
=======
1. ```./tools/configure.sh esp32c3-devkit:stack```
2. ```make -j20```
3. 将镜像烧录到你的板卡
   .. code-block :: bash

      nsh> cat /proc/1/stack
      StackAlloc: 0x3fc8b5b0
      StackBase:  0x3fc8b5e0
      StackSize:  2000
      MaxStackUsed:1344
      Backtrace         Size
      0x42009198          32
      0x42009200          48
      0x420081a0         128
      0x42008d18          64
      0x4201da60          80
      0x420199e0          80
      0x42018c6c          48
      0x420194f4          48
      0x42017d30          32
      0x4201634c          32
      0x420163ac          48
      0x42016408          32
      0x420132c0          48
      0x42010598          32
      0x4200fd98          48
      0x4200f5dc          80
      0x4200f8e0         160

实现细节
======================
具体原理基于 gcc 的插桩。在对应任务的 TCB（线程控制块）中，记录每个函数入口处的栈指针（sp）的最大值。如果是最大值，则记录回溯。

注意
======
使用 CONFIG_ARCH_INSTRUMENT_ALL 选项时要谨慎：
1. 它会对每个函数进行插桩，可能存在递归风险。
2. 它也会对入口函数进行插桩，例如 _start()。此时，bss 段和数据段尚未初始化，这可能导致错误。当前实现使用魔数来避免此问题，但在热启动时表现不佳。解决方案是使用 noinstrument_function 标志标记入口函数以防止插桩。
