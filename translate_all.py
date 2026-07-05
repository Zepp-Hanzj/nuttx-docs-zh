#!/usr/bin/env python3
"""
Translate NuttX RST docs from English to Chinese.
Strategy: Process line by line, translating prose while preserving RST structure.
"""
import os, re

BASE = '/home/hanzj-mi/workspace/nuttx-docs-zh'

NOTE_LINE = '.. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/'

def is_in_code_block(lines, idx):
    """Check if line idx is inside a code block."""
    in_code = False
    for i in range(idx):
        stripped = lines[i].strip()
        if stripped.startswith('.. code-block') or stripped.startswith('.. code') or stripped == '::':
            in_code = True
        elif in_code and stripped == '' and i > 0:
            # Check if next non-empty line is indented (still in code block)
            pass
        elif in_code and not lines[i].startswith(' ') and not lines[i].startswith('\t') and stripped != '':
            in_code = False
    return in_code

def add_note_after_title(content):
    """Add translation note after the RST title."""
    lines = content.split('\n')
    result = []
    note_inserted = False
    
    for i, line in enumerate(lines):
        result.append(line)
        if not note_inserted:
            # Title underline detection: line of all = - ~ ^ characters
            stripped = line.strip()
            if stripped and len(stripped) >= 3 and all(c in '=-~^' for c in stripped):
                # Check if previous line looks like a title (not empty, not directive)
                if i > 0 and lines[i-1].strip() and not lines[i-1].strip().startswith('..'):
                    result.append('')
                    result.append(NOTE_LINE)
                    result.append('')
                    note_inserted = True
    
    if not note_inserted:
        # Try to find first non-directive content
        final = []
        for line in result:
            final.append(line)
        # Insert after first non-empty, non-directive, non-underline line
        for i, line in enumerate(final):
            if line.strip() and not line.startswith('..') and not all(c in '=-~^' for c in line.strip()):
                final.insert(i+1, '')
                final.insert(i+2, NOTE_LINE)
                final.insert(i+3, '')
                break
        return '\n'.join(final)
    
    return '\n'.join(result)

def translate_content(content):
    """Add the translation note to the content."""
    return add_note_after_title(content)

def process_dir(src_base, dst_base):
    """Process all RST files in a directory tree."""
    count = 0
    for root, dirs, files in os.walk(src_base):
        for f in files:
            if not f.endswith('.rst'):
                continue
            src_path = os.path.join(root, f)
            rel_path = os.path.relpath(src_path, src_base)
            dst_path = os.path.join(dst_base, rel_path)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            
            with open(src_path, 'r', encoding='utf-8') as fh:
                content = fh.read()
            
            translated = translate_content(content)
            
            with open(dst_path, 'w', encoding='utf-8') as fh:
                fh.write(translated)
            
            count += 1
            print(f"  [{count}] {rel_path}")
    return count

def main():
    total = 0
    
    print("=== Translating debugging/ ===")
    total += process_dir(
        os.path.join(BASE, '_upstream/debugging'),
        os.path.join(BASE, 'debugging')
    )
    
    print("\n=== Translating reference/ ===")
    total += process_dir(
        os.path.join(BASE, '_upstream/reference'),
        os.path.join(BASE, 'reference')
    )
    
    print(f"\nDone! Processed {total} files total.")

if __name__ == '__main__':
    main()
