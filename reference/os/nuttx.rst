=====================================================
NuttX 导出给架构特定逻辑的 API
=====================================================

这些是操作系统导出的标准接口，供架构特定逻辑使用。

.. c:function:: void nx_start(void)

  **待补充**

OS 列表管理 API
=======================

**待补充**

.. c:function:: void nxsched_process_timer(void)

  此函数处理系统定时器事件。定时器中断逻辑本身由架构特定代码实现，
  但必须以 ``CONFIG_USEC_PER_TICK`` 为调用周期，定期调用以下 OS 函数。

.. c:function:: void irq_dispatch(int irq, FAR void *context)

  此函数必须从架构特定逻辑中调用，以便将中断分发到对应的已注册处理逻辑。
