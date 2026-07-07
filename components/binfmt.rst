.. _binfmt:

=============
Binary Loader
=============

*二进制加载器* 的目的是加载并执行位于文件系统中的各种 *二进制格式* 的模块。加载是指以某种方式实例化二进制模块，通常是将全部或部分二进制模块复制到内存中，然后将该模块与其他组件进行链接。在大多数架构中，二进制模块必须链接的主要组件是基础 FLASH 代码，因为那是 RTOS 和主要任务所在的位置。程序模块在加载完成后即可执行。

**二进制格式**。二进制加载器为不同的二进制格式提供通用支持。它支持 *注册接口*，允许在运行时加载已支持的二进制格式。每种二进制格式都提供了一个供二进制加载器使用的通用接口。当收到加载二进制文件的请求时，二进制加载器会查询每种已注册的二进制格式，为其提供要加载的二进制对象路径。当第一种二进制格式识别出该二进制对象并成功加载时，或当所有已注册的二进制格式都尝试加载该二进制对象但均失败时，二进制加载器将停止查询。

目前，NuttX 支持以下二进制格式：

  - **ELF**。标准 ELF 格式文件。
  - **NXFLAT**。NuttX NXFLAT 格式文件。有关 NXFLAT 二进制格式的更多信息，请参阅 :ref:`NXFLAT 文档 <nxflat>`。

**可执行文件和库**。通用二进制加载器逻辑不关心加载的是什么。它可以加载可执行程序或库。没有严格的规则，但库倾向于导出符号，而程序倾向于导入符号：程序将使用库导出的符号。但是，目前所有已支持的二进制格式都不支持符号导出。

**binfmt**。在 NuttX 源代码中，短名称 ``binfmt`` 用于指代 NuttX 二进制加载器。这是包含二进制加载器的目录名称，也是二进制加载器使用的头文件和变量的名称。

名称 ``binfmt`` 与 Linux 二进制加载器使用的名称相同。然而，NuttX 二进制加载器是独立开发的，与 Linux 二进制加载器除了相同的名称和基本功能外没有任何共享。

Binary Loader Interface
=======================

Header Files
------------

二进制加载器的接口在头文件 ``include/nuttx/binfmt/binfmt.h`` 中描述。下面列出了该头文件中定义的数据结构和接口的简要说明。

Data Structures
---------------

当二进制格式向二进制加载器注册时，它提供一个指向 :c:struct:`binfmt_s` 的可写实例的指针。

.. c:struct:: binfmt_s

  .. code-block:: c

    struct binfmt_s
    {
      FAR struct binfmt_s *next;             /* Supports a singly-linked list */
      int (*load)(FAR struct binary_s *bin); /* Verify and load binary into memory */
    };

  ``load`` 方法用于将二进制格式加载到内存中。返回 ``OK`` (0) 表示二进制对象加载成功，返回负的 ``errno`` 表示加载失败的原因。

.. c:struct:: binary_s

  类型 ``struct binary_s`` 用于 (1) 描述要加载的二进制对象，以及在加载成功后 (2) 提供有关二进制对象加载位置和方式的信息。该结构如下所示：

  .. code-block:: c

    struct symtab_s;
    struct binary_s
    {
      /* Information provided to the loader to load and bind a module */

      FAR const char *filename;            /* Full path to the binary to be loaded */
      FAR const char **argv;               /* Argument list */
      FAR const struct symtab_s *exports;  /* Table of exported symbols */
      int nexports;                        /* The number of symbols in exports[] */

      /* Information provided from the loader (if successful) describing the
       * resources used by the loaded module.
       */

      main_t entrypt;                      /* Entry point into a program module */
      FAR void *mapped;                    /* Memory-mapped, address space */
      FAR void *alloc[BINFMT_NALLOC];      /* Allocated address spaces */

      /* Constructors/destructors */

    #ifdef CONFIG_BINFMT_CONSTRUCTORS
      FAR binfmt_ctor_t *ctors;            /* Pointer to a list of constructors */
      FAR binfmt_dtor_t *dtors;            /* Pointer to a list of destructors */
      uint16_t nctors;                     /* Number of constructors in the list */
      uint16_t ndtors;                     /* Number of destructors in the list */
    #endif

      /* Address environment.
       *
       * addrenv - This is the handle created by up_addrenv_create() that can be
       *   used to manage the tasks address space.
       */

    #ifdef CONFIG_ARCH_ADDRENV
      arch_addrenv_t addrenv;              /* Task group address environment */
    #endif

      size_t mapsize;                      /* Size of the mapped address region (needed for munmap) */

      /* Start-up information that is provided by the loader, but may be modified
       * by the caller between load_module() and exec_module() calls.
       */

      uint8_t priority;                    /* Task execution priority */
      size_t stacksize;                    /* Size of the stack in bytes (unallocated) */
    #ifndef CONFIG_BUILD_KERNEL
      FAR void *stackaddr;                 /* Task stack address */
    #endif
    };

  其中类型 ``binfmt_ctor_t`` 和 ``binfmt_dtor_t`` 定义了一个 C++ 构造函数或析构函数的类型：

  .. code-block:: c

    typedef FAR void (*binfmt_ctor_t)(void);
    typedef FAR void (*binfmt_dtor_t)(void);

Function Interfaces
-------------------

Binary format management
~~~~~~~~~~~~~~~~~~~~~~~~

.. c:function:: int register_binfmt(FAR struct binfmt_s *binfmt)

  注册一种二进制格式的加载器。

  :return: 这是 NuttX 内部函数，遵循惯例：成功时返回 0 (OK)，失败时返回负的 errno。

.. c:function:: int unregister_binfmt(FAR struct binfmt_s *binfmt)

  注销一种二进制格式的加载器。

  :return:
    这是 NuttX 内部函数，遵循惯例：成功时返回 0 (OK)，失败时返回负的 errno。

Basic module management
~~~~~~~~~~~~~~~~~~~~~~~

.. c:function:: int load_module(FAR struct binary_s *bin)

  将模块加载到内存中，将其绑定到导出符号表，并为执行做好准备。

  :param bin:
    ``filename`` 字段将用于从文件系统中定位要加载的模块。文件名必须是文件的完整绝对路径，除非定义了 ``CONFIG_LIBC_ENVPATH``。在这种情况下，文件名可以是相对路径；将使用 ``PATH`` 环境变量生成一组候选绝对路径，``load_module()`` 将尝试加载在这些绝对路径下找到的每个文件。

  :return:
    这是 NuttX 内部函数，遵循惯例：成功时返回 0 (``OK``)，失败时返回负的 ``errno``。

.. c:function:: int unload_module(FAR struct binary_s *bin)

  从内存中卸载一个（非正在执行的）模块。如果模块已经通过 :c:func:`exec_module` 启动且尚未退出，调用此函数将是致命的。

  但是，此函数必须在模块退出后调用。具体如何实现取决于你的逻辑。也许你可以将其注册为通过 :c:func:`on_exit` 调用？

  :return:
    这是 NuttX 内部函数，遵循惯例：成功时返回 0 (``OK``)，失败时返回负的 ``errno``。

.. c:function:: int exec_module(FAR const struct binary_s *bin);

  执行一个已通过 :c:func:`load_module` 加载到内存中的模块。

  :return:
    这是 NuttX 内部函数，遵循惯例：成功时返回 0 (``OK``)，失败时返回负的 ``errno``。

.. tip::
  函数 :c:func:`exec` 是一个便捷函数，将 :c:func:`load_module` 和 :c:func:`exec_module` 封装为一次调用。

``PATH`` traversal logic
~~~~~~~~~~~~~~~~~~~~~~~~

.. c:function:: ENVPATH_HANDLE envpath_init(void);

  初始化以遍历 ``PATH`` 变量中的每个值。使用顺序如下：

  #. 调用 :c:func:`envpath_init` 以初始化遍历。``envpath_init()`` 将返回一个不透明句柄，该句柄可随后提供给 :c:func:`envpath_next` 和 :c:func:`envpath_release`。
  #. 反复调用 :c:func:`envpath_next` 以检查 ``PATH`` 变量目录中的每个文件。
  #. 调用 :c:func:`envpath_release` 以释放 :c:func:`envpath_init` 分配的资源。

  :return:
    成功时，:c:func:`envpath_init` 返回一个非 ``NULL`` 的不透明句柄，可随后用于调用 :c:func:`envpath_next` 和 :c:func:`envpath_release`。出错时，返回 ``NULL`` 句柄值。最可能的错误原因是 ``PATH`` 变量没有关联的值。

.. c:function:: FAR char *envpath_next(ENVPATH_HANDLE handle, FAR const char *relpath)

  遍历 PATH 变量中所有可能的值，以便在仅提供相对路径时尝试找到可执行文件的完整路径。

  :param handle: :c:func:`envpath_init` 返回的句柄值。
  :param relpath: 要查找的文件的相对路径。

  :return:
    成功时，返回一个指向以 null 结尾的字符串的非 ``NULL`` 指针。这是文件系统中存在的文件的完整路径。此函数将验证文件是否存在（但不会验证该文件是否标记为可执行）。

  .. note::
    成功情况下返回的字符串指针指向已分配的内存。调用者必须通过调用 :c:func:`kmm_free` 来释放该内存。

  当无法从 ``PATH`` 变量中的任何绝对路径解析 ``relpath`` 时，返回 ``NULL``。在这种情况下，没有必要进一步调用 :c:func:`envpath_next`；必须调用 :c:func:`envpath_release` 来释放 :c:func:`envpath_init` 分配的资源。

.. c:function:: void envpath_release(ENVPATH_HANDLE handle)

  释放创建句柄值时 :c:func:`envpath_init` 分配的所有资源。该函数返回后句柄值将失效。尝试使用过期句柄调用 :c:func:`envpath_next` 或 :c:func:`envpath_release` 将导致未定义（即不良的）行为。

  :param handle: :c:func:`envpath_init` 返回的句柄值。

Symbol Tables
=============

**符号表**。符号表是名称-值映射的列表：名称是标识符号的字符串，值是该符号在内存中的地址。在大多数 NuttX 架构中，符号表至少是动态链接加载的二进制对象与 FLASH 上的基础代码所必需的。由于二进制对象是单独构建和链接的，这些符号在二进制对象中将显示为 *未定义* 符号。二进制加载器将使用符号表按名称查找符号，并在需要时提供与该符号关联的地址，以执行二进制对象到基础 FLASH 代码的动态链接。

某些工具链会在符号前加下划线前缀。为了支持这些工具链，可以定义 ``CONFIG_SYMTAB_DECORATED`` 设置。这将在动态链接期间忽略 *未定义* 符号的前导下划线。

Symbol Table Header Files
-------------------------

符号表逻辑的接口在头文件 ``include/nuttx/binfmt/symtab.h`` 中描述。下面列出了该头文件中定义的数据结构和接口的简要说明。

Symbol Table Data Structures
----------------------------

.. c:struct:: symbtab_s

  描述符号表中的一个条目。

  .. code-block:: c

    struct symtab_s
    {
      FAR const char *sym_name;          /* A pointer to the symbol name string */
      FAR const void *sym_value;         /* The value associated with the string */
    };

  符号表是 ``struct symtab_s`` 的固定大小数组。信息有意保持最少，仅支持：

  #. 函数指针作为 ``sym_values``。如果需要支持其他类型的值，则还需要在结构中包含类型信息。
  #. 固定大小数组。没有明确的机制用于动态添加或删除符号表条目（如果需要可以使用 realloc）。其意图是仅支持在编译或链接时完全定义的固定大小数组。

Symbol Table Function Interfaces
--------------------------------

.. c:function:: FAR const struct symtab_s *symtab_findbyname(FAR const struct symtab_s *symtab, FAR const char *name, int nsyms);

  在符号表中查找名称匹配的符号。如果未选择 ``CONFIG_SYMTAB_ORDEREDBYNAME``，实现将对 ``nsyms`` 是线性的；如果选择了，则是对数的。

  :return:
    如果找到名称匹配的条目，返回符号表条目的引用；如果未找到，返回 NULL。

.. c:function:: FAR const struct symtab_s *symtab_findbyvalue(FAR const struct symtab_s *symtab, FAR void *value, int nsyms);

  在符号表中查找值最接近（但不大于）所提供值的符号。此版本假设表未按符号值排序，因此访问时间对 ``nsyms`` 是线性的。

  :return:
    如果找到值匹配的条目，返回符号表条目的引用；如果未找到，返回 ``NULL``。

Configuration Variables
=======================

  - ``CONFIG_BINFMT_DISABLE``：默认情况下，会构建对可加载二进制格式的支持。定义此设置可以禁用该逻辑。
  - ``CONFIG_BINFMT_CONSTRUCTORS``：为加载的模块构建 C++ 构造函数支持。
  - ``CONFIG_SYMTAB_ORDEREDBYNAME``：符号表按名称排序（而不是按值排序）。
  - ``CONFIG_SYMTAB_DECORATED``：符号在目标文件中将带有前导下划线。

每种启用的二进制格式可能还需要其他配置选项。
