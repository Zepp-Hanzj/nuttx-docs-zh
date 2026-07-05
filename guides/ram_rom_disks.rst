=======================
RAM 磁盘和 ROM 磁盘
=======================

.. warning:: 
    迁移自： 
    https://cwiki.apache.org/confluence/display/NUTTX/RAM+Disks+and+ROM+Disks

NSH mkrd 命令
================

创建 RAM 磁盘的典型方式是使用 NuttShell (NSH) ``mkrd`` 命令。语法为：

.. code-block:: shell

   mkrd [-m <minor>] [-s <sector-size>] <nsectors>

此命令创建一个由 ``<nsectors>`` 个扇区组成的 RAM 磁盘，
每个扇区大小为 ``<sector-size>``（如果未指定 ``<sector-size>`` 则为 512 字节）。
RAM 磁盘随后注册为 ``/dev/ram<minor>``。如果未指定 ``<minor>``，
``mkrd`` 尝试将 RAM 磁盘注册为 ``/dev/ram0``。

在内部，NSH ``mkrd`` 命令是操作系统 ``boardctl()`` 接口的简单包装器，
使用 ``BOARDIOC_MKRD`` 命令。"在底层"，此 ``boardctl()`` 命令执行以下操作：

1. 使用 ``kmm_malloc()`` 分配大小为 ``<nsectors>`` 乘以 ``<sector-size>`` 的内核空间内存
2. 将分配的内存清零，以及
3. 调用操作系统内部函数 ``ramdisk_register()`` 创建 RAM 磁盘。

NSH ROMFS /etc 支持
======================

ROM 磁盘是从存储在 FLASH 或其他 ROM 中的只读文件系统镜像创建的块设备。
没有 NSH 命令可在运行时创建 ROM 磁盘。但是，可以使用 ``CONFIG_NSH_ROMFSETC``
选项在 NSH 中启用 ROM 磁盘支持，如 `NSH 用户指南 <https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=139629410>`_
中 NSH 启动脚本部分所述。

任何应用程序都可以使用 ``boardctl()`` 接口和 ``BOARDIOC_ROMDISK`` 命令创建 ROM 磁盘。

在板启动逻辑中创建 RAM 磁盘
==========================================

RAM 磁盘可以在以管理器模式运行的板特定初始化逻辑中创建。
该逻辑可能如下所示：

.. code-block:: c

  int board_ramdisk(int minor, unsigned int sectsize, unsigned int nsectors)
  {
    size_t allocsize = (size_t)sectsize * (size_t)nsectors;
    FAR uint8_t *buffer;
  
    /* Allocate the memory backing up the ramdisk */
  
    buffer = (FAR uint8_t *)kmm_zalloc(allocsize);
    if (buffer == NULL)
      {
        return -ENOMEM;
      }
  
    /* Then register the ramdisk */
  
    ret = ramdisk_register(minor, buffer, nsectors, sectsize,
                          RDFLAG_WRENABLED | RDFLAG_FUNLINK);
    if (ret < 0)
      {
        kmm_free(buffer);
      }
  
    return ret;
  }

或者，这可以替换为对操作系统内部函数 ``mkrd()`` 的调用。

在板启动逻辑中创建 ROM 磁盘
==========================================

.. note::

   目前，``romdisk_register()`` 函数仅在操作系统内部可用。
   ``apps/`` 中的某些逻辑直接调用 ``romdisk_register()``，
   这违反了可移植的 POSIX 操作系统接口。
   应用程序的正确方法是通过 ``boardctl(BOARDIOC_ROMDISK)`` 创建 ROM 磁盘，
   如上所述。直接调用 ``romdisk_register()`` 不仅违反了 NuttX 的可移植接口，
   而且在 PROTECTED 或 KERNEL 构建模式下也不允许。

ROM 磁盘，即 FLASH 中的只读磁盘，可以由板启动逻辑以类似于 RAM 磁盘的方式创建，
但有以下注意事项：

- 不分配 FLASH 区域；FLASH 地址、扇区大小和扇区数必须已知。
- 使用 ``romdisk_register()`` 函数而不是 ``ramdisk_register()``。

一个简单的示例可能如下：

.. code-block:: c

  int board_romdisk(int minor, FAR uint8_t *buffer, unsigned int sectsize,
                    unsigned int nsectors)
  {
    /* Register the romdisk */
  
    return romdisk_register(minor, buffer, nsectors, sectsize);
  }

调用 ``romdisk_register()`` 等同于以最终参数 ``flags == 0``
调用 ``ramdisk_register()``。

大多数 ROM 磁盘使用 ROMFS 文件系统，尽管 CROMFS 是另一种选择。
创建 ROMFS 文件系统镜像涉及多个步骤。
有工具可以简化构建 ROMFS 镜像的过程，但该主题超出了此 Wiki 页面的范围。
