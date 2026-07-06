============
``zipme.sh``
============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

我使用此脚本为发布创建 nuttx-xx.yy.tar.gz 压缩包。
它很方便，因为它还执行制作干净代码发布所需的清理工作。
它还可以对最终的压缩包进行 PGP 签名并创建其 SHA512 哈希。
任何 VCS 文件或目录都会从最终的压缩包中排除。

帮助：

.. code:: console

   $ ./tools/zipme.sh -h
     USAGE="USAGE: ./tools/zipme.sh [-d|h|v|s] [-b <build]> [-e <exclude>] [-k <key-id>] [<major.minor.patch>]"

示例：

.. code:: console

   $ ./tools/zipme.sh -s 9.0.0
   # Create version 9.0.0 tarballs and sign them.
   $ ./tools/zipme.sh -s -k XXXXXX 9.0.0
   # Same as above but use the key-id XXXXXX to sign the tarballs
   $ ./tools/zipme.sh -e "*.swp tmp" 9.0.0
   # Create the tarballs but exclude any .swp file and the "tmp" directory.
