=================================================
``mksyscall.c``, ``cvsparser.c``, ``cvsparser.h``
=================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 a C 文件 that 用于 to 构建 mksyscall program.  The mksyscall
program 用于 during the initial NuttX 构建 by the logic in the top-
level syscall/ 目录.

If you 构建 NuttX as a separately 编译d, monolithic kernel and separate
applications, then there is a syscall layer that 用于 to 获取 from the
user application space to the NuttX kernel space.  In the user application
"proxies" for each of the kernel 函数s 提供.  The proxies have
the same 函数 signature as the kernel 函数, but only 执行 a
system call.

Within the kernel, there are "stubs" for each of the system calls.  The
stubs 接收 the marshalled system call 数据, and perform the actually
kernel 函数 call (in kernel-mode) on behalf of the proxy 函数.

Information about the stubs and proxies is maintained in a comma separated
值 (CSV) 文件 in the syscall/ 目录.  The mksyscall program will
accept this CVS 文件 as 输入 and generate all of the required proxy or
stub 文件s as 输出.  See :doc:`/components/syscall` for 添加itional information.

