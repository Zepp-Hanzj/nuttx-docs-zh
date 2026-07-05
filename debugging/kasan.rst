====================================
内核地址消毒器 (KASAN)
====================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

概述
--------

内核地址消毒器（KASAN）是一个动态内存安全错误检测器，旨在发现越界访问和释放后使用（use-after-free）的错误。

当前版本的 NuttX 有两种模式：

1. 通用 KASAN
2. 基于软件标签的 KASAN

通用 KASAN 通过 CONFIG_MM_KASAN_GENERIC 启用，是用于调试的模式，类似于 Linux 用户级 ASan。此模式在许多 CPU 架构上受支持，但有显著的性能和内存开销。当前 NuttX 通用 KASAN 可以支持检测由默认 NuttX 堆分配器分配的内存越界，这取决于 CONFIG_MM_DEFAULT_MANAGER 或 CONFIG_MM_TLSF_MANAGER，以及全局变量的越界检测。

基于软件标签的 KASAN 或 SW_TAGS KASAN，通过 CONFIG_MM_KASAN_SW_TAGS 启用，可用于调试。此模式仅支持 arm64，但其适度的内存开销允许在内存受限的设备上使用真实工作负载进行测试。

支持
-------

架构
~~~~~~~~~~~~~~~~~~~~~

通用 KASAN 在 x86_64、arm、arm64、riscv、xtensa 等上受支持。

基于软件标签的 KASAN 模式仅在 arm64 上受支持。

用法
-----

要启用通用 KASAN，请按如下配置内核::

    CONFIG_MM_KASAN=y
    CONFIG_MM_KASAN_INSTRUMENT_ALL=y
    CONFIG_MM_KASAN_GENERIC=y

如果你想启用全局变量越界检测，可以在上述基础上添加配置::

    CONFIG_MM_KASAN_GLOBAL=y

要启用基于软件标签的 KASAN，请按如下配置内核::

    CONFIG_MM_KASAN=y
    CONFIG_MM_KASAN_INSTRUMENT_ALL=y
    CONFIG_MM_KASAN_SW_TAGS=y

实现细节
----------------------

通用 KASAN：

使用参数 -fsanitize=kernel-address 编译，使用编译时插桩来插入内存访问检查。编译器在每次大小为 1、2、4、8 或 16 的内存访问之前插入函数调用（``__asan_load*(addr)``、``__asan_store*(addr)``）。这些函数通过检查相应的影子内存来检查内存访问是否有效。

它与 Linux 略有不同。一方面，在影子区域的来源方面；NuttX 的影子区域来自每个堆的末尾。在堆初始化期间，它被偏移并在末尾形成一个 kasan 区域。多个堆之间的区域使用链表连接。

其次，为了节省更多内存消耗，NuttX 的实现采用位图检测方法；例如，在 32 位机器的情况下，如果 NuttX 堆分配器为其分配了四字节内存，kasan 模块将在四字节的基础上为每个内存组分配一个单位位的影子区域。如果影子区域为 0，则该内存组可以访问，否则为 1 表示不可访问。

第三，此 NuttX 的全局变量越界检测实现也与 Linux 不同。由于影子区域的特殊性，NuttX 需要为全局变量所在的数据段和 bss 段分别构建 kasan 区域。编译前，添加编译选项 '--param asan-globals=1'。这样，编译器将所有全局变量信息存储在特殊段 '.data..LASAN0' 中，这两个段存储所有全局变量的信息，可以使用以下结构解析::

    struct kasan_global {
      const void *beg;                /* 全局变量起始地址 */
      size_t size;                    /* 全局变量大小 */
      size_t size_with_redzone;       /* 变量大小 + 红区大小。32 字节对齐 */
      const void *name;
      const void *module_name;        /* 声明全局变量的模块名称 */
      unsigned long has_dynamic_init; /* C++ 需要此字段 */

      /* 它将指向存储每个全局变量的文件行号、
       * 列号和文件名信息的位置 */

      struct kasan_source_location *location;
      char *odr_indicator;
    };

为了减少编译器生成的占用宝贵 flash 空间的数据量，NuttX 的方法是使用多次链接通过脚本从 elf 中提取全局变量信息，根据 kasan 区域规则构造全局变量的 region 和 shadow，形成数组，最后链接到程序中。程序将数组连接到 kasan 的 region 链表。

编译器生成的数据将放置在不存在的内存块中。编译完成后，该段将被删除，不会复制到最终烧录板卡的 bin 文件中。

基于软件标签的 KASAN：

基于软件标签的 KASAN 使用软件内存标签方法来检查访问有效性。它目前仅为 arm64 架构实现。

基于软件标签的 KASAN 使用 arm64 CPU 的 Top Byte Ignore（TBI）功能在内核指针的高位字节中存储指针标签。它使用影子内存来存储与每个堆分配内存单元关联的内存标签（因此，它将内核内存的 1/8 用于影子内存）。

每次内存分配时，基于软件标签的 KASAN 生成一个随机标签，用此标签标记分配的内存，并将相同的标签嵌入返回的指针中。

基于软件标签的 KASAN 使用编译时插桩在每次内存访问之前插入检查。这些检查确保正在访问的内存的标签等于用于访问此内存的指针的标签。在标签不匹配的情况下，基于软件标签的 KASAN 会打印错误报告。

开发者指南
--------------

忽略访问
~~~~~~~~~~~~~~~~~

如果你想让你正在编写的模块不被编译器插桩，可以在单个模块中添加选项 'CFLAGS += -fno-sanitize=kernel-address'。如果是文件，可以这样写，
special_file.o: CFLAGS = -fno-sanitize=kernel-address
