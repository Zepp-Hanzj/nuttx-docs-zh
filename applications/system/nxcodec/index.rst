===============================
``nxcodec`` NuttX 编解码器工具
===============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``nxcodec`` 是 NuttX 的编解码器工具，用于处理音视频编解码操作。

概述
----

nxcodec 提供了一个命令行接口来测试和使用 NuttX 中的编解码器框架。它支持
各种编解码器的加载和使用。

配置选项
--------

- ``CONFIG_SYSTEM_NXCODEC`` – 启用 nxcodec 应用程序。
- ``CONFIG_VIDEO`` – 启用视频子系统支持。
- ``CONFIG_AUDIO`` – 启用音频子系统支持。
