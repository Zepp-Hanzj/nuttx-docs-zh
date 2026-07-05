================
On-Demand Paging
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/


The NuttX On-Demand Paging feature permits embedded MCUs with some
limited RAM space to execute large programs from some non-random
access media. If the platform meets certain requirements, then
NuttX can provide on-demand paging: It can copy .text from the
large program in non-volatile media into RAM as needed to execute
a huge program from the small RAM. Design and porting issues for
this feature are discussed in a separate document. Please see the
:ref:`NuttX Demand Paging <ondemandpaging>` design document
for further information.
