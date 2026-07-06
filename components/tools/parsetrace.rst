=================
``parsetrace.py``
=================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``parsetrace.py`` 是 NuttX RTOS 的 trace 日志解析工具。它支持将二进制或文本 trace 日志转换为人类可读的 systrace 格式，并能从 ELF 文件中解析符号和类型信息。该工具还支持通过串口实时解析 trace 数据。

特性
--------
- 支持解析二进制和文本 trace 日志格式。
- 集成 ELF 文件以解析符号和类型信息，提高日志可读性。
- 支持从串口设备实时解析 trace 数据。
- 输出 systrace 兼容格式，用于性能分析和调试。

依赖
------------
- Python 3
- pyelftools
- cxxfilt
- pydantic
- parse
- pycstruct
- colorlog
- serial

安装依赖：

.. code-block:: bash

   pip install pyelftools cxxfilt pydantic parse pycstruct colorlog serial

使用方法
-----

.. code-block:: bash

   python3 tools/parsetrace.py -t <trace_file> -e <elf_file> [-o <output_file>] [-v]

参数：

- ``-t, --trace``：原始 trace 文件路径（支持二进制或文本格式）
- ``-e, --elf``：NuttX ELF 文件路径（用于符号解析）
- ``-o, --output``：输出文件路径，默认为 ``trace.systrace``
- ``-v, --verbose``：启用详细输出
- ``-d, --device``：串口设备名（用于实时 trace 解析）
- ``-b, --baudrate``：串口波特率，默认为 115200

示例
--------

解析文本 trace 日志并输出为 systrace 格式：

.. code-block:: bash

   python3 tools/parsetrace.py -t trace.log -e nuttx.elf -o trace.systrace

解析二进制 trace 日志：

.. code-block:: bash

   python3 tools/parsetrace.py -t trace.bin -e nuttx.elf

从串口设备实时解析 trace 数据：

.. code-block:: bash

   python3 tools/parsetrace.py -d /dev/ttyUSB0 -e nuttx.elf

主要类和函数
--------------------------

- ``SymbolTables``：处理 ELF 符号和类型信息解析。
- ``Trace``：解析文本 trace 日志。
- ``ParseBinaryLogTool``：解析二进制 trace 日志。
- ``TraceDecoder``：从串口解析实时 trace 数据。

更多详情请参阅 ``tools/parsetrace.py`` 中的源代码。
