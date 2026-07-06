===========
示例代码
===========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``apps/examples/nx*``。本文档未提供示例代码。但可以在 NuttX 源码树的
以下位置找到示例：这些示例代码旨在测试 NX。由于是测试代码，其目的是
验证功能，不一定代表最佳的 NX 编码实践。

- ``apps/examples/nx``。测试窗口功能，可选带工具栏。创建两个窗口，
  进行调整大小、移动、提升和降低操作。提供模拟鼠标和键盘输入。
- ``apps/examples/nxhello``。这是最简单的 NX 测试：在显示屏幕中央
  显示 "Hello, World!" 文字。
- ``apps/examples/nxtext``。演示如何管理字体以提供滚动文本窗口。
  包含弹出窗口，用于验证文本显示的裁剪和重绘功能。

在当前形式下，NX 图形系统提供了较低层次的图形和窗口支持。大部分
重绘管理和鼠标/键盘事件处理的复杂逻辑必须由 NX 客户端代码实现。

**构建** ``apps/examples/nx``。测试使用基于 Linux/Cygwin 的 NuttX
模拟器进行。该模拟器的构建说明在本文档的 `附录 C <#testcoverage>`__
中提供。

