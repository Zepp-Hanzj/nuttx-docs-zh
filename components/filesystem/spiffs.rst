======
SPIFFS
======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

创建镜像
=================

此实现应与以下工具生成的镜像兼容：

* `mkspiffs <https://github.com/igrr/mkspiffs>`_
* ESP-IDF `spiffsgen.py <https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/storage/spiffs.html#spiffsgen-py>`_

注意：请确保以下 NuttX 配置与这些工具兼容：

* ``CONFIG_SPIFFS_COMPAT_OLD_NUTTX`` 已禁用
* ``CONFIG_SPIFFS_LEADING_SLASH=y``

mkspiffs
--------

* 为 ``SPIFFS_OBJ_NAME_LEN`` 指定 ``CONFIG_SPIFFS_NAME_MAX + 1``。
* 为 ``SPIFFS_OBJ_META_LEN`` 指定 0。

ESP-IDF ``spiffsgen.py``
------------------------

* 为 ``--obj-name-len`` 选项指定 ``CONFIG_SPIFFS_NAME_MAX + 1``。
* 为 ``--meta-len`` 选项指定 0。
