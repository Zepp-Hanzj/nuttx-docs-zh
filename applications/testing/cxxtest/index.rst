============================
``cxxtest`` C++ test program
============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是对 C++ 标准库的测试。目前已有 uClibc++ C++ 库的移植版本。由于许可问题，uClibc++ C++ 库默认不包含在 NuttX 源代码树中，必须手动安装（有关安装说明，请参见 uClibc++ 下载包中的 ``README.txt`` 文件）。

uClibc++ 测试包括以下简单测试：

- iostreams（输入输出流）
- STL（标准模板库）
- RTTI（运行时类型识别）
- Exceptions（异常）

### Example Configuration Options

- ``CONFIG_TESTING_CXXTEST=y`` – 启用此示例

### Other Required Configuration Settings

其他必需的 NuttX 配置包括：

- ``CONFIG_HAVE_CXX=y``
- ``CONFIG_HAVE_CXXINITIALIZE=y``
- ``CONFIG_UCLIBCXX=y`` 或 ``CONFIG_LIBCXX=y``

您的构建环境中可能还需要额外的 ``uClibc++/libcxx`` 设置。
