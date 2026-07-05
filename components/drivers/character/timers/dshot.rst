=============
DShot 驱动程序
=============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

DShot（Digital Shot）是一种数字通信协议，主要用于在无人机、多旋翼飞行器和其他机器人系统中控制无刷电机电子调速器（ESC）。与传统的基于 PWM 的协议不同，DShot 提供更稳健和更快的数字通信，并支持可选的双向遥测功能。

NuttX DShot 驱动程序分为两部分：

#. "上半部分"，通用驱动程序，为应用程序代码提供通用 DShot 接口，处理数据包编码/解码、遥测解析，并管理字符设备接口。
#. "下半部分"，平台特定的驱动程序，实现底层硬件控制以生成 DShot 信号时序，并可选地捕获遥测响应。

支持 DShot 的文件可以在以下位置找到：

- **接口定义**：NuttX DShot 驱动程序的头文件位于 ``include/nuttx/timers/dshot.h``。此头文件包含 DShot 驱动程序的应用程序级别接口以及"上半部分"和"下半部分"驱动程序之间的接口。
- **"上半部分"驱动程序**：通用的"上半部分" DShot 驱动程序位于 ``drivers/timers/dshot.c``。
- **"下半部分"驱动程序**：平台特定的 DShot 驱动程序位于 ``arch/<architecture>/src/<hardware>`` 目录，针对特定处理器 ``<architecture>`` 和特定 ``<chip>`` 外设设备。例如，基于 i.MX9 FlexIO 的实现位于 ``arch/arm64/src/imx9/imx9_flexio_dshot.c``。

DShot 协议概述
=======================

DShot 协议以固定比特率传输 16 位帧。每帧由以下部分组成：

- **11 位**：油门值（0-2047）或特殊命令
- **1 位**：遥测请求标志
- **4 位**：CRC 校验和

支持的比特率（速度）：

- **DShot150**：150 kbit/s
- **DShot300**：300 kbit/s
- **DShot600**：600 kbit/s（最常用）
- **DShot1200**：1200 kbit/s
- **DShot2400**：2400 kbit/s（实验性）
- **DShot3600**：3600 kbit/s（实验性）

双向 DShot
-------------------

双向 DShot 允许 ESC 在用于命令的同一信号线上将遥测数据发送回控制器。遥测数据包括：

- **eRPM**：电机的电气转速
- **扩展遥测**：温度、电压、电流、调试值等

当启用双向模式时，命令数据包中的 CRC 被取反，ESC 在命令后响应一个 GCR 编码的遥测帧。

应用程序级别接口
============================

要在应用程序中使用 DShot 驱动程序，请包含头文件：

.. code-block:: c

   #include <nuttx/timers/dshot.h>

DShot 驱动程序注册为 ``/dev`` 命名空间中的 POSIX 字符设备文件。打开设备以获取文件描述符进行操作：

.. code-block:: c

   int fd = open("/dev/dshot0", O_RDWR);
   if (fd < 0)
     {
       /* 处理错误 */
     }

配置
-------------

在发送命令之前，使用所需的速度、遥测频率、活动通道和双向模式配置 DShot 实例：

.. code-block:: c

   struct dshot_config_s config;

   config.freq = DSHOT_SPEED_600;      /* 600 kbit/s */
   config.telem_freq = 750000;         /* 标准 ESC 为 1.25 * freq */
   config.active_mask = 0x0F;          /* 启用通道 0-3 */
   config.bidir = true;                /* 启用双向遥测 */

   int ret = ioctl(fd, DSHOTIOC_CONFIGURE, (unsigned long)&config);
   if (ret < 0)
     {
       /* 处理错误 */
     }

``telem_freq`` 通常应设置为比特率频率的 1.25 倍。但是，某些 ESC（例如 T-motor F55A）可能需要不同的值，如比特率的 1.15 倍。

设置油门
----------------

向一个或多个通道发送油门值或特殊命令：

.. code-block:: c

   struct dshot_throttle_s throttle;

   memset(&throttle, 0, sizeof(throttle));

   /* 设置通道 0-3 的油门值 */
   throttle.throttle[0] = 1000;  /* 油门范围：48-2047（解锁） */
   throttle.throttle[1] = 1000;  /*                 0 = 解锁 */
   throttle.throttle[2] = 1000;  /*                 1-47 = 特殊命令 */
   throttle.throttle[3] = 1000;
   throttle.ch_mask = 0x0F;      /* 更新通道 0-3 */
   throttle.telemetry_req = 0x01; /* 请求通道 0 的遥测 */

   ret = ioctl(fd, DSHOTIOC_SET_THROTTLE, (unsigned long)&throttle);
   if (ret < 0)
     {
       /* 处理错误 */
     }

特殊命令
----------------

DShot 支持用于 ESC 控制和配置的特殊命令。这些命令使用油门值 0-47：

.. code-block:: c

   struct dshot_throttle_s cmd;

   memset(&cmd, 0, sizeof(cmd));

   /* 向通道 0 发送蜂鸣命令 */
   cmd.throttle[0] = DSHOT_CMD_BEEP1;
   cmd.ch_mask = 0x01;

   /* 命令应多次发送（通常 10 次） */
   for (int i = 0; i < 10; i++)
     {
       ioctl(fd, DSHOTIOC_SET_THROTTLE, (unsigned long)&cmd);
       usleep(1000); /* 命令之间的短延迟 */
     }

常用特殊命令：

- ``DSHOT_CMD_MOTOR_STOP`` (0)：解除电机武装
- ``DSHOT_CMD_BEEP1`` 到 ``DSHOT_CMD_BEEP5`` (1-5)：音频提示音
- ``DSHOT_CMD_ESC_INFO`` (6)：请求 ESC 信息
- ``DSHOT_CMD_SPIN_DIRECTION_NORMAL`` (20)：正向旋转
- ``DSHOT_CMD_SPIN_DIRECTION_REVERSED`` (21)：反向旋转
- ``DSHOT_CMD_SIGNAL_LINE_TELEMETRY_ENABLE`` (33)：启用遥测
- ``DSHOT_CMD_SIGNAL_LINE_CONTINUOUS_ERPM_TELEMETRY`` (34)：连续 eRPM

读取遥测
-----------------

当启用双向模式时，从 ESC 检索遥测数据：

.. code-block:: c

   struct dshot_telemetry_s telem;

   telem.ch_mask = 0x0F; /* 从通道 0-3 读取遥测 */

   ret = ioctl(fd, DSHOTIOC_GET_TELEMETRY, (unsigned long)&telem);
   if (ret < 0)
     {
       /* 处理错误 */
     }

   /* 处理每个通道的遥测数据 */
   for (int i = 0; i < 4; i++)
     {
       printf("Channel %d:\n", i);
       printf("  eRPM: %u\n", telem.ch_telemetry[i].erpm);
       printf("  EDT Type: 0x%02x\n", telem.ch_telemetry[i].edt_type);
       printf("  EDT Value: %u\n", telem.ch_telemetry[i].edt_value);
     }

遥测结构体还包括时间戳，指示从每个 ESC 接收到最后一个有效响应的时间。

高效遥测处理
-----------------------------

为了高效操作，``DSHOTIOC_SET_THROTTLE`` ioctl 可以在单次调用中同时发送命令和检索之前的遥测响应：

.. code-block:: c

   struct dshot_throttle_s throttle;

   memset(&throttle, 0, sizeof(throttle));
   throttle.throttle[0] = 1000;
   throttle.ch_mask = 0x01;
   throttle.telemetry_req = 0x01; /* 请求遥测 */

   ret = ioctl(fd, DSHOTIOC_SET_THROTTLE, (unsigned long)&throttle);

   /* 之前的遥测现在可在 throttle.ch_telemetry[] 中获取 */
   printf("Previous eRPM: %u\n", throttle.ch_telemetry[0].erpm);

配置选项
=====================

以下配置选项控制 DShot 驱动程序行为：

- ``CONFIG_DSHOT``：启用 DShot 驱动程序支持
- ``CONFIG_DSHOT_NCHANNELS``：DShot 通道的最大数量（默认：8，最大：16）

.. note::

   除了这些通用 DShot 选项外，您还必须启用和配置架构特定的下半部分驱动程序。例如，在 i.MX9 上：

   - ``CONFIG_IMX9_FLEXIO_DSHOT``：启用基于 FlexIO 的 DShot 驱动程序
   - ``CONFIG_IMX9_FLEXIO_DSHOT_CHANNEL_COUNT``：硬件通道数量

   请参考您平台的 Kconfig 选项以获取特定的下半部分设置。

``defconfig`` 中的示例配置：

.. code-block:: text

   CONFIG_DSHOT=y
   CONFIG_DSHOT_NCHANNELS=8

   # 平台特定（i.MX9 示例）
   CONFIG_IMX9_FLEXIO_DSHOT=y
   CONFIG_IMX9_FLEXIO_DSHOT_CHANNEL_COUNT=8

下半部分驱动程序接口
============================

下半部分驱动程序必须实现 ``struct dshot_ops_s`` 中定义的操作：

.. code-block:: c

   struct dshot_ops_s
   {
     CODE int (*setup)(FAR struct dshot_lowerhalf_s *dev);
     CODE int (*shutdown)(FAR struct dshot_lowerhalf_s *dev);
     CODE int (*configure)(FAR struct dshot_lowerhalf_s *dev,
                           FAR const struct dshot_config_s *cfg);
     CODE int (*send_command)(FAR struct dshot_lowerhalf_s *dev,
                              FAR const uint16_t *packets,
                              uint16_t ch_mask);
     CODE int (*get_raw_telemetry)(FAR struct dshot_lowerhalf_s *dev,
                                   FAR struct dshot_raw_telemetry_s *raw,
                                   uint16_t ch_mask);
     CODE int (*ioctl)(FAR struct dshot_lowerhalf_s *dev,
                       int cmd, unsigned long arg);
   };

操作描述
----------------------

**setup**
  当设备被打开时调用。初始化硬件并分配资源。

**shutdown**
  当设备被关闭时调用。停止输出并释放硬件资源。

**configure**
  配置 DShot 速度（比特率）、遥测捕获频率、活动通道掩码和双向模式。下半部分驱动程序应相应地重新配置定时器/外设。

**send_command**
  向指定通道传输 DShot 数据包。``packets`` 数组包含预编码的 16 位 DShot 帧（包括 CRC），``ch_mask`` 指示要更新哪些通道。

**get_raw_telemetry**
  检索从 ESC 响应捕获的原始 GCR 编码遥测数据。上半部分将把这些解码为人类可读的值。

**ioctl**（可选）
  处理标准接口未涵盖的平台特定 ioctl 命令。

注册下半部分驱动程序
--------------------------------

下半部分驱动程序使用以下方式向上半部分注册：

.. code-block:: c

   int dshot_register(FAR const char *path, FAR struct dshot_lowerhalf_s *dev);

板初始化代码示例：

.. code-block:: c

   /* 初始化平台特定的 DShot 硬件 */
   FAR struct dshot_lowerhalf_s *dshot = imx9_dshot_initialize();
   if (dshot == NULL)
     {
       return -ENODEV;
     }

   /* 向上半部分注册 */
   ret = dshot_register("/dev/dshot0", dshot);
   if (ret < 0)
     {
       return ret;
     }

实现注意事项
==============================

时序要求
-------------------

DShot 需要精确的时序。对于 DShot600：

- 位周期：1.67 μs
- 逻辑 '1'：~1.25 μs 高电平，~0.42 μs 低电平（75% 占空比）
- 逻辑 '0'：~0.63 μs 高电平，~1.04 μs 低电平（37.5% 占空比）

下半部分实现通常使用硬件定时器（PWM/DMA）或 FlexIO 等专用外设来生成精确的波形。

遥测捕获
-----------------

双向遥测要求信号线在发送命令后从输出模式切换到输入模式。ESC 在命令后约 30-40 μs 响应一个 21 位 GCR 编码帧。精确捕获需要：

- 快速引脚方向切换
- 精确的边沿时序测量
- GCR 解码和 CRC 验证（由上半部分处理）

多通道支持
---------------------

对于多通道系统，需要考虑：

- 跨通道同步输出（对电机控制很重要）
- 高效使用 DMA 以减少 CPU 开销
- 同时遥测捕获的缓冲区管理

最佳实践
==============

1. **初始化序列**

   - 等待 ESC 初始化（上电后通常 3-5 秒）
   - 在尝试发送命令之前配置 DShot
   - 初始化后发送 ``DSHOT_CMD_MOTOR_STOP`` 以确保电机已解除武装

2. **命令重复**

   特殊命令应多次发送（通常 6-10 次重复）以确保可靠接收。

3. **遥测轮询**

   **双向模式**：在每个命令周期请求遥测是正常且预期的。遥测响应在命令后立即在同一信号线上接收。

   **非双向模式**（专用 UART 遥测）：考虑 UART 线路能力和响应数据包的时序。将 UART 接收与 DShot 命令传输分开处理。

4. **错误处理**

   监控遥测时间戳以检测 ESC 通信故障。过时的遥测可能表示信号完整性问题。

5. **安全**

   在关闭设备或紧急情况下，始终发送 ``DSHOT_CMD_MOTOR_STOP``（油门值 0）。

示例应用程序
===================

DShot 电机控制的完整示例：

.. code-block:: c

   #include <nuttx/config.h>

   #include <fcntl.h>
   #include <stdio.h>
   #include <string.h>
   #include <unistd.h>

   #include <nuttx/timers/dshot.h>

   /****************************************************************************
    * 公共函数
    ****************************************************************************/

   int main(int argc, FAR char *argv[])
   {
     struct dshot_config_s config;
     struct dshot_throttle_s throttle;
     int fd;
     int ret;
     int i;

     /* 打开 DShot 设备 */

     fd = open("/dev/dshot0", O_RDWR);
     if (fd < 0)
       {
         fprintf(stderr, "Failed to open DShot device\n");
         return -1;
       }

     /* 配置 DShot600 并启用双向遥测 */

     config.freq        = DSHOT_SPEED_600;
     config.telem_freq  = 750000;
     config.active_mask = 0x0f;  /* 4 个电机 */
     config.bidir       = true;

     ret = ioctl(fd, DSHOTIOC_CONFIGURE, (unsigned long)&config);
     if (ret < 0)
       {
         fprintf(stderr, "Configuration failed\n");
         close(fd);
         return -1;
       }

     /* 武装 ESC - 发送零油门 */

     memset(&throttle, 0, sizeof(throttle));
     throttle.ch_mask = 0x0f;

     for (i = 0; i < 100; i++)
       {
         ioctl(fd, DSHOTIOC_SET_THROTTLE, (unsigned long)&throttle);
         usleep(10000);
       }

     /* 逐渐增加油门 */

     for (i = 48; i <= 1000; i += 10)
       {
         throttle.throttle[0]   = i;
         throttle.throttle[1]   = i;
         throttle.throttle[2]   = i;
         throttle.throttle[3]   = i;
         throttle.telemetry_req = 0x01;

         ret = ioctl(fd, DSHOTIOC_SET_THROTTLE, (unsigned long)&throttle);
         if (ret == 0 && throttle.ch_telemetry[0].erpm > 0)
           {
             printf("Throttle: %d, eRPM: %u\n", i,
                    throttle.ch_telemetry[0].erpm);
           }

         usleep(20000);
       }

     /* 停止电机 */

     memset(&throttle, 0, sizeof(throttle));
     throttle.ch_mask = 0x0f;
     ioctl(fd, DSHOTIOC_SET_THROTTLE, (unsigned long)&throttle);

     close(fd);
     return 0;
   }

参考
==========

- DShot 协议规范：https://github.com/betaflight/betaflight/wiki/DShot
- ESC 遥测协议：https://github.com/bird-sanctuary/extended-dshot-telemetry
- DShot 和双向 DShot：https://brushlesswhoop.com/dshot-and-bidirectional-dshot/
