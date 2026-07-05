=======================
以太网设备驱动
=======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

-  ``include/nuttx/net/netdev.h``。使用以太网驱动所需的
   所有结构和 API 都在此头文件中提供。结构 ``struct net_driver_s``
   定义了接口并通过 ``netdev_register()`` 传递给网络。

-  ``int netdev_register(FAR struct net_driver_s *dev, enum net_lltype_e lltype);``。
   每个以太网驱动通过调用 ``netdev_register()`` 注册自身。

-  **示例**：``drivers/net/dm90x0.c``、
   ``arch/drivers/arm/src/c5471/c5471_ethernet.c``、
   ``arch/z80/src/ez80/ez80_emac.c`` 等。
