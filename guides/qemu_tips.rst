=========
QEMU 技巧
=========

使用 TAP 设备进行网络连接
==========================

步骤 1：使用 ``NETUTILS_NETINIT`` 配置 NuttX 网络::

  CONFIG_NETUTILS_NETINIT=y
  CONFIG_NETINIT_IPADDR=0xc0a80868   # 目标：192.168.8.104
  CONFIG_NETINIT_DRIPADDR=0xc0a80801 # 路由器：192.168.8.1
  CONFIG_NETINIT_NETMASK=0xffffff00  # 掩码：255.255.255.0

步骤 2：在主机上创建和配置 TAP 设备::

  # 创建网桥
  sudo ip link add name br0 type bridge
  sudo ip link set br0 up

  # 创建 tap 接口
  sudo ip tuntap add dev tap0 mode tap
  sudo ip link set tap0 master br0
  sudo ip link set tap0 up

  # （可选）如果你想要局域网访问，也可以附加你的真实网卡
  # sudo ip link set enp3s0 master br0

  # 为 *网桥* 分配 IP
  sudo ip addr add 192.168.8.1/24 dev br0

步骤 3：使用 TAP 接口启动 QEMU::

  qemu-system-x86_64 -m 2G -smp 4 -cpu host -enable-kvm \
  -kernel nuttx -nographic -serial mon:stdio \
  -device e1000,netdev=mynet0 \
  -netdev tap,id=mynet0,ifname=tap0,script=no,downscript=no

步骤 4：清理::

  sudo ip link set tap0 down
  sudo ip link set br0 down
  sudo ip tuntap del dev tap0 mode tap
  sudo ip link del br0
