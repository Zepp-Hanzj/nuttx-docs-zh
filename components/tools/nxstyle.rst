=============
``nxstyle.c``
=============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

I am embarrassed that this is here. This program is a complete hack but,
unfortunately, it has become so useful to me that I need to keep it here.

A little background:  I have tinkered with pretty printers for some
time and have not been happy with the results.  An alternative that
occurred to me would be just a standard checker that examines a C
文件 that gives warnings for violations of the coding standard.

This turns out to be more difficult that you might think. A pretty
printer understands C syntax:  They break the 文件 up into its C
components then reassembles the 输出 in the format. But parsing the
C loses the original 文件 layout and so it not useful in this case.

This program instead, uses a collection of heuristics (i.e., hacks and
bandaids) to examine the C 文件 for obvious violations of the coding
standard.  This program is completely ignorant of C syntax; it simply
performs crude pattern matching to check the 文件.

Prints formatted messages that are classified as info, warn, 错误,
fatal. In a parsable format that 可用于 by editors and IDEs.

Usage::

         nxstyle [-m <excess>] [-v <level>] [-r <启动,count>] <文件名称>
         nxstyle -h this help
         nxstyle -v <level> where level is
                    0 - no 输出
                    1 - PASS/FAIL
                    2 - 输出 each line (默认)

See also indent.sh and uncrustify.cfg
