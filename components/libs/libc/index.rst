====
libc
====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This 目录 contains numerous, small 函数s typically associated with
what you would expect to find in a standard C library.  The sub-directories
in this 目录 contain standard 接口 that can be 执行d by user-
mode programs.

Normally, NuttX is built with no protection and all th读取s 运行ning in kernel-
mode.  In that mode, there is no real architectural distinction between
what is a kernel-mode program and what is a user-mode program; the system is
more like an multi-th读取ed program that all 运行s in kernel-mode.

But if the ``CONFIG_BUILD_PROTECTED`` 选项 is selected, NuttX will be built
into distinct user-mode and kernel-mode sections.  In that case, most of the
code in the ``nuttx/`` 目录 will 运行 in kernel-mode with exceptions
of (1) the user-mode "proxies" found in syscall/proxies, and (2) the
standard C library 函数s found in this 目录.  In this 构建 mode,
it is critical to separate the user-mode OS 接口s in this way.

If ``CONFIG_BUILD_KERNEL`` is selected, then only a NuttX kernel will be built
with no applications.

子目录
===============

The 文件s in the ``libs/libc/`` 目录 are organized (mostly) according
which 文件 in the ``include/`` 目录 provides the proto类型 for library
函数s.  So we have::

  audio     - This part of the audio system: nuttx/audio/audio.h
  builtin   - 支持 for builtin applications.  Used by nuttx/binfmt and NSH.
  dlfcn     - dlfcn.h
  endian    - endian.h
  errno     - errno.h
  hex2bin   - hex2bin.h
  libgen    - libgen.h
  locale    - locale.h
  lzf       - lzf.h
  fixedmath - fixedmath.h
  grp       - grp.h
  int类型s  - int类型s.h
  machine   - Various architecture-specific implementations.
  math      - math.h
  elf    - Part of module and shared library logic: nuttx/lib/elf.h
  net       - Various network-related header 文件s: netinet/ether.h, arpa/inet.h
  pth读取   - pth读取.h
  pwd       - pwd.h
  queue     - queue.h
  sched     - sched.h
  search    - search.h
  semaphore - semaphore.h
  std位    - std位.h (选项al C23)
  stdio     - stdio.h
  stdlib    - stdlib.h
  string    - string.h (and legacy strings.h and non-standard nuttx/b2c.h)
  time      - time.h
  uio       - sys/uio.h
  unistd    - unistd.h
  wchar     - wchar.h
  wc类型    - wc类型.h

Most of these are "standard" header 文件s; some are not: ``hex2bin.h`` and
``fixemath.h`` are non-standard.

There is also a ``misc/`` sub目录 that contains various internal 函数s
and 接口s from header 文件s that are too few to warrant their own sub-
目录::

  misc      - Nonstandard "glue" logic, nuttx/debug.h, crc32.h, dirent.h

Library Database
================

Information about 函数s available in the NuttX C library information is
maintained in a 数据base.  That "数据base" is implemented as a simple comma-
separated-值 文件, libc.csv.  Most sp读取sheets programs will accept this
format and 可用于 to maintain the library 数据base.

This library 数据base will (eventually) be used to generate symbol library
symbol table information that can be exported to external applications.

The format of the CSV 文件 for each line is::

  Field 1: 函数 名称
  Field 2: The header 文件 that contains the 函数 proto类型
  Field 3: Condition for compilation
  Field 4: The 类型 of 函数 返回 值.
  Field 5 - N+5: The 类型 of each of the N formal 参数s of the 函数

Each 类型 field has a format as follows::

  类型 名称:
        For all simpler 类型s
  formal 类型 | actual 类型:
        For array 类型s where the form of the formal (eg. int param[2])
        differs from the 类型 of actual passed 参数 (eg. int*).  This
        is necessary because you cannot do simple casts to array 类型s.
  formal 类型 | union member actual 类型 | union member field名称:
        A similar situation exists for unions.  例如, the formal
        参数 类型 union sigval -- You cannot cast a uintptr_t to
        a union sigval, but you can cast to the 类型 of one of the union
        member 类型s when passing the actual 参数.  Similarly, we
        cannot cast a union sigval to a uinptr_t either.  Rather, we need
        to cast a specific union member field名称 to uintptr_t.

注意： The tool mksymtab 可用于 to generate a symbol table from this CSV
文件.  See ``Documentation/components/tools`` for further details about the use of mksymtab.

symtab
======

Symbol Tables and Build Modes
-----------------------------

This 目录 provide 支持 for a symbol table which provides all/most of
system and C library services/函数s to the application and NSH.

Symbol tables have differing usefulness in different NuttX 构建 modes:

#. In the FLAT 构建 (``CONFIG_BUILD_FLAT``), symbol tables 用于 to bind
   地址es in loaded ELF or NxFLAT modules to base code that usually
   resides in FLASH 内存.  Both OS 接口s and user/application
   libraries are made available to the loaded module via symbol tables.

#. Symbol tables may be of 值 in a protected 构建
   (``CONFIG_BUILD_PROTECTED``) where the newly 启动ed user task must
   share resources with other user code (but should use system calls to
   interact with the OS).

#. But in the kernel 构建 mode (``CONFIG_MODULES``), only fully 链接ed
   executables loadable via ``execl()``, ``execv()``, or ``posix_spawan()``
   可用于.
   There is no use for a symbol table with the kernel 构建 since all
   内存 resources are separate; nothing is share-able with the newly
   启动ed process.

Code/Text Size Implications
---------------------------

The 选项 can have substantial effect on system 图像 大小, mainly
code/文本.  That is because the instructions to generate symtab.inc
above will cause EVERY 接口 in the NuttX RTOS and the C library to be
included into 构建.  添加 to that the 大小 of a huge symbol table.

In order to reduce the code/文本 大小, you may want to manually p运行e the
auto-generated symtab.inc 文件 to 移除 all 接口s that you do
not wish to include into the base FLASH 图像.

Implementation Details
======================

.. toctree::
   :maxdepth: 1
   :caption: Contents:
   
   search.rst
   std位.rst
   stream.rst
   zoneinfo.rst
