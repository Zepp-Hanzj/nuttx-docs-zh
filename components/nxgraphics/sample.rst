===========
Sample Code
===========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``apps/examples/nx*``. No sample code 提供 in this document.
However, examples can be found in the NuttX source tree at the follow
locations: That example code is intended to test NX. Since it is test
code, it is designed to exercise 函数ality and does not necessarily
represent best NX coding practices.

- ``apps/examples/nx``. This is a test of windows, optionally with
  toolbars. Two 窗口s are 创建d, re-大小d, moved, raise lowered.
  Simulated mouse and keyboard 输入 提供.
- ``apps/examples/nxhello``. This is intended to be simplest NX test:
  It simply 显示s the words "Hello, World!" centered on the 显示.
- ``apps/examples/nxtext``. This illustrates how fonts may be managed
  to provide scrolling 文本 窗口s. Pop-up 窗口s are included to
  verify the clipping and re-drawing of the 文本 显示.

In its current form, the NX graphics system provides a low level of
graphics and 窗口 支持. Most of the complexity of manage redrawing
and handling mouse and keyboard events must be implemented by the NX
client code.

**构建ing** ``apps/examples/nx``. Testing was performed using the
Linux/Cygwin-based NuttX simulator. Instructions 提供 for
构建ing that simulation 提供 in `Appendix C <#testcoverage>`__
of this document.

