=====
libnx
=====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

The graphics capability consist both of components internal to the RTOS
and of user-callable 接口s.  In the NuttX kernel mode 构建 there are
some components of the graphics subsystem are callable in user mode and
other components that are internal to the RTOS.  This 目录, ``libs/libnx/``,
contains only those user-callable components.

The RTOS internal 函数s are contained in the ``graphics/`` 目录.
Please refer to ``Documentation/components/graphics`` for more detailed information.


.. toctree::
   :maxdepth: 1
   :caption: Contents:
   
   nxfonts.rst
