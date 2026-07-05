===========
Shell 登录
===========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

启用 Shell 登录
=====================

NuttShell 会话可以通过要求用户在会话开始时提供用户名和密码凭据来保护。
可以使用以下方式为标准 USB 或串口控制台启用登录::

  CONFIG_NSH_CONSOLE_LOGIN=y

可以使用以下方式单独为 Telnet 会话启用登录::

  CONFIG_NSH_TELNET_LOGIN=y

可以为一种或两种会话类型启用登录。成功登录后，用户将有权访问 NSH 会话::

  login: admin
  password:
  User Logged-in!

  NuttShell (NSH)
  nsh>

每次登录尝试失败后，可以设置延迟。此延迟的目的是阻止暴力破解密码的尝试。
该延迟通过以下方式配置::

  CONFIG_NSH_LOGIN_FAILDELAY=0

此设置提供登录失败延迟，以毫秒为单位。系统将在每次登录尝试失败后暂停此时间。
在一定次数的登录尝试失败后，会话将被关闭。该次数由以下控制::

  CONFIG_NSH_LOGIN_FAILCOUNT=3

凭据验证
===========================

NSH 可以配置三种方式在登录时验证用户凭据：

  #. 最简单的实现只是使用固定的登录凭据，通过以下方式选择::

      CONFIG_NSH_LOGIN_FIXED=y

     固定登录凭据通过以下方式选择::

      CONFIG_NSH_LOGIN_USERNAME=admin
      CONFIG_NSH_LOGIN_PASSWORD="Administrator"

     这不是很灵活，因为只能有一个用户，并且密码固定在 FLASH 映像中。
     此选项也不是很安全，因为恶意用户只需查看 flash 映像中的 ``.text``
     字符串即可获取密码。

  #. NSH 还可以配置为使用此设置将整个用户凭据验证推迟到特定于平台的逻辑::

      CONFIG_NSH_LOGIN_PLATFORM=y

     在这种情况下，NSH 将调用特定于平台的函数来执行用户凭据验证。
     特定于平台的逻辑必须提供具有以下原型的函数：

     .. code-block:: c

       int platform_user_verify(FAR const char *username, FAR const char *password);

     其原型和描述在 ``apps/include/nsh.h`` 中，可以这样包含：

     .. code-block:: c

      #include <apps/nsh.h>

     实现此函数的合适位置可能在 ``apps/platform/<board>`` 目录中。

  #. 最后一个选项是使用包含加密密码信息的密码文件。此最终选项通过以下方式选择，
     并在下面的段落中更详细地描述::

       CONFIG_NSH_LOGIN_PASSWD=y

密码文件
==============

NuttX 还可以配置为支持密码文件，默认位置为 ``/etc/passwd``。此选项启用密码文件支持::

  CONFIG_NSH_LOGIN_PASSWD=y

此选项要求您已选择 ``CONFIG_FSUTILS_PASSWD=y`` 以启用 ``apps/fsutils/passwd`` 的访问方法::

  CONFIG_FSUTILS_PASSWD=y

这确定了密码文件在挂载卷中的位置::

  CONFIG_FSUTILS_PASSWD_PATH="/etc/passwd"

``/etc/passwd`` 是*标准*位置，但您需要在有挂载卷的地方定位密码文件。

密码文件可以是 ROMFS 文件系统中的固定用户列表，也可以是维护在某个可写文件系统中的可修改
列表。如果密码文件位于 ROMFS 等只读文件系统中，则还应指示密码文件为只读。

  CONFIG_FSUTILS_PASSWD_READONLY=y

如果密码文件是可写的，则将启用额外的 NSH 命令来修改密码文件：
```useradd`` <#cmduseradd>`__、```userdel`` <#cmduserdel>`__ 和
```passwd`` <#cmdpasswd>`__。如果您不希望这些命令可用，则应专门禁用它们。

密码文件逻辑需要一些额外的设置：

  #. 用于文件访问的动态分配和释放缓冲区的大小::

       CONFIG_FSUTILS_PASSWD_IOBUFFER_SIZE=512

  #. 以及 128 位加密密钥。密码文件当前使用小型加密算法（TEA），但可以扩展为
     使用更强大的算法。

        CONFIG_FSUTILS_PASSWD_KEY1=0x12345678
        CONFIG_FSUTILS_PASSWD_KEY2=0x9abcdef0
        CONFIG_FSUTILS_PASSWD_KEY3=0x12345678
        CONFIG_FSUTILS_PASSWD_KEY4=0x9abcdef0

密码只能通过访问此密钥来解密。请注意，此密钥可能从您的 FLASH 映像中被提取出来，
但没有任何符号信息，这将是一项困难的工作，因为 TEA 密钥是二进制数据，无法与
FLASH 映像中的其他二进制数据区分开来。

如果启用了密码文件（``CONFIG_NSH_LOGIN_PASSWD=y``），则固定用户凭据将不用于
NSH 会话登录。相反，将查阅密码文件以验证用户凭据。

为 ROMFS 文件系统创建密码文件
================================================

我们想要实现的是一个挂载在 ``/etc`` 的 ROMFS 文件系统，其中包含密码文件 ``passwd``，如::

  NuttShell (NSH)
  nsh> ls -Rl /etc
  /etc:
   dr-xr-xr-x       0 .
   dr-xr-xr-x       0 init.d/
   -r--r--r--      39 passwd
  /etc/init.d:
   dr-xr-xr-x       0 ..
   -r--r--r--     110 rcS
   -r--r--r--     110 rc.sysinit
  nsh>

其中 ``/etc/init.d/rc.sysinit`` 是系统初始化脚本，``/etc/init.d/rcS`` 是启动脚本；
``/etc/passwd`` 是密码文件。请注意，这里我们假设您已经在使用启动脚本。然后我们可以
将 passwd 文件嵌入到为 NSH 启动文件挂载的 ``/etc`` 文件系统中，如上 `上面 <#custinit>`__ 所述。

sim/nsh 配置可用于创建新的密码文件，但也可以使用其他配置。该配置已经支持 ROMFS 文件系统、
密码和登录提示。首先对该配置进行以下更改。

  #. 禁用登录：

    .. code-block:: diff

      - CONFIG_NSH_CONSOLE_LOGIN=y
      + # CONFIG_NSH_CONSOLE_LOGIN is not set
        # CONFIG_NSH_TELNET_LOGIN is not set

  #. 将密码文件移动到可写文件系统：

    .. code-block:: diff

      - CONFIG_FSUTILS_PASSWD_PATH="/etc/passwd"
      + CONFIG_FSUTILS_PASSWD_PATH="/tmp/passwd"

  #. 使密码文件可修改

    .. code-block:: diff

      - CONFIG_FSUTILS_PASSWD_READONLY=y
      # CONFIG_FSUTILS_PASSWD_READONLY is not set

现在重新构建模拟。进入 shell 应该不需要登录，您应该在帮助摘要中找到
```useradd`` <#cmduseradd>`__、```userdel`` <#cmduserdel>`__ 和
```passwd`` <#cmdpasswd>`__ 命令（如果它们已启用）。确保 ``useradd``
命令未被禁用::

  # CONFIG_NSH_DISABLE_USERADD is not set

使用 NSH ```useradd`` <#cmduseradd>`__ 命令添加具有新用户密码的新用户，如::

  nsh> useradd <username> <password>

您可以按需多次执行此操作。每次执行此操作时，都会向 ``/tmp/passwd`` 的 ``passwd``
文件添加一个带加密密码的新条目。您可以这样查看密码文件的内容::

  nsh> cat /tmp/passwd

完成后，您可以简单地复制 ``cat`` 命令输出的 ``/tmp/passwd`` 内容并粘贴到编辑器中。
如果您使用 Windows，请确保删除可能出现在文件中的任何回车符。

然后按照下面的描述创建/重新创建 ``nsh_romfsimg.h`` 文件。

  #. ``nsh_romfsimg.h`` 头文件的内容从模板目录结构生成。创建目录结构::

      mkdir etc
      mkdir etc/init.d

     并将您现有的启动脚本复制到 ``etc/init.c`` 中作为 ``rcS``。

  #. 将新的密码文件保存在 ``etc/`` 目录中作为 ``passwd``。

  #. 创建新的 ROMFS 映像::

      genromfs -f romfs_img -d etc -V MyVolName

  #. 将 ROMFS 映像转换为 C 头文件::

      xxd -i romfs_img >nsh_romfsimg.h

  #. 编辑 ``nsh_romfsimg.h``：将两个数据定义都标记为 ``const``，以便数据存储在 FLASH 中。

  #. 编辑 nsh_romfsimg.h，将两个数据定义都标记为 ``const``，以便数据存储在 FLASH 中。

在 NSH 模拟配置中有一个很好的示例，位于
`boards/sim/sim/sim/configs/nsh <https://github.com/apache/nuttx/blob/master/boards/sim/sim/sim/configs/nsh/>`__。
ROMFS 支持文件在
`boards/sim/include <https://github.com/apache/nuttx/blob/master/boards/sim/sim/sim/include/>`__ 提供，
:doc:`/platforms/sim/sim/boards/sim/index` 页面提供了创建和修改 ROMFS 文件系统的详细信息。
