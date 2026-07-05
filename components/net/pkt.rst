===========================
"原始" 数据包套接字支持
===========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

数据包套接字 (:c:macro:`AF_PACKET`) 允许在没有中间传输协议的情况下
接收和发送帧。接收到的帧在进入网络之前被复制到数据包套接字分接头中。
写入数据包套接字的数据将完全绕过网络，并被放置在网络接口驱动的
传输缓冲区中。

配置选项
=====================

``CONFIG_NET_PKT_PREALLOC_CONNS``
  预分配的数据包连接数（所有任务）。
``CONFIG_NET_PKT_ALLOC_CONNS``
  数据包连接的动态内存分配。
``CONFIG_NET_PKT_MAX_CONNS``
  数据包连接的最大数量。
``CONFIG_NET_PKT_WRITE_BUFFERS``
  为数据包套接字使用写缓冲区，支持 SOCK_NONBLOCK 模式。
``CONFIG_NET_PKTPROTO_OPTIONS``
  启用在数据包套接字上设置协议选项。

使用方法
=====

.. code-block:: c

  struct sockaddr_ll addr;
  uint8_t buffer[BUFSIZE];
  int sd = socket(AF_PACKET, SOCK_RAW, 0); /* 创建原始数据包套接字 */

  addr.sll_family = AF_PACKET;
  addr.sll_ifindex = if_nametoindex("eth0");
  addr.sll_protocol = htons(ETH_P_ALL);
  bind(sd, (FAR struct sockaddr *)&addr, sizeof(addr)); /* 绑定到设备 */

  recv(sd, buffer, sizeof(buffer), 0); /* read(sd, buffer, sizeof(buffer)); */
  send(sd, buffer, sizeof(buffer), 0); /* write(sd, buffer, sizeof(buffer)); */

  close(sd); /* 关闭套接字 */

.. code-block:: c

  struct sockaddr_ll addr;
  uint8_t buffer[BUFSIZE];
  int sd = socket(AF_PACKET, SOCK_DGRAM, 0); /* 创建 Dgram 数据包套接字 */

  addr.sll_family = AF_PACKET;
  addr.sll_ifindex = if_nametoindex("eth0");
  addr.sll_protocol = htons(ETH_P_IP);
  bind(sd, (FAR struct sockaddr *)&addr, sizeof(addr)); /* 绑定到设备 */

  recv(sd, buffer, sizeof(buffer), 0); /* read(sd, buffer, sizeof(buffer)); */

  memset(addr.sll_addr, 0xff, sizeof(addr.sll_addr)); /* 目标 MAC 地址 */
  addr.sll_halen = ETH_ALEN;
  sendto(sd, buffer, sizeof(buffer), 0, /* SOCK_DGRAM 不能使用 write() */
         (struct sockaddr *)&addr, sizeof(addr));

  close(sd); /* 关闭套接字 */

.. code-block:: c

    int sd;
    struct packet_mreq mreq;
    char macaddr[ETH_ALEN] = {0x91, 0xe0, 0xf0, 0x00, 0x0e, 0x01};

    sd = socket(AF_PACKET, SOCK_RAW, 0);

    mreq.mr_ifindex = if_nametoindex("eth0");
    mreq.mr_type = PACKET_MR_MULTICAST;
    mreq.mr_alen = ETH_ALEN;
    memcpy(&mreq.mr_address, macaddr, ETH_ALEN);

    setsockopt(sd, SOL_PACKET, PACKET_ADD_MEMBERSHIP, &mreq,
               sizeof(struct packet_mreq));

    close(sd);
