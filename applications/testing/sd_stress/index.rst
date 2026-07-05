================================================
``sd_stress`` SD card or mount point stress test
================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

使用文件系统层对 SD 卡或其他挂载点执行压力测试。

单次测试运行：

- 创建一个暂存目录
- 在此目录中创建多个文件。对每个文件写入、读取和验证一组字节。
- 重命名暂存目录。
- 从重命名的目录中删除创建的文件。
- 删除重命名的目录。

以下运行时选项可用::

  nsh> sdstress -h
  Stress test on a mount point
  sdstress: [-r] [-b] [-f]
    -r   Number of runs (1-10000), default 32
    -b   Number of bytes (1-10000), default 4096
    -f   Number of files (1-999), default 64


已完成测试的示例::

  nsh> sdstress -b 4096 -f 32 -r 5
  Start stress test with 32 files, 4096 bytes and 5 iterations.
  iteration 0 took 4063.445 ms: OK
  iteration 1 took 4158.073 ms: OK
  iteration 2 took 4216.130 ms: OK
  iteration 3 took 4295.138 ms: OK
  iteration 4 took 4352.903 ms: OK
  Test OK: Average time: 4217.138 ms

以下 Kconfig 选项可用于在编译时配置应用程序。

- ``CONFIG_TESTING_SD_STRESS`` - 启用压力测试工具。
- ``CONFIG_TESTING_SD_STRESS_PROGNAME`` - 在 nsh 中注册的程序名称。
- ``CONFIG_TESTING_SD_STRESS_PRIORITY`` - 任务的优先级。
- ``CONFIG_TESTING_SD_STRESS_STACKSIZE`` - 任务的堆栈大小。
- ``CONFIG_TESTING_SD_STRESS_STACKSIZE`` - 要测试的文件系统的挂载点。
