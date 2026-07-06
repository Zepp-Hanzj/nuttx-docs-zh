=====
libxx
=====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此目录包含三个 C++ 库：

- 一个片段化的 C++ 库，仅允许构建最简单的 C++ 应用程序。
  在深度嵌入式领域，这可能就是全部所需。

  目前，这里仅支持以下功能：

  .. code-block:: C

     void *operator new(std::size_t nbytes)

  .. code-block:: C

     void operator delete(void* ptr)

  .. code-block:: C

     void operator delete[](void *ptr)

  .. code-block:: C

     void __cxa_pure_virtual(void)

  .. code-block:: C

     int __aeabi_atexit(void* object, void (*destroyer)(void*), void *dso_handle)

  .. code-block:: C

     int __cxa_atexit(__cxa_exitfunc_t func, FAR void *arg, FAR void *dso_handle)

  当以下两个选项均未启用时，将选择此实现。

- LLVM "libc++" C++ 库 (http://libcxx.llvm.org/)
  通过 CONFIG_LIBCXX=y 选择此实现。

- uClibc++ C++ 库 (http://cxx.uclibc.org/)
  通过 CONFIG_UCLIBCXX=y 选择此实现。

operator new
------------

此运算符应接受 ``size_t`` 类型。但 size_t 的底层类型未知。
在 NuttX 的 ``sys/types.h`` 头文件中，``size_t`` 被定义为 ``uint32_t``
（由特定架构的逻辑决定）。但 C++ 编译器可能认为 ``size_t`` 是不同的类型，
从而导致运算符中的编译错误。使用底层整数类型代替 size_t 似乎可以解决
编译问题。需要重新审视此问题。

在某些 C++ 编译器上，这会导致错误::

    Problem:     "'operator new' takes size_t ('...') as first parameter"
    Workaround:  Add -fpermissive to the compilation flags
