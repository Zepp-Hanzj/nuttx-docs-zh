==================
I3C 设备驱动
==================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

I3C（改进型集成电路总线）驱动是一个综合性的软件框架，旨在支持 I3C 协议的高级特性。它包括系统框架和底层 IP 驱动，两者都是实现 I3C 设备之间无缝通信的关键组件。系统框架由 Vela OS 提供，提供用户级设备节点和内核级驱动接口。同时，专门为 I3C 驱动框架开发的底层 IP 驱动处理 IP 功能的实现和框架级接口的适配。

- I3C 驱动框架的关键组件：

 #. **动态寻址和访问**：I3C 相对于 I2C 的主要改进之一是支持动态寻址。这允许更灵活的设备管理和寻址方案。
 #. **CCC（通用命令码）支持**：I3C 驱动框架支持 CCC 命令的传输，扩展了 I3C 设备的功能和能力。动态地址分配和释放命令是必需的，而其他 CCC 命令是可选的，可根据需要实现。
 #. **数据传输**：框架支持 I3C 和 I2C 设备数据传输，确保与现有 I2C 设备的兼容性，同时利用 I3C 的增强功能。
 #. **接口回调**：I3C 驱动框架提供了一组回调接口，使 IP 驱动能与框架层交互。这些接口包括动态地址配置和释放、CCC 命令传输、I3C 设备数据传输和 I2C 设备数据传输的接口。

- 数据结构和接口：

 #. **I3C 主控制器 (struct i3c_master_controller)**：表示 I3C 控制器并管理 I3C 总线的基本软件信息。
 #. **I3C 总线操作回调 (struct i3c_master_controller_ops)**：使应用程序级能访问 I3C 进行数据传输和其他操作。关键函数包括用于总线初始化的 bus_init、用于设备附加的 attach_i3c_dev 和 attach_i2c_dev、用于 CCC 命令传输的 ccc_xfer、用于私有数据传输的 priv_xfers 以及用于 I2C 设备数据传输的 i2c_xfers。
 #. **I2C 和 I3C 传输的数据结构**：分别为传输到 I2C 和 I3C 设备的数据定义了单独的结构 (struct i2c_msg_s 和 struct i3c_priv_xfer)。
 #. **CCC 命令传输 (struct i3c_ccc_cmd)**：用于封装传输到 I3C 设备的 CCC 命令的专用结构。

- I3C 的应用使用

应用程序通过设备节点（I3C 设备为 /dev/i3cX，I2C 设备为 /dev/i2cX，其中 X 表示特定的总线编号）与 I3C 设备交互。支持标准文件操作，如 open、close、read、write 和 ioctl。

- IOCTL 命令：

  #. 对于 I2C 设备，可用的 IOCTL 命令包括 I2C_TRANSFER 和 I2C_RESET，允许应用程序传输数据和重置 I2C 设备。
  #. 对于 I3C 设备，提供了一系列 IOCTL 命令，包括用于数据传输的 I3CIOC_PRIV_XFERS、用于启用和禁用 IBI（带内中断）命令的 I3CIOC_EN_IBI 和 I3CIOC_DIS_IBI、用于请求和释放 IBI 命令的 I3CIOC_REQ_IBI 和 I3CIOC_FREE_IBI 以及用于检索设备信息的 I3CIOC_GET_DEVINFO。

- 数据传输格式：

当向 I3C 从设备传输数据时，应用程序必须将其数据封装在 struct i3c_transfer_s 格式中。此结构包括目标地址 (target_addr)、要传输的数据帧数量 (nxfers)、数据帧格式 (xfers) 以及用于 IBI 操作请求和设备信息检索的附加字段。

- 临时 ID 实现：

由于 I3C 中使用动态寻址，设备可以使用临时 ID (PID) 来标识。这些 PID 编码在 boardinfo 结构的 reg[3] 数组中，制造商 ID、部件 ID、实例 ID 和附加信息的编码有特定规则。此编码方案确保 I3C 设备的唯一可识别性，即使在静态寻址不可用时也是如此。
