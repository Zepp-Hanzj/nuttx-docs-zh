=========================================
``termios`` Simple Termios interface test
=========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This directory contains a simple application that uses the termios interface
to change serial parameters. Just import a ``nsh`` config and enable the
following symbols:

- ``CONFIG_SERIAL_TERMIOS``   – Enable the termios support.
- ``CONFIG_EXAMPLES_TERMIOS`` – Enable the example itself.
