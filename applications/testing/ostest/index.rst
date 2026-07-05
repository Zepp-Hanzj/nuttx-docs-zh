.. _ostest:

==================
``ostest`` OS test
==================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 NuttX _资格认证_ 套件。它试图测试一组广泛的操作系统功能。截至撰写本文时，其覆盖范围不是很广泛，但它用于验证每个 NuttX 版本的资格。

``ostest`` 的行为可以通过 ``boards/<arch>/<chip>/<board>/configs/<config>/defconfig`` 文件中的以下设置进行修改：

- ``CONFIG_NSH_BUILTIN_APPS`` – 将 OS 测试示例构建为 NSH 内置应用程序。
- ``CONFIG_TESTING_OSTEST_LOOPS`` – 用于控制测试的执行次数。如果未定义，测试执行一次。如果定义为零，测试将永远运行。

- ``CONFIG_TESTING_OSTEST_STACKSIZE`` – 用于创建 ostest 任务。默认为 ``8192``。
- ``CONFIG_TESTING_OSTEST_NBARRIER_THREADS`` – 指定在屏障测试中创建的线程数。默认为 8，但在没有足够内存启动这么多线程的系统上可能需要更小的数字。

- ``CONFIG_TESTING_OSTEST_RR_RANGE`` – 在轮询调度测试期间创建两个线程。每个线程在可配置的范围内搜索质数，执行可配置的次数。此值指定搜索范围的末尾，与运行次数一起允许配置此测试的长度——它应该至少持续几十秒。允许值 ``[1; 32767]``，默认 ``10000``。

- ``CONFIG_TESTING_OSTEST_RR_RUNS`` – 在轮询调度测试期间创建两个线程。每个线程在可配置的范围内搜索质数，执行可配置的次数。
