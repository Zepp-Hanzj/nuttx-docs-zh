==========
主机工具
==========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本页讨论 ``tools/`` 目录，其中包含各种脚本和主机 C 程序，
它们是 NuttX 构建系统的重要组成部分：

.. toctree::
   :caption: Tool documentation pages
   :maxdepth: 1
   :glob:

   ./*

.. _mkpasswd_autogen:

mkpasswd — 构建时 ``/etc/passwd`` 生成
-------------------------------------------------

``tools/mkpasswd`` 是一个 C 主机工具（从 ``tools/mkpasswd.c`` 编译），
在构建时生成单个 ``/etc/passwd`` 条目。当设置了
``CONFIG_BOARD_ETC_ROMFS_PASSWD_ENABLE=y`` 时，它会由 ROMFS 构建步骤
自动调用。

为什么要在构建时生成？
~~~~~~~~~~~~~~~~~~~~~~~~~~

在固件中硬编码默认密码是一个众所周知的安全弱点（CWE-798）。
通过在构建时从用户提供的明文密码生成 ``/etc/passwd`` 条目，
每个固件镜像都携带唯一的凭据。如果密码留空，构建将失败，
防止无凭据的意外部署。

为了提高基本安全性，配置的密码长度必须至少为 8 个字符。

工作原理
~~~~~~~~~~~~

1. 主机工具从 ``CONFIG_BOARD_ETC_ROMFS_PASSWD_PASSWORD`` 读取明文密码。
2. 密码使用 Tiny Encryption Algorithm (TEA) 进行哈希处理——与运行时在
   ``libs/libc/misc/lib_tea_encrypt.c`` 中使用的实现相同——并使用与
   ``apps/fsutils/passwd/passwd_encrypt.c`` 匹配的自定义 base64 编码。
3. 生成的哈希条目写入 ``etctmp/<mountpoint>/passwd``，然后嵌入到 ROMFS 镜像中。
4. **明文密码永远不会存储在固件镜像中**。

Kconfig 选项
~~~~~~~~~~~~~~~

通过 ``make menuconfig`` 启用该特性并配置凭据：

.. code:: kconfig

   CONFIG_BOARD_ETC_ROMFS_PASSWD_ENABLE=y
   CONFIG_NSH_CONSOLE_LOGIN=y                     # required to enforce login prompt
   CONFIG_BOARD_ETC_ROMFS_PASSWD_USER="root"          # default: root
   CONFIG_BOARD_ETC_ROMFS_PASSWD_PASSWORD="<secret>"  # required, min length 8
   CONFIG_BOARD_ETC_ROMFS_PASSWD_UID=0
   CONFIG_BOARD_ETC_ROMFS_PASSWD_GID=0
   CONFIG_BOARD_ETC_ROMFS_PASSWD_HOME="/"

TEA 加密密钥可以通过 ``CONFIG_FSUTILS_PASSWD_KEY1..4`` 从默认值更改。

``/etc/passwd`` 文件格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: text

   user:x:uid:gid:home

其中：

* ``user`` — 用户名
* ``x`` — 经 TEA 哈希、base64 编码的密码
* ``uid`` — 数字用户 ID
* ``gid`` — 数字组 ID
* ``home`` — 登录目录

验证生成的条目
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

启用 ``CONFIG_BOARD_ETC_ROMFS_PASSWD_ENABLE`` 并设置密码后，
重新构建并验证：

1. **配置并构建**:

   .. code:: console

      $ make menuconfig   # 启用 BOARD_ETC_ROMFS_PASSWD_ENABLE 并设置密码
      $ make

2. **检查生成的 passwd 行**（写入开发板构建目录）:

   .. code:: console

      $ cat boards/<arch>/<chip>/<board>/src/etctmp/etc/passwd
      root:8Tv+Hbmr3pLVb5HHZgd26D:0:0:/

3. **验证固件中不存在明文**:

   .. code:: console

      $ grep <your-password> boards/<arch>/<chip>/<board>/src/etctmp.c
      # must print nothing

关于 ``savedefconfig`` 的注意事项
~~~~~~~~~~~~~~~~~~~~~~~~~~

为避免将凭据泄露到开发板 defconfig 中，``make savedefconfig`` 不会在
生成的 defconfig 中保存以下选项：

* ``CONFIG_BOARD_ETC_ROMFS_PASSWD_PASSWORD``
* ``CONFIG_FSUTILS_PASSWD_KEY1``
* ``CONFIG_FSUTILS_PASSWD_KEY2``
* ``CONFIG_FSUTILS_PASSWD_KEY3``
* ``CONFIG_FSUTILS_PASSWD_KEY4``

如果你需要这些值用于本地开发，请在运行 ``make savedefconfig`` 后
手动将其添加到本地 defconfig 中。
