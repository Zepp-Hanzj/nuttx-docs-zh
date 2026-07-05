=======================
矩阵键盘（KMATRIX）
=======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

**什么是键盘？**
键盘是一种小型键盘，键数有限，通常排列成矩阵形式。它通常用于数字输入、访问控制或简单用户界面。

例如，典型的 12 键数字键盘如下所示：

.. image:: images/keypad-example.png
  :alt: 12 键矩阵键盘示例
  :align: center
  :width: 200px

**用途**。KMATRIX 驱动程序为通过 GPIO 暴露开关矩阵的板卡提供通用键盘实现。它定期扫描行和列，使用简单的去抖动检测状态变化，并通过通用键盘上半部分发出键盘事件。这使设备可用作字符驱动程序（例如 ``/dev/keypad0``），使用标准键盘接口。

**为什么使用轮询**。此第一版本使用轮询，以便在任何具有可用 GPIO 的板卡上广泛使用，无需每块板卡的 IRQ 布线、引脚中断功能或扩展器特定的中断支持。轮询还简化了早期启动过程，并在验证键映射和 GPIO 配置时使驱动程序可预测。预计未来的迭代将添加中断驱动扫描和 I2C 扩展器变体；GPIO 轮询路径仍然是一个良好的基线和后备方案。

**驱动程序概述**。KMATRIX 下半部分扫描矩阵，并在检测到按键或释放时调用 ``keyboard_event()``。键盘上半部分在请求的 ``devpath`` 注册字符设备，并将事件存储在循环缓冲区中。应用程序从设备读取 ``struct keyboard_event_s`` 或使用可选的 kbd-codec 层。

**板卡支持**。要支持 KMATRIX，板卡必须提供：

#. **GPIO 定义**

   - 定义行和列 GPIO（引脚数组）。
   - 提供按 ``row * ncols + col`` 索引的键映射数组。

#. **配置回调**

   - ``config_row(pin)``：将行 GPIO 配置为输出。
   - ``config_col(pin)``：将列 GPIO 配置为输入，上拉或下拉与接线一致。
   - ``row_set(pin, active)``：驱动行激活/非激活。对于 STM32F4Discovery 示例，行被驱动为低电平以激活。
   - ``col_get(pin)``：读取列并在按下时返回 ``true``。

#. **注册钩子**

   - 实现 ``board_kmatrix_initialize(const char *devpath)`` 以调用 ``kmatrix_register(&config, devpath)``。
   - 在启动期间调用板卡钩子（例如 ``board_kmatrix_initialize("/dev/keypad0")``）。

**参考实现（STM32F4Discovery）**。当前参考实现位于 ``boards/arm/stm32/common/src/stm32_kmatrix_gpio.c``：

- 行：``BOARD_KMATRIX_ROW0..3``（输出）
- 列：``BOARD_KMATRIX_COL0..2``（带上拉的输入）
- 键映射：4x3 电话键盘布局
- 回调：``km_stm32_config_row``、``km_stm32_config_col``、``km_stm32_row_set``、``km_stm32_col_get``
- 注册：``board_kmatrix_initialize()`` 调用 ``kmatrix_register()``

**数据路径摘要**。

- 板卡调用 ``board_kmatrix_initialize("/dev/keypad0")``
- ``kmatrix_register()`` 配置 GPIO 并调用 ``keyboard_register(&lower, devpath, buflen)``
- 上半部分在 ``devpath`` 注册设备节点
- ``kmatrix_scan_worker()`` 在按键/释放时调用 ``keyboard_event()``
- 应用程序从设备节点读取事件
