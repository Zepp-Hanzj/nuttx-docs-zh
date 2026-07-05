====================================
栈溢出检查
====================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
--------

目前 NuttX 支持三种类型的栈溢出检测：
    1. 函数调用期间的栈溢出软件检查
    2. 上下文切换期间的栈溢出软件检查
    3. 栈溢出硬件检查
    4. 栈金丝雀检查

函数调用期间的软件栈检测包括两种实现思路：
    1. 通过栈内存着色实现
    2. 通过比较 sp 和 sl 寄存器实现

上下文切换期间的软件栈检测包括两种实现思路：
    1. 通过栈内存着色实现
    2. 通过检查栈底内存和 sp 寄存器实现

支持
-------

软件和硬件栈溢出检测实现目前仅在 ARM Cortex-M（32 位）系列芯片上实现。
栈金丝雀检查在所有平台上可用。

函数调用期间的栈溢出软件检查
--------------------------------------------------

1. 内存着色实现原理
    1. 使用栈之前，线程会将栈区域刷新为 0xdeadbeef
    2. 线程运行时会覆盖 0xdeadbeef
    3. up_check_tcbstack() 检测 0xdeadbeef 以获取栈峰值

    用法：
        启用 CONFIG_STACK_COLORATION

2. 比较 sp 和 sl
    编译程序时，保留 r10 并使用 r10 作为 stackbase::
    '''
    ARCHOPTIMIZATION += -finstrument-functions -ffixed-r10

    每个函数在进入和退出时会自动添加以下内容：
    __cyg_profile_func_enter
    __cyg_profile_func_exit

    用法：
        启用 CONFIG_ARMV8M_STACKCHECK 或 CONFIG_ARMV7M_STACKCHECK

上下文切换期间的栈溢出软件检查
------------------------------------------------------

1. 通过检测栈底指定的字节数来判断。
2. 检查 sp 寄存器是否越界。

用法：
    通过 STACKCHECK_MARGIN 设置检测长度

栈溢出硬件检查
-----------------------------

1. 上下文切换时设置 MSPLIM PSPLIM
2. 每次操作 sp 时，硬件自动比较 sp 和 PSPLIM。如果 sp 低于 PSPLIM，则崩溃

用法：
    启用 CONFIG_ARMV8M_STACKCHECK_HARDWARE

栈金丝雀检查
-----------------------------

1. 在栈中添加金丝雀值
2. 线程运行时，金丝雀值被覆盖
3. 线程运行时，金丝雀值与原始值比较
4. 如果值不同，则表示栈溢出

用法：
    启用 CONFIG_STACK_CANARIES
