==================
``uncrustify.cfg``
==================

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

这是用于 uncrustify 代码美化工具的配置脚本。
Uncrustify 能很好地在 "if" 语句中强制使用花括号，并按照 NuttX C 编码标准
进行缩进。它能正确处理诸如将所有花括号放在独立行上并保持适当缩进级别等操作。
但它无法处理编码标准中的某些要求，例如：

- 指针声明中的 FAR 属性。
- NuttX 标准函数头块注释。
- 命名违规，如使用 CamelCase 变量名、小写预处理器定义等。

注释块、函数头、文件头等必须手动格式化。

它对块注释的处理比较脆弱。如果注释是完美的，它会保持原样，但如果块注释
被认为需要修复，它会错误地缩进注释的续行。

- uncrustify.cfg 搞乱了大多数块注释的缩进。
  cmt_sp_before_star_cont 的应用不一致。我添加了::

        cmt_indent_multi = false # 禁用所有多行注释更改

  到 .cfg 文件中，以限制其对块注释的损害。
- 它在第 78 列处非常严格地换行。即使第 79 列仅包含结束 ``*/`` 的 ``/`` 也是如此。
  这导致了许多不良的续行。

- 它将打开结构体的 '{' 移到了定义结构体的那一行。
  nl_struct_brace = add（或 force）似乎被忽略了。

- 它还以看似任意的方式对齐声明中的变量名和赋值语句中的 '=' 符号。
  做出了不必要的更改。

.. note::

    uncrustify.cfg 应**仅**用于具有不一致编码风格的新文件。
    uncrustify.cfg 应该能让你接近目标，但你应该预期需要审阅和手动编辑
    文件以确保 100% 的合规性。

.. warning::

   **切勿** 将 uncrustify.cfg 用于对现有 NuttX 文件的修改。它可能会以
   隐蔽的方式破坏代码风格！

此工具最后由 Bob Feretich 用 uncrustify 0.66.1 进行了验证。

关于 uncrustify：Uncrustify 是一个高度可配置、易于修改的源代码美化工具。
要了解更多关于 uncrustify 的信息：

    http://uncrustify.sourceforge.net/

源代码可在 GitHub 上获取：

    https://github.com/uncrustify/uncrustify

可通过命令行安装器获取适用于 Linux 的二进制包。
适用于 Windows 和 Linux 的二进制文件可在以下位置获取：

    https://sourceforge.net/projects/uncrustify/files/

另请参阅 :doc:`/components/tools/indent` 和 :doc:`/components/tools/nxstyle`。
