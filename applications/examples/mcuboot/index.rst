============================
``mcuboot`` MCUboot 示例
============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``swap_test``
=============

描述
-----------

MCUboot Swap Image 是一个演示使用内部闪存进行固件升级的应用程序。
它模拟 MCUboot API 步骤来在两个有效镜像之间切换。

该应用程序向 NuttX NSH 添加了 3 个内置应用程序：version、set_img 和 confirm。
应用程序构建完成并生成 ``nuttx.bin`` 后，必须对二进制文件进行签名。
请查阅您的板卡文档页面获取签名操作说明。

如何构建和烧录
----------------------

第一步是使用 ``mcuboot-loader`` 作为目标构建您的板卡配置。
这将创建引导加载程序本身。``nuttx.bin`` 必须按常规方式烧录。

之后，清理环境并将 ``mcuboot-swap-test`` 设置为目标。构建输出将生成 ``nuttx.bin`` 文件。
您应该执行名为 ``imgtool.py`` 的 MCUboot 脚本，并对二进制文件进行两次签名。

第一次使用 ``--version 1.0.0`` 和 ``signedv1.bin`` 作为输出文件。
第二次签名需要更改为 ``--version 2.0.0`` 和 ``signedv2.bin`` 作为输出文件。

``signedv1.bin`` 文件必须放在 MCUboot Slot-0 分区，``signedv2.bin`` 放在 Slot-1。

关于签名和烧录的更多说明可以在板卡文档页面找到。

运行镜像交换测试
-----------------------

打开终端并重启您的板卡。您可以看到类似下面的输出。
可以使用 ``?`` 命令检查内置应用程序::

  *** Booting MCUboot build 7c890f4b075aed73e4c825ccf875b2fb9ebf2ded ***
  NuttShell (NSH) NuttX-10.2.0
  nsh> ?
  help usage:  help [-v] [<cmd>]

    .         cd        echo      hexdump   mv        rmdir     true      xd
    [         cp        exec      kill      printf    set       truncate
    ?         cmp       exit      ls        ps        sleep     uname
    basename  dirname   false     mkdir     pwd       source    umount
    break     dd        free      mkrd      reboot    test      unset
    cat       df        help      mount     rm        time      usleep

  Builtin Apps:
    mcuboot_set_img  mcuboot_confirm  sh
    mcuboot_version  ramtest          nsh
  nsh>

第一步（检查版本）::

  nsh> mcuboot_version
  Image version 1.0.0.0
  nsh>

第二步（标记镜像为正常，因为它正在运行）。这是一个可选步骤，
如果您在运行 ``imgtool.py`` 时没有使用可选参数 ``--confirm``，则必须执行此步骤::

  nsh> mcuboot_confirm
  Application Image successfully confirmed!
  nsh>

第三步（重启查看结果）::

  nsh> reboot
  *** Booting MCUboot build 7c890f4b075aed73e4c825ccf875b2fb9ebf2ded ***
  NuttShell (NSH) NuttX-10.2.0
  nsh> mcuboot_version
  Image version 1.0.0.0
  nsh>

第四步（切换镜像）::

  nsh> mcuboot_set_img
  Requested update for next boot. Restarting...
  *** Booting MCUboot build 7c890f4b075aed73e4c825ccf875b2fb9ebf2ded ***
  NuttShell (NSH) NuttX-10.2.0
  nsh> mcuboot_version
  Image version 2.0.0.0
  nsh>

现在，我们已从镜像版本 1.0.0 切换到镜像 2.0.0。但是，我们故意不运行 ``mcuboot_confirm`` 应用程序::

  nsh> reboot
  *** Booting MCUboot build 7c890f4b075aed73e4c825ccf875b2fb9ebf2ded ***
  NuttShell (NSH) NuttX-10.2.0
  nsh> mcuboot_version
  Image version 1.0.0.0
  nsh>

这意味着如果应用程序因任何原因重启、出现故障或无法启动，
MCUboot 将切换回旧的"正常"镜像！请记住我们在第二步执行了 ``mcuboot_confirm``。

第五步（切换到镜像版本 2 并标记为永久）::

  nsh> mcuboot_set_img
  Requested update for next boot. Restarting...
  *** Booting MCUboot build 7c890f4b075aed73e4c825ccf875b2fb9ebf2ded ***
  NuttShell (NSH) NuttX-10.2.0
  nsh> mcuboot_confirm
  Application Image successfully confirmed!
  nsh> mcuboot_version
  Image version 2.0.0.0
  nsh>

第六步（重启并确认 V2 镜像）::

  nsh> reboot
  *** Booting MCUboot build 7c890f4b075aed73e4c825ccf875b2fb9ebf2ded ***
  NuttShell (NSH) NuttX-10.2.0
  nsh> mcuboot_version
  Image version 2.0.0.0
  nsh>

结论：一旦启动了更新的镜像并确认它，MCUboot 将始终运行该镜像，除非您指示它再次交换！

``mcuboot_local_agent``
=======================

MCUBoot 本地更新代理是一个演示使用本地存储中的二进制文件进行固件升级的应用程序。
与远程更新机制不同，此示例将固件二进制文件直接从本地存储（如 SD 卡、USB 驱动器或任何已挂载的文件系统）复制到辅助闪存插槽，
供 MCUBoot 在下次启动时处理。

该应用程序提供了一种简单可靠的方式来更新固件，无需网络连接或复杂的远程更新基础设施。

功能：

* 从本地存储复制固件二进制文件到辅助闪存插槽
* 固件复制过程中的进度指示
* 自动大小验证（确保固件适合辅助插槽）
* 闪存区域擦除和写入
* 自动启动标记和系统重启

构建和烧录
----------------------

首先，使用 MCUBoot、SD 卡支持构建您的板卡配置，并在
`Application Configuration → Examples → MCUboot Examples → MCUBoot Local Update Agent` 下启用此工具。

正常烧录板卡。

生成更新二进制文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

要创建用于更新的固件二进制文件：

1. 配置构建目标为辅助插槽::

     make menuconfig
     # Configure MCUBoot to build for secondary slot
     # (specific configuration varies by architecture)

2. 可选择修改应用程序（例如更改 MOTD）以直观地识别更新后的镜像

3. 构建更新二进制文件::

     make

4. 生成的二进制文件应复制到您的本地存储设备（即 SD 卡）。
   请查阅您的板卡文档获取具体的二进制文件名和任何必需的后处理步骤。

运行本地更新代理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 挂载包含固件二进制文件的存储设备::

     nsh> mount -t vfat /dev/mmcsd0 /mnt

2. 验证固件文件可访问::

     nsh> ls /mnt
     /mnt:
      nuttx.bin
      readme.txt

3. 使用固件文件路径运行更新代理::

     nsh> mcuboot_local_agent /mnt/nuttx.bin

   如果未指定路径，默认为 ``/mnt/sdcard/nuttx.bin``

示例输出
~~~~~~~~~~~~~~

运行更新代理时，您应该看到类似以下的输出::

  nsh> mcuboot_local_agent /mnt/nuttx.bin
  MCUBoot Local Update Agent
  Firmware file: /mnt/nuttx.bin
  Firmware file size: 1048576 bytes
  Erasing secondary flash slot...
  Copying firmware to secondary slot...
  Progress: 4096/1048576 bytes [0%]
  Progress: 8192/1048576 bytes [0%]
  Progress: 12288/1048576 bytes [1%]
  ...
  Progress: 1044480/1048576 bytes [99%]
  Progress: 1048576/1048576 bytes [100%]
  Firmware copy completed successfully!
  Firmware successfully copied to secondary slot!
  Update scheduled for next boot. Restarting...
  reboot status=0

重启后，MCUBoot 将检测到辅助插槽中的新固件并执行更新。
您应该看到指示交换过程的 MCUBoot 消息::

  *** Booting MCUboot build v2.2.0-rc1 ***
  ...
  Primary image: magic=good, swap_type=0x1, copy_done=0x3, image_ok=0x1
  Scratch: magic=unset, swap_type=0x1, copy_done=0x3, image_ok=0x3
  Boot source: primary slot
  Image index: 0, Swap type: test
  Starting swap using scratch algorithm.
  ...
  This is MCUBoot Updated Image!!
  nsh>
