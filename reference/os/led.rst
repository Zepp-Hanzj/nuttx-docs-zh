===========
LED 支持
===========

板级架构可能包含也可能不包含 LED。如果板级包含 LED，则大多数架构在 NuttX 配置文件中选中 ``CONFIG_ARCH_LEDS`` 后，会提供类似的 LED 支持。此 LED 支持属于架构特定逻辑的一部分，不由 NuttX 核心逻辑管理。不过，各架构提供的支持足够相似，因此可以在此处进行文档说明。

头文件
============

LED 相关定义由两个头文件提供：

-  每个板级的 LED 定义位于 ``board.h`` 中，该文件位于 ``<board-name>/include/board.h``
   （在配置 RTOS 时也会链接到 ``include/arch/board/board.h``）。这些定义将在
   `下文 <#leddefinitions>`__ 中讨论。
-  板级特定逻辑提供 LED 接口的具体实例。这是因为不同板级上 LED 支持的实现
   可能差异很大。不过，这些板级特定实现的函数原型会在架构通用头文件中提供。
   该头文件通常位于 ``<arch-name>/src/common/up_internal.h``，但在某些特定架构中
   也可能位于其他位置。这些函数原型将在 `下文 <#ledapis>`__ 中讨论。

LED 定义
===============

LED 支持的实现与板级架构密切相关。有些板级有多个 LED，有些只有一两个，还有些板级没有 LED。有些板级使用 LED 矩阵来显示字母数字数据等。NuttX 逻辑不直接引用特定的 LED，而是引用要在 LED 上显示的事件，并以适合板级的方式呈现；事件的呈现方式取决于板级上的可用硬件。

NuttX 使用的模型是板级可以显示 8 个事件，这些事件在 ``<board-name>/include/board.h`` 中定义如下：

.. code-block:: c

  #define LED_STARTED       ??
  #define LED_HEAPALLOCATE  ??
  #define LED_IRQSENABLED   ??
  #define LED_STACKCREATED  ??
  #define LED_INIRQ         ??
  #define LED_SIGNAL        ??
  #define LED_ASSERTION     ??
  #define LED_PANIC         ??

为每个预处理器变量分配的具体值可以是任何使板级逻辑实现最简便的值。每个定义的\ *含义*\ 如下：

-  ``LED_STARTED`` 描述 LED 逻辑首次初始化时 LED 的设置状态。此 LED 值被设置后不会被清除。
-  ``LED_HEAPALLOCATE`` 表示 NuttX 堆已完成配置。这是启动序列中的重要节点，因为如果内存配置错误，系统很可能会在此 LED 设置状态下崩溃。此 LED 值被设置后不会被清除。
-  ``LED_IRQSENABLED`` 表示中断已启用。同样，在调试过程中（或存在硬件问题时），系统很可能会在中断刚启用时崩溃，LED 会保留此设置。此 LED 值被设置后不会被清除。
-  ``LED_STACKCREATED`` 每次创建新栈时被设置。如果被设置，表示系统已尝试启动至少一个新线程。此 LED 值被设置后不会被清除。
-  ``LED_INIRQ`` 在每次中断的入口和出口处设置和清除。如果中断工作正常，此 LED 会呈现暗淡的光亮。
-  ``LED_SIGNAL`` 在信号处理函数的入口和出口处设置和清除。信号处理较为复杂，因此这在新架构的调试过程中尤其有用。
-  ``LED_ASSERTION`` 在发生断言时被设置。
-  ``LED_PANIC`` 在系统发生 panic 并挂起时以约 1Hz 的频率闪烁。

通用 LED 接口
=====================

``include/nuttx/board.h`` 包含以下声明：

.. c:function:: void board_autoled_initialize(void)

  在上电初始化的早期调用，用于初始化 LED 硬件。

  .. note:: 在大多数架构中，
    ``board_autoled_initialize()`` 从板级特定的初始化逻辑中调用。但也有少数架构
    仍然从通用芯片架构逻辑中调用此初始化函数。但无论如何，此接口都不是
    通用板级接口。

  .. warning:: 此接口名称最终将被移除；
    请勿在新的板级移植中使用。新的实现不应使用通用板级接口的命名约定，
    而应使用微处理器特定接口或板级特定接口的命名约定
    （例如 ``stm32_led_initialize()``）。

.. c:function:: void board_autoled_on(int led)

  调用以实例化事件的 LED 显示。
  ``led`` 参数是 ``<board-name>/include/board.h`` 中提供的定义之一。

.. c:function:: void board_autoled_off(int led)

  调用以终止事件的 LED 显示。
  ``led`` 参数是 ``<board-name>/include/board.h`` 中提供的定义之一。请注意，
  只有 ``LED_INIRQ``、``LED_SIGNAL``、``LED_ASSERTION`` 和 ``LED_PANIC``
  指示会被终止。
