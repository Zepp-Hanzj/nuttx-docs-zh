================================================
``sd_bench`` SD card or mount point bench test
================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

使用文件系统层对 SD 卡或其他挂载点执行基准测试。

单次测试运行：

- 顺序将字节块写入设备上的测试文件，直到测试持续时间结束。
- 可选地，读回并验证写入的字节数。

以下运行时选项可用::

  sdbench: [-b] [-r] [-d] [-k] [-s] [-a] [-v]
    -b   Block size per write (1-65536), default 512
    -r   Number of runs (1-10000), default 5
    -d   Max duration of a test (ms) (1-60000), default 2000
    -k   Keep test file when finished, default false
    -s   Call fsync after each block, false calls fsync
         only at the end of each run, default false
    -a   Test performance on aligned data, default false
    -v   Verify data and block number, default true

已完成测试的示例::

  nsh> sdbench
  Using block size = 512 bytes, sync = false

  Testing Sequential Write Speed...
    Run  1:    345.9 KB/s, max write time: 156.907 ms (3.2 KB/s), fsync: 259.687 ms
    Run  2:    378.8 KB/s, max write time: 30.273 ms (16.5 KB/s), fsync: 240.832 ms
    Run  3:    372.1 KB/s, max write time: 37.630 ms (13.3 KB/s), fsync: 261.005 ms
    Run  4:    341.7 KB/s, max write time: 186.352 ms (2.7 KB/s), fsync: 240.875 ms
    Run  5:    375.6 KB/s, max write time: 37.785 ms (13.2 KB/s), fsync: 250.928 ms
    Avg   :    362.8 KB/s, 3.999 MB written.

  Testing Sequential Read Speed...
    Run  1:    636.5 KB/s, max read/verify time: 54.1180 ms (9.2 KB/s)
    Run  2:    648.9 KB/s, max read/verify time: 54.0520 ms (9.3 KB/s)
    Run  3:    663.2 KB/s, max read/verify time: 43.5360 ms (11.5 KB/s)
    Run  4:    721.8 KB/s, max read/verify time: 11.7640 ms (42.5 KB/s)
    Avg   :    652.6 KB/s, 3.999 MB and verified


以下 Kconfig 选项可用于在编译时配置应用程序。

- ``CONFIG_TESTING_SD_BENCH`` - 启用 SD 基准测试工具。
- ``CONFIG_TESTING_SD_BENCH_PROGNAME`` - 在 nsh 中注册的程序名称。
- ``CONFIG_TESTING_SD_BENCH_PRIORITY`` - 任务的优先级。
- ``CONFIG_TESTING_SD_BENCH_STACKSIZE`` - 任务的堆栈大小。
- ``CONFIG_TESTING_SD_BENCH_DEVICE`` - 运行 sdbench 的挂载点。
