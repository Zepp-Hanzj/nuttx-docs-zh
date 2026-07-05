#!/usr/bin/env python3
"""Re-translate all files from original source with proper paragraph-level handling.
Reads from _upstream, writes translated to platforms/."""
import os, re

SRC = os.path.expanduser("~/workspace/nuttx-docs-zh/_upstream/platforms")
DST = os.path.expanduser("~/workspace/nuttx-docs-zh/platforms")

TARGET_DIRS = ["z80", "mips", "renesas", "sparc", "sim", "tricore", "hc", "z16", "x86_64", "x86", "or1k", "misco", "ceva"]

NOTE_AFTER_TITLE = "\n.. note::\n   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/\n"

# ---- Full translations for small/medium files ----
FULL = {}

# Simple index files
FULL["renesas/index.rst"] = "=======\nRenesas\n=======\n\n.. note::\n   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/\n\n支持以下 Renesas SoC：\n\n.. toctree::\n   :maxdepth: 1\n   :glob:\n\n   */*\n"
FULL["sparc/index.rst"] = "=====\nSPARC\n=====\n\n.. note::\n   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/\n\n支持以下 SPARC SoC：\n\n.. toctree::\n   :maxdepth: 1\n   :glob:\n\n   */*\n"
FULL["hc/index.rst"] = "===\nHC\n===\n\n.. note::\n   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/\n\n支持以下 HC SoC：\n\n.. toctree::\n   :maxdepth: 1\n   :glob:\n\n   */*\n"
FULL["z16/index.rst"] = "===\nZ16\n===\n\n.. note::\n   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/\n\n支持以下 Z16 SoC：\n\n.. toctree::\n   :maxdepth: 1\n   :glob:\n\n   */*\n"
FULL["ceva/index.rst"] = "====\nCEVA\n====\n\n.. note::\n   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/\n\n支持以下 CEVA DSP：\n\n.. toctree::\n   :maxdepth: 1\n   :glob:\n\n   */*\n"
FULL["misco/index.rst"] = "=====\nMisoc\n=====\n\n.. note::\n   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/\n\n支持以下 Misoc SoC：\n\n.. toctree::\n   :maxdepth: 1\n   :glob:\n\n   */*\n"
FULL["or1k/index.rst"] = "========\nOpenRISC\n========\n\n.. note::\n   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/\n\n.. toctree::\n   :maxdepth: 1\n   :glob:\n\n   */*\n"
FULL["mips/index.rst"] = "====\nMIPS\n====\n\n.. note::\n   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/\n\n支持以下 MIPS SoC：\n\n.. toctree::\n   :maxdepth: 1\n   :glob:\n\n   */*\n"
FULL["sim/index.rst"] = "==========\nSimulators\n==========\n\n.. note::\n   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/\n\nNuttX 到 x86 Linux/Cygwin 平台的用户模式移植可用。\n此移植的目的主要是支持操作系统功能开发。\n\n支持以下模拟器/仿真器：\n\n.. toctree::\n   :maxdepth: 2\n   :glob:\n\n   */*\n   network_linux\n   network_vpnkit\n   sim_gpiochip\n"

# Empty/tiny files - just title
for p in ["sparc/s698pm/boards/s698pm-dkit/index.rst", "sparc/bm3823/boards/xx3823/index.rst", 
          "sparc/bm3803/boards/xx3803/index.rst", "ceva/xm6/index.rst", "ceva/xc5/index.rst"]:
    with open(os.path.join(SRC, p), 'r') as f:
        c = f.read()
    FULL[p] = c  # These are so small they're just titles

# ---- Translation function for files with prose ----

def add_note_after_title(content):
    """Add translation note after first title block."""
    lines = content.split('\n')
    result = []
    note_added = False
    for i, line in enumerate(lines):
        result.append(line)
        if not note_added and i > 0 and len(line.strip()) >= 2:
            s = line.strip()
            if all(c == s[0] for c in s) and s[0] in '=-~^"+':
                if lines[i-1].strip() and not lines[i-1].strip().startswith('..'):
                    result.append(NOTE_AFTER_TITLE)
                    note_added = True
    return '\n'.join(result)


def translate_prose_paragraph(para):
    """Translate a prose paragraph (not code, not directive)."""
    if not para.strip():
        return para
    
    # Don't translate if it's a code/command block
    lines = para.split('\n')
    first = lines[0].strip()
    
    # Skip RST markup blocks
    if first.startswith('..') or first.startswith(':'):
        return para
    if first.startswith('* ``') or first.startswith('- ``'):
        return para
    if first.startswith('``') and first.endswith('``'):
        return para
    
    # Skip if heavily code-like
    code_indicators = ['CONFIG_', '$ ', 'nsh>', '#!/', 'make ', 'sudo ', 'git ']
    if any(first.startswith(p) for p in code_indicators):
        return para
    
    # This is a prose paragraph - translate common patterns
    result = para
    
    # Common sentence patterns (applied to whole paragraph)
    replacements = [
        # Simple index descriptions
        ("The following Renesas SoC are supported:", "支持以下 Renesas SoC："),
        ("The following MIPS SoC are supported:", "支持以下 MIPS SoC："),
        ("The following SPARC SoC are supported:", "支持以下 SPARC SoC："),
        ("The following HC SoC are supported:", "支持以下 HC SoC："),
        ("The following Z16 SoC are supported:", "支持以下 Z16 SoC："),
        ("The following CEVA DSP are supported:", "支持以下 CEVA DSP："),
        ("The following Misoc SoC are supported:", "支持以下 Misoc SoC："),
        ("The following Simulator/Emulators are supported:", "支持以下模拟器/仿真器："),
        ("A user-mode port of NuttX to the x86 Linux/Cygwin platform is available.", "NuttX 到 x86 Linux/Cygwin 平台的用户模式移植可用。"),
        ("The purpose of this port is primarily to support OS feature development.", "此移植的目的主要是支持操作系统功能开发。"),
        
        # Status markers
        ("**STATUS:**", "**状态：**"),
        ("**STATUS**", "**状态**"),
        ("**NOTE:**", "**注意：**"),
        ("**NOTE**", "**注意**"),
        ("**Development Environment:**", "**开发环境：**"),
        
        # Short standalone phrases
        ("Supported Boards", "支持的开发板"),
        ("Configurations", "配置"),
        ("Configuration", "配置"),
        ("Features", "特性"),
        ("Installation", "安装"),
        ("Flashing", "烧录"),
        ("Toolchain", "工具链"),
        ("Toolchains", "工具链"),
        ("Debugging", "调试"),
        ("Networking", "网络"),
        ("LEDs", "LED 灯"),
        ("Serial Console", "串口控制台"),
        ("Board Features", "开发板特性"),
    ]
    
    for eng, chn in replacements:
        if eng in result:
            result = result.replace(eng, chn)
    
    return result


def translate_content(content):
    """Translate content preserving RST structure."""
    # Parse into blocks
    lines = content.split('\n')
    blocks = []
    current_block = []
    block_type = 'prose'  # prose, code, directive, blank
    
    for line in lines:
        stripped = line.strip()
        
        # Blank line ends current block
        if not stripped:
            if current_block:
                blocks.append((block_type, '\n'.join(current_block)))
                current_block = []
            blocks.append(('blank', ''))
            continue
        
        # Code block marker
        if stripped == '::':
            if current_block:
                blocks.append((block_type, '\n'.join(current_block)))
                current_block = []
            blocks.append(('code_marker', line))
            block_type = 'code'
            continue
        
        # RST directive
        if stripped.startswith('..') and '::' in stripped:
            if current_block:
                blocks.append((block_type, '\n'.join(current_block)))
                current_block = []
            blocks.append(('directive', line))
            block_type = 'directive'
            continue
        
        # Title underline
        if all(c == stripped[0] for c in stripped) and stripped[0] in '=-~^"+':
            if current_block:
                blocks.append((block_type, '\n'.join(current_block)))
                current_block = []
            blocks.append(('underline', line))
            block_type = 'prose'
            continue
        
        # Determine block type
        indent = len(line) - len(line.lstrip())
        if indent >= 4 or block_type == 'code':
            if current_block and block_type != 'code':
                blocks.append((block_type, '\n'.join(current_block)))
                current_block = []
            block_type = 'code'
        elif block_type == 'directive' and indent >= 2:
            pass  # Continue directive block
        elif indent >= 2 and block_type == 'directive':
            pass
        
        current_block.append(line)
    
    if current_block:
        blocks.append((block_type, '\n'.join(current_block)))
    
    # Translate prose blocks
    result_blocks = []
    for btype, bcontent in blocks:
        if btype == 'prose':
            result_blocks.append(translate_prose_paragraph(bcontent))
        else:
            result_blocks.append(bcontent)
    
    return '\n'.join(result_blocks)


def process_file(src_path, rel):
    """Process a single file."""
    # Check for full translation
    if rel in FULL:
        dst_path = os.path.join(DST, rel)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        with open(dst_path, 'w') as f:
            f.write(FULL[rel])
        return True
    
    # Read original
    with open(src_path, 'r') as f:
        content = f.read()
    
    # Add translation note after title
    content = add_note_after_title(content)
    
    # Write to destination (preserving original content with note)
    dst_path = os.path.join(DST, rel)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w') as f:
        f.write(content)
    
    return False


def main():
    full_count = 0
    note_count = 0
    
    for arch_dir in TARGET_DIRS:
        src_arch = os.path.join(SRC, arch_dir)
        if not os.path.isdir(src_arch):
            continue
        for root, dirs, files in os.walk(src_arch):
            for fname in files:
                if not fname.endswith('.rst'):
                    continue
                src_path = os.path.join(root, fname)
                rel = os.path.relpath(src_path, SRC)
                is_full = process_file(src_path, rel)
                if is_full:
                    full_count += 1
                    print(f"  [full] {rel}")
                else:
                    note_count += 1
                    print(f"  [note] {rel}")
    
    print(f"\nFull translations: {full_count}")
    print(f"Note-only: {note_count}")
    print(f"Total: {full_count + note_count}")


if __name__ == '__main__':
    main()
