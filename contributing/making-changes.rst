.. include:: /substitutions.rst
.. _making-changes:

========================
使用 Git 进行更改
========================

Apache NuttX 项目使用 `Git 版本控制系统 <https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control>`_
来跟踪更改，源代码托管在 `GitHub <https://www.github.com>`_ 上。

如果您想对 NuttX 进行更改，无论是为了个人使用还是将更改提交回项目以改进 NuttX，
这都很简单。就本指南而言，您将需要一个 `GitHub <https://www.github.com>`_ 帐户，
因为 Apache NuttX 团队使用 GitHub。（您也可以在本地使用 git，或将更改保存到
其他站点，如 `GitLab <https://about.gitlab.com/>`_ 或 `BitBucket <https://bitbucket.org>`_，
但这超出了本指南的范围）。

操作步骤如下：

#. 设置您的 git 用户名和电子邮件

    .. code-block:: bash

       $ cd nuttx/
       $ git config --global user.name "Your Name"
       $ git config --global user.email "yourname@somedomaincom"

#. 登录 GitHub

   如果您没有 `GitHub <https://www.github.com>`_ 帐户，可以免费注册。

#. Fork 项目

   访问以下两个链接并点击页面右上角的 Fork 按钮：

   * `NuttX <https://github.com/apache/nuttx/>`_
   * `NuttX Apps <https://github.com/apache/nuttx-apps/>`_

#. 克隆仓库

   在您的 fork 的 ``nuttx`` 项目的 GitHub 网页上，复制克隆 URL -
   通过点击右上角的绿色 ``Clone or Download`` 按钮获取。然后执行：

    .. code-block:: bash

       $ git clone <your forked nuttx project clone url> nuttx
       $ cd nuttx
       $ git remote add upstream https://github.com/apache/nuttx.git

   对您的 fork 的 ``nuttx-apps`` 项目执行相同操作：

    .. code-block:: bash

       $ cd ..
       $ git clone <your forked nuttx-apps project clone url> apps
       $ cd apps
       $ git remote add upstream https://github.com/apache/nuttx-apps.git

#. 创建本地 Git 分支

   现在您可以创建本地 git 分支并将其推送到 GitHub：

    .. code-block:: bash

       $ git checkout -b test/my-new-branch
       $ git push

使用上游仓库的 Git 工作流程
========================================

主要的 NuttX git 仓库被称为"上游"仓库 - 这是因为它是主要的真理来源，
其更改流向下游到 fork 该仓库的人，比如我们。

使用上游仓库稍微复杂一些，但这是值得的，因为您可以向主要的 NuttX 仓库
提交修复和功能。您需要定期做的事情之一是保持您的本地仓库与上游同步。
在使用本地分支工作时，您可以进行更改，从上游拉取新软件并合并，
可能会这样做多次。然后当一切正常时，该分支就可以作为 Pull Request 提出。
工作原理如下：

#. 获取上游更改并合并到本地 master：

    .. code-block:: bash

       $ git checkout master
       $ git fetch upstream
       $ git merge upstream/master
       $ git push

#. 将本地 master 合并到本地分支：

    .. code-block:: bash

       $ git checkout my-local-branch
       $ git merge master
       $ git push

#. 进行更改并推送到您的 fork

    .. code-block:: bash

       $ vim my-file.c
       $ git add my-file.c
       $ git commit my-file.c
       $ git push

#. 根据需要重复步骤 1-3

#. 对您的文件运行 ``tools/checkpatch.sh`` 脚本

   当您的代码运行后，您几乎准备好提交了。但首先您需要检查代码以确保
   它符合 NuttX :ref:`contributing/coding_style:C Coding Standard`。
   ``tools/checkpatch.sh`` 脚本可以完成此操作。以下是使用信息：

    .. code-block:: bash

       $ ./tools/checkpatch.sh -h
       USAGE: ./tools/checkpatch.sh [options] [list|-]

       Options:
       -h
       -c spell check with codespell(install with: pip install codespell
       -r range check only (used with -p and -g)
       -p <patch list> (default)
       -g <commit list>
       -f <file list>
       -  read standard input mainly used by git pre-commit hook as below:
          git diff --cached | ./tools/checkpatch.sh -

   对您的文件运行它并更正您添加的代码中的所有错误，以便
   ``tools/checkpatch.sh`` 不报告任何错误。然后提交结果。
   例如：

    .. code-block:: bash

       $ ./tools/checkpatch.sh -f my-file.c
       arch/arm/src/sama5/hardware/my-file.c:876:82: warning: Long line found
       $ # 修复错误
       $ vim my-file.c
       $ # 再次运行
       $ ./tools/checkpatch.sh -f my-file.c

   如果您做了很多更改，也可以使用此 bash 命令行查看分支中所有已更改的 C
   文件的错误（假设您当前在有更改文件的分支上）：

    .. code-block:: bash

       $ git diff --name-only master | egrep "\.c|\.h" | xargs echo | xargs ./tools/checkpatch.sh -f | less

   请注意，``checkpatch.sh`` 使用的 ``nxstyle`` 程序存在一些错误，因此
   它可能会报告一些实际上不是错误的错误。提交者将帮助您
   发现这些错误。（或查看
   `nxstyle Issues <https://github.com/apache/nuttx/issues?q=is%3Aissue+is%3Aopen+nxstyle>`_。）
   |br|
   |br|

#. 提交修复后的文件

    .. code-block:: bash

       $ git add my-file.c
       $ git commit my-file.c
       $ git push

将您的更改提交给 NuttX
================================

  Pull Request 让您可以告诉其他人您已推送到 GitHub 仓库中某个分支的更改。
  一旦 Pull Request 被打开，您可以与协作者讨论和审查潜在的更改，
  并在更改合并到基础分支之前添加后续提交。

  （来自 GitHub 的 `关于 Pull Request <https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests>`_ 页面）

在进行 Pull Request 之前，NuttX 团队通常会希望您在分支中所做的所有更改
被"压缩"成单个提交，这样当他们审查您的更改时，会有一个清晰的历史视图。
如果在 Pull Request 审查反馈后有更改，它们可以是单独的提交。
以下是在提交 Pull Request 之前进行初始压缩的最简单方法：

#. 检出 ``my-branch``

    .. code-block:: bash

       $ git checkout my-branch

#. 获取上游代码

    .. code-block:: bash

       $ git fetch upstream

#. 变基到上游代码

    .. code-block:: bash

       $ git rebase upstream/master

#. 推送到您的远程仓库

   这需要使用 ``-f`` 进行强制推送。

    .. code-block:: bash

       $ git push -u my-branch -f

#. 创建 GitHub Pull Request

   Pull Request 是您请求上游审查和合并更改的方式。

   以下是 `GitHub 创建 Pull Request 的说明 <https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request>`_。

   包含有信息的提交标题和提交消息非常重要。

   .. note::

      您可以将克隆的 NuttX 副本的本地 Git 配置设置为
      每次提交时使用提供的提交模板。

      .. code:: console

         $ cd nuttx
         $ git config commit.template .gitmessage

      这将在您的编辑器中使用模板预填充提交消息，
      您可以将其作为起点进行编辑。

   在提交标题中，请包含与您的贡献相关的子系统/领域，
   后跟描述性消息。一些示例：

    添加或修复平台

    .. code-block:: bash

       arch/arm/stm32/: Add arch support for stm32 platform

       This patch adds initial support for stm32 platform. Please read
       the documentation included for more details how to wire the display.

       Signed-off-by: Your Name <you@whoareyou.com>

    添加或修复板级

    .. code-block:: bash

       arm/stm32f4discover: Add board initialization for SSD1306 OLED Display

       This patch adds support to use the display SSD1306 on I2C1, please read
       the documentation included for more details how to wire the display.

       Signed-off-by: Your Name <you@whoareyou.com>

   另一个示例，提交修复虚构传感器 xyz123 中的问题：

    .. code-block:: bash

       sensors/xyz123: Fix a pressure conversion resolution issue

       I found an issue in the XYZ123 sensor when converting the
       pressure. The raw value should be divided by 4.25 instead
       of 4.52.

       Signed-off-by: Your Name <you@whoareyou.com>

   您可以在 GitHub 提交历史中搜索更多示例。

#. 获取 Pull Request 反馈并实施更改

   从审阅者那里获取改进建议，进行更改，并推送到分支。一旦审阅者满意，
   他们可能会建议再次压缩和合并以创建单个提交。在这种情况下，您需要
   重复步骤 1 到 6。

   .. note::

      NuttX 使用 ``CODEOWNERS`` 文件来帮助跟踪哪些用户是某些
      NuttX 子系统的"专家"。有时，如果您修改了某个文件，
      该文件的"代码所有者"将被自动请求审查您的 PR。这只是为了
      帮助贡献者从了解相关领域的人员那里获得更相关的审查。

      如果您创建了新文件，例如驱动程序文件，您可以通过修改
      ``.github/CODEOWNERS`` 将自己添加为该文件的代码所有者。
      阅读 `GitHub CODEOWNERS 文档
      <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners>`_
      了解更多信息。

如何在 Pull Request 中包含建议？
====================================================

如果您提交了第一个 PR（Pull Request）并收到了一些修改提交的反馈，
那么您可能已经修改了它并创建了一个包含这些修改的新提交并提交了它。

您可能还看到这个新提交出现在 NuttX 的 GitHub 页面上的 Pull Request 中
（在 Commits 选项卡中）。

所以，有人会要求您做一些神秘的事情："请 rebase 并 squash 这些提交！"

基本上他们的意思是您需要更新您的仓库并将您的提交合并为单个提交。

让我们逐步完成这个操作！

移动到上游分支并从那里拉取新提交：

    .. code-block:: bash

       $ git checkout upstream
       $ git pull

返回您的工作分支并将其与上游 rebase：

    .. code-block:: bash

       $ git checkout my-branch
       $ git rebase upstream

如果您运行 git log，将看到您的提交仍然在那里：


    .. code-block:: bash

       $ git log
       commit xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (HEAD -> firstpr, upstream/master, upstream)

       Author: Me Myself
       Date: Today few seconds ago

       Fix suggestions from mainline

       commit xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

       Author: Me Myself
       Date: Today few minutes ago

       Initial support for something fantastic

       commit 6aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
       Author: Xiang Xiao <xiaoxiang@xiaomi.com>
       Date:   Sun Dec 18 00:00:00 2022 +0800

       Some existing commit from mainline

看，您有两个提交（Fix suggestions... 和 Initial support...），
我们可以将它们压缩为单个提交！

您可以使用 git rebase 交互式命令来压缩这两个提交：


    .. code-block:: bash

       $ git rebase -i HEAD~2

注意：如果您有 3 个提交，则应将 HEAD~2 替换为 HEAD~3，依此类推。

此命令将打开 nano 编辑器，显示以下屏幕：


    .. code-block:: bash

       pick 10ef3900b2 Initial support for something fantastic
       pick 9431582586 Fix suggestions from mainline

       # Rebase 9b0e1659ea..9431582586 onto 9b0e1659ea (2 commands)
       #
       # Commands:
       # p, pick <commit> = use commit
       ...

在这里您可以控制 git 将对您的提交执行的操作。

因为我们想要将第二个提交与第一个压缩，您需要将第二行的
'pick' 替换为 'squash'（或只是 's'），如下所示：


    .. code-block:: bash

       pick 10ef3900b2 Initial support for something fantastic
       squash 9431582586 Fix suggestions from mainline

       # Rebase 9b0e1659ea..9431582586 onto 9b0e1659ea (2 commands)
       #
       # Commands:
       # p, pick <commit> = use commit
       ...

现在只需按 `Ctrl + X` 保存此修改。在下一个屏幕中，您可以编辑您的 git
提交消息。之后再次按 Ctrl + X 保存。

如果您再次运行 git log，将看到现在只有一个提交：


    .. code-block:: bash

       $ git log
       commit xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (HEAD -> firstpr, upstream/master, upstream)
       Author: Me Myself
       Date: Right now baby, right now

       Initial support for something fantastic

       This commit includes the suggestions from mainline

       commit 6aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
       Author: Xiang Xiao <xiaoxiang@xiaomi.com>
       Date:   Sun Dec 18 00:00:00 2022 +0800

       Some existing commit from mainline

只需将这个新提交强制推送到您的仓库：


    .. code-block:: bash

       $ git push -f

现在您可以在 NuttX 的 GitHub 上查看您的 PR，以确认
这个压缩的提交在那里。

Git 资源
=============

* `Git 速查表（GitHub 版） <https://github.github.com/training-kit/downloads/github-git-cheat-sheet.pdf>`_
* `Git 手册（在线） <https://git-scm.com/book/en/v2>`_
* `NuttX 代码贡献工作流程（草案） <https://cwiki.apache.org/confluence/display/NUTTX/Code+Contribution+Workflow>`_
  – 所有细节都在这里，如果您需要的话！
