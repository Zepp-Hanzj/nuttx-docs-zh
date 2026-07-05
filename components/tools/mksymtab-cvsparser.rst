================================================
``mksymtab.c``, ``cvsparser.c``, ``cvsparser.h``
================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 a C 文件 that 用于 to 构建 symbol tables from comma separated
值 (CSV) 文件s.  This tool is not used during the NuttX 构建, but
可用于 as needed to generate 文件s.

Usage:

.. code:: console

   $ ./mksymtab [-d] <cvs-file> <symtab-file> [<symtab-name> [<nsymbols-name>]]

Where::

    <cvs-文件>      : The 路径 to the 输入 CSV 文件 (required)
    <symtab-文件>   : The 路径 to the 输出 symbol table 文件 (required)
    <symtab-名称>   : 选项al 名称 for the symbol table 变量
                      默认: "g_symtab"
    <nsymbols-名称> : 选项al 名称 for the symbol table 变量
                      默认: "g_nsymbols"
    -d              : 启用 debug 输出

Example:

.. code:: console

   $ cd nuttx/tools
   $ cat ../syscall/syscall.csv ../lib/libc.csv | sort >tmp.csv
   $ ./mksymtab.exe tmp.csv tmp.c
