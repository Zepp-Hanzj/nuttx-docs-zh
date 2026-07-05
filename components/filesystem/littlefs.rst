========
LITTLEFS
========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

一个为微控制器设计的小型故障安全文件系统，来自
https://github.com/littlefs-project/littlefs。

在 NuttX 中，littlefs 可以通过虚拟文件系统进行交互。这意味着它可以正常使用 ``read()``、``write()`` 等调用，以及文件操作（``fopen()``、``fclose()`` 等）。

.. note::

   由于 littlefs 具有断电安全特性，必须在写入被永久存储之前提交写入（防损坏机制），因此需要定期对文件调用 ``fsync`` 来提交您的写入。关于 littlefs 文件何时被提交的确切语义在 `此 issue <https://github.com/apache/nuttx/issues/15840>`_ 中讨论。


..note::

  如果您的 littlefs 设置在启动时遇到崩溃，请尝试通过调整 Kconfig 中的 ``BLOCK_SIZE_FACTOR`` 选项来排查问题。系数 4 对 SD 卡效果很好。

.. warning::

   NuttX 上的 littlefs 支持仅适用于 mtd 驱动程序，用于闪存芯片、SD 卡和 eMMC 等存储设备。在 SD 卡和 eMMC 设备上的性能比闪存差。
