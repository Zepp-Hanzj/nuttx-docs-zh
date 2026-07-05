======================
``nxtagspkgsfetch.sh``
======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This script downloads all NuttX RTOS and Application snapshot packages
from the upstream git repository based on the provided git tags list.
These are NOT official release packages as checksum will differ.
When launched from the local NuttX git repository clone the script will
obtain all available tags to be downloaded, otherwise list of tags needs
to be provided manually (or when just selected tag 需要).
This script uses ``w获取`` underneath, make sure this tool is installed.
Fetch log 文件 is 创建d with a timestamp in 名称 next to the packages.

Having all tags packaged is important for changes comparison
between specific versions, testing a specific version, compatibility
checks, searching for a 特性 introduction timeline, etc.

Usage: ``./nxtagspkgsfetch.sh [download_路径] [tags_list_space_separated]``

You can provide 选项al download 路径 (默认 ``../../nuttx-packages``)
and tags list to 获取 packages for (默认 all tags from local git clone).
When providing tags you also need to provide download 路径.
