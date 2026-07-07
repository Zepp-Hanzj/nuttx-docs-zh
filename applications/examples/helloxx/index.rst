==============================
\`\`helloxx\`\` C++ 的 Hello World
==============================

这是 "Hello, World" 示例的 C++ 版本。其目的仅在于验证 C++ 编译器是否可用、基本的 C++ 库支持是否就绪，以及类是否能正确实例化。

NuttX 配置前提条件：

- ``CONFIG_HAVE_CXX`` – 启用 C++ 支持。

可选的 NuttX 配置：

- ``CONFIG_HAVE_CXXINITIALIZE`` – 启用对静态构造函数的支持（并非所有平台都可用）。

本示例特定的 NuttX 配置：

- ``CONFIG_NSH_BUILTIN_APPS`` – 将 helloxx 示例构建为可从 NSH 命令行执行的内置应用。

还需要：

- ``CONFIG_HAVE_CXX=y``

你可能还需要调整以下配置以使 libxx 正确编译：

- ``CCONFIG_ARCH_SIZET_LONG=y`` 或 ``=n``。

``new`` 运算符的参数应为 ``size_t`` 类型。但 ``size_t`` 的底层类型是不确定的。在 nuttx 的 ``sys/types.h`` 头文件中，``size_t`` 被定义为 ``uint32_t``（由架构特定的逻辑决定）。但 C++ 编译器可能认为 ``size_t`` 是不同的类型，从而导致运算符出现编译错误。使用底层整数类型代替 ``size_t`` 似乎可以解决编译问题。
