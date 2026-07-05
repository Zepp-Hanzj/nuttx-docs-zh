====================================
``syslogd`` 系统日志守护进程
====================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``syslogd`` 是一个系统日志守护进程，用于接收和处理系统日志消息。

概述
----

``syslogd`` 实现了标准的 syslog 协议，可以接收来自系统各组件的日志消息，
并将它们写入指定的日志文件或其他输出目标。

配置选项
--------

- ``CONFIG_SYSTEM_SYSLOGD`` – 启用 syslogd 应用程序。
- ``CONFIG_NET`` – 启用网络支持（用于远程日志接收）。
- ``CONFIG_SYSTEM_SYSLOGD_SOCKET_PATH`` – 指定 syslog 套接字路径。
