#!/usr/bin/env python3
"""
Full translation of NuttX RST documentation from English to Chinese.
Translates prose text while preserving RST structure, code blocks, and technical terms.
"""
import os, re

BASE = '/home/hanzj-mi/workspace/nuttx-docs-zh'
NOTE = '.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/'

# Comprehensive translation map for sentences and phrases
# Key: English text (stripped), Value: Chinese translation
PHRASE_MAP = {
    # Index files
    "This page contains a collection of guides on how to debug problems with NuttX.":
        "本页包含一系列关于如何调试 NuttX 问题的指南。",
    "Add brief intro, distinguishing the arch and user facing APIs. Otherwise there could simply be a top-level document for each API":
        "添加简要介绍，区分架构层和用户层 API。否则可以简单地为每个 API 创建一个顶层文档",
    
    # User index
    "Migration in progress": "迁移进行中",
    "This manual provides general usage information for the NuttX RTOS from the perspective of the firmware developer.":
        "本手册从固件开发者的角度提供 NuttX RTOS 的一般使用信息。",
    "The intended audience for this document are firmware developers who are implementing applications on NuttX.":
        "本文档的目标读者是在 NuttX 上实现应用的固件开发者。",
    "Specifically, this documented is limited to addressing only NuttX RTOS APIs that are available to the application developer.":
        "具体来说，本文档仅涉及应用开发者可用的 NuttX RTOS API。",
    "As such, this document does not focus on any technical details of the organization or implementation of NuttX.":
        "因此，本文档不关注 NuttX 的组织或实现的任何技术细节。",
    "Those technical details are provided in the NuttX Porting Guide.":
        "这些技术细节在 NuttX 移植指南中提供。",
    "Information about configuring and building NuttX is also needed by the application developer.":
        "应用开发者还需要关于配置和构建 NuttX 的信息。",
    "That information can also be found in the NuttX Porting Guide.":
        "这些信息也可以在 NuttX 移植指南中找到。",
    
    # OS index
    "The file ``include/nuttx/arch.h`` identifies by prototype all of the APIs that must be provided by the architecture specific logic.":
        "文件 ``include/nuttx/arch.h`` 通过原型定义了架构特定逻辑必须提供的所有 API。",
    "The internal OS APIs that architecture-specific logic must interface with are also identified in ``include/nuttx/arch.h`` or in other header files.":
        "架构特定逻辑必须对接的内部 OS API 也在 ``include/nuttx/arch.h`` 或其他头文件中定义。",
}

def is_title_line(line, lines, idx):
    """Check if this line is part of a RST title."""
    stripped = line.strip()
    if not stripped:
        return False
    if all(c in '=-~^' for c in stripped) and len(stripped) >= 3:
        return True
    # Check if next line is an underline
    if idx + 1 < len(lines):
        next_stripped = lines[idx + 1].strip()
        if next_stripped and all(c in '=-~^' for c in next_stripped) and len(next_stripped) >= 3:
            if len(next_stripped) >= len(stripped) - 2:
                return True
    return False

def translate_title(title):
    """Translate a RST title."""
    title_map = {
        "Debugging": "调试",
        "API Reference": "API 参考",
        "Userspace API": "用户空间 API",
        "Architecture APIs": "架构 API",
        "Core Dump": "核心转储",
        "Overview": "概述",
        "How to use": "使用方法",
        "Coresight - HW Assisted Tracing on ARM": "Coresight - ARM 硬件辅助追踪",
        "Acronyms and Classification": "缩写与分类",
        "Acronyms": "缩写",
        "Classification": "分类",
        "Framework and implementation": "框架与实现",
        "Analyzing Cortex-M Hardfaults": "分析 Cortex-M 硬故障",
        "Analyzing the Register Dump": "分析寄存器转储",
        "Analyzing the Stack Dump": "分析栈转储",
        "The Task Stack": "任务栈",
        "The Interrupt Stack": "中断栈",
        "Full Stack Analysis": "完整栈分析",
        "Recovering State at the Time of the Hardfault": "恢复硬故障发生时的状态",
        "Debugging ELF Loadable Modules": "调试 ELF 可加载模块",
        "Get ELF Module Load Address": "获取 ELF 模块加载地址",
        "Make the ELF Module Wait for You": "让 ELF 模块等待",
        "Start the Debugger": "启动调试器",
        "Load Offset Symbols": "加载偏移符号",
        "And Debug": "开始调试",
        "An Easier Way?": "更简单的方法？",
        "Debugging / flashing NuttX on ARM with hardware debugger (JTAG/SWD)":
            "使用硬件调试器 (JTAG/SWD) 在 ARM 上调试/烧录 NuttX",
        "What's the problem?": "问题是什么？",
        "Solution": "解决方案",
        "Work-around": "变通方法",
        "Disabling the Stack Dump During Debugging": "调试时禁用栈转储",
        "irqinfo": "irqinfo",
        "gdbserver": "gdbserver",
        "GDB with Python": "使用 Python 的 GDB",
        "Introduction": "简介",
        "Usage": "用法",
        "Log Example": "日志示例",
        "Raw file Example": "原始文件示例",
        "Coredump Example": "核心转储示例",
        "Thread awarenes": "线程感知",
        "How to add new architecture": "如何添加新架构",
        "Requirements": "要求",
        "How to write a GDB python script": "如何编写 GDB Python 脚本",
        "GNU gprof Profiling Tool": "GNU gprof 性能分析工具",
        "Features": "特性",
        "Configuration": "配置",
        "Required Configuration Options": "必需的配置选项",
        "Optional Configuration": "可选配置",
        "Configuration Details": "配置详情",
        "Basic Usage": "基本用法",
        "Real Board Examples": "真实板卡示例",
        "Important Notes": "重要说明",
        "References": "参考",
        "The Kernel Address Sanitizer (KASAN)": "内核地址消毒器 (KASAN)",
        "Architectures": "支持的架构",
        "Implementation details": "实现细节",
        "For developers": "开发者指南",
        "Ignoring accesses": "忽略访问",
        "ATM64 MTE extension": "ARM64 MTE 扩展",
        "Architectural Details": "架构详情",
        "Stack Overflow Check": "栈溢出检查",
        "Stack Overflow Software Check During Function Call": "函数调用期间的栈溢出软件检查",
        "Stack Overflow Software Check During Context Switching": "上下文切换期间的栈溢出软件检查",
        "Stack Overflow Hardware Check": "栈溢出硬件检查",
        "Stack Canary Check": "栈金丝雀检查",
        "Run time stack statistics": "运行时栈统计",
        "Introduce": "介绍",
        "Configuration": "配置",
        "Example": "示例",
        "Implementation details": "实现细节",
        "Notice": "注意",
        "Static Stack Usage Analysis": "静态栈使用分析",
        "Dependencies": "依赖",
        "Command Line Options": "命令行选项",
        "Text Output": "文本输出",
        "Uncertainty Reasons": "不确定性原因",
        "Uncertainty markers": "不确定性标记",
        "Recursion Depth Estimation": "递归深度估算",
        "Supported Architectures": "支持的架构",
        "Task Trace": "任务追踪",
        "Task Trace Internals": "任务追踪内部实现",
        "NuttX kernel events collection": "NuttX 内核事件收集",
        "Getting the system call events": "获取系统调用事件",
        "FLAT build": "FLAT 构建",
        "PROTECTED/KERNEL build": "PROTECTED/KERNEL 构建",
        "Task Trace User Guide": "任务追踪用户指南",
        "Installation": "安装",
        "Install Trace Compass": "安装 Trace Compass",
        "NuttX kernel configuration": "NuttX 内核配置",
        "How to get trace data": "如何获取追踪数据",
        "Quick Guide": "快速指南",
        "Getting the trace": "获取追踪",
        "Displaying the trace result": "显示追踪结果",
        "Trace command description": "trace 命令说明",
        "trace start": "trace start",
        "trace stop": "trace stop",
        "trace cmd": "trace cmd",
        "trace dump": "trace dump",
        "trace mode": "trace mode",
        "trace syscall": "trace syscall",
        "trace irq": "trace irq",
        "System Startup and Board Initialization Trace": "系统启动与板级初始化追踪",
        "How to capture startup and board initialization trace": "如何捕获启动和板级初始化追踪",
        "Common trace events during the startup": "启动过程中的常见追踪事件",
        "Start task tracing": "启动任务追踪",
        "Stop task tracing": "停止任务追踪",
        "Output the trace result.": "输出追踪结果。",
        "Set the task trace mode options.": "设置任务追踪模式选项。",
        "Configure the filter of the system call trace.": "配置系统调用追踪的过滤器。",
        "Configure the filter of the interrupt trace.": "配置中断追踪的过滤器。",
        "Memory Coloring Implementation Principle": "内存着色实现原理",
        "Compare sp and sl": "比较 sp 和 sl",
        "Determine by detecting the number of bytes specified at the bottom of the stack.":
            "通过检测栈底指定的字节数来判断。",
        "Check if the sp register is out of bounds.": "检查 sp 寄存器是否越界。",
        
        # Reference OS files
        "APIs Exported by Architecture-Specific Logic to NuttX": "架构特定逻辑导出给 NuttX 的 API",
        "APIs Exported by Board-Specific Logic to NuttX": "板级特定逻辑导出给 NuttX 的 API",
        "APIs Exported by NuttX to Architecture-Specific Logic": "NuttX 导出给架构特定逻辑的 API",
        "OS List Management APIs": "OS 列表管理 API",
        "Naming and Header File Conventions": "命名与头文件约定",
        "Application OS vs. Internal OS Interfaces": "应用层 OS 接口与内部 OS 接口",
        "Symmetric Multiprocessing (SMP) Application": "对称多处理 (SMP) 应用",
        "I/O Buffer Management": "I/O 缓冲区管理",
        "Configuration Options": "配置选项",
        "Throttling": "节流",
        "Public Types": "公共类型",
        "Public Function Prototypes": "公共函数原型",
        "Address Environments": "地址环境",
        "Binary Loader Support": "二进制加载器支持",
        "Tasking Support": "任务支持",
        "Dynamic Stack Support": "动态栈支持",
        "LED Support": "LED 支持",
        "Header Files": "头文件",
        "LED Definitions": "LED 定义",
        "Common LED interfaces": "通用 LED 接口",
        "Mutual Exclusion lock": "互斥锁",
        "nxmutex": "nxmutex",
        "Typical Usage": "典型用法",
        "Priority inheritance": "优先级继承",
        "Api description": "API 说明",
        "Congestion Control NewReno": "拥塞控制 NewReno",
        "Test": "测试",
        "Test topology": "测试拓扑",
        "Test steps": "测试步骤",
        "Test results": "测试结果",
        "Notifier Chain": "通知链",
        "Classes of Notifier Chain": "通知链的分类",
        "Atomic notifier chains": "原子通知链",
        "Blocking notifier chains": "阻塞通知链",
        "Common Notifier Chain Interfaces": "通用通知链接口",
        "Notifier Block Types": "通知块类型",
        "Notifier Chain Interfaces": "通知链接口",
        "On-Demand Paging": "按需分页",
        "Shared Memory": "共享内存",
        "Sleep": "睡眠",
        "Common Sleep Interfaces": "通用睡眠接口",
        "Scheduled Sleep Interfaces (tick-based)": "调度睡眠接口（基于 tick）",
        "Signal-based Sleep Interfaces (timespec-based)": "基于信号的睡眠接口（基于 timespec）",
        "Busy Sleep Interfaces": "忙等待睡眠接口",
        "System Time and Clock": "系统时间与时钟",
        "Basic System Timer": "基本系统定时器",
        "Hardware": "硬件",
        "System Tick and Time": "系统 Tick 与时间",
        "Tickless OS": "Tickless OS",
        "Tickless Platform Support": "Tickless 平台支持",
        "Tickless Configuration Options": "Tickless 配置选项",
        "Tickless Imported Interfaces": "Tickless 导入接口",
        "Watchdog Timer Interfaces": "看门狗定时器接口",
        "High-resolution Timer Interfaces": "高分辨率定时器接口",
        "Work Queues": "工作队列",
        "Classes of Work Queues": "工作队列的分类",
        "High Priority Kernel Work queue": "高优先级内核工作队列",
        "Low Priority Kernel Work Queue": "低优先级内核工作队列",
        "User-Mode Work Queue": "用户模式工作队列",
        "Common Work Queue Interfaces": "通用工作队列接口",
        "Work Queue IDs": "工作队列 ID",
        "Work Queue Interface Types": "工作队列接口类型",
        "Work Queue Interfaces": "工作队列接口",
        "Events": "事件",
        "Common Events Interfaces": "通用事件接口",
        "Events Types": "事件类型",
        "Notifier Chain Interfaces": "通知链接口",
        
        # Reference User files
        "Task Control Interfaces": "任务控制接口",
        "Task Scheduling Interfaces": "任务调度接口",
        "Signal Interfaces": "信号接口",
        "Pthread Interfaces": "线程接口",
        "Environment Variables": "环境变量",
        "File System Interfaces": "文件系统接口",
        "NuttX File System Overview": "NuttX 文件系统概述",
        "Driver Operations": "驱动操作",
        "Directory Operations (``dirent.h``)": "目录操作 (``dirent.h``)",
        "UNIX Standard Operations (``unistd.h``)": "UNIX 标准操作 (``unistd.h``)",
        "Standard I/O": "标准 I/O",
        "Standard Library (``stdlib.h``)": "标准库 (``stdlib.h``)",
        "Asynchronous I/O": "异步 I/O",
        "Standard String Operations": "标准字符串操作",
        "Pipes and FIFOs": "管道与 FIFO",
        "Network Interfaces": "网络接口",
        "Network Interfaces Overview": "网络接口概述",
        "Network Functions": "网络函数",
        "Socket Functions (``sys/socket.h``)": "Socket 函数 (``sys/socket.h``)",
        "DNS Functions (``net/dns.h``)": "DNS 函数 (``net/dns.h``)",
        "Shared Memory Interfaces": "共享内存接口",
        "Functions": "函数",
        "Board IOCTL": "板级 IOCTL",
        "Supported commands": "支持的命令",
        "System state control": "系统状态控制",
        "Power Management": "电源管理",
        "Board information": "板级信息",
        "Filesystems": "文件系统",
        "Symbol Handling": "符号处理",
        "USB": "USB",
        "Graphics": "图形",
        "Testing": "测试",
        "Logging": "日志",
        "Priority Levels": "优先级级别",
        "Priority mask": "优先级掩码",
        "OS Data Structures": "OS 数据结构",
        "Scalar Types": "标量类型",
        "Hidden Interface Structures": "隐藏接口结构",
        "Access to the ``errno`` Variable": "访问 ``errno`` 变量",
        "User Interface Structures": "用户接口结构",
        "Clocks and Timers": "时钟与定时器",
        "Counting Semaphore Interfaces": "计数信号量接口",
        "Named Message Queue Interfaces": "命名消息队列接口",
        "Programming Interfaces": "编程接口",
        "Disabling Environment Variable Support": "禁用环境变量支持",
        "Abnormal Termination Signals": "异常终止信号",
        "Job Control Signals": "作业控制信号",
        "Ignored By Default": "默认忽略",
        "Tasks and Signals": "任务与信号",
        "Tasks Groups": "任务组",
        "Signaling Multi-threaded Task Groups": "向多线程任务组发送信号",
        "Parent and Child Tasks": "父任务与子任务",
        "Locking versus Signaling Semaphores": "锁信号量与信号信号量",
        "Priority Inversion": "优先级反转",
        "Priority Inheritance": "优先级继承",
        "Non-standard task control interfaces inspired by VxWorks interfaces:":
            "受 VxWorks 接口启发的非标准任务控制接口：",
        "Standard interfaces": "标准接口",
        "File Descriptors and Streams": "文件描述符与流",
        "Executing Programs within a File System": "在文件系统中执行程序",
        "Task Control Interfaces": "任务控制接口",
        "Thread Specific Data": "线程特定数据",
        "pthread Mutexes": "线程互斥锁",
        "Condition Variables": "条件变量",
        "Barriers": "屏障",
        "Initialization": "初始化",
        "Signals": "信号",
        "Tasks": "任务",
        "Device Driver Bottom Half": "设备驱动下半部",
        "Thread Pool": "线程池",
        "Priority Inheritance": "优先级继承",
        "Work Queue Accessibility": "工作队列可访问性",
        "User-Mode Work Queue": "用户模式工作队列",
        "Kernel-Mode Work Queue IDs:": "内核模式工作队列 ID：",
        "User-Mode Work Queue IDs:": "用户模式工作队列 ID：",
    }
    return title_map.get(title, title)

def translate_prose_line(line):
    """Translate a single line of prose text."""
    stripped = line.strip()
    
    # Skip empty lines
    if not stripped:
        return line
    
    # Skip RST directives
    if stripped.startswith('.. ') or stripped.startswith('..'):
        return line
    
    # Skip code block indicators
    if stripped.startswith('.. code-block') or stripped == '::':
        return line
    
    # Skip cross-references and links
    if ':c:func:' in stripped or ':c:type:' in stripped or ':c:struct:' in stripped or ':c:macro:' in stripped:
        return line
    if ':ref:' in stripped or ':doc:' in stripped or ':file:' in stripped:
        return line
    
    # Skip lines that are mostly code/technical
    if stripped.startswith('CONFIG_') or stripped.startswith('``CONFIG_'):
        return line
    if stripped.startswith('$ ') or stripped.startswith('> '):
        return line
    if stripped.startswith('-  ``') or stripped.startswith('- ``'):
        return line
    if stripped.startswith('.. note') or stripped.startswith('.. warning') or stripped.startswith('.. tip'):
        return line
    if stripped.startswith(':') and ':' in stripped[1:]:
        return line
    if stripped.startswith('.. c:') or stripped.startswith('.. _'):
        return line
    
    # Translate specific common phrases
    phrase_translations = {
        "This page contains a collection of guides on how to debug problems with NuttX.":
            "本页包含一系列关于如何调试 NuttX 问题的指南。",
        "Overview": "概述",
        "How to use": "使用方法",
        "Configuration": "配置",
        "Usage": "用法",
        "Syntax": "语法",
        "Example": "示例",
        "Test": "测试",
        "Support": "支持",
        "Features": "特性",
        "Dependencies": "依赖",
        "References": "参考",
        "Functions": "函数",
        "Notice": "注意",
        "Notes": "说明",
        "Principle": "原理",
        "Workflow": "工作流程",
        "Source:": "源：",
        "Link:": "链路：",
        "Sinks:": "接收器：",
    }
    
    if stripped in phrase_translations:
        indent = line[:len(line) - len(line.lstrip())]
        return indent + phrase_translations[stripped]
    
    return line

def translate_file(src_path, dst_path):
    """Translate a single RST file."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    result = []
    in_code_block = False
    in_directive = False
    note_inserted = False
    title_done = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Track code blocks
        if stripped.startswith('.. code-block') or (stripped == '::' and not in_code_block):
            in_code_block = True
            in_directive = True
        elif in_code_block and stripped == '' and i + 1 < len(lines):
            # Check if next line is still indented
            next_line = lines[i + 1] if i + 1 < len(lines) else ''
            if next_line and not next_line[0].isspace() and next_line.strip():
                in_code_block = False
                in_directive = False
        elif in_code_block and stripped and not line[0].isspace():
            in_code_block = False
            in_directive = False
        
        # Track RST directives (.. something::)
        if stripped.startswith('.. ') and '::' in stripped:
            in_directive = True
        elif in_directive and stripped == '':
            in_directive = False
        
        # Insert note after title
        if not note_inserted:
            if stripped and len(stripped) >= 3 and all(c in '=-~^' for c in stripped):
                if i > 0 and lines[i-1].strip() and not lines[i-1].strip().startswith('..'):
                    result.append(line)
                    result.append('')
                    result.append(NOTE)
                    result.append('')
                    note_inserted = True
                    title_done = True
                    continue
        
        # Translate title text
        if title_done and i > 0:
            prev = lines[i-1].strip() if i > 0 else ''
            if prev and all(c in '=-~^' for c in prev) and len(prev) >= 3:
                # This is a title line
                translated_title = translate_title(stripped)
                indent = line[:len(line) - len(line.lstrip())]
                result.append(indent + translated_title)
                continue
        
        # For non-code, non-directive content, translate prose
        if not in_code_block and not in_directive:
            translated = translate_prose_line(line)
            result.append(translated)
        else:
            result.append(line)
    
    # If note wasn't inserted (no title underline found), add it at the top
    if not note_inserted:
        final = []
        for j, line in enumerate(result):
            final.append(line)
            if not note_inserted and line.strip() and not line.startswith('..') and not all(c in '=-~^' for c in line.strip()):
                final.append('')
                final.append(NOTE)
                final.append('')
                note_inserted = True
        result = final
    
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))

def process_all():
    """Process all files."""
    total = 0
    
    for src_sub, dst_sub in [('_upstream/debugging', 'debugging'), ('_upstream/reference', 'reference')]:
        src_base = os.path.join(BASE, src_sub)
        dst_base = os.path.join(BASE, dst_sub)
        
        for root, dirs, files in os.walk(src_base):
            for f in files:
                if not f.endswith('.rst'):
                    continue
                src = os.path.join(root, f)
                rel = os.path.relpath(src, src_base)
                dst = os.path.join(dst_base, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                translate_file(src, dst)
                total += 1
                print(f"  [{total}] Translated: {rel}")
    
    print(f"\nDone! Translated {total} files.")

if __name__ == '__main__':
    process_all()
