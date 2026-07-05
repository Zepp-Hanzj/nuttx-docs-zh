===================
VLAN 设备驱动
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

-  ``include/nuttx/net/vlan.h``。使用 VLAN 驱动所需的
   所有结构和 API 都在此头文件中提供。
-  我们还创建用于管理 VLAN 的 VLAN 设备，它们将成为类似 ``eth0.58`` 的接口。
-  还支持 QinQ，我们可以在另一个 VLAN 设备之上创建 VLAN 设备，如 ``eth0.100.101``（甚至 ``eth0.1.2.3.4``，Linux 上也支持）。
-  支持 SIOCSIFVLAN 的 ADD_VLAN_CMD 和 DEL_VLAN_CMD。
-  我们添加了默认 PCP，因为某些应用程序可能不想手动设置 PCP。
-  ``include/nuttx/net/ethernet.h``。802.1Q VLAN 的一些定义。

   .. code-block:: c

      #define VLAN_PRIO_MASK   0xe000 /* 优先级代码点 */
      #define VLAN_PRIO_SHIFT  13
      #define VLAN_CFI_MASK    0x1000 /* 规范格式指示器 / 丢弃合格指示器 */
      #define VLAN_VID_MASK    0x0fff /* VLAN 标识符 */
      #define VLAN_N_VID       4096

-  **驱动**：``drivers/net/vlan.c``

配置选项
=====================

``CONFIG_NET_VLAN``
  启用 802.1Q VLAN 接口支持。
``CONFIG_NET_VLAN_COUNT``
  每个物理以太网接口的最大 VLAN 接口数量。

使用
=====

.. code-block:: c

  #include <nuttx/net/vlan.h>
  #include "netutils/netlib.h"

  /* 创建 VLAN 接口 (eth0.100, VLAN ID 100) */

  FAR const char *ifname = "eth0";
  uint16_t vlanid = 100;
  uint8_t priority = 0; /* 默认 PCP */

  int sockfd = socket(NET_SOCK_FAMILY, NET_SOCK_TYPE, NET_SOCK_PROTOCOL);

  if (sockfd >= 0)
   {
      struct vlan_ioctl_args ifv;

      strncpy(ifv.vlan_devname, ifname, sizeof(ifv.device1));
      ifv.u.VID  = vlanid;
      ifv.vlan_qos = priority;
      ifv.cmd = ADD_VLAN_CMD;
      if (ioctl(sockfd, SIOCSIFVLAN, (unsigned long)&ifv) < 0)
        {
          /* 处理错误 */
        }
      close(sockfd);
   }

  /* 启用 VLAN 接口 */

  netdev_ifup("eth0.100");

.. code-block:: c

  #include <nuttx/net/vlan.h>
  #include "netutils/netlib.h"

  /* 删除 VLAN 接口 (eth0.100, VLAN ID 100) */

  FAR const char *ifname = "eth0.100";

  int sockfd = socket(NET_SOCK_FAMILY, NET_SOCK_TYPE, NET_SOCK_PROTOCOL);

  if (sockfd >= 0)
   {
      struct vlan_ioctl_args ifv;

      strncpy(ifv.vlan_devname, ifname, sizeof(ifv.device1));
      ifv.cmd = DEL_VLAN_CMD;
      if (ioctl(sockfd, SIOCSIFVLAN, (unsigned long)&ifv) < 0)
        {
          /* 处理错误 */
        }
      close(sockfd);
   }
