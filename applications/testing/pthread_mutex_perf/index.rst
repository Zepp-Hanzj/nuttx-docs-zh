=======
Testing
=======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``pthread_mutex_perf`` 是一个简单的性能测试，用于验证某些特定的内核修改是否影响了 pthread_mutex_trylock()。

基本上，该测试将运行 1000000 次忙等待尝试获取已锁定的互斥锁。然后计算总时间和平均时间，重复此周期 10 次。

此测试不旨在确认 pthread mutex 是否正常工作，对于这一点最好使用 ostest。其目标是验证内核中可能被认为是回归的影响。

