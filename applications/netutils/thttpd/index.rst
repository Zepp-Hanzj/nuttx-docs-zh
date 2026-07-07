============================
``thttpd`` THTTPD Web 服务器
============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 Jef Poskanzer 的 THTTPD HTTP 服务器的移植版本。有关 THTTPD 的一般信息，请参阅 http://acme.com/software/thttpd/。有关接口信息，请参阅 ``apps/include/netutils/thttpd.h``。使用此 ``thttpd`` 的应用程序需要在 ``defconfig`` 文件中提供以下定义以选择适当的 ``netutils`` 库::

  CONFIG_NETUTILS_NETLIB=y
  CONFIG_NETUTILS_THTTPD=y
