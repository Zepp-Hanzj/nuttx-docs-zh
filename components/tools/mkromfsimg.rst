=================
``mkromfsimg.sh``
=================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This script may be used to automate the generation of a ROMFS 文件 system
图像. It accepts an rcS script "template" and generates an 图像 that
may be mounted under /etc in the NuttX pseudo 文件 system.

.. tip::

   Edit the resulting header 文件 and mark the generated 数据 值s as
   ``const`` so that they will be stored in FLASH.
