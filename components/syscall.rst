=============
Syscall Layer
=============

本页面讨论从单体内核模式 NuttX 内核与单独构建的用户模式应用程序集之间通信的 syscall 层支持。

对于大多数 MCU，NuttX 构建为一个平坦的单可执行映像，包含 NuttX RTOS 以及所有应用程序代码。RTOS 代码和应用程序在同一地址空间中运行，并具有相同的内核模式权限。为了利用某些处理器的安全功能，还支持替代构建模型：NuttX 可以单独构建为单体内核模式模块，应用程序可以作为单独构建的用户模式模块添加。

此目录中提供的 syscall 层作为用户模式应用程序到内核模式 RTOS 的通信层。从用户模式到内核模式的切换使用软件中断 (SWI) 完成。SWI 由不同制造商以不同方式实现和命名，但所有本质上工作方式相同：在用户模式下执行特殊指令，导致软件生成的中断。软件生成的中断在内核中被捕捉并在内核模式下处理。

Header Files
------------

``include/syscall.h``
~~~~~~~~~~~~~~~~~~~~~

此头文件支持对 SWI 设施的通用访问。它只是一个包装文件，包含 ``include/sys/syscall.h`` 和 ``include/arch/syscall.h``。

``include/sys/syscall.h``
~~~~~~~~~~~~~~~~~~~~~~~~~

内核接收的 SWI 通过一个代码来区分，该代码标识如何处理 SWI。此头文件定义了 NuttX 内核理解的所有此类代码。

``include/arch/syscall.h`` (or ``arch/<cpu>/include/syscall.h``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

此头文件由平台特定逻辑提供，并声明（或定义）在此平台上提供软件中断的机制。以下函数必须在此头文件中声明（或定义）：

- 仅带 ``SYS_`` 调用号的 ``SWI``：

  .. code-block:: C

    uintptr_t sys_call0(unsigned int nbr);

- 带 ``SYS_`` 调用号和一个参数的 ``SWI``：

  .. code-block:: C

    uintptr_t sys_call1(unsigned int nbr, uintptr_t parm1);

- 带 ``SYS_`` 调用号和两个参数的 ``SWI``：

  .. code-block:: C

    uintptr_t sys_call2(unsigned int nbr, uintptr_t parm1, uintptr_t parm2);

- 带 ``SYS_`` 调用号和三个参数的 ``SWI``：

  .. code-block:: C

    uintptr_t sys_call3(unsigned int nbr, uintptr_t parm1,
                        uintptr_t parm2, uintptr_t parm3);

- 带 ``SYS_`` 调用号和四个参数的 ``SWI``：

  .. code-block:: C

    uintptr_t sys_call4(unsigned int nbr, uintptr_t parm1, uintptr_t parm2,
                        uintptr_t parm3, uintptr_t parm4);

- 带 ``SYS_`` 调用号和五个参数的 ``SWI``：

  .. code-block:: C

    uintptr_t sys_call5(unsigned int nbr, uintptr_t parm1, uintptr_t parm2,
                        uintptr_t parm3, uintptr_t parm4, uintptr_t parm5);

- 带 ``SYS_`` 调用号和六个参数的 ``SWI``：

  .. code-block:: C

    uintptr_t sys_call6(unsigned int nbr, uintptr_t parm1, uintptr_t parm2,
                        uintptr_t parm3, uintptr_t parm4, uintptr_t parm5,
                        uintptr_t parm6);

Syscall Database
~~~~~~~~~~~~~~~~

Sycall 信息维护在一个数据库中。该"数据库"以简单的逗号分隔值文件 ``syscall.csv`` 实现。大多数电子表格程序接受此格式，可用于维护 syscall 数据库。

CSV 文件每行的格式如下：

* 字段 1：函数名称

* 字段 2：包含函数原型的头文件

* 字段 3：编译条件

* 字段 4：函数返回值类型。

* 字段 5 - N+5：函数的 N 个形式参数的每个参数的类型

* 字段 N+5 - ：如果最后一个参数是"..."，则以下字段提供可能的可选参数的类型和数量。参见下面关于可变参数函数的说明

每个类型字段的格式如下：

* type name：

  对于所有较简单的类型

* formal type | actual type：

  对于数组类型，其中形式参数的形式（例如 ``int param[2]``）与实际传递参数的类型（例如 ``int*``）不同。这是必要的，因为你不能对数组类型进行简单的类型转换。

* formal type | union member actual type | union member fieldname：

  联合体存在类似情况。例如，形式参数类型 union sigval -- 你不能将 uintptr_t 转换为 union sigval，但在传递实际参数时可以转换为其中一个联合体成员类型。类似地，我们也不能将 union sigval 转换为 uinptr_t。相反，我们需要将特定的联合体成员字段名转换为 ``uintptr_t``。

Variadic Functions
------------------

具有任意数量和任意类型参数的通用可变参数函数无法表示为系统调用。``syslog()`` 就是一个很好的例子。通常你会通过使用接受 ``va_list`` 作为参数的非可变参数形式的 OS 接口来解决此问题，在本例中为 ``vsyslog()``。

有许多函数具有可变参数形式但只接受一个或两个可选参数。这些可以作为系统调用处理，但只能将它们视为具有固定数量的参数。

这些在 ``syscall.csv`` 中通过附加可选参数的数量和类型来处理。例如，考虑 ``open()`` OS 接口。其原型是：

.. code-block:: C

      int open(const char *path, int oflag, ...);

实际上，open 可能只接受一个类型为 ``mode_t`` 的可选参数，在 ``syscall.csv`` 中表示如下::

      "open","fcntl.h","","int","const char*","int","...","mode_t"

``mode_t`` 的存在告诉 ``tools/mksyscall`` 最多有一个可选参数，如果存在，其类型为 ``mode_t``。

注意：此 CSV 文件不仅用于支持 trap 信息的生成，还用于符号表的生成。有关更多信息，请参阅 ``Documentation/components/tools/`` 和 ``Documentation/components/libs/``。

Auto-Generated Files
--------------------

stubs 和 proxies 从该 CSV 数据库自动生成。使用以下定义：

* Proxy - 在用户空间中执行的一小段代码。Proxy 与其代理的"真实"函数具有完全相同的函数原型。但是，它仅用于将函数调用映射为 syscall，并根据需要编组所有系统调用参数。

* Stub - 在 NuttX 内核中执行的另一小段代码，用于将内核接收的软件中断映射到内核函数调用。Stubs 接收编组的系统调用数据，并代表 proxy 函数执行实际的内核函数调用（在内核模式下）。

Sub-Directories
---------------

* ``stubs`` - 自动生成的 stub 文件放置在此目录中。
* ``proxies`` - 自动生成的 proxy 文件放置在此目录中。

mksyscall
---------

mksyscall 是一个 C 程序，在初始 NuttX 构建期间由顶层 ``syscall/`` 目录中的逻辑使用。关于 stubs 和 proxies 的信息维护在 ``syscall/`` 目录中的逗号分隔值 (CSV) 文件中。mksyscall 程序将接受此 CSV 文件作为输入，并生成所有必需的 proxy 或 stub 文件作为输出。有关更多信息，请参阅 ``Documentation/components/tools/``。
