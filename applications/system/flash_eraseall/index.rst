====================================
``flash_eraseall`` Flash 擦除工具
====================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``flash_eraseall`` 命令用于擦除整个 MTD 设备或擦除指定的分区。该命令需要
在 NuttX 配置中启用 ``CONFIG_SYSTEM_FLASH_ERASEALL=y``。

用法
----

::

  flash_eraseall [-q] <mtd_device>

选项
----

- ``-q``: 静默模式，不显示进度信息。
- ``<mtd_device>``: 要擦除的 MTD 设备路径，例如 ``/dev/mtd0`` 或 ``/dev/mtdblock0``。

示例
----

.. code-block:: bash

  flash_eraseall /dev/mtd0

注意事项
--------

- 擦除操作会永久删除设备上的所有数据，请谨慎使用。
- 确保在擦除前备份重要数据。
