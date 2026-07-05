================================
``getevent`` 输入事件监视器
================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``getevent`` 是一个命令行输入事件监视器。它通过输入子系统捕获并显示来自鼠标、触摸屏和键盘设备的实时事件。

它对于驱动程序调试、输入调试和系统集成测试非常有用。

支持的事件类型
=====================

- **鼠标** -- 按钮状态、x/y 坐标、滚轮（当 ``CONFIG_INPUT_MOUSE_WHEEL`` 启用时）
- **触摸屏** -- 带坐标、标志、时间戳的多点触控以及可选的压力/大小详情
- **键盘** -- 键码和事件类型

配置
=============

在 NuttX 配置中启用 ``getevent``::

  CONFIG_GRAPHICS_INPUT_GETEVENT=y

可选设置：

.. list-table::
   :header-rows: 1

   * - 选项
     - 默认值
     - 描述
   * - ``CONFIG_GRAPHICS_INPUT_GETEVENT_STACKSIZE``
     - ``DEFAULT_TASK_STACKSIZE``
     - getevent 任务的栈大小
   * - ``CONFIG_GRAPHICS_INPUT_GETEVENT_PRIORITY``
     - ``100``
     - 任务优先级
   * - ``CONFIG_GRAPHICS_INPUT_GETEVENT_DETAIL_INFO``
     - ``n``
     - 显示额外的触控详情（压力、宽度、高度）

使用方法
=====

自动检测所有输入设备::

  nsh> getevent

监视特定设备::

  nsh> getevent -m /dev/mouse0
  nsh> getevent -t /dev/input0
  nsh> getevent -k /dev/kbd0

组合多个设备::

  nsh> getevent -m /dev/mouse0 -t /dev/input0 -k /dev/kbd0

显示帮助::

  nsh> getevent -h

按 ``Ctrl+C`` 停止监视。

工作原理
============

当不带参数启动时，``getevent`` 扫描 ``/dev`` 中与已知输入设备名称模式（``mouse*``、``input*``、``kbd*``）匹配的字符设备。每个检测到的设备以非阻塞模式打开。

主事件循环使用 500ms 超时的 ``poll()`` 等待所有打开的文件描述符上的数据。当事件可用时，相应的读取回调解码并通过 ``syslog`` 打印事件结构。

处理 ``SIGINT``（``Ctrl+C``）以允许正常关闭并正确清理资源。

示例输出
==============

鼠标事件::

  [getevent]: mouse event: /dev/mouse0
  [getevent]:    buttons : 01
  [getevent]:          x : 120
  [getevent]:          y : 340

触控事件::

  [getevent]: touch event: /dev/input0
  [getevent]:    npoints : 1
  [getevent]: Point      : 0
  [getevent]:      flags : 03
  [getevent]:          x : 200
  [getevent]:          y : 450
  [getevent]:  timestamp : 123456789

键盘事件::

  [getevent]: keyboard event: /dev/kbd0
  [getevent]:          type : 1
  [getevent]:          code : 28
