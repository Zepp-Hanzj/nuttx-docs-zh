================================
``smart_test`` SMART File System
================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``CONFIG_TESTING_SMART_TEST=y``

Author: Ken Pettit
Date: April 24, 2013

对 SMART（或任何）文件系统执行基于文件的测试。验证 seek、append 和 seek-with-write 操作::

  Usage:

    flash_test mtdblock_device

  Additional options:

    --force                     to replace existing installation

