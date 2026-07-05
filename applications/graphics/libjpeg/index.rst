==========================================
``libjpeg`` JPEG 图像编码库
==========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``libjpeg`` 是一个开源库，提供以 JPEG 格式编码和解码图像的功能。它实现了基线 JPEG 标准，通常用于与图像相关的应用程序和实用程序。

引入库
=====================

要在 C 程序中使用 ``libjpeg``，请包含主头文件：

.. code-block:: c

   #include <jpeglib.h>

配置
=============

需要在 Kconfig 中启用 ``libjpeg`` 支持：

  CONFIG_LIBJPEG=y

示例
=======

NuttX 提供了一个示例应用程序，演示如何使用 ``libjpeg`` 编码、解码和调整 JPEG 图像大小。它位于：

``apps/graphics/jpgresizetool``
