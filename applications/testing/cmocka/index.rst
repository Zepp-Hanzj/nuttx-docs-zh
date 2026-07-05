====================
``cmocka`` libcmocka
====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

cmocka 是：
    一个优雅的 C 语言单元测试框架，支持 mock 对象。它只需要标准 C 库，
    可在多种计算平台（包括嵌入式系统）上运行，并且支持不同的编译器。

NuttX apps 中的 cmocka 应用是将 cmocka 适配到 NuttX 构建系统的版本。

您可以在 `cmocka 官方网站 <https://cmocka.org/index.html>`_ 上了解更多关于如何使用 cmocka 库的信息。

Interface Notes
---------------

cmocka 库头文件要求在它之前包含多个其他标准头文件。您的 include 语句应该如下所示：

.. code:: c

   #include <setjmp.h>
   #include <stdarg.h>
   #include <stddef.h>
   #include <stdint.h>

   #include <cmocka.h>

Build options
-------------

* ``CONFIG_TESTING_CMOCKA_PROG``: 如果启用，将在您的镜像中包含一个 `cmocka` 测试二进制文件。

* ``CONFIG_TESTING_CMOCKA_LEAKDETECT``: Cmocka 可以检查内存泄漏。预期在本地环境中使用。
