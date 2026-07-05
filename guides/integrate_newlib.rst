=======================
与 Newlib 集成
=======================

.. warning:: 
    迁移自: 
    https://cwiki.apache.org/confluence/display/NUTTX/Integrating+with+Newlib

内置 C 库
==================

NuttX 有自己的小型内置 C 库。与该 C 库一起的是所有具有该内置 C 库特定定义的头文件。这些头文件中的定义与您在任何其他 C 库附带的头文件中找到的定义不兼容，尝试将它们与其他 C 库的头文件混合使用肯定会给您带来问题。

当 GCC 被构建时，它是针对 C 库构建的。NuttX `buildroot` 工具当然是针对内置 NuttX C 库构建的，似乎是使用工具的明显选择。但使用其他工具链有很多原因。例如，NuttX `buildroot` 工具在 C++ 支持方面有一些限制。另一个例子是，您可能想要使用其他 C 库实现中包含的更高性能的数学库。

有许多可用的 C 库：`glibc` 和 `uClibc` 通常与 Linux 工具一起使用。应避免使用这些。大多数嵌入式工具链是针对 `newlib` 构建的。因此，如果您不使用 NuttX buildroot 工具链，您很可能使用的是内置了 `newlib` 的工具链。因此，如果您在 NuttX 代码中包含 `newlib` 头文件，可能会出现问题。

头文件问题
==================

math.h
------

NuttX 包含一个内置数学库，可通过 ``CONFIG_LIBM=y`` 选择。然而，有理由使用外部数学库：NuttX 数学库是用 C 编写的，性能不如为您的处理器架构调优的自定义数学库。NuttX 数学库还有一些其他问题，如顶层 TODO 列表中所述。

许多人选择使用 `newlib` 数学库。如果您在未选择 ``CONFIG_LIBM=y`` 的情况下包含 ``math.h``，您可能会得到 `newlib` 数学库，并且肯定会看到涉及类型 ``wint_t`` 定义的编译错误。

NuttX 论坛中描述了许多变通方法。以下是一些：

* 将 newlib ``math.h`` 复制到 ``nuttx/include/math.h`` 并删除对 ``wint_t`` 的引用。

* 将以下内容添加到 ``nuttx/libc/stdio/lib_libvsprintf.c``。我特别不喜欢这个解决方案，因为它涉及对无法上游接受的 NuttX 头文件的修改。

.. code-block:: c

    /* Include floating point functions */
 
    #ifdef CONFIG_LIBC_FLOATINGPOINT
    #  include "wchar.h"
    #  include "stdio/lib_libdtoa.c"
    #endif

* 提供您自己的 ``math.h`` 版本（仅限 GCC），包含以下内容。并将此 ``math.h`` 的路径添加到您的 ``CFLAGS`` 包含路径参数中。路径可以通过在 CFLAGS 中添加 ``-system`` 或 ``-I`` 来指定。此 ``math.h`` 的路径必须最后定义，以便它具有优先权。这将包含 NuttX ``wint_t`` 定义，然后继续包含默认版本的 ``math.h``。

.. code-block:: c

    #ifndef _MYMATH_H
    #define _MYMATH_H
    
    #include "wchar.h"
    #include_next <math.h>
    
    #endif /* _MYMATH_H */

* PX4 团队使用这些补丁来解决 `cwhar <https://github.com/PX4/Firmware/blob/nuttx_v3/nuttx-patches/c%2B%2B11.patch>`_ 和 `math.h <https://github.com/PX4/Firmware/blob/nuttx_v3/nuttx-patches/math.h.patch>`_ 的问题。但请注意该代码中的注释：

.. code-block:: c 

    /* N.B. The following definitions are enabled at this time to allow the PX4
   * development to continue until there is a SAFE  solution to foreign
   * (non-nuttx) header file inclusion. There is a potential of a binary
   * incompatibility and runtime errors, memory overwrites or corruption
   * VVVVVVVVVVVVVVVVVVVVVVVVVV Begin Warning VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
   */

* 有人建议将 ``wint_t`` 的类型定义添加到 ``nuttx/include/sys/types.h``，仅仅因为该头文件将被包含到 newlib ``math.h`` 中。当然，这种包含也非常 `危险`，因为 NuttX ``sys/types.h`` 头文件中的类型可能与预编译的 newlib 数学库中的类型不一致。无论如何，不建议使用此解决方案。类型 ``wint_t`` 已在 ``nuttx/include/sys/wchar.h`` 中正确定义，根据 `OpenGroup.org <http://pubs.opengroup.org/onlinepubs/007908775/xsh/wchar.h.html>`_，这是唯一正确的位置。对我来说，为什么 newlib ``math.h`` 头文件使用 ``wint_t`` 而不包含 ``wchar.h`` 是个谜。如果它包含了，那么这个编译问题就不会存在（仍然可能存在微妙的二进制兼容性问题）。

* 理想的解决方案是将第三方优化的 ARM 数学库集成到 NuttX 中，仅使用 NuttX 头文件构建。这将保证没有二进制不兼容性，并将是对 NuttX 非常有用的贡献。

可能还需要更改 ``nuttx/arch/<architecture>/src/Makefile``，以便链接器可以找到并包含数学库（类似于 ``Makefile`` 中查找 ``libgcc.a`` 的现有逻辑）。

更新：此问题可能最终已通过此提交解决：

.. code-block::

    commit 894ca622e6a408e5fa858a3fee46fb16f32cf86c
    Author: Xiang Xiao \<xiaoxiang@xiaomi.com\>
    Date:   Mon Aug 27 06:26:37 2018 -0600
    
    include/sys/types:  Move wint_t and wctype_t from wchar.h to
    types.h.  This change is compatible as before since wchar.h
    include types.h indirectly.  This fixes a compilation error with
    newlib's math.h:  'unknown type name wint_t'

cmath
-----

已报告此错误：

.. code-block:: bash

    /nuttx/include/cxx/cmath:124:11: error: '::log2l' has not been declared...

显然，函数逻辑 ``log2l()`` 在 NuttX ``math.h`` 中定义，并在 ``cmath`` 中添加到 ``std::`` 命名空间。但是，显然 newlib ``math.h`` 没有 ``lib2l()`` 的原型。

如果您计划使用 newlib ``math.h`` 和 NuttX ``cmath``，那么您可能还需要修改 ``cmath``。

alloca.h
--------

如果您导入的应用程序包含 ``alloca.h``，那么您将遇到同样类型的问题。NuttX 不提供此头文件，因此您可能最终会包含 newlib 版本的 ``alloca.h``，这会产生类似的灾难性结果。

对于 GCC（仅限）的一种解决方案是提供您自己的 ``alloca.h``，包含：

.. code-block:: C

    #ifndef _ALLOCA_H
    #define _ALLOCA_H
    
    #define alloca __builtin_alloca
    
    #endif /* _ALLOCA_H */

并将此 ``alloca.h`` 的路径添加到您的 ``CFLAG`` 包含路径参数中。路径可以通过在 CFLAGS 中添加 ``-system`` 或 ``-I`` 来指定。此 ``alloca.h`` 的路径必须最后定义，以便它具有优先权。

但是，如果您包含的 newlib 头文件又包含其他 ``alloc.h``，您可能仍然会包含 newlib ``alloca.h``。因此另一种解决方案可能是包含您自己的 ``math.h``，例如包含类似以下内容：

.. code-block:: C

    #ifndef _MYMATH_H
    #define _MYMATH_H
    #ifndef _ALLOCA_H
    #define _ALLOCA_H

    #define alloca __builtin_alloca

    #endif /* _ALLOCA_H */

    #include_next <math.h>

    #endif /* _MYMATH_H */

这将提供 ``alloca()`` 定义，然后继续包含默认版本的 ``math.h``。这之所以有效，是因为幂等预处理器变量 ``_ALLOC_H`` 与 newlib ``alloca.h`` 中使用的相同幂等变量匹配。因此，任何偷偷包含的 ``alloca.h`` 都不会起作用。

C++ 问题
==========

大多数 C++ 问题与头文件无关，而是与 C++ 名称修饰和严格类型有关。

new 运算符
------------

C++ new 运算符的原型是：

.. code-block:: C

    void *operator new(size_t nbytes)

然而，``size_t`` 在工具链中被定义为 ``unsigned long`` 或 ``unsigned int``。这在不同版本的 GCC 工具链中有所不同，与头文件包含无关。NuttX 支持一个配置选项来解决此问题，将 new 更改为：

.. code-block:: C

    #ifdef CONFIG_CXX_NEWLONG
    void *operator new(unsigned long nbytes)
    #else
    void *operator new(unsigned int nbytes)
    #endif

这个 C++ 名称修饰问题已经存在多年，并且因 GCC 编译器而异，显然是由于某些 `newlib` 配置差异。

uint32_t
--------

类似地，您可能会发现 NuttX 中 ``uint32_t`` 的定义可能与您的工具链库不兼容。您可能会看到类似以下错误：

.. code-block:: bash

    error: redeclaration of 'typedef long unsigned int std::uint_least32_t'

ARM 头文件 ``nuttx/arch/arm/include/types.h`` 中的定义是：

.. code-block:: C

    typedef signed int _int32_t;
    typedef unsigned int _uint32_t;

在 ARM 平台上，``unsigned long`` 和 ``unsigned int`` 都是 32 位整数，因此使用哪个定义并不重要。但如果您关心编译器使用 size_t 的 C++ 名称修饰，这就有关系了。如果您看到上述错误，那么您可以替换这些类型定义以避免 C++ 名称修饰不兼容，例如：

.. code-block:: C

    typedef signed long _int32_t;
    typedef unsigned long _uint32_t;

但这现在可能会导致额外的问题，NuttX 中使用的 ``size_t`` 定义与库中使用的 ``size_t`` 定义之间可能存在不兼容性。

size_t
------

``size_t`` 应该是足够宽的整数类型，可以容纳最大内存对象的大小。因此 ``size_t`` 实际上取决于底层指针类型的大小。例如，对于具有 16 位寻址的 CPU，``size_t`` 的宽度应为 16 位；对于具有 32 位寻址的 CPU，宽度应为 32 位。

``uint32_t`` 当然应该始终是 32 位宽。

使用 newlib 头文件时，您还会遇到某些类型定义之间的不兼容性，``uint32_t`` 和 ``size_t`` 类型通常是问题的根源。例如：

.. code-block:: bash

    error: redeclaration of 'typedef unsigned int std::size_t'

此问题的根本原因是社区无法就 ``size_t`` 的正确定义达成一致。NuttX 使用此 `灵活的` ``size_t`` 定义：

.. code-block:: c

    typedef uint32_t size_t;

它在 ``uint32_t`` 由架构特定头文件决定（而非 RTOS 本身）的意义上是 `灵活的`。该定义将是 ``unsigned long`` 或 ``unsigned int``。因此 ``size_t`` 类型兼容性可能因不同的编译器和不同的架构而异（注意，由于 ``size_t`` 应该足够宽以容纳最大可寻址对象的大小，``uint32_t`` 仅适用于 32 位可寻址机器。也许 ``size_t`` 真的应该定义为 ``uintptr_t`` 类型？）。

这可以通过如上所述更改 ``uint32_t`` 的定义来修复。但这可能会引入 ``uint32_t`` 名称修饰不兼容性。在这种情况下，您别无选择，只能通过更改 ``nuttx/include/sys/types.h`` 中的定义来将 ``size_t`` 的定义与 ``uint32_t`` 解耦：

.. code-block:: c

    typedef unsigned int size_t;

或

.. code-block:: c

    typedef unsigned long size_t;

以解决不兼容性。
