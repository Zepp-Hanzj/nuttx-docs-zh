==================================
``netlib`` 网络支持库
==================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``netlib`` 库提供了一组网络实用函数，用于管理网络接口、IP 地址、路由表和其他网络相关操作。这些函数定义在 ``netutils/netlib.h`` 中，仅供 NuttX 应用程序内部使用。

设备管理
==================

  - :c:func:`netlib_get_devices`

.. c:function:: ssize_t netlib_get_devices(struct netlib_device_s *devlist, unsigned int nentries, sa_family_t family)

  获取所有网络设备的列表。

  :param devlist: 指向 ``netlib_device_s`` 结构体数组的指针，用于接收设备列表。
  :param nentries: 数组中的最大条目数。
  :param family: 地址族过滤器（``AF_INET``、``AF_INET6`` 或 ``AF_UNSPEC`` 表示全部）。

  :return: 成功时返回设备数量；出错时返回 -1，``errno`` 被适当设置。

地址转换函数
=============================

  - :c:func:`netlib_ipv4addrconv`
  - :c:func:`netlib_ethaddrconv`

.. c:function:: bool netlib_ipv4addrconv(const char *addrstr, uint8_t *addr)

  将 IPv4 地址的文本表示形式转换为数值表示形式。此函数接受 ``a.b.c.d`` 形式的 IP 地址并将其转换为 4 字节数组。

  :param addrstr: 指向包含文本形式 IP 地址的字符串的指针。
  :param addr: 指向 4 字节数组的指针，将被填充为地址的数值表示。

  :return: 如果 IP 地址解析成功返回 ``true``；否则返回 ``false``。

.. c:function:: bool netlib_ethaddrconv(const char *hwstr, uint8_t *hw)

  将以太网 MAC 地址的文本表示形式转换为数值表示形式。

  :param hwstr: 指向包含文本形式 MAC 地址的字符串的指针（例如 ``"00:11:22:33:44:55"``）。
  :param hw: 指向字节数组的指针，将被填充为 MAC 地址的数值表示。

  :return: 如果 MAC 地址解析成功返回 ``true``；否则返回 ``false``。

MAC 地址管理
=======================

  - :c:func:`netlib_setmacaddr`
  - :c:func:`netlib_getmacaddr`

.. c:function:: int netlib_setmacaddr(const char *ifname, const uint8_t *macaddr)

  设置以太网网络接口的 MAC 地址。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param macaddr: 指向包含 MAC 地址的 6 字节数组的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_getmacaddr(const char *ifname, uint8_t *macaddr)

  获取以太网网络接口的 MAC 地址。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param macaddr: 指向 6 字节数组的指针，用于接收 MAC 地址。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

IPv4 地址管理
========================

  - :c:func:`netlib_set_ipv4addr`
  - :c:func:`netlib_get_ipv4addr`
  - :c:func:`netlib_set_dripv4addr`
  - :c:func:`netlib_get_dripv4addr`
  - :c:func:`netlib_set_ipv4netmask`
  - :c:func:`netlib_get_ipv4netmask`
  - :c:func:`netlib_ipv4adaptor`

.. c:function:: int netlib_set_ipv4addr(const char *ifname, const struct in_addr *addr)

  设置网络接口的 IPv4 地址。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param addr: 指向包含 IPv4 地址的 ``in_addr`` 结构体的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_get_ipv4addr(const char *ifname, struct in_addr *addr)

  获取网络接口的 IPv4 地址。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param addr: 指向 ``in_addr`` 结构体的指针，用于接收 IPv4 地址。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_set_dripv4addr(const char *ifname, const struct in_addr *addr)

  设置网络接口的默认路由器（网关）IPv4 地址。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param addr: 指向包含网关地址的 ``in_addr`` 结构体的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_get_dripv4addr(const char *ifname, struct in_addr *addr)

  获取网络接口的默认路由器（网关）IPv4 地址。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param addr: 指向 ``in_addr`` 结构体的指针，用于接收网关地址。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_set_ipv4netmask(const char *ifname, const struct in_addr *addr)

  设置网络接口的 IPv4 子网掩码。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param addr: 指向包含子网掩码的 ``in_addr`` 结构体的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_get_ipv4netmask(const char *ifname, struct in_addr *addr)

  获取网络接口的 IPv4 子网掩码。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param addr: 指向 ``in_addr`` 结构体的指针，用于接收子网掩码。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_ipv4adaptor(in_addr_t destipaddr, in_addr_t *srcipaddr)

  查找与目标地址通信时应使用的适当源 IPv4 地址。

  :param destipaddr: 目标 IPv4 地址（网络字节序）。
  :param srcipaddr: 指向用于接收源 IPv4 地址的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

IPv6 地址管理
========================

  - :c:func:`netlib_set_ipv6addr`
  - :c:func:`netlib_get_ipv6addr`
  - :c:func:`netlib_add_ipv6addr`
  - :c:func:`netlib_del_ipv6addr`
  - :c:func:`netlib_set_dripv6addr`
  - :c:func:`netlib_set_ipv6netmask`
  - :c:func:`netlib_ipv6adaptor`
  - :c:func:`netlib_ipv6netmask2prefix`
  - :c:func:`netlib_prefix2ipv6netmask`

.. c:function:: int netlib_set_ipv6addr(const char *ifname, const struct in6_addr *addr)

  设置网络接口的 IPv6 地址。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。对于多个地址可以包含槽位号（例如 ``"eth0:0"``）。
  :param addr: 指向包含 IPv6 地址的 ``in6_addr`` 结构体的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_get_ipv6addr(const char *ifname, struct in6_addr *addr)

  获取网络接口的 IPv6 地址。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。对于多个地址可以包含槽位号（例如 ``"eth0:0"``）。
  :param addr: 指向 ``in6_addr`` 结构体的指针，用于接收 IPv6 地址。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_add_ipv6addr(const char *ifname, const struct in6_addr *addr, uint8_t preflen)

  向网络接口添加 IPv6 地址。建议使用此函数来管理单个接口上的多个 IPv6 地址。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param addr: 指向包含 IPv6 地址的 ``in6_addr`` 结构体的指针。
  :param preflen: 前缀长度（0-128）。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_del_ipv6addr(const char *ifname, const struct in6_addr *addr, uint8_t preflen)

  从网络接口删除 IPv6 地址。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param addr: 指向包含要删除的 IPv6 地址的 ``in6_addr`` 结构体的指针。
  :param preflen: 前缀长度（0-128）。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_set_dripv6addr(const char *ifname, const struct in6_addr *addr)

  设置网络接口的默认路由器（网关）IPv6 地址。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param addr: 指向包含网关地址的 ``in6_addr`` 结构体的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_set_ipv6netmask(const char *ifname, const struct in6_addr *addr)

  设置网络接口的 IPv6 子网掩码。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param addr: 指向包含子网掩码的 ``in6_addr`` 结构体的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_ipv6adaptor(const struct in6_addr *destipaddr, struct in6_addr *srcipaddr)

  查找与目标地址通信时应使用的适当源 IPv6 地址。

  :param destipaddr: 指向目标 IPv6 地址的指针。
  :param srcipaddr: 指向用于接收源 IPv6 地址的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: uint8_t netlib_ipv6netmask2prefix(const uint16_t *mask)

  将 IPv6 子网掩码转换为前缀长度。

  :param mask: 指向表示子网掩码的 16 位数组的指针。

  :return: 前缀长度（0-128）。

.. c:function:: void netlib_prefix2ipv6netmask(uint8_t preflen, struct in6_addr *netmask)

  将前缀长度转换为 IPv6 子网掩码。

  :param preflen: 前缀长度（0-128）。
  :param netmask: 指向 ``in6_addr`` 结构体的指针，用于接收子网掩码。

网络接口管理
=============================

  - :c:func:`netlib_getifstatus`
  - :c:func:`netlib_ifup`
  - :c:func:`netlib_ifdown`
  - :c:func:`netlib_set_mtu`
  - :c:func:`netlib_check_ifconflict`

.. c:function:: int netlib_getifstatus(const char *ifname, uint8_t *flags)

  获取网络接口的状态标志。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param flags: 指向用于接收接口标志的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_ifup(const char *ifname)

  启动网络接口（激活它）。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_ifdown(const char *ifname)

  关闭网络接口（停用它）。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_set_mtu(const char *ifname, int mtu)

  设置网络接口的最大传输单元（MTU）。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。
  :param mtu: MTU 值，单位为字节。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_check_ifconflict(const char *ifname)

  检查网络接口的 IP 地址冲突状态。此函数从 procfs 文件系统（``/proc/net/<ifname>``）读取冲突状态，该状态由 ARP 地址冲突检测（ACD）模块填充。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。

  :return: 如果未检测到冲突返回 0；如果检测到冲突返回 1；出错返回负值，``errno`` 被适当设置。

网络缓冲区统计
==========================

  - :c:func:`netlib_get_iobinfo`

.. c:function:: int netlib_get_iobinfo(struct iob_stats_s *iob)

  获取网络 IOB（I/O 缓冲区）统计信息。此函数从 procfs 文件系统（``/proc/iobinfo``）读取 IOB 使用信息，该信息提供有关网络数据包缓冲池的详细信息。

  IOB 缓冲区被 NuttX 网络栈用于在传输和接收期间缓冲网络数据包。此函数允许监控 IOB 缓冲池以检测潜在的缓冲区耗尽或限流状况。

  :param iob: 指向 ``iob_stats_s`` 结构体的指针，用于接收 IOB 统计信息。该结构体包含以下字段：

              - ``ntotal``：配置的 IOB 缓冲区总数（``CONFIG_IOB_NBUFFERS``）
              - ``nfree``：当前可用的空闲 IOB 缓冲区数量
              - ``nwait``：等待 IOB 缓冲区的任务数量（当 ``nfree < 0`` 时）
              - ``nthrottle``：被限流的 IOB 缓冲区数量（当低于 ``CONFIG_IOB_THROTTLE`` 阈值时）

  :return: 成功返回 0；失败返回负值，``errno`` 被适当设置。

  **注意：** 此函数需要启用 ``CONFIG_MM_IOB``。IOB 统计信息由内核的 IOB 缓冲区管理系统提供，反映网络数据包缓冲池的当前状态。

网络连接
=====================

  - :c:func:`netlib_check_ipconnectivity`
  - :c:func:`netlib_check_ifconnectivity`
  - :c:func:`netlib_check_httpconnectivity`

.. c:function:: int netlib_check_ipconnectivity(FAR const char *ip, int timeout, int retry)

  使用 ICMP ping 检查到指定 IPv4 地址的网络连接。此函数向目标地址发送 ICMP 回显请求并计算收到的回复数。

  :param ip: 要检查的 IPv4 地址字符串（例如 ``"192.168.1.1"``）。如果为 ``NULL``，函数将使用通过 ``CONFIG_NETDB_DNSSERVER_IPv4ADDR`` 配置的默认 DNS 服务器地址（如果可用）。
  :param timeout: 每次 ping 尝试的最大超时时间（毫秒）。
  :param retry: 发送的 ping 尝试次数。

  :return: 成功时返回收到的回复数（0 或正数）。值为 0 表示未收到回复（网络不可达或超时）。负值表示发生错误（例如，如果 ``ip`` 为 ``NULL`` 且未配置 DNS 服务器则返回 ``-EINVAL``）。

  **注意：** 此函数需要启用 ``CONFIG_NETUTILS_PING``。该函数是阻塞的，将在返回前等待所有 ping 尝试完成。

.. c:function:: int netlib_check_ifconnectivity(FAR const char *ifname, int timeout, int retry)

  通过 ping 网关检查网络接口连接。此函数获取指定网络接口的默认网关地址，然后向网关发送 ICMP 回显请求以验证连接。

  :param ifname: 网络接口名称（例如 ``"eth0"``、``"wlan0"``）。
  :param timeout: 每次 ping 尝试的最大超时时间（毫秒）。
  :param retry: 发送的 ping 尝试次数。

  :return: 成功时返回网关 ping 回复数（0 或正数）。值为 0 表示未收到回复（网关不可达或超时）。负值表示发生错误（例如，如果无法获取接口的网关地址，或网关地址无效）。

  **注意：** 此函数需要启用 ``CONFIG_NETUTILS_PING``。该函数是阻塞的，将在返回前等待所有 ping 尝试完成。函数内部调用 :c:func:`netlib_get_dripv4addr` 获取网关地址，然后使用 :c:func:`netlib_check_ipconnectivity` 执行实际的 ping 测试。

.. c:function:: int netlib_check_httpconnectivity(FAR const char *host, FAR const char *getmsg, int port, int expect_code)

  通过发送 HTTP GET 请求并验证响应状态码来检查 HTTP 服务连接。此函数建立到指定主机和端口的 TCP 连接，发送 HTTP/1.1 GET 请求以获取指定路径，并验证服务器返回预期的 HTTP 状态码。

  :param host: 远程主机名或 IP 地址（例如 ``"www.example.com"`` 或 ``"192.168.1.1"``）。如果启用了 ``CONFIG_LIBC_NETDB``，函数支持 DNS 解析，否则期望数字 IPv4 地址。
  :param getmsg: HTTP GET 请求的 URL 路径（例如 ``"index.html"`` 或 ``"api/health"``）。空字符串（``""``）请求根路径（``"/"``）。函数会自动在路径前添加正斜杠。
  :param port: HTTP 服务器的 TCP 端口号（通常 HTTP 为 80，替代 HTTP 服务为 8080）。
  :param expect_code: 预期的 HTTP 状态码（例如 ``200`` 表示成功，``404`` 表示未找到）。函数仅在服务器返回完全匹配的状态码时返回成功。

  :return: 成功返回 0（HTTP 状态码与预期值匹配）。失败返回负值，如果服务器返回的状态码与预期不同，可能是负的 HTTP 状态码（例如 ``-404``）；如果连接、DNS 解析或其他错误发生，可能是负的错误码（例如 ``-EINVAL``、``-ENETUNREACH``）。

  **注意：** 此函数是阻塞的，将等待 HTTP 请求和响应完成。函数仅读取 HTTP 响应的前 256 字节以提取状态码。它不支持 HTTPS（TLS/SSL），仅适用于 HTTP/1.1 服务器。该函数可用于 HTTP 服务健康检查、网络诊断和自动化服务监控。

ARP 表支持
==================

  - :c:func:`netlib_set_arpmapping`
  - :c:func:`netlib_get_arpmapping`
  - :c:func:`netlib_del_arpmapping`
  - :c:func:`netlib_get_arptable`

.. c:function:: int netlib_set_arpmapping(const struct sockaddr_in *inaddr, const uint8_t *macaddr, const char *ifname)

  添加或更新将 IPv4 地址映射到 MAC 地址的 ARP 表条目。

  :param inaddr: 指向包含 IPv4 地址的 ``sockaddr_in`` 结构体的指针。
  :param macaddr: 指向包含 MAC 地址的 6 字节数组的指针。
  :param ifname: 网络接口名称（例如 ``"eth0"``），或 NULL 表示任意接口。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_get_arpmapping(const struct sockaddr_in *inaddr, uint8_t *macaddr, const char *ifname)

  从 ARP 表中检索与 IPv4 地址关联的 MAC 地址。

  :param inaddr: 指向包含 IPv4 地址的 ``sockaddr_in`` 结构体的指针。
  :param macaddr: 指向 6 字节数组的指针，用于接收 MAC 地址。
  :param ifname: 网络接口名称（例如 ``"eth0"``），或 NULL 表示任意接口。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_del_arpmapping(const struct sockaddr_in *inaddr, const char *ifname)

  从 ARP 表中删除条目。

  :param inaddr: 指向包含 IPv4 地址的 ``sockaddr_in`` 结构体的指针。
  :param ifname: 网络接口名称（例如 ``"eth0"``），或 NULL 表示任意接口。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: ssize_t netlib_get_arptable(struct arpreq *arptab, unsigned int nentries)

  检索整个 ARP 表。

  :param arptab: 指向 ``arpreq`` 结构体数组的指针，用于接收 ARP 表条目。
  :param nentries: 数组中的最大条目数。

  :return: 成功时返回条目数；出错返回 -1，``errno`` 被适当设置。

路由表支持
======================

  - :c:func:`netlib_ipv4router`
  - :c:func:`netlib_ipv6router`
  - :c:func:`netlib_open_ipv4route`
  - :c:func:`netlib_close_ipv4route`
  - :c:func:`netlib_read_ipv4route`
  - :c:func:`netlib_open_ipv6route`
  - :c:func:`netlib_close_ipv6route`
  - :c:func:`netlib_read_ipv6route`
  - :c:func:`netlib_get_route`

.. c:function:: int netlib_ipv4router(const struct in_addr *destipaddr, struct in_addr *router)

  查找用于到达目标 IPv4 地址的路由器（网关）地址。

  :param destipaddr: 指向目标 IPv4 地址的指针。
  :param router: 指向用于接收路由器 IPv4 地址的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_ipv6router(const struct in6_addr *destipaddr, struct in6_addr *router)

  查找用于到达目标 IPv6 地址的路由器（网关）地址。

  :param destipaddr: 指向目标 IPv6 地址的指针。
  :param router: 指向用于接收路由器 IPv6 地址的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: FILE *netlib_open_ipv4route(void)

  打开 IPv4 路由表以供读取。这是一个打开 ``/proc/net/route/ipv4`` 的宏。

  :return: 成功返回文件指针；出错返回 NULL。

.. c:function:: void netlib_close_ipv4route(FILE *stream)

  关闭 IPv4 路由表文件。这是一个调用 ``fclose()`` 的宏。

  :param stream: ``netlib_open_ipv4route()`` 返回的文件指针。

.. c:function:: ssize_t netlib_read_ipv4route(FILE *stream, struct netlib_ipv4_route_s *route)

  从 IPv4 路由表读取一个条目。

  :param stream: ``netlib_open_ipv4route()`` 返回的文件指针。
  :param route: 指向 ``netlib_ipv4_route_s`` 结构体的指针，用于接收路由条目。

  :return: 成功返回 1；文件末尾返回 0；出错返回 -1。

.. c:function:: FILE *netlib_open_ipv6route(void)

  打开 IPv6 路由表以供读取。这是一个打开 ``/proc/net/route/ipv6`` 的宏。

  :return: 成功返回文件指针；出错返回 NULL。

.. c:function:: void netlib_close_ipv6route(FILE *stream)

  关闭 IPv6 路由表文件。这是一个调用 ``fclose()`` 的宏。

  :param stream: ``netlib_open_ipv6route()`` 返回的文件指针。

.. c:function:: ssize_t netlib_read_ipv6route(FILE *stream, struct netlib_ipv6_route_s *route)

  从 IPv6 路由表读取一个条目。

  :param stream: ``netlib_open_ipv6route()`` 返回的文件指针。
  :param route: 指向 ``netlib_ipv6_route_s`` 结构体的指针，用于接收路由条目。

  :return: 成功返回 1；文件末尾返回 0；出错返回 -1。

.. c:function:: ssize_t netlib_get_route(struct rtentry *rtelist, unsigned int nentries, sa_family_t family)

  使用 Netlink 检索路由表条目。

  :param rtelist: 指向 ``rtentry`` 结构体数组的指针，用于接收路由条目。
  :param nentries: 数组中的最大条目数。
  :param family: 地址族过滤器（``AF_INET``、``AF_INET6`` 或 ``AF_UNSPEC`` 表示全部）。

  :return: 成功时返回条目数；出错返回 -1，``errno`` 被适当设置。

DHCP 支持
=============

  - :c:func:`netlib_obtain_ipv4addr`
  - :c:func:`netlib_icmpv6_autoconfiguration`
  - :c:func:`netlib_obtain_ipv6addr`

.. c:function:: int netlib_obtain_ipv4addr(const char *ifname)

  通过 DHCP 为指定网络接口获取 IPv4 地址。此函数阻塞直到获取到地址或发生错误。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_icmpv6_autoconfiguration(const char *ifname)

  为指定网络接口执行 IPv6 无状态地址自动配置（SLAAC）。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_obtain_ipv6addr(const char *ifname)

  通过 DHCPv6 为指定网络接口获取 IPv6 地址。

  :param ifname: 网络接口名称（例如 ``"eth0"``）。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

DNS 服务器地址管理
===============================

  - :c:func:`netlib_set_ipv4dnsaddr`
  - :c:func:`netlib_del_ipv4dnsaddr`
  - :c:func:`netlib_del_ipv4dnsaddr_by_index`
  - :c:func:`netlib_set_ipv6dnsaddr`
  - :c:func:`netlib_del_ipv6dnsaddr`
  - :c:func:`netlib_del_ipv6dnsaddr_by_index`

.. c:function:: int netlib_set_ipv4dnsaddr(const struct in_addr *inaddr)

  向解析器配置添加 IPv4 DNS 服务器地址。

  :param inaddr: 指向包含 DNS 服务器地址的 ``in_addr`` 结构体的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_del_ipv4dnsaddr(const struct in_addr *inaddr)

  从解析器配置中删除 IPv4 DNS 服务器地址。

  :param inaddr: 指向包含要删除的 DNS 服务器地址的 ``in_addr`` 结构体的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_del_ipv4dnsaddr_by_index(int index)

  按索引从解析器配置中删除 IPv4 DNS 服务器。

  :param index: 要删除的 DNS 服务器的索引（从 0 开始）。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_set_ipv6dnsaddr(const struct in6_addr *inaddr)

  向解析器配置添加 IPv6 DNS 服务器地址。

  :param inaddr: 指向包含 DNS 服务器地址的 ``in6_addr`` 结构体的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_del_ipv6dnsaddr(const struct in6_addr *inaddr)

  从解析器配置中删除 IPv6 DNS 服务器地址。

  :param inaddr: 指向包含要删除的 DNS 服务器地址的 ``in6_addr`` 结构体的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_del_ipv6dnsaddr_by_index(int index)

  按索引从解析器配置中删除 IPv6 DNS 服务器。

  :param index: 要删除的 DNS 服务器的索引（从 0 开始）。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

无线配置
=======================

  - :c:func:`netlib_getessid`
  - :c:func:`netlib_setessid`

.. c:function:: int netlib_getessid(const char *ifname, char *essid, size_t idlen)

  获取无线网络接口的 ESSID（网络名称）。

  :param ifname: 无线网络接口名称（例如 ``"wlan0"``）。
  :param essid: 接收 ESSID 字符串的缓冲区。
  :param idlen: 缓冲区大小。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_setessid(const char *ifname, const char *essid)

  设置无线网络接口的 ESSID（网络名称）。

  :param ifname: 无线网络接口名称（例如 ``"wlan0"``）。
  :param essid: 要设置的 ESSID 字符串。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

URL 解析
============

  - :c:func:`netlib_parsehttpurl`
  - :c:func:`netlib_parseurl`

.. c:function:: int netlib_parsehttpurl(const char *url, uint16_t *port, char *hostname, int hostlen, char *filename, int namelen)

  将 HTTP URL 解析为其组成部分。

  :param url: 要解析的 URL 字符串（例如 ``"http://example.com:8080/path/file"``）。
  :param port: 指向用于接收端口号的指针（未指定时默认为 80）。
  :param hostname: 接收主机名的缓冲区。
  :param hostlen: 主机名缓冲区大小。
  :param filename: 接收路径/文件名的缓冲区。
  :param namelen: 文件名缓冲区大小。

  :return: 成功返回 0；出错返回 -1。

.. c:function:: int netlib_parseurl(const char *str, struct url_s *url)

  将通用 URL 解析为其组成部分。此函数处理 HTTP 之外的各种 URL 方案。

  :param str: 要解析的 URL 字符串。
  :param url: 指向 ``url_s`` 结构体的指针，用于接收解析后的组成部分。

  :return: 成功返回 0；出错返回 -1。

服务器支持
===============

  - :c:func:`netlib_listenon`
  - :c:func:`netlib_server`

.. c:function:: int netlib_listenon(uint16_t portno)

  创建 TCP 套接字并在指定端口上监听。这是一个用于设置服务器套接字的便捷函数。

  :param portno: 要监听的端口号。

  :return: 成功返回套接字描述符；出错返回 -1，``errno`` 被适当设置。

.. c:function:: void netlib_server(uint16_t portno, pthread_startroutine_t handler, int stacksize)

  创建一个简单的服务器，在指定端口上监听，并为每个连接使用提供的处理函数生成一个新线程。

  :param portno: 要监听的端口号。
  :param handler: 每个新连接要调用的函数。处理函数接收客户端套接字描述符作为参数。
  :param stacksize: 处理线程的堆栈大小。

邻居表（IPv6）
======================

  - :c:func:`netlib_get_nbtable`

.. c:function:: ssize_t netlib_get_nbtable(struct neighbor_entry_s *nbtab, unsigned int nentries)

  检索 IPv6 邻居表（类似于 IPv4 的 ARP）。

  :param nbtab: 指向 ``neighbor_entry_s`` 结构体数组的指针，用于接收邻居表条目。
  :param nentries: 数组中的最大条目数。

  :return: 成功时返回条目数；出错返回 -1，``errno`` 被适当设置。

连接跟踪（Netfilter）
=================================

  - :c:func:`netlib_get_conntrack`
  - :c:func:`netlib_parse_conntrack`

.. c:function:: int netlib_get_conntrack(sa_family_t family, netlib_conntrack_cb_t cb)

  从内核的连接跟踪表中检索连接跟踪条目。

  :param family: 地址族过滤器（``AF_INET``、``AF_INET6`` 或 ``AF_UNSPEC`` 表示全部）。
  :param cb: 为每个连接调用的回调函数。回调接收指向 ``netlib_conntrack_s`` 结构体的指针。

  :return: 成功返回 0；出错返回 -1，``errno`` 被适当设置。

.. c:function:: int netlib_parse_conntrack(const struct nlmsghdr *nlh, size_t len, struct netlib_conntrack_s *ct)

  解析包含连接跟踪信息的 Netlink 消息。

  :param nlh: 指向 Netlink 消息头的指针。
  :param len: 消息长度。
  :param ct: 指向 ``netlib_conntrack_s`` 结构体的指针，用于接收解析后的连接信息。

  :return: 成功返回 0；出错返回 -1。
