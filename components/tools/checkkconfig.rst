===================
``checkkconfig.py``
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``checkkconfig.py`` 是一个 Python 脚本，用于模拟修改 CONFIG 项的效果。
它可用于检查我的配置更改是否符合预期。

Help message::

  $ tools/checkkconfig.py -h
  usage: checkkconfig.py [-h] -f FILE (-s CONFIG VALUE | -d DIFF)

  optional arguments:
    -h, --help            show this help message and exit
    -f FILE, --file FILE  Path to the input defconfig file
    -s CONFIG_XXX VALUE, --single CONFIG VALUE
                          Analyze single change: CONFIG_NAME y/m/n
    -d DIFF, --diff DIFF  Analyze changes from diff file

  example: ./tools/checkkconfig.py -f defconfig -s ELF n

  outputs:
  Change report for ELF=n
  Config Option                            Old                  New
  ----------------------------------------------------------------------
  BINFMT_LOADABLE                          y                    n
  ELF                                      y                    n
  ELF_STACKSIZE                            8192                 <unset>
  LIBC_ARCH_ELF                            y                    n
  LIBC_MODLIB                              y                    n
  MODLIB_ALIGN_LOG2                        2                    <unset>
  MODLIB_BUFFERINCR                        32                   <unset>
  MODLIB_BUFFERSIZE                        32                   <unset>
  MODLIB_MAXDEPEND                         2                    <unset>
  MODLIB_RELOCATION_BUFFERCOUNT            256                  <unset>
  MODLIB_SYMBOL_CACHECOUNT                 256                  <unset>

如我们所见，可以清楚地知道
如果此时在 defconfig 中关闭 ELF，
会带来以下配置联动变化。

它还可以解析 diff 文件，用于检查多个配置的更改。
