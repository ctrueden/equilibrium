#!/usr/bin/env python3
"""
review-session.py — Semi-automated review of session (episode) pages.

Usage:
    _bin/review-session.py [--apply] [--all] [page.md ...]

With no pages given, reviews every episode page marked `reviewed: false`
(or, with --all, every episode page).

For each page, it:
1. Links the first mention of each known entity (dossiers, locales, orgs,
   creatures, relics) in each recap text field (summary, short_summary, ...;
   each is shown as its own tab), in the scenes, and in the markdown body.
   Only unambiguous names are linked: full titles, `nav-title`s, `aliases`,
   and distinctive first/last names (see _bin/entities.py).
2. Fills in missing `wiki:` links of the npcs/locations/items sidebar lists.
3. Flags capitalized names that match no wiki page: either probable
   misspellings of a known name (add the misspelling to that page's
   `aliases:` front matter, and fix the text), or new entities that may
   deserve a page.

Without --apply, nothing is written: it only reports what it would do.
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import entities  # noqa: E402
import yaml  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EVENTS = ROOT / '_pages' / 'events'

# Front matter fields holding recap prose; each one is linked independently.
TEXT_KEYS = ['notes', 'callie_journal', 'summary', 'short_summary',
             'classic_summary', 'middle_english_summary', 'snarky_summary',
             'limerick_style_summary']
# Fields whose prose is linked as one unit.
SCENE_KEYS = ['scenes']
# Sidebar reference lists: entries get a `wiki:` link when resolvable.
SIDEBAR_KEYS = ['npcs', 'locations', 'items']
# Sidebar lists whose unlinked names are worth flagging.
FLAG_SIDEBAR_KEYS = ['npcs', 'locations']
# Capitalized words that are not names.
NOT_NAMES = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
             'Sunday', 'PowerPoint', 'GM', 'DM', 'PC', 'NPC', 'OK',
             "I'm", "I'd", "I'll", "I've", 'I’m', 'I’d', 'I’ll', 'I’ve'}

PROTECT_RE = re.compile(
    r'\[[^\]]*\]\([^)]*\)'      # markdown link
    r'|\{%.*?%\}|\{\{.*?\}\}'   # Liquid
    r'|<[^>]+>'                 # HTML tag
    r'|`[^`]*`'                 # code
    r'|https?://\S+',           # bare URL
    re.S)


def top_level_regions(fm_text):
    """Map each top-level front matter key to (start, end) offsets of its
    value (everything after 'key:' up to the next top-level key)."""
    keys = list(re.finditer(r'^([A-Za-z_][\w\-]*):', fm_text, re.M))
    regions = {}
    for i, m in enumerate(keys):
        end = keys[i + 1].start() if i + 1 < len(keys) else len(fm_text)
        regions[m.group(1)] = (m.end(), end)
    return regions


def name_pattern(name):
    words = [re.escape(w) for w in name.split()]
    return re.compile(r"(?<![\w\[/'’-])" + r'\s+'.join(words) + r"(?![\w\]-])")


class Linker:
    def __init__(self, index):
        self.index = index
        self.names = [(n, e, name_pattern(n)) for n, e in index.linkable_names()]

    def link(self, text, skip_line_re=None, yaml_context=False):
        """Link the first mention of each entity in text.
        Returns (new_text, [(name, entity)])."""
        protected = [m.span() for m in PROTECT_RE.finditer(text)]
        if yaml_context:
            # A plain YAML scalar must not start with "[": skip names at the
            # very start of a list item or "key: value" line.
            for m in re.finditer(r'(?m)^[ \t]*(?:-[ \t]+|[\w-]+:[ \t]+)', text):
                protected.append((m.end(), m.end() + 1))
        if skip_line_re:
            for m in re.finditer(r'^.*$', text, re.M):
                if skip_line_re.match(m.group(0)):
                    protected.append(m.span())
        already = set()
        for m in re.finditer(r'\]\(([^)]*)\)', text):
            already.add(m.group(1).rstrip('/').split('#')[0])

        def free(a, b, spans):
            return all(b <= s or a >= e for s, e in spans)

        candidates = []
        for name, ent, pat in self.names:
            if ent.link in already:
                continue
            for m in pat.finditer(text):
                if free(m.start(), m.end(), protected) and not self.part_of_bigger_name(text, m):
                    candidates.append((m.start(), m.end(), ent))
        # Longer matches claim their spans first ("Serelda Voth" beats "Voth").
        claimed = []
        for a, b, ent in sorted(candidates, key=lambda c: (-(c[1] - c[0]), c[0])):
            if free(a, b, [(s, e) for s, e, _ in claimed]):
                claimed.append((a, b, ent))
        first = {}
        for a, b, ent in sorted(claimed):
            first.setdefault(ent.link, (a, b, ent))
        out, linked = text, []
        for a, b, ent in sorted(first.values(), reverse=True):
            out = out[:a] + f'[{out[a:b]}]({ent.link})' + out[b:]
            linked.append((re.sub(r'\s+', ' ', text[a:b]), ent))
        return out, sorted(linked, key=lambda x: x[0])

    def part_of_bigger_name(self, text, m):
        """Whether a match is part of a longer, unknown name: "Kell" in
        "Soran Kell" is likely someone else (or a misspelling)."""
        vocab = self.index.vocabulary
        before = re.search(r"([A-Z][\w'’-]*)[ \t]+$", text[max(0, m.start() - 40):m.start()])
        after = re.match(r"[ \t]+([A-Z][\w-]*)", text[m.end():m.end() + 40])
        return any(w and strip_possessive(w.group(1)).lower() not in vocab
                   for w in (before, after))


# ---------------------------------------------------------------------------
# Unknown-name detection
# ---------------------------------------------------------------------------

CAP_RUN = re.compile(
    r"(?<![\w'’])[A-Z][\w'’\-]*(?:\s(?:(?:of|the|de|du|von|van)\s)*[A-Z][\w'’\-]*)*")
SENTENCE_START = re.compile(r'(?:^|[.!?:;"“”(\[*>#\-]\s*|\n\s*)$')


def strip_possessive(w):
    return re.sub(r"['’]s?$", '', w)


def find_unknown_names(text, index):
    """Return {name: count} for capitalized names not known to the wiki."""
    known = index.all_names()
    known_words = {w for n in known for w in n.split()}
    vocab = index.vocabulary
    clean = PROTECT_RE.sub(lambda m: re.sub(r'\[([^\]]*)\]\([^)]*\)', ' ', m.group(0))
                           if m.group(0).startswith('[') else ' ', text)
    found = {}
    for m in CAP_RUN.finditer(clean):
        run = m.group(0)
        words = [strip_possessive(w) for w in run.split()]
        name = ' '.join(words)
        if name in known:
            continue
        at_start = bool(SENTENCE_START.search(clean[:m.start()][-3:] if m.start() else ''))
        if m.start() == 0:
            at_start = True
        # Drop leading ordinary words ("The", or any word at sentence start).
        while words and (words[0].lower() in vocab or words[0].lower() in ('the', 'a', 'an')) \
                and (at_start or words[0] in ('The', 'A', 'An')):
            words = words[1:]
            at_start = False
        while words and words[0] in ('of', 'the', 'de', 'du', 'von', 'van'):
            words = words[1:]
        if not words:
            continue

        def ordinary(w):
            parts = [p for p in w.split('-') if p]
            return all(p.lower() in vocab or p in known_words for p in parts)
        unknown = [w for w in words if w not in known_words and not ordinary(w)
                   and w not in NOT_NAMES and not w.isupper() and len(w) > 1]
        if not unknown:
            continue
        name = ' '.join(words)
        if name in known:
            continue
        found[name] = found.get(name, 0) + 1
    return found


def suggest(name, index):
    known = sorted(index.all_names())
    out = difflib.get_close_matches(name, known, n=3, cutoff=0.75)
    if not out:
        for w in name.split():
            out += difflib.get_close_matches(w, known, n=2, cutoff=0.8)
    return list(dict.fromkeys(out))


# ---------------------------------------------------------------------------
# Page processing
# ---------------------------------------------------------------------------

def sidebar_links(fm_text, regions, index, report):
    """Insert `wiki:` under sidebar entries that lack one."""
    inserts = []
    for key in SIDEBAR_KEYS:
        if key not in regions:
            continue
        a, b = regions[key]
        region = fm_text[a:b]
        entries = list(re.finditer(r'^(\s*)- name:\s*(.+?)\s*$', region, re.M))
        for i, m in enumerate(entries):
            end = entries[i + 1].start() if i + 1 < len(entries) else len(region)
            body = region[m.end():end]
            if re.search(r'^\s*wiki:', body, re.M):
                continue
            name = m.group(2).strip('"\'')
            ent = index.lookup(name)
            if not ent:
                continue
            indent = m.group(1) + '  '
            inserts.append((a + m.end(), f'\n{indent}wiki: {ent.link}'))
            note = '' if name in (ent.title, ent.front.get('nav-title')) else \
                f'  (sidebar says "{name}"; page title is "{ent.title}")'
            report.append(f'  sidebar {key}: {name} -> {ent.link}{note}')
    for pos, text in sorted(inserts, reverse=True):
        fm_text = fm_text[:pos] + text + fm_text[pos:]
    return fm_text


def unlinked_sidebar(fm, index):
    out = []
    for key in FLAG_SIDEBAR_KEYS:
        for e in fm.get(key) or []:
            if isinstance(e, dict) and not e.get('wiki') and e.get('name'):
                if not index.lookup(str(e['name'])):
                    out.append((key, str(e['name'])))
    return out


def apply_fixes(text, fixes):
    """Replace misspelled names (whole words, including across line wraps)."""
    for old, new in fixes:
        words = [re.escape(w) for w in old.split()]
        pat = re.compile(r'(?<![\w-])' + r'\s+'.join(words) + r'(?![\w-])')
        text = pat.sub(lambda m: new, text)
    return text


def review(path, linker, index, apply, fixes=()):
    text = path.read_text(encoding='utf-8')
    original = text
    text = apply_fixes(text, fixes)
    m = re.match(r'(---\s*\n)(.*?\n)(---\s*\n)(.*)', text, re.S)
    if not m:
        print(f'{path}: no front matter; skipped')
        return
    head, fm_text, sep, body = m.groups()
    fm = yaml.safe_load(fm_text) or {}
    report = []
    prose = []

    # 1. Recap fields, each linked independently; scenes as one unit.
    regions = top_level_regions(fm_text)
    for key in sorted(regions, key=lambda k: -regions[k][0]):
        if key not in TEXT_KEYS + SCENE_KEYS:
            continue
        a, b = regions[key]
        skip = re.compile(r'^\s*-?\s*title:') if key in SCENE_KEYS else None
        new, linked = linker.link(fm_text[a:b], skip, yaml_context=True)
        prose.append(re.sub(r'^\s*-?\s*title:.*$', '', fm_text[a:b], flags=re.M))
        if linked:
            report.append(f'  {key}: ' + ', '.join(f'{n} -> {e!r}' for n, e in linked))
        fm_text = fm_text[:a] + new + fm_text[b:]

    # 2. Sidebar lists.
    fm_text = sidebar_links(fm_text, top_level_regions(fm_text), index, report)

    # 3. Markdown body.
    if body.strip():
        prose.append(body)
        body, linked = linker.link(body, re.compile(r'^\s*#'))
        if linked:
            report.append('  body: ' + ', '.join(f'{n} -> {e!r}' for n, e in linked))

    # 4. Names the wiki doesn't know.
    unknown = {}
    for chunk in prose:
        for n, c in find_unknown_names(chunk, index).items():
            unknown[n] = unknown.get(n, 0) + c
    for key, name in unlinked_sidebar(fm, index):
        unknown.setdefault(name, 0)

    print(f'== {path.relative_to(ROOT)}')
    print('\n'.join(report) if report else '  (no new links)')
    misspelled, new = [], []
    suggestions = {name: suggest(name, index) for name in unknown}
    # "Zarlis Shale" ~ "Xarlus Shale" implies "Zarlis" ~ "Xarlus".
    for name, sugg in list(suggestions.items()):
        words = name.split()
        for sg in sugg:
            if len(sg.split()) == len(words) > 1:
                for w, sw in zip(words, sg.split()):
                    if w != sw and w in suggestions and sw not in suggestions[w]:
                        suggestions[w].insert(0, sw)
    for name, count in sorted(unknown.items(), key=lambda kv: (-kv[1], kv[0])):
        sugg = suggestions[name]
        (misspelled if sugg else new).append((name, count, sugg))
    if misspelled:
        print('  possible misspellings (fix the text, or add to the page\'s aliases):')
        for name, count, s in misspelled:
            print(f'    {name} ({count}x): did you mean {" / ".join(s)}?')
    if new:
        print('  names without wiki pages:')
        print('    ' + ', '.join(f'{n} ({c}x)' for n, c, _ in new))

    new_text = head + fm_text + sep + body
    if apply and new_text != original:
        path.write_text(new_text, encoding='utf-8')
        print('  (written)')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('pages', nargs='*', type=Path)
    ap.add_argument('--apply', action='store_true', help='write changes')
    ap.add_argument('--all', action='store_true', help='review all episode pages')
    ap.add_argument('--fix', action='append', default=[], metavar='OLD=NEW',
                    help='correct a misspelled name first (repeatable), '
                         'e.g. --fix "Zarlis=Xarlus"')
    args = ap.parse_args()

    pages = [p.resolve() for p in args.pages]
    if not pages:
        for p in sorted(EVENTS.glob('case-*e*.md')):
            fm, _ = entities.read_front_matter(p)
            if args.all or fm.get('reviewed') is False:
                pages.append(p)
    index = entities.Index(ROOT)
    linker = Linker(index)
    fixes = [tuple(f.split('=', 1)) for f in args.fix]
    for p in pages:
        review(p, linker, index, args.apply, fixes)


if __name__ == '__main__':
    main()
