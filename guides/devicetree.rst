====================
设备树
====================

概述
--------

目前，NuttX 支持使用 libfdt（用于读取和操作二进制格式的实用程序库）解析 FDT（扁平设备树）：

https://github.com/dgibson/dtc/

在此基础上，NuttX 实现了一些获取属性的通用函数。NuttX 中的设备树支持将减少芯片/板的配置，目前尚未在 NuttX 内核框架中使用。

如何使用
-----------

1. 启用设备树和 libfdt

启用 Kconfig 设置：

    .. code-block:: console

      CONFIG_DEVICE_TREE=y                        /* Enable Device Tree */
      CONFIG_LIBFDT=y                             /* Enable utility library */

2. 注册 DTB 地址

使用 fdt_register 在 NuttX 中设置 DTB 地址

3. 解析 DTB

芯片/板将使用 fdt_get 获取 DTB 地址，然后使用 fdt_* API 解析 DTB 属性。
