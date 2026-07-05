========
stdbit.h
========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

The 选项al C23 ``std位.h`` header provides 位 manipulation macros
(endianness, leading/trailing zeros and ones, count, single-位 test,
位 宽度, 位 floor, 位 ceil). NuttX provides this header only when
explicitly 启用d via Kconfig.

配置
=============

- **CONFIG_ARCH_HAVE_STDBIT_H** (bool, selected by arch)
  Architecture indicates it provides ``arch/<arch>/include/std位.h``.

- **CONFIG_ARCH_STDBIT_H** (bool "std位.h", depends on ARCH_HAVE_STDBIT_H)
  Use the redirecting header. The 构建 copies
  ``include/nuttx/lib/stdbit.h`` to ``include/stdbit.h``; that header
  then includes ``<arch/std位.h>`` when this 选项 is 设置.

- **CONFIG_LIBC_STDBIT_GENERIC** (bool "std位.h (generic C23)")
  Use the generic C23 implementation. The same redirecting 文件
  ``include/nuttx/lib/stdbit.h`` is copied to ``include/stdbit.h``,
  and the generic implementation 用于 (no arch header). Requires
  compiler builtins (e.g. ``__builtin_clz``, ``__builtin_ctz``,
  ``__builtin_popcount``); see ``CONFIG_HAVE_BUILTIN_*`` in
  ``nuttx/编译r.h``.

Either **CONFIG_ARCH_STDBIT_H** or **CONFIG_LIBC_STDBIT_GENERIC** may be
启用d so that ``#include <std位.h>`` 可用.
