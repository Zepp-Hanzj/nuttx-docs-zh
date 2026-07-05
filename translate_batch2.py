#!/usr/bin/env python3
"""Translate remaining NuttX system application RST files (batch 2)."""

import os

DST_DIR = "/home/hanzj-mi/workspace/nuttx-docs-zh/applications/system"
NOTE = ".. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/"

def write(rel, content):
    path = os.path.join(DST_DIR, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Wrote: {rel}")

def main():
    print("Translating remaining content files (batch 2)...")
    
    # composite/index.rst
    write("composite/index.rst", f"""\
===========================================
``composite`` USB 复合设备命令
===========================================

{NOTE}

此逻辑添加了一个 NSH 命令来控制 USB 复合设备。复合设备中唯一支持的设备是
CDC/ACM 串口和 USB 大容量存储设备。复合设备中包含哪些设备通过配置结构体数组
传递给 ``composite_initialize()`` 函数来配置。

必需的总体配置：

启用硬件/处理器的 USB 支持，例如 ``SAMV7_USBDEVHS=y``

- ``CONFIG_USBDEV=y`` – USB 设备支持。
- ``CONFIG_USBDEV_COMPOSITE=y`` – USB 复合设备支持。
- ``CONFIG_COMPOSITE_IAD=y`` – 需要接口关联描述符。
- ``CONFIG_CDCACM=y`` – USB CDC/ACM 串口设备支持。
- ``CONFIG_CDCACM_COMPOSITE=y`` – USB CDC/ACM 串口复合设备支持。

接口、字符串描述符和端点编号通过上述配置结构体进行配置。CDC/ACM 串口设备
需要三个端点：一个中断驱动端点和两个批量端点。

- ``CONFIG_USBMSC=y`` – USB 大容量存储设备支持。
- ``CONFIG_USBMSC_COMPOSITE=y`` – USB 大容量存储复合设备支持。

与 CDC/ACM 的配置类似，描述符和端点编号通过配置结构体进行配置。

根据配置结构体，您需要配置不同的供应商 ID 和产品 ID。每个 ``VID``/``PID`` 对
设备而言是唯一的，因此对应于特定的配置。

Linux 会尝试检测设备类型，如果 ``VID``/``PID`` 对未知，则安装默认驱动程序。

Windows 要求已知且已安装的配置。使用 Atmel 硬件并安装了 Atmel-Studio 或
Atmel-USB 驱动程序后，您可以使用 Atmel 示例供应商 ID 和产品 ID 测试您的配置。

如果您的组合中配置了 USBMSC 和 CDC/ACM，则可以尝试使用：

- ``VID = 0x03EB`` (ATMEL)
- ``PID = 0x2424`` (ASF 示例，包含 MSC 和 CDC)

例如，如果您尝试测试最多七个 CDC 的配置，则：

- ``VID = 0x03EB`` (ATMEL)
- ``PID = 0x2426`` (ASF 示例，最多七个 CDC)

此附加组件可以构建为两个 NSH "内置" 命令：

- ``CONFIG_NSH_BUILTIN_APPS`` – 如果选择此选项：``conn`` 将连接 USB 复合设备；
  ``disconn`` 将断开 USB 复合设备。

此附加组件特有的配置选项：

- ``CONFIG_SYSTEM_COMPOSITE_DEBUGMM`` – 启用一些调试测试以检查内存使用和内存泄漏。

如果启用了 ``CONFIG_USBDEV_TRACE``（或 ``CONFIG_DEBUG_FEATURES`` 和
``CONFIG_DEBUG_USB``），则附加组件代码还将管理 USB 跟踪输出。跟踪输出量
可以使用以下选项控制：

- ``CONFIG_SYSTEM_COMPOSITE_TRACEINIT`` – 显示初始化事件。
- ``CONFIG_SYSTEM_COMPOSITE_TRACECLASS`` – 显示类驱动程序事件。
- ``CONFIG_SYSTEM_COMPOSITE_TRACETRANSFERS`` – 显示数据传输事件。
- ``CONFIG_SYSTEM_COMPOSITE_TRACECONTROLLER`` – 显示控制器事件。
- ``CONFIG_SYSTEM_COMPOSITE_TRACEINTERRUPTS`` – 显示中断相关事件。
""")

    # debugpoint/index.rst
    write("debugpoint/index.rst", f"""\
=====================================
``debugpoint`` 调试工具
=====================================

{NOTE}

``CONFIG_SYSTEM_DEBUGPOINT=y``

``debugpoint`` 工具是一个用于测试和管理系统中调试点（断点和监视点）的工具。
它允许用户设置、移除和测试各种类型的调试点。

用法::

    debugpoint [options]

选项::

    -r addr  在地址处设置读监视点
    -w addr  在地址处设置写监视点
    -b addr  在地址处设置断点
    -x addr  在地址处设置读写监视点
    -c       取消监视点或断点（必须与 -r、-w、-b 或 -x 一起使用）
    -l len   设置监视长度（必须与 -r、-w、-b 或 -x 一起使用）

示例::

    # 在地址 0x1000 处设置读监视点
    debugpoint -r 0x1000

    # 在地址 0x2000 处设置写监视点
    debugpoint -w 0x2000

    # 在地址 0x3000 处设置断点
    debugpoint -b 0x3000

    # 在地址 0x4000 处设置读写监视点
    debugpoint -x 0x4000

    # 取消地址 0x1000 处的读监视点
    debugpoint -r 0x1000 -c

    # 取消地址 0x2000 处的写监视点
    debugpoint -w 0x2000 -c

    # 取消地址 0x3000 处的断点
    debugpoint -b 0x3000 -c

    # 取消地址 0x4000 处的读写监视点
    debugpoint -x 0x4000 -c

    # 为地址 0x1000 处的读监视点设置 8 字节监视长度
    debugpoint -r 0x1000 -l 8

    # 为地址 0x2000 处的写监视点设置 8 字节监视长度
    debugpoint -w 0x2000 -l 8

    # 为地址 0x3000 处的断点设置 8 字节监视长度
    debugpoint -b 0x3000 -l 8

``debug`` 工具还包含断点和监视点的自动化测试。当不使用任何选项运行时，
它将执行这些测试以验证调试点的功能。
""")

    # dumpstack/index.rst
    write("dumpstack/index.rst", f"""\
========================================
``dumpstack`` 任务调用栈回溯
========================================

{NOTE}

描述
-----------

``dumpstack`` 应用程序是一个调试工具，用于显示 NuttX 系统中一个或多个任务（线程）
的调用栈回溯信息。它帮助开发者理解任务的执行路径和函数调用层次结构，这对于调试
崩溃、死锁或异常行为特别有用。

该应用程序利用 NuttX 内核中的 ``sched_dumpstack()`` 函数来检索和显示回溯信息。
根据配置，回溯可以显示原始内存地址或符号化的函数名。

特性
--------

* 按 PID 转储单个任务的回溯
* 按 PID 范围转储多个任务的回溯
* 支持符号化回溯显示（需要 ``CONFIG_ALLSYMS``）

用法
-----

基本语法
^^^^^^^^^^^^

.. code-block:: bash

   dumpstack [start_pid] [end_pid]

**无参数** – 转储当前任务的回溯：

.. code-block:: bash

   nsh> dumpstack

**单个 PID** – 转储特定任务的回溯：

.. code-block:: bash

   nsh> dumpstack 5

**PID 范围** – 转储从 start_pid 到 end_pid（包含）的所有任务的回溯：

.. code-block:: bash

   nsh> dumpstack 3 10

示例
^^^^^^^^

1. **转储 PID 4 到 6 的任务回溯（未启用 CONFIG_ALLSYMS）：**

   .. code-block:: bash

      nsh> dumpstack 4 6
      sched_dumpstack: backtrace| 4: 0x0000000010024fe8 0x000000001000cccc 0x000000001002504c 0x000000001002759c 0x000000001002a870
      sched_dumpstack: backtrace| 5: 0x0000000010024fe8 0x000000001000cccc 0x000000001002504c 0x000000001002759c 0x000000001002a870
      sched_dumpstack: backtrace| 6: 0x000000001002bbb4 0x000000001002bd70 0x00000000100d3890 0x00000000100d3908 0x000000001005193c 0x000000001004fc74 0x0000000010051514 0x000000001005160c
      sched_dumpstack: backtrace| 6: 0x0000000010051870 0x0000000010047fa8 0x000000001002cd50 0x000000001003d5ec 0x000000001002a888

2. **转储 PID 4 的任务回溯（启用 CONFIG_ALLSYMS）：**

   .. code-block:: bash

      nsh> dumpstack 4
      sched_dumpstack: backtrace:
      sched_dumpstack: [ 4] [<0x10025174>] nxsem_wait_slow+0x158/0x1ac
      sched_dumpstack: [ 4] [<0x1000cccc>] nxsem_wait+0x94/0xb0
      sched_dumpstack: [ 4] [<0x100251d8>] nxsem_wait_uninterruptible+0x10/0x2c
      sched_dumpstack: [ 4] [<0x10027728>] work_thread+0x1b4/0x238
      sched_dumpstack: [ 4] [<0x1002a9fc>] nxtask_start+0x7c/0xa4

配置
-------------

**CONFIG_SYSTEM_DUMPSTACK**

依赖
^^^^^^^^^^^^

dumpstack 应用程序需要以下内核配置：

* **CONFIG_SCHED_BACKTRACE** – 必须启用以提供 ``sched_backtrace()`` 函数
* **CONFIG_ALLSYMS** – 可选，启用回溯输出中的符号化函数名

限制
-----------

* 每次迭代的最大回溯深度为 16 帧
* 某些架构可能有有限的或没有回溯支持（已知问题：sim 环境无法查看其他线程的栈）
""")

    # gcov/index.rst
    write("gcov/index.rst", f"""\
==================
``gcov`` gcov 工具
==================

{NOTE}

gcov 是一个用于测试代码覆盖率的工具。程序运行后，可以查看每个文件的行覆盖率、
函数覆盖率和分支覆盖率。

支持
-------

当前系统支持四种代码覆盖率检测实现：

1. GCC 原生实现
2. CLANG 原生实现
3. GCC 覆盖率 nuttx 精简版
4. CLANG 覆盖率 nuttx 精简版

下表显示了四种实现之间的具体差异（截至 24.11.26）：

支持              GCC原生    CLANG原生     GCC-nuttx精简版    CLANG-nuttx精简版
编译器版本:        ALL          ALL        GCC 13.2 及以下    CLANG 17.0 及以下

程序覆盖率统计支持：

主程序              √            √                 √                     √
中断程序            ×            √                 √                     √

架构支持：

    arm                √            √                 √                     √
    arm64              √            √                 √
    riscv              √            √
    X86_X64            √            √
    xtensa             √            √
    sim                √            √

用法
=====

应用用法
---------
用法::

    gcov [-d path] [-t strip] [-r] [-h]

其中：

  -d 转储覆盖率，path 是覆盖率文件的路径，默认输出到标准输出
  -t 去除路径前缀的层数
  -r 重置覆盖率
  -h 显示此帮助文本并退出

适用平台示例
--------------------------------

1. SIM 平台用法

  1. 请启用以下配置

    # 支持对 sim 中所有代码的插桩
    1. CONFIG_COVERAGE_TOOLCHAIN=y

    # 启用插桩
    2. CONFIG_COVERAGE_ALL=y

    # 启用 gcov 应用
    3. CONFIG_SYSTEM_GCOV=y

  2. 编译并运行
     ```
     $ 代码编译后，会在 *.o 文件旁边生成同名的 *.gcno 文件。
     $ 编译完成后，运行待测试的代码，执行完成后退出 sim
     ```

  3. 运行 gcov 应用
     ```
     $ gcov -d path_to_gcno_file
     ```

  4. 检查是否生成成功
     ```
     在项目根目录执行以下命令检查是否有 gcda 文件生成（代码覆盖率数据）
     find ./ -name "*.gcno"
     find ./ -name "*.gcda"
     ```

  5. 示例：
     ```
     $ ./tools/configure.sh sim:nsh
     nsh: poweroff
     $ ./nuttx/tools/gcov.py -t gcov
     然后用浏览器打开 ./gcov/result/index.html
     ```

2. 适用于设备

  由于实现方式的差异，设备端分为 GCC 和 CLANG

  1. GCC

    1. 请启用以下配置

      # 推荐使用 nuttx 精简版
      CONFIG_COVERAGE_MINI=y

      # 启用 gcov 应用
      CONFIG_SYSTEM_GCOV=y

      # 请根据编译器在 makefile 中添加不同的编译选项
      CFLAGS += -fprofile-arcs -ftest-coverage -fno-inline

    2. 运行 gcov 应用
       ```
       $ gcov -d path_to_gcno_file
       ```

    3. 导出数据

      在设备上运行代码后，在 nuttx 命令行中执行 gcov -d /tmp/gcov 命令
      将生成的数据保存到文件系统。您需要使用您的方法将文件导出到主机。

    4. 生成报告

      1. 安装工具

        sudo apt install lcov

      2. 生成报告

        运行以下命令生成覆盖率报告

        # 默认在 vela 项目根目录生成，添加参数指定报告生成位置
        # -t 参数指定 gcov 版本，需要与 gcc 版本匹配

        # sim
        ./tools/gcov.py -t gcov

        # arm 平台
        ./tools/gcov.py -t arm-none-eabi-gcov

    5. 影响和注意事项
       ```
       1. 使用 .tools/gcov.sh 工具前，需要确保 *.gcno 和 *.gcda 文件存在
       2. 如果 *.gcno 不存在，请在 distclean 后重新编译代码
       3. 如果 *.gcda 不存在，请检查并使用 poweroff 正常退出 Vela
       ```

  2. CLANG

    # NXboards/arm/mps/mps3-an547/configs/gcov 中有现成的 defconfig 可供参考

    1. 请启用以下配置

      # 推荐使用 nuttx 精简版
      CONFIG_COVERAGE_MINI=y

      # 启用 gcov 应用
      CONFIG_SYSTEM_GCOV=y

      # 请根据编译器在 makefile 中添加不同的编译选项
      CFLAGS += -fprofile-instr-generate -fcoverage-mapping

    2. 修改链接脚本

      请在链接脚本中为以下数据找到相应的存储位置：

      详细示例请参考 boards/arm/mps/mps3-an547/scripts/flash.ld

      .. code-block:: none
          __llvm_prf_names : {{
              __start__llvm_prf_names = .;
              KEEP (*(__llvm_prf_names))
              __end__llvm_prf_names = .;
          }}

          __llvm_prf_data : {{
              __start__llvm_prf_data = .;
              KEEP (*(__llvm_prf_data))
              __end__llvm_prf_data = .;
          }}

          __llvm_prf_vnds : {{
              __start__llvm_prf_vnds = .;
              KEEP (*(__llvm_prf_vnds))
              __end__llvm_prf_vnds = .;
          }}

          __llvm_prf_cnts : {{
              __start__llvm_prf_cnts = .;
              KEEP (*(__llvm_prf_cnts))
              __end__llvm_prf_cnts = .;
          }}


    3. 运行 gcov 应用

      ```
      $ gcov -d path_to_gcno_file
      ```

    4. 导出数据

    5. 生成报告

      请执行以下命令，其中

      1. xxxfile：设备上导出的数据文件
      2. xxxelf：设备对应的 ELF 文件

      # 转换导出的覆盖率数据文件
      llvm-profdata merge -sparse xxxfile -o result.profdata

      # 生成可视化 html 文件
      llvm-cov show -format=html xxxelf -instr-profile=result.profdata -output-dir=./coverage/html
""")

    print("Batch 2 part 1 done.")
    return True

if __name__ == '__main__':
    main()
