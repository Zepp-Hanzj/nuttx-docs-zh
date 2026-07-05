=====================
``pipe`` Pipe example
=====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

A test of the ``mkfifo()`` and ``pipe()`` APIs. Requires ``CONFIG_PIPES``

- ``CONFIG_EXAMPLES_PIPE_STACKSIZE`` – Sets the size of the stack to use when
  creating the child tasks. The default size is ``1024``.
