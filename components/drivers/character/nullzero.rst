=================================
``dev_null.c`` 和 ``dev_zero.c``
=================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这些文件提供标准的 ``/dev/null`` 和 ``/dev/zero`` 设备。参见 ``include/nuttx/drivers/drivers.h`` 了解如果您想注册这些设备应调用的函数原型（``devnull_register()`` 和 ``devzero_register()``）。
