============
Renesas M16C
============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**Renesas M16C/26 Microcontroller**. This port uses the Renesas SKP16C26
Starter kit and the GNU M32C toolchain. The development environment is
either Linux or Cygwin under WinXP.

**STATUS:** Initial source files released in nuttx-0.4.2. At this point,
the port has not been integrated; the target cannot be built because the
GNU ``m16c-nuttx-elf-ld`` link fails with the following message:

Where the reference line is:

No workaround is known at this time. This is a show stopper for M16C.
Refer to the NuttX board
`README <https://github.com/apache/nuttx/blob/master/Documentation/platforms/renesas/m16c/boards/skp16c26/README.txt>`__
file for further information.

支持的开发板
======

.. toctree::
   :glob:
   :maxdepth: 1

   boards/*/*
