=============
``netusb.sh``
=============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Helper script used to 设置 up the CDC ECM Ethernet Over USB 驱动,
host routes, and IP Tables rules to 支持 networking with a NuttX
system that has a CDC ECM Ethernet Over USB 驱动 configured. Only
支持ed on Linux.

General usage:

.. code:: console

   $ ./tools/netusb.sh
   Usage: tools/netusb.sh <main-interface> <usb-net-interface> <on|off>

This has been tested on the SAMA5D3-Xplained board; see
`Documentation/platforms/arm/sama5/boards/sama5d3-xplained/README.txt`
for more information on how to configure the CDC ECM 驱动 for that board.
