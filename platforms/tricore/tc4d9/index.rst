=============
TriCore/TC4DA
=============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**TriCore/TC4DA** An TriCore flat address port was ported in NuttX-12.0. It
consists of the following features:

- Runs in Supervisor Mode.
- IRQs are managed by Interrupt Router (INT), IR Service Request Control Registers (SRC).
- Used System timer (STM) for systick.

This kernel with ostest have been tested with

-  Infineon's AURIX™ TC4DA Evaluation Board: TRIBOARD_TC4X9_COM

支持的开发板
======

.. toctree::
   :glob:
   :maxdepth: 1

   boards/*/*
