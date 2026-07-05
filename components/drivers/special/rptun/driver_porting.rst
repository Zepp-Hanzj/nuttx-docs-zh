=========================
驱动移植指南
=========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

RPTUN 框架设计为可移植的。它通过 ``rptun_ops`` 结构中定义的一组回调函数与特定硬件平台解耦。要在新的硬件平台上支持 RPTUN，平台驱动开发人员必须实现以下核心接口以满足框架的运行要求。

驱动核心职责
============================

提供资源信息
----------------------------

- 驱动必须定义共享内存区域并正确填充其中的资源表。

- 驱动需要通过 ``get_resource()`` 或 ``get_firmware()`` 接口向 RPTUN 框架提供资源表或远程固件地址。

实现核心操作接口 (rptun_ops)
-----------------------------------------------

**生命周期管理**

提供启动 (``start``) 和停止 (``stop``) 远程核的底层实现。

**核间通信**

- ``notify``：实现向远程核发送通知的逻辑（通常触发硬件中断）。

- ``register_callback``：注册一个回调函数，当从远程核接收到中断时，底层中断服务例程应调用该函数。

**地址空间转换**

如果主核和远程核的地址空间不一致，必须实现 ``get_addrenv()`` 接口以提供地址转换表。

关联硬件中断
-----------------------------

在平台的中断服务例程 (ISR) 中，必须能够识别来自远程核的硬件中断，并准确调用通过 ``register_callback`` 注册的回调函数。

rptun_ops 结构
===================

每个 RPTUN 驱动必须实现 ``struct rptun_ops_s`` 的一个实例：

.. code-block:: c

   struct rptun_ops_s
   {
     CODE FAR const char *(*get_local_cpuname)(FAR struct rptun_dev_s *dev);
     CODE FAR const char *(*get_cpuname)(FAR struct rptun_dev_s *dev);
     CODE FAR const char *(*get_firmware)(FAR struct rptun_dev_s *dev);

     CODE FAR const struct rptun_addrenv_s *(*get_addrenv)(
                           FAR struct rptun_dev_s *dev);
     CODE FAR struct rptun_rsc_s *(*get_resource)(FAR struct rptun_dev_s *dev);

     CODE bool (*is_autostart)(FAR struct rptun_dev_s *dev);
     CODE bool (*is_master)(FAR struct rptun_dev_s *dev);

     CODE int (*config)(struct rptun_dev_s *dev, void *data);
     CODE int (*start)(FAR struct rptun_dev_s *dev);
     CODE int (*stop)(FAR struct rptun_dev_s *dev);
     CODE int (*notify)(FAR struct rptun_dev_s *dev, uint32_t vqid);
     CODE int (*register_callback)(FAR struct rptun_dev_s *dev,
                                   rptun_callback_t callback, FAR void *arg);

     CODE void (*reset)(FAR struct rptun_dev_s *dev, int value);
     CODE void (*panic)(FAR struct rptun_dev_s *dev);
   };

接口描述
======================

get_local_cpuname
-----------------

返回本地 CPU 名称字符串。

get_cpuname
-----------

返回远程 CPU 名称字符串。此名称用于标识通信通道并注册字符设备。

get_firmware
------------

返回远程固件文件路径。如果远程核固件需要由主核加载，此接口应返回固件路径。

get_addrenv
-----------

返回地址环境转换表。当各核之间物理地址不同时使用。

.. code-block:: c

   struct rptun_addrenv_s
   {
     uintptr_t pa;    /* 本地核上的物理地址 */
     uintptr_t da;    /* 远程核上的设备地址 */
     size_t    size;  /* 内存区域大小 */
   };

get_resource
------------

返回资源表的指针。驱动必须在共享内存中准备资源表并通过此接口返回其地址。

is_autostart
------------

返回是否自动启动远程核。如果为 ``true``，``rptun_initialize()`` 将自动调用 ``rptun_dev_start()``。

is_master
---------

返回本地核是否为主核。主核通常负责初始化共享内存和资源表。

config
------

配置远程核。在启动远程核之前调用。

start
-----

启动远程核。实现硬件特定的启动序列。

stop
----

停止远程核。实现硬件特定的关闭序列。

notify
------

向远程核发送通知。通常通过触发硬件中断（如邮箱、软件中断）实现。

register_callback
-----------------

注册用于接收远程核通知的回调函数。驱动的 ISR 应在接收到核间中断时调用此回调。

reset
-----

使用指定的复位值复位远程核。

panic
-----

触发远程核的 panic 状态。

示例实现
======================

以下是实现 RPTUN 驱动操作的最小示例：

.. code-block:: c

   static FAR const char *myboard_rptun_get_cpuname(FAR struct rptun_dev_s *dev)
   {
     return "remote";
   }

   static FAR struct rptun_rsc_s *
   myboard_rptun_get_resource(FAR struct rptun_dev_s *dev)
   {
     return &g_rptun_rsc;  /* 预定义的资源表 */
   }

   static bool myboard_rptun_is_master(FAR struct rptun_dev_s *dev)
   {
     return true;
   }

   static int myboard_rptun_start(FAR struct rptun_dev_s *dev)
   {
     /* 硬件特定的远程核启动 */
     return OK;
   }

   static int myboard_rptun_stop(FAR struct rptun_dev_s *dev)
   {
     /* 硬件特定的远程核关闭 */
     return OK;
   }

   static int myboard_rptun_notify(FAR struct rptun_dev_s *dev, uint32_t vqid)
   {
     /* 触发核间中断 */
     return OK;
   }

   static int myboard_rptun_register_callback(FAR struct rptun_dev_s *dev,
                                              rptun_callback_t callback,
                                              FAR void *arg)
   {
     /* 存储回调供 ISR 使用 */
     g_callback = callback;
     g_arg = arg;
     return OK;
   }

   static const struct rptun_ops_s g_myboard_rptun_ops =
   {
     .get_cpuname       = myboard_rptun_get_cpuname,
     .get_resource      = myboard_rptun_get_resource,
     .is_master         = myboard_rptun_is_master,
     .start             = myboard_rptun_start,
     .stop              = myboard_rptun_stop,
     .notify            = myboard_rptun_notify,
     .register_callback = myboard_rptun_register_callback,
   };

现有实现
========================

参考实现可在以下文件中找到：

- ``arch/sim/src/sim/sim_rptun.c`` - 模拟器 RPTUN 驱动
- ``arch/arm/src/stm32h7/stm32_rptun.c`` - STM32H7 RPTUN 驱动
- ``arch/arm/src/imx9/imx9_rptun.c`` - i.MX9 RPTUN 驱动
- ``arch/arm/src/nrf53/nrf53_rptun.c`` - nRF53 RPTUN 驱动
- ``arch/risc-v/src/k230/k230_rptun.c`` - K230 RPTUN 驱动
- ``arch/risc-v/src/qemu-rv/qemu_rv_rptun.c`` - QEMU RISC-V RPTUN 驱动
