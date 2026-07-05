================
``abi_check.py``
================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``abi_check.py`` is a Python tool for checking binary compatibility based on
DWARF debug information.

It 支持s three related workflows:

1. Given one or more static libraries (``.a``) and an ELF 文件, collect the
   undefined (external) symbols referenced by the libraries, locate those
   函数s in the ELF 文件, and 写入 their 函数 signatures to a JSON
   文件.
2. Generate two JSON 文件s from two different ELF 文件s (例如, an old
   构建 and a new 构建), and compare the signatures of 函数s with the
   same 名称 (返回 类型, 参数s, and for structs also 大小, member
   off设置s, member 类型s, etc.).
3. Given a single ELF 文件, detect structs with the same 名称 but different
   members.

Prerequisites:

- Python 3
- ``pyelftools`` (used to read ELF/DWARF)
- ``ar`` (used to extract object files from ``.a`` archives)
- ``pahole`` (only for ``--struct_check``)

.. note::

   Although the help 文本 mentions ``.so``, the current implementation uses
   ``ar x`` on each ``--lib`` input, so it expects ``.a`` archives.

Help message::

  $ python3 tools/abi_check.py -h
  usage: abi_check.py [-h] [-a LIB [LIB ...]] [-e ELF] [-c] [-d] [-j JSON] [-s]
                      [-i INPUT_JSON INPUT_JSON]

  This tool 用于 to check the binary compatibility of static libraries and has 以下 特性s:
      1. The 输入 consists of multiple static libraries and an ELF 文件. The tool searches
         for external APIs used by the static libraries, then locates these API 函数 signatures
         in the ELF 文件, and 输出s the results as a JSON 文件.
      2. Using the first 特性, with the static libraries unchanged,
         the tool can take a new ELF 文件 and an old ELF 文件 as 输入, 输出 two JSON 文件s,
         and compare the 函数 signatures of 函数s with the same 名称 in the two JSON 文件s.
         The comparison includes 返回 值s, 参数s, and if they are 结构s,
         it also compares the 结构 大小, member off设置s, member 类型s, etc.
      3.When the 输入 is a single ELF 文件, the tool can check if 结构s with the same 名称 have different members.

  选项s:
    -h, --help            show this help message and exit
    -a LIB [LIB ...], --lib LIB [LIB ...]
                          路径 to liba.so or lib.a
    -e ELF, --elf ELF     路径 to elf 文件
    -c, --check           If the static library contains debug information,
                          try to find the 函数 in the static library,
                          and 输出 the result to lib_<json> 文件
    -d, --dump            Dump result
    -j JSON, --json JSON  Save result to json 文件
    -s, --struct_check    Dump struct different
    -i INPUT_JSON INPUT_JSON, --输入_json INPUT_JSON INPUT_JSON
                          Diff two json 文件s

Examples::

  # 1) Extract signatures for external APIs referenced by one or more archives
  $ python3 tools/abi_check.py -a libfoo.a libbar.a -e nuttx -j out.json

  # 2) Compare signatures across two ELF 文件s
  $ python3 tools/abi_check.py -a libfoo.a libbar.a -e nuttx_old -j old.json
  $ python3 tools/abi_check.py -a libfoo.a libbar.a -e nuttx_new -j new.json
  $ python3 tools/abi_check.py -i old.json new.json

  # 3) Find struct definition mismatches within a single ELF
  $ python3 tools/abi_check.py -e nuttx -s
