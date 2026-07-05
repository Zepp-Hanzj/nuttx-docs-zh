=====
ZipFS
=====

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

Zipfs 是一个只读文件系统，通过 NuttX VFS 接口将 zip 文件挂载为 NuttX 文件系统。
这允许用户在解压缩的同时读取文件，无需额外的存储空间。

CONFIG
======

.. code-block:: bash

    CONFIG_FS_ZIPFS=y
    CONFIG_LIB_ZLIB=y

示例
=======

1. ``./tools/configure.sh sim:zipfs`` 构建支持 zipfs 的 sim 平台。

2. ``make`` 构建 NuttX。

3. ``./nuttx`` 运行 NuttX。

4. ``nsh> mount -t hostfs -o /home/<your host name>/work /host`` 挂载宿主目录到 ``/host``。

5. ``nsh> mount -t zipfs -o /host/test.zip /zip`` 挂载 zip 文件到 ``/zipfs``。

6. 使用 cat/ls 命令测试。

.. code-block:: bash

    nsh> ls /zip
    /zip:
     a/1
     a/2
    nsh> cat /zip/a/1
    this is zipfs test 1
    nsh> cat /zip/a/2
    this is zipfs test 2
