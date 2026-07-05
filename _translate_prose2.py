#!/usr/bin/env python3
"""Translate all prose paragraphs in remaining NuttX platform docs.
Uses pattern matching for common sentences and phrases."""
import os, re

DST = os.path.expanduser("~/workspace/nuttx-docs-zh/platforms")

TARGET_DIRS = ["mips", "renesas", "sparc", "sim", "tricore", "hc", "z16", "x86_64", "x86", "or1k", "misco", "ceva"]

# Full line translations (exact match after stripping)
LINE_MAP = {
    "The following Renesas SoC are supported:": "支持以下 Renesas SoC：",
    "The following MIPS SoC are supported:": "支持以下 MIPS SoC：",
    "The following SPARC SoC are supported:": "支持以下 SPARC SoC：",
    "The following HC SoC are supported:": "支持以下 HC SoC：",
    "The following Z16 SoC are supported:": "支持以下 Z16 SoC：",
    "The following CEVA DSP are supported:": "支持以下 CEVA DSP：",
    "The following Misoc SoC are supported:": "支持以下 Misoc SoC：",
    "The following Simulator/Emulators are supported:": "支持以下模拟器/仿真器：",
    "A user-mode port of NuttX to the x86 Linux/Cygwin platform is available.": "NuttX 到 x86 Linux/Cygwin 平台的用户模式移植可用。",
    "The purpose of this port is primarily to support OS feature development.": "此移植的目的主要是支持操作系统功能开发。",
}

# Phrase replacements (order matters - longer first)
PHRASES = [
    # Status/informational
    ("**STATUS:**", "**状态：**"),
    ("**STATUS**", "**状态**"),
    ("**NOTE:**", "**注意：**"),
    ("**NOTE**", "**注意**"),
    ("**Development Environment:**", "**开发环境：**"),
    ("Refer to the NuttX board", "有关更多信息，请参阅 NuttX 开发板"),
    ("file for further information.", "文件。"),
    ("for further information.", "有关更多信息。"),
    ("for further information", "有关更多信息"),
    ("See the NuttX board", "请参阅 NuttX 开发板"),
    ("Refer to the NuttX", "请参阅 NuttX"),
    
    # Common technical phrases
    ("This port uses the", "此移植使用"),
    ("This port uses", "此移植使用"),
    ("This port use the", "此移植使用"),
    ("This port", "此移植"),
    ("the port", "此移植"),
    ("development kit", "开发套件"),
    ("development board", "开发板"),
    ("command line tools", "命令行工具"),
    ("development environment", "开发环境"),
    ("The development environment is", "开发环境为"),
    ("is a simple", "是一个简单的"),
    ("will allow you to", "将允许您"),
    ("Before using, copy the following files", "使用前，请复制以下文件"),
    ("from the toplevel directory", "从顶层目录"),
    ("to this directory", "到此目录"),
    ("as described above", "如上所述"),
    ("This README", "此 README"),
    ("This documentation", "本文档"),
    ("This page file describes", "本页文件描述"),
    ("port of NuttX to", "NuttX 移植到"),
    ("NuttX port to", "NuttX 移植到"),
    ("architectural support for the", "架构支持，适用于"),
    ("Architectural support for the", "架构支持，适用于"),
    ("was contributed by", "由以下人员贡献："),
    ("was released in", "发布于"),
    ("was ported in", "移植于"),
    ("in NuttX version", "在 NuttX 版本"),
    ("in NuttX-", "在 NuttX-"),
    ("NuttX version", "NuttX 版本"),
    
    # Board descriptions
    ("This board features the", "此开发板搭载"),
    ("This board configuration", "此开发板配置"),
    ("Board Features", "开发板特性"),
    ("board features", "开发板特性"),
    
    # Microcontroller descriptions
    ("Microcontroller.", "微控制器。"),
    ("Microcontroller", "微控制器"),
    
    # Common verbs
    ("is available", "可用"),
    ("is supported", "受支持"),
    ("are supported", "受支持"),
    ("is in progress", "进行中"),
    ("is complete", "已完成"),
    ("is enabled", "已启用"),
    ("is disabled", "已禁用"),
    ("is required", "必需的"),
    ("is not set", "未设置"),
    ("can be selected as follows", "可按如下方式选择"),
    ("can be configured", "可配置"),
    ("can be used", "可使用"),
    ("must be", "必须"),
    ("should be", "应该"),
    ("has been tested", "已测试"),
    ("has been verified", "已验证"),
    ("has been completed", "已完成"),
    ("has been contributed", "已贡献"),
    
    # Configuration/testing
    ("This configuration", "此配置"),
    ("the configuration", "配置"),
    ("the following configurations", "以下配置"),
    ("following configurations", "以下配置"),
    ("need to be enabled", "需要启用"),
    ("configurations need to be enabled", "配置需要启用"),
    ("The following testing is executed", "执行以下测试"),
    ("The following can be used", "以下可用"),
    ("Following command can be used", "可使用以下命令"),
    ("where b is bus number", "其中 b 是总线编号"),
    ("where b is bus number and x is number of words to exchange.", "其中 b 是总线编号，x 是要交换的字数。"),
    
    # Common phrases in board docs
    ("The P112", "P112"),
    ("the NuttX board", "NuttX 开发板"),
    ("the NuttX", "NuttX"),
    ("NuttX configurations for", "NuttX 配置，适用于"),
    ("NuttX configurations", "NuttX 配置"),
    ("issues unique to", "特有的问题"),
    ("This README discusses", "此 README 讨论"),
    ("discusses issues unique to", "讨论以下特有的问题"),
    ("for more information about the chip", "有关芯片的更多信息"),
    ("this board uses.", "此开发板使用的。"),
    
    # Installation/build
    ("A GNU GCC-based toolchain is assumed.", "假设使用基于 GNU GCC 的工具链。"),
    ("The PATH environment variable should be", "PATH 环境变量应该"),
    ("modified to point to the correct path", "修改为指向正确的路径"),
    ("If you have no", "如果您没有"),
    ("one can be downloaded from", "可以从以下地址下载"),
    ("You must have already configured NuttX", "您必须已经配置了 NuttX"),
    ("Download the latest", "下载最新的"),
    ("Make sure that the", "确保"),
    ("Make sure that", "确保"),
    ("includes the path to the newly built", "包含新构建的"),
    ("binaries.", "二进制文件的路径。"),
    ("You can use the following command", "您可以使用以下命令"),
    ("to configure the NuttX build", "来配置 NuttX 构建"),
    ("where ``<config>`` is one of the configurations listed below", "其中 ``<config>`` 是下面列出的配置之一"),
    
    # Connection descriptions
    ("This board needs to be connected to", "此开发板需要连接到"),
    ("using USB cable", "使用 USB 线缆"),
    ("connected to PC", "连接到 PC"),
    ("USB Serial port", "USB 串口"),
    ("needs to be downloaded on PC side.", "需要在 PC 端下载。"),
    ("Configure Teraterm to", "配置 Teraterm 为"),
    ("baud.", "波特率。"),
    
    # Common testing phrases
    ("The characters typed from the keyboard were executed correctly.", "从键盘输入的字符被正确执行。"),
    ("The output of the commands mentioned above should be seen on", "上述命令的输出应在以下位置可见："),
    ("is enumerated as", "枚举为"),
    ("in ``/dev`` directory.", "在 ``/dev`` 目录中。"),
    ("The block device is mounted using the command as mentioned below:", "使用以下命令挂载块设备："),
    ("The MSC device is mounted", "MSC 设备已挂载"),
    ("The copy command is executed to test the Read/Write functionality", "执行复制命令以测试读写功能"),
    
    # Generic
    ("NuttX-12.10.0", "NuttX-12.10.0"),
    ("NuttX-8.2", "NuttX-8.2"),
    ("NuttX-9.0", "NuttX-9.0"),
    ("NuttX-7.9", "NuttX-7.9"),
    ("NuttX-7.29", "NuttX-7.29"),
    ("NuttX-7.31", "NuttX-7.31"),
    ("NuttX-7.24", "NuttX-7.24"),
    ("NuttX-7.25", "NuttX-7.25"),
    ("NuttX-7.19", "NuttX-7.19"),
    ("NuttX-7.2", "NuttX-7.2"),
    ("NuttX-6.33", "NuttX-6.33"),
    ("NuttX-5.19", "NuttX-5.19"),
    ("NuttX-6.0", "NuttX-6.0"),
    ("NuttX-12.0", "NuttX-12.0"),
]


def translate_line(line):
    """Translate a single line."""
    stripped = line.strip()
    
    # Skip empty, RST directives, code, underlines
    if not stripped:
        return line
    if stripped.startswith('..') and '::' in stripped:
        return line
    if stripped.startswith(':') and ':' in stripped[1:]:
        return line
    if stripped == '::':
        return line
    if '.. include::' in stripped:
        return line
    if stripped and all(c == stripped[0] for c in stripped) and stripped[0] in '=-~^"+':
        return line
    
    # Skip indented content (code blocks, directives)
    indent = len(line) - len(line.lstrip())
    if indent >= 4:
        return line
    
    # Skip code/command lines
    if any(stripped.startswith(p) for p in [
        '$', '#!/', 'CONFIG_', 'nsh>', 'git ', 'make ', 'sudo ',
        'cd ', 'cp ', 'mv ', 'rm ', 'mkdir ', 'export ', 'tools/',
        './tools/', 'http://', 'https://', 'ftp://', 'wget ', 'tar ',
        'qemu-', 'bochs', 'ip ', 'ifconfig', 'ping ', 'apt ',
        'setcap', 'socat', 'mount ', 'echo ', 'cat ', 'ls ',
        'adb ', 'pactl', 'grub-', 'JLinkGDBServer', '- ',
        '#', 'ifeq', 'endif', '@echo', '$(Q)', '$(OBJCOPY)',
    ]):
        return line
    
    # Skip lines that are mostly code references
    if stripped.startswith('``') and '``' in stripped[2:]:
        # But translate the surrounding text
        pass
    
    # Check exact line match
    if stripped in LINE_MAP:
        indent_str = line[:len(line)-len(line.lstrip())]
        return indent_str + LINE_MAP[stripped] + '\n' if line.endswith('\n') else indent_str + LINE_MAP[stripped]
    
    # Apply phrase replacements
    result = line
    for eng, chn in PHRASES:
        if eng in result:
            result = result.replace(eng, chn, 1)
    
    return result


def translate_file(filepath):
    """Translate all prose in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    result = []
    in_code = False
    
    for line in lines:
        stripped = line.strip()
        
        # Track code blocks
        if stripped == '::' and not in_code:
            in_code = True
            result.append(line)
            continue
        if in_code:
            if stripped and not line[0].isspace() and not stripped.startswith('#'):
                in_code = False
            else:
                result.append(line)
                continue
        
        result.append(translate_line(line))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(result)


def main():
    count = 0
    for arch_dir in TARGET_DIRS:
        arch_path = os.path.join(DST, arch_dir)
        if not os.path.isdir(arch_path):
            continue
        for root, dirs, files in os.walk(arch_path):
            for fname in files:
                if fname.endswith('.rst'):
                    fpath = os.path.join(root, fname)
                    translate_file(fpath)
                    rel = os.path.relpath(fpath, DST)
                    count += 1
                    print(f"  {rel}")
    
    print(f"\nTotal: {count} files")


if __name__ == '__main__':
    main()
