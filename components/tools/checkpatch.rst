.. _checkpatch.sh:

=================
.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``checkpatch.sh``
=================

``checkpatch.sh`` 是一个 bash 脚本，利用 ``nxstyle`` 和 ``codespell`` 工具
来格式化补丁并确保文件符合 NuttX 编码标准。它用于 NuttX 的 GitHub CI 中。

帮助信息：

.. code:: console

   $ tools/checkpatch.sh -h
   USAGE: tools/checkpatch.sh [options] [list|-]

   Options:
   -h
   -c spell check with codespell (install with: pip install codespell)
   -u encoding check with cvt2utf (install with: pip install cvt2utf)
   -r range check only (coupled with -p or -g)
   -p <patch file names> (default)
   -m Check commit message (coupled with -g)
   -g <commit list>
   -f <file list>
   -x format supported files (only .py, requires: pip install black)
   -  read standard input mainly used by git pre-commit hook as below:
      git diff --cached | ./tools/checkpatch.sh -
   Where a <commit list> is any syntax supported by git for specifying git revision, see GITREVISIONS(7)
   Where a <patch file names> is a space separated list of patch file names or wildcard. or *.patch
