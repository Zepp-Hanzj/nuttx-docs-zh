=====================
多个 NSH 会话
=====================

.. warning:: 
    迁移自： 
    https://cwiki.apache.org/confluence/display/NUTTX/Multiple+NSH+Sessions

问： 
  我想在多个串口上运行 NuttShell，但还没有弄清楚怎么做；
  你能给我指出正确的方向吗？

答： 
  很简单。不要使用 ``apps/examples/nsh_main.c``。创建你自己的 main 函数，
  大致如下（为简洁起见省略了所有错误处理）。顺便说一下，这些都是标准的
  POSIX 内容，你只需搜索 `dup2` 或 `I/O 重定向` 就能获得详细信息：

.. code-block:: c

   int my_main(int argc, char **argv)
   {
     const char *tty = argv[1];
     int fd = open(tty, O_RDWR);
     (void)dup2(fd, 0);
     (void)dup2(fd, 1);
     (void)dup2(fd, 2);
     close(fd);
     ...
   }

其余部分与原始 ``nsh_main()`` 函数相同（实际上，或许现有的
``nsh_main()`` 函数可以选择性地扩展为接受控制台设备字符串？）。
然后你可以在任何 TTY 上启动新的 NSH 会话，例如：

.. code-block:: none

   nsh> mynsh /dev/ttyS2 &

这将导致一个新的 NSH 会话出现在 ``ttyS2`` 上。该会话将一直持续，
直到你在新会话中执行以下操作：

.. code-block:: none

   nsh> exit

然后新会话，即 ``my_main()`` 将退出。

如果你执行类似以下的操作：

.. code-block:: none

   nsh> mynsh /dev/console

那么你将在同一个控制台上获得嵌套的 NSH 会话。第一个会话将暂停并
等待第二个会话接管控制台，直到它退出。然后第一个会话将重新接管控制台。

NuTTY
=====

在之前的讨论中，有人提到在 NuttX 中实现类似 getty 的功能
（当然，它会被命名为 "nutty"）。nutty 的简单实现方式如下：

1. 它将在每个（已配置的）串口设备上使用 ``poll()`` 等待。
2. 每当被唤醒时，它将在活动的串口上启动类似 ``my_main()`` 的程序。
3. NSH 有一个选项可以启用登录功能，但最好将现有的登录信息从 NSH 中
   移除，并将其集中在 nutty 中。

这样，你可以连接到任何 TTY，按回车键，然后就会获得一个 NSH 会话。
嗯……目前还不清楚 nutty 在会话关闭后如何回收 TTY。这部分可能需要
进一步的思考。

其他想法
===========

还有其他方式可以获得多个 NSH 会话：

- Telnet 已经支持多个会话。
- 将现有的 NSH 实现为 ELF 程序，然后你可以通过 ``posix_spawn`` 
  简单地重定向 I/O 来获得多个 NSH 会话。
- 使用 tiny NxWM 窗口管理器，已经支持多个 NSH 窗口。
