===================
``checkkconfig.py``
===================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

``checkkconfig.py`` is a Python script that simulates the effects of modifying a CONFIG item.
It 可用于 to check whether my config changes are what I expected.

Help message::

  $ tools/checkkconfig.py -h
  usage: checkkconfig.py [-h] -f FILE (-s CONFIG VALUE | -d DIFF)

  选项al 参数s:
    -h, --help            show this help message and exit
    -f FILE, --文件 FILE  路径 to the 输入 defconfig 文件
    -s CONFIG_XXX VALUE, --single CONFIG VALUE
                          Analyze single change: CONFIG_NAME y/m/n
    -d DIFF, --diff DIFF  Analyze changes from diff 文件

  example: ./tools/checkkconfig.py -f defconfig -s ELF n

  输出s:
  Change report for ELF=n
  Config Option                            Old                  New
  ----------------------------------------------------------------------
  BINFMT_LOADABLE                          y                    n
  ELF                                      y                    n
  ELF_STACKSIZE                            8192                 <un设置>
  LIBC_ARCH_ELF                            y                    n
  LIBC_MODLIB                              y                    n
  MODLIB_ALIGN_LOG2                        2                    <un设置>
  MODLIB_BUFFERINCR                        32                   <un设置>
  MODLIB_BUFFERSIZE                        32                   <un设置>
  MODLIB_MAXDEPEND                         2                    <un设置>
  MODLIB_RELOCATION_BUFFERCOUNT            256                  <un设置>
  MODLIB_SYMBOL_CACHECOUNT                 256                  <un设置>

As we can see, we can clearly know that
if I turn off ELF in defconfig at this time,
it will bring about 以下 配置 链接age changes

It can also parse diff 文件s, which 可用于 to check the changes of multiple
configs.
