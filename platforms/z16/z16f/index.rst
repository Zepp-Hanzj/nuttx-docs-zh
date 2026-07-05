===============
Zilog ZNEO Z16F
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**Zilog z16f2800100zcog development kit**. This port use the Zilog
z16f2800100zcog development kit and the Zilog ZDS-II Windows command
line tools. The development environment is either Windows native or
Cygwin under Windows.

**STATUS:** The initial release of support for the z16f was made
available in NuttX version 0.3.7. A working NuttShell (NSH)
configuration as added in NuttX-6.33 (although a patch is required to
work around an issue with a ZDS-II 5.0.1 tool problem). An ESPI
driver was added in NuttX-7.2. Refer to the NuttX board
`README <https://github.com/apache/nuttx/blob/master/Documentation/platforms/z16/z16f/boards/z16f2800100zcog/README.txt>`__
file for further information.

支持的开发板
======

.. toctree::
   :glob:
   :maxdepth: 1

   boards/*/*
