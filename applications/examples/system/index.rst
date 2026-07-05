===========================
``system`` System() example
===========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This is a simple test of the ``system()`` command. The test simply executes this
``system`` command:

.. code-block:: C

  ret = system("ls -Rl /");
