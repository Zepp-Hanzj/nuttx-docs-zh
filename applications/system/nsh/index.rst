=================================
``nsh`` NuttShell (NSH) 示例
=================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

基本配置
-------------------

本目录提供了如何配置和使用 NuttShell (NSH) 应用程序的示例。NSH 是一个简单的 shell 应用程序。
NSH 的说明文档位于 ``apps/nshlib/README.md``。通过以下配置启用此功能::

  CONFIG_SYSTEM_NSH=y

使用此示例的应用程序需要在配置目录中提供一个 ``defconfig`` 文件，其中包含构建 NSH 库的指令::

  CONFIG_NSH_LIBRARY=y

其他配置要求
--------------------------------

**注意**：如果使用 NSH 串口控制台，则还需要以下配置来构建 ``readline()`` 库::

  CONFIG_SYSTEM_READLINE=y

如果包含网络支持::

  CONFIG_NETUTILS_NETLIB=y
  CONFIG_NETUTILS_DHCPC=y
  CONFIG_NETDB_DNSCLIENT=y
  CONFIG_NETUTILS_TFTPC=y
  CONFIG_NETUTILS_WEBCLIENT=y

如果启用了 Telnet 控制台，则 defconfig 文件还应包含::

  CONFIG_NETUTILS_TELNETD=y

此外，如果启用了 Telnet 控制台，请确保在 NuttX 配置文件中设置以下选项，
否则性能会很差（因为每次 TCP 传输只传输一个字符）：

- ``CONFIG_STDIO_BUFFER_SIZE`` – 某个值 ``>= 64``
- ``CONFIG_STDIO_LINEBUFFER=y``
