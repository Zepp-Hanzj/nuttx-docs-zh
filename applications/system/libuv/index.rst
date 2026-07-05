========================
``libuv`` libuv 库
========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``libuv`` 是一个跨平台的异步 I/O 库，最初为 Node.js 开发，现已成为独立项目。

概述
----

libuv 提供了事件循环、异步网络、异步文件系统操作、子进程管理等功能。

配置选项
--------

- ``CONFIG_SYSTEM_LIBUV`` – 启用 libuv 库支持。
