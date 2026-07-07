===========================
\`\`igmp\`\` 简单 IGMP 测试
===========================

这是 NuttX IGMP 功能的简单测试。目前它并没有做太多有价值的事情——要验证 IGMP 功能还需要更多工作！

- ``CONFIG_EXAMPLES_IGMP_NOMAC`` – 如果硬件没有 MAC 地址则设置此项；系统将分配一个。
- ``CONFIG_EXAMPLES_IGMP_IPADDR`` – 目标板 IP 地址。
- ``CONFIG_EXAMPLES_IGMP_DRIPADDR`` – 默认路由器地址。
- ``CONFIG_EXAMPLES_IGMP_NETMASK`` – 网络掩码。
- ``CONFIG_EXAMPLES_IGMP_GRPADDR`` – 多播组地址。
- ``CONFIG_EXAMPLES_NETLIB`` – 需要网络库。
