============================
GNU gprof 性能分析工具
============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
--------

gprof 是一个性能分析工具，帮助开发者分析运行时性能、识别性能热点并理解程序中的函数调用关系。NuttX 通过采样和函数调用追踪集成了 gprof 支持，以生成详细的性能分析报告。

特性
--------

gprof 提供以下关键功能：

1. **平面分析（Flat Profile）**：显示各函数的执行时间分布
2. **调用图（Call Graph）**：显示函数间的调用关系和时间分布
3. **函数统计（Function Statistics）**：提供详细指标，包括调用次数、累计时间和自身时间

配置
-------------

必需的配置选项
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

要启用 gprof 功能，请将以下选项添加到内核配置中::

    CONFIG_FRAME_POINTER=y
    CONFIG_PROFILE_MINI=y
    CONFIG_SYSTEM_GPROF=y

可选配置
~~~~~~~~~~~~~~~~~~~~~~

- ``CONFIG_PROFILE_ALL=y``：启用包含调用图信息的完整分析

配置详情
~~~~~~~~~~~~~~~~~~~~~

- ``CONFIG_FRAME_POINTER``：启用帧指针用于栈展开
- ``CONFIG_PROFILE_MINI``：启用基于定时器采样的轻量级分析，仅记录函数执行时间
- ``CONFIG_SYSTEM_GPROF``：启用 gprof 命令行工具
- ``CONFIG_PROFILE_ALL``：启用完整的函数调用图分析（可选，会增加性能开销）。记录函数调用关系。如果只需要特定模块的调用图分析，可以跳过此选项，改为在模块的 Makefile 或 CMakeLists.txt 中添加 ``-pg`` 编译器标志

基本用法
-----------

示例：CoreMark 性能分析
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

以下演示了对 CoreMark 基准测试的性能分析。

**步骤 1：配置和构建**::

    $ ./tools/configure.sh qemu-armv7a/nsh
    $ make -j
    $ qemu-system-arm -cpu cortex-a7 -nographic \
     -machine virt,virtualization=off,gic-version=2 \
     -net none -chardev stdio,id=con,mux=on -serial chardev:con \
     -mon chardev=con,mode=readline -kernel ./nuttx -s | tee gprof.log

**步骤 2：运行分析**::

    nsh> gprof start
    nsh> coremark
    nsh> gprof stop
    nsh> gprof dump /tmp/gmon.out
    nsh> hexdump /tmp/gmon.out

**步骤 3：在主机上分析**::

    $ grep -E "^[0-9a-f]+:" gprof.log | xxd -r > gmon.out
    $ arm-none-eabi-gprof nuttx gmon.out -b

    Flat profile:

    Each sample counts as 0.001 seconds.
      %   cumulative   self              self     total
     time   seconds   seconds    calls  Ts/call  Ts/call  name
     41.90     16.93    16.93                             up_idle
     20.61     25.26     8.33                             core_state_transition
      5.21     27.36     2.11                             core_list_find
      4.61     29.22     1.86                             core_list_reverse
      4.49     31.04     1.81                             core_bench_list
      3.64     34.18     1.47                             matrix_mul_matrix
      3.16     35.46     1.28                             coremark_crcu8
      ...

**结果解读：**

- ``up_idle`` 占 41.90% 的执行时间，表明系统大部分时间处于空闲状态
- ``core_state_transition`` 消耗 20.61%，是 CoreMark 中最耗时的函数
- 其他性能热点包括列表操作（``core_list_find``、``core_list_reverse``）和矩阵操作（``matrix_mul_matrix``）

示例：调用图分析
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

以下演示了启用 ``CONFIG_PROFILE_ALL`` 后的调用图分析。

**步骤 1：配置和构建**::

    $ ./tools/configure.sh mps2-an500/nsh
    $ make -j
    $ qemu-system-arm -M mps2-an500 -cpu cortex-m7 -nographic -kernel ./nuttx -s | tee gprof.log

**步骤 2：运行分析**::

    nsh> gprof start
    nsh> sleep 1
    nsh> gprof stop
    nsh> gprof dump /tmp/gmon.out
    nsh> hexdump /tmp/gmon.out

**步骤 3：在主机上分析**::

    $ grep -E "^[0-9a-f]+:" gprof.log | xxd -r > gmon.out
    $ arm-none-eabi-gprof nuttx/nuttx gmon.out -b
    Call graph

    granularity: each sample hit covers 4 byte(s) for 0.10% of 1.00 seconds

    index % time    self  children    called     name
    -----------------------------------------------
                    0.00    0.00    2066/2066        irq_dispatch [9]
    [5]      0.0    0.00    0.00    2066         perf_gettime [5]
                    0.00    0.00    2066/2066        up_perf_gettime [6]
    -----------------------------------------------
                    0.00    0.00    2066/2066        perf_gettime [5]
    [6]      0.0    0.00    0.00    2066         up_perf_gettime [6]
    -----------------------------------------------
                    0.00    0.00    1007/2017        systick_interrupt [21]
                    0.00    0.00    1010/2017        systick_getstatus [13]
    [7]      0.0    0.00    0.00    2017         systick_is_running [7]
    -----------------------------------------------

**调用图解读：**

上面的示例显示了完整的调用链::

    irq_dispatch [9]
      └─> perf_gettime [5]
            └─> up_perf_gettime [6]

有关调用图输出解读的详细信息，请参阅 gprof 手册：https://sourceware.org/binutils/docs/gprof/Call-Graph.html

分析单个模块
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如果你不想全局启用 ``CONFIG_PROFILE_ALL``（以减少性能开销），可以通过在模块的构建配置中添加 ``-pg`` 编译器标志来分析特定模块。

**在 Makefile 中添加 -pg**::

    # 为整个目录启用 -pg
    CFLAGS += -pg

**在 CMakeLists.txt 中添加 -pg**::

    target_compile_options(mymodule PRIVATE -pg)

这种方法允许精确分析关键模块，同时保持整体系统性能。

从串口控制台恢复数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如果你无法直接从设备导出文件，可以通过串口控制台的 xxd 输出恢复数据并在主机上重建：

**步骤 1：在设备上显示十六进制数据**::

    nsh> hexdump /tmp/gmon.out

**步骤 2：** 将串口控制台输出保存到日志文件（例如 ``gprof.log``）

**步骤 3：使用 xxd -r 将 xxd 输出转换为二进制**::

    $ grep -E "^[0-9a-f]+:" gprof.log | xxd -r > gmon.out

**步骤 4：使用 gprof 分析转换后的文件**::

    $ arm-none-eabi-gprof nuttx/nuttx gmon.out -b

真实板卡示例
-------------------

QEMU aarch64 示例
~~~~~~~~~~~~~~~~~~~~

此示例使用 **QEMU** 和 **aarch64-none-elf-gcc**，配合 **qemu-armv8a** 板卡。

**步骤 1：配置和构建**::

    $ ./tools/configure.sh -E qemu-armv8a:nsh
    # 确保 CONFIG_SYSTEM_GPROF 和 CONFIG_PROFILE_MINI 已启用
    $ make -j

**步骤 2：启动 QEMU**::

    $ qemu-system-aarch64 -cpu cortex-a53 -smp 4 -nographic \
      -machine virt,virtualization=on,gic-version=3 \
      -chardev stdio,id=con,mux=on -serial chardev:con \
      -mon chardev=con,mode=readline -semihosting -kernel ./nuttx

**步骤 3：挂载 hostfs 以保存数据**::

    nsh> mount -t hostfs -o fs=. /mnt

**步骤 4：运行分析**::

    nsh> gprof start
    # 在此进行一些测试
    nsh> gprof stop
    nsh> gprof dump /mnt/gmon.out

**步骤 5：在主机上分析**::

    $ aarch64-none-elf-gprof nuttx gmon.out -b

ESP32-S3 示例（使用 Ymodem 传输）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

此示例演示了在 **esp32s3-devkit** 上通过 Ymodem 传输数据进行性能分析。

**步骤 1：配置和构建**::

    $ ./tools/configure.sh -E esp32s3-devkit:nsh
    # 启用以下选项：
    # CONFIG_PROFILE_MINI=y
    # CONFIG_SYSTEM_GPROF=y
    # CONFIG_FS_TMPFS=y
    # CONFIG_SYSTEM_YMODEM=y
    $ make flash ESPTOOL_PORT=/dev/ttyUSB0 -j

**步骤 2：连接到板卡**::

    $ minicom -D /dev/ttyUSB0 -b 115200

**步骤 3：在设备上运行分析**::

    nsh> gprof start
    # 在此进行一些测试，例如 ostest
    nsh> gprof stop
    nsh> gprof dump /tmp/gmon.out
    nsh> sb /tmp/gmon.out

**步骤 4：接收文件并在主机上分析**::

    # 在 minicom 中通过 Ymodem 接收文件，然后：
    $ cp nuttx nuttx_prof
    $ xtensa-esp32s3-elf-objcopy -I elf32-xtensa-le --rename-section .flash.text=.text nuttx_prof
    $ xtensa-esp32s3-elf-gprof nuttx_prof gmon.out

.. note:: 对于 Xtensa 目标，``objcopy --rename-section`` 步骤是必需的，因为代码段有不同的名称（``.flash.text``）。

重要说明
---------------

- ``CONFIG_PROFILE_ALL`` 会显著增加性能开销和内存使用。仅在需要调用图分析时启用。
- 对于模拟器环境，使用 ``CONFIG_SIM_PROFILE`` 启用 gprof 功能。
- 在 ARM Cortex-M v6/v7/v8 上，Flat Profile 功能有限制，需要修改 ``_vectors`` 以在中断期间捕获线程 PC 指针。

参考
----------

- GNU gprof 手册：https://sourceware.org/binutils/docs/gprof/
