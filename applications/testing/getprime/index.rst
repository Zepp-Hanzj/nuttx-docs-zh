======================
``getprime`` benchmark
======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此应用程序用于通过多线程进行处理时间基准测试。每个生成的线程将在 1 到 10,000 的范围内查找所有质数。

要使用 ``getprime``，将您希望运行的线程数作为唯一参数传递。线程完成处理后，测试的持续时间将打印到控制台。

.. code:: console

   nsh> getprime 3
   Set thread priority to 10
   Set thread policy to SCHED_RR
   Start thread #0
   Start thread #1
   Start thread #2
   thread #0 started, looking for primes < 10000, doing 10 run(s)
   thread #1 started, looking for primes < 10000, doing 10 run(s)
   thread #2 started, looking for primes < 10000, doing 10 run(s)
   thread #0 finished, found 1230 primes, last one was 9973
   thread #1 finished, found 1230 primes, last one was 9973
   thread #2 finished, found 1230 primes, last one was 9973
   Done
   getprime took 89040 msec

该程序可用于观察不同开发板、单核与 SMP、线程调度设置等之间的性能差异。
