===========================
``nxlines`` NX 线条绘制
===========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

一个非常简单的图形示例，只是演示 NX 线条绘制逻辑。

可以选择以下配置选项：

- ``CONFIG_EXAMPLES_NXLINES_VPLANE`` – 从帧缓冲驱动中选择用于测试的平面。默认：``0``。
- ``CONFIG_EXAMPLES_NXLINES_DEVNO`` – 从 LCD 驱动中选择用于测试的 LCD 设备。默认：``0``。
- ``CONFIG_EXAMPLES_NXLINES_BGCOLOR`` – 背景颜色。默认取决于 ``CONFIG_EXAMPLES_NXLINES_BPP``。
- ``CONFIG_EXAMPLES_NXLINES_LINEWIDTH`` – 以像素为单位选择线条宽度（默认：``16``）。
- ``CONFIG_EXAMPLES_NXLINES_LINECOLOR`` – 背景窗口中绘制的中心线条颜色。
  默认取决于 ``CONFIG_EXAMPLES_NXLINES_BPP``（实际上没有有意义的默认值）。
- ``CONFIG_EXAMPLES_NXLINES_BORDERWIDTH`` – 背景窗口中绘制的圆形边框宽度。（默认：``16``）。
- ``CONFIG_EXAMPLES_NXLINES_BORDERCOLOR`` – 背景窗口中绘制的圆形边框颜色。
  默认取决于 ``CONFIG_EXAMPLES_NXLINES_BPP``（实际上没有有意义的默认值）。
- ``CONFIG_EXAMPLES_NXLINES_CIRCLECOLOR`` – 背景窗口中填充的圆形区域颜色。
  默认取决于 ``CONFIG_EXAMPLES_NXLINES_BPP``（实际上没有有意义的默认值）。
- ``CONFIG_EXAMPLES_NXLINES_BORDERCOLOR`` – 背景窗口中绘制的线条颜色。
  默认取决于 ``CONFIG_EXAMPLES_NXLINES_BPP``（实际上没有有意义的默认值）。
- ``CONFIG_EXAMPLES_NXLINES_BPP`` – 每像素位数。有效选项包括 ``2``、``4``、``8``、``16``、``24`` 和 ``32``。默认为 ``16``。
- ``CONFIG_NSH_BUILTIN_APPS`` – 将 NX 线条示例构建为 NSH 内置函数。
