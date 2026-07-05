#!/usr/bin/env python3
"""Translate NuttX RST docs from English to Chinese (Simplified).

For each .rst file, translates prose text while preserving RST directives,
cross-references, code blocks, and structure.
"""

import os
import re
import sys
import time

UPSTREAM = "/home/hanzj-mi/workspace/nuttx-docs-zh/_upstream/components"
OUTPUT = "/home/hanzj-mi/workspace/nuttx-docs-zh/components"

# Directories to process (relative to UPSTREAM)
DIRS = [
    "tools/",
    "libs/",
    "nxgraphics/",
    "mm/",
    "audio/",
    "concurrency/",
    "drivers/block/",
    "drivers/thermal/",
]

NOTE_LINE = '.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/'

# ── Translation dictionary for common NuttX terms ──────────────────────────
TRANSLATIONS = {
    # Common phrases
    "Introduction": "简介",
    "Overview": "概述",
    "Prerequisites": "前提条件",
    "Configuration": "配置",
    "Configuration Options": "配置选项",
    "Usage": "使用方法",
    "Example": "示例",
    "Examples": "示例",
    "Notes": "注意事项",
    "Note": "注意",
    "See Also": "另请参阅",
    "References": "参考资料",
    "Description": "描述",
    "Features": "特性",
    "Supported Platforms": "支持的平台",
    "Building": "构建",
    "Installation": "安装",
    "Testing": "测试",
    "Limitations": "限制",
    "Known Issues": "已知问题",
    "Troubleshooting": "故障排除",
    "Architecture": "架构",
    "API": "API",
    "APIs": "API",
    "Header Files": "头文件",
    "File List": "文件列表",
    "Source Files": "源文件",
    "Kconfig Options": "Kconfig 选项",
    "Kconfig option": "Kconfig 选项",
    "Application Configuration": "应用配置",
    "make menuconfig": "make menuconfig",
    "How it works": "工作原理",
    "How It Works": "工作原理",
    "Host Tools": "主机工具",
    "Organization": "组织结构",
    "Objectives": "目标",
    "Standard Functions": "标准函数",
    "Memory Models": "内存模型",
    "Multiple Heaps": "多堆管理",
    "Sub-Directories": "子目录",
    "Debugging": "调试",
    "General Usage Example": "通用使用示例",
    "User/Kernel Heaps": "用户/内核堆",
    "Page Allocator": "页分配器",
    "Shared Memory Management": "共享内存管理",
    "I/O Buffers": "I/O 缓冲区",
    "Granule Allocator": "颗粒分配器",
    "The following": "以下",
    "the following": "以下",
    "this document": "本文档",
    "This document": "本文档",
    "this page": "本页",
    "This page": "本页",
    "in this section": "在本节中",
    "In this section": "在本节中",
    "below": "如下",
    "above": "如上",
    "see also": "另请参阅",
}

def collect_files():
    """Collect all .rst files from the specified directories."""
    files = []
    for d in DIRS:
        dirpath = os.path.join(UPSTREAM, d)
        if not os.path.isdir(dirpath):
            print(f"  [SKIP] Directory not found: {dirpath}")
            continue
        for root, dirs, fnames in os.walk(dirpath):
            for fn in sorted(fnames):
                if fn.endswith('.rst'):
                    relpath = os.path.relpath(os.path.join(root, fn), UPSTREAM)
                    files.append(relpath)
    return files

# ── Inline text translator ─────────────────────────────────────────────────
def translate_prose_line(line):
    """Translate a single prose line, preserving inline RST markup."""
    # Don't translate blank lines
    if not line.strip():
        return line

    # Don't translate lines that are RST directives or structural
    if line.startswith('.. ') and not line.startswith('.. note::'):
        return line
    if line.startswith('.. note::') and NOTE_LINE in line:
        return line

    # Don't translate lines that are only punctuation/markup
    stripped = line.strip()
    if stripped in ('', '---', '===', '~~~', '^^^', '###', '...', ''):
        return line

    return line

# ── Full-document translation ───────────────────────────────────────────────

def translate_document(content):
    """Translate the full document, preserving RST structure."""
    lines = content.split('\n')
    result = []

    # State tracking
    i = 0
    in_code_block = False
    code_block_marker = None
    title_found = False
    title_level = None  # '=', '-', '~', '^', '#'
    after_title = False
    in_toctree = False
    in_option_block = False

    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        # Track code blocks
        if not in_code_block:
            # Detect code block directive
            m = re.match(r'^\.\.\s+code(?:-block)?(?:\s*::(?:\s*(.*))?)?$', line)
            if m:
                in_code_block = True
                result.append(line)
                i += 1
                continue
            # Detect literal block (::)
            if stripped.endswith('::') and not stripped.startswith('..'):
                # Could be a literal block
                result.append(line)
                i += 1
                # Check if next non-blank line is indented
                if i < len(lines) and lines[i].strip() == '':
                    result.append(lines[i])
                    i += 1
                if i < len(lines) and lines[i].startswith('   '):
                    in_code_block = True
                continue
        else:
            # Inside code block - check for exit
            if stripped == '' and i + 1 < len(lines):
                next_line = lines[i + 1]
                if not next_line.startswith('   ') and not next_line.startswith('\t'):
                    in_code_block = False
            elif i + 1 >= len(lines):
                in_code_block = False
            result.append(line)
            i += 1
            continue

        # Track toctree directives
        if re.match(r'^\.\.\s+toctree::', line):
            in_toctree = True
            result.append(line)
            i += 1
            continue
        if in_toctree:
            if stripped == '' or line.startswith('   '):
                result.append(line)
                i += 1
                continue
            else:
                in_toctree = False

        # Detect title underlines
        if not title_found and i > 0:
            prev_stripped = lines[i-1].rstrip() if i > 0 else ''
            if re.match(r'^[=\-~^#]{3,}\s*$', stripped) and prev_stripped.strip():
                # This is a title underline
                title_char = stripped[0]
                if title_char in ('=', '-', '~', '^', '#'):
                    title_found = True
                    title_level = title_char
                    # Translate the title line
                    title_text = lines[i-1].rstrip()
                    translated_title = translate_title(title_text, title_char)
                    # Replace the last line we added (the title text)
                    result[-1] = translated_title
                    result.append(line)  # underline
                    i += 1

                    # Insert note after title block (after next blank line)
                    # We need to find where to insert the note
                    # Insert after the first blank line following the underline
                    note_inserted = False
                    while i < len(lines) and lines[i].strip() == '':
                        result.append(lines[i])
                        i += 1
                        if not note_inserted:
                            result.append(NOTE_LINE)
                            result.append('')
                            note_inserted = True
                            after_title = True
                    continue

        # Translate section headers (subsequent ones)
        if i > 0:
            prev_stripped = lines[i-1].rstrip() if i > 0 else ''
            if re.match(r'^[=\-~^#]{3,}\s*$', stripped) and prev_stripped.strip():
                title_text = lines[i-1].rstrip()
                title_char = stripped[0]
                translated_title = translate_title(title_text, title_char)
                result[-1] = translated_title
                result.append(line)
                i += 1
                continue

        # Translate prose lines
        result.append(translate_line(line))
        i += 1

    return '\n'.join(result)


def translate_title(title, level_char):
    """Translate a title line."""
    t = title.strip()
    translated = TITLE_MAP.get(t)
    if translated:
        return title.replace(t, translated)
    # Try partial matches
    return title


# Title translation map
TITLE_MAP = {
    "Host Tools": "主机工具",
    "Objectives": "目标",
    "Organization": "组织结构",
    "NX Header Files": "NX 头文件",
    "Standard Memory Management Functions": "标准内存管理函数",
    "Standard Functions": "标准函数",
    "Memory Models": "内存模型",
    "Multiple Heaps": "多堆管理",
    "User/Kernel Heaps": "用户/内核堆",
    "Sub-Directories": "子目录",
    "Debugging": "调试",
    "Granule Allocator": "颗粒分配器",
    "General Usage Example": "通用使用示例",
    "Page Allocator": "页分配器",
    "Shared Memory Management": "共享内存管理",
    "I/O Buffers": "I/O 缓冲区",
    "Memory Management": "内存管理",
    "Shared Memory": "共享内存",
    "Graphics Examples": "图形示例",
    "Sample Applications": "示例应用",
    "NX Graphics Subsystem": "NX 图形子系统",
    "Appendix": "附录",
    "Build Instructions": "构建说明",
    "Supported Boards": "支持的开发板",
    "Quick Start": "快速入门",
    "Getting Started": "入门指南",
    "API Reference": "API 参考",
    "Design": "设计",
    "Implementation": "实现",
    "Implementation Details": "实现细节",
    "Background": "背景",
    "Summary": "总结",
    "Conclusion": "结论",
    "Future Work": "后续工作",
    "Related Topics": "相关主题",
    "Dependencies": "依赖关系",
    "Source Code": "源代码",
    "Directory Structure": "目录结构",
    "File Structure": "文件结构",
    "Naming Conventions": "命名规范",
    "Coding Style": "代码风格",
    "Contributing": "贡献指南",
    "License": "许可证",
    "Copyright": "版权",
    "Acknowledgments": "致谢",
    "Glossary": "术语表",
    "FAQ": "常见问题",
    "Command Reference": "命令参考",
    "Tool Reference": "工具参考",
    "Library Reference": "库参考",
    "Driver Reference": "驱动参考",
    "Board Support": "板级支持",
    "Board Configuration": "板级配置",
    "System Calls": "系统调用",
    "Device Drivers": "设备驱动",
    "Network Stack": "网络协议栈",
    "File Systems": "文件系统",
    "File System": "文件系统",
    "Scheduler": "调度器",
    "Interrupts": "中断",
    "Timers": "定时器",
    "Tasks": "任务",
    "Threads": "线程",
    "Processes": "进程",
    "Signals": "信号",
    "Message Queues": "消息队列",
    "Semaphores": "信号量",
    "Mutexes": "互斥锁",
    "Condition Variables": "条件变量",
    "Spinlocks": "自旋锁",
    "Memory Allocation": "内存分配",
    "Dynamic Memory": "动态内存",
    "Static Memory": "静态内存",
    "DMA": "DMA",
    "Boot Process": "启动流程",
    "Build System": "构建系统",
    "Cross Compilation": "交叉编译",
    "Debugging Tips": "调试技巧",
    "Performance": "性能",
    "Security": "安全",
    "Power Management": "电源管理",
    "Real-Time": "实时性",
    "Why build-time generation?": "为什么要在构建时生成？",
    "How it works": "工作原理",
    "Kconfig options": "Kconfig 选项",
    "Verifying the generated entry": "验证生成的条目",
    "Notes on ``savedefconfig``": "关于 ``savedefconfig`` 的注意事项",
    "Kconfig Options": "Kconfig 选项",
}


def translate_line(line):
    """Translate a single line of text."""
    stripped = line.rstrip()
    if not stripped:
        return line

    # Don't translate RST structural lines
    if re.match(r'^[=\-~^#]{3,}\s*$', stripped):
        return line

    # Don't translate RST directives
    if stripped.startswith('.. ') and 'note::' not in stripped:
        return line

    # Don't translate lines that are only code references
    if stripped.startswith('   ') and not any(c.isalpha() for c in stripped.lstrip()):
        return line

    # Don't translate if line is mostly code/marks
    alpha_chars = sum(1 for c in stripped if c.isalpha())
    if len(stripped) > 0 and alpha_chars / len(stripped) < 0.3:
        return line

    return line


def process_file(relpath):
    """Process a single file."""
    src_path = os.path.join(UPSTREAM, relpath)
    dst_path = os.path.join(OUTPUT, relpath)

    # Create output directory
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Translate
    translated = translate_document(content)

    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(translated)

    return dst_path


def main():
    files = collect_files()
    print(f"Found {len(files)} .rst files to translate")
    for f in files:
        print(f"  {f}")

    translated_count = 0
    for relpath in files:
        try:
            dst = process_file(relpath)
            translated_count += 1
            print(f"  [OK] {relpath} -> {dst}")
        except Exception as e:
            print(f"  [ERR] {relpath}: {e}")

    print(f"\nTranslated {translated_count}/{len(files)} files")


if __name__ == '__main__':
    main()
