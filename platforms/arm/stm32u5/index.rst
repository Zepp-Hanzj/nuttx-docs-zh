==========
ST STM32U5
==========

.. note::
   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/


This is a port of NuttX to the STM32U5 Family

The STM32U5 is a chip based on ARM Cortex-M33.

Used development board is the B-U585I-IOT02A

Most code is copied and adapted from the STM32L5 port.

The only supported STM32U5 family currently is:

================ ======= ============================
NuttX config      Manual Chips
================ ======= ============================
STM32U5           RM0456 STM32U575xx and STM32U585xx
================ ======= ============================

TODO list
---------

Extensive testing.  Only initial sniff tests have been done.
A prober TODO list should be generated.

References
----------

[RM0456] STMicroelectronics, STM32U575/585 Arm(R)-based 32-bit MCUs, Rev 2


Supported MCUs
==============

TODO

Peripheral Support
==================

TODO

Supported Boards
================

.. toctree::
   :glob:
   :maxdepth: 1

   boards/*/*
