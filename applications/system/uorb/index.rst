.. _uorb:

==========================================
``uorb`` uorb（微对象请求代理）
==========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``uORB（微对象请求代理）`` 是开源飞行控制系统 PX4 中的关键中间件。它是一个基于发布-订阅模式的消息总线，主要负责多个模块之间的数据传输。基于无锁设计理念，uORB 内部通过共享内存实现任务间的进程间通信（IPC），并以最优的内存占用实现低延迟数据交换。其不依赖于线程或工作队列。

与 uORB 相关的主要概念包括 ``角色`` 和 ``设备节点``。

**角色**
^^^^^^^^^

在 uORB 总线中，有两个角色：订阅者和发布者。传输的内容称为主题消息，由其元数据（meta）描述，包括名称、大小等。

每个主题支持多个实例，发布者的频率为采样率（interval），最大发布延迟为批量延迟。

例如，如果加速度计传感器的采样率为 50Hz，最大发布延迟为 100ms，则硬件每 100ms 生成一次中断，每次发布 5 个数据点（100/(1000/50)）。

**两种类型**
^^^^^^^^^^^^^

此外，NuttX 将主题分为两种类型：**通知** 主题和 **通用** 主题。

**通知** 主题的订阅者不关心发布者的存在或是否已发生发布；他们直接获取当前状态。当应用程序订阅时，它直接从当前设备节点获取最新数据作为当前状态。

**通用** 主题的订阅者不关心过去的状态；他们获取的数据必须是当前或未来的事件。例如，对于加速度计传感器，应用程序只关心传感器下一次数据就绪中断报告的数据，而不是过去时刻的数据。

要发布 **通知** 主题消息，使用带 **persist** 后缀的 API 进行主题发布，订阅者行为与 **通用** 主题一致。

**设备节点**
^^^^^^^^^^^^^^^^

每个被发布或订阅的主题对应一个字符设备节点，订阅者和发布者通过内部循环缓冲区共享数据。在实现中，以 O_WRONLY 模式打开设备节点的调用者被视为发布者，以 O_RDONLY 模式打开的被视为订阅者。

发布者向节点写入以发布数据，订阅者从节点读取以订阅数据。双方都可以使用 poll 监控节点以接收感兴趣的事件。发布者和订阅者对设备节点的控制通过 ioctl 操作实现。

**代码位置**
^^^^^^^^^^^^^^^^^

目录 apps/system/uorb 包含 uORB 封装器、单元测试、物理传感器主题定义和 uorb_listener 工具。

::

  ├── Kconfig
  ├── listener.c   // Implementation of uorb_listener.c
  ├── Make.defs
  ├── Makefile
  ├── sensor       // Definitions for physical sensor topics
  │   ├── accel.c
  │   ├── accel.h
  │   ├── baro.c
  │   ├── baro.h
  │   ├── cap.c
  │   ├── cap.h
  │   ├── ...c
  │   ├── tvoc.c
  │   ├── tvoc.h
  │   ├── uv.c
  │   └── uv.h
  ├── test
  │   ├── unit_test.c   // Unit tests for uORB
  │   ├── utility.c
  │   └── utility.h
  └── uORB
      ├── uORB.c   // Implementation of uORB wrapper
      └── uORB.h

**关键数据结构介绍**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

每个 uORB 主题对应一个 ``struct orb_metadata`` 结构体，用于描述主题的元数据，包括名称 o_name、消息大小 o_size 和调试格式指针 o_format。

::

  struct orb_metadata
  {
    FAR const char   *o_name;       // Name of the topic
    uint16_t          o_size;       // Size of the message
    #ifdef CONFIG_DEBUG_UORB
    FAR const char   *o_format;     //  Format string used for structure input and output
    #endif
  };

::

  typedef FAR const struct orb_metadata *orb_id_t; // Pointer to orb_metadata as an identifier for uORB topics

在发布或订阅每个 uORB 主题后，调用者可以通过调用 orb_get_state 获取主题状态，包括当前最大发布频率 max_frequency、最小批量间隔 min_batch_interval、内部循环队列长度 queue_size、订阅者数量 nsubscribers 和主线程的代数索引 generation。

::

  struct orb_state              
  {                             
    uint32_t max_frequency;     // Maximum publication frequency
    uint32_t min_batch_interval;// Minimum batch interval
    uint32_t queue_size;        // Length of the internal circular queue
    uint32_t nsubscribers;      // Number of subscribers
    uint64_t generation;        // Generation index for the main thread
  };

uORB 支持将主题实例化为多个实体，每个实体有对应的实例号，从 0 开始递增。struct orb_object 包含一个实体的信息：其元数据 meta 和实例号 instance。

::

  struct orb_object
  {
    orb_id_t meta;      // Pointer to the metadata of the topic
    int      instance;  // Instance number of the topic entity
  };

**主题定义**
^^^^^^^^^^^^^^^^^^^^

PX4 中定义了大量 uORB 主题，详见 https://docs.px4.io/main/en/middleware/uorb_graph.html。

定义新主题涉及创建主题的数据结构、声明主题元数据的全局变量，以及可选地定义主题数据的调试输出函数。定义过程中常用三个宏：

``ORB_ID``：用于获取主题的全局元数据句柄。

``ORB_DECLARE``：用于声明主题的全局元数据。

``ORB_DEFINE``：用于定义主题的全局元数据。

**API 描述**
^^^^^^^^^^^^^^^^^^^

uORB 共有 30 个 API，可分为四组：发布者类、订阅者类、通用 API 类和工具类。几乎所有这些 API 都使用文件描述符操作，因此应特别注意避免跨进程（任务）使用。

**发布者类 API**
------------------------

**通知类型主题发布**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

此类别共有 5 个 API，其中 orb_advertise、orb_advertise_queue 和 orb_advertise_multi 内部基于 orb_advertise_multi_queue 实现。它们是参数 data、instance 和 queue_size 的排列组合。

``orb_advertise_multi_queue`` 在发布主题时需要指定主题元数据 meta、初始数据 data、实例 instance 和内部队列大小。成功时返回文件描述符；失败时返回 -1 并设置 errno。

instance 是输入参数的指针。如果为 NULL，实例将从其现有值递增。否则，\\*instance 指向的内容将用于发布。

支持对同一主题实例进行多次发布，允许在单个设备节点上有多个发布者。

::

  int orb_advertise_multi_queue(FAR const struct orb_metadata *meta,
                                FAR const void *data,               
                                FAR int *instance,                  
                                unsigned int queue_size);  
                                
  static inline int orb_advertise(FAR const struct orb_metadata *meta,
                                  FAR const void *data)
  {
    int instance = 0;
  
    return orb_advertise_multi_queue(meta, data, &instance, 1);
  }     
  
  static inline int orb_advertise_queue(FAR const struct orb_metadata *meta,
                                        FAR const void *data,
                                        unsigned int queue_size)
  {
    int instance = 0;
  
    return orb_advertise_multi_queue(meta, data, &instance, queue_size);
  }
  
  static inline int orb_advertise_multi(FAR const struct orb_metadata *meta,
                                        FAR const void *data,
                                        FAR int *instance)
  {
    return orb_advertise_multi_queue(meta, data, instance, 1);
  }

``orb_advertise_multi_queue_persist`` 与 ``orb_advertise_multi_queue`` 共享相同的参数，但内部实现不同。

::

  int orb_advertise_multi_queue_persist(FAR const struct orb_metadata *meta,
                                        FAR const void *data,
                                        FAR int *instance,
                                        unsigned int queue_size);

**取消发布主题**
~~~~~~~~~~~~~~~~~~~~~~~

``orb_unadvertise`` 函数以主题发布返回的文件描述符 fd 为参数，内部调用 orb_close 实现取消发布。

::

  static inline int orb_unadvertise(int fd)
  {
    return orb_close(fd);
  }

**发布主题数据**
~~~~~~~~~~~~~~~~~~~~~~~~~

``orb_publish`` 函数以主题元数据 meta、发布句柄 fd 和指向要发布数据 data 的指针为参数。每次只能发布一条数据。相比之下，orb_publish_multi 允许批量发布。两个函数的返回值不同：orb_publish 成功时返回 0，失败时返回 -1 并设置 errno，而 orb_publish_multi 成功时返回发布数据的长度。

::

  ssize_t orb_publish_multi(int fd, FAR const void *data, size_t len);
  
  static inline int orb_publish(FAR const struct orb_metadata *meta,
                                int fd, FARorb_close const void *data)
  {
    int ret;
  
    ret = orb_publish_multi(fd, data, meta->o_size);
    return ret == meta->o_size ? 0 : -1;
  }
  
  static inline int orb_publish_auto(FAR const struct orb_metadata *meta,
                                     FAR int *fd, FAR const void *data,
                                     FAR int *instance)；

**订阅者类 API**
------------------------

**订阅主题**
~~~~~~~~~~~~~~~~~~~~~~~~

``orb_subscribe`` 函数内部由 orb_subscribe_multi 实现，两者的主要区别在于是否需要指定订阅的实例。订阅成功时返回 fd（文件描述符）；失败时返回 -1 并设置 errno。

::

  int orb_subscribe_multi(FAR const struct orb_metadata *meta,
                          unsigned instance);
  
  static inline int orb_subscribe(FAR const struct orb_metadata *meta)
  {
    return orb_subscribe_multi(meta, 0);
  }
  
**取消订阅**
~~~~~~~~~~~~~~~

``orb_unsubscribe`` 函数以订阅返回的 fd（文件描述符）为参数，内部调用 orb_close 取消订阅。

::

  static inline int orb_unsubscribe(int fd)
  {
    return orb_close(fd);
  }

**检索数据**
~~~~~~~~~~~~~~~~~

``orb_copy`` 函数以主题元数据 meta、订阅句柄 fd 和指向存储数据的缓冲区 buffer 的指针为参数。每次只能读取一条数据。相比之下，orb_copy_multi 允许批量读取。两个函数的返回值不同：orb_copy 成功时返回 0，失败时返回 -1 并设置 errno，而 orb_copy_multi 成功时返回读取数据的长度。

::

  ssize_t orb_copy_multi(int fd, FAR void *buffer, size_t len);
  
  static inline int orb_copy(FAR const struct orb_metadata *meta,
                             int fd, FAR void *buffer)
  {
    int ret;
  
    ret = orb_copy_multi(fd, buffer, meta->o_size);
    return ret == meta->o_size ? 0 : -1;
  }

**通用类 API**
---------------------

**打开/关闭设备节点**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``orb_open`` 用于打开字符设备节点。参数包括 name（主题名称）、instance（主题实例索引）和 flags（打开模式）。订阅者通常以 O_RDONLY 打开，发布者以 O_WRONLY 打开，第三方可以以 "0" 打开节点以获取设备节点信息。对应的 ``orb_close`` 用于关闭节点。

::

  int orb_open(FAR const char *name, int instance, int flags);
  int orb_close(int fd);

**检索主题状态**
~~~~~~~~~~~~~~~~~~~~~~~~~

``orb_get_state``

::

  int orb_get_state(int fd, FAR struct orb_state *state);

**检查更新**
~~~~~~~~~~~~~~~~~~~~~

``orb_check`` 用于检查当前主题是否有新数据。它以指向更新变量的指针作为输入参数。

::

  int orb_check(int fd, FAR bool *updated);

**控制主题**
~~~~~~~~~~~~~~~~~~~~~

应用程序可以使用 ``orb_ioctl`` 控制物理传感器主题，例如调整加速度计、陀螺仪、磁力计和 PPG 传感器的量程、分辨率等。

::

  int orb_ioctl(int fd, int cmd, unsigned long arg);

**设置/获取主题批量参数**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``orb_set_batch_interval``/``orb_get_batch_interval`` 用于设置/获取主题的最大延迟报告时间，单位为微秒（μs）。此 API 仅适用于支持硬件 FIFO 的物理传感器。

::

  int orb_set_batch_interval(int fd, unsigned batch_interval);
  int orb_get_batch_interval(int fd, FAR unsigned *batch_interval);

**设置/获取主题间隔参数**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

频率和采样间隔互为倒数。``orb_set_interval``/``orb_get_interval`` 用于设置/获取采样率，单位为微秒（μs），而 ``orb_set_frequency``/``orb_get_frequency`` 用于设置/获取采样频率，单位为赫兹（Hz）。

::

  int orb_set_interval(int fd, unsigned interval);
  int orb_get_interval(int fd, FAR unsigned *interval);
  static inline int orb_set_frequency(int fd, unsigned frequency)
  static inline int orb_get_frequency(int fd, FAR unsigned *frequency)

**orb_flush**
~~~~~~~~~~~~~

``orb_flush`` 支持对具有硬件 FIFO 的主题执行刷新操作。刷新操作完成后，将为 fd 生成 POLLPRI 事件，然后可以调用 orb_get_events 获取相应事件。

::

  int orb_flush(int fd);

**orb_get_events**
~~~~~~~~~~~~~~~~~~

``orb_get_events`` 获取事件。目前支持的事件包括 ORB_EVENT_FLUSH_COMPLETE。

::

  int orb_get_events(int fd, FAR unsigned int *events);

**工具类 API**
-------------------

**检查主题是否存在发布者**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``orb_exists`` 用于检查主题是否存在发布者。以主题元数据 meta 和主题实例索引 instance 为参数。检查成功返回 0，失败返回错误码。

::
  
  int orb_exists(FAR const struct orb_metadata *meta, int instance);


**时间戳计算**
~~~~~~~~~~~~~~~~~~~~~~~~~

``orb_absolute_time`` 返回当前时间戳。
``orb_elapsed_time`` 返回两个时间戳之间的差值。

::

  orb_abstime orb_absolute_time(void);
  static inline orb_abstime orb_elapsed_time(FAR const orb_abstime *then)

**获取主题实例数量**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``orb_group_count`` 返回特定主题的实例数量。

::

  int orb_group_count(FAR const struct orb_metadata *meta);

**获取主题元数据**
~~~~~~~~~~~~~~~~~~~~~~

``orb_get_meta`` 用于通过字符串检索主题元数据的指针。目前此功能有较大限制：对于非物理传感器，必须显式订阅或发布主题才能成功获取元数据指针。

::

  FAR const struct orb_metadata *orb_get_meta(FAR const char *name);

这些工具类 API 提供了用于处理 ORB（对象请求代理）主题的额外工具，支持检查发布者存在性、计算时间戳、检索主题实例数量和访问主题元数据等任务。这些函数对于在基于 ORB 的系统中管理和交互主题至关重要。

**在 NuttX 中的使用**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在 NuttX 中，所有物理传感器驱动程序在系统启动时自动发布其主题。然后根据是否有应用程序订阅了相关主题来控制传感器的开启或关闭，实现智能低功耗管理。

所有虚拟主题（算法、状态、跨核主题）在首次发布或订阅时自动注册字符设备节点。一旦注册，即使发布或订阅后来被取消，这些节点仍保持活动状态。

当应用程序中的订阅者和发布者需要相互监控状态时，使用 poll 函数进行状态通知。订阅者和发布者通过 POLLPRI 信号同步状态。当发布者发布数据时，生成 POLLIN 事件通知所有订阅者。POLLPRI 事件在以下场景触发：

当新订阅者或发布者加入主题时。

当订阅者设置主题的采样率或批量参数时。

当订阅者或发布者离开主题时。

每当发生 POLLPRI 事件时，可以调用 orb_get_state 获取主题的当前状态，包括最大发布频率（max_frequency）、最小批量间隔（min_batch_interval）、内部环形缓冲区大小（queue_size）、订阅者数量（nsubscribers）和数据代数计数。

总之，如果订阅者和发布者相互依赖，建议使用基于 poll 或 libuv 的编程结构。如果它们相互独立，则优先使用基于通知的主题方法。

**融合算法模型**
---------------------------

如果多个应用程序相互连接，一个作为输入，另一个作为输出，可以建立共享主题以促进应用程序之间的解耦。例如，校准算法模块可以订阅未校准的传感器数据主题并发布校准后的传感器数据。运动算法模块可以订阅校准和未校准数据以生成算法主题，多个应用程序彼此忽略对方的存在。

**订阅者和发布者监控**
---------------------------------------

订阅者可以通过 POLLIN 事件检查更新事件，而发布者可以通过 POLLPRI 事件监控订阅者数量、采样率和其他状态的变化。最佳状态可以使用 orb_get_state 获取。通过利用这些机制，NuttX 为嵌入式系统环境中的高效数据通信和管理提供了强大的框架。

**工具**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _uorb_listener:

**uorb_listener**
-----------------

``uorb_listener`` 是位于 uORB 层之上的测试工具。它调用 uORB API 订阅和获取主题信息，进一步验证底层系统是否正常工作。uorb_listener 仅监控已发布的主题。整个监听过程可以使用 Ctrl+C 暂停。通过运行 uorb_listener -h 可以查看使用说明。以下是一些常用用法：

::

  listener <command> [arguments...]
   Commands:
          <topics_name> Topic name. Multi name are separated by ','
          [-h       ]  Listener commands help
          [-f       ]  Record uorb data to file
          [-n <val> ]  Number of messages, default: 0
          [-r <val> ]  Subscription rate (unlimited if 0), default: 0
          [-b <val> ]  Subscription maximum report latency in us(unlimited if 0), default: 0
          [-t <val> ]  Time of listener, in seconds, default: 5
          [-T       ]  Top, continuously print updating objects
          [-l       ]  Top only execute once.
        

``uorb_listener`` 以主题发布的频率持续打印所有主题的信息。

``uorb_listener -f`` 以主题发布的频率将持续将所有主题的信息保存到 /data/uorb/**/\*\*\*.csv。如果使用 -f 标志但无法创建文件，数据将改为输出到终端。

``uorb_listener -f sensor_accel0`` 以主题发布的频率持续将指定主题的信息保存到文件。

``uorb_listener n 1`` 打印所有主题当前信息的快照。

``uorb_listener n`` num 以主题发布的频率打印所有主题的信息，直到接收到 num 条消息。

``uorb_listener r 1`` 以 1Hz 的频率打印所有主题的信息。

``uorb_listener r x n`` num 以 xHz 的频率打印所有主题的信息，直到接收到 num 条消息。

``uorb_listener [specified_topic_list] r 1`` 以 1Hz 的频率持续打印指定主题的信息。在指定主题列表中，主题以逗号（,）分隔。每个条目可以是主题名称，如 sensor_accel，将打印该主题所有实例的信息。也可以是主题实例名称，如 sensor_mag0，将仅打印该特定主题实例的信息。

此工具提供了灵活的方式来监控和记录 uORB 主题数据，有助于调试和验证系统行为。


**Generator 调试工具说明**
-----------------------------------------

``uorb_generator`` 此工具可与 ``uorb_listener`` 配合使用。

使用此工具前，需要将 CONFIG_LINE_MAX 参数设置为足够长的长度，以确保终端能接受完整的输入数据。建议设置为 256 或 512。

传入的数据可以通过 uorb_listener 打印或手动使用格式信息拼接，但必须确保字符串和结构体信息一致。使用 uorb_listener -f 保存的主题可以拉取并导入到模拟器中进行调试（mount -t hostfs -o fs=/home/xxx/ /data）。

**参数说明：**

``-f`` 指定输入播放文件的路径。
``-n`` 指定数据播放次数。此选项仅在启用 -s 时有效。
``-r`` 指定播放频率（单位为 HZ，如 5hz、20hz）。此选项仅在启用 -s 时有效。
``-t`` 指定播放的主题，后面可以指定特定的实例值。
``-s`` 启用模拟（假数据）播放，从终端输入生成结构体数据。它会将当前数据的时间戳修改为实时时间。模拟数据应放在整个命令的末尾。

按照这些说明，用户可以有效地将 Generator 调试工具与 uorb_listener 配合使用，进行系统调试和验证。

::

  The tool publishes topic data via uorb.
  Notice:LINE_MAX must be set to 128 or more.
  
  generator <command> [arguments...]
    Commands:
      <topics_name> The playback topic name.
      [-h       ]  Listener commands help.
      [-f <val> ]  File path to be played back(absolute path).
      [-n <val> ]  Number of playbacks(fake model), default: 1
      [-r <val> ]  The rate for playing fake data is only valid when parameter 's' is used. 
                   default:10hz.
      [-s <val> ]  Playback fake data.
      [-t <val> ]  Playback topic.
       e.g.:
          sim - sensor_accel0:
            uorb_generator -n 100 -r 5 -s -t sensor_accel0 timestamp:23191100,x:0.1,y:9.7,z:0.81,temperature:22.15
  
          sim - sensor_baro0:
            uorb_generator -n 100 -r 5 -s -t sensor_baro0 timestamp:23191100,pressure:999.12,temperature:26.34
  
          fies - sensor_accel1
          uorb_generator -f /data/uorb/20240823061723/sensor_accel0.csv -t sensor_accel1
