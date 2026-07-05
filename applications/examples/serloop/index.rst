===========================
``serloop`` Serial Loopback
===========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This is a mindlessly simple loopback test on the console. Useful for testing new
serial drivers. Configuration options include:

- ``CONFIG_EXAMPLES_SERLOOP_BUFIO`` – Use C buffered I/O (``getchar``/``putchar``) vs.
   raw console I/O (read/write).
