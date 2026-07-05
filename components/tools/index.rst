==========
主机工具
==========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

本页讨论 the ``tools/`` 目录 containing miscellaneous scripts
and host C programs that are important parts of the NuttX 构建 system:

.. toctree::
   :caption: Tool documentation pages
   :maxdepth: 1
   :glob:

   ./*

.. _mkpasswd_autogen:

mkpasswd — Build-time ``/etc/passwd`` Generation
-------------------------------------------------

``tools/mkpasswd`` is a C host tool (compiled from ``tools/mkpasswd.c``) that
generates a single ``/etc/passwd`` entry at 构建 time.  It is invoked
automatically by the ROMFS 构建 step when
``CONFIG_BOARD_ETC_ROMFS_PASSWD_ENABLE=y`` is 设置.

为什么要在构建时生成？
~~~~~~~~~~~~~~~~~~~~~~~~~~

Shipping a hard-coded 默认 password in firmware is a well-known security
weakness (CWE-798).  By generating the ``/etc/passwd`` entry from a
user-supplied plain文本 password at 构建 time, each firmware 图像 carries
unique credentials.  The 构建 will fail if the password is left empty,
preventing accidental deployments with no credentials.

For improved baseline security, the configured password must be at least
8 characters long.

工作原理
~~~~~~~~~~~~

1. The host tool 读取s the plain文本 password from
   ``CONFIG_BOARD_ETC_ROMFS_PASSWD_PASSWORD``.
2. The password is hashed using the Tiny Encryption Algorithm (TEA) — the
   same implementation used at 运行time in
   ``libs/libc/misc/lib_tea_encrypt.c`` — with custom base64 encoding
   matching ``apps/fsutils/passwd/passwd_encrypt.c``.
3. The resulting hashed entry is written to
   ``etctmp/<mountpoint>/passwd`` and then embedded into the ROMFS 图像.
4. The **plain文本 password is never stored in the firmware 图像**.

Kconfig 选项
~~~~~~~~~~~~~~~

启用 the 特性 and configure credentials via ``make menuconfig``:

.. code:: kconfig

   CONFIG_BOARD_ETC_ROMFS_PASSWD_ENABLE=y
   CONFIG_NSH_CONSOLE_LOGIN=y                     # required to enforce login prompt
   CONFIG_BOARD_ETC_ROMFS_PASSWD_USER="root"          # default: root
   CONFIG_BOARD_ETC_ROMFS_PASSWD_PASSWORD="<secret>"  # required, min length 8
   CONFIG_BOARD_ETC_ROMFS_PASSWD_UID=0
   CONFIG_BOARD_ETC_ROMFS_PASSWD_GID=0
   CONFIG_BOARD_ETC_ROMFS_PASSWD_HOME="/"

The TEA encryption keys can be changed from their 默认s via
``CONFIG_FSUTILS_PASSWD_KEY1..4``.

``/etc/passwd`` 文件格式
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: text

   user:x:uid:gid:home

Where:

* ``user`` — user name
* ``x`` — TEA-hashed, base64-encoded password
* ``uid`` — numeric user ID
* ``gid`` — numeric group ID
* ``home`` — login directory

验证生成的条目
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After enabling ``CONFIG_BOARD_ETC_ROMFS_PASSWD_ENABLE`` and 设置 a
password, re构建 and verify:

1. **Configure and 构建**:

   .. code:: console

      $ make menuconfig   # 启用 BOARD_ETC_ROMFS_PASSWD_ENABLE and 设置 password
      $ make

2. **Inspect the generated passwd line** (written to the board 构建 tree):

   .. code:: console

      $ cat boards/<arch>/<chip>/<board>/src/etctmp/etc/passwd
      root:8Tv+Hbmr3pLVb5HHZgd26D:0:0:/

3. **Verify the plain文本 is absent from firmware**:

   .. code:: console

      $ grep <your-password> boards/<arch>/<chip>/<board>/src/etctmp.c
      # must print nothing

关于 ``savedefconfig`` 的注意事项
~~~~~~~~~~~~~~~~~~~~~~~~~~

To avoid leaking credentials into board defconfigs, ``make savedefconfig``
does not save 以下 选项s in the generated defconfig:

* ``CONFIG_BOARD_ETC_ROMFS_PASSWD_PASSWORD``
* ``CONFIG_FSUTILS_PASSWD_KEY1``
* ``CONFIG_FSUTILS_PASSWD_KEY2``
* ``CONFIG_FSUTILS_PASSWD_KEY3``
* ``CONFIG_FSUTILS_PASSWD_KEY4``

If you need these 值s for local development, 添加 them manually to your
local defconfig after 运行ning ``make savedefconfig``.