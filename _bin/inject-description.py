#!/usr/bin/env python3
"""
inject-description.py — Add a session description entry to an Equilibrium entity page.

Usage:
  _bin/inject-description.py <page_path> <session_id> <content>

If the page already has a descriptions entry for <session_id>, it will be
updated (unless --no-overwrite is passed). New entries are appended in
chronological session order.

Exits 0 on success, 1 on error.
"""

import sys
import re
import os

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def session_sort_key(session_id):
    """Sort sessions like '01e01', '02e03', '14e09' numerically."""
    m = re.match(r'(\d+)e(\d+)', session_id)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return (999, 999)

def format_description_entry(session_id, content):
    """Format a single descriptions entry as YAML text."""
    lines = ["  - session: \"{}\"\n    content: |".format(session_id)]
    for line in content.strip().split('\n'):
        lines.append("      " + line if line.strip() else "")
    lines.append("")  # trailing blank line after block
    return '\n'.join(lines)

def inject(path, session_id, content, no_overwrite=False):
    text = load_file(path)

    # Split into frontmatter + body
    if not text.startswith('---'):
        print(f"ERROR: {path} does not start with YAML frontmatter", file=sys.stderr)
        return False

    # Find end of frontmatter
    end_fm = text.index('---', 3)
    frontmatter = text[3:end_fm].rstrip()
    body = text[end_fm + 3:]

    new_entry = format_description_entry(session_id, content)

    # Check if descriptions key exists
    if re.search(r'^descriptions:', frontmatter, re.MULTILINE):
        # Check if this session already exists
        session_pattern = r'- session: ["\']?' + re.escape(session_id) + r'["\']?'
        if re.search(session_pattern, frontmatter):
            if no_overwrite:
                print(f"SKIP: {path} already has session {session_id}", file=sys.stderr)
                return True
            else:
                # Replace existing entry
                # Find the block for this session and replace it
                # Match from "  - session: ..." to the next "  - session:" or end of descriptions
                pattern = r'(  - session: ["\']?' + re.escape(session_id) + r'["\']?\n    content: \|.*?(?=\n  - session:|\Z))'
                replacement = new_entry.rstrip()
                new_fm = re.sub(pattern, replacement, frontmatter, flags=re.DOTALL)
                if new_fm == frontmatter:
                    # Try simpler replace for empty content entries
                    pattern2 = r'(  - session: ["\']?' + re.escape(session_id) + r'["\']?\n    content: ".*?")'
                    new_fm = re.sub(pattern2, new_entry.rstrip(), frontmatter, flags=re.DOTALL)
                frontmatter = new_fm
        else:
            # Append new entry to descriptions, in sorted order
            # Find where descriptions block ends
            desc_start = frontmatter.find('\ndescriptions:')
            if desc_start == -1:
                desc_start = frontmatter.find('descriptions:')
            
            # Find all existing session entries and their sort keys
            existing = re.findall(r'  - session: ["\']?(\d+e\d+)["\']?', frontmatter)
            
            # Find insertion point (maintain sort order)
            new_key = session_sort_key(session_id)
            insert_after = None
            for sid in existing:
                if session_sort_key(sid) < new_key:
                    insert_after = sid
            
            if insert_after:
                # Insert after the last entry whose key < new_key
                # Find the end of that entry's content block
                pattern = r'(  - session: ["\']?' + re.escape(insert_after) + r'["\']?\n    content: \|[^\n]*(?:\n(?!  - )[^\n]*)*)'
                match = re.search(pattern, frontmatter, re.DOTALL)
                if match:
                    insert_pos = match.end()
                    frontmatter = frontmatter[:insert_pos] + '\n' + new_entry.rstrip() + frontmatter[insert_pos:]
                else:
                    # Fallback: just append to descriptions
                    frontmatter = frontmatter + '\n' + new_entry.rstrip()
            else:
                # Insert at start of descriptions list
                desc_list_start = re.search(r'\ndescriptions:\n', frontmatter)
                if desc_list_start:
                    insert_pos = desc_list_start.end()
                    frontmatter = frontmatter[:insert_pos] + new_entry.rstrip() + '\n' + frontmatter[insert_pos:]
                else:
                    frontmatter = frontmatter + '\n' + new_entry.rstrip()
    else:
        # No descriptions key yet — add it at the end of frontmatter
        frontmatter = frontmatter + '\ndescriptions:\n' + new_entry.rstrip()

    new_text = '---\n' + frontmatter + '\n---' + body
    save_file(path, new_text)
    print(f"OK: {path} — added session {session_id}")
    return True

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('page_path')
    parser.add_argument('session_id')
    parser.add_argument('content')
    parser.add_argument('--no-overwrite', action='store_true')
    args = parser.parse_args()
    
    ok = inject(args.page_path, args.session_id, args.content, args.no_overwrite)
    sys.exit(0 if ok else 1)
