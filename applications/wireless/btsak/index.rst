====================================
``btsak`` Bluetooth Swiss Army Knife
====================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

命令
--------

help::

  Command:      help
  Description:  显示总体命令帮助
  Usage:        bt <ifname> help

info::

  Command:      info
  Description:  显示蓝牙驱动信息
  Usage:        bt <ifname> info [-h]

features::

  Command:      features
  Description:  显示蓝牙驱动信息
  Usage:        bt <ifname> features [-h] [le]
  Where:        le - 选择 LE 特性而非 BR/EDR 特性

scan::

  Command:      scan
  Description:  蓝牙扫描命令
  Usage:        bt <ifname> scan [-h] <start [-d]|get|stop>
  Where:        start - 启动扫描。-d 选项启用重复过滤。
                get   - 显示新的累积扫描结果
                stop  - 停止扫描

advertise::

  Command:      advertise
  Description:  蓝牙广播命令
  Usage:        bt <ifname> advertise [-h] <start|stop>
  Where:        start - 启动广播
                stop  - 停止广播

security::

  Command:      security
  Description:  为连接启用安全性（加密）：
                如果设备已配对，将启用密钥加密。如果链路已使用足够强的密钥
                加密，此命令不执行任何操作。

                如果设备未配对，将启动配对。如果设备已配对但密钥太弱，
                而输入输出能力允许使用足够强的密钥，将启动配对。

                如果由于本地或远程设备限制（例如输入输出能力）无法达到
                所需的安全级别，此命令可能返回错误。

bt::

  Usage:        bt <ifname> security [-h] <addr> public|random <level>
  Where:        <addr>  - 已连接对端的 6 字节地址
                <level> - 安全级别，以下之一：

                  low     - 无加密且无认证
                  medium  - 有加密但无认证（无 MITM）
                  high    - 有加密且有认证（MITM）
                  fips    - 经认证的 LE 安全连接和加密

gatt::

  Command:      gatt
  Description:  通用属性（GATT）命令
  Usage:        bt <ifname> gatt [-h] <cmd> [option [option [option...]]]
  Where:        参见下方"GATT 命令"

GATT 命令
-------------

exchange-mtu::

  Command:      exchange-mtu
  Description:  将 MTU 设置为最大值并与对端协商 MTU
  Usage:        bt <ifname> gatt exchange-mtu [-h] <addr> public|random

mget::

  Command:      mget
  Description:  获取最后一次 GATT 'exchange-mtu' 命令的成功/失败结果
  Usage:        bt <ifname> gatt mget [-h]

discover::

  Command:      discover
  Description:  启动发现
  Usage:        bt <ifname> gatt discover [-h] <addr> public|random <uuid16> [<start> [<end>]]

characteristic::

  Command:      characteristic
  Description:  启动特征发现
  Usage:        bt <ifname> gatt characteristic [-h] <addr> public|random [<start> [<end>]]

descriptor::

  Command:      descriptor
  Description:  启动描述符发现
  Usage:        bt <ifname> gatt descriptor [-h] <addr> public|random [<start> [<end>]]

dget::

  Command:      dget
  Description:  获取最后一次发现操作的结果
  Usage:        bt <ifname> gatt dget [-h]

read::

  Command:      read
  Description:  启动 GATT 读操作。
  Usage:        bt <ifname> gatt read [-h] <addr> public|random <handle> [<offset>]

read-multiple::

  Command:      read-multiple
  Description:  启动 GATT 多次读操作。
  Usage:        bt <ifname> gatt read-multiple [-h] <addr> public|random <handle> [<handle> [<handle>]..]

rget::

  Command:      rget
  Description:  获取最后一次读操作的结果数据
  Usage:        bt <ifname> gatt rget [-h]

write::

  Command:      write
  Description:  启动 GATT 写操作。
  Usage:        bt <ifname> gatt write [-h] <addr> public|random <handle> <byte> [<byte> [<byte>]..]

wget::

  Command:      wget
  Description:  获取最后一次 GATT 'write' 命令的成功/失败结果
  Usage:        bt <ifname> gatt wget [-h]
