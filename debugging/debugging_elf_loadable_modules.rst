==============================
调试 ELF 可加载模块
==============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

.. warning:: 
    迁移自： 
    https://cwiki.apache.org/confluence/display/NUTTX/Debugging+ELF+Loadable+Modules

调试加载到内存中的 ELF 模块可能很棘手，因为内存中的加载地址与 ELF 文件中的地址不匹配。这个挑战在调试 uClinux 程序和 Linux 内核模块时长期存在；相同的解决方案可用于 NuttX ELF 文件（也可能用于 NxFLAT 模块）。以下是解决此问题的一种方法的概述：

1. 获取 ELF 模块加载地址
==============================

在 ``nuttx/binfmt`` 中添加更改，以便打印 ELF 代码段加载到内存中的地址。

开启 BINFMT 调试（``CONFIG_DEBUG_BINFMT=y``）应该能给你相同的信息，尽管它可能提供比你实际需要更多的输出。

或者，你可以在 ``main()`` 函数开头放置一个 ``printf()``，这样你的 ELF 模块就可以打印自己的加载地址。例如，目标文件中 ``main()`` 的地址与运行时 ``main()`` 的地址之间的差值揭示了实际的加载地址。

2. 让 ELF 模块等待
===================================

在 ELF 程序的 ``main()`` 例程中插入一个无限循环。例如：

.. code-block:: c

    volatile bool waitforme;
    int main (int arc, char **argv)
    {
        while (!waitforme);
        ...

当你启动 ELF 程序时，你会看到它在内存中的加载位置，ELF 程序将一直停留在无限循环中。它将继续等待 ``waitforme`` 变为 true 才继续执行。

3. 启动调试器
=====================

启动调试器，连接到 GDB 服务器，并暂停程序。如果你的调试器行为正常，它应该停在 ``main()`` 中的无限循环处。

4. 加载偏移符号
======================

使用 ELF 模块加载的偏移量加载符号：

.. code-block:: shell

   (gdb) add-symbol-file <myprogram> <load-address>

这里，``<myprogram>`` 是包含符号的 ELF 文件，``<load-address>`` 是程序代码段实际加载的地址（如上确定）。单步执行几次，确认你在无限循环中。

5. 开始调试
============

将 ``waitforme`` 设置为非零值。执行应该退出无限循环，现在你可以用通常的方式调试加载到 RAM 中的 ELF 程序。

更简单的方法？
==============

可能有一种替代方法，允许你进入 ELF 模块而无需修改代码以包含 ``waitforme`` 循环。你可以在 OS 函数 ``task_start()`` 上设置断点。该函数在你的 ELF 程序启动之前运行，因此你应该能够从 OS 代码单步进入你加载的 ELF 应用程序——无需对 ELF 应用程序进行任何更改。

当你进入应用程序的 ``main()`` 时，你就有了 ``main()`` 的重定位地址，可以使用该地址（参见步骤 #1）计算加载偏移量。
