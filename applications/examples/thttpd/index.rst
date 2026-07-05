========================
``thttpd`` THTTPD server
========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

An example that builds ``netutils/thttpd`` with some simple NXFLAT CGI programs.
In addition to those, this example accepts:

- ``CONFIG_EXAMPLES_THTTPD_NOMAC``    – (May be defined to use software assigned
  MAC)
- ``CONFIG_EXAMPLES_THTTPD_DRIPADDR`` – Default router IP address.
- ``CONFIG_EXAMPLES_THTTPD_NETMASK``  – Network mask.

Applications using this example will need to enable the following ``netutils``
libraries in the ``defconfig`` file: ::

  CONFIG_NETUTILS_NETLIB=y
  CONFIG_NETUTILS_THTTPD=y
