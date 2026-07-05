===================================
``fstest`` Generic file system test
===================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是一个通用的文件系统测试，源自 ``testing/nxffs``。它最初是为了测试 tmpfs 文件系统而创建的，但应该适用于任何文件系统，前提是所有初始化工作已在启动测试之前完成。

该测试适用于任何文件系统的通用测试，但包含一些针对 SPIFFS 文件系统的特定钩子。

- ``CONFIG_TESTING_FSTEST`` – 启用文件系统示例。
- ``CONFIG_TESTING_FSTEST_MAXNAME`` – 确定文件系统中使用的名称的最大大小。
- ``CONFIG_TESTING_FSTEST_MAXFILE`` – 确定文件的最大大小。
- ``CONFIG_TESTING_FSTEST_MAXIO`` – 最大 I/O，默认 ``347``。
- ``CONFIG_TESTING_FSTEST_MAXOPEN`` – 最大打开文件数。
- ``CONFIG_TESTING_FSTEST_MOUNTPT`` – 文件系统的挂载路径。
- ``CONFIG_TESTING_FSTEST_NLOOPS`` – 测试循环次数，默认 ``100``。
- ``CONFIG_TESTING_FSTEST_VERBOSE`` – 详细输出。

EXAMPLE::

  fstest -m /mnt -n 10 – Test /mnt 10 times
  fstest -h            – Get help message
  fstest               – Test path define by `CONFIG_TESTING_FSTEST_MOUNTPT`
                         `CONFIG_TESTING_FSTEST_NLOOPS` times

