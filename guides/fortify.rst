========
Fortify
========

概述
--------

C 程序中的一个常见错误是调用可能超出内存边界的函数，导致崩溃或未定义行为。例如不正确地使用 ``memcpy`` 和 ``memset`` 等函数。`FORTIFY_SOURCE` 是一种旨在帮助开发人员快速检测和缓解因不当使用库函数而导致的边界相关问题的机制。

支持
-------

`FORTIFY_SOURCE` 作为编译器的软件检查实现，支持所有架构。它通过在标准库函数调用中添加额外的验证检查来工作。

用法
-----

要启用 `FORTIFY_SOURCE`，使用以下选项配置内核：

``CONFIG_FORTIFY_SOURCE=level``

其中 `level` 可以设置为：

1. **编译时检查**：  
   通过分析源代码在编译期间检测问题。

2. **栈变量检查**：  
   在级别 1 的基础上，在运行时检查栈变量。

3. **堆内存检查**：  
   在级别 2 的基础上，为使用 ``malloc`` 分配的内存添加检查。  
   （需要 GCC 版本 12 或更高版本。）

FORTIFY_SOURCE 概述
=======================

`FORTIFY_SOURCE` 通过在编译时静态分析源代码来检测潜在的安全漏洞。它将标准库函数调用替换为包含额外边界检查的更安全版本。这些更安全的版本在执行某些操作之前验证操作的边界和输入的有效性。

GCC 内置函数
-----------------------

GCC 编译器内部为 `FORTIFY_SOURCE` 实现了两个关键函数：  

- ``__builtin_object_size``：确定静态分配对象的大小。  
- ``__builtin_dynamic_object_size``：确定动态分配对象的大小（例如通过 ``malloc``）。

从 GCC 12 开始，这些函数支持获取使用 ``malloc`` 分配的变量的大小。

通过将变量或缓冲区作为参数传递给这些函数，编译器可以计算相应的大小。使用此大小，可以检查运行时操作中潜在的越界行为。

示例：NuttX 中的 memcpy 实现
----------------------------------------

以下示例演示了如何在 NuttX 中使用 `FORTIFY_SOURCE` 来增强 ``memcpy`` 实现的安全性：

.. code-block:: c

   fortify_function(memcpy) 
   FAR void *memcpy(FAR void *dest,
                    FAR const void *src,
                    size_t n)
   {
     fortify_assert(n <= fortify_size(dest, 0) && n <= fortify_size(src, 0));
     return __real_memcpy(dest, src, n);
   }

在此实现中，``fortify_assert`` 宏确保源和目标缓冲区的大小足以处理请求的内存操作。如果断言失败，则表示存在潜在的缓冲区溢出，帮助开发人员快速识别和解决此类漏洞。
