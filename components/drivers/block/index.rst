====================
Block Device Drivers
====================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

.. toctree::
  :maxdepth: 1

  ramdisk.rst


块设备驱动具有以下属性：

-  ``include/nuttx/fs/fs.h``。此头文件提供了与块驱动配合使用所需的所有结构和 API。

-  ``struct block_operations``。每个块设备驱动必须实现一个 ``struct block_operations`` 实例。该结构定义了一个包含以下方法的调用表：

-  ``int register_blockdriver(const char *path, const struct block_operations *bops, mode_t mode, void *priv);``。
   每个块驱动通过调用 ``register_blockdriver()`` 注册自身，传入它在 :ref:`伪文件系统 <file_system_overview>` 中出现的 ``path`` 及其初始化的 ``struct block_operations`` 实例。

-  **用户访问**。用户通常不直接访问块驱动，而是通过 ``mount()`` API 间接访问。``mount()`` API 将块驱动实例与文件系统和挂载点绑定。然后用户可以使用块驱动访问底层存储介质上的文件系统。*示例*：参见 ``apps/nshlib/nsh_fscmds.c`` 中的 ``cmd_mount()`` 实现。

-  **将字符驱动作为块设备访问**。参见 ``drivers/loop.c`` 中的 loop 设备。*示例*：参见 ``apps/nshlib/nsh_fscmds.c`` 中的 ``cmd_losetup()`` 实现。

-  **将块驱动作为字符设备访问**。参见 ``drivers/bch/`` 中的块到字符 (BCH) 转换逻辑。*示例*：参见 ``apps/nshlib/nsh_ddcmd.c`` 中的 ``cmd_dd()`` 实现。

-  **示例**。``drivers/loop.c``、``drivers/mmcsd/mmcsd_spi.c``、``drivers/ramdisk.c`` 等。
