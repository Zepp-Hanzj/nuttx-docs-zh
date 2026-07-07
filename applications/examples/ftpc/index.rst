===================
``ftpc`` FTP 客户端
===================

这是一个简单的 FTP 客户端 shell，用于测试 FTPC 库（``apps/netutils/ftpc``）的功能。

在 NSH 中，启动命令序列如下。这只是一个示例，您的配置可能有不同的存储设备、挂载路径和 FTP 目录：

  nsh> mount -t vfat /dev/mmcsd0 /tmp  # 将 SD 卡挂载到 /tmp
  nsh> cd /tmp                         # 切换到 /tmp 目录
  nsh> ftpc <host> <port>              # 启动 FTP 客户端
  nfc> login <name> <password>         # 登录 FTP 服务器
  nfc> help                            # 查看 FTP 命令列表

其中 ``<host>`` 是 FTP 服务器的 IP 地址或主机名，``<port>`` 是可选的端口号。

**注意**：默认情况下，FTPC 使用 ``readline`` 从 ``stdin`` 获取数据。因此您的 defconfig 文件必须包含以下构建路径：

  CONFIG_SYSTEM_READLINE=y

**注意**：如果通过 telnet NSH 连接使用 ftpc 任务，则应设置以下配置项：

  CONFIG_EXAMPLES_FTPC_FGETS=y

默认情况下，FTPC 客户端使用 ``readline()`` 从控制台获取字符。Readline 包含命令行编辑器，并将从 stdin 接收到的字符回显到 ``stdout``。这两种行为在使用 Telnet 时都是不可取的。

您可能还需要在配置文件中定义以下内容，否则将无法获得任何运行反馈：

  CONFIG_DEBUG_FEATURES=y
  CONFIG_DEBUG_INFO=y
  CONFIG_DEBUG_FTPC=y
