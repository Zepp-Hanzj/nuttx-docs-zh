===========================================
``incdir.sh``, ``incdir.bat``, ``incdir.c``
===========================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

不同的编译器在编译器命令行上指定包含文件路径列表时有不同的约定。
incdir.sh bash 脚本允许构建系统创建包含文件路径，而不必关心
所使用的特定编译器。

incdir.bat 脚本是在原生 Windows 构建中使用的对应版本。
但目前在该环境中仅支持一种编译器：MinGW-GCC。

incdir.c 是 incdir.sh 的高性能版本，已转换为 C 语言实现。
