===============
``mkfsdata.pl``
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此 perl 脚本用于构建 apps/netutils/webserver 所需的"伪"文件系统和
CGI 支持。目前仅被 apps/examples/uip 的 Makefile 使用。
该示例展示了如何配置 uIP Web 服务器的"伪"文件系统。

.. note::

   此 perl 脚本来自 uIP，（可能）由 Adam Dunkels 编写。
   uIP 具有与 NuttX 兼容的许可证。
