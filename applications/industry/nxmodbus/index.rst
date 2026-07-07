=========================
``nxmodbus`` NuttX Modbus
=========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NxModbus 是一个针对 NuttX RTOS 的轻量级 Modbus 协议栈实现。
它为 RTU、ASCII 和 TCP 传输提供客户端和服务器功能，具有清晰的基于回调的 API。

NxModbus 遵循 Modbus 组织的现代术语（2020 年 9 月采用）：

- **客户端**：发起请求的设备（原"主站"）
- **服务器**：处理请求并返回响应的设备（原"从站"）
- **设备**：远程 Modbus 设备（在异常代码中）

这与当前的行业标准一致，并与其他现代协议（HTTP、MQTT、OPC-UA）匹配。

NxModbus 使用 **0 基地址**。传递给应用程序回调的地址直接匹配 Modbus 线路协议：
线路上的地址 0 就是回调中的地址 0。这与 libmodbus、pymodbus 和 Modbus 应用协议规范一致。

这与 FreeModBus 不同，后者在将线路地址传递给回调之前会加 1（PLC 寄存器编号约定）。
如果从 FreeModBus 迁移，请删除回调函数中的任何 ``addr - 1`` 调整。

功能
========

- **多种传输**：RTU（串行）、ASCII（串行）、TCP 和原始 ADU
- **客户端/服务器模式**：完全支持两种角色
- **回调架构**：无内部数据存储，应用程序控制所有数据
- **条件 Termios**：支持有和没有 termios 的系统
- **线程安全**：互斥锁保护的上下文操作
- **多实例**：支持具有独立配置的并发实例
- **可扩展**：通过 ``nxmb_register_custom_fc()`` 注册自定义功能码

支持的功能码
========================

NxModbus 实现以下 Modbus 功能码：

位访问：

- **FC01** (0x01)：读取线圈
- **FC02** (0x02)：读取离散输入
- **FC05** (0x05)：写入单个线圈
- **FC15** (0x0F)：写入多个线圈

寄存器访问：

- **FC03** (0x03)：读取保持寄存器
- **FC04** (0x04)：读取输入寄存器
- **FC06** (0x06)：写入单个保持寄存器
- **FC16** (0x10)：写入多个保持寄存器
- **FC23** (0x17)：读取/写入多个保持寄存器

诊断和识别：

- **FC08** (0x08)：诊断（子功能 0x0000 返回查询数据）
- **FC17** (0x11)：报告服务器 ID

每个服务器端功能码处理器可以通过 Kconfig 单独启用或禁用（默认全部启用）。
禁用的处理器以非法功能异常响应。当启用 ``CONFIG_NXMODBUS_CLIENT`` 时，
客户端请求函数始终可用。当启用 ``CONFIG_NXMODBUS_CUSTOM_FC`` 时，
可以通过 ``nxmb_register_custom_fc()`` 注册自定义功能码。

传输模式
===============

- RTU（``CONFIG_NXMODBUS_RTU``）：
  通过串行进行二进制编码，使用 CRC16 错误检查。使用 T1.5 和 T3.5 字符定时时进行帧分隔。
  支持可配置的波特率和奇偶校验。

- ASCII（``CONFIG_NXMODBUS_ASCII``）：
  通过串行进行十六进制编码文本，使用 LRC 错误检查。帧以 ':' 开始和 CR/LF 结束标记分隔。
  字符超时可通过 ``CONFIG_NXMODBUS_ASCII_TIMEOUT_SEC`` 配置。

- TCP（``CONFIG_NXMODBUS_TCP``）：
  使用 MBAP（Modbus 应用协议）头将 Modbus 帧封装在 TCP/IP 中。默认端口 502。
  支持服务器（监听）和客户端（连接）模式。服务器模式支持多个同时客户端连接
  （通过 ``CONFIG_NXMODBUS_TCP_MAX_CLIENTS`` 配置，默认 1，最多 8）。
  需要 ``CONFIG_NET_TCP``。

- 原始 ADU（``CONFIG_NXMODBUS_RAW_ADU``）：
  应用程序提供的回调用于发送和接收原始 Modbus 帧。
  支持自定义传输后端，如 TLS、CAN、BLE 或 MQTT。

架构
============

NxModbus 使用三层架构：

1. **核心层**（``core/``）：协议逻辑、功能处理器、异常处理
2. **传输层**（``transport/``）：RTU、ASCII、TCP 和原始 ADU 实现
3. **公共 API**（``include/nxmodbus/``）：应用程序接口

传输层使用基于函数指针的抽象（``nxmb_transport_ops_s``），允许运行时选择传输模式。

配置选项
=====================

NxModbus 配置集成到 NuttX Kconfig 系统中：

角色选择：

- ``CONFIG_NXMODBUS_SERVER`` – 启用 Modbus 服务器支持
- ``CONFIG_NXMODBUS_CLIENT`` – 启用 Modbus 主站（客户端）支持

传输选择：

- ``CONFIG_NXMODBUS_RTU`` – 启用 Modbus RTU（串行）传输
- ``CONFIG_NXMODBUS_ASCII`` – 启用 Modbus ASCII（串行）传输
- ``CONFIG_NXMODBUS_TCP`` – 启用 Modbus TCP 传输（需要 ``CONFIG_NET_TCP``）
- ``CONFIG_NXMODBUS_RAW_ADU`` – 启用原始 ADU 传输（自定义后端）

功能码选择（服务器端，默认全部启用）：

- ``CONFIG_NXMODBUS_FUNC_READ_COILS`` – FC01 读取线圈
- ``CONFIG_NXMODBUS_FUNC_READ_DISCRETE`` – FC02 读取离散输入
- ``CONFIG_NXMODBUS_FUNC_READ_HOLDING`` – FC03 读取保持寄存器
- ``CONFIG_NXMODBUS_FUNC_READ_INPUT`` – FC04 读取输入寄存器
- ``CONFIG_NXMODBUS_FUNC_WRITE_COIL`` – FC05 写入单个线圈
- ``CONFIG_NXMODBUS_FUNC_WRITE_HOLDING`` – FC06 写入单个保持寄存器
- ``CONFIG_NXMODBUS_FUNC_DIAGNOSTICS`` – FC08 诊断
- ``CONFIG_NXMODBUS_FUNC_WRITE_COILS`` – FC15 写入多个线圈
- ``CONFIG_NXMODBUS_FUNC_WRITE_HOLDINGS`` – FC16 写入多个保持寄存器
- ``CONFIG_NXMODBUS_FUNC_REPORT_SERVER_ID`` – FC17 报告服务器 ID
- ``CONFIG_NXMODBUS_FUNC_READWRITE_HOLDINGS`` – FC23 读取/写入多个保持寄存器

实例和缓冲区配置：

- ``CONFIG_NXMODBUS_MAX_INSTANCES`` – 最大并发 Modbus 实例数（1-16，默认：1）
- ``CONFIG_NXMODBUS_BUFFER_SIZE`` – ADU 缓冲区大小（字节）（64-256，默认：256）

FC17 报告服务器 ID：

- ``CONFIG_NXMODBUS_REP_SERVER_ID_BUF`` – 报告服务器 ID 响应数据的缓冲区大小
  （4-253，默认：32）。保存服务器 ID、运行指示器和通过 ``nxmb_set_server_id()`` 配置的可选附加数据。

超时：

- ``CONFIG_NXMODBUS_CLIENT_TIMEOUT_MS`` – 默认客户端响应超时（毫秒）
  （100-60000，默认：1000）。可以通过 ``nxmb_set_timeout()`` 在运行时覆盖。
- ``CONFIG_NXMODBUS_TCP_MAX_CLIENTS`` – 每个服务器实例的最大同时 TCP 客户端连接数
  （1-8，默认：1）。
- ``CONFIG_NXMODBUS_TCP_TIMEOUT_SEC`` – TCP 空闲连接超时（秒）
  （1-3600，默认：60）。超过此时间无活动的连接将被关闭。
- ``CONFIG_NXMODBUS_RTU_IDLE_TIMEOUT_MS`` – RTU 帧间空闲超时（毫秒）
  （1-1000，默认：50）。等待新帧时的 ``select()`` 超时回退值。
  T3.5 字符定时时仍在活动接收期间用于帧分隔。
- ``CONFIG_NXMODBUS_ASCII_TIMEOUT_SEC`` – ASCII 模式的字符超时（秒）
  （1-60，默认：1）

串行配置（RTU/ASCII）：

- ``CONFIG_SERIAL_TERMIOS`` – 启用基于 termios 的串行配置

  如果禁用，串行端口以原始模式使用，不配置波特率或奇偶校验。
  这对于没有 termios 支持的系统或使用预配置串行设备时很有用。

可扩展性：

- ``CONFIG_NXMODBUS_CUSTOM_FC`` – 启用自定义功能码处理器注册

Termios 支持
===============

NxModbus 根据 ``CONFIG_SERIAL_TERMIOS`` 条件使用 termios 进行串行端口配置：

有 termios（``CONFIG_SERIAL_TERMIOS=y``）：

- 完整的波特率配置（9600、19200、38400、57600、115200）
- 奇偶校验配置（无、偶数、奇数）
- 自动原始模式设置（无回显、无规范模式）
- 清理时保存和恢复原始设置

无 termios（``CONFIG_SERIAL_TERMIOS=n``）：

- 串行设备以原始模式打开
- 无波特率或奇偶校验配置
- 设备必须预配置或支持原始 I/O
- 适用于：

  - 没有 termios 支持的系统
  - 预配置的串行后端
  - 自定义串行驱动程序
  - 非标准串行设备

API 参考
=============

实例管理：

- ``nxmb_create()`` – 创建并初始化 NxModbus 实例
- ``nxmb_destroy()`` – 销毁实例并释放资源
- ``nxmb_enable()`` – 启用传输并开始处理
- ``nxmb_disable()`` – 停止处理并释放传输

服务器配置：

- ``nxmb_set_callbacks()`` – 注册应用程序回调以访问数据模型
- ``nxmb_set_server_id()`` – 配置 FC17 报告服务器 ID 响应数据
- ``nxmb_poll()`` – 执行一次服务器端轮询迭代

客户端函数（需要 ``CONFIG_NXMODBUS_CLIENT``）：

- ``nxmb_read_coils()`` – 读取线圈（FC01）
- ``nxmb_read_discrete()`` – 读取离散输入（FC02）
- ``nxmb_read_holding()`` – 读取保持寄存器（FC03）
- ``nxmb_read_input()`` – 读取输入寄存器（FC04）
- ``nxmb_write_coil()`` – 写入单个线圈（FC05）
- ``nxmb_write_holding()`` – 写入单个保持寄存器（FC06）
- ``nxmb_write_coils()`` – 写入多个线圈（FC15）
- ``nxmb_write_holdings()`` – 写入多个保持寄存器（FC16）
- ``nxmb_readwrite_holdings()`` – 读取/写入多个保持寄存器（FC23）
- ``nxmb_set_timeout()`` – 设置客户端响应超时

可扩展性（需要 ``CONFIG_NXMODBUS_CUSTOM_FC``）：

- ``nxmb_register_custom_fc()`` – 注册自定义功能码处理器

异常代码
===============

NxModbus 实现标准 Modbus 异常代码：

- ``NXMB_EX_NONE`` (0x00)：无异常
- ``NXMB_EX_ILLEGAL_FUNCTION`` (0x01)：不支持的功能码
- ``NXMB_EX_ILLEGAL_DATA_ADDRESS`` (0x02)：寄存器地址超出范围
- ``NXMB_EX_ILLEGAL_DATA_VALUE`` (0x03)：无效的数据值
- ``NXMB_EX_DEVICE_FAILURE`` (0x04)：设备故障
- ``NXMB_EX_ACKNOWLEDGE`` (0x05)：请求已确认（长操作）
- ``NXMB_EX_DEVICE_BUSY`` (0x06)：设备忙
- ``NXMB_EX_MEMORY_PARITY_ERROR`` (0x08)：内存奇偶校验错误
- ``NXMB_EX_GATEWAY_PATH_FAILED`` (0x0A)：网关路径不可用
- ``NXMB_EX_GATEWAY_TGT_FAILED`` (0x0B)：网关目标未能响应

与 FreeModBus 的比较
==========================

NxModbus 是 FreeModBus 的替代方案，具有多项改进：

- 现代客户端/服务器术语
- 使用不透明句柄的更清晰 API
- 多实例支持
- 条件 termios 支持
- 设计上线程安全
- 无全局状态
- 用于自定义后端（TLS、CAN、BLE、MQTT）的原始 ADU 传输
- 通过 ``nxmb_register_custom_fc()`` 可扩展的功能码表
