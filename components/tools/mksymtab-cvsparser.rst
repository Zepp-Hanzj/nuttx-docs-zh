================================================
``mksymtab.c``, ``cvsparser.c``, ``cvsparser.h``
================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是一个 C 文件，用于从逗号分隔值（CSV）文件构建符号表。
此工具不在 NuttX 构建期间使用，但可根据需要用于生成文件。

Usage:

.. code:: console

   $ ./mksymtab [-d] <cvs-file> <symtab-file> [<symtab-name> [<nsymbols-name>]]

Where::

    <cvs-file>      : 输入 CSV 文件的路径（必需）
    <symtab-file>   : 输出符号表文件的路径（必需）
    <symtab-name>   : 符号表变量的可选名称
                      默认: "g_symtab"
    <nsymbols-name> : 符号表变量的可选名称
                      默认: "g_nsymbols"
    -d              : 启用调试输出

Example:

.. code:: console

   $ cd nuttx/tools
   $ cat ../syscall/syscall.csv ../lib/libc.csv | sort >tmp.csv
   $ ./mksymtab.exe tmp.csv tmp.c
