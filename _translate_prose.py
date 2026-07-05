#!/usr/bin/env python3
"""Translate prose content in NuttX platform docs from English to Chinese.
Only processes the 13 target architecture directories."""

import os
import re

DST = os.path.expanduser("~/workspace/nuttx-docs-zh/platforms")

TARGET_DIRS = [
    "z80", "mips", "renesas", "sparc", "sim", "tricore",
    "hc", "z16", "x86_64", "x86", "or1k", "misco", "ceva"
]

# Comprehensive phrase/sentence translation dictionary
# Keys are exact or near-exact matches; translations preserve RST markup
PHRASE_MAP = [
    # Common section headers (match whole lines)
    ("Supported Boards", "支持的开发板"),
    ("Supported Board", "支持的开发板"),
    ("Configurations", "配置"),
    ("Configuration", "配置"),
    ("Configuration Options", "配置选项"),
    ("Configuration Sub-Directories", "配置子目录"),
    ("Common Configuration Notes", "通用配置说明"),
    ("Features", "特性"),
    ("Installation", "安装"),
    ("Flashing", "烧录"),
    ("Flashing NuttX", "烧录 NuttX"),
    ("Toolchain", "工具链"),
    ("Toolchains", "工具链"),
    ("Tool Issues", "工具问题"),
    ("Serial Console", "串口控制台"),
    ("Serial Connection Configuration", "串口连接配置"),
    ("Debugging", "调试"),
    ("Networking", "网络"),
    ("Network Support on Linux", "Linux 上的网络支持"),
    ("Network support with VPNKit", "使用 VPNKit 的网络支持"),
    ("Overview", "概述"),
    ("Issues", "已知问题"),
    ("Limitations", "限制"),
    ("Hardware", "硬件"),
    ("Hardware setup", "硬件设置"),
    ("Hardware acceleration", "硬件加速"),
    ("LEDs", "LED 灯"),
    ("Buttons and LEDs", "按钮和 LED 灯"),
    ("On Board Debug Support", "板载调试支持"),
    ("Board Features", "开发板特性"),
    ("Pin Mapping", "引脚映射"),
    ("Memory Configuration", "内存配置"),
    ("Serial Communication", "串口通信"),
    ("Ethernet Connections", "以太网连接"),
    ("USB Device", "USB 设备"),
    ("USB Host", "USB 主机"),
    ("USB Device Configurations", "USB 设备配置"),
    ("USB Device Testing", "USB 设备测试"),
    ("USB Host Configurations", "USB 主机配置"),
    ("USB Host Driver Testing", "USB 主机驱动测试"),
    ("USB Host Hub Configurations", "USB 主机集线器配置"),
    ("USB Host Hub Driver Testing", "USB 主机集线器驱动测试"),
    ("USB Host Jumpers", "USB 主机跳线"),
    ("USB Device Jumpers", "USB 设备跳线"),
    ("RSPI Configurations", "RSPI 配置"),
    ("RSPI Testing", "RSPI 测试"),
    ("RIIC Configurations", "RIIC 配置"),
    ("RIIC Testing", "RIIC 测试"),
    ("DTC Configurations", "DTC 配置"),
    ("DTC Testing", "DTC 测试"),
    ("RTC Testing", "RTC 测试"),
    ("NuttX Configurations", "NuttX 配置"),
    ("NuttX Configuration Options", "NuttX 配置选项"),
    ("Buildroot Toolchain", "Buildroot 工具链"),
    ("Creating a bootable disk", "创建可启动磁盘"),
    ("Making the disk", "制作磁盘"),
    ("Grub with UEFI", "Grub 与 UEFI"),
    ("Real machine", "真实机器"),
    ("ROMFS", "ROMFS"),
    ("ROMFS System-Init", "ROMFS 系统初始化"),
    ("Updating the ROMFS File System", "更新 ROMFS 文件系统"),
    ("Replacing the Password File", "替换密码文件"),
    ("Architecture-Specific Directories", "架构特定目录"),
    ("Chip-Specific directories", "芯片特定目录"),
    ("Chip-Specific Directories", "芯片特定目录"),
    ("Supported Operations", "支持的操作"),
    ("Direction Control", "方向控制"),
    ("Read/Write Pin", "读写引脚"),
    ("Interrupt Configuration", "中断配置"),
    ("Interrupt Callback", "中断回调"),
    ("Host Layer API", "主机层 API"),
    ("Host Prepare", "主机准备"),
    ("Linux Kernel Version Requirements", "Linux 内核版本要求"),
    ("Usage Example", "使用示例"),
    ("Interrupt Handling", "中断处理"),
    ("Files", "相关文件"),
    ("See Also", "另请参阅"),
    ("OpenOCD", "OpenOCD"),
    ("Building the R8C/M16C/M32C GNU Toolchain Using Buildroot", "使用 Buildroot 构建 R8C/M16C/M32C GNU 工具链"),
    ("Soft Registers", "软寄存器"),
    ("FreeScale HCS12 Serial Monitor", "FreeScale HCS12 串口监视器"),
    ("Cygwin GCC BUILD NOTES", "Cygwin GCC 构建说明"),
    ("Clock source", "时钟源"),
    ("Multiboot Framebuffer", "Multiboot 帧缓冲"),
    ("Kernel build", "内核构建"),
    ("PCI bus", "PCI 总线"),
    ("Running QEMU", "运行 QEMU"),
    ("Running Bochs", "运行 Bochs"),
    ("QEMU Installation", "QEMU 安装"),
    ("Executing QEMU", "执行 QEMU"),
    ("Or1k Build", "Or1k 构建"),
    ("Qemu Build", "Qemu 构建"),
    ("Host Route Mode", "主机路由模式"),
    ("Bridge Mode", "桥接模式"),
    ("Basic Usage", "基本用法"),
    ("VPNKit setup", "VPNKit 设置"),
    ("How to run", "如何运行"),
    ("Notes", "注意事项"),
    ("Setup Script", "设置脚本"),
    ("Configuring at Startup", "启动时配置"),
    ("BASIC", "BASIC"),
    ("Configurations", "配置"),
    ("SMP", "SMP"),
    ("X11 Issues", "X11 问题"),
    ("Symbol Collisions", "符号冲突"),
    ("Networking Issues", "网络问题"),
    ("Stack Size Issues", "栈大小问题"),
    ("64-Bit Issues", "64 位问题"),
    ("Compiler differences", "编译器差异"),
    ("Cygwin64 Issues", "Cygwin64 问题"),
    ("Timing Fidelity", "时序精度"),
    ("Fake Interrupts", "伪中断"),
    ("QEMU/KVM", "QEMU/KVM"),
    ("Bochs", "Bochs"),
    ("Login test inside the simulator", "模拟器中的登录测试"),
]

# Sentence-level translations for prose paragraphs
SENTENCE_MAP = [
    # Common introductory sentences
    ("The following", "以下"),
    ("are supported:", "受支持："),
    ("is supported:", "受支持："),
    ("This port uses", "此移植使用"),
    ("This port", "此移植"),
    ("development kit", "开发套件"),
    ("development board", "开发板"),
    ("command line tools", "命令行工具"),
    ("development environment", "开发环境"),
    ("STATUS:", "状态："),
    ("STATUS", "状态"),
    ("for further information", "有关更多信息"),
    ("Refer to the NuttX board", "请参阅 NuttX 开发板"),
    ("file for further information", "文件以获取更多信息"),
    ("is a simple", "是一个简单的"),
    ("will allow you to", "将允许您"),
    ("Before using", "使用前"),
    ("copy the following files", "复制以下文件"),
    ("from the toplevel directory", "从顶层目录"),
    ("to this directory", "到此目录"),
    ("The development environment is", "开发环境为"),
    ("under Linux or Cygwin", "在 Linux 或 Cygwin 下"),
    ("under Windows", "在 Windows 下"),
    ("under WinXP", "在 WinXP 下"),
    ("This configuration", "此配置"),
    ("configuration", "配置"),
    ("This README", "此 README"),
    ("This documentation", "本文档"),
    ("This page file describes", "本页文件描述"),
    ("the contents of the build configurations available for", "可用于以下目标的构建配置内容："),
    ("NuttX port to", "NuttX 移植到"),
    ("port of NuttX to", "NuttX 移植到"),
    ("is available", "可用"),
    ("was released in", "发布于"),
    ("was contributed by", "由以下人员贡献："),
    ("was ported in", "移植于"),
    ("can be selected as follows", "可按如下方式选择"),
    ("can be configured", "可配置"),
    ("must be", "必须"),
    ("should be", "应该"),
    ("is assumed", "假设使用"),
    ("is enabled", "已启用"),
    ("is disabled", "已禁用"),
    ("is required", "必需的"),
    ("is not set", "未设置"),
    ("as mentioned below", "如下所述"),
    ("as follows", "如下"),
    ("in order to", "以便"),
    ("you can", "您可以"),
    ("you must", "您必须"),
    ("you will need to", "您需要"),
    ("you may need to", "您可能需要"),
    ("need to be", "需要"),
    ("the following", "以下"),
    ("following command", "以下命令"),
    ("the port", "此移植"),
    ("the basic port", "基本移植"),
    ("this port", "此移植"),
    ("NOTE:", "注意："),
    ("WARNING:", "警告："),
    ("Warning:", "警告："),
    ("Note:", "注意："),
]


def translate_prose_line(line):
    """Translate a single line of prose text."""
    stripped = line.strip()
    
    # Skip empty lines
    if not stripped:
        return line
    
    # Skip RST directives
    if stripped.startswith('..') and '::' in stripped:
        return line
    
    # Skip RST field lists
    if stripped.startswith(':') and ':' in stripped[1:]:
        return line
    
    # Skip title underlines
    if stripped and all(c == stripped[0] for c in stripped) and stripped[0] in '=-~^"+':
        return line
    
    # Skip code block markers
    if stripped == '::':
        return line
    
    # Skip include directives
    if '.. include::' in stripped:
        return line
    
    # Skip indented code/config lines
    indent = len(line) - len(line.lstrip())
    if indent >= 4:
        return line
    
    # Skip lines that are clearly code/commands
    if any(stripped.startswith(p) for p in [
        '$', '#!/', 'CONFIG_', 'nsh>', 'git ', 'make ', 'sudo ', 
        'cd ', 'cp ', 'mv ', 'rm ', 'mkdir ', 'export ', 'tools/',
        './tools/', 'http://', 'https://', 'ftp://', 'wget ', 'tar ',
        'qemu-', 'bochs', 'ip ', 'ifconfig', 'ping ', 'apt ',
        'setcap', 'socat', 'mount ', 'echo ', 'cat ', 'ls ',
        'adb ', 'pactl', 'grub-', 'JLinkGDBServer'
    ]):
        return line
    
    # Skip list items that are paths/code
    if stripped.startswith('* ``') or stripped.startswith('- ``'):
        return line
    
    # Skip lines that are entirely code references
    if stripped.startswith('``') and stripped.endswith('``') and len(stripped) < 80:
        return line
    
    # Apply phrase translations
    result = line
    for eng, chn in PHRASE_MAP:
        # Match as standalone words/phrases
        result = re.sub(r'\b' + re.escape(eng) + r'\b', chn, result)
    
    return result


def translate_file(filepath):
    """Translate a single file's prose content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    result = []
    in_code_block = False
    in_directive = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Track code blocks
        if stripped == '::' and not in_code_block:
            in_code_block = True
            result.append(line)
            continue
        
        if in_code_block:
            if stripped and not line[0].isspace() and not stripped.startswith('#'):
                in_code_block = False
            else:
                result.append(line)
                continue
        
        # Track directive blocks (indented content after .. directive::)
        if stripped.startswith('..') and '::' in stripped:
            in_directive = True
            result.append(line)
            continue
        
        if in_directive:
            if stripped and not line[0].isspace():
                in_directive = False
            elif stripped:
                result.append(line)
                continue
        
        # Translate prose lines
        result.append(translate_prose_line(line))
    
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
                    print(f"  translated: {rel}")
    
    print(f"\nTotal: {count} files translated")

if __name__ == '__main__':
    main()
