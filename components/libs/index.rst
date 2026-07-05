===============
NuttX 库
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本页讨论 the NuttX libraries that can be found in ``libs/``

Libraries in NuttX are very special creatures.  They have these properties:

#. They can be shared by both application logic and logic within the OS when
   using the FLAT 构建.

#. But in PROTECTED and KERNEL modes, they must be built differently:  The
   copies used by applications and the OS cannot be the same.  Rather,
   separate versions of libraries must be built for the kernel and for
   applications.

#. When used by the OS, some special care must be taken to assure that the
   OS logic does not disrupt the user's errno 值 and that the OS does
   not 创建 inappropriate cancellation points.

   例如, ``sem_wait()`` is both a cancellation point and modifies the
   errno 值.  So within the FLAT 构建 and without kernel version for
   the PROTECTED and KERNEL 构建s, the special internal OS 接口
   ``nxsem_wait()`` 必须使用.

注意：  The libraries under ``libs/`` 构建 differently from other NuttX
components:  There are no 构建-related 文件s in the ``libs/`` 目录; it
is simply a container for other well-known, individual library directories.
The upper level Make文件 logic is aware of the libraries within the ``libs/``
container.

The only real 函数 of the ``libs/`` 目录 is to prevent the top-level
目录 from becoming cluttered with individual libraries.

.. toctree::
   :maxdepth: 1
   :caption: Contents:
   
   libc/index.rst
   libdsp.rst
   libm.rst
   libxx.rst
   libnx/index.rst
