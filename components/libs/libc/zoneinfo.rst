==================
libs/libc/zoneinfo
==================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

作者：Gregory Nutt <gnutt@nuttx.org>

目录内容
==================

本目录包含用于创建 TZ/Olson 数据库版本的逻辑。如果通过
CONFIG_LIBC_LOCALTIME 选择了 localtime() 支持，则需要此数据库。
本目录中的逻辑执行以下操作：

- 从 IANA 网站下载当前 TZ 数据库
- 从同一位置下载当前时区工具
- 构建工具并生成二进制 TZ 数据库
- 随后可选择性地构建包含该数据库的 ROMFS 文件系统镜像

创建和挂载 ROMFS TZ 数据库
=========================================

ROMFS 文件系统镜像可以在启动过程中挂载，以便 localtime() 逻辑使用。
实现此功能需要两个步骤：

- 首先，必须创建一个 ROM 磁盘设备。这通过调用函数 romdisk_register()
  来完成，具体描述见 nuttx/include/nuttx/drivers/ramdisk.h。这是一项
  OS 级别的操作，必须在应用程序启动之前在板级逻辑中完成。

  romdisk_register() 将在 /dev/ramN 创建一个块设备驱动，其中 N 是
  提供给 romdisk_register 的次设备号。

- 第二步是挂载文件系统。此步骤可以在板级配置逻辑中执行，也可以由
  应用程序使用 nuttx/include/sys/mount.h 中描述的 mount() 接口执行。

  但是，这些步骤必须在初始化的非常早期完成，要在任何与时间相关的
  服务被需要之前。

以下代码示例展示了这两个步骤的完整用法，位于本页末尾。

示例配置
=====================

我使用 sim/nsh 配置对此进行了测试。以下是用于测试的配置修改::

  CONFIG_BOARD_LATE_INITIALIZE=y

  CONFIG_LIBC_LOCALTIME=y
  CONFIG_LIBC_TZDIR="/share/zoneinfo"
  CONFIG_LIBC_TZ_MAX_TIMES=370
  CONFIG_LIBC_TZ_MAX_TYPES=20

  CONFIG_LIBC_ZONEINFO=y
  CONFIG_LIBC_ZONEINFO_ROMFS=y

注意：完整的 TZ 数据库非常大。为了创建合理大小的 ROMFS 镜像，
我不得不裁剪部分文件，如下所示::

  cd nuttx
  tools/configure.sh sim:nsh
  make menuconfig

选择上述 localtime() 和 nuttx/zoneinfo 配置设置。然后::

  make context
  cd ../nuttx/libs/libc/zoneinfo/tzbin/usr/share/zoneinfo

尽可能多地删除时区文件。不要删除 GMT、localtime 或 posixrules 文件，
这些在任何情况下都可能需要。然后可以通过删除一些文件来强制重新
构建 ROMFS 文件系统::

  cd ../../..
  rm romfs_zoneinfo.*
  rm *.o
  cd ../../nuttx
  make

如果您在平台上构建模拟器时遇到问题，请查看
:doc:`/platforms/sim/sim/boards/sim/index`，或许能找到一些帮助。

以下是一次示例运行。我在逐步调试逻辑时没有发现任何错误，
但也不能确定一切都工作正常::

  NuttShell (NSH)
  nsh> date
  Jul 01 00:00:02 2008
  nsh> set TZ US/Mountain
  nsh> date -s "Apr 11 11:53:00 2015"
  nsh> date
  Apr 11 17:53:00 2015

注意：由于夏令时，US/Mountain 在 4 月 11 日为 GMT-6。以上结果
暗示 NSH 的 date 命令可能设置的是本地时间，但打印的是 GMT 时间？

挂载 ROMFS 文件系统的示例代码
=========================================

.. code-block:: C
                
   /****************************************************************************
    * Included Files
    ****************************************************************************/

   #include <nuttx/config.h>

   #include <sys/mount.h>
   #include <stdio.h>
   #include <stdlib.h>
   #include <errno.h>

   #include <nuttx/drivers/ramdisk.h>
   #include <nuttx/zoneinfo.h>

   /****************************************************************************
    * Pre-processor Definitions
    ****************************************************************************/

   #ifndef CONFIG_LIBC_TZDIR
   #  error CONFIG_LIBC_TZDIR is not defined
   #endif

   #ifdef CONFIG_DISABLE_MOUNTPOINT
   #  error "Mountpoint support is disabled"
   #endif

   #ifndef CONFIG_FS_ROMFS
   #  error "ROMFS support not enabled"
   #endif

   #define SECTORSIZE  64
   #define NSECTORS(b) (((b)+SECTORSIZE-1)/SECTORSIZE)

   /****************************************************************************
    * Public Functions
    ****************************************************************************/

   int mount_zoneinfo(int minor)
   {
      char devname[32];
      int  ret;

     /* Create a RAM disk for the test */

     ret = romdisk_register(minor, romfs_zoneinfo_img,
                            NSECTORS(romfs_zoneinfo_img_len), SECTORSIZE);
     if (ret < 0)
       {
         printf("ERROR: Failed to create RAM disk\n");
         return ret;
       }

     /* Use the minor number to create a name for the ROM disk block device */

     snprintf(devname, sizeof(devname), "/dev/ram%d", minor);

     /* Mount the ROMFS file system */

     printf("Mounting ROMFS filesystem at target=%s with source=%s\n",
            CONFIG_LIBC_TZDIR, devname);

     ret = mount(devname, CONFIG_LIBC_TZDIR, "romfs", MS_RDONLY, NULL);
     if (ret < 0)
       {
         printf("ERROR: Mount failed: %d\n", errno);
         return ret;
       }

     printf("TZ database mounted at %s\n", CONFIG_LIBC_TZDIR);
     return OK;
   }
