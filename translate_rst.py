#!/usr/bin/env python3
"""Translate NuttX RST docs from English to Chinese using Google Translate.

Preserves all RST directives, cross-references, code blocks, and structure.
Translates only prose text. Keeps code, commands, paths, variable names,
Kconfig options in English.
"""

import os
import re
import sys
import time
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='en', target='zh-CN')

UPSTREAM = os.path.expanduser("~/workspace/nuttx-docs-zh/_upstream")
TARGET = os.path.expanduser("~/workspace/nuttx-docs-zh")

TRANSLATE_NOTE = ".. note:: 本文档翻译自 NuttX 官方文档，如需查阅最新版本请访问 https://nuttx.apache.org/docs/latest/"

def translate_text(text):
    """Translate English text to Chinese, with rate limiting."""
    if not text or not text.strip():
        return text
    try:
        result = translator.translate(text)
        return result if result else text
    except Exception as e:
        print(f"  [WARN] Translation error: {e}")
        time.sleep(2)
        try:
            result = translator.translate(text)
            return result if result else text
        except:
            return text

def is_rst_directive(line):
    """Check if line is an RST directive."""
    stripped = line.strip()
    return stripped.startswith('.. ') and '::' in stripped

def is_title_underline(lines, i):
    """Check if line i is a title underline."""
    line = lines[i].rstrip()
    if not line or len(line) < 2:
        return False
    # Must be all same character from set of title chars
    if not all(c == line[0] for c in line):
        return False
    if line[0] not in '=-~^"#*+':
        return False
    # Previous line must be non-empty text
    if i > 0 and lines[i-1].strip():
        return True
    return False

def translate_rst_file(src_path, dst_path):
    """Translate a single RST file."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    result = []
    i = 0
    note_inserted = False
    in_code_block = False
    code_block_indent = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()
        stripped_content = stripped.strip()
        
        # ── Handle code blocks ──
        if is_rst_directive(stripped) and (
            'code-block' in stripped or 
            stripped.startswith('.. code::') or
            stripped.startswith('.. code-block::')
        ):
            in_code_block = True
            # Calculate indent for code content (usually 3 spaces after directive)
            base_indent = len(line) - len(line.lstrip())
            code_block_indent = base_indent + 3
            result.append(line)
            i += 1
            continue
        
        if in_code_block:
            if stripped_content == '':
                result.append(line)
                i += 1
                continue
            line_indent = len(line) - len(line.lstrip())
            if line_indent >= code_block_indent:
                result.append(line)
                i += 1
                continue
            else:
                in_code_block = False
        
        # ── Handle toctree and other directives with content ──
        if is_rst_directive(stripped):
            result.append(line)
            i += 1
            # Consume directive options and content (indented lines)
            while i < len(lines):
                next_line = lines[i]
                next_stripped = next_line.strip()
                if next_stripped == '':
                    result.append(next_line)
                    i += 1
                    # Check if next non-empty line is still indented content
                    if i < len(lines) and lines[i].strip():
                        next_indent = len(lines[i]) - len(lines[i].lstrip())
                        ref_indent = len(line) - len(line.lstrip())
                        if next_indent > ref_indent:
                            continue
                    break
                elif next_line.startswith('   ') or next_line.startswith('\t'):
                    result.append(next_line)
                    i += 1
                elif next_stripped.startswith(':'):
                    result.append(next_line)
                    i += 1
                else:
                    break
            continue
        
        # ── Handle title underlines ──
        if is_title_underline(lines, i):
            title_line = lines[i-1] if i > 0 else ''
            underline = lines[i]
            
            # Translate the title
            title_content = title_line.strip()
            if title_content:
                translated_title = translate_text(title_content)
                # Preserve the original underline length (adjust if needed)
                title_indent = title_line[:len(title_line) - len(title_line.lstrip())]
                result_line = title_indent + translated_title
                # Replace the previous line (title) with translated version
                result[-1] = result_line
                # Keep underline same length as translated title
                new_underline = underline[0] * len(translated_title.encode('utf-8'))
                # Actually use the character count for underline
                new_underline = underline[0] * len(result_line)
                result.append(new_underline)
            else:
                result.append(underline)
            
            # Insert translation note after title
            if not note_inserted:
                result.append('')
                result.append(TRANSLATE_NOTE)
                note_inserted = True
            
            i += 1
            continue
        
        # ── Handle regular prose lines ──
        if stripped_content and not stripped_content.startswith('.. '):
            # Check if it's a list item with inline code
            # Translate the prose parts while preserving inline markup
            
            # Simple heuristic: if line has mostly code/config, don't translate
            # Count backtick-enclosed segments
            backtick_count = stripped_content.count('``')
            total_len = len(stripped_content)
            
            # If more than 60% is code, skip translation
            code_chars = 0
            for m in re.finditer(r'``[^`]+``', stripped_content):
                code_chars += len(m.group())
            
            if total_len > 0 and code_chars / total_len > 0.6:
                result.append(line)
            elif stripped_content.startswith('.. ') or stripped_content.startswith(':'):
                result.append(line)
            else:
                # Translate this line
                indent = line[:len(line) - len(line.lstrip())]
                translated = translate_text(stripped_content)
                result.append(indent + translated)
        else:
            result.append(line)
        
        i += 1
    
    # Write output
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))


def main():
    dirs = [
        "components/tools/",
        "components/libs/",
        "components/nxgraphics/",
        "components/mm/",
        "components/arch/",
        "components/audio/",
        "components/concurrency/",
        "components/drivers/block/",
        "components/drivers/thermal/",
    ]
    
    files = []
    for d in dirs:
        full_dir = os.path.join(UPSTREAM, d)
        if os.path.exists(full_dir):
            for root, _, filenames in os.walk(full_dir):
                for fn in filenames:
                    if fn.endswith('.rst'):
                        rel = os.path.relpath(os.path.join(root, fn), UPSTREAM)
                        files.append(rel)
    
    # Add drivers/index.rst
    drivers_index = os.path.join(UPSTREAM, "components/drivers/index.rst")
    if os.path.exists(drivers_index):
        files.append("components/drivers/index.rst")
    
    # Remove duplicates
    files = sorted(set(files))
    
    print(f"Found {len(files)} RST files to translate")
    
    success = 0
    failed = 0
    for idx, rel in enumerate(files, 1):
        src = os.path.join(UPSTREAM, rel)
        dst = os.path.join(TARGET, rel)
        try:
            print(f"[{idx}/{len(files)}] {rel}...", end=' ', flush=True)
            translate_rst_file(src, dst)
            print("✓")
            success += 1
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"✗ {e}")
            failed += 1
    
    print(f"\nDone: {success} translated, {failed} failed out of {len(files)} total")


if __name__ == '__main__':
    main()
