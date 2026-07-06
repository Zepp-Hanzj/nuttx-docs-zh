.. _makefile_host:

=================
``Makefile.host``
=================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是用于从 mkconfig.c C 文件构建 mkconfig 程序、
从 cmpconfig.c C 文件构建 cmpconfig 程序、
从 mkconfig.c C 文件构建 mkversion 程序、或
从 mksyscall.c 文件构建 mksyscall 程序的 Makefile。

Usage:

.. code:: console

   $ cd tools/
   $ make -f Makefile.host <program>
