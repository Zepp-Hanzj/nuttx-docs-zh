===========================
``inifile`` INI 文件解析器
===========================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

语法
------

此目录包含一个非常简单的 INI 文件解析器。INI 文件由一系列行组成，直到文件结束。一行可以是以下之一：

1. 空行。

2. 注释行。任何以 ``;`` 开头的行

3. 节标题。定义被分为多个节。每个节以包含方括号括起的节名的行开始。例如，``[section1]``。左方括号必须是行的第一个字符。节名不区分大小写，即 ``SECTION1`` 和 ``Section1`` 指的是同一个节。

4. 变量赋值。变量赋值是变量名后跟 ``=`` 符号，然后是变量的值。例如，``A=B``：``A`` 是变量名；``B`` 是变量值。节标题后的所有变量都属于该节。

   变量名前可以有空白字符。``=`` 符号前不允许有空白字符。变量名不区分大小写，即 ``A`` 和 ``a`` 指的是同一个变量名。

   变量值可以是数字（任何进制）或字符串。字符串参数的大小写会被保留。

编程接口
----------------------

有关 INI 文件解析器支持的接口，请参阅 ``apps/include/fsutils/inifile.h``。

测试程序
----------------

以下是一个简单的测试程序：

.. code-block:: C

  int main(int argc, char *argv[])
    {
      INIHANDLE handle;
      FILE *stream;
      FAR char *ptr;
      long value;

      stream = fopen("/tmp/file.ini", "w");
      fprintf(stream, "; Test INI file\n");
      fprintf(stream, "[section1]\n");
      fprintf(stream, "  VAR1=1\n");
      fprintf(stream, "  VAR2=2\n");
      fprintf(stream, "  VAR3=3\n");
      fprintf(stream, "\n");
      fprintf(stream, "[section2]\n");
      fprintf(stream, "  VAR4=4\n");
      fprintf(stream, "  VAR5=5\n");
      fprintf(stream,   "VAR6=6\n");
      fprintf(stream, "\n");
      fclose(stream);

      handle = inifile_initialize("/tmp/file.ini");

      ptr = inifile_read_string(handle, "section2", "VAR5", "OOPS");
      printf("Section: %s Variable: %s String: %s\n", "section2", "VAR5", ptr);
      inifile_free_string(ptr);

      ptr = inifile_read_string(handle, "section1", "VAR2", "OOPS");
      printf("Section: %s Variable: %s String: %s\n", "section1", "VAR2", ptr);
      inifile_free_string(ptr);

      ptr = inifile_read_string(handle, "section3", "VAR3", "OOPS");
      printf("Section: %s Variable: %s String: %s\n", "section3", "VAR3", ptr);
      inifile_free_string(ptr);

      ptr = inifile_read_string(handle, "section1", "VAR3", "OOPS");
      printf("Section: %s Variable: %s String: %s\n", "section1", "VAR3", ptr);
      inifile_free_string(ptr);

      ptr = inifile_read_string(handle, "section1", "VAR1", "OOPS");
      printf("Section: %s Variable: %s String: %s\n", "section1", "VAR1", ptr);
      inifile_free_string(ptr);

      ptr = inifile_read_string(handle, "section1", "VAR42", "OOPS");
      printf("Section: %s Variable: %s String: %s\n", "section1", "VAR42", ptr);
      inifile_free_string(ptr);

      ptr = inifile_read_string(handle, "section2", "VAR6", "OOPS");
      printf("Section: %s Variable: %s String: %s\n", "section2", "VAR6", ptr);
      inifile_free_string(ptr);

      ptr = inifile_read_string(handle, "section2", "VAR4", "OOPS");
      printf("Section: %s Variable: %s String: %s\n", "section2", "VAR4", ptr);
      inifile_free_string(ptr);

      value = inifile_read_integer(handle, "section1", "VAR3", 0);
      printf("Section: %s Variable: %s Value: %ld\n", "section1", "VAR3", value);

      value = inifile_read_integer(handle, "section3", "VAR3", 0);
      printf("Section: %s Variable: %s String: %ld\n", "section3", "VAR3", value);

      value = inifile_read_integer(handle, "section1", "VAR1", 0);
      printf("Section: %s Variable: %s Value: %ld\n", "section1", "VAR1", value);

      value = inifile_read_integer(handle, "section2", "VAR5", 0);
      printf("Section: %s Variable: %s Value: %ld\n", "section2", "VAR5", value);

      value = inifile_read_integer(handle, "section2", "VAR6", 0);
      printf("Section: %s Variable: %s Value: %ld\n", "section2", "VAR6", value);

      value = inifile_read_integer(handle, "section1", "VAR42", 0);
      printf("Section: %s Variable: %s String: %ld\n", "section1", "VAR42", value);

      value = inifile_read_integer(handle, "section1", "VAR2", 0);
      printf("Section: %s Variable: %s Value: %ld\n", "section1", "VAR2", value);

      value = inifile_read_integer(handle, "section2", "VAR4", 0);
      printf("Section: %s Variable: %s Value: %ld\n", "section2", "VAR4", value);

      inifile_uninitialize(handle);
      return 0;
    }

测试程序输出::

  Section: section2 Variable: VAR5 String: 5
  Section: section1 Variable: VAR2 String: 2
  Section: section3 Variable: VAR3 String: OOPS
  Section: section1 Variable: VAR3 String: 3
  Section: section1 Variable: VAR1 String: 1
  Section: section1 Variable: VAR42 String: OOPS
  Section: section2 Variable: VAR6 String: 6
  Section: section2 Variable: VAR4 String: 4

  Section: section1 Variable: VAR3 Value: 3
  Section: section3 Variable: VAR3 Value: 0
  Section: section1 Variable: VAR1 Value: 1
  Section: section2 Variable: VAR5 Value: 5
  Section: section2 Variable: VAR6 Value: 6
  Section: section1 Variable: VAR42 String: 0
  Section: section1 Variable: VAR2 Value: 2
  Section: section2 Variable: VAR4 Value: 4
