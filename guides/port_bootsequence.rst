启动序列图
============================

此序列图的前提是 NuttX12.4.0、cxd56xx、非 SMP 和 Flat 构建。

启动序列的开始是 ``__start()``。

``__start()`` 将调用 ``nx_start()``。``nx_start()`` 将初始化内核
并调用 ``nsh_main()``。``nsh_main()`` 将执行 NuttShell(NSH)。
``nx_start()`` 是 NuttX 标准函数，但其行为取决于一些内核配置。
例如，调用 ``nsh_main()`` 也是可配置的。关于相关内核配置，请参阅
:doc:`/guides/port_relatedkernelconfigrations`。

.. uml::

   bootloader --> cxd56_start.c : 通过函数调用跳转到 __start 或解除 CM4F 的复位信号

   note over cxd56_start.c : 初始化 SP
   note over cxd56_start.c : 在处理器级别禁用 IRQ
   note over cxd56_start.c : 初始化 .data/.bss
   note over cxd56_start.c : cxd56_board_initialize() 作为 <arch>_board_initialize()

   cxd56_start.c --> nx_start.c : nx_start()

   note over nx_start.c : 初始化 IDLE 任务 TCB
   note over nx_start.c : nxsem_initialize()
   note over nx_start.c : 初始化堆
   note over nx_start.c : 创建并初始化 IDLE 组实例
   note over nx_start.c : sched_lock()
   note over nx_start.c : fs_initialize()
   note over nx_start.c : irq_initialize()
   note over nx_start.c : clock_initialize()
   note over nx_start.c : timer_initialize()
   note over nx_start.c : nxsig_initialize()
   note over nx_start.c : nxmq_initialize()
   note over nx_start.c : net_initialize()
   note over nx_start.c : binfmt_initialize()
   note over nx_start.c : up_initialize()
   note over nx_start.c : drivers_initialize()
   note over nx_start.c : board_early_initialize()
   note over nx_start.c : 为 IDLE 任务初始化 SDIO

   nx_start.c --> nx_bringup.c : nx_bringup()

   note over nx_bringup.c : 初始化环境变量（PWD、PATH、LD_LIBRARY_PATH）
   note over nx_bringup.c : 启动工作队列

   nx_bringup.c --> nx_start_application : nx_start_task()

   note over nx_start_application : board_late_initialize()
   note over nx_start_application : coredump_initialize()
   note over nx_start_application : 作为应用程序初始化任务启动 nsh_main()

   note over nx_start.c : up_idle()
