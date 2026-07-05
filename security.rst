========
安全
========

.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/

.. toctree::

已知漏洞
=====================

Apache NuttX RTOS 漏洞以 CVE（通用漏洞披露）标识符标注。已知的、经负责任披露并已修复的漏洞列表可在
`CVE.ORG <https://www.cve.org/CVERecord/SearchResults?query=nuttx>`_
上公开查阅，也可在本页底部的 `NuttX CVEs`_ 部分查看。

`CVE <https://cve.org/>`_ ID 是分配给安全漏洞的唯一标识符。Apache 安全团队是
`CVE 编号授权机构 (CNA) <https://www.cve.org/ProgramOrganization/CNAs>`_，
负责覆盖所有 Apache 项目，是唯一能够为 Apache 软件基金会项目问题分配 ID 的组织。


不属于安全漏洞的情况
============================

Apache NuttX RTOS 具有高度可移植性，支持超过 15 种不同的 CPU 架构，
包括内存资源仅有数千字节 RAM/Flash 的微控制器。在通用性之外增加额外的检查
会严重影响最终固件的性能和体积。
**函数参数和传入数据的验证责任在于自定义应用/固件的开发者。**

处理以下内容时应格外小心：

 * 系统调用。
 * 指针（使用前后始终设置为 NULL）。
 * 结构体（使用前始终用 ``{0}`` 初始化）。
 * 用户可控数据（类型和大小）。
 * 网络数据。
 * 动态分配的缓冲区。

.. note::
  如果您在现有代码库中发现可能影响机密性、完整性或可用性（例如信息泄露、
  拒绝服务、远程代码执行）的通用性问题，且该问题并非您自定义应用特有的，
  请向我们发送安全报告。


安全问题处理流程
========================

安全相关问题的处理遵循
`Apache 安全团队指南 <https://www.apache.org/security/>`_
和 `Apache 提交者安全指南
<https://www.apache.org/security/committers.html>`_。
在提交和/或处理安全漏洞之前，请仔细阅读这些文件。以下是信息摘录。

.. warning::
  请勿在项目的公开缺陷跟踪器、问题或拉取请求中输入安全漏洞的详细信息。
  在本流程结束并正式公告之前，请勿公开漏洞相关信息。
  与任何提交相关的消息都不应提及该提交的安全性质。


1. 报告：

  1. 请通过电子邮件将潜在安全漏洞报告至 security@nuttx.apache.org，
     **在此之前请勿以任何形式公开披露**。这使得在详细信息公开之前能够为
     所有受影响者提供修复，从而实现负责任的披露。发送到我们 security@ 地址的
     邮件会自动抄送至 security@apache.org。

  2. 请为每个您正在报告的漏洞发送一封纯文本、未加密的电子邮件。
     如果您将报告以图片、视频、HTML 或 PDF 附件形式发送（而您本可以用纯文本
     轻松描述），我们可能会要求您重新提交。

  3. 请勿在项目的公开缺陷跟踪器、问题或拉取请求中输入安全漏洞的详细信息。
     **在本流程结束并正式公告之前，请勿公开漏洞相关信息。**
     与任何提交相关的消息都不应提及该提交的安全性质。

  4. 安全修复通常是标准发布周期的一部分，但对于紧急情况，
     可能会创建特殊的补丁发布来解决问题。为保持流程顺畅，
     请尽可能提供详细信息。**可复现的示例、概念验证代码，
     但最重要的是修复补丁，都非常欢迎。**

  5. 有些问题我们已经知晓，并且已被多次报告，但我们不将其归类为安全漏洞，
     详情请参见 `不属于安全漏洞的情况`_。请考虑在 GitHub 上将其作为
     Issue 或 Pull Request 报告。

  6. 项目团队向原始报告者发送电子邮件确认收到报告，并抄送至相关安全邮件列表。


2. 调查：

  1. 项目团队调查报告并决定拒绝或接受。

  2. 项目团队成员可以在项目安全团队的判断下与领域专家（包括其雇主的同事）
     共享漏洞信息，前提是他们明确表示 **信息不得公开披露。**

  3. 如果项目团队 **拒绝** 该报告，团队会向报告者写信解释原因，
     并抄送至相关安全邮件列表。

  4. 如果项目团队 **接受** 该报告，团队会向报告者写信告知已接受报告，
     并正在开发修复方案或验证报告者提供的修复方案。
     会在解决问题时请求 CVE ID 并报告问题详情。


3. 解决：

  1. 项目团队在私有邮件列表上就修复方案达成一致。

  2. 项目团队从内部门户 https://cveprocess.apache.org 请求 CVE（通用漏洞披露）
     ID。Apache 安全团队可以帮助确定一份报告是否需要多个 CVE ID，
     或者多份报告是否应合并为单个 CVE ID。CVE ID 可以与报告者共享。

  3. 项目团队在内部门户上记录漏洞和修复的详细信息。门户会生成公告草案文本。
     关于公告示例，请参见 Tomcat 的 CVE-2008-2370 公告。报告中包含的详细程度
     取决于判断。通常，报告应包含足够的信息，使人们能够评估漏洞对其自身系统的
     风险，但不应过多。**公告通常不包含复现漏洞的步骤。**

  4. 可选地，CVE 可以设置为 REVIEW 状态以请求 Apache 安全团队进行审核。
     可以使用"评论"功能进行讨论，评论也会发送到私有邮件列表。

  5. 项目团队向报告者提供修复副本和漏洞公告草案以征求意见。

  6. 项目团队与报告者就修复方案、公告和发布时间表达成一致。
     如果报告者在合理时间内未响应，不应阻止项目团队继续推进后续步骤，
     尤其是在问题严重程度/影响较高的情况下。

  7. 项目团队提交修复，**且不提及该提交与安全漏洞相关。**

  8. 项目团队创建包含该修复的发布版本。


4. 公开公告：

  1. 在发布公告之后（或同时），项目团队公告漏洞和修复方案。
     CVE 状态在内部门户中设置为 READY，该门户也用于发送邮件。
     **这是漏洞相关信息首次公开的时间点。** 漏洞公告应发送至以下目的地：

     a. 与发布公告相同的地址。
     b. 漏洞报告者。
     c. 项目安全列表（如项目没有专用安全列表，则发送至 security@apache.org）。
     d. oss-security@lists.openwall.com（无需订阅）。

  2. 项目团队更新项目的安全页面。


NuttX CVEs
==========

CVE-2025-48769
--------------

* 标题：fs/vfs/fs_rename：释放后使用。
* 发布日期：2026-01-01。
* 受影响版本：>= 7.20，< 12.11.0。
* 修复版本：12.11.0。
* 类型：`CWE-416 释放后使用 <https://cwe.mitre.org/data/definitions/416.html>`_。
* 致谢：

  * 发现者：Liu, Richard Jiayang <rjliu3@illinois.edu>。
  * 修复开发者：Liu, Richard Jiayang <rjliu3@illinois.edu>。
  * 协调者：Arnout Engelen <engelen@apache.org>。
  * 协调者：Tomek CEDRO <cederom@apache.org>。
  * 修复审核者：Xiang Xiao <xiaoxiang@apache.org>。
  * 修复审核者：Jiuzhu Dong <jiuzhudong@apache.org>。

* 参考资料：

  * https://www.cve.org/CVERecord?id=CVE-2025-48769。
  * http://www.openwall.com/lists/oss-security/2025/12/31/11。
  * https://github.com/apache/nuttx/pull/16455。
  * https://lists.apache.org/thread/7m83v11ldfq7bvw72n9t5sccocczocjn。

在 Apache NuttX RTOS 的 fs/vfs/fs_rename 代码中发现了释放后使用漏洞，
由于递归实现和两个不同指针变量使用同一缓冲区，允许对用户提供的任意大小的缓冲区
进行重新分配并写入先前释放的堆块，在特定情况下可能导致意外的虚拟文件系统
重命名/移动操作结果。此问题影响 Apache NuttX RTOS：从 7.20 到 12.11.0 之前。
使用基于虚拟文件系统服务且具有写访问权限（尤其是通过网络暴露，如 FTP）的用户
受影响，建议升级至修复该问题的版本 12.11.0。

CVE-2025-48768
--------------

* 标题：fs/inode：fs_inoderemove 根 inode 删除。
* 发布日期：2026-01-01。
* 受影响版本：>= 10.0.0，< 12.10.0。
* 修复版本：12.10.0。
* 类型：`CWE-763 释放无效指针或引用 <https://cwe.mitre.org/data/definitions/763.html>`_。
* 致谢：

  * 发现者：Liu, Richard Jiayang <rjliu3@illinois.edu>。
  * 修复开发者：Liu, Richard Jiayang <rjliu3@illinois.edu>。
  * 协调者：Arnout Engelen <engelen@apache.org>。
  * 协调者：Tomek CEDRO <cederom@apache.org>。
  * 修复审核者：Alan Carvalho de Assis <acassis@apache.org>。
  * 修复审核者：Tomek CEDRO <cederom@apache.org>。
  * 修复审核者：Xiang Xiao <xiaoxiang@apache.org>。
  * 修复审核者：Jiuzhu Dong <jiuzhudong@apache.org>。

* 参考资料：

  * https://www.cve.org/CVERecord?id=CVE-2025-48768。
  * http://www.openwall.com/lists/oss-security/2025/12/31/10。
  * https://github.com/apache/nuttx/pull/16437。
  * https://lists.apache.org/thread/nwo1kd08b7t3dyz082q2pghdxwvxwyvo。

在 Apache NuttX RTOS 的 fs/inode/fs_inoderemove 代码中发现了释放无效指针或引用
漏洞，该漏洞允许删除根文件系统 inode，导致调试断言触发（默认禁用）、
NULL 指针解引用（根据目标架构的不同而有不同处理），或通常导致拒绝服务。
此问题影响 Apache NuttX RTOS：从 10.0.0 到 12.10.0 之前。通过网络暴露
（如 FTP）的具有写访问权限的文件系统服务用户受影响，建议升级至修复该问题的
版本 12.10.0。

CVE-2025-47869
--------------

* 标题：examples/xmlrpc：修复调用缓冲区大小。
* 发布日期：2025-06-16。
* 受影响版本：>= 6.22，< 12.9.0。
* 修复版本：12.9.0。
* 类型：`CWE-119 内存缓冲区操作限制不当 <https://cwe.mitre.org/data/definitions/119.html>`_。
* 致谢：

  * 报告者：Chánh Phạm <chanhphamviet@gmail.com>。
  * 修复开发者：Arnout Engelen <engelen@apache.org>。
  * 协调者：Arnout Engelen <engelen@apache.org>。
  * 协调者：Tomek CEDRO <cederom@apache.org>。
  * 修复审核者：Alan Carvalho de Assis <acassis@apache.org>。
  * 修复审核者：Alin Jerpelea <jerpelea@apache.org>。
  * 修复审核者：Lee, Lup Yuen <lupyuen@apache.org>。
  * 修复审核者：Xiang Xiao <xiaoxiang@apache.org>。
  * 修复审核者：Jianyu Wang <wangjianyu3@xiaomi.com>。

* 参考资料：

  * https://www.cve.org/CVERecord?id=CVE-2025-47869。
  * http://www.openwall.com/lists/oss-security/2025/06/14/2。
  * https://github.com/apache/nuttx-apps/pull/3027。
  * https://lists.apache.org/thread/306qcqyc3bpb2ozh015yxjo9kqs4jbvj。

在 Apache NuttX RTOS apps/exapmles/xmlrpc 应用中发现了内存缓冲区操作限制不当
漏洞。在该示例应用中，存储远程提供的参数的设备统计结构使用了硬编码的缓冲区大小，
可能导致缓冲区溢出。结构成员缓冲区已更新为 CONFIG_XMLRPC_STRINGSIZE+1 的有效大小。
此问题影响在 6.22 到 12.9.0 之间的发布版本中使用或基于该示例应用编写代码的
Apache NuttX RTOS 用户。建议 Apache NuttX RTOS 中的 XMLRPC 用户检查其代码中
是否存在此模式，并按照发布版本 12.9.0 中示例版本更新缓冲区大小。

CVE-2025-47868
--------------

* 标题：tools/bdf-converter：修复循环终止条件。
* 发布日期：2025-06-16。
* 受影响版本：>= 6.9，< 12.9.0。
* 修复版本：12.9.0。
* 类型：

  * `CWE-787 越界写入 <https://cwe.mitre.org/data/definitions/787.html>`_。
  * `CWE-122 堆缓冲区溢出 <https://cwe.mitre.org/data/definitions/122.html>`_。

* 致谢：

  * 发现者：Chánh Phạm <chanhphamviet@gmail.com>。
  * 修复开发者：Nathan Hartman <hartmannathan@apache.org>。
  * 协调者：Arnout Engelen <engelen@apache.org>。
  * 协调者：Tomek CEDRO <cederom@apache.org>。
  * 修复审核者：Alan Carvalho de Assis <acassis@apache.org>。
  * 修复审核者：Alin Jerpelea <jerpelea@apache.com>。
  * 修复审核者：Lee, Lup Yuen <lupyuen@apache.org>。
  * 修复审核者：Nathan Hartman <hartmannathan@apache.org>。
  * 修复审核者：Simone Falsetti <simbit18@apache.org>。

* 参考资料：

  * https://www.cve.org/CVERecord?id=CVE-2025-47868。
  * http://www.openwall.com/lists/oss-security/2025/06/14/1。
  * https://github.com/apache/nuttx/pull/16000。
  * https://lists.apache.org/thread/p4o2lcqgspx3ws1n2p4wmoqbqow1w1pw。

在 Apache NuttX RTOS 仓库中的 tools/bdf-converter 字体转换工具中发现了越界写入
导致的可能堆缓冲区溢出漏洞。该独立程序是可选的，既不是 NuttX RTOS 也不是
应用程序运行时的一部分，但当该工具暴露于外部提供的用户数据（如公开可用的自动化）
时，活跃的 bdf-converter 用户可能受到影响。此问题影响 Apache NuttX：从 6.9 到
12.9.0 之前。建议用户升级至修复该问题的版本 12.9.0。

CVE-2025-35003
--------------

* 标题：NuttX 蓝牙栈 HCI 和 UART DoS/RCE 漏洞。
* 发布日期：2025-05-26。
* 受影响版本：>= 7.25，< 12.9.0。
* 修复版本：12.9.0。
* 类型：

  * `CWE-119 内存缓冲区操作限制不当 <https://cwe.mitre.org/data/definitions/119.html>`_。
  * `CWE-121 栈缓冲区溢出 <https://cwe.mitre.org/data/definitions/121.html>`_。

* 致谢：

  * 报告者：Chongqing Lei <leicq@seu.edu.cn>。
  * 报告者：Zhen Ling <zhenling@seu.edu.cn>。
  * 修复开发者：Chongqing Lei <leicq@seu.edu.cn>。
  * 协调者：Arnout Engelen <engelen@apache.org>。
  * 协调者：Tomek CEDRO <cederom@apache.org>。
  * 修复审核者：Lee, Lup Yuen <lupyuen@apache.org>。
  * 修复审核者：Xiang Xiao <xiaoxiang@apache.org>。

* 参考资料：

  * https://www.cve.org/CVERecord?id=CVE-2025-35003。
  * http://www.openwall.com/lists/oss-security/2025/05/26/1。
  * https://github.com/apache/nuttx/pull/16179。
  * https://lists.apache.org/thread/k4xzz3jhkx48zxw9vwmqrmm4hmg78vsj。

在 Apache NuttX RTOS 蓝牙栈（HCI 和 UART 组件）中发现了内存缓冲区操作限制不当
和栈缓冲区溢出漏洞，接收恶意构造的数据包后可能导致系统崩溃、拒绝服务或
任意代码执行。建议 NuttX 蓝牙 HCI/UART 栈用户升级至修复已识别实现问题的
版本 12.9.0。

CVE-2021-34125
--------------

* 发布日期：2023-03-09。
* 受影响版本：PX4-Autopilot <= 1.11.3。
* 修复版本：

  * nuttx#016873788280ca815ba886195535bbe601de6e48。
  * nuttx-apps#2fc1157f8585acc39f13a31612ebf890f41e76ca。
  * px4-autopilot#555f900cf52c0057e4c429ff3699c91911a21cab。

* 参考资料：

  * https://www.cve.org/CVERecord?id=CVE-2021-34125。
  * https://github.com/PX4/PX4-Autopilot/issues/17062。
  * https://github.com/PX4/PX4-Autopilot/pull/17264/commits/555f900cf52c0057e4c429ff3699c91911a21cab。
  * https://www.st.com/resource/en/application_note/dm00493651-introduction-to-stm32-microcontrollers-security-stmicroelectronics.pdf。
  * https://nuttx.apache.org/。
  * https://nuttx.apache.org/docs/latest/applications/nsh/commands.html#access-memory-mb-mh-and-mw。
  * https://gist.github.com/swkim101/f473b9a60e6d4635268402a2cd2025ac。
  * https://github.com/apache/incubator-nuttx/pull/3292/commits/016873788280ca815ba886195535bbe601de6e48。
  * https://github.com/apache/incubator-nuttx-apps/pull/647/commits/2fc1157f8585acc39f13a31612ebf890f41e76ca。

在 Yuneec Mantis Q 和 PX4-Autopilot v1.11.3 及以下版本中发现了一个问题，
允许攻击者通过各种 nuttx 命令获取敏感信息。

CVE-2021-26461
--------------

* 标题：malloc、realloc 和 memalign 实现存在整数绕回漏洞。
* 发布日期：2021-06-21。
* 受影响版本：< 10.1.0。
* 修复版本：10.1.0。
* 类型：`CWE-190 整数溢出或绕回 <https://cwe.mitre.org/data/definitions/190.html>`_。
* 致谢：Apache NuttX 感谢微软公司 Azure Defender for IoT 的 Section 52 的
  Omri Ben-Bassat 将此问题告知我们。
* 参考资料：

  * https://www.cve.org/CVERecord?id=CVE-2021-26461。
  * https://lists.apache.org/thread.html/r806fccf8b003ae812d807c6c7d97950d44ed29b2713418cbe3f2bddd%40%3Cdev.nuttx.apache.org%3E。

10.1.0 之前的 Apache NuttX 版本在 malloc、realloc 和 memalign 函数中存在整数
绕回漏洞。这种不正确的内存分配可能导致任意内存分配，从而导致意外行为，
如崩溃或远程代码注入/执行。

CVE-2020-17529
--------------

* 标题：Apache NuttX（孵化中）IP 头中指定的无效分片偏移值导致越界写入。
* 发布日期：2020-12-09。
* 受影响版本：< 10.0.1。
* 修复版本：10.0.1。
* 类型：`CWE-787 越界写入 <https://cwe.mitre.org/data/definitions/787.html>`_。
* 致谢：Apache NuttX 感谢 Forescout 报告此问题。
* 参考资料：

  * https://www.cve.org/CVERecord?id=CVE-2020-17529。
  * http://www.openwall.com/lists/oss-security/2020/12/09/5。
  * https://lists.apache.org/thread.html/r4d71ae3ab96b589835b94ba7ac4cb88a704e7307bceefeab749366f3%40%3Cdev.nuttx.apache.org%3E。

Apache NuttX（孵化中）9.1.0 及以下和 10.0.0 版本的 TCP 栈中的越界写入漏洞，
允许攻击者通过提供 IP 头中指定的无效分片偏移值来损坏内存。此问题仅影响同时启用
CONFIG_EXPERIMENTAL 和 CONFIG_NET_TCP_REASSEMBLY 编译标志的构建。

CVE-2020-17528
--------------

* 标题：Apache NuttX（孵化中）TCP 紧急数据长度无效导致越界写入。
* 发布日期：2020-12-09。
* 受影响版本：< 10.0.1。
* 修复版本：10.0.1。
* 类型：`CWE-787 越界写入 <https://cwe.mitre.org/data/definitions/787.html>`_。
* 致谢：Apache NuttX 感谢 Forescout 报告此问题。
* 参考资料：

  * https://www.cve.org/CVERecord?id=CVE-2020-17528。
  * http://www.openwall.com/lists/oss-security/2020/12/09/4。
  * https://lists.apache.org/thread.html/r7f4215aba288660b41b7e731b6262c8275fa476e91e527a74d2888ea%40%3Cdev.nuttx.apache.org%3E。

Apache NuttX（孵化中）9.1.0 及以下和 10.0.0 版本 TCP 栈中的越界写入漏洞，
允许攻击者通过在 TCP 数据包内提供任意紧急数据指针偏移量（包括超出数据包长度的偏移）
来损坏内存。

CVE-2020-1939
-------------

* 发布日期：2020-05-12。
* 受影响版本：>= 6.15，<= 8.2。
* 修复版本：9.0.0。
* 参考资料：

  * https://www.cve.org/CVERecord?id=CVE-2020-1939。
  * https://lists.apache.org/thread.html/re3adc65ff4d8d9c34e5bccba3941a28cbb0a47191c150df2727e101d%40%3Cdev.nuttx.apache.org%3E。

Apache NuttX（孵化中）项目提供了一个可选的独立"apps"仓库，其中包含各种可选组件
和示例程序。其中之一的 ftpd 存在 NULL 指针解引用缺陷。NuttX RTOS 本身不受影响。
可选 apps 仓库的用户仅在启用 ftpd 时受到影响。受影响版本为 6.15 至 8.2。

CVE-2018-20578
--------------

* 发布日期：2018-12-28。
* 受影响版本：< 7.27。
* 修复版本：7.27。
* 参考资料：

  * https://www.cve.org/CVERecord?id=CVE-2018-20578。
  * https://bitbucket.org/nuttx/nuttx/issues/119/denial-of-service-infinite-loop-while。
  * https://bitbucket.org/nuttx/nuttx/downloads/nuttx-7_27-README.txt。

在 7.27 之前的 NuttX 中发现了一个问题。apps/netutils/netlib/netlib_parsehttpurl.c
中的函数 netlib_parsehttpurl() 未能正确处理超过 hostlen 字节的 URL
（在 webclient 中默认设置为 40），导致无限循环。攻击向量是 HTTP 3xx 响应的
Location 头。

