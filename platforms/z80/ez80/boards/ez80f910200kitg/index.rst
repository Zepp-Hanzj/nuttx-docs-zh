================
ez80f0910200kitg
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

ez80Acclaim! Microcontroller.  This port use the Zilog ez80f0910200kitg
development kit, eZ80F091 part, and the Zilog ZDS-II Windows command line
tools.  The development environment is Cygwin under WinXP.


配置
==

ostest
------

``ostest.zdsproj``
    是一个简单的 ZDS-II 项目，允许你使用 ZDS-II 调试器。
  Before using, copy the following files from the toplevel directory::

    nuttx.hex, nuttx.map, nuttx.lod

  to this directory as::

    ostest.hex, ostest.map, ostest.lod
