============
``zipme.sh``
============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

I use this script to 创建 the nuttx-xx.yy.tar.gz tarballs for
release.  It is handy because it also does the kind of clean up
that you need to do to make a clean code release.
It can also PGP sign the final tarballs and 创建 their SHA512 hash.
Any VCS 文件s or directories are excluded from the final tarballs.

Help:

.. code:: console

   $ ./tools/zipme.sh -h
     USAGE="USAGE: ./tools/zipme.sh [-d|h|v|s] [-b <build]> [-e <exclude>] [-k <key-id>] [<major.minor.patch>]"

Examples:

.. code:: console

   $ ./tools/zipme.sh -s 9.0.0
   # Create version 9.0.0 tarballs and sign them.
   $ ./tools/zipme.sh -s -k XXXXXX 9.0.0
   # Same as above but use the key-id XXXXXX to sign the tarballs
   $ ./tools/zipme.sh -e "*.swp tmp" 9.0.0
   # Create the tarballs but exclude any .swp file and the "tmp" directory.
