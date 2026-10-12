#!/usr/bin/env python3
"""
descriptions.py — Review the per-session `descriptions:` entries of entity
pages (dossiers, locales, orgs, creatures, relics).

Usage:
    _bin/descriptions.py show 17e09      # episode text, GM notes, and all
                                         # entity descriptions for 17e09
    _bin/descriptions.py list 17e09      # just the entity descriptions
    _bin/descriptions.py apply edits.yaml

The edits file names the session and maps entity pages to new content
(null removes that session's entry from the page):

    session: 17e09
    dossiers/ulgrim: |
      Bear shaman who ...
    locales/storm-stables: null
"""

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import entities  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / '_pages'


def entity_pages():
    for kind in entities.ENTITY_DIRS:
        for p in sorted((PAGES / kind).glob('*.md')):
            yield f'{kind}/{p.stem}', p


def descriptions_for(sid):
    out = []
    for key, p in entity_pages():
        fm, _ = entities.read_front_matter(p)
        for d in fm.get('descriptions') or []:
            if str(d.get('session')) == sid:
                out.append((key, fm.get('title'), (d.get('content') or '').strip()))
    return out


def show(sid, full=True):
    if full:
        for rel in (f'events/case-{sid}.md', f'gm/events/case-{sid}.md'):
            p = PAGES / rel
            if p.exists():
                print(f'########## {rel}')
                text = p.read_text(encoding='utf-8')
                # Drop the noisy parts of GM Assistant exports.
                text = re.sub(r'\n(memorable_moments|middle_english_summary|limerick_style_summary|'
                              r'classic_summary|snarky_summary):.*?(?=\n[a-z_]+:|\n---)', '\n', text, flags=re.S)
                print(text)
    print(f'########## descriptions for {sid}')
    for key, title, content in descriptions_for(sid):
        print(f'--- {key} ({title})')
        print(content)


ENTRY_RE = r'(?m)^  - session: ["\']?{sid}["\']?\n    content: (?:\|-?|>-?)?.*?(?=^  - session:|^[^\s]|\Z)'


def format_entry(sid, content):
    lines = [f'  - session: "{sid}"', '    content: |']
    lines += ['      ' + l if l.strip() else '' for l in content.strip().split('\n')]
    return '\n'.join(lines) + '\n'


def set_description(path, sid, content):
    text = path.read_text(encoding='utf-8')
    m = re.match(r'---\n(.*?\n)---\n', text, re.S)
    fm, rest = m.group(1), text[m.end():]
    pat = re.compile(ENTRY_RE.format(sid=re.escape(sid)), re.S)
    if pat.search(fm):
        fm = pat.sub(lambda _: format_entry(sid, content) if content else '', fm, count=1)
        if not re.search(r'^  - session:', fm, re.M):
            fm = re.sub(r'(?m)^descriptions:\s*\n', '', fm)
    elif content:
        if not re.search(r'(?m)^descriptions:', fm):
            fm = fm + 'descriptions:\n'
        # Insert in session order.
        key = lambda s: tuple(int(x) for x in re.findall(r'\d+', s))
        entries = list(re.finditer(ENTRY_RE.format(sid=r'(\d+e\d+)'), fm, re.S))
        later = [e for e in entries if key(e.group(1)) > key(sid)]
        if later:
            pos = later[0].start()
        elif entries:
            pos = entries[-1].end()
        else:
            pos = re.search(r'(?m)^descriptions:\s*\n', fm).end()
        fm = fm[:pos] + format_entry(sid, content) + fm[pos:]
    else:
        return False
    yaml.safe_load(fm)  # sanity check
    path.write_text('---\n' + fm + '---\n' + rest, encoding='utf-8')
    return True


def apply(edits_path):
    edits = yaml.safe_load(Path(edits_path).read_text(encoding='utf-8'))
    sid = str(edits.pop('session'))
    for key, content in edits.items():
        p = PAGES / f'{key}.md'
        if not p.exists():
            print(f'MISSING PAGE: {key}')
            continue
        changed = set_description(p, sid, (content or '').strip())
        print(f'{"updated" if changed else "unchanged"}: {key}')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cmd, arg = sys.argv[1], sys.argv[2]
    if cmd == 'show':
        show(arg)
    elif cmd == 'list':
        show(arg, full=False)
    elif cmd == 'apply':
        apply(arg)
    else:
        print(__doc__)
        sys.exit(1)
