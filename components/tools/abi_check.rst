================
``abi_check.py``
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``abi_check.py`` 是一个基于 DWARF 调试信息检查二进制兼容性的 Python 工具。

它支持三种相关工作流：

1. 给定一个或多个静态库（``.a``）和一个 ELF 文件，收集
   库引用的未定义（外部）符号，在 ELF 文件中定位
   这些函数，并将其函数签名写入 JSON 文件。
2. 从两个不同的 ELF 文件（例如一个旧构建和一个新构建）
   生成两个 JSON 文件，并比较同名函数的签名
   （返回类型、参数，对于结构体还包括大小、成员偏移量、
   成员类型等）。
3. 给定单个 ELF 文件，检测同名但成员不同的结构体。

前置条件：

- Python 3
- ``pyelftools``（用于读取 ELF/DWARF）
- ``ar``（用于从 ``.a`` 归档中提取目标文件）
- ``pahole``（仅用于 ``--struct_check``）

.. note::

   尽管帮助文本提到了 ``.so``，但当前实现对每个 ``--lib`` 输入
   使用 ``ar x``，因此它期望 ``.a`` 归档。

Help message::

  $ python3 tools/abi_check.py -h
  usage: abi_check.py [-h] [-a LIB [LIB ...]] [-e ELF] [-c] [-d] [-j JSON] [-s]
                      [-i INPUT_JSON INPUT_JSON]

  This tool is used to check the binary compatibility of static libraries and has the following features:
      1. The input consists of multiple static libraries and an ELF file. The tool searches
         for external APIs used by the static libraries, then locates these API function signatures
         in the ELF file, and outputs the results as a JSON file.
      2. Using the first feature, with the static libraries unchanged,
         the tool can take a new ELF file and an old ELF file as input, output two JSON files,
         and compare the function signatures of functions with the same name in the two JSON files.
         The comparison includes return values, parameters, and if they are structures,
         it also compares the structure size, member offsets, member types, etc.
      3.When the input is a single ELF file, the tool can check if structures with the same name have different members.

  options:
    -h, --help            show this help message and exit
    -a LIB [LIB ...], --lib LIB [LIB ...]
                          Path to liba.so or lib.a
    -e ELF, --elf ELF     Path to elf file
    -c, --check           If the static library contains debug information,
                          try to find the function in the static library,
                          and output the result to lib_<json> file
    -d, --dump            Dump result
    -j JSON, --json JSON  Save result to json file
    -s, --struct_check    Dump struct different
    -i INPUT_JSON INPUT_JSON, --input_json INPUT_JSON INPUT_JSON
                          Diff two json files

Examples::

  # 1) 提取一个或多个归档引用的外部 API 签名
  $ python3 tools/abi_check.py -a libfoo.a libbar.a -e nuttx -j out.json

  # 2) 比较两个 ELF 文件的签名
  $ python3 tools/abi_check.py -a libfoo.a libbar.a -e nuttx_old -j old.json
  $ python3 tools/abi_check.py -a libfoo.a libbar.a -e nuttx_new -j new.json
  $ python3 tools/abi_check.py -i old.json new.json

  # 3) 在单个 ELF 中查找结构体定义不匹配
  $ python3 tools/abi_check.py -e nuttx -s
