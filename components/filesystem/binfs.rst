=====
BINFS
=====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是 binfs 文件系统，它允许通过文件系统"伪执行" NSH 内置应用程序。binfs 文件系统可以通过启用以下配置选项来构建到系统中::

    CONFIG_BUILTIN=y
    CONFIG_FS_BINFS=y

然后可以通过 NSH 命令行挂载::

   mount -t binfs /bin

示例::

  NuttShell (NSH) NuttX-6.31
  nsh> hello
  nsh: hello: command not found

  nsh> mount -t binfs /bin
  nsh> ls /bin
  ls /bin
  /bin:
   hello

  nsh> /bin/hello
  Hello, World!!

