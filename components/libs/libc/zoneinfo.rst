==================
libs/libc/zoneinfo
==================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Author: Gregory Nutt <gnutt@nuttx.org>

Directory Contents
==================

This 目录 contains logic to 创建 a version of the TZ/Olson 数据base.
This 数据base 需要 if localtime() 支持 is selected via
CONFIG_LIBC_LOCALTIME.  This logic in this 目录 does 以下:

- It downloads the current TZ 数据base from the IANA website
- It downloads the current timezone tools from the same location
- It 构建s the tools and constructs the binary TZ 数据base
- It will then, 选项ally, 构建 a ROMFS 文件system 图像 containing
  the 数据 base.

Creating and Mounting a ROMFS TZ Database
=========================================

The ROMFS 文件system 图像 can that be mounted during the boot-up sequence
so that it 可用 for the localtime() logic.  There are two steps to
doing this:

- First, a ROM disk 设备 must be 创建d.  这是 done by calling
  the 函数 romdisk_注册() as described in
  nuttx/include/nuttx/驱动s/ramdisk.h.  这是 an OS level 操作
  and must be done in the board-level logic before your application
  启动s.

  romdisk_注册() will 创建 a block 驱动 at /dev/ramN where N
  is the 设备 minor 数量 that was provided to romdisk_注册.

- The second step is to mount the 文件 system.  This step can be
  performed either in your board 配置 logic or by your
  application using the mount() 接口 described in
  nuttx/include/sys/mount.h.

  These steps, however, must be done very early in initialization,
  before there is any need for time-related services.

Both of these steps are shown to获取her in 以下 code sample at the
end of this page.

Example Configuration
=====================

I have tested this using the sim/nsh 配置.  Here are the
modifications to the 配置 that I used for testing::

  CONFIG_BOARD_LATE_INITIALIZE=y

  CONFIG_LIBC_LOCALTIME=y
  CONFIG_LIBC_TZDIR="/share/zoneinfo"
  CONFIG_LIBC_TZ_MAX_TIMES=370
  CONFIG_LIBC_TZ_MAX_TYPES=20

  CONFIG_LIBC_ZONEINFO=y
  CONFIG_LIBC_ZONEINFO_ROMFS=y

注意：  The full TZ 数据base is quite large.  To 创建 a reasonable 大小d
ROMFS 图像, I had to trim some of the 文件s like this::

  cd nuttx
  tools/configure.sh sim:nsh
  make menuconfig

Select the above localtime() and nuttx/zoneinfo 配置 设置s.
Then::

  make con文本
  cd ../nuttx/libs/libc/zoneinfo/tzbin/usr/share/zoneinfo

移除 as many timezone 文件s as you can.  Do not 移除 the GMT, localtime,
or posixrules 文件s.  Those might be needed in any event.  Then you can
force re构建ing of the ROMFS 文件system be removing some 文件s::

  cd ../../..
  rm romfs_zoneinfo.*
  rm *.o
  cd ../../nuttx
  make

If you have problems 构建ing the simulator on your platform, check out
:doc:`/platforms/sim/sim/boards/sim/index`.
You might find some help there.

Here is a sample 运行.  I have not seen any 错误s in single stepping through
the logic but neither am I certain that everything is working properly::

  NuttShell (NSH)
  nsh> date
  Jul 01 00:00:02 2008
  nsh> 设置 TZ US/Mountain
  nsh> date -s "Apr 11 11:53:00 2015"
  nsh> date
  Apr 11 17:53:00 2015

注意： Because of daylight savings time, US/Mountain is GMT-6 on Apr 11.  The
above suggests that perhaps the NSH 数据 command may be 设置 local time,
but printing GMT time?

Sample Code to Mount the ROMFS Filesystem
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
