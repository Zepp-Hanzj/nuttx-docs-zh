#!/usr/bin/env python3
"""Translate commands.rst from English to Chinese."""
import os

SRC = os.path.expanduser("~/workspace/nuttx-docs-zh/_upstream/applications/nsh/commands.rst")
DST = os.path.expanduser("~/workspace/nuttx-docs-zh/applications/nsh/commands.rst")

# Translation mapping: English prose -> Chinese
# We process line by line, translating prose paragraphs
# while preserving RST structure (titles, code blocks, tables, directives)

translations = {
    "========\n": "========\n",
    "Commands\n": "命令\n",
    "**Command Syntax:**\n": "**命令语法：**\n",
    "**Command Syntax**\n": "**命令语法**\n",
    "**Command Syntax 1:**\n": "**命令语法 1：**\n",
    "**Command Syntax 2:**\n": "**命令语法 2：**\n",
    "**Synopsis**. These are two alternative forms of the same command.\n": "**摘要**。这是同一命令的两种替代形式。\n",
    "They support evaluation of a boolean expression which sets\n": "它们支持对布尔表达式求值，该表达式设置\n",
    "``$?``. This command is used most frequently as\n": "``$?``。此命令最常用于\n",
    "the conditional command following the ``if`` in the\n": "作为 ``if-then[-else]-fi`` 中 ``if`` 之后的\n",
    "``if-then[-else]-fi``.\n": "条件命令。\n",
    "**Expression Syntax:**\n": "**表达式语法：**\n",
}

with open(SRC, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Process the file - we need to translate prose while preserving structure
# Strategy: identify prose blocks vs code blocks/tables/directives
output = []
in_code_block = False
in_table = False
code_block_marker = ""

i = 0
while i < len(lines):
    line = lines[i]
    
    # Track code blocks
    if line.rstrip() in ('::', '.. code-block:: bash', '.. code-block:: c', 
                          '.. code-block:: fish', '.. code-block:: diff',
                          '.. code-block:: console'):
        in_code_block = True
        code_block_marker = line.rstrip()
    
    # Check if we're leaving a code block (empty line after indented content)
    if in_code_block and line.strip() == '' and i + 1 < len(lines):
        next_line = lines[i+1]
        if next_line.strip() and not next_line.startswith('   ') and not next_line.startswith('\t'):
            if not next_line.startswith('..') and not all(c in '=-' for c in next_line.rstrip()):
                in_code_block = False
    
    # Track RST directives
    if line.startswith('.. ') and '::' in line:
        in_code_block = True  # Treat directives as protected
    
    # For non-code-block lines, apply translations
    if not in_code_block or line.startswith('.. note::'):
        # Apply line-level translations
        translated = translate_line(line, lines, i)
        output.append(translated)
    else:
        output.append(line)
    
    # Check if we're entering/exiting a table
    if line.rstrip() and all(c in '=' for c in line.rstrip()) and len(line.rstrip()) > 5:
        in_table = not in_table
    
    i += 1

def translate_line(line, lines, idx):
    """Translate a single line of prose."""
    stripped = line.rstrip('\n')
    
    # Don't translate empty lines
    if not stripped:
        return line
    
    # Don't translate RST directives (except notes)
    if stripped.startswith('.. ') and not stripped.startswith('.. note::'):
        return line
    
    # Don't translate cross-references
    if stripped.startswith(':ref:') or stripped.startswith(':doc:'):
        return line
    
    # Don't translate toctree
    if 'toctree' in stripped:
        return line
    
    # Translate known prose patterns
    t = {
        "========\n": "========\n",
        "Commands\n": "命令\n",
        "**Command Syntax:**": "**命令语法：**",
        "**Command Syntax**": "**命令语法**",
        "**Command Syntax 1:**": "**命令语法 1：**",
        "**Command Syntax 2:**": "**命令语法 2：**",
    }
    
    if stripped in t:
        return t[stripped] + "\n" if line.endswith('\n') else t[stripped]
    
    return line

with open(DST, 'w', encoding='utf-8') as f:
    f.writelines(output)

print(f"Processed {len(lines)} lines -> {DST}")
