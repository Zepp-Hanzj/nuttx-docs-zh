===============================================
``nxhello`` NX 图形 "Hello, World!" 示例
===============================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

一个非常简单的图形示例，只是在显示器中央显示 "Hello, World!"。

可以选择以下配置选项：

- ``CONFIG_NSH_BUILTIN_APPS`` – 将 ``NXHELLO`` 示例构建为可从 NSH 命令行执行的内置应用程序
- ``CONFIG_EXAMPLES_NXHELLO_VPLANE`` – 从帧缓冲驱动中选择用于测试的平面。默认：``0``。
- ``CONFIG_EXAMPLES_NXHELLO_DEVNO`` – 从 LCD 驱动中选择用于测试的 LCD 设备。默认：``0``。
- ``CONFIG_EXAMPLES_NXHELLO_BGCOLOR`` – 背景颜色。默认取决于 ``CONFIG_EXAMPLES_NXHELLO_BPP``。
- ``CONFIG_EXAMPLES_NXHELLO_FONTID`` – 选择字体（参见 include/nuttx/nx/nxfonts.h 中的字体 ID 编号）。
- ``CONFIG_EXAMPLES_NXHELLO_FONTCOLOR`` – 背景窗口中使用的字体颜色。默认取决于 ``CONFIG_EXAMPLES_NXHELLO_BPP``。
- ``CONFIG_EXAMPLES_NXHELLO_BPP`` – 每像素位数。有效选项包括 ``2``、``4``、``8``、``16``、``24`` 和 ``32``。默认：``32``。
