===============================
``libtest`` 静态库测试
===============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本示例演示了如何创建静态库。具体步骤如下：

创建一个名为 libtest.a 的静态库，其中包含一个提供符号 library_test() 的对象。

将该库作为 EXTRA_LIB 添加到构建中::

  EXTRA_LIBS += -ltest
  EXTRA_LIBPATHS += -L$(APPDIR)/examples/libtest

此外，还可以选择性地配置为：

生成一个可以由 NSH 执行的内置命令。该命令逻辑链接了由 libtest.a 静态库提供的符号 library_test()。
