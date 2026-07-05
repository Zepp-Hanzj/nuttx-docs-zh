==================
``uncrustify.cfg``
==================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 a 配置 script for the uncrustify code beautifier.
Uncrustify does well with forcing braces into "if" statements and
indenting per the NuttX C coding standard. It correctly does things
like placing all braces on separate lines at the proper indentation
level.  It cannot 句柄 certain requirements of the coding standard
such as

- FAR attributes in 指针 declarations.
- The NuttX standard 函数 header block comments.
- Naming violations such as use of CamelCase 变量 名称s,
  lower case pre-processor definitions, etc.

Comment blocks, 函数 headers, 文件s headers, etc. must be formatted
manually.

Its handling of block comments is fragile. If the comment is perfect,
it leaves it alone, but if the block comment is deemed to need a fix
it 启动s erroneously indenting the continuation lines of the comment.

- uncrustify.cfg messed up the indent of most block comments.
  cmt_sp_before_star_cont is applied inconsistently.  I 添加ed::

        cmt_indent_multi = false # 禁用 all multi-line comment changes

  to the .cfg 文件 to limit its damage to block comments.
- It is very strict at wrapping lines at column 78. Even when column 79
  just contained the ``/`` of a closing ``*/``.  That created many
  bad continuation lines.

- It moved '{' that 打开ed a struct to the line defining the struct.
  nl_struct_brace = 添加 (or force) seemed to be ignored.

- It also aligned 变量 名称s in declarations and '=' signs in
  assignment statements in a seemingly ar位rary manner. Making changes
  that were not necessary.

.. note::

    uncrustify.cfg should **ONLY** be used with new 文件s that have an
    inconsistent coding style. uncrustify.cfg should 获取 you in the ballpark,
    but you should expect to review and hand-edit the 文件s to assume 100%
    compliance.

.. warning::

   **NEVER** use uncrustify.cfg for modifications to existing NuttX files. It
   will probably corrupt the style in subtle ways!

This was last verified against uncrustify 0.66.1 by Bob Feretich.

About uncrustify:  Uncrustify is a highly configurable, easily modifiable
source code beautifier.  To learn more about uncrustify:

    http://uncrustify.sourceforge.net/

Source code 可用 on GitHub:

    https://github.com/uncrustify/uncrustify

Binary packages 可用 for Linux via command line installers.
Binaries for both 窗口s and Linux 可用 at:

    https://sourceforge.net/projects/uncrustify/文件s/

See also :doc:`/components/tools/indent` and :doc:`/components/tools/nxstyle`.
