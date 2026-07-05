===========
``detab.c``
===========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Convert tabs to spaces in a 文件. Usage:

.. code:: console

   $ detab [-4] <source-file> <out-file>

Default ``<source-file>`` tab size is 8 spaces; ``-4`` selects 4 space tab size.
