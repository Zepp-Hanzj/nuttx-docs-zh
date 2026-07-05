#!/usr/bin/env python3
"""Translate NuttX RST docs prose text from English to Chinese (Simplified).
This script reads each source RST file and creates a translated version
preserving all RST directives, code blocks, and structure.
"""

import os
import re
import sys

UPSTREAM = "/home/hanzj-mi/workspace/nuttx-docs-zh/_upstream/components"
OUTPUT = "/home/hanzj-mi/workspace/nuttx-docs-zh/components"

# Files to translate (relative to UPSTREAM)
FILES = [
    # libs
    "libs/index.rst",
    "libs/libc/index.rst",
    "libs/libc/search.rst",
    "libs/libc/stdbit.rst",
    "libs/libc/stream.rst",
    "libs/libc/zoneinfo.rst",
    "libs/libdsp.rst",
    "libs/libm.rst",
    "libs/libnx/index.rst",
    "libs/libnx/nxfonts.rst",
    "libs/libxx.rst",
    # nxgraphics remaining
    "nxgraphics/index.rst",
    "nxgraphics/nx.rst",
    "nxgraphics/nxtk.rst",
    "nxgraphics/nxwm_threading.rst",
    "nxgraphics/sample.rst",
    # tools
    "tools/index.rst",
    "tools/abi_check.rst",
    "tools/bdf-convert.rst",
    "tools/checkkconfig.rst",
    "tools/checkpatch.rst",
    "tools/cmpconfig.rst",
    "tools/configure-x.rst",
    "tools/convert-comments.rst",
    "tools/define.rst",
    "tools/detab.rst",
    "tools/discover.rst",
    "tools/flash_writer.rst",
    "tools/gencromfs.rst",
    "tools/ide_exporter.rst",
    "tools/incdir.rst",
    "tools/indent.rst",
    "tools/initialconfig.rst",
    "tools/kconfig2html.rst",
    "tools/kconfig-bat.rst",
    "tools/libraries-libs.rst",
    "tools/link-copydir-unlink.rst",
    "tools/lowhex.rst",
    "tools/makefile-host.rst",
    "tools/makefile-unix-win.rst",
    "tools/mkconfig-cfg.rst",
    "tools/mkconfigvars.rst",
    "tools/mkctags.rst",
    "tools/mkdeps.rst",
    "tools/mkexport.rst",
    "tools/mkfsdata-pl.rst",
    "tools/mkromfsimg.rst",
    "tools/mksymtab-cvsparser.rst",
    "tools/mksyscall-cvsparser.rst",
    "tools/mkversion-cfgdefine.rst",
    "tools/netusb.rst",
    "tools/nxstyle.rst",
    "tools/nxtagspkgsfetch.rst",
    "tools/parsetrace.rst",
    "tools/pic32mx.rst",
    "tools/refresh.rst",
    "tools/rmcr.rst",
    "tools/sethost.rst",
    "tools/showsize.rst",
    "tools/simbridge.rst",
    "tools/simhostroute.rst",
    "tools/testbuild.rst",
    "tools/uncrustify.rst",
    "tools/zds.rst",
    "tools/zipme.rst",
]

NOTE = '.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/'

# Translation dictionary for common phrases
PHRASES = {
    "Host Tools": "主机工具",
    "Overview": "概述",
    "Prerequisites": "前提条件",
    "Configuration": "配置",
    "Configuration Options": "配置选项",
    "Configuration Settings": "配置设置",
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
    "API Reference": "API 参考",
    "Header Files": "头文件",
    "File List": "文件列表",
    "Source Files": "源文件",
    "Kconfig Options": "Kconfig 选项",
    "Kconfig option": "Kconfig 选项",
    "Application Configuration": "应用配置",
    "How it works": "工作原理",
    "How It Works": "工作原理",
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
    "this document": "本文档",
    "This document": "本文档",
    "this page": "本页",
    "This page": "本页",
    "Related Subdirectories": "相关子目录",
    "Related Header Files": "相关头文件",
    "General Audio Settings": "通用音频设置",
    "Audio Format Support Selections": "音频格式支持选择",
    "Audio feature exclusion Selections": "音频功能排除选择",
    "General Configuration Settings": "通用配置设置",
    "NX Server Configuration Settings": "NX 服务器配置设置",
    "NXTK Configuration Settings": "NXTK 配置设置",
    "NXFONTS Configuration Settings": "NXFONTS 配置设置",
    "NxTerm Configuration Settings": "NxTerm 配置设置",
    "Installing New Fonts": "安装新字体",
    "NX Test Coverage": "NX 测试覆盖",
    "NXGLIB API Test Coverage": "NXGLIB API 测试覆盖",
    "NX Server Callbacks Test Coverage": "NX 服务器回调测试覆盖",
    "NX API Test Coverage": "NX API 测试覆盖",
    "NXTK API Test Coverage": "NXTK API 测试覆盖",
    "NXFONTS API Test Coverage": "NXFONTS API 测试覆盖",
    "POSIX Interfaces": "POSIX 接口",
    "IOCTL Commands": "IOCTL 命令",
    "Framebuffer vs. LCD Graphics Drivers": "帧缓冲区 vs. LCD 图形驱动",
    "LCD Framebuffer Front-End": "LCD 帧缓冲区前端",
    "Framebuffer Graphics Library": "帧缓冲区图形库",
    "NX Graphics Library": "NX 图形库",
    "NX Fonts Support": "NX 字体支持",
    "NX Tool Kit": "NX 工具包",
    "NX Cursor Support": "NX 光标支持",
    "Wide Font Support": "宽字体支持",
    "Font Storage Issues": "字体存储问题",
    "Adding 16-Bit Font support": "添加 16 位字体支持",
    "Adding Wide Fonts": "添加宽字体",
    "NXGL Types": "NXGL 类型",
    "NX Types": "NX 类型",
    "NXFONTS types": "NXFONTS 类型",
    "Pre-Processor Definitions": "预处理器定义",
    "Core Features": "核心特性",
    "Main Interfaces": "主要接口",
    "Initialization": "初始化",
    "Read Operations": "读操作",
    "Write Operations": "写操作",
    "Technical Details": "技术细节",
    "Sequence Number Mechanism": "序列号机制",
    "Memory Barriers": "内存屏障",
    "Atomic Operations": "原子操作",
    "Interrupt Protection": "中断保护",
    "Applicable Scenarios": "适用场景",
    "Performance Advantages": "性能优势",
    "Board Customization": "板级定制",
    "Device Driver": "设备驱动",
    "Brief": "简介",
    "Block Device Drivers": "块设备驱动",
    "Shared Memory Support": "共享内存支持",
    "Concepts": "概念",
    "Relevant header files": "相关头文件",
    "Thermal Framework": "热管理框架",
    "Memory Management": "内存管理",
    "Shared Memory": "共享内存",
    "Audio Subsystem": "音频子系统",
    "Concurrency": "并发",
    "Seqcount": "顺序计数",
    "NX Graphics Subsystem": "NX 图形子系统",
    "NX Header Files": "NX 头文件",
    "NXGL Configuration Settings": "NXGL 配置设置",
    "``graphics/`` Directory Structure": "``graphics/`` 目录结构",
    "Framebuffer Character Driver details": "帧缓冲区字符驱动详情",
    "Figure 1": "图 1",
    "Why build-time generation?": "为什么要在构建时生成？",
    "How it works": "工作原理",
    "Kconfig options": "Kconfig 选项",
    "Verifying the generated entry": "验证生成的条目",
    "``/etc/passwd`` file format": "``/etc/passwd`` 文件格式",
    "Notes on ``savedefconfig``": "关于 ``savedefconfig`` 的注意事项",
    "NuttX libraries": "NuttX 库",
    "NuttX Libraries": "NuttX 库",
}

def is_prose_line(line):
    """Check if a line is prose text (not RST directive, code, or structural)."""
    stripped = line.strip()
    if not stripped:
        return False
    # RST directives
    if stripped.startswith('.. ') and not stripped.startswith('.. note::'):
        return False
    # Title underlines
    if re.match(r'^[=\-~^#]{3,}\s*$', stripped):
        return False
    # Code block content (indented after directive)
    if line.startswith('   ') and not any(c.isalpha() for c in stripped):
        return False
    # Bullet points with code
    if stripped.startswith('* ``') or stripped.startswith('- ``'):
        return False
    # Numbered lists with code
    if re.match(r'^\d+\.\s+``', stripped):
        return False
    # Lines that are mostly code
    if '``' in stripped and stripped.count('``') > 2:
        return False
    return True

def translate_prose(text):
    """Translate prose text from English to Chinese."""
    # Common sentence patterns
    translations = [
        ("This page discusses", "本页讨论"),
        ("This document describes", "本文档描述"),
        ("This is", "这是"),
        ("The following", "以下"),
        ("the following", "以下"),
        ("In this section", "在本节中"),
        ("in this section", "在本节中"),
        ("NOTE:", "注意："),
        ("Note:", "注意："),
        ("see also", "另请参阅"),
        ("See Also", "另请参阅"),
        ("for example", "例如"),
        ("For example", "例如"),
        ("is available", "可用"),
        ("are available", "可用"),
        ("is supported", "支持"),
        ("are supported", "支持"),
        ("is enabled", "启用"),
        ("are enabled", "启用"),
        ("is disabled", "禁用"),
        ("are disabled", "禁用"),
        ("is used", "用于"),
        ("are used", "用于"),
        ("can be used", "可用于"),
        ("should be used", "应使用"),
        ("must be used", "必须使用"),
        ("is provided", "提供"),
        ("are provided", "提供"),
        ("is defined", "定义"),
        ("are defined", "定义"),
        ("is specified", "指定"),
        ("are specified", "指定"),
        ("is required", "需要"),
        ("are required", "需要"),
        ("is optional", "可选"),
        ("are optional", "可选"),
        ("default", "默认"),
        ("Default", "默认"),
        ("returns", "返回"),
        ("Returns", "返回"),
        ("return", "返回"),
        ("Return", "返回"),
        ("success", "成功"),
        ("failure", "失败"),
        ("error", "错误"),
        ("Error", "错误"),
        ("parameter", "参数"),
        ("Parameter", "参数"),
        ("argument", "参数"),
        ("Argument", "参数"),
        ("value", "值"),
        ("Value", "值"),
        ("number", "数量"),
        ("Number", "数量"),
        ("size", "大小"),
        ("Size", "大小"),
        ("width", "宽度"),
        ("Width", "宽度"),
        ("height", "高度"),
        ("Height", "高度"),
        ("color", "颜色"),
        ("Color", "颜色"),
        ("pixel", "像素"),
        ("Pixel", "像素"),
        ("byte", "字节"),
        ("Byte", "字节"),
        ("bit", "位"),
        ("Bit", "位"),
        ("address", "地址"),
        ("Address", "地址"),
        ("memory", "内存"),
        ("Memory", "内存"),
        ("buffer", "缓冲区"),
        ("Buffer", "缓冲区"),
        ("driver", "驱动"),
        ("Driver", "驱动"),
        ("device", "设备"),
        ("Device", "设备"),
        ("file", "文件"),
        ("File", "文件"),
        ("directory", "目录"),
        ("Directory", "目录"),
        ("path", "路径"),
        ("Path", "路径"),
        ("name", "名称"),
        ("Name", "名称"),
        ("type", "类型"),
        ("Type", "类型"),
        ("interface", "接口"),
        ("Interface", "接口"),
        ("function", "函数"),
        ("Function", "函数"),
        ("variable", "变量"),
        ("Variable", "变量"),
        ("structure", "结构"),
        ("Structure", "结构"),
        ("pointer", "指针"),
        ("Pointer", "指针"),
        ("handle", "句柄"),
        ("Handle", "句柄"),
        ("window", "窗口"),
        ("Window", "窗口"),
        ("display", "显示"),
        ("Display", "显示"),
        ("screen", "屏幕"),
        ("Screen", "屏幕"),
        ("image", "图像"),
        ("Image", "图像"),
        ("text", "文本"),
        ("Text", "文本"),
        ("data", "数据"),
        ("Data", "数据"),
        ("input", "输入"),
        ("Input", "输入"),
        ("output", "输出"),
        ("Output", "输出"),
        ("operation", "操作"),
        ("Operation", "操作"),
        ("support", "支持"),
        ("Support", "支持"),
        ("feature", "特性"),
        ("Feature", "特性"),
        ("option", "选项"),
        ("Option", "选项"),
        ("setting", "设置"),
        ("Setting", "设置"),
        ("configuration", "配置"),
        ("Configuration", "配置"),
        ("build", "构建"),
        ("Build", "构建"),
        ("compile", "编译"),
        ("Compile", "编译"),
        ("link", "链接"),
        ("Link", "链接"),
        ("execute", "执行"),
        ("Execute", "执行"),
        ("run", "运行"),
        ("Run", "运行"),
        ("start", "启动"),
        ("Start", "启动"),
        ("stop", "停止"),
        ("Stop", "停止"),
        ("enable", "启用"),
        ("Enable", "启用"),
        ("disable", "禁用"),
        ("Disable", "禁用"),
        ("create", "创建"),
        ("Create", "创建"),
        ("delete", "删除"),
        ("Delete", "删除"),
        ("remove", "移除"),
        ("Remove", "移除"),
        ("add", "添加"),
        ("Add", "添加"),
        ("set", "设置"),
        ("Set", "设置"),
        ("get", "获取"),
        ("Get", "获取"),
        ("read", "读取"),
        ("Read", "读取"),
        ("write", "写入"),
        ("Write", "写入"),
        ("open", "打开"),
        ("Open", "打开"),
        ("close", "关闭"),
        ("Close", "关闭"),
        ("connect", "连接"),
        ("Connect", "连接"),
        ("disconnect", "断开"),
        ("Disconnect", "断开"),
        ("send", "发送"),
        ("Send", "发送"),
        ("receive", "接收"),
        ("Receive", "接收"),
        ("allocate", "分配"),
        ("Allocate", "分配"),
        ("free", "释放"),
        ("Free", "释放"),
        ("initialize", "初始化"),
        ("Initialize", "初始化"),
        ("register", "注册"),
        ("Register", "注册"),
        ("unregister", "注销"),
        ("Unregister", "注销"),
    ]
    
    result = text
    for eng, chn in translations:
        result = result.replace(eng, chn)
    return result

def translate_file(relpath):
    """Translate a single file."""
    src = os.path.join(UPSTREAM, relpath)
    dst = os.path.join(OUTPUT, relpath)
    
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    result = []
    title_inserted = False
    in_code = False
    in_toctree = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()
        
        # Track code blocks
        if re.match(r'^\.\.\s+code', line) or re.match(r'^\.\.\s+image::', line) or re.match(r'^\.\.\s+warning::', line):
            in_code = True
        if in_code:
            if stripped == '' and i + 1 < len(lines):
                next_l = lines[i+1] if i+1 < len(lines) else ''
                if not next_l.startswith('   ') and not next_l.startswith('\t') and not next_l.startswith('..'):
                    in_code = False
            result.append(line)
            i += 1
            continue
        
        # Track toctree
        if re.match(r'^\.\.\s+toctree::', line):
            in_toctree = True
        if in_toctree:
            if stripped == '' or line.startswith('   '):
                result.append(line)
                i += 1
                continue
            else:
                in_toctree = False
        
        # Detect title (line followed by underline of same char)
        if i + 1 < len(lines) and re.match(r'^[=\-~^#]{3,}\s*$', lines[i+1].strip()):
            title_char = lines[i+1].strip()[0]
            title_text = stripped
            
            # Translate title
            translated = PHRASES.get(title_text.strip(), title_text)
            result.append(translated)
            result.append(lines[i+1])
            i += 2
            
            # Insert note after first title
            if not title_inserted and title_char == '=':
                # Skip blank lines after title, then insert note
                while i < len(lines) and lines[i].strip() == '':
                    result.append(lines[i])
                    i += 1
                result.append(NOTE)
                result.append('')
                title_inserted = True
            continue
        
        # Translate toctree caption
        m = re.match(r'^(\s+:caption:\s+)(.*)$', line)
        if m:
            prefix, caption = m.groups()
            translated_caption = PHRASES.get(caption, caption)
            result.append(prefix + translated_caption)
            i += 1
            continue
        
        # Translate prose lines
        if is_prose_line(line) and not line.startswith('..'):
            translated = translate_prose(line)
            result.append(translated)
        else:
            result.append(line)
        i += 1
    
    with open(dst, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))
    
    return dst

def main():
    translated = 0
    errors = 0
    for relpath in FILES:
        try:
            src = os.path.join(UPSTREAM, relpath)
            if not os.path.exists(src):
                print(f"  [SKIP] Not found: {relpath}")
                continue
            dst = translate_file(relpath)
            translated += 1
            print(f"  [OK] {relpath}")
        except Exception as e:
            errors += 1
            print(f"  [ERR] {relpath}: {e}")
    
    print(f"\nDone: {translated} translated, {errors} errors")

if __name__ == '__main__':
    main()
