================================
\`\`i2cchar\`\` I2C 传输
================================

一个极其简单的 I2C 驱动测试。它以尽可能快的速度向 I2C 发送器和/或接收器读写垃圾数据。

本测试依赖以下特定的 I2S/AUDIO/NSH 配置（你的 I2S 设置可能需要额外的配置）。

- ``CONFIG_I2S`` – 启用 I2S 支持。
- ``CONFIG_AUDIO`` – 启用音频支持。
- ``CONFIG_DRIVERS_AUDIO`` – 启用音频设备支持。
- ``CONFIG_AUDIO_I2SCHAR`` – 启用 I2S 字符设备支持。
- ``CONFIG_NSH_BUILTIN_APPS`` – 将 I2S 测试构建为 NSH 内置函数。默认：构建为独立程序。

本示例的特定配置选项包括：

- ``CONFIG_EXAMPLES_I2SCHAR`` – 启用 I2C 测试。

- ``CONFIG_EXAMPLES_I2SCHAR_DEVPATH`` – ADC 设备的默认路径。默认值：``/dev/i2schar0``。

- ``CONFIG_EXAMPLES_I2SCHAR_TX`` – 如果 I2S 设备支持发送器，应设置此项。

- ``CONFIG_EXAMPLES_I2SCHAR_TXBUFFERS`` – TX 传输终止前要发送的默认音频缓冲区数量。当 TX 和 RX 传输都终止时，任务退出（如果是 NSH 内置应用，``i2schar`` 命令返回）。此数值可从 NSH 命令行修改。

- ``CONFIG_EXAMPLES_I2SCHAR_TXSTACKSIZE`` – 启动发送线程时使用的栈大小。默认值：``1536``。

- ``CONFIG_EXAMPLES_I2SCHAR_RX`` – 如果 I2S 设备支持接收器，应设置此项。

- ``CONFIG_EXAMPLES_I2SCHAR_RXBUFFERS`` – RX 传输终止前要接收的默认音频缓冲区数量。当 TX 和 RX 传输都终止时，任务退出（如果是 NSH 内置应用，``i2schar`` 命令返回）。此数值可从 NSH 命令行修改。

- ``CONFIG_EXAMPLES_I2SCHAR_RXSTACKSIZE`` – 启动接收线程时使用的栈大小。默认值：``1536``。

- ``CONFIG_EXAMPLES_I2SCHAR_BUFSIZE`` – 单个音频缓冲区中数据负载的大小。适用于 TX 和 RX 音频缓冲区。

- ``CONFIG_EXAMPLES_I2SCHAR_DEVINIT`` – 如果架构特定的 I2S 设备初始化可用，则定义此项。如果定义了，平台特定代码必须提供 ``i2schar_devinit()`` 函数，每次执行此测试时都会调用该函数。在内核构建模式下不可用。
