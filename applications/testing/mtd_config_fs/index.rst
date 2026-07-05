=========================================
``mtd_nvs`` MTD non-volatile storage Test
=========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 MTD 非易失性存储的测试。MTD 非易失性存储最初由 Laczen 在 Zephyr 中实现。我们对原始设计进行了几处修改。这些修改的主要目的是：

1. 在 nvs API 中支持 C 字符串键（原始设计仅支持 uint16_t 作为键）
2. 同时通过限制 flash 读取次数来获得更好的性能（理论上优于基于原始 NVS 的 Zephyr subsys/settings）。

Options:
- ``CONFIG_TESTING_FAILSAFE_MTD_CONFIG`` – Enable the test.
- ``CONFIG_TESTING_FAILSAFE_MTD_CONFIG_VERBOSE`` – Verbose output.

EXAMPLE::
  mtdconfig_fs_test -m /dev/config  – Test MTD NVS on /dev/config
  mtdconfig_fs_test -h              – Get help message
