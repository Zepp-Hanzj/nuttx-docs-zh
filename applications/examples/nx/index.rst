==========================
``nx`` NX 图形示例
==========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此目录包含对 ``include/nuttx/nx/nx.h`` 中定义的 NX API 子集的简单测试。
可以选择以下配置选项：

- ``CONFIG_NSH_BUILTIN_APPS`` – 将 NX 示例构建为可从 NSH 命令行执行的内置应用程序
- ``CONFIG_EXAMPLES_NX_BGCOLOR`` – 背景颜色。默认取决于 ``CONFIG_EXAMPLES_NX_BPP``。
- ``CONFIG_EXAMPLES_NX_COLOR1`` – 窗口 1 的颜色。默认取决于 ``CONFIG_EXAMPLES_NX_BPP``。
- ``CONFIG_EXAMPLES_NX_COLOR2`` – 窗口 2 的颜色。默认取决于 ``CONFIG_EXAMPLES_NX_BPP``。
- ``CONFIG_EXAMPLES_NX_TBCOLOR`` – 工具栏的颜色。默认取决于 ``CONFIG_EXAMPLES_NX_BPP``。
- ``CONFIG_EXAMPLES_NX_FONTID`` – 选择字体（参见 ``include/nuttx/nx/nxfonts.h`` 中的字体 ID 编号）。
- ``CONFIG_EXAMPLES_NX_FONTCOLOR`` – 字体颜色。默认取决于 ``CONFIG_EXAMPLES_NX_BPP``。
- ``CONFIG_EXAMPLES_NX_BPP`` – 每像素位数。有效选项包括 ``2``、``4``、``8``、``16``、``24`` 和 ``32``。默认为 ``32``。
- ``CONFIG_EXAMPLES_NX_RAWWINDOWS`` – 使用原始窗口；默认使用带有工具栏的美观的、带边框的 NXTK 窗口。
- ``CONFIG_EXAMPLES_NX_STACKSIZE`` – 创建 NX 服务器时使用的堆栈大小。默认 ``2048``。
- ``CONFIG_EXAMPLES_NX_CLIENTPRIO`` – 客户端优先级。默认：``100``
- ``CONFIG_EXAMPLES_NX_SERVERPRIO`` – 服务器优先级。默认：``120``
- ``CONFIG_EXAMPLES_NX_LISTENERPRIO`` – 事件监听器线程的优先级。默认 ``80``。

该示例还具有以下设置，如果不符合预期将生成错误::

  CONFIG_DISABLE_MQUEUE=n
  CONFIG_DISABLE_PTHREAD=n
  CONFIG_NX_BLOCKING=y
  CONFIG_BOARDCTL=y
