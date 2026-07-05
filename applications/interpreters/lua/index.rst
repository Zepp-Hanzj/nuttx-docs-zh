=======================
``lua`` Lua 解释器
=======================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

获取并构建 Lua 解释器。支持 5.2 到 5.4 版本。``lua`` 命令将被添加到 NSH 中。
Lua 可以运行给定路径的脚本、执行代码字符串，或在 NSH 控制台上打开与 readline 兼容的 REPL。
``<lua.h>`` 和 ``<lauxlib.h>`` 头文件可用于启动新的嵌入式解释器或使用 C 模块扩展 Lua。
请参阅 ``luamod_hello`` 示例了解如何包含内置模块。

构建需要数学库。启用 ``LIBM`` 配置或使用工具链提供的数学库。

以下配置建议用于功能完整的 Lua 解释器：
- ``LIBC_FLOATINGPOINT``
- ``SYSTEM_READLINE``


Lua 模块：

- cjson
- lfs
- luasyslog
- luv
