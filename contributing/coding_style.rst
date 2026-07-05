.. include:: /substitutions.rst
.. _coding-standard:

=================
C 编码标准
=================

NuttX 遵循特定的编码风格，贡献被接受时必须始终遵循。
请在编写新代码之前阅读本文档，以便从一开始就遵循该风格。
要检查您的代码是否符合编码风格，您应该使用 :ref:`checkpatch.sh`
脚本（它调用 `nxstyle <#nxstyle>`_ 工具），该脚本位于
主 NuttX 仓库的 ``tools/`` 目录下，或启用 `pre-commit <#precommit>`__
中描述的 pre-commit 功能。

**************************
快速合规检查
**************************

在提交/更新 Pull Request 之前，请验证您的 git 提交的格式。
使用 :ref:`checkpatch.sh` 脚本来验证编码风格、编码和拼写问题：

  .. code-block:: bash

    ./tools/checkpatch.sh -c -u -m -g HEAD~...HEAD

或者，您可以使用 ``-f`` 开关传递要检查的 .c 文件或 .h 头文件来运行此脚本：

  .. code-block:: bash

    ./tools/checkpatch.sh -c -u -m -f path/to/your/file.c

*******************
通用规范
*******************

文件组织
=================

**文件扩展名** 使用 ``.h`` 扩展名作为 C 头文件，
使用 ``.c`` 作为 C 源文件。

**文件头**。每个 C、C++、make 文件或脚本都以文件头开始。
该文件头用*块注释*（见下文）括起来。在块注释中，必须包含：

  -  从顶级目录到文件的相对路径。
  -  可选的单行文件内容描述。
  -  一个空行
  -  NuttX 标准 Apache 2.0 许可信息，如
     `附录 <#appndxa>`__ 中所提供。

**示例文件头**。示例文件头在本文档的
`附录 <#appndxa>`__ 中提供。NuttX 源代码树中不得包含
没有许可信息的新软件。NuttX 源代码树中不得包含
没有 Apache 2.0 许可证或（在第三方文件的情况下）
兼容许可证（如 BSD 或 MIT 许可证）的新软件。
如果文件不遵循 Apache 2.0 许可，则应在头文件中提供
适当的许可信息，而不是 Apache 2.0 许可信息，
并且应在顶级 ``LICENSE`` 和/或 ``NOTICE`` 文件中
包含注释，以指示与 Apache 2.0 许可的任何差异。

**分组**。C 源文件或头文件中的所有类似组件都分组在一起。
定义不会随意出现在文件中，而是将类似的定义分组在一起，
并在前面加上标识分组的*块注释*。

**块注释**。文件中的每个分组用*块注释*分隔。
块注释包括：

-  一行由开始 C 注释（``/*``）后跟一系列星号组成，
   延伸到行的长度（通常到第 78 列）。
-  分组名称，从第 4 列开始。星号在第 1 列位于分组名称之前。
-  一行由结束 C 注释（``*/``）在行尾（通常第 78 列）组成，
   前面是一系列星号延伸到第 1 列。

**块注释示例**。参见 `附录 A <#appndxa>`__ 了解块注释的示例。

**分组顺序**。以下分组应按以下顺序出现在所有 C 源文件中：

  #. 包含的文件
  #. 预处理器定义
  #. 私有类型（定义）
  #. 私有函数原型（声明）
  #. 私有数据（定义）
  #. 公共数据（定义）
  #. 私有函数（定义）
  #. 公共函数（定义）

以下分组应按以下顺序出现在所有 C 头文件中：

  #. 包含的文件
  #. 预处理器定义
  #. 公共类型（定义）
  #. 公共数据（声明）
  #. 内联函数（定义）
  #. 公共函数原型（声明）

**大文件与小文件**。在较大的文件中，所有分组都应包含
块注释，即使它们是空的；空分组本身提供了重要信息。
较小的文件可以省略一些块注释；如果块注释比文件内容
还大就显得笨拙了！

**头文件幂等性**。C 头文件必须通过使用宏来"保护"
多次包含，以防止在头文件被多次包含时出现多次定义。

-  每个头文件必须在头文件开头附近包含以下预处理器
   条件逻辑：在文件头和"包含的文件"块注释之间。
   例如::

    #ifndef __INCLUDE_NUTTX_ARCH_H
    #define __INCLUDE_NUTTX_ARCH_H

   请注意，头文件中的定义不遵循通常的规则：
   文件顶部的条件测试不会导致文件中剩余的定义被缩进。

-  然后条件编译在头文件的最后一行关闭::

    #endif /* __INCLUDE_NUTTX_ARCH_H */

**形成保护名称**。保护中使用的预处理器宏名称由头文件的
完整相对路径组成，从顶级控制目录开始。该路径前面有
``__``，``_`` 替换宏名称中无效的每个字符。
因此，例如，``__INCLUDE_NUTTX_ARCH_H`` 对应于头文件
``include/nuttx/arch.h``

**Doxygen 信息**。NuttX 不使用 Doxygen 进行文档编写，
任何文件都不应包含 Doxygen 标签或 Doxygen 风格的注释。

**示例文件格式**。C 源文件和头文件模板在本文档的
`附录 <#appndxa>`__ 中提供。

行
=====

**行尾**。文件应使用换行符（``\n``）作为行尾格式化
（Unix 风格行尾），特别*不要*使用 Windows 风格行尾的
回车换行序列（``\r\n``）。行尾不应有多余的空白。
此外，所有文本文件应以单个换行符（``\n``）结尾。
这可以避免某些工具生成的*"文件末尾没有换行"*警告。

**行宽**。典型的 C 源文件或头文件中的文本不应超过第 78 列。
有时文件内容的性质可能要求行超过此限制。
这在头文件中经常发生，因为定义自然较长。
如果行宽必须超过 78 行，则可以在文件中使用更宽的行宽，
只要它被一致使用。

**换行**。

.. error:: 这是不正确的

  .. code-block:: c

    struct some_long_struct_name_s
    {
      struct some_long_struct_name_s *flink;  /* The forward link to the next instance of struct some_long_struct_name_s in a singly linked list */
      int short_name1;   /* Short comment 1 */
      int short_name2;   /* This is a very long comment describing subtle aspects of the short_name2 field */
    };

    struct some_medium_name_s *ptr = malloc(sizeof(some_medium_name_s);

    struct some_long_struct_name_s *ptr = malloc(sizeof(some_long_struct_name_s);

    ret = some_function_with_many parameters(long_parameter_name_1, long_parameter_name_2, long_parameter_name_3, long_parameter_name_4, long_parameter_name_5, long_parameter_name_6, long_parameter_name_7, long_parameter_name_8);

    ret = some_function_with_many parameters(long_parameter_name_1,
      long_parameter_name_2,
      long_parameter_name_3
      long_parameter_name_4,
      long_parameter_name_5,
      long_parameter_name_6,
      long_parameter_name_7,
      long_parameter_name_8);

.. hint:: 这是正确的

  .. code-block:: c

    struct some_long_struct_name_s
    {
      /* The forward link to the next instance of struct
       * some_long_struct_name_s in a singly linked list.
       */

      struct some_long_struct_name_s *flink;
      int short_name1;   /* Short comment 1. */
      int short_name2;   /* This is a very long comment describing subtle
                          * aspects of the short_name2 field. */
    };

    FAR struct some_medium_name_s *ptr = malloc(sizeof(some_medium_name_s);

    FAR struct some_medium_name_s *ptr = malloc(sizeof(some_medium_name_s);

    FAR struct some_long_struct_name_s *ptr = malloc(sizeof(some_long_struct_name_s);

    ret = some_function_with_many parameters(long_parameter_name_1,
                                             long_parameter_name_2,
                                             long_parameter_name_3,
                                             long_parameter_name_4,
                                             long_parameter_name_5,
                                             long_parameter_name_6,
                                             long_parameter_name_7,
                                             long_parameter_name_8);

**注意**：参见 `指针 <#farnear>`__ 的讨论，了解上面使用的 ``FAR`` 限定符。

**双间距**。可以使用单个空行来分隔逻辑分组，设计者认为合适。
单个空行在某些上下文中也是必需的，如本标准中所定义。
禁止使用额外的空行（两个或更多）。

**列式组织**。类似的事物应对齐在同一列，除非这样做会导致
行宽超过限制。

.. note:: 这是可接受的

  .. code-block:: c

    dog = cat;
    monkey = oxen;
    aardvark = macaque;

.. hint:: 这是首选

  .. code-block:: c

    dog      = cat;
    monkey   = oxen;
    aardvark = macaque;

**块注释** 最后的星号（``*``）应出现在第 78 列
（或具有较长行的文件的行宽）。请注意，块注释的
最后注释分隔符是例外，位于第 79 列。

注释
========

**通用**。在注释中，文本必须是标准英语，
符合标准英语语法和拼写规则（美式英语拼写）。
当然，这不是总结所有英语语法的地方，但作为注释中
常见语法问题的示例：

-  所有句子应以大写字符开头，并以 '.'、'?' 或 '!' 结尾。
-  句子片段和短语通常与句子相同处理。
-  标点符号 '.' 和 ':' 后跟两个空格；标点符号 ',' 和 ';' 后跟一个空格。
-  '.' 或 ':' 后的文本以大写字符开头；',' 或 ';' 后的文本以小写字符开头。

**行间距** 每个注释前后应有一个空行。唯一的例外是：

对于从第一行开始的文件头块注释；在这种情况下前面没有空行。
对于条件编译。条件编译应包括条件逻辑*和*与条件逻辑相关的所有注释。
在这种情况下，空行出现在条件*之前*，而不是之后。条件后的注释前面没有空行。
对于花括号。包含开始左花括号的行与注释之间没有空行。
在结束右花括号之前的最后一个注释后面没有空行。
对于标签。包含标签的行与注释之间没有空行。

.. error:: 这是不正确的

  .. code-block:: c

      /* set a equal to b */
      a = b;
      /* set b equal to c */
      b = c;

      /* Do the impossible */

    #ifdef CONFIG_THE_IMPOSSIBLE
      the_impossible();
    #endif

      if (a == b)
        {

          /* Only a comment */

        }

      here:

      /* This is the place */

.. tip:: 这是正确的

  .. code-block:: c

      /* Set a equal to b. */

      a = b;

      /* Set b equal to c. */

      b = c;

    #ifdef CONFIG_THE_IMPOSSIBLE
      /* Do the impossible */

      the_impossible();
    #endif

      if (a == b)
        {
          /* Only a comment */
        }

      here:
        /* This is the place */

**缩进** 注释通常应放在它们适用的代码部分之前。
注释缩进应与以下代码的缩进规则相同（如果适用）。

**简短的单行注释**。简短的注释必须在单行上。
注释分隔符必须在同一行上。

.. error:: 这是不正确的

  .. code-block:: c

    /*
     * This is a single line comment
     */

.. tip:: 这是正确的

  .. code-block:: c

    /* This is a single line comment. */

**多行注释**。如果注释太长无法放在单行上，
它必须分成多行注释。注释必须在多行注释的
第一行以开始注释分隔符（``/*``）开始。
多行注释的后续行必须以星号（``*``）对齐，
与前一行中的星号在同一列。结束注释分隔符
必须在单独的行上，星号（``*``）与前一行中的
星号对齐在同一列。

.. error:: 这是不正确的

  .. code-block:: c

    /*
       This is the first line of a multi-line comment.
       This is the second line of a multi-line comment.
       This is the third line of a multi-line comment. */

    /* This is the first line of another multi-line comment.  */
    /* This is the second line of another multi-line comment. */
    /* This is the third line of another multi-line comment.  */

.. tip:: 这是正确的

  .. code-block:: c

    /* This is the first line of a multi-line comment.
     * This is the second line of a multi-line comment.
     * This is the third line of a multi-line comment.
     */

**语句右侧的注释**。C 源文件中语句右侧的注释不鼓励使用。
如果使用此类注释，它们应（1）非常短，以便不超过行宽
（通常 78 个字符），（2）对齐，使注释在每行的同一列开始。

.. error:: 这是不正确的

  .. code-block:: c

    dog = cat; /* Make the dog be a cat */
    monkey = oxen; /* Make the monkey be an oxen */
    aardvark = macaque; /* Make the aardvark be a macaque */

.. note:: 这是可接受的

  .. code-block:: c

    dog      = cat;     /* Make the dog be a cat. */
    monkey   = oxen;    /* Make the monkey be an oxen. */
    aardvark = macaque; /* Make the aardvark be a macaque. */

.. tip:: 这是首选

  .. code-block:: c

    /* Make the dog be a cat. */

    dog      = cat;

    /* Make the monkey be an oxen. */

    monkey   = oxen;

    /* Make the aardvark be a macaque. */

    aardvark = macaque;

**数据定义右侧的注释**。另一方面，枚举或结构的
声明右侧的注释是鼓励的，前提是注释简短且不超过
最大行宽（通常 78 个字符）。注释的列式对齐非常理想
（但通常在不违反行宽的情况下无法实现）。

.. error:: 这是不正确的

  .. code-block:: c

    struct animals_s
    {
      int dog; /* This is a dog */
      int cat; /* This is a cat */
      double monkey; /* This is a monkey */
      double oxen; /* This is an oxen */
      bool aardvark; /* This is an aardvark */
      bool macaque; /* This is a macaque */
    };

.. note:: 这是可接受的

  .. code-block:: c

    struct animals_s
    {
      int dog;       /* This is a dog. */
      int cat;       /* This is a cat. */
      double monkey; /* This is a monkey. */
      double oxen;   /* This is an oxen. */
      bool aardvark; /* This is an aardvark. */
      bool macaque;  /* This is a macaque. */
    };

.. tip:: 这是首选

  .. code-block:: c

    struct animals_s
    {
      int    dog;      /* This is a dog. */
      int    cat;      /* This is a cat. */
      double monkey;   /* This is a monkey. */
      double oxen;     /* This is an oxen. */
      bool   aardvark; /* This is an aardvark. */
      bool   macaque;  /* This is a macaque. */
    };

**右侧的长注释**。语句或数据定义右侧的注释必须简短，
并且在同一行上适合而不超过最大行长度。如果需要更长的
注释，则应出现在语句或定义的上方而不是右侧。

**在语句右侧拆分长注释** 在语句右侧拆分长注释也是可接受的，
但不鼓励。在这种情况下，注释必须在多行右侧注释的
第一行以开始注释分隔符（/*）开始。多行右侧注释的
后续行必须以星号（*）对齐，与前一行中的星号在同一列。
结束注释分隔符必须与星号在*同一*行上。

.. error:: 这是不正确的

  .. code-block:: c

    dog = cat; /* This assignment will convert what was at one time a lowly dog into a ferocious feline. */

.. note:: 这是可接受的

  .. code-block:: c

    dog = cat;       /* This assignment will convert what was at one time a
                      * lowly dog into a ferocious feline. */

.. tip:: 这是首选

  .. code-block:: c

    /* This assignment will convert what was at one time a lowly dog into a
     * ferocious feline.
     */

    dog = cat;

**注意**，如果注释在多行上继续，注释对齐和多行注释规则
仍然适用，但有一个例外：结束 ``*/`` 出现在注释的最后一行
文本的同一行。此规则的例外是为了防止语句和定义变得
过于分散。

**块注释**。块注释仅用于在整体 `文件组织 <#fileorganization>`__
中界定分组，除非用法与界定程序中的逻辑分组一致，否则不应使用。

**C 风格注释**。C99/C11/C++ 风格注释（以 ``//`` 开头）不应
在 NuttX 中使用。NuttX 通常遵循 C89，架构特定目录之外的所有代码
必须与 C89 兼容。

.. error:: 这是不正确的

  .. code-block:: c

    // This is a structure of animals
    struct animals_s
    {
      int    dog;      // This is a dog
      int    cat;      // This is a cat
      double monkey;   // This is a monkey
      double oxen;     // This is an oxen
      bool   aardvark; // This is an aardvark
      bool   macaque;  // This is a macaque
    };

.. tip:: 这是正确的

  .. code-block:: c

    /* This is a structure of animals. */

    struct animals_s
    {
      int    dog;      /* This is a dog. */
      int    cat;      /* This is a cat. */
      double monkey;   /* This is a monkey. */
      double oxen;     /* This is an oxen. */
      bool   aardvark; /* This is an aardvark. */
      bool   macaque;  /* This is a macaque. */
    };

**"注释掉"大代码块**。不要使用 C 或 C++ 注释来禁用
大块代码的编译。而是使用 ``#if 0`` 来完成。
确保在 ``#if 0`` 之前有注释来解释为什么代码不被编译。

.. error:: 这是不正确的

  .. code-block:: c

    void some_function(void)
    {
      ... compiled code ...

      /*
      ... disabled code ..
       */

      ... compiled code ...
    }

    void some_function(void)
    {
      ... compiled code ...

      //
      // ... disabled code ..
      //

      ... compiled code ...
    }

.. tip:: 这是正确的

  .. code-block:: c

    void some_function(void)
    {
      ... compiled code ...

      /* The following code is disabled because it is no longer needed. */

    #if 0
      ... disabled code ..
    #endif

      ... compiled code ...
    }

花括号
======

通常，NuttX 编码标准中花括号的使用与 `GNU 编码标准 <https://www.gnu.org/prep/standards/standards.pdf>`__
中的花括号使用类似，有一些细微差异。

**编码标准：**

-  **总是在单独的行上**。花括号总是在单独的行上出现，
   除了空白外不包含其他内容。
-  **花括号上不要放注释**。不要在与花括号同一行上放注释。
-  **复合语句**。在本文档中，开始左花括号后跟一系列语句，
   以结束右花括号结束的称为*复合语句*。
-  **嵌套复合语句**。在嵌套复合语句以多个连续右花括号结束的情况下，
   每个结束右花括号必须在单独的行上，并且必须缩进以匹配
   相应的开始花括号。
-  **最后花括号后跟单个空行**。*最后*右花括号后必须跟一个空行，
   按照标准规则。此规则有两个例外：

   #. 在嵌套多个连续右花括号的情况下，除了*最后*右花括号后
      不应插入空行。
   #. 当结束右花括号后跟 ``break;`` 语句时，不应使用空行分隔。

-  **特殊缩进规则**。特殊的 `缩进规则 <#indentation>`__ 适用于花括号。

.. error:: 这是不正确的

  .. code-block:: c

    while (true)
      {
        if (valid)
          {
          ...
          } /* if valid */
        else
          {
          ...
          } /* not valid */
      } /* end forever */
    if (a < b) {
      if (a < 0) {
          c = -a;
      } else {
          c = a;
      }
    } else {
      if (b < 0) {
          c = -b;
      } else {
          c = b;
      }
    }

.. tip:: 这是正确的

  .. code-block:: c

    while (true)
      {
        if (valid)
          {
          ...
          }
        else
          {
          ...
          }
      }

    if (a < b)
      {
        if (a < 0)
          {
            c = -a;
          }
        else
          {
            c = a;
          }
      }
    else
      {
        if (b < 0)
          {
            c = -b;
          }
        else
          {
            c = b;
          }
      }

**花括号缩进规则的例外**。例外是结构、枚举、联合和函数声明
后面的花括号。这些花括号没有额外的缩进；这些花括号与
定义的开头对齐。

.. error:: 这是不正确的

  .. code-block:: c

    enum kinds_of_dogs_e
      {
      ...
      };

    struct dogs_s {
      ...
      union {
      ...
      } u;
      ...
    };

    struct cats_s
      {
      ...
        union
         {
         ...
         } u;
      ...
      };

    int animals(int animal)
      {
      ...
      }

.. tip:: 这是正确的

  .. code-block:: c

    enum kinds_of_dogs_e
    {
      ...
    };

    struct dogs_s
    {
      ...
      union
      {
      ...
      } u;
      ...
    };

    struct cats_s
    {
      ...
      union
      {
      ...
      } u;
      ...
    };

    int animals(int animal)
    {
      ...
    }

缩进
===========

通常，NuttX 编码标准中的缩进与 `GNU 编码标准 <https://www.gnu.org/prep/standards/standards.pdf>`__
中的缩进要求类似，有一些细微差异。

**缩进单位**。缩进以两个空格为单位；每个缩进级别比前一个
缩进级别向右两个空格。TAB 字符不能用于缩进。

.. error:: 这是不正确的

  .. code-block:: c

    if (x == y) {
	    dosomething(x);
    }

      if (x == y) {
          dosomething(x);
      }

.. tip:: 这是正确的

  .. code-block:: c

    if (x == y)
      {
        dosomething(x);
      }

**TAB 字符的使用**。在 C 源文件和头文件中禁止使用 TAB 字符进行缩进。
但是，TAB 字符用于 make 文件、汇编语言源文件、Kconfig 文件和某些脚本文件。
当在这些文件中使用 TAB 字符时，空格不能用于缩进。
在这些情况下，正确的 TAB 设置是 4 个空格（不是 8 个）。

**花括号对齐**。请注意，由于花括号必须在单独的行上（见上文），
这种两个空格的缩进有一个有趣的特性：

-  所有 C 语句（和 case 选择器）位于 4 空格倍数的行上
   （从两个缩进开始）：2、6、10、... (4*n + 2)（对于缩进级别 n = 0, 1, ...）

-  花括号也在单独的行上，也缩进 4 空格的倍数：
   4、8、12、... 4*n（对于缩进级别 n = 1, 2, ...）

因此，缩进级别的所有代码应对齐在同一列。
类似地，同一缩进级别的开始和结束花括号也应对齐在
同一（但不同的）列。

**预处理器行的缩进**。任何条件计算后的 C 预处理器命令
也遵循基本相同的缩进规则，不同之处在于 ``#`` 始终
保留在第 1 列。

当 C 预处理器语句被缩进时，它们应按每个缩进级别
在 ``#`` 后缩进 2 个空格。当 C 预处理器语句被包含在
C 预处理器条件逻辑（``#if``.. ``#endif``）中时，
应缩进 C 预处理器语句。缩进级别随着此类嵌套
条件逻辑的每个级别而增加。

在每个文件的 ``预处理器定义`` `部分 <#cfilestructure>`__ 中，
C 预处理器语句应始终以此方式缩进。在文件的
``公共/私有数据`` 和 ``公共/私有函数`` 部分中，
C 预处理器语句可以缩进。然而，C 预处理器语句的缩进
经常与 C 代码的缩进冲突，使代码更难阅读。
在这种情况下，应省略这些部分中 C 预处理器语句的缩进。

.. error:: 这是不正确的

  .. code-block:: c

    #ifdef CONFIG_ABC
    #define ABC_THING1 1
    #define ABC_THING2 2
    #define ABC_THING3 3
    #endif

    #ifdef CONFIG_ABC
      #define ABC_THING1 1
      #define ABC_THING2 2
      #define ABC_THING3 3
    #endif

.. tip:: 这是正确的

  .. code-block:: c

    #ifdef CONFIG_ABC
    #  define ABC_THING1 1
    #  define ABC_THING2 2
    #  define ABC_THING3 3
    #endif

    #ifdef CONFIG_ABC
    #  define ABC_THING1 1
    #  define ABC_THING2 2
    #  define ABC_THING3 3
    #endif

**例外**。每个头文件在开头包含 `幂等定义 <#idempotence>`__。
此条件编译*不会*导致缩进的任何更改。

.. error:: 这是不正确的

  .. code-block:: c

    #ifndef __INCLUDE_SOMEHEADER_H
    #  define __INCLUDE_SOMEHEADER_H
    ...
    #  define THING1 1
    #  define THING2 2
    #  define THING3 3
    ...
    #endif /* __INCLUDE_SOMEHEADER_H */

.. tip:: 这是正确的

  .. code-block:: c

    #ifndef __INCLUDE_SOMEHEADER_H
    #define __INCLUDE_SOMEHEADER_H
    ...
    #define THING1 1
    #define THING2 2
    #define THING3 3
    ...
    #endif /* __INCLUDE_SOMEHEADER_H */

括号
===========

**编码标准：**

-  **关键字后加空格**。不要在任何 C 关键字（``for``、``switch``、
   ``while``、``do``、``return`` 等）后立即放左括号（``(``）。
   在这些情况下，在左括号前放一个空格。
-  **否则，左括号前不加空格**。否则，左括号前不应有空格。
-  **函数名和参数列表之间不加空格**。函数名和参数列表之间
   不应有空格。
-  **右括号前永远不加空格**。右括号（ ``)`` ）前永远不应有空格。
-  **返回值不加括号**。返回值永远不应被括号括起来，
   除非括号是强制正确的运算顺序所必需的。

.. error:: 这是不正确的

  .. code-block:: c

    int do_foobar ( void )
    {
      int ret = 0;
      int i;

      for( i = 0; ( ( i < 5 ) || ( ret < 10 ) ); i++ )
        {
          ret = foobar ( i );
        }

      return ( ret );
    }

.. tip:: 这是正确的

  .. code-block:: c

    int do_foobar(void)
    {
      int ret = 0;
      int i;

      for (i = 0; i < 5 || ret < 10; i++)
        {
          ret = foobar(i);
        }

      return ret;
    }

**注意：** 许多人不信任自己对运算符优先级的理解，
因此在表达式中使用大量括号来强制求值顺序，
即使括号可能没有效果。这当然可以避免由于意外的
求值顺序导致的错误，但也会使代码丑陋和过于复杂
（如上例所示）。通常，NuttX 不使用不必要的括号
来强制运算顺序。在这方面没有特别的政策。
但是，建议您在必要时查阅 C 编程语言书籍，
并尽可能避免不必要的括号。

*************************
数据和类型定义
*************************

每行一个定义/声明
===================================

.. error:: 这是不正确的

  .. code-block:: c

    extern long time, money;
    char **ach, *bch;
    int i, j, k;

.. tip:: 这是正确的

  .. code-block:: c

    extern long time;
    extern long money;
    FAR char **ach;
    FAR char *bch;
    int i;
    int j;
    int k;

**注意**：参见 `指针 <#farnear>`__ 的讨论，了解上面使用的 ``FAR`` 限定符。

全局变量
================

**全局 vs. 局部 vs. 公共 vs. 私有** *全局*变量指的是在函数外部定义的
任何变量。区分在于这种*全局*和函数*局部*定义之间的区别，
指的是符号*在文件内*的作用域。文件内定义的所有*全局*名称的
相关概念是名称在不同文件之间的作用域。如果全局符号前面有
``static`` 存储类，则全局符号的作用域仅在文件内。
这是一个稍微不同的概念，在 NuttX 中您会发现它们被区分为
*私有*与*公共*全局符号。然而，在本标准中，术语*全局变量*
将指任何具有超过局部作用域的变量。

**编码标准：**

-  **简短的全局变量名**。名称应简洁，但通常描述变量的用途。
   尝试用变量名表达一些信息，但不要尝试表达太多。
   例如，变量名 ``g_filelen`` 比 ``g_lengthoffile`` 更可取。
-  **全局变量前缀**。所有全局变量以 ``g_`` 前缀开头，
   以指示变量的作用域。
-  **模块名前缀** 如果全局变量属于名为 ``xyz`` 的*模块*，
   则该模块应作为前缀包含，如：``g_xyz_``。
-  **小写**，使用所有小写字母。
-  **最小化使用** ``_``。名称中最好不要有 ``_`` 分隔符。
   长变量名可能需要使用 ``_`` 进行一些分隔。
   但是，长变量名是不鼓励的。
-  **使用结构**。如果可能，将所有全局变量包装在结构中，
   以最小化名称冲突的可能性。
-  **尽可能避免全局变量**。一般不鼓励使用全局变量，
   除非没有其他合理的解决方案。

.. error:: 这是不正确的

  .. code-block:: c

    extern int someint;
    static int anotherint;
    uint32_t dwA32BitInt;
    uint32_t gAGlobalVariable;

.. note:: 这是可接受的

  .. code-block:: c

    extern int g_someint;
    static int g_anotherint;
    uint32_t g_a32bitint;
    uint32_t g_aglobal;

.. tip:: 这是首选

  .. code-block:: c

    struct my_variables_s
    {
      uint32_t a32bitint;
      uint32_t aglobal;
    };

    extern int g_someint;
    static int g_anotherint;
    struct my_variables_s g_myvariables;

参数和局部变量
==============================

**编码标准：**

-  **通用命名标准**。函数参数和局部变量的命名相同。
-  **简短的变量名**。名称应简洁，但通常描述变量的用途。
   尝试用变量名表达一些信息，但不要尝试表达太多。
   例如，变量名 ``len`` 比 ``lengthofiobuffer`` 更可取。
-  **无特殊装饰**。没有特殊的装饰来指示变量是局部变量。
   如果有助于将变量与其他类似名称的局部变量区分开来，
   前缀 ``p`` 或 ``pp`` 可以用于指针（或指向指针的指针）的名称。
   即使这种约定在不必要时也不鼓励。
-  **小写** 使用所有小写字母。
-  **最小化使用单字符变量名**。首选短变量名。
   但是，应避免单字符变量名。例外包括 ``i``、``j`` 和 ``k``，
   它们仅保留用作循环索引（我们 Fortran 遗产的一部分）。
-  **最小化使用** ``_``。名称中最好不要有 ``_`` 分隔符。
   长变量名可能需要使用 ``_`` 进行一些分隔。
   但是，长变量名是不鼓励的。

.. error:: 这是不正确的

  .. code-block:: c

    uint32_t somefunction(int a, uint32_t dwBValue)
    {
      uint32_t this_is_a_long_variable_name = 1;
      int i;

      for (i = 0; i &lt; a; i++)
        {
          this_is_a_long_variable_name *= dwBValue--;
        }

      return this_is_a_long_variable_name;
    }

.. tip:: 这是正确的

  .. code-block:: c

    uint32_t somefunction(int limit, uint32_t value)
    {
      uint32_t ret = 1;
      int i;

      for (i = 0; i &lt; limit; i++)
        {
          ret *= value--;
        }

      return ret;
    }

**注意：** 您会看到代码库中经常使用名为 ``ret`` 的局部变量，
用于表示将返回其值或接收调用函数返回值的局部变量。

类型定义
================

**编码标准：**

-  **简短的类型名**。类型名应简洁，但通常描述类型的用途。
   尝试用类型名表达一些信息，但不要尝试表达太多。
   例如，类型名 ``fhandle_t`` 比 ``openfilehandle_t`` 更可取。
-  **类型名后缀**。所有 ``typedef`` 定义的名称以 ``_t`` 后缀结尾。
-  **模块名前缀** 如果类型属于名为 ``xyz`` 的*模块*，
   则该模块应作为前缀包含，如：``xyz_``。
-  **小写**。使用所有小写字母。
-  **最小化使用** ``_``。类型名中最好少有 ``_`` 分隔符。
   长类型名可能需要使用 ``_`` 进行一些分隔。
   但是，长类型名是不鼓励的。

.. error:: 这是不正确的

  .. code-block:: c

    typedef void *myhandle;
    typedef int myInteger;

.. tip:: 这是正确的

  .. code-block:: c

    typedef FAR void *myhandle_t;
    typedef int myinteger_t;

**注意**：参见 `指针 <#farnear>`__ 的讨论，了解上面使用的 ``FAR`` 限定符。

结构
==========

**结构命名**

-  **无未命名结构**。所有结构必须命名，即使它们是类型定义的一部分。
   也就是说，结构名称必须在所有结构定义中跟在保留字 ``struct`` 之后。
   此规则有两个例外：

   #. 首先是在另一个联合或结构中定义的结构（不鼓励）。在这些情况下，
      应始终省略结构名称。
   #. 其次是作为局部变量类型的结构。在这种情况下，同样应始终省略结构名称。

-  **不鼓励在结构中定义结构**。结构中的字段可以是另一个仅在包含结构
   的作用域内定义的结构。此做法是可接受的，但不鼓励。
-  **无未命名结构字段**。结构可以包含其他结构作为字段。
   在这种情况下，结构字段必须命名。C11 允许结构中的此类未命名结构字段。
   NuttX 通常遵循 C89，架构特定目录之外的所有代码必须与 C89 兼容。
-  **类型定义中不要定义结构**。在类型定义中定义结构的做法是不鼓励的。
   首选结构定义和类型定义是分开的定义。通常，NuttX 编码风格不鼓励
   对结构进行任何 ``typedef``；通常在整个代码中使用完整的结构名作为类型。
   这样做的原因是结构指针可以在头文件中前向引用，而无需包含提供
   类型定义的文件。这大大减少了头文件耦合。
-  **简短的结构名**。结构名应简洁，但通常描述结构包含的内容。
   尝试用结构名表达一些信息，但不要尝试表达太多。
   例如，结构名 ``xyz_info_s`` 比 ``xyz_datainputstatusinformation_s``
   更可取。
-  **结构名后缀**。所有结构名以 ``_s`` 后缀结尾。
-  **模块名前缀** 如果结构属于名为 ``xyz`` 的*模块*，
   则该模块应作为前缀包含，如：``xyz_``。
-  **小写**。使用所有小写字母。
-  **最小化使用** ``_``。结构名中最好少有 ``_`` 分隔符。
   长变量名可能需要使用 ``'_'`` 进行一些分隔。
   但是，长变量名是不鼓励的。

**结构字段命名**

-  **通用变量命名**。结构字段命名通常与局部变量相同。
-  **每行一个定义**。`每行一个定义 <#onedatperline>`__ 规则适用于
   结构字段，包括位字段定义。
-  **每个字段应有注释**。每个结构字段应有注释。
   注释应遵循 `标准规范 <#comments>`__。
-  **可选的结构字段前缀**。在每个字段名前添加两个字母的前缀
   以明确字段属于哪个结构可能有所帮助。虽然这是一种好做法，
   但该约定在 NuttX 中并未一致使用。
-  **小写**。使用所有小写字母。
-  **最小化使用** ``_``。字段名中最好少有 ``_`` 分隔符。
   长变量名可能需要使用 ``'_'`` 进行一些分隔。
   但是，长变量名是不鼓励的。

**其他适用的编码标准**。参见与 `行格式 <#lines>`__、
`花括号使用 <#braces>`__、`缩进 <#indentation>`__ 和
`注释 <#comments>`__ 相关的部分。

**大小优化**。在声明结构中的字段时，按数据大小排序声明，
以最小化数据对齐导致的内存浪费。这本质上意味着字段应按数据大小
组织，而不是按功能：将所有指针放在一起，所有 ``uint8_t`` 放在一起，
所有 ``uint32_t`` 放在一起。像 ``uint8_t`` 和 ``uint32_t`` 这样
已知大小的数据类型也应按升序或降序排列。

.. error:: 这是不正确的

  .. code-block:: c

    typedef struct       /* Un-named structure */
    {
      ...
      int val1, val2, val3; /* Values 1-3 */
      ...
    } xzy_info_t;

    struct xyz_information
    {
      ...
      uint8_t bita : 1,  /* Bit A */
              bitb : 1,  /* Bit B */
              bitc : 1;  /* Bit C */
      ...
    };

    struct abc_s
    {
      ...
      struct
      {
        int a;           /* Value A */
        int b;           /* Value B */
        int c;           /* Value C */
      };                 /* Un-named structure field */
      ...
    };

.. tip:: 这是正确的

  .. code-block:: c

    struct xyz_info_s
    {
      ...
      int val1;          /* Value 1 */
      int val2;          /* Value 2 */
      int val3;          /* Value 3 */
      ...
    };

.. warning:: 这是不鼓励的

  .. code-block:: c

    typedef struct xyz_info_s xzy_info_t;

使用 typedef 定义的结构是可接受的，但不鼓励。

.. tip:: 这是正确的

  .. code-block:: c

    struct xyz_info_s
    {
      ...
      uint8_t bita : 1,  /* Bit A */
      uint8_t bitb : 1,  /* Bit B */
      uint8_t bitc : 1,  /* Bit C */
      ...
    };

.. warning:: 这是不鼓励的

  .. code-block:: c

    struct abc_s
    {
      ...
      struct
      {
        int a;           /* Value A */
        int b;           /* Value B */
        int c;           /* Value C */
      } abc;
      ...
    };

使用在其他结构中定义的结构是可接受的，前提是它们定义了命名字段。
然而，在另一个结构的作用域内定义结构的一般做法仍然不鼓励。
以下是首选：

.. tip:: 这是首选

  .. code-block:: c

    struct abc_s
    {
      ...
      int a;             /* Value A */
      int b;             /* Value B */
      int c;             /* Value C */
      ...
    };

联合
======

**联合和字段命名**。联合和联合内字段的命名遵循与
`结构和结构字段 <#structures>`__ 相同的命名规则。
唯一的区别是使用后缀 ``_u`` 来标识联合。

**其他适用的编码标准**。参见与 `行格式 <#lines>`__、
`花括号使用 <#braces>`__、`缩进 <#indentation>`__ 和
`注释 <#comments>`__ 相关的部分。

.. note:: 这是可接受的

  .. code-block:: c

    union xyz_union_u  /* All unions must be named */
    {
      uint8_t  b[4];   /* Byte values. */
      uint16_t h[2];   /* Half word values. */
      uint32_t w;      /* Word Value. */
    };

    typedef union xyz_union_u xzy_union_t;

使用 typedef 定义的联合是可接受的，但不鼓励。

.. tip:: 这是首选

  .. code-block:: c

    struct xyz_info_s
    {
      ...
      union
      {
        uint8_t  b[4]; /* Byte values. */
        uint16_t h[2]; /* Half word values. */
        uint32_t w;    /* Word Value. */
      } u;             /* All union fields must be named */
      ...
    };

**注意：** 请注意，结构中的联合字段通常命名为 ``u``。
这是对禁止使用单字符变量和字段名的另一个例外。
短字段名 ``u`` 清楚地标识了联合字段，并防止联合值的
全名过长。

枚举
============

**枚举命名**。枚举的命名遵循与 `结构 <#structures>`__ 和
`联合 <#unions%22>`__ 相同的命名规则。
唯一的区别是使用后缀 ``_e`` 来标识枚举。

**枚举值命名**。然而，枚举值遵循更类似于 `宏 <#macros>`__ 的命名约定。

-  **大写**。枚举值始终大写。
-  **鼓励使用** ``_``。与其他命名不同，鼓励使用下划线字符 ``_``
   来分隔枚举名称。
-  **前缀**。枚举中的每个值应以大写前缀开头，标识该值为枚举的成员。
   理想情况下，此前缀应源自枚举的名称。
-  **无悬挂逗号**。枚举的最后一个值不应有悬挂逗号。
   最常用的工具链对这种悬挂逗号是宽容的，但其他工具链不会。

**其他适用的编码标准**。参见与 `行格式 <#lines>`__、
`花括号使用 <#braces>`__、`缩进 <#indentation>`__ 和
`注释 <#comments>`__ 相关的部分。

.. tip:: 这是正确的

  .. code-block:: c

    enum xyz_state_e
    {
      XYZ_STATE_UNINITIALIZED = 0, /* Uninitialized state. */
      XYZ_STATE_WAITING,           /* Waiting for input state. */
      XYZ_STATE_BUSY,              /* Busy processing input state. */
      XYZ_STATE_ERROR,             /* Halted due to an error. */
      XYZ_STATE_TERMINATING,       /* Terminating stated. */
      XYZ_STATE_TERMINATED         /* Terminating stated. */
    };

C 预处理器宏
======================

**编码标准：**

**宏命名**。宏命名遵循与 `枚举值 <#enumerations>`__ 类似的命名约定。

-  **大写**。宏名称始终大写。
-  **小写例外**。NuttX 宏名称中有一些小写值。
   例如用于句点或小数点的小写 ``p``（如 ``VOLTAGE_3p3V``）。
   小写 ``v`` 也用于版本号（如 ``CONFIG_NET_IPv6``）。
   然而，这些是规则的例外，而不是说明规则。
-  **可能是函数的宏**。如果宏是可能在其他上下文中使用的函数名的
   替代品，则小写宏名称也是可接受的。在这种情况下，适用正常的函数命名。
-  **鼓励使用** ``_``。与其他命名不同，鼓励使用下划线字符 ``_``
   来分隔宏名称。
-  **前缀**。每个相关的宏值应以大写前缀开头，标识该值为值集的一部分
   （并最小化命名冲突的可能性）。
-  ``#define`` **后单个空格**。单个空格字符应将 ``#define`` 与宏名称分隔。
   从不使用制表符。
-  **正常注释规则**。适用正常的注释规则。
-  **行继续**。宏定义可以通过在换行符前用 ``\\`` 字符终止行来
   继续到下一行。``\\`` 字符前应有一个空格。
   多行继续上对齐的 ``\\`` 字符是不鼓励的，因为它们是维护问题。
-  **宏参数展开周围加括号**。宏可以有参数列表。
   在宏展开中，每个参数应被括号括起来。
-  **真实语句**。如果宏作为语句使用，则宏展开应包装在
   ``do { ... } while (0)`` 中，以确保宏确实是一个语句。
-  **代码中禁止魔法数字**。任何不直观的数字值必须适当命名，
   并作为预处理器宏或枚举值提供。
-  **副作用**。注意副作用。
-  **缩进**。参见上面的 `预处理器行缩进 <#indentation>`__ 要求。

**其他适用的编码标准**。参见与 `行格式 <#lines>`__、
`缩进 <#indentation>`__ 和 `注释 <#comments>`__ 相关的部分。

.. error:: 这是不正确的

  .. code-block:: c

    #define max(a,b) a > b ? a : b

    #define ADD(x,y) x + y

    #ifdef HAVE_SOMEFUNCTION
    int somefunction(struct somestruct_s* psomething);
    #else
    #define SOMEFUNCTION() (0)
    #endif

    #	define	IS_A_CAT(c)		((c) == A_CAT)

    #define LONG_MACRO(a,b)                                  \
      {                                                      \
        int value;                                           \
        value = b-1;                                         \
        a = b*value;                                         \
      }

    #define DO_ASSIGN(a,b) a = b

.. tip:: 这是正确的

  .. code-block:: c

    #define MAX(a,b) (((a) > (b)) ? (a) : (b))

    #define ADD(x,y) ((x) + (y))

    #ifdef HAVE_SOMEFUNCTION
    int somefunction(struct somestruct_s* psomething);
    #else
    #  define somefunction(p) (0)
    #endif

    # define IS_A_CAT(c)  ((c) == A_CAT)

    #define LONG_MACRO(a,b) \
      { \
        int value; \
        value = (b)-1; \
        (a) = (b)*value; \
      }

    #define DO_ASSIGN(a,b) do { (a) = (b); } while (0)

.. _farnear:

指针变量
=================

**指针命名**。指针遵循与其他变量类型相同的命名约定。
指针（或指向指针的指针）变量可以在 ``p``（或 ``pp``）前面
加上 ``p``（或 ``pp``），中间没有下划线字符 ``_``，
以标识该变量是指针。然而，这种约定不鼓励使用，
只有在有理由担心可能与其他仅不是指针的变量混淆时才合适。

**空白**。指针变量声明中使用的星号或解引用指针变量时
应紧接在变量名之前，中间没有空格。在转换为指针类型时，
星号前应有一个空格。

.. error:: 这是不正确的

  .. code-block:: c

    int somefunction(struct somestruct_s* psomething);

    ptr = (struct somestruct_s*)value;

.. tip:: 这是正确的

  .. code-block:: c

    int somefunction(FAR struct somestruct_s *something);

    ptr = (FAR struct somestruct_s *)value;

.. c:macro:: FAR

``FAR``、``NEAR``、``DSEG`` 和 ``CODE`` 指针。某些架构需要
指针上的限定符来标识指针引用的地址空间。
``FAR``、``NEAR``、``DSEG`` 和 ``CODE`` 宏在
``include/nuttx/compiler.h`` 中定义，在需要时为此限定符提供含义。
为了可移植性，一般规则是可能位于栈、堆、``.bss`` 或 ``.data``
中的数据指针应以 ``FAR`` 限定符开头；函数指针可能位于代码地址空间中，
应具有 ``CODE`` 限定符。这些宏在具有意义的架构上的典型效果是
确定指针的大小（指针值的位宽度）。

初始化
============

**适用的编码标准**。参见与 `括号 <#parentheses>`__ 相关的部分。

**C89 兼容性**。所有通用 NuttX 代码必须符合 ANSI C89 要求。
较新的 C 标准允许使用命名初始化器和数组初始化器进行更灵活的初始化。
然而，这些与 C89 不向后兼容，不能在通用代码中使用。
较新的 C99 功能可以在架构特定子目录中包含，在那里不可能使用
较旧的工具链。C11 包含在 NuttX 中，但尚未经过验证，
因此不鼓励在任何地方使用。

*********
函数
*********

函数头
================

**编码标准：**

-  **函数头**。每个函数前面有一个函数头。函数头是提供
   函数信息的*块注释*。块注释包括以下内容：

   -  块注释以一行开始，该行由第 1 列的开始 C 注释（``/*``）后跟
      一系列星号组成，延伸到行的长度（通常到第 78 列）。
   -  块注释以一行结束，该行由一系列星号从第 2 列开始延伸到
      行尾附近（通常到第 77 列），后跟结束 C 注释
      （通常在第 78 列，总长度为 79 个字符）。
   -  关于函数的信息包含在第一行和最后一行之间的行中。
      每行以第 1 列的空格、第 2 列的星号（``*``）和第 3 列的空格开头。

-  **函数头前有一个空行**。每个函数头前正好有一个空行。
-  **函数头后有一个空行**。函数头和函数定义之间正好有一个空行。
-  **函数头部分**。在函数头中，必须提供以下数据部分：

   -  ``* Name:`` 后跟同一行上的函数名。
   -  ``* Description:`` 后跟从第二行开始的函数描述。
      函数描述的每行额外缩进两个空格。
   -  ``* Input Parameters:`` 后跟从第二行开始的每个输入参数的描述。
      每个输入参数以额外缩进两个空格的分隔行开始。
      描述需要包括（1）输入参数的名称，和（2）输入参数的简短描述。
   -  ``* Returned Value:`` 后跟从第二行开始的返回值描述。
      返回值的描述应标识函数返回的所有错误值。
   -  ``* Assumptions/Limitations:`` 后跟正确使用函数所需的
      任何额外信息。此部分是可选的，如果函数使用不需要此类特殊信息，
      可以省略。

   这些数据部分中的每一个都用 ``*`` 的单行分隔。

**函数头模板**。参见 `附录 A <#cfilestructure>`__ 了解函数头的模板。

函数命名
===============

**编码标准：**

-  **简短的函数名**。函数名应简洁，但通常描述函数的用途。
   尝试用函数名表达一些信息，但不要尝试表达太多。
   例如，变量名 ``xyz_putvalue`` 比
   ``xyz_savethenewvalueinthebuffer`` 更可取。
-  **小写**。使用所有小写字母。
-  **模块前缀**。同一*模块*、*子系统*或同一文件中的所有函数
   应具有以公共前缀开头的名称，用下划线 ``'_'`` 字符与函数名的
   其余部分分隔。例如，对于名为 *xyz* 的模块，所有函数应以
   ``xyz_`` 开头。
-  **扩展前缀**。其他更大的功能分组应具有命名约定中的另一个级别。
   例如，如果模块 *xyz* 包含一组管理 I/O 缓冲区 (IOB) 的函数，
   则这些函数都应以公共前缀开头，如 ``xyz_iob_``。
-  **不鼓励使用** ``_``。在函数命名中进一步使用 ``'_'`` 分隔符
   是不鼓励的。长函数名可能需要使用 ``'_'`` 进行一些额外的分隔。
   但是，长函数名也是不鼓励的。
-  **动词和对象**。函数名的其余部分应采用*动词-对象*或*对象-动词*形式。
   只要在*模块*内使用一致，哪种都可以。常见的动词包括用于检索数据的
   *get* 和用于存储数据的 *set*（或 *put*）。动词 *is* 保留用于执行
   某些测试并返回布尔值以指示测试结果的函数。在这种情况下，*对象*
   应指示正在测试什么，``true`` 的返回值应与测试结果为真一致。

参数列表
===============

**编码标准**。参见 `参数命名 <#localvariable>`__ 的通用规则。
另请参见与 `括号 <#parentheses>`__ 使用相关的部分。

**使用** ``const`` **参数**。鼓励使用 ``const`` 存储类。
这适用于指示函数不会修改对象。

函数体
=============

**编码标准：**

-  **单个复合语句**。函数体由单个复合语句组成。
-  **第 1 列的花括号** 复合语句的开始和结束花括号必须放在第 1 列。
-  **第 3 列的第一个定义或语句**。函数体中的第一个数据定义或语句
   缩进两个空格。语句的标准在 `以下段落 <#statements>`__ 中介绍。
-  **局部变量优先**。因为 NuttX 符合较旧的 C89 标准，
   在复合语句上具有作用域的所有变量必须在任何可执行语句之前
   在复合语句的开头定义。局部变量定义与以下可执行语句序列
   混合是禁止的。局部变量定义后必须跟一个空行，
   将局部变量定义与以下可执行语句分开。
   **注意**，函数体由复合语句组成，但通常 ``if``、``else``、
   ``for``、``while``、``do`` 后面的语句也是如此。
   局部变量定义也可以在这些复合语句的开头使用。
-  **不鼓励长函数**。根据经验，函数的长度应限制为适合单页
   （如果您要打印源代码）。
-  **返回语句**。``return`` 语句的参数*不应*被括号括起来。
   合理的例外是返回值参数是复杂表达式且括号提高代码可读性的情况。
   此类复杂表达式可能是布尔表达式或包含条件的表达式。
   简单的算术计算不会被视为*复杂*表达式。
-  **函数体后的空格**。函数体的结束右花括号后必须有一个（且仅一个）空行。

**其他适用的编码标准**。参见与 `通用规范 <#general>`__、
`参数和局部变量 <#localvariable>`__ 和 `语句 <#statements>`__ 相关的部分。

.. error:: 这是不正确的

  .. code-block:: c

    int myfunction(int a, int b)
      {
        int c, d;
        c = a
        d = b;

        int e = c + d;

        for (int i = 0; i &lt; a; i++)
          {
            for (int j = 0; j &lt; b; j++)
              {
                e += j * d;
              }
          }

        return (e / a);
      }

.. tip:: 这是正确的

  .. code-block:: c

    int myfunction(int a, int b)
    {
      int c;
      int d;
      int e;
      int i;

      c = a
      d = b;
      e = c + d;

      for (i = 0; i &lt; a; i++)
        {
          int j;

          for (j = 0; j &lt; b; j++)
            {
              e += j * d;
            }
        }

      return e / a;
    }

返回值
===============

**操作系统内部函数**。通常，操作系统内部函数返回 ``int`` 类型
以指示成功或失败条件。非负值表示成功。零返回值是典型的
成功返回值，但其他成功的返回可以用其他正值表示。
错误总是用负值报告。这些负值必须是文件
``nuttx/include/errno.h`` 中定义的明确定义的 ``errno``。

**应用程序/操作系统接口**。除少数外，所有操作系统接口都符合
本文档编码标准之上的文档标准。

**检查返回值**。操作系统内部函数的调用者应始终检查返回值是否有错误。
至少，调试语句应指示发生了错误。忽略的返回值总是可疑的。
特别地，对 ``malloc`` 或 ``realloc`` 的所有调用必须检查内存分配失败，
以避免使用 NULL 指针。

**********
语句
**********

每行一个语句
======================

**编码标准：**

-  **每行一个语句**。一行上永远不应有多个语句。
-  **每个语句不超过一个赋值**。与此相关，同一语句中不应有多个赋值。
-  **语句不应与任何关键字在同一行**。语句不应与 case 选择器或
   任何 C 关键字在同一行。

**其他适用的编码标准**。参见与 `花括号使用 <#braces>`__ 相关的部分。

.. error:: 这是不正确的

  .. code-block:: c

    if (var1 &lt; var2) var1 = var2;

    case 5: var1 = var2; break;

    var1 = 5; var2 = 6; var3 = 7;

    var1 = var2 = var3 = 0;

.. tip:: 这是正确的

  .. code-block:: c

    if (var1 &lt; var2)
      {
        var1 = var2;
      }

    case 5:
      {
        var1 = var2;
      }
      break;

    var1 = 5;
    var2 = 6;
    var3 = 7;

    var1 = 0;
    var2 = 0;
    var3 = 0;

类型转换
=====

**编码标准：**

-  **类型转换中不加空格**。类型转换和被转换的值之间不应有空格。

.. error:: 这是不正确的

  .. code-block:: c

    struct something_s *x = (struct something_s*) y;

.. tip:: 这是正确的

  .. code-block:: c

    struct something_s *x = (struct something_s *)y;

运算符
=========

**二元运算符前后加空格**。所有二元运算符（出现在两个值之间的运算符），
如 ``+``、``-``、``=``、``!=``、``==``、``>`` 等，
应在运算符前后各有一个空格，以提高可读性。例如：

.. error:: 这是不正确的

  .. code-block:: c

    for=bar;
    if(a==b)
    for(i=0;i<5;i++)

.. tip:: 这是正确的

  .. code-block:: c

    for = bar;
    if (a == b)
    for (i = 0; i < 5; i++)

**一元运算符不加空格分隔**。一元运算符（仅对一个值操作的运算符），
如 ``++``，运算符和它们操作的变量或数字之间*不应*有空格。

.. error:: 这是不正确的

  .. code-block:: c

    x ++;

.. tip:: 这是正确的

  .. code-block:: c

    x++;

**禁止多字符形式**。许多运算符以字符与 ``=`` 组合的形式表示，
如 ``+=``、``>=``、``>>=`` 等。某些编译器会接受序列开头或结尾的
``=``。然而，本标准要求 ``=`` 始终出现在最后，以避免 ``=``
出现在开头时可能出现的歧义。例如，``a =++ b;`` 也可以解释为
``a =+ +b;`` 或 ``a = ++b``，所有这些都非常不同。

``if then else`` 语句
==========================

**编码标准：**

-  ``if`` **与** ``<condition>`` **分隔**。``if`` 关键字和 ``<condition>``
   必须出现在同一行。``if`` 关键字和 ``<condition>`` 必须用单个空格分隔。
-  **缩进和括号**。``if <condition>`` 遵循标准的缩进和括号规则。
-  **对齐**。``if <condition>`` 行中的 ``if`` 和 ``else`` 必须对齐在同一列。
-  **语句始终用花括号括起来**。``if <condition>`` 和 ``else`` 关键字后的
   语句必须始终用花括号括起来。即使在（a）没有包含的语句或（b）只有
   单个语句的情况下，花括号也必须跟在 ``if <condition>`` 和 ``else`` 行之后！
-  **花括号和缩进**。花括号和语句的放置必须遵循
   `花括号和缩进 <#braces>`__ 的标准规则。
-  **最后花括号后跟单个空行**。``if``-``else`` 的*最后*右花括号后
   在大多数情况下必须跟一个空行（下面给出的例外）。这可能是
   ``if`` 复合语句的最后花括号（如果 ``else`` 关键字不存在）。
   或者可能是 ``else`` 复合语句的最后花括号（如果存在）。
   如果 ``else`` 关键字存在，关闭 ``if`` 复合语句的右花括号后
   永远不会有空行。花括号的使用必须遵循
   `花括号和间距 <#braces>`__ 的所有其他标准规则。
-  **例外**。在某些情况下，``if <condition>``-``else`` 语句嵌套在
   另一个复合语句中时，必须省略该空行；连续右花括号之间不应有空行，
   如 `花括号使用 <#braces>`__ 标准规则中所讨论的。

**其他适用的编码标准**。参见与 `花括号使用 <#braces>`__ 和
`缩进 <#indentation>`__ 相关的部分。

.. error:: 这是不正确的

  .. code-block:: c

    if(var1 < var2) var1 = var2;

    if(var > 0)
      var--;
    else
      var = 0;

    if (var1 > 0) {
      var1--;
    } else {
      var1 = 0;
    }
    var2 = var1;

.. tip:: 这是正确的

  .. code-block:: c

    if (var1 < var2)
      {
        var1 = var2;
      }

    if (var > 0)
      {
        var--;
      }
    else
      {
        var = 0;
      }

    if (var1 > 0)
      {
        var1--;
      }
    else
      {
        var1 = 0;
      }

    var2 = var1;

**三元运算符**（``<condition> ? <then> : <else>``）：

-  **仅在表达式简短时使用**。仅当整个序列简短且整齐地适合一行时，
   此形式才合适。
-  **禁止多行**。如果此形式扩展到多行，则禁止使用。
-  **使用括号**。条件和整个序列通常用括号括起来。
   然而，如果表达式在没有括号的情况下正确求值，则不需要括号。

**其他适用的编码标准**。参见与 `括号 <#parentheses>`__ 相关的部分。

.. tip:: 这是正确的

  .. code-block:: c

    int arg1 = arg2 > arg3 ? arg2 : arg3;
    int arg1 = ((arg2 > arg3) ? arg2 : arg3);

``switch`` 语句
====================

**定义：**

-  **Case 逻辑**。*Case 逻辑*指的是 ``case`` 或 ``default`` 以及
   ``case`` 或 ``default`` 后的所有代码行，直到下一个 ``case``、
   ``default`` 或指示 switch 语句结束的右花括号。

**编码标准：**

-  ``switch`` **与** ``<value>`` **分隔**。``switch`` 关键字和 switch
   ``<value>`` 必须出现在同一行。``if`` 关键字和 ``<value>`` 必须用
   单个空格分隔。
-  **贯穿**。只要包含注释，允许从一个 case 语句贯穿到下一个 case 语句。
-  ``default`` **case**。``default`` case 应始终存在，
   如果在不应该到达时到达，则触发错误。
-  **case 逻辑用花括号括起来**。首选所有 *case 逻辑*
   （除了 ``break``）用花括号括起来。如果您需要在 case 逻辑中
   实例化局部变量，则该逻辑必须用花括号括起来。
-  ``break`` **在花括号外**。``break`` 语句通常缩进两个空格。
   当与 *case 逻辑*一起有条件使用时，break 语句的放置遵循
   正常的缩进规则。
-  **case 逻辑后跟单个空行**。单个空行必须分隔 *case 逻辑*
   和任何后续的 ``case`` 或 ``default``。然而，*case 逻辑*
   和结束右花括号之间不应有空行。
-  **switch 后跟单个空行**。关闭 ``switch <value>`` 语句的最后右花括号后
   必须跟一个空行。
-  **例外**。在 ``switch <value>`` 语句嵌套在另一个复合语句中的
   某些情况下，必须省略该空行；连续右花括号之间不应有空行，
   如 `花括号使用 <#braces>`__ 标准规则中所讨论的。

**其他适用的编码标准**。参见与 `花括号使用 <#braces>`__、
`缩进 <#indentation>`__ 和 `注释 <#comments>`__ 相关的部分。

.. tip:: 这是正确的

  .. code-block:: c

    switch (...)
      {
        case 1:  /* Example of a comment following a case selector. */
        ...

        /* Example of a comment preceding a case selector. */

        case 2:
          {
            /* Example of comment following the case selector. */

            int value;
            ...
          }
          break;

        default:
          break;
      }

``while`` 语句
===================

**编码标准：**

-  ``while`` **与** ``<condition>`` **分隔**。``while`` 关键字和
   ``<condition>`` 必须出现在同一行。``while`` 关键字和 ``<condition>``
   必须用单个空格分隔。
-  **关键字在单独的行上**。``while <condition>`` 必须在单独的行上，
   行上没有其他内容。
-  **缩进和括号**。``while <condition>`` 遵循标准的缩进和括号规则。
-  **语句用花括号括起来** ``while <condition>`` 后的语句必须始终
   用花括号括起来，即使只有单个语句。
-  **空语句不加花括号**。如果 ``while <condition>`` 后没有语句，
   则不需要花括号。单个分号（空语句）就足够了；
-  **花括号和缩进**。花括号和语句的放置必须遵循花括号和缩进的标准规则。
-  **后跟单个空行**。关闭 ``while <condition>`` 语句的最后右花括号后
   必须跟一个空行。
-  **例外**。在 ``while <condition>`` 语句嵌套在另一个复合语句中的
   某些情况下，必须省略该空行；连续右花括号之间不应有空行，
   如 `花括号使用 <#braces>`__ 标准规则中所讨论的。

**其他适用的编码标准**。参见与 `花括号使用 <#braces>`__、
`缩进 <#indentation>`__ 和 `注释 <#comments>`__ 相关的部分。

.. error:: 这是不正确的

  .. code-block:: c

    while( notready() )
      {
      }
    ready = true;

    while (*ptr != '\0') ptr++;

.. tip:: 这是正确的

  .. code-block:: c

    while (notready());

    ready = true;

    while (*ptr != '\0')
      {
        ptr++;
      }

``do while`` 语句
======================

**编码标准：**

-  **关键字在单独的行上**。``do`` 和 ``while <condition>`` 必须在
   单独的行上，行上没有其他内容。
-  **缩进和括号**。``do .. while <condition>`` 遵循标准的缩进和括号规则。
-  **语句用花括号括起来** ``do`` 后的语句必须始终用花括号括起来，
   即使只有单个语句（或没有语句）。
-  **花括号和缩进**。花括号和语句的放置必须遵循花括号和缩进的标准规则。
-  ``while`` **与** ``<condition>`` **分隔**。``while`` 关键字和
   ``<condition>`` 必须出现在同一行。``while`` 关键字和 ``<condition>``
   必须用单个空格分隔。
-  **后跟单个空行**。结束的 ``while <condition>`` 后必须跟一个空行。

**其他适用的编码标准**。参见与 `花括号使用 <#braces>`__、
`缩进 <#indentation>`__ 和 `注释 <#comments>`__ 相关的部分。

.. error:: 这是不正确的

  .. code-block:: c

    do {
      ready = !notready();
    } while (!ready);
    senddata();

    do ptr++; while (*ptr != '\0');

.. tip:: 这是正确的

  .. code-block:: c

    do
      {
        ready = !notready();
      }
    while (!ready);

    senddata();

    do
      {
        ptr++;
      }
    while (*ptr != '\0');

使用 ``goto``
===============

**编码标准：**

-  **限制使用** ``goto``。禁止使用 ``goto`` 语句，但有一个例外：
   用于处理复杂嵌套逻辑中的错误条件。在这些条件下，简单的 ``goto``
   可以大大提高代码的可读性和降低复杂性。
-  **标签命名**。标签必须全部小写。允许使用下划线字符 ``_``
   来分隔长标签。
-  **错误退出标签**。错误退出标签通常称为 ``errout``。
   多个错误标签通常需要*展开*以恢复错误前逻辑中提交的资源
   或*撤销*前面的操作。这些其他标签的命名类似
   ``errout_with_allocation``、``errout_with_openfile`` 等。
-  **标签定位**。标签从不缩进。标签必须始终从第 1 列开始。

.. tip:: 这是正确的

  .. code-block:: c

       FAR struct some_struct_s *ptr;
       int fd;
       int ret;
       ...

       if (arg == NULL)
         {
           ret = -EINVAL;
           goto errout;
         }
       ...
       ptr = malloc(sizeof(struct some_struct_s));
       if (!ptr)
         {
           ret = -ENOMEM;
           goto errout;
         }
       ...
       fd = open(filename, O_RDONLY);
       if (fd < 0)
         {
           errcode = -errno;
           DEBUGASSERT(errcode > 0);
           goto errotout_with_alloc;
         }
       ...
       ret = readfile(fd);
       if (ret < 0)
         {
           goto errout_with_openfile;
         }
       ...
    errout_with_openfile:
      close(fd);

    errout_with_alloc:
      free(ptr);

    error:
      return ret;

**注意**：参见 `指针 <#farnear>`__ 的讨论，了解上面使用的 ``FAR`` 限定符。

***
C++
***

目前没有提供完整的 NuttX C++ 文件编码标准的文档。
本节在此处提供 C++ 代码开发的一些最低限度的指导。
在大多数细节如缩进、间距和文件组织方面，它与 C 编码标准相同。
但在可接受的标准方面存在显著差异。主要差异如下：

C++ 风格注释不仅允许而且是必需的（以下例外除外）。
这包括本标准 `附录 <#appndxa>`__ 中描述的 *源文件结构* 中的块注释。

Doxygen 标签是可接受的。需要提供 DOxygen 标签时也接受 C 风格注释。

目前没有要求符合任何特定的 C++ 版本。然而，出于可移植性原因，
在合理的情况下鼓励符合较旧的、C++11 之前的标准。

C++ 文件扩展名：扩展名 ``.cxx`` 用于 C++ 源文件；扩展名 ``.hxx``
用于 C++ 头文件。

所有命名必须使用 *CamelCase*。不鼓励使用下划线字符 '_'。
这包括变量、类、结构等：所有用户可命名的 C++ 元素。
预处理器定义仍然要求全部大写。

局部变量、方法名和函数名必须全部以小写字母开头。
例如，``myLocalVariable`` 将是局部变量的合规名称；
``myMethod`` 将是方法的合规名称；

命名空间、全局变量、类、结构、模板和枚举名称以大写字母开头，
标识正在命名的内容：

 *命名空间名称*
   命名空间以大写字符开头，但不指定特定字符。
   例如，``MyNamespace`` 完全合规。
 *全局变量名称*
   全局变量和单例以大写 '**G**' 开头。例如，``GMyGlobalVariable``。
   从不使用前缀 ``g_``。
 *实现类名称*
   实现方法的类以大写 '**C**' 开头。例如，``CMyClass``。
   ``CMyClass`` 的完全限定方法可以是 ``MyNamespace::CMyClass::myMethod``
 *纯虚基类名称*
   此类基类以大写 '**I**' 开头。例如，``IMyInterface``。
 *模板类名称*
   模板类以大写 '**T**' 开头。例如，``TMyTemplate``。
 *``typedef`` 定义的类型名称*
   目前所有此类类型也以大写 '**T**' 开头。
   这可能需要一些解决以区分模板名称。从不使用后缀 ``_t``。
 *结构名称*
   结构以大写 '**S**' 开头。例如，``SMyStructure``。
   从不使用后缀 ``_s``。
 *枚举名称*
   枚举以大写 '**E**' 开头。例如，``EMyEnumeration``。
   从不使用后缀 ``_e``。

.. _precommit:

******************
使用 Pre-Commit
******************
您可以使用 `pre-commit <https://pre-commit.com/>`_ 工具自动检查
样式问题。这是一个基于 Python 的第三方工具，简化了 linter 检查，
并在您提交修改时自动运行。

该工具使用 NuttX 根目录中的 `.pre-commit-config.yaml` 文件作为参考。

安装
=============
按照 `pre-commit <https://pre-commit.com/>`_ 网站上的安装指南操作。
如果您无法直接使用 pip 安装，请考虑使用
`snap <https://snapcraft.io/install/pre-commit/ubuntu>`_ 或 `apt`。
然后，进入 NuttX 仓库并运行：``pre-commit install``。

使用
========
提交更改时，工具应自动运行。
每个检查应显示"Passed"，否则提交不会发生。
如果任何测试失败，您应该：修复错误，然后再次 ``git add`` 和 ``git commit``。

示例终端输出：

.. code-block:: console

 user@machine:~/nuttxspace/nuttx$ git commit -m "Testing pre-commit"
 fix end of files.........................................................Passed
 trim trailing whitespace.................................................Passed
 check for added large files..............................................Passed
 nxstyle..................................................................Passed
 [feature/example_wifi 8394e9f3cf] Testing pre-commit
 1 file changed, 1 insertion(+)

可以手动运行工具而不提交，只检查目录中的所有文件。
只需运行：``pre-commit run --files drivers/i2c/*``

钩子
========
以下钩子在 `.pre-commit-config.yaml` 中启用：

-  **end-of-file-fixer：** 在文件末尾添加空行。
-  **trailing-whitespace：** 查找并删除行尾的空白。
-  **check-added-large-files：** 验证是否向提交中添加了大文件。
-  **cmake-format：** 检查 CMakeLists 文件的样式。
-  **nxstyle：** 检查 NuttX 样式 (nxstyle)。当前运行整个 ``checkpatch.sh`` 脚本。

.. _appndxa:

********
附录
********

.. _cfilestructure:

C 源文件结构
=======================

.. code-block:: c

   /****************************************************************************
    * <Relative path to the file>
    * <Optional one line file description>
    *
    * Licensed to the Apache Software Foundation (ASF) under one or more
    * contributor license agreements.  See the NOTICE file distributed with
    * this work for additional information regarding copyright ownership.  The
    * ASF licenses this file to you under the Apache License, Version 2.0 (the
    * "License"); you may not use this file except in compliance with the
    * License.  You may obtain a copy of the License at
    *
    *   http://www.apache.org/licenses/LICENSE-2.0
    *
    * Unless required by applicable law or agreed to in writing, software
    * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
    * License for the specific language governing permissions and limitations
    * under the License.
    *
    ****************************************************************************/

   /****************************************************************************
    * Included Files
    ****************************************************************************/

*所有头文件都在此处包含。*

.. code-block:: c

   /****************************************************************************
    * Pre-processor Definitions
    ****************************************************************************/

*所有 C 预处理器宏都在此处定义。*

.. code-block:: c

   /****************************************************************************
    * Private Types
    ****************************************************************************/

*文件使用的任何类型、枚举、结构或联合都在此处定义。*

.. code-block:: c

   /****************************************************************************
    * Private Function Prototypes
    ****************************************************************************/

*文件中所有静态函数的原型在此处提供。*

.. code-block:: c

   /****************************************************************************
    * Private Data
    ****************************************************************************/

*所有静态数据定义出现在此处。*

.. code-block:: c

   /****************************************************************************
    * Public Data
    ****************************************************************************/

*所有具有全局作用域的数据定义出现在此处。*

.. code-block:: c

   /****************************************************************************
    * Private Functions
    ****************************************************************************/

   /****************************************************************************
    * Name: <Static function name>
    *
    * Description:
    *   Description of the operation of the static function.
    *
    * Input Parameters:
    *   A list of input parameters, one-per-line, appears here along with a
    *   description of each input parameter.
    *
    * Returned Value:
    *   Description of the value returned by this function (if any),
    *   including an enumeration of all possible error values.
    *
    * Assumptions/Limitations:
    *   Anything else that one might need to know to use this function.
    *
    ****************************************************************************/

*文件中的所有静态函数在此分组中定义。每个函数前面都有类似上面的函数头。*

.. code-block:: c

   /****************************************************************************
    * Public Functions
    ****************************************************************************/

   /****************************************************************************
    * Name: <Global function name>
    *
    * Description:
    *   Description of the operation of the function.
    *
    * Input Parameters:
    *   A list of input parameters, one-per-line, appears here along with a
    *   description of each input parameter.
    *
    * Returned Value:
    *   Description of the value returned by this function (if any),
    *   including an enumeration of all possible error values.
    *
    * Assumptions/Limitations:
    *   Anything else that one might need to know to use this function.
    *
    ****************************************************************************/

*文件中的所有全局函数在此处定义。*

C 头文件结构
=======================

.. code-block:: c

  /****************************************************************************
  * <Relative path to the file>
  * <Optional one line file description>
  *
  * Licensed to the Apache Software Foundation (ASF) under one or more
  * contributor license agreements.  See the NOTICE file distributed with
  * this work for additional information regarding copyright ownership.  The
  * ASF licenses this file to you under the Apache License, Version 2.0 (the
  * "License"); you may not use this file except in compliance with the
  * License.  You may obtain a copy of the License at
  *
  *   http://www.apache.org/licenses/LICENSE-2.0
  *
  * Unless required by applicable law or agreed to in writing, software
  * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
  * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
  * License for the specific language governing permissions and limitations
  * under the License.
  *
  ****************************************************************************/

*头文件* `幂等 <#idempotence>`__ *定义在此处*

.. code-block:: c

  /****************************************************************************
  * Included Files
  ****************************************************************************/

*所有头文件都在此处包含。*

.. code-block:: c

  /****************************************************************************
  * Pre-processor Definitions
  ****************************************************************************/

*所有 C 预处理器宏都在此处定义。*

.. code-block:: c

  /****************************************************************************
  * Public Types
  ****************************************************************************/

  #ifndef __ASSEMBLY__

*任何类型、枚举、结构或联合都在此处定义。*

.. code-block:: c

  /****************************************************************************
  * Public Data
  ****************************************************************************/

  #ifdef __cplusplus
  #define EXTERN extern "C"
  extern "C"
  {
  #else
  #define EXTERN extern
  #endif

*所有具有全局作用域的数据声明出现在此处，前面有定义* ``EXTERN``。

.. code-block:: c

 /****************************************************************************
  * Inline Functions
  ****************************************************************************/

 /****************************************************************************
  * Name: <Inline function name>
  *
  * Description:
  *   Description of the operation of the inline function.
  *
  * Input Parameters:
  *   A list of input parameters, one-per-line, appears here along with a
  *   description of each input parameter.
  *
  * Returned Value:
  *   Description of the value returned by this function (if any),
  *   including an enumeration of all possible error values.
  *
  * Assumptions/Limitations:
  *   Anything else that one might need to know to use this function.
  *
  ****************************************************************************/

*任何静态内联函数可以在此分组中定义。每个函数前面都有类似上面的函数头。*

.. code-block:: c

  /****************************************************************************
  * Public Function Prototypes
  ****************************************************************************/

  /****************************************************************************
  * Name: <Global function name>
  *
  * Description:
  *   Description of the operation of the function.
  *
  * Input Parameters:
  *   A list of input parameters, one-per-line, appears here along with a
  *   description of each input parameter.
  *
  * Returned Value:
  *   Description of the value returned by this function (if any),
  *   including an enumeration of all possible error values.
  *
  * Assumptions/Limitations:
  *   Anything else that one might need to know to use this function.
  *
  ****************************************************************************/

*文件中的所有全局函数原型在此处提供。关键字* ``extern`` *或定义*
``EXTERN`` *从不用于函数原型。*

.. code-block:: c

   #undef EXTERN
   #ifdef __cplusplus
   }
   #endif

   #endif /* __INCLUDE_ASSERT_H */

以头文件 `幂等 <#idempotence>`__ ``#endif`` 结束。
