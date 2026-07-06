===============
``gencromfs.c``
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是一个用于生成 CROMFS 文件系统镜像的 C 程序。
用法很简单：

.. code:: console

   $ gencromfs <dir-path> <out-file>

Where:

* ``<dir-path>`` 是将成为新 CROMFS 文件系统镜像根目录的目录路径。

* ``<out-file>`` 是生成的输出 C 文件名。此文件必须经过编译
  才能生成二进制 CROMFS 文件系统镜像。
