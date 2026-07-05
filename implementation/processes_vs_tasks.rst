==============================
Linux 进程与 NuttX 任务
==============================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

您可能习惯于运行存储在 Linux 或 Windows 文件中的程序。
如果您转向在资源有限的 MCU 上使用 NuttX 任务，您会遇到一些行为差异。本 Wiki 页面将总结其中的一些差异。

NuttX 构建类型
=================

NuttX 可以通过几种不同的方式构建：

* **内核构建** 内核构建通过 ``CONFIG_BUILD_KERNEL`` 选择，使用 MCU 的内存管理单元（MMU）来实现与 Linux 进程非常相似的进程。这里没有有趣的讨论；NuttX 的行为与 Linux 非常相似。

* **平板构建** 大多数资源有限的 MCU 没有 MMU，代码被构建为在未受保护的平板地址空间中从片上 FLASH 内存运行的二进制块。此构建模式通过 ``CONFIG_BUILD_FLAT`` 选择，是迄今为止人们构建 NuttX 最常见的方式。这是本 Wiki 页面针对的有趣情况。

* **保护构建** 另一个构建选项是保护构建。这本质上与平板构建相同，但使用 MCU 的内存保护单元（MPU）将未保护的用户地址范围与受保护的系统地址范围分开。本 Wiki 页面的评论也适用于此情况。

全局变量的初始化
==================================

Linux 行为
--------------

如果您习惯于为 Linux 编写程序，那么您会注意到的一件事是全局变量在系统上电时只初始化一次。例如。考虑这个小程序：

.. code-block:: C
                
   bool test = true;
 
   int main(int argc, char **argv)
   {
     printf("test: %i\n", test);
     test = false;
     printf("test: %i\n", test);
     return 0;
   }

如果您在 Linux 下构建并运行此程序，您将始终看到此输出::

  test: 1
  test: 0

在这种情况下，每次将文件加载到内存并运行时，全局变量都会被重新初始化。

NuttX 平板构建行为
-------------------------

但如果您将此程序构建到片上 FLASH 中并作为任务启动（例如通过 ``task_start()``），您将在第一次运行程序时看到::

  test: 1
  test: 0

但在那之后，您将始终看到::

  test: 0
  test: 0

test 变量在上电时只初始化为 true（1）一次，但每次程序运行时都会重置为 false（0）。

如果您希望在程序构建到公共 FLASH 块中时具有相同的行为，那么您需要修改代码，使全局变量在每次程序运行时显式重置，例如：

.. code-block:: C

   bool test;
   
   int main(int argc, char **argv)
   {
     test = true;
     printf("test: %i\n", test);
     test = false;
     printf("test: %i\n", test);
     return 0;
   }

NuttX 可加载程序
------------------------

如果您像 Linux 那样从文件将程序加载到 RAM 中并执行它们，那么 NuttX 将再次表现得像 Linux。因为平板构建的 NuttX 以相同的方式工作：当您执行文件中的 NuttX ELF 或 NxFLAT 模块时，文件被复制到 RAM 中，并在程序运行之前初始化全局变量。

但构建到 FLASH 中的代码工作方式不同。只有一组全局变量：整个 FLASH 映像的二进制块中的所有全局变量。它们都在上电复位时初始化一次。

这是使将 Linux 应用程序移植到 FLASH 块中变得更加复杂的原因之一。每次启动任务时，都必须在 ``main()`` 中手动初始化每个全局变量。

全局变量和多个任务副本
=========================================

在平板构建上下文中，最好尽可能避免使用全局变量，因为这种用法增加了另一个限制：在任何给定时间只能运行程序的一个副本。这是因为全局变量由每个实例共享（再次与从文件运行程序不同，后者每个全局变量都有私有副本）。

支持 FLASH 中程序的多个副本的一种方法是将所有全局变量移入一个结构体中。如果全局变量所需的内存量很小，那么每个 ``main()`` 可以简单地在栈上分配该结构体的副本。在上面的简单示例中，这可能是：

.. code-block:: C

   struct my_globals_s
   {
     bool test;
   };
 
   int main(int argc, char **argv)
   {
     struct my_globals_s my_globals = { true };
 
     printf("test: %i\n", my_globals.test);
     my_globals.test = false;
     printf("test: %i\n", my_globals.test);
     return EXIT_SUCCESS;
   }

然后，包含已分配全局变量的结构体的指针需要作为参数传递给需要访问全局变量的每个内部函数。因此，您将把内部函数改为：

.. code-block:: C

   static void print_value(void)
   {
     printf("test: %i\n", test);
   }

改为：

.. code-block:: C

   static void print_value(FAR struct my_globals_s *globals)
   {
     printf("test: %i\n", globals->test);
   }

然后在每次调用函数时传递对已分配全局数据结构的引用，例如：

.. code-block:: C

   print_value(&my_globals);

如果全局变量结构体的大小很大，那么在栈上分配实例可能不是好主意。在这种情况下，使用 ``malloc()`` 分配全局变量结构体可能更好。但不要忘记在退出前 ``free()`` 已分配的变量结构体！（参见后面的内存清理讨论）。

.. code-block:: C

   struct my_globals_s
   {
     bool test;
   };
 
   int main(int argc, char **argv)
   {
     FAR struct my_globals_s *my_globals;
 
     my_globals = (FAR struct my_globals_s *)malloc(sizeof(struct my_globals_s));
     if (my_globals = NULL)
       {
         fprintf(stderr, "ERROR: Failed to allocate state structure\n");
         return EXIT_FAILURE;
       }
 
     my_globals=>test = true;
     printf("test: %i\n", my_globals->test);
     my_globals=>test = false;
     printf("test: %i\n", my_globals->test);
 
     free(my_globals);
     return EXIT_SUCCESS;
   }

内存清理
===============

Linux 进程退出
------------------

另一个不相关的使将 Linux 程序移植到 FLASH 块中变得更加复杂的因素是内存清理。当 Linux 进程退出时，其整个地址环境都被销毁，包括所有分配的内存。如果作为 Linux 进程实现，这个小程序不会泄漏内存：

.. code-block:: C

   int main(int argc, char **argv)
   {
     char *buffer = malloc(1024);
     ... 使用 buffer 做一些事情 ...
     return 0;
   }

同样的程序，如果移植到 FLASH 块中，将会有内存泄漏，因为任务退出时没有自动清理分配的内存。相反，您必须通过释放来显式清理所有分配的内存：

.. code-block:: C

   int main(int argc, char **argv)
   {
     char *buffer = malloc(1024);
     ... 使用 buffer 做一些事情 ...
     free(buffer);
     return 0;
   }

Linux 进程退出时的内存清理是进程终止时进程地址环境拆除的结果。每个进程包含自己的堆；当进程地址环境被拆除时，该进程堆被返回给操作系统页面分配器。因此内存清理基本上是免费的。

NuttX 任务退出
---------------

但在单体的片上 FLASH 块中运行任务时，您与所有其他任务共享同一个堆。没有可以找到并释放您在公共堆中任务分配的内存的神奇清理（参见"任务退出时释放内存的方法"）。

NuttX 进程退出
------------------

请注意，当您在 NuttX 上运行进程（使用 ``CONFIG_BUILD_KERNEL``）时，NuttX 也以与 Linux 相同的方式运行：地址环境在任务退出时被销毁，所有内存都被回收。但所有其他情况都会泄漏内存。

任务退出时释放内存的方法
--------------------------------

有一些方法可以将分配的内存与任务关联起来，以便在任务退出时进行清理。然而，这种方法已被拒绝，因为 (1) 它无法可靠地完成，(2) 它会增加在内存受限的上下文中不可接受的内存分配开销。

相关问题可以在 `Github <https://github.com/apache/nuttx/issues/3345>`_ 上找到。
