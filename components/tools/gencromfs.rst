===============
``gencromfs.c``
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 a C program that 用于 to generate CROMFS 文件 system 图像s.
Usage is simple:

.. code:: console

   $ gencromfs <dir-path> <out-file>

Where:

* ``<dir-path>`` is the path to the directory will be at the root of the new
  CROMFS 文件 system 图像.

* ``<out-file>`` the name of the generated, output C file. This file must be
  编译d in order to generate the binary CROMFS 文件 system 图像.
