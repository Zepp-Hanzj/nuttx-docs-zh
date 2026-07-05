=================
构建 uClibc++
=================

.. warning:: 
    迁移自: 
    https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=139629550 
    可能已过时

`uClibc++ <http://cxx.uclibc.org/>`_ 的一个版本已被移植到 NuttX，并在 NuttX uClibc++ GIT 仓库 `Bitbucket.org <https://bitbucket.org/nuttx/uclibc/>`_ 中提供。此版本的 uClibc++ 由 RGMP 团队为 NuttX 适配。

此自定义版本的 uClibc++ 位于 NuttX 仓库中：

  https://bitbucket.org/nuttx/uclibc/

而非 NuttX 主源码树中，原因是许可问题：NuttX 使用宽松的修改版 BSD 许可证；而 uClibc++ 使用更严格的 GNU LGPL 版本 3 许可证。

通用构建说明在 uClibc++ `README.txt <https://bitbucket.org/nuttx/uclibc/src/master/README.txt>`_ 文件中提供。此处不重复这些说明。本文档记录了构建此 NuttX 版本 uClibc++ 时遇到的特定问题及其解决方法。

``_impure_ptr`` 的未定义引用
======================================

**问题**

构建 uClibc++ 时，您可能会遇到类似以下的 ``_impure_ptr`` 未定义引用：

.. code-block:: none

   LD: nuttx
   .../arm-none-eabi/lib/armv7e-m\libsupc++.a(vterminate.o): In function
   `__gnu_cxx::__verbose_terminate_handler()':
   vterminate.cc:(.text._ZN9__gnu_cxx27__verbose_terminate_handlerEv+0xfc):
   undefined reference to `_impure_ptr'

**解决方案**

目前尚无明确的、优雅的解决方案，但以下变通方法已被证明有效：

1. 找到可以找到 ``libsupc++`` 的目录：

   .. code-block:: console

      arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -print-file-name=libsupc++.a

2. 转到该目录并保存 ``vterminate.o`` 的副本（以备后用）：

   .. code-block:: console

      cd <the-directory-containing-libsupc++.a>
      arm-none-eabi-ar.exe -x libsupc++.a vterminate.o

3. 从库中删除 ``vterminate.o``。在构建时，uClibc++ 包将提供一个可用的替代品：

   .. code-block:: console

      arm-none-eabi-ar.exe -d libsupc++.a vterminate.o

4. 此时，NuttX 应该可以正常链接。如果您想将原始的 ``vterminate.o`` 恢复到 ``libsupc++.a``，可以通过运行以下命令来实现：

   .. code-block:: console

      arm-none-eabi-ar.exe rcs libsupc++.a vterminate.o

从标准库中删除 ``vterminate.o`` 后，uClibc++ 提供的 ``vterminate.o`` 成为活动实现，防止在链接过程中出现对 ``_impure_ptr`` 的引用。

.. note::
   修改工具链库时请务必谨慎。此变通方法已知有效，但它替换了标准库对象，在其他工具链使用场景中可能会有副作用。
