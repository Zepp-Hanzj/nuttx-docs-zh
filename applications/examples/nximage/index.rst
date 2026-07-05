==============================
``nximage`` 显示 NuttX 标志
==============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

一个简单的示例，只是将 NuttX 标志图像放在显示器中央。
目前仅适用于 ``RGB23``（``888``）、``RGB16``（``656``）、``RGB8``（``332``）和 8 位灰度。

- ``CONFIG_NSH_BUILTIN_APPS`` – 将 ``NXIMAGE`` 示例构建为可从 NSH 命令行执行的内置应用程序。
- ``CONFIG_EXAMPLES_NXIMAGE_VPLANE`` – 从帧缓冲驱动中选择用于测试的平面。默认：``0``。
- ``CONFIG_EXAMPLES_NXIMAGE_DEVNO`` – 从 LCD 驱动中选择用于测试的 LCD 设备。默认：``0``。
- ``CONFIG_EXAMPLES_NXIMAGE_BPP`` – 每像素位数。有效选项包括 ``8``、``16`` 和 ``24``。默认为 ``16``。
- ``CONFIG_EXAMPLES_NXIMAGE_XSCALEp5``、``CONFIG_EXAMPLES_NXIMAGE_XSCALE1p5`` 或
  ``CONFIG_EXAMPLES_NXIMAGE_XSCALE2p0`` – 标志图像宽度为 160 列。可以定义其中一个
  来将图像水平缩放 0.5、1.5 或 2.0 倍。
- ``CONFIG_EXAMPLES_NXIMAGE_YSCALEp5``、``CONFIG_EXAMPLES_NXIMAGE_YSCALE1p5`` 或
  ``CONFIG_EXAMPLES_NXIMAGE_YSCALE2p0`` – 标志图像高度为 160 行。可以定义其中一个
  来将图像垂直缩放 0.5、1.5 或 2.0 倍。
- ``CONFIG_EXAMPLES_NXIMAGE_GREYSCALE`` – 灰度图像。默认：``RGB``。

那个行程编码图像是如何生成的？

1. 使用 GIMP 将图像输出为 ``.c`` 文件。
2. 添加一些 C 逻辑来对 GIMP ``.c`` 文件中的 RGB 图像进行调色板化。
3. 然后对调色板化图像添加一些简单的行程编码。

但现在有一个工具可以在 NxWidgets 包中找到，位于
``NxWidgets/tools/bitmap_converter.py``，可用于将任何图形格式转换为 NuttX RLE 格式。

**注意**：截至撰写本文时，大多数像素深度、缩放选项及其组合尚未经过测试。
