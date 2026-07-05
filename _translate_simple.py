#!/usr/bin/env python3
"""Write properly translated simple index files (title + toctree only).
These are files that only have a title, maybe a short description, and a toctree."""
import os

DST = os.path.expanduser("~/workspace/nuttx-docs-zh/platforms")
SRC = os.path.expanduser("~/workspace/nuttx-docs-zh/_upstream/platforms")

NOTE = "\n.. note::\n   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/\n"

# Simple index files - just title, short description, and toctree
SIMPLE_FILES = {
    "renesas/index.rst": ("Renesas", "支持以下 Renesas SoC："),
    "sparc/index.rst": ("SPARC", "支持以下 SPARC SoC："),
    "hc/index.rst": ("HC", "支持以下 HC SoC："),
    "z16/index.rst": ("Z16", "支持以下 Z16 SoC："),
    "ceva/index.rst": ("CEVA", "支持以下 CEVA DSP："),
    "misco/index.rst": ("Misoc", "支持以下 Misoc SoC："),
    "or1k/index.rst": ("OpenRISC", None),
    "sparc/s698pm/index.rst": ("S698PM", None),
    "sparc/s698pm/boards/s698pm-dkit/index.rst": ("s698pm-dkit", None),
    "sparc/bm3823/index.rst": ("BM3823", None),
    "sparc/bm3823/boards/xx3823/index.rst": ("xx3823", None),
    "sparc/bm3803/index.rst": ("BM3803", None),
    "sparc/bm3803/boards/xx3803/index.rst": ("xx3803", None),
    "ceva/xm6/index.rst": ("CEVA xm6", None),
    "ceva/xc5/index.rst": ("CEVA xc5", None),
    "x86_64/index.rst": None,  # Special handling
    "x86/index.rst": None,  # Special handling
}


def write_simple_files():
    count = 0
    for rel, info in SIMPLE_FILES.items():
        if info is None:
            continue
        title, desc = info
        # Read original to get the exact underline
        src_path = os.path.join(SRC, rel)
        if os.path.exists(src_path):
            with open(src_path, 'r') as f:
                lines = f.readlines()
            underline = lines[2].rstrip() if len(lines) > 2 else "=" * len(title)
        else:
            underline = "=" * len(title)
        
        content = f"{underline}\n{title}\n{underline}\n{NOTE}\n"
        if desc:
            content += f"\n{desc}\n"
        else:
            content += "\n"
        
        # Add toctree if original had one
        src_path = os.path.join(SRC, rel)
        if os.path.exists(src_path):
            with open(src_path, 'r') as f:
                src_content = f.read()
            if '.. toctree::' in src_content:
                # Extract toctree block
                in_toctree = False
                toctree_lines = []
                for line in src_content.split('\n'):
                    if '.. toctree::' in line:
                        in_toctree = True
                    if in_toctree:
                        toctree_lines.append(line)
                        if line.strip() and not line.strip().startswith(':') and not line.strip().startswith('..') and toctree_lines[-1] != line:
                            pass
                content += '\n'.join(toctree_lines) + '\n'
        
        dst_path = os.path.join(DST, rel)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        with open(dst_path, 'w') as f:
            f.write(content)
        count += 1
        print(f"  {rel}")
    
    return count


def main():
    count = write_simple_files()
    print(f"\nWrote {count} simple files")


if __name__ == '__main__':
    main()
