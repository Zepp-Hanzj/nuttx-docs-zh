=======
irqinfo
=======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``irqinfo`` 是一个自定义 GDB 命令，用于打印系统中 IRQ 的信息。输出包括 IRQ 编号、IRQ 被触发的次数、IRQ 处理程序中花费的总时间、IRQ 的速率、IRQ 处理函数和处理程序的参数。

如果可能，参数将显示为函数。

它类似于 nsh 命令 ``irqinfo``，但在 GDB 中工作。更多信息请参阅 :ref:`cmdirqinfo`。

``RATE`` 列不可用。

.. tip::
    要显示 ``COUNT`` 列，你需要在 NuttX 配置中启用 ``CONFIG_SCHED_IRQMONITOR`` 选项。

语法
------

  ``irqinfo``


示例
-------
.. code-block:: bash

    (gdb) irqinfo
    IRQ  COUNT      TIME   RATE   HANDLER                                          ARGUMENT
    0    0          0      N/A    mps_reserved                             0x0 <sensor_unregister>
    2    0          0      N/A    mps_nmi                                  0x0 <sensor_unregister>
    3    0          0      N/A    arm_hardfault                            0x0 <sensor_unregister>
    4    0          0      N/A    arm_memfault                             0x0 <sensor_unregister>
    5    0          0      N/A    arm_busfault                             0x0 <sensor_unregister>
    6    0          0      N/A    arm_usagefault                           0x0 <sensor_unregister>
    11   1          0      N/A    arm_svcall                               0x0 <sensor_unregister>
    12   0          0      N/A    arm_dbgmonitor                           0x0 <up_debugpoint_remove>
    14   0          0      N/A    mps_pendsv                               0x0 <up_debugpoint_remove>
    15   6581421    0      N/A    systick_interrupt                        0x100010c <g_systick_lower>
    49   2          0      N/A    uart_cmsdk_tx_interrupt                  0x1000010 <g_uart0port>
    50   0          0      N/A    uart_cmsdk_rx_interrupt                  0x1000010 <g_uart0port>
    59   2          0      N/A    uart_cmsdk_ov_interrupt                  0x1000010 <g_uart0port>
    (gdb)
