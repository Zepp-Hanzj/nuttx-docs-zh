===============================
``ustream`` Unix Stream Sockets
===============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This is the same test as ``examples/udp`` and similar to ``examples/udgram``, but
using Unix domain stream sockets.

Dependencies:

- ``CONFIG_NET_LOCAL`` – Depends on support for Unix domain sockets.

Configuration:

- ``CONFIG_EXAMPLES_USTREAM`` – Enables the Unix domain socket example.
- ``CONFIG_EXAMPLES_USTREAM_ADDR`` – Specifics the Unix domain address. Default:
  ``/dev/fifo``.
