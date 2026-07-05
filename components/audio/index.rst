===============
Audio Subsystem
===============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本页讨论 NuttX 的音频子系统支持，仅当在 NuttX 配置文件中定义了 ``CONFIG_AUDIO`` 时才会构建。

nuttx/audio 中的文件
====================

本目录包含 NuttX 音频子系统的上半部分。上半部分为应用程序提供了一个通用接口，同时也为特定的下半部分音频设备驱动定义了绑定层。

* ``audio.c`` - 绑定到 drivers/audio 子目录中下半部分驱动的上半部分驱动。对于每个连接的音频设备，都会有一个上半部分驱动的实例绑定到下半部分驱动上下文的实例。
* ``pcm_decode.c`` - 解码 PCM / WAV 类型数据的例程。

音频系统接口的部分内容具有应用程序接口。这些部分位于 ``nuttx/libc/audio`` 目录中，在该处构建以供操作系统驱动逻辑和用户应用程序逻辑访问。``nuttx/libc/audio`` 中的相关文件包括：

* ``buffer.c`` - 管理音频子系统中使用的音频管线缓冲区 (apb) 的创建和销毁的例程。音频管线缓冲区在用户应用程序和音频驱动之间传递，用于提供播放（或未来的录音）的音频内容。

相关头文件
====================

``include/nuttx/audio/audio.h`` - 定义音频接口的顶级包含文件
``include/nuttx/audio/vs1053.h`` - 特定驱动初始化原型

配置设置
======================

通用音频设置
----------------------

* ``CONFIG_AUDIO``
  启用音频子系统的整体支持
* ``CONFIG_AUDIO_MULTI_SESSION``
  启用音频子系统跟踪与低级音频设备的多个打开会话的支持。
* ``CONFIG_AUDIO_LARGE_BUFFERS``
  指定缓冲区大小变量应为 32 位而非正常的 16 位大小。这允许在 RAM 充足的系统上使用大于 64K 字节的缓冲区。
* ``CONFIG_AUDIO_NUM_BUFFERS``
  设置用于音频操作的音频缓冲区数量。如果配置设置了 ``CONFIG_AUDIO_DRIVER_SPECIFIC_BUFFERS``，且音频设备不支持该操作，则此值成为要使用的默认缓冲区数量。
* ``CONFIG_AUDIO_BUFFER_SIZE``
  设置用于音频操作的音频缓冲区大小。如果配置设置了 ``CONFIG_AUDIO_DRIVER_SPECIFIC_BUFFERS``，且音频设备不支持该操作，则此值成为要使用的默认缓冲区大小。
* ``CONFIG_AUDIO_DRIVER_SPECIFIC_BUFFERS``
  启用低级音频驱动指定为与该驱动交互获得最佳性能而应分配的缓冲区数量和大小的支持。
* ``CONFIG_AUDIO_CUSTOM_DEV_PATH``
  指定所有音频设备应在标准 ``/dev/audio`` 目录以外的文件系统位置注册。
* ``CONFIG_AUDIO_DEV_ROOT``
  指定所有音频设备应在 ``/dev`` 目录中注册。由于不需要额外的目录，可以节省少量代码和 RAM 空间，但在搜索音频设备时会牺牲执行速度，因为必须打开 ``/dev`` 中的所有条目并测试它们是否提供音频支持。仅在选择了 ``CONFIG_AUDIO_CUSTOM_DEV_PATH`` 时可用。
* ``CONFIG_AUDIO_DEV_PATH``
  指定音频设备将注册的自定义目录。在选择了 ``CONFIG_AUDIO_CUSTOM_DEV_PATH`` 且未选择 ``CONFIG_AUDIO_DEV_ROOT`` 时可用。

音频格式支持选择
-------------------------------

* ``CONFIG_AUDIO_FORMAT_AC3``
  指定如果下半部分驱动可用，应启用 AC3 支持。
* ``CONFIG_AUDIO_FORMAT_DTS``
  指定如果下半部分驱动可用，应启用 DTS 支持。
* ``CONFIG_AUDIO_FORMAT_PCM``
  指定如果下半部分驱动可用，应启用 PCM 支持。
* ``CONFIG_AUDIO_FORMAT_MP3``
  指定如果下半部分驱动可用，应启用 MP3 支持。
* ``CONFIG_AUDIO_FORMAT_MIDI``
  指定如果下半部分驱动可用，应启用 MIDI 支持。
* ``CONFIG_AUDIO_FORMAT_WMA``
  指定如果下半部分驱动可用，应启用 WMA 支持。
* ``CONFIG_AUDIO_FORMAT_OGG_VORBIS``
  指定如果下半部分驱动可用，应启用 Ogg Vorbis 支持。

音频功能排除选择
----------------------------------

* ``CONFIG_AUDIO_EXCLUDE_VOLUME``
  禁用所有库和驱动中设置播放音量的支持。在这种情况下，设备音量将取决于低级驱动定义的默认级别，通常通过配置设置。
* ``CONFIG_AUDIO_EXCLUDE_BALANCE``
  禁用所有库和驱动中设置播放平衡的支持。此外，要使平衡正常工作或有意义，不能排除音量支持。
* ``CONFIG_AUDIO_EXCLUDE_TONE``
  禁用设置低音和高音的支持。
* ``CONFIG_AUDIO_EXCLUDE_PAUSE_RESUME``
  禁用所有库和驱动中暂停和恢复播放的支持。
* ``CONFIG_AUDIO_EXCLUDE_STOP``
  禁用所有库和驱动中在音频播放开始后停止播放的支持。通常在只需要短通知音效（而非媒体播放类型应用程序）时选择。

相关子目录
======================

* ``drivers/audio`` - 包含低级设备特定驱动。
* ``apps/system/nxplayer`` - 用户模式音频子系统接口库。
