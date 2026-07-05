==========================
Sensor Monitor (procfs)
==========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
========

传感器监控器是一个动态调试工具，作为 procfs 接口实现，允许用户在
运行时监控和控制传感器日志记录。它提供了一种灵活的方式来启用/禁用
传感器调试输出，而无需重建系统，使其在生产环境中调试传感器相关
问题时特别有用。

监控器使用哈希表来存储被监控的传感器主题及其关联的日志级别，
允许高效查找和修改监控设置。

为什么需要传感器监控器？
-------------------

过去，向传感器框架添加调试信息会导致多个传感器的日志在输出中混合
在一起，使得难以定位和诊断特定问题。当启用 ``CONFIG_DEBUG_SENSORS_INFO``
时，所有传感器会同时输出调试消息，创建嘈杂的日志流，掩盖了与问题
相关的信息。

**传感器监控器通过以下方式解决此问题：**

1. **选择性监控**：允许您动态指定要监控的传感器类型，从日志输出中
   过滤掉不相关的传感器数据。

2. **运行时配置**：允许在不重新编译系统的情况下添加或删除被监控的
   传感器，消除了调试期间的重建周期。

3. **减少干扰**：通过仅监控感兴趣的传感器，日志输出变得更清晰、
   更集中，显著减少了来自其他传感器的噪声和干扰。

4. **提高调试效率**：集中日志记录使得更容易识别模式、异常和传感器
   相关问题的根本原因。

5. **精细控制**：每个被监控的传感器可以有自己独立的日志级别（0-7），
   允许对不同传感器的调试输出详细程度进行微调。这意味着您可以为一个
   启用详细的 DEBUG 级别日志，同时将另一个保持在仅 ERROR 级别，
   取决于您的调试需求。

例如，在一个同时运行加速度计、陀螺仪、磁力计、气压计和光传感器的
系统中，您可以选择仅监控加速度计并使用详细的 DEBUG 级别日志，同时
保持其他传感器静默，使跟踪加速度计特定问题变得容易，而不会被不
相关的传感器数据分散注意力。

现有工具的局限性
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

虽然 NuttX 提供了 ``apps/system/sensortest`` 和 ``apps/system/uorb``
等有用的工具用于传感器测试和监控，但这些工具在调试传感器框架时存在
局限性：

- **sensortest**：此应用程序旨在通过从用户空间读取传感器数据来
  测试传感器功能。但是，它只能观察传递给应用程序的最终输出数据。
  它无法提供对传感器框架内部操作的可见性，如数据处理、主题管理
  或订阅处理。

- **uorb**：此工具允许订阅和监控 uORB 主题，但同样在应用程序级别
  工作。它显示正在发布到主题的数据，但无法揭示框架的内部行为、
  事件传播或传感器子系统层内的数据流。

这两个工具对于验证传感器输出和应用程序级集成都很出色，但它们缺乏
调试传感器框架内部问题的能力，例如：

- 主题注册和初始化
- 数据发布和订阅流程
- 框架事件处理
- 传感器数据缓冲和排队
- 框架状态管理
- 传感器子系统内的组件间通信

**注意：** 传感器监控器专门设计用于调试传感器**框架层**。它不提供
低级硬件调试功能，如寄存器访问、中断处理或特定硬件驱动程序问题。
对于硬件级调试，请使用硬件调试器（JTAG/SWD）或驱动程序特定的
调试接口。

功能
========

- **动态配置**：在运行时添加或删除被监控的传感器
- **日志级别控制**：为不同传感器设置不同的日志级别
- **批量操作**：在单个命令中添加或删除多个传感器
- **Procfs 接口**：通过标准文件操作易于使用
- **哈希表后端**：使用 ``hsearch_r()`` 进行高效存储和查找
- **持久配置**：默认传感器列表可在构建时配置

配置
=============

要启用传感器监控器，需要以下配置选项：

.. code-block:: kconfig

   CONFIG_SENSORS_MONITOR=y                    # 启用传感器监控器
   CONFIG_SENSORS_MONITOR_BUCKET=<size>        # 哈希表桶大小
   CONFIG_SENSORS_MONITOR_LIST="<sensors>"     # 默认被监控的传感器

配置选项
---------------------

**CONFIG_SENSORS_MONITOR**
  启用传感器监控器 procfs 接口。

**CONFIG_SENSORS_MONITOR_BUCKET**
  指定用于存储被监控传感器的哈希表中的桶数量。较大的值为更多传感器
  提供更好的性能，但使用更多内存。推荐值：

  - 小型系统：16-32
  - 中型系统：64-128
  - 大型系统：256+

**CONFIG_SENSORS_MONITOR_LIST**
  包含以空格分隔的传感器名称的字符串，默认进行监控。此列表在
  初始化期间应用。

  示例::

    CONFIG_SENSORS_MONITOR_LIST="sensor_accel sensor_gyro"

用法
=====

传感器监控器通过 ``/proc/sensor_monitor`` 文件访问。

读取状态
--------------

要查看当前被监控的传感器及其日志级别：

.. code-block:: bash

   cat /proc/sensor_monitor

这将显示：

1. 使用说明
2. 命令示例
3. 当前被监控的传感器列表及其日志级别

示例输出::

  Sensor procfs - Dynamic sensor debugging tool

  Usage:
    cat /proc/sensor_monitor - Show currently monitored topics
    echo <level> <topic> > /proc/sensor_monitor - Add topic(s)
    echo rm <topic> > /proc/sensor_monitor - Remove topic(s)
    ...

  sensor_accel            1
  sensor_gyro             2
  sensor_compass          1

添加传感器
--------------

**使用默认日志级别（1）添加**

.. code-block:: bash

   echo sensor_accel > /proc/sensor_monitor

**使用特定日志级别添加**

.. code-block:: bash

   echo 2 sensor_accel > /proc/sensor_monitor

日志级别对应于 syslog 级别（0-7）：

.. list-table::
   :header-rows: 1
   :widths: 10 15 75

   * - 级别
     - 名称
     - 含义
   * - 0
     - EMERG
     - 系统当前不可用
   * - 1
     - ALERT
     - 需要立即采取行动
   * - 2
     - CRIT
     - 严重故障，但系统可能仍在运行
   * - 3
     - ERR
     - 错误状态。操作失败，但范围有限且系统保持稳定。
   * - 4
     - WARNING
     - 异常情况。发生了意外情况，但尚未失败。
   * - 5
     - NOTICE
     - 重要的正常事件。预期行为，但重要到需要记录。
   * - 6
     - INFO
     - 信息性消息。常规状态更改、进度消息、正常操作。
   * - 7
     - DEBUG
     - 调试级详细信息。面向开发人员，噪声大，不用于生产诊断。

**添加多个传感器**

.. code-block:: bash

   echo sensor_accel sensor_gyro sensor_compass > /proc/sensor_monitor
   echo 2 sensor_accel sensor_gyro > /proc/sensor_monitor

删除传感器
----------------

**删除单个传感器**

.. code-block:: bash

   echo rm sensor_accel > /proc/sensor_monitor

**删除多个传感器**

.. code-block:: bash

   echo rm sensor_accel sensor_gyro > /proc/sensor_monitor

**删除所有传感器**

.. code-block:: bash

   echo clean > /proc/sensor_monitor

批量操作
----------------

您可以在单个命令中组合添加和删除操作：

.. code-block:: bash

   echo "add 1 sensor_accel rm sensor_gyro" > /proc/sensor_monitor

此命令：

1. 以日志级别 1 添加 ``sensor_accel``
2. 删除 ``sensor_gyro``

实现细节
======================

架构
------------

传感器监控器由以下组件组成：

**Procfs 接口**
  为 ``/proc/sensor_monitor`` 实现标准文件操作（open、close、read、write）。

**哈希表存储**
  使用 POSIX ``hsearch_r()`` 系列函数存储传感器-主题映射：

  - **键**：传感器名称（字符串）
  - **值**：日志级别（以指针形式存储的整数）

**命令解析器**
  从写入操作解析以空格分隔的命令并执行相应的操作。

数据结构
---------------

**struct sensor_monitor_buffer_s**

用于在读取操作期间格式化输出：

.. code-block:: c

   struct sensor_monitor_buffer_s
   {
     FAR char *buffer;      /* 输出缓冲区指针 */
     size_t   totalsize;    /* 已写入的总字节数 */
     size_t   buflen;       /* 剩余缓冲区大小 */
     off_t    offset;       /* 当前文件偏移 */
   };

**哈希表条目**

每个被监控的传感器存储为 ``ENTRY``：

.. code-block:: c

   ENTRY item;
   item.key = "sensor_accel";           /* 传感器名称 */
   item.data = (void *)(intptr_t)1;     /* 日志级别 */

关键函数
-------------

**sensor_monitor_initialize()**

初始化传感器监控器子系统：

1. 分配并初始化哈希表
2. 设置自定义 ``free_entry`` 回调
3. 处理来自 ``CONFIG_SENSORS_MONITOR_LIST`` 的默认传感器列表
4. 注册 procfs 条目

.. code-block:: c

   int sensor_monitor_initialize(void);

**sensor_monitor_level()**

检索特定传感器的日志级别：

.. code-block:: c

   int sensor_monitor_level(FAR const char *name);

**参数：**

- ``name``：要查询的传感器名称

**返回值：**

- 如果传感器被监控，返回日志级别（0-7）
- 如果传感器未被监控，返回 ``LOG_EMERG``（0）

**使用示例：**

.. code-block:: c

   int level = sensor_monitor_level("sensor_accel");
   if (level >= LOG_INFO)
     {
       syslog(LOG_INFO, "Accel data: x=%d y=%d z=%d\n", x, y, z);
     }

**sensor_monitor_add()**

将传感器添加到监控表：

.. code-block:: c

   static int sensor_monitor_add(FAR const char *name, int level);

**参数：**

- ``name``：传感器名称
- ``level``：日志级别（0-7）

**返回值：**

- 成功时返回 ``OK``
- 分配失败时返回 ``-ENOMEM``

**行为：**

- 如果传感器已存在，更新其日志级别
- 如果传感器是新的，分配内存并添加到哈希表

**sensor_monitor_remove()**

从监控表中删除传感器：

.. code-block:: c

   static int sensor_monitor_remove(FAR const char *token);

**参数：**

- ``token``：要删除的传感器名称

**返回值：**

- 成功时返回 ``OK``
- 未找到传感器时返回 ``-ENOENT``

**sensor_monitor_clean()**

删除所有被监控的传感器：

.. code-block:: c

   static void sensor_monitor_clean(void);

销毁并重新创建哈希表，有效地清除所有条目。

**sensor_monitor_print()**

与 ``hforeach_r()`` 一起使用的回调函数，用于打印每个被监控的传感器：

.. code-block:: c

   static void sensor_monitor_print(FAR ENTRY *item, FAR void *args);

与传感器驱动程序的集成
================================

传感器驱动程序可以查询监控器以确定是否应输出调试信息：

.. code-block:: c

   #include <nuttx/sensors/sensor.h>

   void my_sensor_process_data(FAR struct sensor_data_s *data)
   {
     int level = sensor_monitor_level("sensor_accel");

     if (level >= LOG_INFO)
       {
         syslog(LOG_INFO, "Sensor data: x=%d y=%d z=%d\n",
                data->x, data->y, data->z);
       }

     if (level >= LOG_DEBUG)
       {
         syslog(LOG_DEBUG, "Detailed sensor state: ...\n");
       }
   }

这允许驱动程序：

1. 检查其传感器是否正在被监控
2. 根据配置的日志级别调整详细程度
3. 未被监控时避免不必要的日志开销

内存管理
=================

**哈希表**

哈希表在初始化期间分配并在整个系统运行期间持续存在。大小由
``CONFIG_SENSORS_MONITOR_BUCKET`` 确定。

**传感器名称**

传感器名称在添加到哈希表时使用 ``strdup()`` 动态分配。自定义
``free_entry`` 回调确保正确的清理：

.. code-block:: c

   static void sensor_monitor_free_entry(FAR ENTRY *entry)
   {
     kmm_free(entry->key);
   }

**缓冲区管理**

读取操作使用临时栈缓冲区（``NAME_MAX`` 大小）在复制到用户空间之前
格式化输出。

错误处理
==============

**写入操作错误**

- 无效的传感器名称：静默忽略（允许灵活的命令语法）
- 分配失败：返回 ``-ENOMEM``
- 未找到传感器（用于删除）：返回 ``-ENOENT``

**读取操作**

- 始终成功
- 返回帮助文本和当前监控状态

**初始化错误**

- 哈希表分配失败：返回 ``-ENOMEM``
- Procfs 注册失败：传播来自 ``procfs_register()`` 的错误

示例
========

示例 1：基本监控
----------------------------

.. code-block:: bash

   # 以默认级别启用加速度计监控
   echo sensor_accel > /proc/sensor_monitor

   # 检查状态
   cat /proc/sensor_monitor

   # 输出显示：
   # sensor_accel            1

示例 2：多传感器设置
------------------------------

.. code-block:: bash

   # 使用不同级别监控多个传感器
   echo 2 sensor_accel > /proc/sensor_monitor
   echo 3 sensor_gyro > /proc/sensor_monitor
   echo 1 sensor_compass > /proc/sensor_monitor

   # 验证
   cat /proc/sensor_monitor

示例 3：动态调整
------------------------------

.. code-block:: bash

   # 从基本监控开始
   echo sensor_accel sensor_gyro > /proc/sensor_monitor

   # 增加加速度计的详细程度
   echo 7 sensor_accel > /proc/sensor_monitor

   # 删除陀螺仪监控
   echo rm sensor_gyro > /proc/sensor_monitor

   # 添加新传感器
   echo 2 sensor_baro > /proc/sensor_monitor

示例 4：清理
------------------

.. code-block:: bash

   # 删除所有被监控的传感器
   echo clean > /proc/sensor_monitor

   # 验证为空
   cat /proc/sensor_monitor

示例 5：Goldfish 平台配置
-------------------------------------------

对于具有虚拟传感器的 Goldfish（QEMU 模拟器）平台，您需要启用
以下 KCONFIG 选项：

**基本传感器监控器配置：**

.. code-block:: kconfig

   CONFIG_SENSORS=y                             # 启用传感器框架
   CONFIG_DEBUG_SENSORS_INFO=y                  # 启用传感器调试信息（必需）
   CONFIG_FS_PROCFS=y                           # 启用 procfs 文件系统
   CONFIG_FS_PROCFS_REGISTER=y                  # 启用 procfs 注册（必需）
   CONFIG_SENSORS_MONITOR=y                     # 启用传感器监控器
   CONFIG_SENSORS_MONITOR_BUCKET=32             # 哈希表大小（根据传感器数量调整）
   CONFIG_SENSORS_MONITOR_LIST="sensor_accel sensor_gyro sensor_mag"  # 默认被监控的传感器

**Goldfish 特定传感器驱动程序：**

.. code-block:: kconfig

   CONFIG_SENSORS_GOLDFISH_SENSOR=y             # 启用 Goldfish 虚拟传感器
   CONFIG_GOLDFISH_PIPE=y                       # 启用 Goldfish pipe（通信必需）

**可选的 Goldfish GNSS 支持：**

.. code-block:: kconfig

   CONFIG_SENSORS_GNSS=y                        # 启用 GNSS 传感器支持
   CONFIG_SENSORS_GOLDFISH_GNSS=y               # 启用 Goldfish GNSS 驱动程序

**Goldfish 完整示例：**

.. code-block:: bash

   # 配置上述选项并启动系统后

   # 检查默认监控哪些传感器
   cat /proc/sensor_monitor

   # 添加更多具有不同日志级别的 Goldfish 传感器
   echo 2 sensor_baro > /proc/sensor_monitor         # 气压计（CRIT 级别）
   echo 3 sensor_light > /proc/sensor_monitor        # 光传感器（ERR 级别）
   echo 1 sensor_proximity > /proc/sensor_monitor    # 接近（ALERT 级别）
   echo 7 sensor_temp > /proc/sensor_monitor         # 温度（DEBUG 级别）

   # 监控方向和铰链传感器（用于可折叠设备模拟）
   echo 2 sensor_orient > /proc/sensor_monitor
   echo 2 sensor_hinge0 > /proc/sensor_monitor

   # 验证所有被监控的传感器
   cat /proc/sensor_monitor

**注意事项：**

- ``CONFIG_DEBUG_SENSORS_INFO`` 和 ``CONFIG_FS_PROCFS_REGISTER`` 是
  ``CONFIG_SENSORS_MONITOR`` 的强制依赖项
- ``CONFIG_SENSORS_MONITOR_BUCKET`` 应至少为您计划同时监控的传感器
  数量的一半（例如，对于最多 64 个传感器，设置为 32）
- ``CONFIG_SENSORS_MONITOR_LIST`` 可以指定在启动时监控的默认传感器
  集合，对于调试启动问题很有用
- Goldfish 传感器通过 Goldfish pipe 机制通信，因此需要
  ``CONFIG_GOLDFISH_PIPE=y``

最佳实践
==============

1. **使用适当的日志级别**

   - 对于错误和关键事件使用较低级别（0-3）
   - 对于详细调试使用较高级别（4-7）
   - 默认级别 1 适用于基本监控

2. **传感器命名约定**

   - 使用与驱动程序名称匹配的描述性名称
   - 常见前缀：``sensor_``
   - 示例：``sensor_accel``、``sensor_gyro_0``、``sensor_temp_cpu``

3. **性能注意事项**

   - 为您的传感器数量配置足够的桶大小
   - 经验法则：桶数 ≥ 传感器数 / 2
   - 避免在中断上下文中过度日志记录

4. **生产使用**

   - 为关键传感器设置 ``CONFIG_SENSORS_MONITOR_LIST``
   - 使用 procfs 在出现问题时启用额外调试
   - 调试后清理以减少开销

5. **驱动程序集成**

   - 在执行昂贵操作前始终检查监控器级别
   - 使用与监控器级别匹配的适当 syslog 级别
   - 考虑频繁查找的性能影响

限制
===========

1. **名称长度**：传感器名称限制为 ``NAME_MAX`` 个字符
2. **内存**：每个被监控的传感器需要内存用于：

   - 哈希表条目
   - 复制的传感器名称字符串
   - 哈希表开销

3. **并发性**：当前实现中没有显式锁定
   （依赖于内核互斥）

4. **持久性**：监控配置在重启后丢失
   （来自 ``CONFIG_SENSORS_MONITOR_LIST`` 的默认列表除外）

另请参阅
========

- :doc:`sensors_uorb` - 主传感器框架文档
- ``nuttx/include/nuttx/sensors/sensor.h`` - 传感器头文件
- ``nuttx/drivers/sensors/sensor_monitor.c`` - 实现
- ``drivers/fs/procfs/`` - Procfs 文件系统实现
