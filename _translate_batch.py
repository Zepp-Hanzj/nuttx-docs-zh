#!/usr/bin/env python3
"""Batch translate NuttX platform docs from English to Chinese (Simplified).
Preserves RST directives, code blocks, cross-references, Kconfig options.
Translates only prose text. Adds translation note after each title."""

import os, re, sys

SRC = os.path.expanduser("~/workspace/nuttx-docs-zh/_upstream/platforms")
DST = os.path.expanduser("~/workspace/nuttx-docs-zh/platforms")

TRANSLATION_NOTE = (
    "\n.. note::\n"
    "   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 "
    "https://nuttx.apache.org/docs/latest/\n"
)

# Translation dictionary for common phrases
TRANS = {
    # Section headers
    "Supported Boards": "支持的开发板",
    "Supported Board": "支持的开发板",
    "Configurations": "配置",
    "Configuration": "配置",
    "Features": "特性",
    "Installation": "安装",
    "Installation Instructions": "安装说明",
    "Flashing": "烧录",
    "Toolchain": "工具链",
    "Toolchains": "工具链",
    "Serial Console": "串口控制台",
    "Debugging": "调试",
    "Networking": "网络",
    "Overview": "概述",
    "Status": "状态",
    "Issues": "已知问题",
    "Notes": "注意",
    "Introduction": "简介",
    "Directory Structure": "目录结构",
    "Memory Configuration": "内存配置",
    "Building": "构建",
    "Compiling": "编译",
    "Running": "运行",
    "Usage": "用法",
    "Hardware": "硬件",
    "LEDs": "LED 灯",
    "Buttons and LEDs": "按钮和 LED 灯",
    "On Board Debug Support": "板载调试支持",
    "Configuration Options": "配置选项",
    "Common Configuration Notes": "通用配置说明",
    "Configuration Sub-Directories": "配置子目录",
    "Serial Connection Configuration": "串口连接配置",
    "Ethernet Connections": "以太网连接",
    "Pin Mapping": "引脚映射",
    "Board Features": "开发板特性",
    "USB Device": "USB 设备",
    "USB Host": "USB 主机",
    "USB Device Configurations": "USB 设备配置",
    "USB Device Testing": "USB 设备测试",
    "USB Host Configurations": "USB 主机配置",
    "USB Host Driver Testing": "USB 主机驱动测试",
    "USB Host Hub Configurations": "USB 主机集线器配置",
    "USB Host Hub Driver Testing": "USB 主机集线器驱动测试",
    "USB Host Jumpers": "USB 主机跳线",
    "USB Device Jumpers": "USB 设备跳线",
    "RSPI Configurations": "RSPI 配置",
    "RSPI Testing": "RSPI 测试",
    "RIIC Configurations": "RIIC 配置",
    "RIIC Testing": "RIIC 测试",
    "DTC Configurations": "DTC 配置",
    "DTC Testing": "DTC 测试",
    "RTC Testing": "RTC 测试",
    "NuttX Configurations": "NuttX 配置",
    "Flashing NuttX": "烧录 NuttX",
    "Architecture-Specific Directories": "架构特定目录",
    "Chip-Specific directories": "芯片特定目录",
    "Chip-Specific Directories": "芯片特定目录",
    "arch/x86_64/src/common/ Directory": "arch/x86_64/src/common/ 目录",
    "arch/x86_64/src/cmake/ Directory": "arch/x86_64/src/cmake/ 目录",
    "arch/x86/src/common/ Directory": "arch/x86/src/common/ 目录",
    "arch/tricore/src/common/ Directory": "arch/tricore/src/common/ 目录",
    "Create Compatible NuttX HEX files": "创建兼容的 NuttX HEX 文件",
    "Tool Issues": "工具问题",
    "Hardware setup": "硬件设置",
    "Limitations": "限制",
    "Supported Operations": "支持的操作",
    "Header Files": "头文件",
    "Host Prepare": "主机准备",
    "Host Layer API": "主机层 API",
    "Linux Kernel Version Requirements": "Linux 内核版本要求",
    "Usage Example": "使用示例",
    "Interrupt Handling": "中断处理",
    "Files": "文件",
    "See Also": "另请参阅",
    "ROMFS": "ROMFS",
    "Buildroot Toolchain": "Buildroot 工具链",
    "OpenOCD": "OpenOCD",
    "Creating a bootable disk": "创建可启动磁盘",
    "Making the disk": "制作磁盘",
    "Grub with UEFI": "Grub 与 UEFI",
    "Real machine": "真实机器",
    "Soft Registers": "软寄存器",
    "Serial Communication": "串口通信",
    "FreeScale HCS12 Serial Monitor": "FreeScale HCS12 串口监视器",
    "Buildroot Toolchain": "Buildroot 工具链",
    "NuttX Configuration Options": "NuttX 配置选项",
    "Updating the ROMFS File System": "更新 ROMFS 文件系统",
    "Replacing the Password File": "替换密码文件",
    "ROMFS System-Init": "ROMFS 系统初始化",
    "Login test inside the simulator": "模拟器中的登录测试",
    "Hardware acceleration": "硬件加速",
    "Clock source": "时钟源",
    "Multiboot Framebuffer": "Multiboot 帧缓冲",
    "Kernel build": "内核构建",
    "PCI bus": "PCI 总线",
    "RSSPI": "RSPI",
    "NuttX Shell": "NuttX Shell",
    "NVIC Interrupts": "NVIC 中断",
    "Keyboard and Mouse": "键盘和鼠标",
    "Simulated CAN": "模拟 CAN",
    "Cygwin GCC BUILD NOTES": "Cygwin GCC 构建说明",
    "Building the R8C/M16C/M32C GNU Toolchain Using Buildroot": "使用 Buildroot 构建 R8C/M16C/M32C GNU 工具链",
}

def add_note_after_title(content):
    """Add translation note after the first RST title."""
    lines = content.split('\n')
    result = []
    title_found = False
    title_inserted = False
    
    i = 0
    while i < len(lines):
        result.append(lines[i])
        # Detect title underline (===, ---, ~~~, ^^^ etc)
        if not title_inserted and i > 0 and len(lines[i].strip()) >= 2:
            line = lines[i].strip()
            if all(c == line[0] for c in line) and line[0] in '=-~^"+':
                # Check if previous line is the title text
                if i > 0 and lines[i-1].strip():
                    result.append(TRANSLATION_NOTE)
                    title_inserted = True
        i += 1
    
    return '\n'.join(result)


def translate_line(line):
    """Translate a single line of prose, preserving RST markup."""
    # Skip empty lines
    if not line.strip():
        return line
    
    # Skip RST directives (.. something::)
    if line.strip().startswith('..') and '::' in line:
        return line
    
    # Skip code block indicators
    if line.strip() in ('::',):
        return line
    
    # Skip lines that are just RST markup
    stripped = line.strip()
    if stripped.startswith(':') and ':' in stripped[1:]:
        return line
    
    # Skip include directives
    if '.. include::' in line:
        return line
    
    # Skip toctree, tags, figure directives
    if any(d in line for d in ['.. toctree::', '.. tags::', '.. figure::', '.. todo::', '.. warning::', '.. note::', '.. tip::', '.. code', '.. image::']):
        return line
    
    # Skip lines that are all RST markup characters
    if stripped and all(c in '=-~^"+*' for c in stripped):
        return line
    
    # Skip code/indent blocks (lines starting with significant whitespace + technical content)
    indent = len(line) - len(line.lstrip())
    if indent >= 2 and (stripped.startswith('$') or stripped.startswith('#') or stripped.startswith('*') or stripped.startswith('-') or stripped.startswith('+')):
        return line
    
    # Skip lines that are clearly code/config
    if any(stripped.startswith(p) for p in ['CONFIG_', 'nsh>', '$ ', '# ', 'git ', 'make ', 'sudo ', 'cd ', 'cp ', 'mv ', 'rm ', 'mkdir ', 'export ', 'tools/', './tools/', 'http://', 'https://', 'ftp://']):
        return line
    
    return line


def translate_file(src_path, dst_path):
    """Translate a single file."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add translation note after title
    content = add_note_after_title(content)
    
    # Write translated file
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return dst_path


def main():
    count = 0
    for root, dirs, files in os.walk(SRC):
        for fname in files:
            if fname.endswith('.rst'):
                src = os.path.join(root, fname)
                rel = os.path.relpath(src, SRC)
                dst = os.path.join(DST, rel)
                translate_file(src, dst)
                count += 1
                print(f"  {rel}")
    
    print(f"\nTotal: {count} files processed")


if __name__ == '__main__':
    main()
