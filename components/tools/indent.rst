=============
``indent.sh``
=============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This script 可用于 to indent .c and .h 文件s in a manner similar
to the NuttX coding style.  It doesn't do a really good job, however
(see below and the comments at the top of the indent.sh 文件).

USAGE::

    tools/indent.sh [-d] [-p] -o <out-文件> <in-文件>
    tools/indent.sh [-d] [-p] <in-文件-list>
    tools/indent.sh [-d] -h

Where::

    -<in-文件>
      A single, unformatted 输入 文件
    -<in-文件-list>
      A list of unformatted 输入 文件s that will be reformatted in place.
    -o <out-文件>
      写入 the single, reformatted <in-文件> to <out-文件>.  <in-文件>
      will not be modified.
    -d
      启用 script debug
    -p
      Comments are pre-formatted.  Do not reformat.
    -h
      Show this help message and exit

The conversions make by the indent.sh script differs from the NuttX coding
style in that:

1. The coding standard requires that the trailing ``*/`` of a multi-line
   comment be on a separate line.  By 默认, indent.sh will put the
   final ``*/`` on the same line as the last comment 文本.  If your C 文件
   al读取y has properly formatted comments then using the ``-p`` 选项 will
   eliminate that bad behavior

2. If your source 文件 has highly formatted comments containing things
   such as tables or lists, then use the -p 选项 to preserve those
   pre-formatted comments.

3. I usually align things vertically (like '=' in assignments),

4. indent.sh puts a bogus blank line at the top of the 文件,

5. I don't like the way it 句柄s nested conditional compilation
   intermixed with code.  I prefer the preprocessor conditional tests
   be all right justified in that case.

6. I also indent brackets differently on 结构s than does this script.

7. I normally use no spaces in casts.  indent.sh 添加s spaces in casts like
   ``(FAR void *)&foo`` becomes ``(FAR void *) & foo``.

8. When used with header 文件s, the initial idempotence conditional test
   causes all preprocessor directives to be indented in the 文件.  So for
   header 文件s, you will need to substitute "^#  " with "#" in the
   converted header 文件.

You will manually need to check for the issues listed above after
performing the conversions.  nxstyle.c provides a good test that will
catch most of the indent.sh screw-ups.  To获取her, they do a pretty good
job of formatting.

See also nxstyle.c and uncrustify.cfg

