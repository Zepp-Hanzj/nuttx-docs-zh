=====
libnx
=====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

图形功能包括 RTOS 内部组件和用户可调用的接口。
在 NuttX 内核模式构建中，图形子系统的某些组件可在用户模式下调用，
而其他组件则是 RTOS 内部的。此目录 ``libs/libnx/`` 仅包含那些
用户可调用的组件。

RTOS 内部函数包含在 ``graphics/`` 目录中。
有关更详细的信息，请参阅 ``Documentation/components/graphics``。


.. toctree::
   :maxdepth: 1
   :caption: Contents:
   
   nxfonts.rst
