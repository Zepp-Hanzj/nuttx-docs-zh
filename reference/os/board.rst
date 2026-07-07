==============================================
板级特定逻辑导出给 NuttX 的 API
==============================================

导出的板级特定接口在头文件 ``include/nuttx/board.h`` 中提供函数原型。
从板级逻辑导出到架构特定逻辑的接口有很多。但从板级特定逻辑导出到通用
NuttX 逻辑的接口只有少数几个。其中与初始化相关的少数接口将在本段中讨论。
还有一些其他接口，如 ``boardctl()`` <#boardctl>`__ 使用的接口，
将在其他段落中讨论。

NuttX OS 逻辑使用的所有板级特定接口都用于受控的板级初始化。
在三个时间点可以插入自定义的板级特定初始化逻辑：

首先是 ``<arch>_board_initialize()``：此函数\ *不是*\ 从通用 OS 逻辑调用的，
而是从架构特定的上电复位逻辑中调用。此函数仅用于非常底层的初始化，
如 GPIO 引脚配置、电源设置、DRAM 初始化等。此时 OS 尚未初始化，
因此不能分配内存或初始化设备驱动。

另外两个板级初始化\ *钩子*\ 从 OS 启动逻辑中调用，如下所述：

.. c:function:: void board_early_initialize(void)

  下一级初始化通过调用 ``up_initialize()``（位于
  ``arch/<arch>/src/common/up_initialize.c``）来执行。此时 OS 已经初始化，
  可以在此阶段初始化驱动。``up_initialize()`` *不是*板级特定接口，
  而是架构特定、板级无关的接口。

  但与此同时，如果在配置中选择了 ``CONFIG_BOARD_EARLY_INITIALIZE=y``，
  OS 还会调用一个名为 ``board_early_initialize()`` 的板级特定初始化函数。
  ``board_early_initialize()`` 的执行上下文适合大多数简单设备驱动的早期初始化，
  是 up_initialize() 的板级特定扩展。

  ``board_early_initialize()`` 在启动初始化线程上运行。某些初始化操作
  不能在启动初始化线程上执行。这是因为初始化线程不能等待事件。
  例如，挂载文件系统或初始化 SD 卡等设备可能需要等待。
  因此，这类驱动初始化必须推迟到 ``board_late_initialize()``。

.. c:function:: void board_late_initialize(void)

  最后，在用户应用代码启动之前。如果在配置中选择了
  ``CONFIG_BOARD_LATE_INITIALIZE=y``，则在启动序列中会执行一个最终的
  附加初始化调用，调用名为 ``board_late_initialize()`` 的函数。
  ``board_late_initialize()`` 将在 ``up_initialize()`` 和
  ``board_early_initialize()`` 调用之后很久才被调用。
  ``board_late_initialize()`` 将在主应用任务启动之前被调用。
  此附加初始化阶段可用于初始化更复杂的板级特定设备驱动。

  在 board_late_initialize() 的上下文中，允许等待事件、使用 I2C、SPI 等。
  这是因为 ``board_late_initialize()`` 将在临时的内部内核线程上运行。
