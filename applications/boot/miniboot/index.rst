===============================
``miniboot`` 最小引导加载程序
===============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

基于 NuttX 的最小引导加载程序。

配置选项：

- ``CONFIG_MINIBOOT_SLOT_PATH`` - 应用固件镜像插槽字符设备驱动程序的路径。默认：``/dev/ota0``
- ``CONFIG_MINIBOOT_HEADER_SIZE`` - 应用固件镜像头大小
