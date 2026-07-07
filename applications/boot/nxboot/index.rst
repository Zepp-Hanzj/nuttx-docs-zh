=============================
``nxboot`` NuttX 引导加载程序
=============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

NuttX 引导加载程序（nxboot）可用于为基于 NuttX 的设备提供更新和恢复功能。
该引导加载程序实现了一种使用三个分区/区域的算法：主分区、次分区和第三分区。
主分区用于运行镜像，因此通常位于程序存储器中。
次分区和第三分区用于存储更新镜像或恢复镜像，例如可以位于外部闪存上。

引导加载程序的镜像在其头部中包含版本信息。请注意，引导加载程序/镜像特性可能因不同版本而异，
可移植的应用程序应考虑到这一点。

算法描述
---------------------

更新通过从更新区域简单复制到主分区来执行，如果恢复区域中尚不存在恢复镜像，则在恢复区域中创建。
一旦用户确认镜像，更新区域中的镜像也会被确认，更新区域变为恢复区域，反之亦然。
这意味着恢复镜像始终存在（第一次更新除外），后续更新只是从更新区域复制镜像到主分区。
这使得更新显著更快，并且更关注闪存磨损，同时保持恢复/回滚的可能性。

未确认的镜像在重启时将回滚到恢复镜像。

可引导镜像由一个头部 :c:struct:`nxboot_img_header` 组成，
包含魔数值、头部版本、头部大小、镜像的 CRC32（包括头部的某些部分）、
不包括头部的镜像大小、平台标识符、扩展头部指针和固件版本。
头部位于镜像本身之前，具有可配置的大小 ``CONFIG_NXBOOT_HEADER_SIZE``。
CRC 从整个镜像（包括头部，但不包括魔数、头部版本和头部大小字段）计算得出。
目前不支持扩展头部，但头部已经为其指针保留了空间。

兼容 nxboot 引导加载程序的镜像可以通过物理编程器（如 STlink 或 JTAG）直接上传到主分区，
也可以通过某些外部应用程序（通过以太网、USB、CAN 等）上传到更新分区。
更新和恢复插槽也可以位于主闪存中，但这会在写入操作期间暂停程序执行，
因此如果不使用外部闪存则不推荐。上传的镜像在下次启动时被引导加载程序检测到并执行更新。

引导加载程序有一个内部魔数值，用于检测更新的镜像。一旦发生更新，镜像从更新分区复制到主分区，
并带有内部魔数值，更新插槽的第一个擦除页被擦除。
只有当其恢复镜像存在时，具有内部魔数值的镜像才被认为是有效的，
因此镜像确认是通过将第一个擦除页（按写入页面大小从主分区复制）写回到更新插槽来完成的。
建议使用 :c:func:`nxboot_confirm` API 来确认镜像。
这种方法会使更新分区的第一个扇区磨损更多，但完全避免了镜像尾部问题，并简化了内部和 API 逻辑。

应用程序可以使用函数 :c:func:`nxboot_get_state` 来确定哪个分区是更新分区和恢复分区，
从而确定更新镜像应该存储在哪里。也可以使用函数 :c:func:`nxboot_open_update_partition`，
它确定正确的更新分区并返回打开的文件描述符。这是推荐的方法，因为它避免了可能的错误。

硬件要求
---------------------

如上所述，引导加载程序使用三个分区，第一个通常位于程序闪存中。

引导加载程序本身只需最少的底层存储设备特性知识。这是通过 ``BCH`` 和 ``FTL`` 子系统实现的，
它们使引导加载程序能够通过字符设备驱动程序使用标准 POSIX 文件系统操作
（例如 ``open()`` / ``close()`` / ``read()`` / ``write()``）来管理 MTD 分区。

目前需要通过上述 ``BCH`` 和 ``FTL`` 子系统访问分区，但未来的增强可以提供通过 ``MTD`` 层的直接访问。

配置
---------------------

以下配置选项可用：

- ``CONFIG_BOOT_NXBOOT``：启用 NuttX 引导加载程序构建。
- ``CONFIG_NXBOOT_PRIMARY_SLOT_PATH``：
    应用固件镜像主插槽字符设备驱动程序的路径。镜像从此位置运行。默认为 ``dev/ota0``。
- ``CONFIG_NXBOOT_SECONDARY_SLOT_PATH``：
    应用固件镜像次插槽字符设备驱动程序的路径。这是更新或恢复插槽。默认为 ``dev/ota1``。
- ``CONFIG_NXBOOT_TERTIARY_SLOT_PATH``：
    应用固件镜像第三插槽字符设备驱动程序的路径。这是更新或恢复插槽。默认为 ``dev/ota2``。
- ``CONFIG_NXBOOT_HEADER_SIZE``：
    镜像头大小。请注意，此大小应与程序存储器写入页面大小对齐！
- ``CONFIG_NXBOOT_PLATFORM_IDENTIFIER```：
    64 位平台标识符。这是引导加载程序用来验证镜像是否应在给定平台上运行的唯一平台标识符。
    如果镜像头部中的值与此选项不匹配，则更新（甚至通过编程器上传的固件）将被拒绝。
- ``CONFIG_NXBOOT_BOOTLOADER``：
    此选项构建并链接引导加载程序应用程序。此应用程序应该是 NuttX 的入口函数。
    它检查可能的更新/回滚操作，执行该操作并引导正确的镜像。
- ``CONFIG_NXBOOT_SWRESET_ONLY``：
    此选项确保更新/回滚仅在软件重置时执行。这样，开发板可以在例如断电期间保持其镜像
    （即使未确认），并且仅在基于用户/维护人员输入的预期情况下执行更新/回滚。
    以下重置原因被视为软件重置。

    ``BOARDIOC_RESETCAUSE_CPU_SOFT``：软件重置

    ``BOARDIOC_RESETCAUSE_CPU_RWDT``：看门狗错误

    ``BOARDIOC_RESETCAUSE_PIN``：重置按钮

- ``NXBOOT_PREVENT_DOWNGRADE``：
    NXboot 使用语义版本 2.0.0（不含构建元数据）。默认情况下，对每个与当前运行版本不匹配的版本执行更新。
    如果选择 NXBOOT_PREVENT_DOWNGRADE，则仅对较新版本执行更新（根据语义版本优先规则）。

    ``WARNING``：NXboot 目前仅实现 ``MAJOR.MINOR.PATCH`` 的优先级，忽略预发布版本。

镜像创建
--------------

由 nxboot 引导加载程序引导的镜像必须预先添加头部才能被正确识别和处理。
位于 ``apps/boot/nxboot/tools`` 目录中的 Python 脚本 ``nximage.py`` 可用于生成 nxboot 兼容的镜像。

.. code-block:: bash

  python3 apps/boot/nxboot/tools/nximage.py  \
		--version "VERSION" \
		--header_size CONFIG_NXBOOT_HEADER_SIZE \
		--identifier CONFIG_NXBOOT_PLATFORM_IDENTIFIER \
		nuttx.bin image.img

它接受输入参数 ``--version``（镜像版本）、``--header_size``（配置的头部大小）和 ``--identifier``（平台标识符）。
输入文件是二进制文件 ``nuttx.bin``，添加头部后的输出是 ``image.img``。

镜像版本遵循 `Semantic Versioning 2.0.0 <https://semver.org/spec/v2.0.0.html>`__，
不使用构建元数据。使用的格式为 MAJOR.MINOR.PATCH-prerelease。
镜像版本对于更新的发生很重要，因为引导加载程序会自动拒绝与已运行固件版本相同的更新固件。

配置选项：

公共 API
--------------

启用 ``CONFIG_BOOT_NXBOOT`` 选项提供以下 NXboot API。

.. code-block:: c

  #include <nxboot.h>

.. c:struct:: nxboot_img_version
.. code-block:: c

  #define NXBOOT_HEADER_PRERELEASE_MAXLEN 94

  struct nxboot_img_version
  {
    /* MAJOR version */
    uint16_t major;
    /* MINOR version */
    uint16_t minor;
    /* PATCH version */
    uint16_t patch;
    /* Additional pre-release version */
    char pre_release[NXBOOT_HEADER_PRERELEASE_MAXLEN];
  };

.. c:struct:: nxboot_hdr_version
.. code-block:: c

  struct nxboot_hdr_version
  {
    /* Header major version */
    uint8_t major;
    /* Header minor version */
    uint8_t minor;
  };

.. c:struct:: nxboot_img_header
.. code-block:: c

  #define NXBOOT_HEADER_MAGIC     0x534f584e
  #define NXBOOT_HEADER_MAGIC_INT 0xaca0abb0

  struct nxboot_img_header
  {
    /* Header magic */
    uint32_t magic;
    /* Version of the header */
    struct nxboot_hdr_version hdr_version;
    /* Size of the header */
    uint16_t header_size;
    /* CRC of the image, exceluding the previous header fields. */
    uint32_t crc;
    /* Image size (excluding the header) */
    uint32_t size;
    /* Platform identifier */
    uint64_t identifier;
    /* Address of optional extended headers */
    uint32_t extd_hdr_ptr;
    /* Image version */
    struct nxboot_img_version img_version;
  };

.. c:enum:: nxboot_update_type
.. code-block:: c

    enum nxboot_update_type
    {
      /* No action to do */
      NXBOOT_UPDATE_TYPE_NONE = 0,
      /* Update will take place upon reboot */
      NXBOOT_UPDATE_TYPE_UPDATE = 1,
      /* Revert will take place upon reboot */
      NXBOOT_UPDATE_TYPE_REVERT = 2,
    };

.. c:struct:: nxboot_state
.. code-block:: c

  #define NXBOOT_PRIMARY_SLOT_NUM 0
  #define NXBOOT_SECONDARY_SLOT_NUM 1
  #define NXBOOT_TERTIARY_SLOT_NUM 2

  struct nxboot_state
  {
    /* Number of update slot */
    int update;
    /* Number of recovery slot */
    int recovery;
    /* True if recovery image contains valid recovery */
    bool recovery_valid;
    /* True if image in a primary slot has a recovery (even non valid) */
    bool recovery_present;
    /* True if primary slot is confirmed */
    bool primary_confirmed;
    /* True if update slot has a valid image */
    enum nxboot_update_type next_boot;
  };

.. c:function:: int nxboot_get_state(struct nxboot_state *state)

  此函数可用于确定主镜像是否已确认。与返回引导加载程序完整状态的 nxboot_get_state 函数相比，
  这提供了更直接的确认状态访问。

  :param state: 指向 ``struct nxboot_state`` 结构体的指针。

  :return: 成功返回 0，失败返回 -1 并设置 errno。

.. c:function:: int nxboot_open_update_partition(void)

  获取当前引导加载程序状态并打开应存储更新镜像的分区。它返回该分区的有效文件描述符，
  用户负责写入并在之后关闭。

  :return: 成功返回有效文件描述符，失败返回 -1 并设置 errno。

.. c:function:: int nxboot_get_confirm(void)

  获取当前运行的镜像是否已确认（因此是稳定的）的信息。

  :return: 1 表示已确认，0 表示未确认，失败返回 -1 并设置 errno。

.. c:function:: int nxboot_confirm(void)

  确认当前位于主分区中的镜像，并将其在更新分区中的副本标记为恢复镜像。

  :return: 成功返回 0，失败返回 -1 并设置 errno。

.. c:function:: int nxboot_perform_update(bool check_only)

  检查可能的固件更新并通过将更新镜像复制到主插槽或在回滚情况下将恢复镜像复制到主插槽来执行。
  在任何情况下，此函数都以主插槽中有效的镜像结束。

  这是一个入口点函数，应从引导加载程序应用程序调用。

  :param check_only: 仅修复损坏的更新。

  :return: 成功返回 0，失败返回 -1 并设置 errno。
