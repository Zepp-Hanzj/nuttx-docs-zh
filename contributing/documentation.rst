=============
文档
=============

Apache NuttX 文档使用
`Sphinx 文档系统 <https://www.sphinx-doc.org/en/master/>`_ 构建。文档
使用 `ReStructured Text <https://docutils.sourceforge.io/rst.html>`_ (RST) 编写，
并包含 Sphinx 特定的指令。RST 是
`Python 文档 <https://docs.python.org/3/>`_ 使用的格式，也被许多其他项目使用。
使用 Sphinx，RST 文件被渲染为可在浏览器中阅读的 HTML 文件。

构建
========

要在本地渲染文档，您应该克隆 NuttX 主仓库并进入其中。然后，

  1. 使用 pipenv 安装 Sphinx 和其他依赖项。
     在 Windows 和 MacOS 等平台上，使用 *pyenv* 管理 Python 安装
     也可能有所帮助。您可以在项目
     `网站 <https://github.com/pyenv/pyenv#installation>`_ 上阅读有关安装的信息。

    .. code-block:: console

      $ pip3 install pipenv
      $ cd Documentation/
      $ # 将依赖项安装到虚拟环境中
      $ pipenv install
      $ # 激活虚拟环境
      $ pipenv shell

  2. `安装 PlantUML 工具 <https://www.javiljoen.net/n/installing-plantuml.html>`_
     （用于渲染 UML 图表）并确保它在您的 ``PATH`` 中。

     .. code:: console

        $ sudo apt install plantuml
        $ plantuml -version

  3. 构建文档：

    .. code-block:: console

      $ make html

    生成的 HTML 文件将位于 ``_build/html`` 目录下。您可以通过以下命令在浏览器中打开：

    .. code-block:: console

      $ xdg-open _build/html/index.html

实时重建
------------

为了更舒适地编辑和预览更改（因为 ``make html`` 会执行较慢的完整重建），
您可以安装 ``sphinx-autobuild``，它将监控文件更改并仅重建受影响的文件。
安装方法（在虚拟环境中）：

.. code-block:: console

  $ pip3 install sphinx-autobuild

运行：

.. code-block:: console

  $ make autobuild

这将执行初始干净构建，然后监控后续更改。

贡献
============

欢迎对文档做出贡献。这些贡献可以是简单的修复拼写错误或格式问题，
也可以是更复杂的更改，例如记录 NuttX 尚未涵盖的部分，甚至为其他用户编写指南。

贡献工作流程与代码相同，因此请查看 :doc:`/contributing/workflow` 以了解
您的更改应如何上游提交。

下面提供了一些标准文档类型的模板，例如板级支持文档或某些驱动程序等。
这些模板可以在浏览器中以 HTML 渲染形式查看，但当您使用这些模板编写自己的
文档时，您需要复制相应的 ``.rst`` 文件并进行修改。

.. toctree::
   :caption: 文档模板
   :glob:

   doc_templates/*

使用 Sphinx 编写 ReStructure Text
====================================

以下链接可用于了解 RST 语法和 Sphinx 特定指令。请注意，
有时 Sphinx 的方法会优于标准 RST，因为它更强大（例如标准链接与 Sphinx
``:ref:`` 可以跨文件使用，``code-block`` 指令与 ``::`` 允许指定高亮语言等）：

  * `Sphinx 文档系统 <https://www.sphinx-doc.org/en/master/>`__
  * `ReStructured Text 文档 <https://docutils.sourceforge.io/rst.html>`__
  * `Sphinx ReStructured Text 指南 <http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`__
  * `Restructured Text 速查表 <https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`__

文档规范
=========================

虽然 RST/Sphinx 提供了多种方式来完成任务，但最好遵循给定的规范以保持一致性并避免
陷阱。因此，文档更改应遵循以下规范集。

缩进
-----------

子块应缩进两个空格。这包括项目列表/枚举。

标题
--------

一般应使用三个级别的标题。用于标记章节的样式基于 ``=`` 和 ``-``。
章节应如下所示：

.. code-block:: RST

  =================
  顶级标题
  =================

  子章节
  ==========

  子子章节
  -------------

代码
----

代码应使用 `C 域 <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-c-domain>`_ 进行文档编写。
例如，函数应按如下方式记录：

.. code-block:: RST

  .. c:function:: bool myfunction(int arg1, int arg2)

    此处应描述函数的功能

    :param arg1: arg1 的描述
    :param arg2: arg2 的描述

    :return: 返回值的描述

要记录一段代码，请使用 ``code-block`` `指令 <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block>`_，
指定高亮语言。如果代码块不是代码而是某些逐字文本，
可以使用 RST 标准的 ``::``。在以下模式中使用时特别有用且紧凑：

.. code-block:: RST

  文本文件应包含以下内容::

    Line1
    Line2
    Line3

链接
-------

要生成内部链接，应使用 Sphinx 的 `角色 <https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#ref-role>`_。
因此，对于内部链接，请使用 ``:ref:`` 而不是标准 RST 语法 ```link <target>`_``。
如果目标在不同的文件中，您可以使用：``:ref:`链接文本 </pathtorst:章节名称>```。

链接到特定文档可以使用 ``:doc:`/path/to/document```（不带 ``.rst`` 扩展名）。

注释和 TODO
---------------

使用 RST `提示框 <https://docutils.sourceforge.io/docs/ref/rst/directives.html#admonitions>`_ 来突出文本中的内容，
例如需要突出显示的注释。

如果您需要在文档中留下 TODO 注释以指出某些内容需要改进，请使用 ``todo`` 提示框，
它通过 ``sphinx.ext.todo`` 扩展提供。这将让文档读者也知道文档
在某些地方尚未完成，并可能进一步激励贡献。

标签
----

使用来自 `sphinx-tags <https://sphinx-tags.readthedocs.io/en/latest/quickstart.html#usage>`_ 的 ``tag`` 提示框来
适当地标记您的页面。这使用户更容易搜索和索引文档。有一些标签
应始终包含：

- ``chip:*`` 标签用于板级/芯片文档，指示哪些板使用哪些芯片
- ``experimental`` 标签用于实验性的板级/功能，不应视为稳定
- 还可以为板包含支持的外设名称标签，如 ``wifi`` 和 ``ethernet``

在页面顶部包含标签指令，每个标签之间用逗号分隔。

用户指示
----------------

要指示按键、菜单操作或 GUI 按钮选择，请使用以下方式：

.. code-block:: RST

  进入菜单 :menuselection:`File --> Save As`，点击 :guilabel:`&OK` 或按 :kbd:`Enter`。

渲染效果如下：

进入菜单 :menuselection:`File --> Save As`，点击 :guilabel:`&OK` 或按 :kbd:`Enter`。

选项卡示例
---------------

要为不同场景（例如不同的操作系统）指示不同的说明/示例，
请使用 `tabs <https://github.com/executablebooks/sphinx-tabs>`_ 扩展（参见链接中的示例）。

提示
====

间距
-------

如果您遇到格式错误，请确保在指令及其内容之间提供适当的间距。
通常，您应遵循以下格式：

.. code-block:: RST

  .. directive::

    子内容

  非子内容，出现在前一个指令之后

注意指令和内容之间的行以及缩进。

