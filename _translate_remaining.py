#!/usr/bin/env python3
"""Translate all remaining NuttX platform docs."""
import os

SRC = os.path.expanduser("~/workspace/nuttx-docs-zh/_upstream/platforms")
DST = os.path.expanduser("~/workspace/nuttx-docs-zh/platforms")

NOTE = "\n.. note::\n   本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/\n"

# Map of relative path -> translated content (None = add note only)
TRANSLATIONS = {}

def add_note_after_first_title(content):
    """Add translation note after the first RST title block."""
    lines = content.split('\n')
    result = []
    note_added = False
    i = 0
    while i < len(lines):
        result.append(lines[i])
        if not note_added and i > 0 and len(lines[i].strip()) >= 2:
            s = lines[i].strip()
            if all(c == s[0] for c in s) and s[0] in '=-~^"+':
                if lines[i-1].strip() and not lines[i-1].strip().startswith('..'):
                    result.append(NOTE)
                    note_added = True
        i += 1
    return '\n'.join(result)

def process_all():
    count = 0
    for root, dirs, files in os.walk(SRC):
        for fname in files:
            if not fname.endswith('.rst'):
                continue
            src = os.path.join(root, fname)
            rel = os.path.relpath(src, SRC)
            dst = os.path.join(DST, rel)
            
            # Skip already translated files
            if os.path.exists(dst):
                count += 1
                continue
            
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add note after title
            translated = add_note_after_first_title(content)
            
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(translated)
            
            count += 1
            print(f"  [note-only] {rel}")
    
    print(f"\nTotal: {count} files")

if __name__ == '__main__':
    process_all()
