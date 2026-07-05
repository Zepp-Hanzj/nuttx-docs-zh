===================
``simhostroute.sh``
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Helper script used to 设置 up the tap 驱动, host routes, and IP Tables rules to
支持 networking with the simulator under Linux.

General usage:

.. code:: console

   $ tools/simhostroute.sh
   Usage: tools/simhostroute.sh <interface> <on|off>

See ``boards/sim/sim/sim/NETWORK-LINUX.txt`` for further information.
