=======================
Devices Category (NUTS)
=======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此测试类别通过与 `/dev` 下的 NuttX 设备的字符驱动程序接口进行交互来测试其行为。可以使用 ``CONFIG_TESTING_NUTS_DEVICES`` 启用该类别。

此类别包含以下测试套件：

* ``CONFIG_TESTING_NUTS_DEVICES_DEVASCII``: ``/dev/ascii`` 的测试
* ``CONFIG_TESTING_NUTS_DEVICES_DEVCONSOLE``: ``/dev/console`` 的测试
* ``CONFIG_TESTING_NUTS_DEVICES_DEVNULL``: ``/dev/null`` 的测试
* ``CONFIG_TESTING_NUTS_DEVICES_DEVURANDOM``: ``/dev/urandom`` 的测试
* ``CONFIG_TESTING_NUTS_DEVICES_DEVZERO``: ``/dev/zero`` 的测试
