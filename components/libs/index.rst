===============
NuttX 库
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本页讨论 ``libs/`` 目录下的 NuttX 库。

NuttX 中的库非常特殊，具有以下特性：

#. 在 FLAT 构建模式下，应用程序逻辑和 OS 内部逻辑可以共享同一份库。

#. 但在 PROTECTED 和 KERNEL 模式下，必须分别构建：应用程序和 OS 使用的
   不能是同一份库，而是需要为内核和应用程序分别构建独立版本。

#. 当 OS 使用这些库时，需要特别注意确保 OS 逻辑不会破坏用户的 errno 值，
   且不会创建不当的取消点。

   例如，``sem_wait()`` 既是一个取消点，也会修改 errno 值。因此在 FLAT
   构建中，以及在 PROTECTED 和 KERNEL 构建的内核版本中，必须使用特殊的
   内部 OS 接口 ``nxsem_wait()``。

注意：``libs/`` 下的库与其他 NuttX 组件的构建方式不同——``libs/`` 目录中
没有任何构建相关文件，它只是一个存放各个独立库目录的容器。上层 Makefile
逻辑会处理 ``libs/`` 容器内的各个库。

``libs/`` 目录的唯一作用是防止顶层目录因大量独立库而变得杂乱。

.. toctree::
   :maxdepth: 1
   :caption: 目录：

   libc/index.rst
   libdsp.rst
   libm.rst
   libxx.rst
   libnx/index.rst
