=================================
``bastest`` Bas BASIC 解释器
=================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此目录包含一个小程序，它将挂载一个 ROMFS 文件系统，其中包含从 Bas ``2.4`` 版本中提取的 BASIC 测试文件。

- ``CONFIG_EXAMPLES_BASTEST_DEVMINOR`` – ROMFS 块驱动程序的次设备号。例如，``/dev/ramN`` 中的 ``N``。用于注册将保存包含 BASIC 测试文件的 ROMFS 文件系统的 RAM 块驱动程序。默认值：``0``。

- ``CONFIG_EXAMPLES_BASTEST_DEVPATH`` – ROMFS 块驱动程序设备的路径。必须与 ``EXAMPLES_BASTEST_DEVMINOR`` 匹配。用于注册将保存包含 BASIC 测试文件的 ROMFS 文件系统的 RAM 块驱动程序。默认值：``/dev/ram0``。

背景
------

Bas 是编程语言 BASIC 经典方言的解释器。它与 1980 年代典型的 BASIC 解释器非常兼容，不像其他一些 UNIX BASIC 解释器实现了不同的语法，破坏了与现有程序的兼容性。Bas 提供了许多用于结构化编程的 ANSI BASIC 语句，如过程、局部变量和各种循环类型。此外还有矩阵操作、自动 LIST 缩进以及特定经典方言中的许多语句和函数。不需要行号。

解释器在运行程序之前对源代码进行分词并解析变量和跳转目标的引用。此编译过程提高了效率并捕获语法错误、类型错误以及从未初始化的变量引用。Bas 使用 ANSI C 为 UNIX 系统编写。

许可证
------

BAS `2.4` 作为 NuttX 的一部分，使用 NuttX 所有组件使用的标准 3 条 BSD 许可证发布。这与原始 BAS `2.4` 许可证不兼容。

Copyright (c) 1999-2014 Michael Haardt

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
