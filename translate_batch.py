#!/usr/bin/env python3
"""Translate NuttX docs from English to Chinese (Simplified).

Reads .rst files from _upstream/applications/{nsh,crypto,interpreters}/
and writes translated versions to applications/{nsh,crypto,interpreters}/

Strategy: Since we can't call an LLM from within the script, we use
a rule-based approach for the translation mapping. For files that are
mostly code/commands (which should stay in English), we translate only
the prose paragraphs.
"""
import os, re, sys

BASE = os.path.expanduser("~/workspace/nuttx-docs-zh")
SRC = os.path.join(BASE, "_upstream/applications")
DST = os.path.join(BASE, "applications")

# Translation dictionary for common phrases/sentences
# We'll do file-by-file manual translation in the main script instead
# This script is just a helper to copy and insert notes

def add_note_after_title(content, title_line_indices):
    """Insert the translation note after the title block."""
    lines = content.split('\n')
    note = '.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/'
    
    # Find the end of the title block (after the === overline/underline)
    # Title patterns: =====\nTitle\n===== or just Title\n=====
    i = 0
    inserted = False
    while i < len(lines):
        line = lines[i].rstrip()
        if line and all(c == '=' for c in line) and i + 1 < len(lines):
            # Check if this is an overline (next line is title text)
            if i + 2 < len(lines) and lines[i+2].rstrip() and all(c == '=' for c in lines[i+2].rstrip()):
                # Overline style: ===\nTitle\n===
                # Insert note after the closing ===
                insert_at = i + 3
                lines.insert(insert_at, '')
                lines.insert(insert_at + 1, note)
                lines.insert(insert_at + 2, '')
                inserted = True
                break
            elif i > 0 and lines[i-1].strip() and not all(c == '=' for c in lines[i-1].rstrip()):
                # Underline style: Title\n===
                insert_at = i + 1
                lines.insert(insert_at, '')
                lines.insert(insert_at + 1, note)
                lines.insert(insert_at + 2, '')
                inserted = True
                break
        i += 1
    
    if not inserted:
        # Try finding first section title
        for i in range(len(lines)):
            if i + 1 < len(lines) and lines[i+1].rstrip() and all(c == '=' for c in lines[i+1].rstrip()):
                insert_at = i + 2
                lines.insert(insert_at, '')
                lines.insert(insert_at + 1, note)
                lines.insert(insert_at + 2, '')
                inserted = True
                break
    
    return '\n'.join(lines)


def process_file(src_path, dst_path, translator=None):
    """Read source, optionally translate, add note, write to dest."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if translator:
        content = translator(content)
    else:
        content = add_note_after_title(content)
    
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Written: {dst_path}")


if __name__ == '__main__':
    # Just list files that need processing
    for subdir in ['nsh', 'crypto', 'interpreters']:
        src_dir = os.path.join(SRC, subdir)
        for root, dirs, files in os.walk(src_dir):
            for f in files:
                if f.endswith('.rst'):
                    src = os.path.join(root, f)
                    rel = os.path.relpath(src, SRC)
                    dst = os.path.join(DST, rel)
                    print(f"NEED: {rel}")
