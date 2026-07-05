===========
Intel 80x86
===========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

All x86 source reside in lower-level common, chip-specific, and architecture-specific
directories.

arch/x86/src/common/ Directory
==============================

This directory holds source files common to all x86 architectures.

架构特定目录
======

Architecture-specific directories hold common source files shared for by
implementations of specific x86 architectures.

``i486``
  This directory holds logic appropriate for any instantiation of the 32-bit
  i486 architecture.

芯片特定目录
======

The same x86 architecture may be realized in different chip implementations.
For SoC chips, in particular, on-chip devices and differing interrupt
structures may require special, chip-specific definitions in these chip-
specific directories.

``qemu``
  This is the implementation of NuttX on the QEMU x86 simulation.

.. toctree::
   :maxdepth: 1
   :glob:

   */*
