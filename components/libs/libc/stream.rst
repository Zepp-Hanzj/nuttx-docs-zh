lib_bsprintf
============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

This 函数 is mainly used to 输出 the contents of the 输入
结构. 支持s standard formats for printf and scanf. For detailed
参数s, see: 1. https://en.cppreference.com/w/c/io/fprintf 2.
https://en.cppreference.com/w/c/io/fscanf

-  **special**:

   1. Float use %hf, “%f” or “%lf” is double, “%Lf” is long double.
   2. The char array 指定 with %.xs. 例如: “char t[30]”
      指定 with “%.30s”, char a [20] - " %.20s "
   3. “%u” is unsigned int.
   4. “%d” is int.
   5. When using %f to format a double 数据 类型, the double is
      t运行cated to 6 decimal places by 默认.
   6. It is recommended that the “char[]” array be placed at the end of
      the 结构 to prevent 参数 配置 错误s such as
      “%.20s” from causing problems in parsing the entire 缓冲区.

-  **demo**

   1. **struct**:

   ::

      begin_packed_struct
      struct test
      {
        uint8_t a;
        uint16_t b;
        uint32_t c;
        int8_t d;
        int16_t e;
        int32_t f;
        float g;
        double h;
        char i[32];
        uint64_t j;
        int64_t k;
        char l;
        unsigned char m;
        short int n;
        unsigned short int o;
        int p;
        unsigned int q;
        long r;
        unsigned long s;
        long long t;
        unsigned long long u;
        大小_t v;
        long double w;
      }end_packed_struct;

   1. **format string**:

   ::

      const char* sg = "           uint8_t:[%hhu]\n" \
                       "          uint16_t:[%hu]\n" \
                       "          uint32_t:[%u]\n" \
                       "            int8_t:[%hhd]\n" \
                       "           int16_t:[%hd]\n" \
                       "           int32_t:[%d]\n" \
                       "             float:[%hf]\n" \
                       "            double:[%f]\n" \
                       "            char[]:[%.32s]\n" \
                       "          uint64_t:[%lu]\n" \
                       "           int64_t:[%ld]\n" \
                       "              char:[%hhd]\n" \
                       "     unsigned char:[%hhu]\n" \
                       "         short int:[%hd]\n" \
                       "unsigned short int:[%hu]\n" \
                       "               int:[%d]\n" \
                       "      unsigned int:[%u]\n" \
                       "              long:[%ld]\n" \
                       "     unsigned long:[%lu]\n" \
                       "         long long:[%lld]\n" \
                       "unsigned long long:[%llu]\n" \
                       "            大小_t:[%uz]\n" \
                       "       long double:[%Lf]\n";

   1. **use**:

   -  输出 to terminal:

   ::

      #ifdef CONFIG_FILE_STREAM
       struct lib_stdoutstream_s stdoutstream;

       lib_stdoutstream(&stdoutstream, stdout);

       flock文件(stdout);
       lib_bsprintf(&stdoutstream.common, sv, &test_v);
       lib_bsprintf(&stdoutstream.common, sg, &test_g);
       funlock文件(stdout);
      #else
       struct lib_rawoutstream_s rawoutstream;
       struct lib_缓冲区edoutstream_s outstream;

       lib_rawoutstream(&rawoutstream, STDOUT_FILENO);
       lib_缓冲区edoutstream(&outstream, &rawoutstream.common);

       lib_bsprintf(&outstream.common, sv, &test_v);
       lib_bsprintf(&outstream.common, sg, &test_g);

       lib_stream_flush(&outstream.common);
      #endif

lib_bscanf
==========

This 函数 添加s a formatted standard scanf string to the
结构(lib_bscanf). 1. https://zh.cppreference.com/w/c/io/fscanf

-  **special**:

   1. Please use %lf for double precision, “%hf” or “%f” for float, long
      double (“%Lf”) is not 支持ed.
   2. Please use %hhd or %hhu for a single char or unsigned char.
   3. Use %hd or %hu for short int or unsigned short int.
   4. When using %s or %c, please specify the length of the char array,
      such as %32s, %32c.
   5. %s will check the string for spaces. When there are spaces in the
      string, it will be t运行cated. If you want to use string with
      spaces, please use %{length}c, but make sure that the length of
      the string can fill the array, otherwise an 错误 will occur.
   6. %[] collection and %n are not 支持ed.

-  **demo**

   1. **struct**: Same as above
   2. **format string**:

   ::

      #define TOSTR(str)   #str
      #define TONNAME(名称) TOSTR(名称)

      #define v_uint8_t    97
      #define v_uint16_t   19299
      #define v_uint32_t   22155

      ......

      #define v_l_double   -9299.9299929912122464755474

      char bflag[] = "%hhu%hu%u%hhd%hd%d%f%lf%32s%llu%lld%hhd%hhu%hd%hu%d%u%ld%lu%lld%llu%zu%ld";

      char b输入[] = TONNAME(v_uint8_t) \
                     " " TONNAME(v_uint16_t) \
                     " " TONNAME(v_uint32_t) \
                     " " TONNAME(v_int8_t) \
                     " " TONNAME(v_int16_t) \
                     " " TONNAME(v_int32_t) \
                     " " TONNAME(v_float) \
                     " " TONNAME(v_double) \
                     " " TONNAME(v_char_arr) \
                     " " TONNAME(v_uint64_t) \
                     " " TONNAME(v_int64_t) \
                     " " TONNAME(v_char) \
                     " " TONNAME(v_u_char) \
                     " " TONNAME(v_s_int) \
                     " " TONNAME(v_u_s_int) \
                     " " TONNAME(v_int) \
                     " " TONNAME(v_u_int) \
                     " " TONNAME(v_long) \
                     " " TONNAME(v_u_long) \
                     " " TONNAME(v_l_l) \
                     " " TONNAME(v_u_l_l) \
                     " " TONNAME(v_大小_t) \
                     " " TONNAME(v_l_double);

   3. **use**:

   ::

      struct test vg;
      ret = lib_bscanf(b输入, bflag, &vg);
