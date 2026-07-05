===================
``flash_writer.py``
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This flash 写入r is using the xmodem for firmware transfer on
boards based on cxd56 chip (Ex. Spresense).  This tool depends on
the xmodem package (https://pypi.org/project/xmodem/).

For flashing the ``.spk`` 图像 to the board please use:

.. code:: console

   $ tools/flash_writer.py -s -c /dev/ttyUSB0 -d -b 115200 -n nuttx.spk
