================================
创建 Apache NuttX 发布版本
================================

NuttX 的发布周期大约为每 3 个月一次。

检出分发 SVN 仓库
==========================================

发布通过 SVN 仓库管理。有两个位置可以提交发布版本：dev 和 release。
在投票之前，发布版本会暂存在 dev 文件夹中；在发布被 IPMC 批准后，
它将被移动到 release 位置并提交以供分发。release 文件夹还包含用于
签名发布的 GPG 公钥，存储在 KEYS 文件中。

.. code-block:: console

  $ svn checkout https://dist.apache.org/repos/dist/dev/nuttx nuttx-dev
  $ svn checkout https://dist.apache.org/repos/dist/release/nuttx nuttx-release

添加您的 GPG 密钥
===================

在 ``dist/release/nuttx 文件夹`` 中有一个 KEYS 文件，提交者必须
在其中上传他们用于签名发布的 GPG 公钥。在文件顶部，您可以看到
如何将密钥添加到此文件的说明。请注意不要删除任何现有密钥。
dev 和 releases 文件夹中都有 KEYS 文件，但上传到 releases 文件夹
是重要的。

如果您还没有为此项目创建 GPG 密钥，请参阅
https://infra.apache.org/openpgp.html#generate-key 重要的是您的
Apache 电子邮件应与此密钥关联。

我的密钥 ID 是 ``3554D78458CEB6954B020E12E1B6E30DB05D6280``。
您可以使用以下命令列出您拥有私钥的密钥。确保您的 Apache 电子邮件
与此密钥关联。

.. code-block:: console

   $ gpg2 --list-secret-keys
    /home/bashton/.gnupg/pubring.kbx
    --------------------------------
    sec>  rsa4096 2019-11-24 [SC] [expires: 2021-09-02]
          3554D78458CEB6954B020E12E1B6E30DB05D6280
          Card serial no. = 0006 09239558
    uid           [ultimate] Brennan Ashton <btashton@apache.org>
    uid           [ultimate] Brennan Ashton <bashton@brennanashton.com>
    ssb>  rsa4096 2019-11-24 [E] [expires: 2021-09-02]
    ssb>  rsa4096 2019-11-24 [A] [expires: 2021-09-02]
    ssb   rsa4096 2019-11-24 [S] [expires: 2021-09-02]

然后您可以使用以下命令添加到 KEYS 文件（将"key id"替换为您的密钥 ID）：

.. code-block:: console

   $ (gpg --list-sigs <key id> && gpg --armor --export <key id>) >> KEYS

您可以使用以下命令验证您的密钥是否在文件中：

.. code-block:: console

   $ cat KEYS | gpg2 --import-options show-only

确认更改满意后，您可以提交您的密钥

.. code-block:: console

   $ svn commit -m "Update <my name> GPG key"

将您的 GPG 密钥添加到 GitHub / Apache
===================================

为了使发布标签显示为"已验证"，请将您的 GPG 密钥附加到您的
Apache 和 GitHub 帐户：

* GitHub: https://docs.github.com/en/github/authenticating-to-github/adding-a-new-gpg-key-to-your-github-account

* Apache: https://id.apache.org

  * *将指纹添加到 OpenPGP Public Key Primary Fingerprint*

创建发布候选版本
============================

当项目对发布分支满意并准备好创建发布候选版本时，
第一步是创建签名标签。这应该对 nuttx 和 nuttx-apps 仓库都执行。

以下是为 12.1.0 发布版本创建 RC0 标签的示例。
这里只显示了 OS 仓库，对 apps 仓库也必须执行相同操作。

.. code-block:: console

   # 导出签名密钥
   $ export GPG_TTY=$(tty)

   # 检出发布分支
   ~/nuttx/wrk/nuttx on  releases/12.1 [$] 
   $ git checkout releases/12.1
   Already on 'releases/12.1'
   Your branch is up to date with 'origin/releases/12.1'.

   # 确保与上游同步
   ~/nuttx/wrk/nuttx on  releases/12.1 [$] 
   $ git pull
   Already up to date.

   # 创建签名标签（注意 -s 选项）
   ~/nuttx/wrk/nuttx on  releases/12.1 [$] 
   $ git tag -s nuttx-12.1.0-RC0 -m nuttx-12.1.0-RC0

   # 验证标签在正确的提交上
   ~/nuttx/wrk/nuttx on  releases/12.1 [$] 
   $ git log -n 1
   commit 16748108c503d762779545d40113825e54b75252 (HEAD -> releases/12.1, tag: nuttx-12.1.0-RC0, origin/releases/12.1)
   Author: Dong Heng <dongheng@espressif.com>
   Date:   Fri Apr 9 20:03:24 2021 +0800

       riscv/esp32c3: Fix heap end address

   # 将标签推送到 apache 仓库
   ~/nuttx/wrk/nuttx on  releases/12.1 [$] 
   $ git push -u origin nuttx-12.1.0-RC0
   Enumerating objects: 1, done.
   Counting objects: 100% (1/1), done.
   Writing objects: 100% (1/1), 805 bytes | 402.00 KiB/s, done.
   Total 1 (delta 0), reused 0 (delta 0), pack-reused 0
   To github.com:apache/nuttx.git
    * [new tag]               nuttx-12.1.0-RC0 -> nuttx-12.1.0-RC0

您应该能在以下位置看到标签：https://github.com/apache/nuttx/tags 和
https://github.com/apache/nuttx-apps/tags。

创建发布压缩包
=============================

确保两个仓库都检出到正确的发布候选版本标签。
文件夹名称必须是 ``nuttx`` 和 ``apps``。

.. code-block:: console

   ~/nuttx/wrk/release 
   $ ls
   apps  nuttx

   ~/nuttx/wrk/release 
   $ git -C nuttx log -n 1
   commit 16748108c503d762779545d40113825e54b75252 (HEAD -> releases/12.1, tag: nuttx-12.1.0-RC0, origin/releases/12.1)
   Author: Dong Heng <dongheng@espressif.com>
   Date:   Fri Apr 9 20:03:24 2021 +0800

       riscv/esp32c3: Fix heap end address

   ~/nuttx/wrk/release 
   $ git -C apps log -n 1
   commit 4348d91d1356335483089c3865282d80f13bedcd (HEAD -> releases/12.1, tag: nuttx-12.1.0-RC0, origin/releases/12.1)
   Author: Abdelatif Guettouche <abdelatif.guettouche@espressif.com>
   Date:   Mon Apr 12 10:11:05 2021 +0200

       wireless/wapi/src/wapi.c: When executing a command return it's error code on failure.
       
       Signed-off-by: Abdelatif Guettouche <abdelatif.guettouche@espressif.com>

创建发布压缩包时，考虑使用 ``-d`` 标志启用调试模式，以确保一切正确，
包括使用正确的文件夹。请注意，这里我们在版本中不使用 RC。
如果此 RC 被接受，这些确切的文件将从 dev 移动到 release 文件夹，
压缩包*不会*重新创建。以下是使用我的密钥 ID 和 12.1.0 发布版本
进行签名的示例：

.. code-block:: console

   ~/nuttx/wrk/release took 2s 
   $ ./nuttx/tools/zipme.sh -d -s -k 3554D78458CEB6954B020E12E1B6E30DB05D6280 12.1.0
   + DEBUG=-d
   + shift
   + '[' '!' -z -s ']'
   + case $1 in
   + sign=1
   + shift
   + '[' '!' -z -k ']'
   + case $1 in
   + shift
   + GPG+=' --default-key 3554D78458CEB6954B020E12E1B6E30DB05D6280'
   + shift
   + '[' '!' -z 12.1.0 ']'
   + case $1 in
   + break
   + VERSION=12.1.0
   + '[' -n 12.1.0 ']'
   + VERSIONOPT='-v 12.1.0'
   + for pat in ${EXCLPAT}
   + TAR+=' --exclude=.github'
   + for pat in ${EXCLPAT}
   + TAR+=' --exclude=.asf.yaml'
   + TAR+=' --exclude-vcs'
   + '[' 0 '!=' 0 ']'
   + TAR+=' -czf'
   ++ basename ./nuttx/tools/zipme.sh
   + MYNAME=zipme.sh
   + '[' -x /home/bashton/nuttx/wrk/release/zipme.sh ']'
   + '[' -x /home/bashton/nuttx/wrk/release/tools/zipme.sh ']'
   + '[' -x /home/bashton/nuttx/wrk/release/nuttx/tools/zipme.sh ']'
   + TRUNKDIR=/home/bashton/nuttx/wrk/release
   + NUTTXDIR=/home/bashton/nuttx/wrk/release/nuttx
   + APPSDIR=/home/bashton/nuttx/wrk/release/apps
   + '[' '!' -d /home/bashton/nuttx/wrk/release ']'
   + cd /home/bashton/nuttx/wrk/release
   + '[' '!' -d /home/bashton/nuttx/wrk/release/nuttx ']'
   + '[' '!' -d /home/bashton/nuttx/wrk/release/apps ']'
   + echo 'Cleaning the repositories'
   Cleaning the repositories
   + '[' 0 '!=' 0 ']'
   + make -C /home/bashton/nuttx/wrk/release/nuttx distclean
   + VERSIONSH=/home/bashton/nuttx/wrk/release/nuttx/tools/version.sh
   + '[' '!' -x /home/bashton/nuttx/wrk/release/nuttx/tools/version.sh ']'
   + /home/bashton/nuttx/wrk/release/nuttx/tools/version.sh -d -v 12.1.0 /home/bashton/nuttx/wrk/release/nuttx/.version
   + shift
   + '[' '!' -z -v ']'
   + case $1 in
   + shift
   + VERSION=12.1.0
   + shift
   + '[' '!' -z /home/bashton/nuttx/wrk/release/nuttx/.version ']'
   + case $1 in
   + break
   + OUTFILE=/home/bashton/nuttx/wrk/release/nuttx/.version
   + '[' -z 12.1.0 ']'
   + '[' -z 12.1.0 ']'
   + '[' -z /home/bashton/nuttx/wrk/release/nuttx/.version ']'
   ++ echo 12.1.0
   ++ cut -d. -f1
   + MAJOR=10
   + '[' X10 = X12.1.0 ']'
   ++ echo 12.1.0
   ++ cut -d. -f2
   + MINOR=1
   + '[' X12.1 = X12.1.0 ']'
   ++ echo 12.1.0
   ++ grep -Eo '[0-9]+\.[0-9]+\.[0-9]+'
   ++ cut -d. -f3
   + PATCH=0
   + '[' -z '' ']'
   ++ git -C /home/bashton/nuttx/wrk/release/nuttx/tools log --oneline -1
   ++ cut '-d ' -f1
   + BUILD=16748108c5
   + '[' -z 16748108c5 ']'
   ++ git -C /home/bashton/nuttx/wrk/release/nuttx/tools diff-index --name-only HEAD
   ++ head -1
   + '[' -n '' ']'
   + echo '#!/bin/bash'
   + echo ''
   + echo 'CONFIG_VERSION_STRING="12.1.0"'
   + echo CONFIG_VERSION_MAJOR=10
   + echo CONFIG_VERSION_MINOR=1
   + echo CONFIG_VERSION_PATCH=0
   + echo 'CONFIG_VERSION_BUILD="16748108c5"'
   + chmod 755 /home/bashton/nuttx/wrk/release/nuttx/.version
   + '[' -z 12.1.0 ']'
   + NUTTX_TARNAME=apache-nuttx-12.1.0.tar
   + APPS_TARNAME=apache-nuttx-apps-12.1.0.tar
   + NUTTX_ZIPNAME=apache-nuttx-12.1.0.tar.gz
   + APPS_ZIPNAME=apache-nuttx-apps-12.1.0.tar.gz
   + NUTTX_ASCNAME=apache-nuttx-12.1.0.tar.gz.asc
   + APPS_ASCNAME=apache-nuttx-apps-12.1.0.tar.gz.asc
   + NUTTX_SHANAME=apache-nuttx-12.1.0.tar.gz.sha512
   + APPS_SHANAME=apache-nuttx-apps-12.1.0.tar.gz.sha512
   + '[' -f apache-nuttx-12.1.0.tar ']'
   + '[' -f apache-nuttx-12.1.0.tar.gz ']'
   + echo 'Removing /home/bashton/nuttx/wrk/release/apache-nuttx-12.1.0.tar.gz'
   Removing /home/bashton/nuttx/wrk/release/apache-nuttx-12.1.0.tar.gz
   + rm -f apache-nuttx-12.1.0.tar.gz
   + '[' -f apache-nuttx-apps-12.1.0.tar ']'
   + '[' -f apache-nuttx-apps-12.1.0.tar.gz ']'
   + '[' -f apache-nuttx-12.1.0.tar.gz.asc ']'
   + '[' -f apache-nuttx-apps-12.1.0.tar.gz.asc ']'
   + '[' -f apache-nuttx-12.1.0.tar.gz.sha512 ']'
   + '[' -f apache-nuttx-apps-12.1.0.tar.gz.sha512 ']'
   + echo 'Archiving and zipping nuttx/'
   Archiving and zipping nuttx/
   ++ basename /home/bashton/nuttx/wrk/release/nuttx
   + tar --exclude=.github --exclude=.asf.yaml --exclude-vcs -czf apache-nuttx-12.1.0.tar.gz nuttx
   + echo 'Archiving and zipping apps/'
   Archiving and zipping apps/
   ++ basename /home/bashton/nuttx/wrk/release/apps
   + tar --exclude=.github --exclude=.asf.yaml --exclude-vcs -czf apache-nuttx-apps-12.1.0.tar.gz apps
   + echo 'Creating the hashes'
   Creating the hashes
   + sha512sum apache-nuttx-12.1.0.tar.gz
   + sha512sum apache-nuttx-apps-12.1.0.tar.gz
   + '[' 1 '!=' 0 ']'
   + echo 'Signing the tarballs'
   Signing the tarballs
   + gpg -sab --default-key 3554D78458CEB6954B020E12E1B6E30DB05D6280 apache-nuttx-12.1.0.tar.gz
   gpg: using "3554D78458CEB6954B020E12E1B6E30DB05D6280" as default secret key for signing
   + gpg -sab --default-key 3554D78458CEB6954B020E12E1B6E30DB05D6280 apache-nuttx-apps-12.1.0.tar.gz
   gpg: using "3554D78458CEB6954B020E12E1B6E30DB05D6280" as default secret key for signing
   + cd /home/bashton/nuttx/wrk/release/nuttx

   ~/nuttx/wrk/release took 6s 
   $ ls
   apache-nuttx-12.1.0.tar.gz      apache-nuttx-12.1.0.tar.gz.sha512  apache-nuttx-apps-12.1.0.tar.gz.asc     apps
   apache-nuttx-12.1.0.tar.gz.asc  apache-nuttx-apps-12.1.0.tar.gz    apache-nuttx-apps-12.1.0.tar.gz.sha512  nuttx

检查发布产物
===========================

在上传产物之前，最好确保它们通过了完整性检查。
您可以通过对它们运行 ``nuttx/tools/checkrelease.sh`` 脚本来完成此操作。
这将仅使用 https://dist.apache.org/repos/dist/dev/nuttx/KEYS 中的 GPG 密钥，
因此请确保。

.. code-block:: console

   ~/nuttx/wrk/release 
   $ ./nuttx/tools/checkrelease.sh --dir ./
   gpg: directory '/tmp/nuttx-checkrelease/.gnupg' created
   gpg: keybox '/tmp/nuttx-checkrelease/.gnupg/pubring.kbx' created
   gpg: /tmp/nuttx-checkrelease/.gnupg/trustdb.gpg: trustdb created
   gpg: key E1B6E30DB05D6280: public key "Brennan Ashton <btashton@apache.org>" imported
   gpg: Total number processed: 1
   gpg:               imported: 1
    OK: https://dist.apache.org/repos/dist/dev/nuttx/KEYS is imported.
   Checking apache-nuttx-12.1.0.tar.gz sha512...
    OK: apache-nuttx-12.1.0.tar.gz sha512 hash matches.

   Checking apache-nuttx-12.1.0.tar.gz GPG signature:
   gpg: Signature made Sat 17 Apr 2021 08:02:29 PM PDT
   gpg:                using RSA key 66C4832A165ECC9354895A209750ED7E692B99E2
   gpg: Good signature from "Brennan Ashton <btashton@apache.org>" [unknown]
   gpg:                 aka "Brennan Ashton <bashton@brennanashton.com>" [unknown]
   gpg: WARNING: This key is not certified with a trusted signature!
   gpg:          There is no indication that the signature belongs to the owner.
   Primary key fingerprint: 3554 D784 58CE B695 4B02  0E12 E1B6 E30D B05D 6280
        Subkey fingerprint: 66C4 832A 165E CC93 5489  5A20 9750 ED7E 692B 99E2
    OK: apache-nuttx-12.1.0.tar.gz gpg signature matches.

   Checking apache-nuttx-12.1.0.tar.gz for required files:
    OK: all required files exist in nuttx.

   Checking apache-nuttx-apps-12.1.0.tar.gz sha512...
    OK: apache-nuttx-apps-12.1.0.tar.gz sha512 hash matches.

   Checking apache-nuttx-apps-12.1.0.tar.gz GPG signature:
   gpg: Signature made Sat 17 Apr 2021 08:02:30 PM PDT
   gpg:                using RSA key 66C4832A165ECC9354895A209750ED7E692B99E2
   gpg: Good signature from "Brennan Ashton <btashton@apache.org>" [unknown]
   gpg:                 aka "Brennan Ashton <bashton@brennanashton.com>" [unknown]
   gpg: WARNING: This key is not certified with a trusted signature!
   gpg:          There is no indication that the signature belongs to the owner.
   Primary key fingerprint: 3554 D784 58CE B695 4B02  0E12 E1B6 E30D B05D 6280
        Subkey fingerprint: 66C4 832A 165E CC93 5489  5A20 9750 ED7E 692B 99E2
    OK: apache-nuttx-apps-12.1.0.tar.gz gpg signature matches.

   Checking apache-nuttx-apps-12.1.0.tar.gz for required files:
    OK: all required files exist in apps.

   Trying to build nuttx sim:nsh...
    OK: we were able to build sim:nsh.

暂存发布候选版本
=============================

要暂存发布版本，应在
https://dist.apache.org/repos/dist/dev/nuttx 下为发布候选版本创建新文件夹，
并将这些发布产物复制到那里：

.. code-block:: console

    apache-nuttx-<version>.tar.gz      apache-nuttx-<version>.tar.gz.sha512  apache-nuttx-apps-<version>.tar.gz.asc
    apache-nuttx-<version>.tar.gz.asc  apache-nuttx-apps-<version>.tar.gz    apache-nuttx-apps-<version>.tar.gz.sha512

如果您按照前面所示将 svn 仓库检出为 nuttx-dev。这应该这样完成：

.. code-block:: console

   ~/nuttx/svn/nuttx-dev 
   $ mkdir 12.1.0-RC0
   
   ~/nuttx/svn/nuttx-dev 
   $ cp -v ../../wrk/release/apache-{nuttx,nuttx-apps}-12.1.0.tar.gz* ./12.1.0-RC0/
   '../../wrk/release/apache-nuttx-12.1.0.tar.gz' -> './12.1.0-RC0/apache-nuttx-12.1.0.tar.gz'
   '../../wrk/release/apache-nuttx-12.1.0.tar.gz.asc' -> './12.1.0-RC0/apache-nuttx-12.1.0.tar.gz.asc'
   '../../wrk/release/apache-nuttx-12.1.0.tar.gz.sha512' -> './12.1.0-RC0/apache-nuttx-12.1.0.tar.gz.sha512'
   '../../wrk/release/apache-nuttx-apps-12.1.0.tar.gz' -> './12.1.0-RC0/apache-nuttx-apps-12.1.0.tar.gz'
   '../../wrk/release/apache-nuttx-apps-12.1.0.tar.gz.asc' -> './12.1.0-RC0/apache-nuttx-apps-12.1.0.tar.gz.asc'
   '../../wrk/release/apache-nuttx-apps-12.1.0.tar.gz.sha512' -> './12.1.0-RC0/apache-nuttx-apps-12.1.0.tar.gz.sha512'

然后提交这些文件：

.. code-block:: console

   ~/nuttx/svn/nuttx-dev 
   $ svn status
   ?       12.1.0-RC0
   
   ~/nuttx/svn/nuttx-dev 
   $ svn add 12.1.0-RC0/
   A         12.1.0-RC0
   A         12.1.0-RC0/apache-nuttx-12.1.0.tar.gz.sha512
   A         12.1.0-RC0/apache-nuttx-apps-12.1.0.tar.gz.sha512
   A  (bin)  12.1.0-RC0/apache-nuttx-12.1.0.tar.gz.asc
   A  (bin)  12.1.0-RC0/apache-nuttx-apps-12.1.0.tar.gz.asc
   A  (bin)  12.1.0-RC0/apache-nuttx-12.1.0.tar.gz
   A  (bin)  12.1.0-RC0/apache-nuttx-apps-12.1.0.tar.gz
   
   ~/nuttx/svn/nuttx-dev 
   $ svn commit -m "Staging apache-nuttx-12.1.0-RC0"

验证发布版本存在于 https://dist.apache.org/repos/dist/dev/nuttx/ 下

发起社区投票
=========================

为此，发送一封类似以下内容的电子邮件：

.. code-block:: text

   Subject: [VOTE] Apache NuttX 12.1.0 RC0 release
   To: dev@nuttx.apache.org

   Hello all,
   Apache NuttX 12.1.0 RC0 has been staged under [1] and it's
   time to vote on accepting it for release. If approved we will seek
   final release approval from the IPMC. Voting will be open for 72hr.

   A minimum of 3 binding +1 votes and more binding +1 than binding -1 are
   required to pass.

   The Apache requirements for approving a release can be found here [3]
   "Before voting +1 [P]PMC members are required to download the signed
   source code package, compile it as provided, and test the resulting
   executable on their own platform, along with also verifying that the
   package meets the requirements of the ASF policy on releases."

   A document to walk through some of this process has been published on
   our project wiki and can be found here [4].

   [ ] +1 accept (indicate what you validated - e.g. performed the non-RM
   items in [4])
   [ ] -1 reject (explanation required)

   Thank you all,
   <Release Manager>

   SCM Information:
     Release tag: nuttx-12.1.0-RC0
     Hash for the release nuttx tag: <GIT HASH>
     Hash for the release nuttx-apps tag: <GIT HASH>

   [1] https://dist.apache.org/repos/dist/dev/nuttx/12.1.0-RC0/
   [2] https://raw.githubusercontent.com/apache/nuttx/nuttx-12.1.0-RC0/ReleaseNotes
   [3] https://www.apache.org/dev/release.html#approving-a-release
   [4] https://cwiki.apache.org/confluence/display/NUTTX/Validating+a+staged+Release

在投票要求满足后（参见电子邮件文本），发送一封电子邮件结束投票。

该电子邮件的示例文本在此。请注意，您需要填写投票计数和投票线程的存档链接。
查找链接的最佳方式是访问 https://lists.apache.org/list.html?dev@nuttx.apache.org

.. code-block:: text

   Subject: [RESULTS][VOTE] Release Apache NuttX 12.1.0 [RC0]
   To: dev@nuttx.apache.org
   
   Hi all,
   
   The vote to release Apache NuttX 12.1.0-rc0 is now closed.
   Thanks to those that took the time to review and vote.
   
   The release has passed with 4 +1 (binding) votes and no 0 or -1 votes.
   
   Binding:
   +1 Lup Yuen Lee
   +1 Roberto Bucher
   +1 Tomek CEDRO
   +1 Alin Jerpelea
   
   Non binding
   +1 Filipe Cavalcanti
   
   Vote thread
   https://lists.apache.org/thread.html/r75faed90e03c7e7a07ff79988bb0586eec224905144f34e99333e9cd%40%3Cgeneral..apache.org%3E
   
   We will proceed with the official release of 12.1.0.

如果投票未通过，请将反馈带给社区，并使用新的 RC 重新开始发布流程。

暂存发布
===================

在发布获得批准后，您现在可以将发布产物复制到发布仓库。
请注意，文件夹名称中不再包含 RC。

.. code-block:: console

   ~/nuttx/svn 
   $ cp -r nuttx-dev/12.1.0-RC0 nuttx-release/12.1.0
   
   ~/nuttx/svn 
   $ cd nuttx-release/
   
   ~/nuttx/svn/nuttx-release 
   $ svn status
   ?       12.1.0
   
   ~/nuttx/svn/nuttx-release 
   $ svn add 12.1.0
   A         12.1.0
   A  (bin)  12.1.0/apache-nuttx-12.1.0.tar.gz
   A  (bin)  12.1.0/apache-nuttx-apps-12.1.0.tar.gz
   A         12.1.0/apache-nuttx-12.1.0.tar.gz.sha512
   A         12.1.0/apache-nuttx-apps-12.1.0.tar.gz.sha512
   A  (bin)  12.1.0/apache-nuttx-12.1.0.tar.gz.asc
   A  (bin)  12.1.0/apache-nuttx-apps-12.1.0.tar.gz.asc
   $ svn commit -m "Releasing apache-nuttx-12.1.0"

此时您应该能在
https://dist.apache.org/repos/dist/release/nuttx/ 看到发布版本

创建发布标签
===================

以与创建 RC 标签相同的方式在两个仓库上创建非 RC 标签：

.. code-block:: console

   # 导出签名密钥
   $ export GPG_TTY=$(tty)
   
   ~/nuttx/wrk/nuttx on  releases/12.1 [$] 
   $ git checkout releases/12.1
   Already on 'releases/12.1'
   Your branch is up to date with 'origin/releases/12.1'.
   
   # 确保与上游同步
   ~/nuttx/wrk/nuttx on  releases/12.1 [$] 
   $ git pull
   Already up to date.
   
   # 创建签名标签（注意 -s 选项）
   ~/nuttx/wrk/nuttx on  releases/12.1 [$] 
   $ git tag -s nuttx-12.1.0 -m nuttx-12.1.0
   
   # 检查 RC 和非 RC 标签都存在于提交上
   ~/nuttx/wrk/release/nuttx on  releases/12.1 [$] took 4s 
   $ git log -n 1
   commit 16748108c503d762779545d40113825e54b75252 (HEAD -> releases/12.1, tag: nuttx-12.1.0-RC0, tag: nuttx-12.1.0, origin/releases/12.1)
   Author: Dong Heng <dongheng@espressif.com>
   Date:   Fri Apr 9 20:03:24 2021 +0800
   
       riscv/esp32c3: Fix heap end address
   
   # 推送标签
   ~/nuttx/wrk/release/nuttx on  releases/12.1 [$] 
   $  git push -u origin nuttx-12.1.0
   Enumerating objects: 1, done.
   Counting objects: 100% (1/1), done.
   Writing objects: 100% (1/1), 805 bytes | 402.00 KiB/s, done.
   Total 1 (delta 0), reused 0 (delta 0), pack-reused 0
   To github.com:apache/nuttx.git
    * [new tag]               nuttx-12.1.0 -> nuttx-12.1.0

您应该能在以下位置看到标签：https://github.com/apache/nuttx/tags 和
https://github.com/apache/nuttx-apps/tags

创建 PR 以将发布版本添加到网站
=============================================

这应该包括发布说明以及下载发布的元数据。
示例在此：apache/nuttx-website#39。在提交到发布 SVN 后 48 小时，
分发镜像应该已经同步，现在可以合并。

合并后大约 10 分钟，您应该能在这里看到发布版本：
https://nuttx.apache.org/download/

发送发布电子邮件
==========================

一旦网站显示发布版本，您现在可以发送发布通知。
以下是该电子邮件的示例。请注意，我们必须在 SVN 提交后等待 48 小时
才能发送此邮件。

.. code-block:: text

   Subject: [ANNOUNCE] Apache NuttX 12.1.0 released
   To: dev@nuttx.apache.org

   The Apache NuttX project team is proud to announce
   Apache NuttX 12.1.0 has been released.

   The release artifacts and Release Notes can be found at:
   https://nuttx.apache.org/download/
   https://nuttx.apache.org/releases/12.1.0/

   Thanks,
   <Release Manager>
   on behalf of Apache NuttX PPMC
