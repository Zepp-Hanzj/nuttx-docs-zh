=======
TriCore
=======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

所有 TriCore 源代码位于底层通用、芯片特定和架构特定的
目录中。

arch/tricore/src/common/ Directory
==================================

此目录包含所有 TriCore 架构通用的源文件。

架构特定目录
======

架构特定目录包含特定 TriCore 架构实现共享的通用源文件。

``TriCore``
    此目录包含适用于 32 位 TriCore 架构任何实例化的逻辑。
  TriCore architecture.

芯片特定目录
======

特别是对于 SoC 芯片，片上设备和不同的中断
结构可能需要在这些芯片特定目录中进行特殊的芯片特定定义。

核心芯片实现基于英飞凌底层驱动（iLLDs）。
统一的 API 对熟悉英飞凌 SDK/HAL 的开发者更加友好。
We can get more code examples on Infineon's official Github: `AURIX_code_examples <https://github.com/Infineon/AURIX_code_examples>`__

``TC3xx/TC4xx``
  This is the implementation of NuttX on the Infineon’s AURIX™- TC3xx/TC4xx microcontroller family.

.. toctree::
   :maxdepth: 1
   :glob:

   */*
