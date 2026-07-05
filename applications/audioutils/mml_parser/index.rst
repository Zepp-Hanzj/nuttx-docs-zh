========================================================
``mml_parser`` Music Macro Language (MML) Parser library
========================================================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

MML 经常被用作在字符串中描述音乐的语言，例如在 BASIC 语言中。mml_parser 是一个
用纯 C 编写的极简音乐宏语言解析器库，专为资源受限的平台设计，特别是微控制器和
其他嵌入式系统。

此库支持的语法
--------------------------------

音符
~~~~~

* **C** (Do)
* **D** (Re)
* **E** (Mi)
* **F** (Fa)
* **G** (Sol)
* **A** (La)
* **B** (Ti)

升号和降号
~~~~~~~~~~~~~~

在音符后添加 "#" 或 "+" 表示升号。例如：``"C#"`` ``"C+."``
在音符后添加 "-" 表示降号。例如：``"C-"``

时值
~~~~~~

音调的时值可以通过两种方式指定。一种是为每个音符指定时值。在音符后添加数字，
可以是 1、2、4、8、16、32 或 64。
例如：``"C8 C16 C#4."``

另一种是使用 ``L``。``L`` 设置默认时值。如果音符没有时值，则使用 "L" 指示的数字。
"L" 后面的数字可以是 1、2、4、8、16、32 或 64。
例如：``"L4 A"`` 表示时值为 4 的 "A"。

此外，支持附点。例如，"C4." 的时值为 4 + 8。"C16.." 的时值为 4 + 8 + 16。

休止符
~~~~

休止符用 "R" 表示。休止符的时值在 "R" 之后，与音符时值相同。如果未指定时值，
则使用 "L" 指定的时值。

和弦
~~~~~

支持和弦。如果一些音符被 ``[`` 和 ``]`` 括起来，则它们被解释为和弦。
例如：``"[CEG]"`` 是 Do、Mi 和 Sol 的和弦。和弦的时值可以放在 ``]`` 之后。
例如：``"[CEG]4"`` 是时值为 4 的和弦。

注意：和弦中的最大音符数在 ``mml_parser.h`` 中定义为 MAX_CHORD_NOTES。

连音
~~~~~~

支持连音。如果一些音符和和弦被 ``{`` 和 ``}`` 括起来，则它们被解释为连音。
例如：``"{C E G [CEG]}"`` 是包含 C、E、G 和 CEG 和弦的连音。
连音的时值可以放在 "}" 之后，时值在每个音符之间平均分配。
例如：在 ``"{C E G [CEG]}4"`` 的情况下，C、E、G 和 CEG 和弦各占 L4 时值的四分之一。

八度
~~~~~~

八度由 "O"、">" 或 "<" 控制。使用 "O" 时，后面跟一个表示八度的数字。
使用 ">" 时，新八度的值为当前八度加一。使用 "<" 时，新八度的值为当前八度减一。
例如：``"CDEFGAB > C R C < BAGFEDC"``，``"O4 CDEFGAB O5 C R C O4 BAGFEDC"``

速度
~~~~~

速度用 "T" 表示，后面跟数字。速度数字决定乐谱的速度。此值用于计算音符（或休止符）
的采样数。
例如：``"T120"``

音量
~~~~~~

音量可以用 "V" 控制。后面跟数字。
例如：``"V4"``

乐谱示例
------------------

Do Re Mi 歌曲的开头
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

速度 120，音量 10，八度 4，默认时值为 4。

``"T120 V10 O4 L4 C. D8 E. C8 E C E2 D. E8 {FF} {ED} F2"``

提供的 C 函数
--------------------

mml_parser 仅提供 2 个函数。

init_mml()
~~~~~~~~~~

初始化 mml 解析器的实例。

.. code-block:: c

   #include <audioutils/mml_parser.h>

   int init_mml(FAR struct music_macro_lang_s *mml,
                int fs, int tempo, int octave, int length);

此函数初始化作为第 1 个参数提供的 ``struct music_macro_lang_s`` 实例。
参数 ``fs`` 是目标音频输出系统的采样频率，此值用于计算在给定速度和音符时值情况下的
采样数。``tempo``、``octave`` 和 ``length`` 分别指定速度、八度和时值的初始值。

成功时，init_mml() 返回 0。出错时，返回负值。

目前不会发生错误。

parse_mml()
~~~~~~~~~~~

从给定字符串解析 MML。

.. code-block:: c

   #include <audioutils/mml_parser.h>

   int parse_mml(FAR struct music_macro_lang_s *mml,
                FAR char **score, FAR struct mml_result_s *result);

parse_mml() 解析 ``score`` 参数给出的字符串中的第一个 MML，并在返回值和
``result`` 参数中给出结果。``result`` 是 mml_result_s 的实例，包含 note_idx、
length 和 chord_notes 作为成员。每个成员值的含义取决于返回值。

出错时，返回负值。成功时，可返回以下值。这些值在 ``mml_parser.h`` 中定义。

===================== ===========================================
返回值                  描述
===================== ===========================================

MML_TYPE_EOF          表示已到达字符串末尾。``result`` 的内容无意义。
MML_TYPE_NOTE         表示已解析某个音符。音符的音阶存储在 ``note_idx[0]`` 中。音符的时值由 ``length`` 成员以采样数形式给出。在连音的情况下，每次解析音符时都返回此返回值。换句话说，连音被解析为单个音符。
MML_TYPE_REST         表示已解析 ``rest``。其时值由 ``length`` 成员以采样数形式给出。
MML_TYPE_TEMPO        表示已解析 ``"T"``。``result`` 中的 ``length`` 成员包含速度值。但速度值保存在 mml 实例中用于计算每个音符的采样数。因此，基本上不需要在代码中处理此返回值。
MML_TYPE_LENGTH       表示已解析 ``"L"``。``result`` 中的 ``length`` 成员包含解析的时值。但当前时值保存在 mml 实例中。因此，基本上不需要在代码中处理此返回值。
MML_TYPE_OCTAVE       表示已解析 ``"O"``、``">"`` 或 ``"<"``。``result`` 中的 ``length`` 成员包含八度值。但八度编码在 ``MML_TYPE_NOTE`` 情况下的 ``note_idx`` 中。因此，基本上不需要在代码中处理此返回值。
MML_TYPE_TUPLETSTART  表示连音刚刚开始。连音的总时值存储在 ``result`` 成员的 ``length`` 中。
MML_TYPE_TUPLETDONE   表示连音刚刚结束。
MML_TYPE_VOLUME       表示已解析 ``"V"``。``result`` 中的 ``length`` 成员包含解析的音量值。
MML_TYPE_TONE         待定。
MML_TYPE_CHORD        表示已解析和弦。和弦包含多个音符，音符数量存储在 ``result`` 的 ``chord_notes`` 成员中。每个音符存储在 ``note_idx[]`` 中。和弦的时值存储在 ``result`` 的 ``length`` 成员中。
===================== ===========================================

``note_idx[]`` 的值编码八度，如下所示

====== ==== ==============
八度 音符 node_idx 值
====== ==== ==============
O0     C    0
O0     C#   1
O0     D    2
O0     D#   3
O0     E    4
O0     F    5
O0     F#   6
O0     G    7
O0     G#   8
O0     A    9
O0     A#   10
O0     B    11
O1     C    12
====== ==== ==============

依此类推。

例如，八度 4 的 G# 编码为 56。

以下错误代码可作为返回值接收。

================================= =================
错误代码                          描述
================================= =================
MML_TYPE_NOTE_ERROR
MML_TYPE_REST_ERROR
MML_TYPE_TEMPO_ERROR
MML_TYPE_LENGTH_ERROR
MML_TYPE_OCTAVE_ERROR
MML_TYPE_VOLUME_ERROR
MML_TYPE_TUPLET_ERROR
MML_TYPE_TONE_ERROR
MML_TYPE_CHORD_ERROR
MML_TYPE_ILLIGAL_COMPOSITION
MML_TYPE_ILLIGAL_TOOMANY_NOTES
MML_TYPE_ILLIGAL_TOOFEW_NOTES
MML_TYPE_ILLIGAL_DOUBLE_TUPLET
================================= =================

运行单元测试
------------------

请参见 examples/mml_parser

Bug
----

有很多。在 GitHub 上报告，或者更好的是——提交拉取请求。
请为您添加的任何新函数编写单元测试——这很有趣！

作者
------

mml_parser 由 Takayoshi Koizumi &lt;takayoshi.koizumi@gmail.com&gt; 编写
