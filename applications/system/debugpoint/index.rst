=====================================
``debugpoint`` 调试工具
=====================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``CONFIG_SYSTEM_DEBUGPOINT=y``

``debugpoint`` 工具是一个用于测试和管理系统中调试点（断点和监视点）的工具。
它允许用户设置、移除和测试各种类型的调试点。

用法::

    debugpoint [options]

选项::

    -r addr  在地址处设置读监视点
    -w addr  在地址处设置写监视点
    -b addr  在地址处设置断点
    -x addr  在地址处设置读写监视点
    -c       取消监视点或断点（必须与 -r、-w、-b 或 -x 一起使用）
    -l len   设置监视长度（必须与 -r、-w、-b 或 -x 一起使用）

示例::

    # 在地址 0x1000 处设置读监视点
    debugpoint -r 0x1000

    # 在地址 0x2000 处设置写监视点
    debugpoint -w 0x2000

    # 在地址 0x3000 处设置断点
    debugpoint -b 0x3000

    # 在地址 0x4000 处设置读写监视点
    debugpoint -x 0x4000

    # 取消地址 0x1000 处的读监视点
    debugpoint -r 0x1000 -c

    # 取消地址 0x2000 处的写监视点
    debugpoint -w 0x2000 -c

    # 取消地址 0x3000 处的断点
    debugpoint -b 0x3000 -c

    # 取消地址 0x4000 处的读写监视点
    debugpoint -x 0x4000 -c

    # 为地址 0x1000 处的读监视点设置 8 字节监视长度
    debugpoint -r 0x1000 -l 8

    # 为地址 0x2000 处的写监视点设置 8 字节监视长度
    debugpoint -w 0x2000 -l 8

    # 为地址 0x3000 处的断点设置 8 字节监视长度
    debugpoint -b 0x3000 -l 8

``debug`` 工具还包含断点和监视点的自动化测试。当不使用任何选项运行时，
它将执行这些测试以验证调试点的功能。
