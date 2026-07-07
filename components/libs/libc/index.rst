====
libc
====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本目录包含大量通常与标准 C 库相关的小型函数。该目录下的子目录包含了
可供用户模式程序调用的标准接口。

通常情况下，NuttX 构建时不启用保护机制，所有线程均以内核模式运行。
在这种模式下，内核模式程序和用户模式程序之间没有真正的架构区分；
整个系统更像是一个全部以内核模式运行的多线程程序。

但如果选择了 ``CONFIG_BUILD_PROTECTED`` 选项，NuttX 将被构建为独立的
用户模式和内核模式部分。在这种情况下，``nuttx/`` 目录中的大部分代码
将在内核模式下运行，但有两个例外：(1) syscall/proxies 中的用户模式
"代理"，以及(2) 本目录中的标准 C 库函数。在此构建模式下，以这种
方式隔离用户模式 OS 接口至关重要。

如果选择了 ``CONFIG_BUILD_KERNEL``，则仅构建 NuttX 内核，不会包含
应用程序。

子目录
===============

``libs/libc/`` 目录中的文件（大部分）按照 ``include/`` 目录中提供函数
原型的头文件进行组织，如下所示::

  audio     - 音频系统的一部分：nuttx/audio/audio.h
  builtin   - 内置应用程序支持，由 nuttx/binfmt 和 NSH 使用。
  dlfcn     - dlfcn.h
  endian    - endian.h
  errno     - errno.h
  hex2bin   - hex2bin.h
  libgen    - libgen.h
  locale    - locale.h
  lzf       - lzf.h
  fixedmath - fixedmath.h
  grp       - grp.h
  inttypes  - inttypes.h
  machine   - 各种特定于架构的实现。
  math      - math.h
  elf    - 模块和共享库逻辑的一部分：nuttx/lib/elf.h
  net       - 各种网络相关的头文件：netinet/ether.h、arpa/inet.h
  pthread   - pthread.h
  pwd       - pwd.h
  queue     - queue.h
  sched     - sched.h
  search    - search.h
  semaphore - semaphore.h
  stdbit    - stdbit.h（可选 C23）
  stdio     - stdio.h
  stdlib    - stdlib.h
  string    - string.h（以及旧版 strings.h 和非标准的 nuttx/b2c.h）
  time      - time.h
  uio       - sys/uio.h
  unistd    - unistd.h
  wchar     - wchar.h
  wctype    - wctype.h

其中大部分是"标准"头文件，但也有非标准的：``hex2bin.h`` 和
``fixedmath.h`` 就是非标准的。

此外还有一个 ``misc/`` 子目录，其中包含各种内部函数和头文件中
数量不足以单独建立子目录的接口::

  misc      - 非标准的"胶水"逻辑，nuttx/debug.h、crc32.h、dirent.h

库数据库
================

NuttX C 库中可用函数的信息维护在一个数据库中。该"数据库"以简单的
逗号分隔值文件 libc.csv 实现。大多数电子表格程序都支持此格式，
可用于维护该库数据库。

该库数据库（最终）将用于生成符号库符号表信息，以便导出到外部应用程序。

CSV 文件每行的格式如下::

  字段 1：函数名称
  字段 2：包含该函数原型的头文件
  字段 3：编译条件
  字段 4：函数返回值的类型
  字段 5 - N+5：函数各形式参数的类型

每个类型字段的格式如下::

  类型名称：
        适用于所有简单类型
  形式类型 | 实际类型：
        适用于数组类型，其中形式参数的形式（例如 int param[2]）
        与实际传递参数的类型（例如 int*）不同。这是必要的，
        因为无法对数组类型进行简单的类型转换。
  形式类型 | 联合体成员实际类型 | 联合体成员字段名：
        联合体也存在类似的情况。例如，形式参数类型 union sigval
        ——无法将 uintptr_t 转换为 union sigval，但可以在传递
        实际参数时转换为联合体成员类型之一。同样，我们也无法
        将 union sigval 转换为 uintptr_t，而是需要将特定的联合体
        成员字段名转换为 uintptr_t。

注意：可以使用工具 mksymtab 从该 CSV 文件生成符号表。
详见 ``Documentation/components/tools`` 了解 mksymtab 的使用方法。

symtab
======

符号表与构建模式
-----------------

本目录提供符号表支持，该符号表为应用程序和 NSH 提供全部/大部分
系统和 C 库服务/函数。

符号表在不同的 NuttX 构建模式下有不同的用途：

#. 在 FLAT 构建（``CONFIG_BUILD_FLAT``）中，符号表用于将已加载的
   ELF 或 NxFLAT 模块中的地址绑定到通常驻留在 FLASH 存储器中的
   基础代码。OS 接口和用户/应用程序库均通过符号表提供给已加载的
   模块。

#. 在保护构建（``CONFIG_BUILD_PROTECTED``）中，符号表可能具有价值，
   因为新启动的用户任务需要与其他用户代码共享资源（但应使用
   系统调用与 OS 交互）。

#. 但在内核构建模式（``CONFIG_MODULES``）中，只能使用通过
   ``execl()``、``execv()`` 或 ``posix_spawan()`` 加载的完全链接的
   可执行文件。由于所有内存资源都是隔离的，符号表在内核构建中
   没有用处；新启动的进程无法共享任何资源。

代码/文本大小影响
---------------------------

该选项可能对系统镜像大小产生重大影响，主要是代码/文本部分。
这是因为生成上述 symtab.inc 的指令会导致 NuttX RTOS 和 C 库中
的每个接口都被包含在构建中，再加上庞大的符号表本身所占的空间。

为了减小代码/文本大小，您可能需要手动裁剪自动生成的 symtab.inc 文件，
移除不希望包含在基础 FLASH 镜像中的接口。

实现细节
======================

.. toctree::
   :maxdepth: 1
   :caption: Contents:
   
   search
   stdbit
   stream
   zoneinfo
