=====================================
``arch_libc`` Arch-specific libc Test
=====================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是一个针对架构特定 libc 函数的测试。架构特定的 libc 函数通常使用汇编语言实现，这里是对这些函数的测试。测试侧重于汇编语言中的关键特性，包括对齐访问、速度、被调用者保存寄存器检查等。
目前，该测试仅包含可能的架构特定 libc 函数的一个子集。欢迎贡献更多测试用例。

Options:
- ``CONFIG_TESTING_ARCH_LIBC`` – Enable the test.
- ``CONFIG_TESTING_ARCH_LIBC_XXXXX`` – Enable test for function XXXXX.
