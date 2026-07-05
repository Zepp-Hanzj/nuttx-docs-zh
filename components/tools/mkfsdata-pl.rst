===============
``mkfsdata.pl``
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This perl script 用于 to 构建 the "fake" 文件 system and CGI 支持
as needed for the apps/netutils/webserver.  It is currently used only
by the Make文件 at apps/examples/uip.  That example serves as an example
of how to configure the uIP webserver "fake" 文件 system.

.. note::

   This perl script comes from uIP and was (probably) written by Adam Dunkels.
   uIP has a license that is compatible with NuttX.
