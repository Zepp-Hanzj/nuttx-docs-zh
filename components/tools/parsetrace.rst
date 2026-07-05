=================
``parsetrace.py``
=================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

`par设置race.py` is a trace log parsing tool for the NuttX RTOS. It 支持s converting binary or 文本 trace logs into a human-读取able systrace format, and can resolve symbols and 类型 information from ELF 文件s. The tool also 支持s real-time trace 数据 parsing via serial port.

特性
--------
- 支持s parsing both binary and 文本 trace log formats.
- Integrates with ELF 文件s to resolve symbols and 类型 information for improved log 读取ability.
- 支持s real-time trace 数据 parsing from a serial 设备.
- 输出s systrace-compatible format for performance analysis and debugging.

Dependencies
------------
- Python 3
- pyelftools
- cxxfilt
- pydantic
- parse
- pycstruct
- 颜色log
- serial

Install dependencies:

.. code-block:: bash

   pip install pyelftools cxxfilt pydantic parse pycstruct colorlog serial

使用方法
-----

.. code-block:: bash

   python3 tools/parsetrace.py -t <trace_file> -e <elf_file> [-o <output_file>] [-v]

参数s:

- ``-t, --trace``: Path to the original trace file (supports binary or text format)
- ``-e, --elf``: Path to the NuttX ELF file (for symbol resolution)
- ``-o, --output``: Output file path, default is ``trace.systrace``
- ``-v, --verbose``: Enable verbose output
- ``-d, --device``: Serial device name (for real-time trace parsing)
- ``-b, --baudrate``: Serial baud rate, default is 115200

示例
--------

Parse a 文本 trace log and 输出 as systrace format:

.. code-block:: bash

   python3 tools/parsetrace.py -t trace.log -e nuttx.elf -o trace.systrace

Parse a binary trace log:

.. code-block:: bash

   python3 tools/parsetrace.py -t trace.bin -e nuttx.elf

Parse trace 数据 from a serial 设备 in real time:

.. code-block:: bash

   python3 tools/parsetrace.py -d /dev/ttyUSB0 -e nuttx.elf

Main Classes and Functions
--------------------------

- ``SymbolTables``: Handles ELF symbol and type information parsing.
- ``Trace``: Parses text trace logs.
- ``ParseBinaryLogTool``: Parses binary trace logs.
- ``TraceDecoder``: Parses real-time trace data from serial port.

For more details, refer to the source code in ``tools/par设置race.py``.
