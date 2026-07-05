==============================
VFS 性能分析器
==============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

虚拟文件系统（VFS）性能分析器提供了一种简单的内核内机制，用于无缝跟踪核心 VFS 操作（read、write、open、close）的执行时间和调用次数。这非常适合 CI/CD 自动化回归测试和性能瓶颈识别。

配置
=============

要启用分析器，请在 Kconfig 中选择 ``CONFIG_FS_PROFILER``。
要通过 procfs 动态暴露指标，请确保启用 ``CONFIG_FS_PROCFS``，并通过 ``CONFIG_FS_PROCFS_PROFILER`` 包含分析器节点。

使用
=====

启用后，分析器会自动拦截对底层 inode 操作的调用，并使用 ``perf_gettime()`` 记录执行经过的时间。由于在更新期间不使用阻塞互斥锁（而是使用快速的 ``atomic.h`` 操作），开销极小，并且在 SMP 上可以安全扩展。

要从 NuttShell (NSH) 集体查看当前统计信息，只需读取该节点：

.. code-block:: bash

    nsh> cat /proc/fs/profile
    VFS Performance Profile:
      Reads:          12 (Total time: 4500120 ns)
      Writes:          3 (Total time:   95050 ns)
      Opens:          15 (Total time: 1005000 ns)
      Closes:         15 (Total time:   45000 ns)

报告的时间是您特定架构上 ``perf_gettime()`` 提供的原始刻度/单位。