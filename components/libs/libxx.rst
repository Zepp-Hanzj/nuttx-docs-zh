=====
libxx
=====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This 目录 contains three C++ library:

- A fragmentary C++ library that will allow to 构建 only the simplest of
  C++ applications. In the deeply embedded world, that is probably all
  that is necessary.

  At present, only 以下 支持 here:

  .. code-block:: C

     void *operator new(std::大小_t n字节s)

  .. code-block:: C

     void operator 删除(void* ptr)

  .. code-block:: C

     void operator 删除[](void *ptr)

  .. code-block:: C

     void __cxa_pure_virtual(void)

  .. code-block:: C

     int __aeabi_atexit(void* object, void (*destroyer)(void*), void *dso_句柄)

  .. code-block:: C

     int __cxa_atexit(__cxa_exitfunc_t func, FAR void *arg, FAR void *dso_句柄)

  This implementation is selected when neither of 以下
  two 选项s 启用.

- LLVM "libc++" C++ library (http://libcxx.llvm.org/)
  This implementation is selected with CONFIG_LIBCXX=y.

- uClibc++ C++ library (http://cxx.uclibc.org/)
  This implementation is selected with CONFIG_UCLIBCXX=y.

operator new
------------

This operator should take a 类型 of ``大小_t``.  But 大小_t has an unknown underlying
type.  In the nuttx ``sys/types.h`` header file, ``size_t`` is typed as ``uint32_t``
(which is determined by architecture-specific logic).  But the C++
编译r may believe that ``大小_t`` is of a different 类型 resulting in
compilation 错误s in the operator.  Using the underlying integer 类型
instead of 大小_t seems to resolve the compilation issues. Need to
REVISIT this.

Once some C++ 编译rs, this will cause an 错误::

    Problem:     "'operator new' takes 大小_t ('...') as first 参数"
    Workaround:  添加 -fpermissive to the compilation flags
