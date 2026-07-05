=======
Inotify
=======

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Inotify 是一个内核子系统，用于监视文件系统事件。它使应用程序能够实时监视文件和目录的更改，如创建、删除、修改、重命名等。inotify 提供了一种高效的方式来检测文件系统中的变化，无需轮询，从而节省系统资源。

CONFIG
------
.. code-block:: c

    COFNIG_FS_NOTIFY=y

用户空间 API
--------------

所有 inotify 用户接口都在文件 ``include/sys/inotify.h`` 中声明。用法与 Linux 版本一致。

.. c:function:: int inotify_init(void)

  初始化一个新的 inotify 实例并返回与新的 inotify 事件队列关联的文件描述符。

.. c:function:: int inotify_init1(int flags)

  inotify_init1 是 inotify_init 的扩展版本，提供用于初始化 inotify 实例的附加选项。与 inotify_init 不同，inotify_init1 允许您指定某些标志来控制 inotify 实例的行为。

.. c:function:: int inotify_add_watch(int fd, FAR const char *pathname, uint32_t mask)

  为位置由 pathname 指定的文件添加新的监视或修改现有的监视；调用者必须对此文件具有读权限。fd 参数是引用要修改其监视列表的 inotify 实例的文件描述符。要监视 pathname 的事件由 mask 位掩码参数指定。

.. c:function:: int inotify_rm_watch(int fd, uint32_t wd)

  从与文件描述符 fd 关联的 inotify 实例中移除与监视描述符 wd 关联的监视。

从 inotify 文件描述符读取事件
----------------------------------------------

要确定发生了什么事件，应用程序从 inotify 文件描述符读取。如果到目前为止没有事件发生，则假设是阻塞文件描述符，read 将阻塞直到至少一个事件发生。

每次成功的读取返回一个包含以下一个或多个结构的缓冲区：

.. code-block:: c

  struct inotify_event {
    int      wd;       /* Watch descriptor */
    uint32_t mask;     /* Mask describing event */
    uint32_t cookie;   /* Unique cookie associating related
                         events (for rename(2)) */
    uint32_t len;      /* Size of name field */
    char     name[];   /* Optional null-terminated name */
  };

**wd** 标识发生此事件的监视。它是先前调用 inotify_add_watch 返回的监视描述符之一。

**mask** 包含描述所发生事件的位。

**cookie** 是一个唯一的整数，用于连接相关事件。目前，这仅用于重命名事件，并允许应用程序将产生的 IN_MOVED_FROM 和 IN_MOVED_TO 事件对连接起来。对于所有其他事件类型，cookie 被设置为 0。

**name** 字段仅当事件是针对被监视目录内的文件返回时才存在；它标识被监视目录内的文件名。此文件名以 null 结尾，可能包含额外的 null 字节（'\0'）以将后续读取对齐到合适的地址边界。

**len** 字段计算 name 中的所有字节，包括 null 字节；因此每个 inotify_event 结构的长度为 sizeof(struct inotify_event)+len。

inotify 事件
--------------
**inotify_add_watch** 的 mask 参数和读取 inotify 文件描述符时返回的 inotify_event 结构中的 mask 字段都是标识 inotify 事件的位掩码。在调用 inotify_add_watch 时可以在 mask 中指定以下位，并可能在 read 返回的 mask 字段中返回：

  **IN_ACCESS** : 文件被访问

  **IN_MODIFY** : 文件被修改（``write()`` 或 ``truncate()``）

  **IN_ATTRIB** : 元数据被更改

  **IN_OPEN** : 文件被打开

  **IN_CLOSE_WRITE** : 以写入方式打开的文件被关闭

  **IN_CLOSE_NOWRITE** : 未以写入方式打开的文件被关闭

  **IN_MOVED_FROM** : 文件从 X 移走

  **IN_MOVED_TO** : 文件移动到 Y

  **IN_CREATE** : 子文件被创建

  **IN_DELETE** : 子文件被删除

  **IN_DELETE_SELF** : 自身被删除

  **IN_MOVE_SELF** : 自身被移动

示例
--------
假设应用程序正在监视目录 ``dir`` 和文件 ``dir/myfile`` 的所有事件。下面的示例显示了将为这两个对象生成的一些事件。

  fd = open("dir/myfile", O_RDWR);
    为 ``dir`` 和 ``dir/myfile`` 生成 **IN_OPEN** 事件。

  read(fd, buf, count);
    为 ``dir`` 和 ``dir/myfile`` 生成 **IN_ACCESS** 事件。

  write(fd, buf, count);
    为 ``dir`` 和 ``dir/myfile`` 生成 **IN_MODIFY** 事件。

  fchmod(fd, mode);
    为 ``dir`` 和 ``dir/myfile`` 生成 **IN_ATTRIB** 事件。

注意
----
Inotify 文件描述符可以使用 select、poll 和 epoll 进行监视。当事件可用时，文件描述符指示为可读。
