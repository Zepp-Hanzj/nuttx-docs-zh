lib_bsprintf
============

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

此函数主要用于输出输入结构体的内容。支持 printf 和 scanf 的标准格式。
详细参数说明请参阅：1. https://en.cppreference.com/w/c/io/fprintf 2.
https://en.cppreference.com/w/c/io/fscanf

-  **特殊说明**：

   1. 浮点数使用 %hf，"%f" 或 "%lf" 表示 double，"%Lf" 表示 long double。
   2. 字符数组使用 %.xs 指定长度。例如："char t[30]"
      使用 "%.30s"，char a[20] 使用 "%.20s"
   3. "%u" 表示 unsigned int。
   4. "%d" 表示 int。
   5. 使用 %f 格式化 double 数据类型时，默认截断为 6 位小数。
   6. 建议将 "char[]" 数组放在结构体末尾，以防止 "%.20s" 等参数
      配置错误导致整个缓冲区解析出现问题。

-  **示例**

   1. **结构体**:

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
        size_t v;
        long double w;
      }end_packed_struct;

   1. **格式字符串**:

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
                       "            size_t:[%uz]\n" \
                       "       long double:[%Lf]\n";

   1. **用法**:

   -  输出到终端:

   ::

      #ifdef CONFIG_FILE_STREAM
       struct lib_stdoutstream_s stdoutstream;

       lib_stdoutstream(&stdoutstream, stdout);

       flockfile(stdout);
       lib_bsprintf(&stdoutstream.common, sv, &test_v);
       lib_bsprintf(&stdoutstream.common, sg, &test_g);
       funlockfile(stdout);
      #else
       struct lib_rawoutstream_s rawoutstream;
       struct lib_bufferedoutstream_s outstream;

       lib_rawoutstream(&rawoutstream, STDOUT_FILENO);
       lib_bufferedoutstream(&outstream, &rawoutstream.common);

       lib_bsprintf(&outstream.common, sv, &test_v);
       lib_bsprintf(&outstream.common, sg, &test_g);

       lib_stream_flush(&outstream.common);
      #endif

lib_bscanf
==========

此函数将格式化的标准 scanf 字符串添加到结构体（lib_bscanf）中。
1. https://zh.cppreference.com/w/c/io/fscanf

-  **特殊说明**：

   1. 请使用 %lf 表示双精度浮点数，"%hf" 或 "%f" 表示单精度浮点数，
      不支持 long double（"%Lf"）。
   2. 请使用 %hhd 或 %hhu 表示单个 char 或 unsigned char。
   3. 使用 %hd 或 %hu 表示 short int 或 unsigned short int。
   4. 使用 %s 或 %c 时，请指定字符数组的长度，例如 %32s、%32c。
   5. %s 会检查字符串中的空格。当字符串中存在空格时，会被截断。
      如果需要使用包含空格的字符串，请使用 %{length}c，但请确保
      字符串长度能够填满数组，否则将出错。
   6. 不支持 %[] 集合和 %n。

-  **示例**

   1. **结构体**：同上
   2. **格式字符串**:

   ::

      #define TOSTR(str)   #str
      #define TONNAME(name) TOSTR(name)

      #define v_uint8_t    97
      #define v_uint16_t   19299
      #define v_uint32_t   22155

      ......

      #define v_l_double   -9299.9299929912122464755474

      char bflag[] = "%hhu%hu%u%hhd%hd%d%f%lf%32s%llu%lld%hhd%hhu%hd%hu%d%u%ld%lu%lld%llu%zu%ld";

      char binput[] = TONNAME(v_uint8_t) \
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
                     " " TONNAME(v_size_t) \
                     " " TONNAME(v_l_double);

   3. **用法**:

   ::

      struct test vg;
      ret = lib_bscanf(binput, bflag, &vg);
