===================
``initialconfig.c``
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 a C 文件 that 可用于 to 创建 an initial 配置. This
permits creating a new 配置 from scratch, without relying on any
existing board 配置 in place. This utility will 创建 a barebones
``.config`` 文件 sufficient only for instantiating the symbolic 链接s necessary
to do a real 配置.
