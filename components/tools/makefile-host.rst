.. _makefile_host:

=================
.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``Makefile.host``
=================

这是 the make文件 that 用于 to make the mkconfig program from
the mkconfig.c C 文件, the cmpconfig program from cmpconfig.c C 文件,
the mkversion program from the mkconfig.c C 文件, or the mksyscall
program from the mksyscall.c 文件.

Usage:

.. code:: console

   $ cd tools/
   $ make -f Makefile.host <program>
