#!/usr/bin/env python3
"""
dnd5e.py — 5etools rules tooltips for the local (GM) site build.

Usage:
    _bin/dnd5e.py              # clone if needed, resolve, write data
    _bin/dnd5e.py -v           # also list every resolved reference
    _bin/dnd5e.py --no-clone   # never touch the network
    _bin/dnd5e.py --lookup "Sneak Attack" [--edition 2024]

The 5etools data (https://github.com/5etools-mirror-3) aggregates published
D&D content that is not licensed for redistribution, so it is never
committed: the repositories are cloned into the gitignored `_external/`
folder (where Jekyll does not look), and this script copies in only what
the site needs, as gitignored build artifacts:

- `_data/dnd5e.json`: the rules entries referenced by the site's pages,
  pre-rendered to HTML, plus a per-page map from referencing text to links.
- `assets/5etools/`: any images those entries use.

Without these files (e.g. on GitHub Pages) the pages render as before:
plain text, no tooltips.

What is resolved:

- Charsheets (`layout: charsheet`): feature names, spell lists, weapon names,
  equipment, skills, senses, languages and condition immunities. Names are
  matched leniently (parenthetical notes, `[...]`, trailing `*`, `Feat:`
  style prefixes are ignored), using the sheet's classes, subclass, race and
  each feature's `source` to pick between same-named entries. A feature,
  weapon or spell list entry can pin the match with `ref:`, or opt out with
  `ref: none` (see REFERENCES below). `cs.rules: 2024` makes the sheet
  prefer the 2024 rules (5e.tools) to the 2014 rules (2014.5e.tools); either
  way, names missing from one edition are looked up in the other.
- Any page: `{% include rule ref="..." %}` (see _includes/rule).

REFERENCES are written `[kind:]Name[|arg|arg...]`, with 5etools' tag
arguments, e.g.:

    Absorb Elements|XGE                  any kind, source XGE
    spell:Revivify|XPHB
    feat:Alert
    optfeature:Agonizing Blast
    classFeature:Cunning Action|Rogue||2
    subclassFeature:Ear for Deceit|Rogue||Inquisitive|XGE|3

5etools' own tag syntax (`{@spell Revivify|XPHB}`) is accepted too. In a
spell list, a single spell can be pinned with `Name|SOURCE`, e.g.
"Bless, Revivify|XPHB".
"""

import argparse
import copy
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXTERNAL = ROOT / '_external'
PAGES = ROOT / '_pages'
OUT_DATA = ROOT / '_data' / 'dnd5e.json'
OUT_IMG = ROOT / 'assets' / '5etools'

EDITIONS = ['2014', '2024']
REPOS = {
    '2014': {'src': '5etools-2014-src', 'img': '5etools-2014-img'},
    '2024': {'src': '5etools-src', 'img': '5etools-img'},
}
GITHUB = 'https://github.com/5etools-mirror-3/'
SITES = {'2014': 'https://2014.5e.tools/', '2024': 'https://5e.tools/'}


def repo_dir(edition, kind):
    return EXTERNAL / f'5etools-{edition}-{kind}'


# ── Cloning ─────────────────────────────────────────────────────────────────

def clone(edition, kind):
    """Clones a 5etools repository, if not already present. The (huge) image
    repositories are partial clones with no checkout: images are fetched
    one at a time, on demand (see copy_image)."""
    dest = repo_dir(edition, kind)
    if dest.exists():
        return True
    url = GITHUB + REPOS[edition][kind]
    cmd = ['git', 'clone', '--depth', '1']
    if kind == 'img':
        cmd += ['--filter=blob:none', '--no-checkout']
    print(f'Cloning {url} into {dest.relative_to(ROOT)}', file=sys.stderr)
    EXTERNAL.mkdir(exist_ok=True)
    return subprocess.run(cmd + [url, str(dest)]).returncode == 0


def copy_image(edition, path):
    """Copies an image from the image repository into assets/5etools,
    returning its site path, or None if it is unavailable."""
    rel = Path(edition) / path
    dest = OUT_IMG / rel
    if not dest.exists():
        repo = repo_dir(edition, 'img')
        if not repo.exists():
            return None
        dest.parent.mkdir(parents=True, exist_ok=True)
        src = repo / path
        if not src.exists():
            src = repo / 'img' / path
        if src.exists():
            subprocess.run(['cp', '--reflink=auto', str(src), str(dest)], check=True)
        else:
            for p in (path, f'img/{path}'):
                r = subprocess.run(['git', '-C', str(repo), 'cat-file', 'blob', f'HEAD:{p}'],
                                   capture_output=True)
                if r.returncode == 0:
                    dest.write_bytes(r.stdout)
                    break
            else:
                return None
    return quote(f'/assets/5etools/{rel.as_posix()}')


# ── Data loading ────────────────────────────────────────────────────────────

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def norm(s):
    """Normalizes a name for matching."""
    s = str(s).replace('’', "'").replace('‘', "'").replace('—', '-')
    return re.sub(r'\s+', ' ', s).strip().lower()


def apply_mod(target, mods):
    """Applies (the common subset of) a 5etools `_copy._mod`."""
    for prop, ops in mods.items():
        for op in ops if isinstance(ops, list) else [ops]:
            if op == 'remove':
                target.pop(prop, None)
                continue
            if not isinstance(op, dict):
                continue
            mode = op.get('mode')
            if prop == '*':
                if mode == 'replaceTxt':
                    for k in list(target):
                        if k not in ('name', 'source'):
                            target[k] = replace_txt(target[k], op)
                continue
            items = op.get('items', [])
            items = items if isinstance(items, list) else [items]
            arr = target.get(prop)
            if mode == 'replaceTxt':
                if prop in target:
                    target[prop] = replace_txt(target[prop], op)
            elif mode == 'appendArr':
                target[prop] = (arr or []) + items
            elif mode == 'prependArr':
                target[prop] = items + (arr or [])
            elif mode == 'appendIfNotExistsArr':
                target[prop] = (arr or []) + [i for i in items if i not in (arr or [])]
            elif mode == 'insertArr':
                arr = list(arr or [])
                ix = op.get('index', 0)
                target[prop] = arr[:ix] + items + arr[ix:]
            elif mode == 'replaceArr' and arr is not None:
                rep = op.get('replace')
                out = []
                for i, it in enumerate(arr):
                    hit = (isinstance(rep, dict) and rep.get('index') == i) or \
                          (isinstance(rep, str) and (it == rep or (isinstance(it, dict) and it.get('name') == rep)))
                    out += items if hit else [it]
                target[prop] = out
            elif mode == 'removeArr' and arr is not None:
                names = op.get('names', [])
                names = names if isinstance(names, list) else [names]
                target[prop] = [it for it in arr if it not in items and not
                                (isinstance(it, dict) and it.get('name') in names)]


def replace_txt(v, op):
    if isinstance(v, str):
        flags = re.I if 'i' in op.get('flags', '') else 0
        try:
            return re.sub(op['replace'], op['with'].replace('$', '\\'), v, flags=flags)
        except (re.error, KeyError):
            return v
    if isinstance(v, list):
        return [replace_txt(x, op) for x in v]
    if isinstance(v, dict):
        return {k: (replace_txt(x, op) if k in ('entries', 'entry', 'items') else x) for k, x in v.items()}
    return v


def resolve_copies(items):
    """Resolves 5etools `_copy` inheritance within a list of entities."""
    by_key = {(norm(e['name']), norm(e.get('source', ''))): e for e in items if 'name' in e}
    done = {}

    def get(e, depth=0):
        if '_copy' not in e or depth > 5:
            return e
        if id(e) in done:
            return done[id(e)]
        c = e['_copy']
        base = by_key.get((norm(c.get('name', '')), norm(c.get('source', ''))))
        if base is None:
            return e
        out = copy.deepcopy(get(base, depth + 1))
        for k in ('srd', 'basicRules', 'reprintedAs', 'otherSources', 'page'):
            out.pop(k, None)
        out.update({k: v for k, v in e.items() if k != '_copy'})
        apply_mod(out, c.get('_mod', {}))
        done[id(e)] = out
        return out

    return [get(e) for e in items]


class Dataset:
    """The indexed rules of one 5etools edition."""

    TRAIT_SKIP = {'age', 'size', 'speed', 'languages', 'language', 'alignment',
                  'ability score increase', 'ability score increases', 'creature type'}

    def __init__(self, edition):
        self.edition = edition
        self.data = repo_dir(edition, 'src') / 'data'
        self.entries = []
        self.index = {}
        self.classes = {}
        self.modern = {'XPHB', 'XDMG', 'XMM'}
        self.published = {}
        for f, key in (('books.json', 'book'), ('adventures.json', 'adventure')):
            p = self.data / f
            if p.exists():
                for b in load_json(p).get(key, []):
                    self.published[b['id']] = b.get('published', '')
                    if b.get('published', '') >= '2024-09':
                        self.modern.add(b['id'])
        self.load()

    def add(self, kind, ent, **extra):
        name = ent.get('name')
        if not name:
            return None
        e = {'kind': kind, 'name': name, 'source': ent.get('source', ''),
             'edition': self.edition, 'data': ent, **extra}
        self.entries.append(e)
        self.index.setdefault(norm(name), []).append(e)
        # "Mystic Arcanum (6th level)" is also found as "Mystic Arcanum",
        # and "The Right Tool for the Job" as "Right Tool for the Job".
        alias = norm(re.sub(r'\s*\([^()]*\)', '', name))
        alias = re.sub(r'^the ', '', alias)
        if alias and alias != norm(name):
            self.index.setdefault(alias, []).append(e)
        return e

    def add_parts(self, kind, parent, entries, depth=0, **extra):
        """Indexes the named sub-entries (e.g. race traits, nested options)."""
        if depth > 3 or not isinstance(entries, list):
            return
        for it in entries:
            if not isinstance(it, dict):
                continue
            name = it.get('name')
            if name and it.get('type') in ('entries', 'item', 'inset', 'section', 'variant',
                                           'variantInner', 'variantSub', 'itemSub'):
                if norm(name) not in self.TRAIT_SKIP and norm(name) != norm(parent['name']):
                    self.add(kind, {**it, 'source': parent['source'], 'page': parent['data'].get('page')},
                             parent=parent, **extra)
            self.add_parts(kind, parent, it.get('entries') or it.get('items'), depth + 1, **extra)

    def load(self):
        d = self.data
        # Classes, subclasses, and their features.
        for fn in load_json(d / 'class' / 'index.json').values():
            j = load_json(d / 'class' / fn)
            for c in j.get('class', []):
                self.classes[(norm(c['name']), norm(c['source']))] = c
                self.add('class', c)
            for sc in j.get('subclass', []):
                self.add('subclass', sc)
            for f in j.get('classFeature', []):
                e = self.add('classFeature', f)
                if e:
                    self.add_parts('classPart', e, f.get('entries'))
            for f in j.get('subclassFeature', []):
                e = self.add('subclassFeature', f)
                if e:
                    self.add_parts('subclassPart', e, f.get('entries'))
        # Spells.
        for fn in load_json(d / 'spells' / 'index.json').values():
            for s in load_json(d / 'spells' / fn).get('spell', []):
                self.add('spell', s)
        # Races and subraces, and their traits.
        races = load_json(d / 'races.json')
        race_list = resolve_copies(races.get('race', []))
        for r in race_list:
            e = self.add('race', r)
            if e:
                self.add_parts('racetrait', e, r.get('entries'), raceName=r['name'])
        for sr in resolve_copies(races.get('subrace', [])):
            if not sr.get('name'):
                continue
            e = self.add('subrace', sr)
            if e:
                self.add_parts('racetrait', e, sr.get('entries'), raceName=sr.get('raceName'))
        # Backgrounds (and their features), feats, optional features.
        for b in resolve_copies(load_json(d / 'backgrounds.json').get('background', [])):
            e = self.add('background', b)
            if e:
                self.add_parts('backgroundPart', e, b.get('entries'))
        for f in resolve_copies(load_json(d / 'feats.json').get('feat', [])):
            self.add('feat', f)
        for f in load_json(d / 'optionalfeatures.json').get('optionalfeature', []):
            self.add('optionalfeature', f)
        # Items.
        base = load_json(d / 'items-base.json')
        for it in base.get('baseitem', []):
            self.add('baseitem', it)
        for it in resolve_copies(load_json(d / 'items.json').get('item', [])):
            self.add('item', it)
        # Miscellaneous rules.
        for fn, keys in (('actions.json', ['action']),
                         ('conditionsdiseases.json', ['condition', 'disease', 'status']),
                         ('variantrules.json', ['variantrule']),
                         ('senses.json', ['sense']),
                         ('skills.json', ['skill']),
                         ('languages.json', ['language'])):
            p = d / fn
            if p.exists():
                j = load_json(p)
                for k in keys:
                    for x in j.get(k, []):
                        self.add(k, x)

    def is_modern(self, e):
        data = e['data'] if 'parent' not in e else e['parent']['data']
        if data.get('edition') == 'one':
            return True
        if data.get('edition') == 'classic':
            return False
        return e['source'] in self.modern or data.get('classSource') in self.modern


# ── Resolution ──────────────────────────────────────────────────────────────

# Kinds searched by each sheet context, in order of preference.
FEATURE_KINDS = ['subclassFeature', 'classFeature', 'subclassPart', 'classPart', 'optionalfeature',
                 'feat', 'racetrait', 'subrace', 'race', 'background', 'backgroundPart', 'spell',
                 'action', 'condition', 'sense', 'variantrule']
KINDS = {
    'feature': FEATURE_KINDS,
    'spell': ['spell'],
    'weapon': ['baseitem', 'item', 'spell', 'subclassFeature', 'classFeature', 'subclassPart',
               'classPart', 'optionalfeature', 'feat', 'racetrait', 'action', 'variantrule'],
    'equipment': ['item', 'baseitem'],
    'skill': ['skill'],
    'sense': ['sense'],
    'language': ['language'],
    'condition': ['condition', 'status', 'disease'],
    'ref': FEATURE_KINDS + ['class', 'subclass', 'item', 'baseitem', 'skill', 'status',
                            'disease', 'language'],
}

# Tag names (as in `{@tag ...}` and `kind:` references) to entry kinds.
TAG_KINDS = {
    'spell': ['spell'], 'feat': ['feat'], 'optfeature': ['optionalfeature'],
    'optionalfeature': ['optionalfeature'], 'race': ['race', 'subrace'], 'subrace': ['subrace'],
    'racetrait': ['racetrait'], 'background': ['background', 'backgroundPart'],
    'item': ['item', 'baseitem'], 'baseitem': ['baseitem'], 'condition': ['condition'],
    'disease': ['disease'], 'status': ['status'], 'action': ['action'],
    'variantrule': ['variantrule'], 'sense': ['sense'], 'skill': ['skill'],
    'language': ['language'], 'class': ['class'], 'subclass': ['subclass'],
    'classfeature': ['classFeature', 'classPart'],
    'subclassfeature': ['subclassFeature', 'subclassPart'],
}

# 5etools tag argument layouts: the position of the source argument, and
# of class/subclass/level arguments, after the name.
TAG_ARGS = {
    'classFeature': ['className', 'classSource', 'level', 'source'],
    'classPart': ['className', 'classSource', 'level', 'source'],
    'subclassFeature': ['className', 'classSource', 'subclassShortName', 'subclassSource', 'level', 'source'],
    'subclassPart': ['className', 'classSource', 'subclassShortName', 'subclassSource', 'level', 'source'],
    'subclass': ['className', 'classSource', 'source'],
}
DEFAULT_SOURCES = {'item': 'DMG', 'baseitem': 'PHB', 'disease': 'DMG', 'variantrule': 'DMG'}

PREFIX_RE = re.compile(r'^(?:feats?|fighting style|eldritch invocations?|invocations?|metamagic|'
                       r'maneuvers?|infusions?|pact boon|boon|trait|feature)\s*:\s*', re.I)


class Context:
    """What a sheet tells us about how to pick between same-named entries."""

    def __init__(self, edition='2014', classes=(), subclass='', race='', label='', kind='ref', level=None):
        self.edition = str(edition)
        self.level = level
        self.classes = {norm(c) for c in classes}
        self.subclass = norm(subclass)
        self.race = norm(race)
        self.label = norm(label)
        self.kind = kind
        self.race_ids = set()  # ids of the sheet's race/subrace entries

    def with_(self, **kw):
        c = copy.copy(self)
        for k, v in kw.items():
            setattr(c, k, norm(v) if k == 'label' else v)
        return c


def words_in(needle, haystack):
    return bool(needle) and re.search(r'(?<![a-z])' + re.escape(needle) + r'(?![a-z])', haystack) is not None


class Resolver:
    def __init__(self, datasets):
        self.datasets = datasets  # edition -> Dataset

    def order(self, edition):
        return [edition] + [e for e in EDITIONS if e != edition and e in self.datasets] \
            if edition in self.datasets else [e for e in EDITIONS if e in self.datasets]

    def score(self, e, ctx, ds, kinds):
        d = e['data']
        cls = d.get('className') or (e.get('parent') or {}).get('data', {}).get('className')
        sub = d.get('subclassShortName') or (e.get('parent') or {}).get('data', {}).get('subclassShortName')
        kind = e['kind']
        label = ctx.label
        label_hit = (
            (label in ('feat', 'feats') and kind == 'feat') or
            (label in ('race', 'species', 'racial') and kind in ('racetrait', 'race', 'subrace')) or
            (label == 'background' and kind.startswith('background')) or
            (label == 'class' and cls is not None and norm(cls) in ctx.classes) or
            (cls is not None and label == norm(cls))
        )
        class_score = 0 if cls is None else (1 if norm(cls) in ctx.classes or label == norm(cls) else -1)
        sub_score = 0 if sub is None else (1 if words_in(norm(sub), ctx.subclass) else -1)
        race_score = 0
        if kind in ('racetrait', 'race', 'subrace'):
            if id(e.get('parent', e)) in ctx.race_ids:
                race_score = 2
            else:
                names = [e['name'] if kind != 'racetrait' else '', e.get('raceName') or d.get('raceName') or '',
                         e['parent']['name'] if 'parent' in e else '']
                race_score = 1 if any(words_in(norm(n), ctx.race) for n in names if n) else 0
        src = e['source']
        # Of same-named features ("Extra Attack (2)"), the highest one reached.
        lvl = int(d.get('level') or 0)
        level_score = ((1, lvl) if lvl <= ctx.level else (0, -lvl)) if ctx.level and lvl else (0, -lvl)
        return (
            label_hit,
            class_score,
            sub_score,
            race_score,
            not src.startswith('UA'),
            ds.is_modern(e) == (ctx.edition == '2024'),
            'reprintedAs' not in d,
            -kinds.index(kind),
            level_score,
            bool(d.get('srd') or d.get('basicRules')),
            src in ('PHB', 'XPHB'),
        )

    def candidates(self, name, ctx, kinds, filters=None, strict=False):
        """Returns (score, entry, dataset) for the entries matching a name,
        best first. When strict, features of classes the sheet does not
        have are skipped."""
        for ed in self.order(ctx.edition):
            ds = self.datasets[ed]
            found = []
            for e in ds.index.get(norm(name), []):
                if e['kind'] not in kinds:
                    continue
                if filters and not all(self.matches(e, k, v) for k, v in filters.items()):
                    continue
                score = self.score(e, ctx, ds, kinds)
                if strict and ctx.classes and score[1] < 0:
                    continue
                found.append((score, e, ds))
            if found:
                return sorted(found, key=lambda t: t[0], reverse=True)
        return []

    @staticmethod
    def matches(e, field, value):
        if not value:
            return True
        d = e['data']
        if field == 'source':
            return norm(e['source']) == norm(value)
        if field == 'level':
            return str(d.get('level', '')) == str(value)
        have = d.get(field) or (e.get('parent') or {}).get('data', {}).get(field)
        if field == 'classSource' and not have:
            have = 'PHB'
        return have is not None and norm(have) == norm(value)

    def lookup(self, name, ctx, kinds=None):
        """Finds the best entry for a name, which may carry a `|SOURCE`."""
        kinds = kinds or KINDS[ctx.kind]
        filters = {}
        if '|' in name:
            name, src = name.split('|', 1)
            filters['source'] = src.split('|')[0].strip()
        found = self.candidates(name.strip(), ctx, kinds, filters, strict=True)
        return found[0][1] if found else None

    def races(self, text, edition):
        """Finds the race (and subrace) entries named by a sheet's race,
        e.g. "Wood Elf", "Tiefling (Asmodeus)", "Gray Dwarf / Duergar":
        for each race named, the best subrace and its race, or the race."""
        text = norm(text)
        for ed in self.order(edition):
            ds = self.datasets[ed]
            groups = {}
            for e in ds.entries:
                if e['kind'] == 'subrace' and words_in(norm(e['data'].get('raceName', '')), text) \
                        and words_in(norm(e['name']), text):
                    groups.setdefault(norm(e['data']['raceName']), []).append(e)
                elif e['kind'] == 'race' and words_in(norm(e['name']), text):
                    groups.setdefault(norm(e['name']), []).append(e)
            if not groups:
                continue
            out = set()
            for race, ents in groups.items():
                def rank(e):
                    d = e['data']
                    return (e['kind'] == 'subrace', not e['source'].startswith('UA'),
                            ds.is_modern(e) == (edition == '2024'), 'reprintedAs' not in d,
                            ds.published.get(e['source'], ''))
                best = max(ents, key=rank)
                out.add(id(best))
                if best['kind'] == 'subrace':
                    d = best['data']
                    for e in ds.index.get(norm(d.get('raceName', '')), []):
                        if e['kind'] == 'race' and norm(e['source']) == norm(d.get('raceSource', 'PHB')):
                            out.add(id(e))
            return out
        return set()

    def lookup_ref(self, ref, ctx):
        """Resolves an explicit reference: `[kind:]Name[|args]` or `{@kind Name|args}`."""
        ref = ref.strip()
        m = re.fullmatch(r'\{@(\w+)\s+(.*)\}', ref)
        if m:
            tag, rest = m.group(1), m.group(2)
        else:
            m = re.match(r'(\w+):(?!\s)(.*)$', ref)
            if m and m.group(1).lower() in TAG_KINDS:
                tag, rest = m.group(1), m.group(2)
            else:
                return self.lookup(ref, ctx.with_(kind='ref'))
        kinds = TAG_KINDS.get(tag.lower())
        if not kinds:
            return None
        parts = [p.strip() for p in rest.split('|')]
        filters = {}
        layout = TAG_ARGS.get(kinds[0], ['source'])
        for field, value in zip(layout, parts[1:]):
            filters[field] = value
        found = self.candidates(parts[0], ctx, kinds, filters)
        if not found and 'source' not in filters and kinds[0] in DEFAULT_SOURCES:
            found = self.candidates(parts[0], ctx, kinds, {'source': DEFAULT_SOURCES[kinds[0]]})
        return found[0][1] if found else None


def clean_name(s):
    """Strips the annotations people put on names: (notes), [notes],
    trailing *, (?), " — notes"."""
    s = str(s).replace('’', "'")
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r'\([^()]*\)|\[[^\[\]]*\]', '', s)
    s = re.sub(r'\s+[—–]\s+.*$|\s+-\s+.*$', '', s)
    s = re.sub(r'[(\[].*$', '', s).replace(')', '').replace(']', '')
    return re.sub(r'\s+', ' ', s).strip(' *?.,;:')


def split_list(s, seps=','):
    """Splits a comma-separated list, outside of parentheses and brackets."""
    out, depth, cur = [], 0, ''
    for ch in str(s):
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth = max(0, depth - 1)
        if ch in seps and depth == 0:
            out.append(cur)
            cur = ''
        else:
            cur += ch
    out.append(cur)
    return out


# ── Rendering ───────────────────────────────────────────────────────────────

SCHOOLS = {'A': 'abjuration', 'C': 'conjuration', 'D': 'divination', 'E': 'enchantment',
           'V': 'evocation', 'I': 'illusion', 'N': 'necromancy', 'T': 'transmutation', 'P': 'psionic'}
ABILITIES = {'str': 'Strength', 'dex': 'Dexterity', 'con': 'Constitution',
             'int': 'Intelligence', 'wis': 'Wisdom', 'cha': 'Charisma'}
DMG_TYPES = {'A': 'acid', 'B': 'bludgeoning', 'C': 'cold', 'F': 'fire', 'O': 'force', 'L': 'lightning',
             'N': 'necrotic', 'P': 'piercing', 'I': 'poison', 'Y': 'psychic', 'R': 'radiant',
             'S': 'slashing', 'T': 'thunder'}
ITEM_TYPES = {'M': 'Melee weapon', 'R': 'Ranged weapon', 'A': 'Ammunition', 'LA': 'Light armor',
              'MA': 'Medium armor', 'HA': 'Heavy armor', 'S': 'Shield', 'RG': 'Ring', 'RD': 'Rod',
              'WD': 'Wand', 'ST': 'Staff', 'P': 'Potion', 'SC': 'Scroll', 'G': 'Adventuring gear',
              'AT': "Artisan's tools", 'T': 'Tools', 'INS': 'Instrument', 'GS': 'Gaming set',
              'SCF': 'Spellcasting focus', 'W': 'Wondrous item', 'TAH': 'Tack and harness',
              'FD': 'Food and drink', 'MNT': 'Mount', 'VEH': 'Vehicle', 'SHP': 'Vehicle',
              'EXP': 'Explosive', '$': 'Treasure', 'TG': 'Trade good', 'OTH': 'Other'}
ITEM_PROPS = {'F': 'finesse', 'L': 'light', 'H': 'heavy', 'R': 'reach', 'T': 'thrown',
              '2H': 'two-handed', 'V': 'versatile', 'A': 'ammunition', 'LD': 'loading',
              'S': 'special', 'RLD': 'reload', 'BF': 'burst fire', 'AF': 'ammunition (firearm)'}
FEATURE_TYPES = {'EI': 'Eldritch Invocation', 'MM': 'Metamagic', 'MV:B': 'Maneuver',
                 'MV': 'Maneuver', 'AI': 'Artificer Infusion', 'PB': 'Pact Boon',
                 'ED': 'Elemental Discipline', 'AS': 'Arcane Shot', 'AS:V1-UA': 'Arcane Shot',
                 'RN': 'Rune', 'AF': 'Alchemical Formula', 'OR': 'Onomancy Resonant',
                 'TT': "Traveler's Trick", 'FS:F': 'Fighting Style', 'FS:R': 'Fighting Style',
                 'FS:P': 'Fighting Style', 'FS:B': 'Fighting Style', 'OTH': 'Other'}
FEAT_CATEGORIES = {'O': 'Origin feat', 'G': 'General feat', 'FS': 'Fighting Style feat',
                   'EB': 'Epic Boon feat', 'D': 'Dragonmark feat'}
TAG_PAGES = {
    'spell': 'spells.html', 'item': 'items.html', 'condition': 'conditionsdiseases.html',
    'disease': 'conditionsdiseases.html', 'status': 'conditionsdiseases.html',
    'creature': 'bestiary.html', 'action': 'actions.html', 'feat': 'feats.html',
    'background': 'backgrounds.html', 'race': 'races.html', 'class': 'classes.html',
    'optfeature': 'optionalfeatures.html', 'variantrule': 'variantrules.html',
    'language': 'languages.html', 'deity': 'deities.html', 'object': 'objects.html',
    'hazard': 'trapshazards.html', 'trap': 'trapshazards.html', 'reward': 'rewards.html',
    'table': 'tables.html', 'vehicle': 'vehicles.html', 'boon': 'cultsboons.html',
    'cult': 'cultsboons.html', 'psionic': 'psionics.html', 'deck': 'decks.html',
    'charoption': 'charcreationoptions.html',
}
TAG_DEFAULT_SOURCES = {'creature': 'MM', 'item': 'DMG', 'disease': 'DMG', 'hazard': 'DMG',
                       'trap': 'DMG', 'object': 'DMG', 'reward': 'DMG', 'table': 'DMG',
                       'deck': 'DMG', 'variantrule': 'DMG', 'boon': 'MTF', 'cult': 'MTF',
                       'vehicle': 'GoS', 'charoption': 'MOT', 'psionic': 'UATheMysticClass'}
# For entity tags, the index of the display-text argument.
TAG_DISPLAY_ARG = {'classFeature': 5, 'subclassFeature': 7, 'deity': 3, 'card': 3,
                   'quickref': 4, 'subclass': 4}


def enc(s):
    """5etools' hash encoding (encodeURIComponent of the lowercased string)."""
    return quote(str(s).lower(), safe="!'()*-._~").lower()


def ordinal(n):
    n = int(n)
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def strip_src(s):
    return str(s).split('|')[0]


class Renderer:
    """Renders 5etools entries to HTML."""

    def __init__(self, ds, baseurl):
        self.ds = ds
        self.site = SITES[ds.edition]
        self.baseurl = baseurl

    # Inline {@tag ...} markup.

    def inline(self, s):
        s = html.escape(str(s), quote=False)
        # Render innermost tags first, until none are left.
        pat = re.compile(r'\{@(\w+)(?:\s([^{}]*))?\}')
        for _ in range(20):
            s, n = pat.subn(lambda m: self.tag(m.group(1), html.unescape(m.group(2) or '')), s)
            if not n:
                break
        return s

    def tag(self, tag, text):
        parts = text.split('|')
        first = parts[0]
        e = lambda x: html.escape(x, quote=False)  # noqa: E731
        simple = {'b': 'b', 'bold': 'b', 'i': 'i', 'italic': 'i', 'u': 'u', 'underline': 'u',
                  's': 's', 'strike': 's', 'sup': 'sup', 'sub': 'sub', 'kbd': 'kbd',
                  'code': 'code', 'note': 'i', 'highlight': 'mark'}
        if tag in simple:
            # The text may already contain rendered (nested) HTML.
            return f'<{simple[tag]}>{text}</{simple[tag]}>'
        if tag in ('dice', 'damage', 'autodice'):
            return e(parts[1] if len(parts) > 1 and parts[1] else first)
        if tag in ('hit', 'd20'):
            return e(parts[1] if len(parts) > 1 and parts[1] else
                     (first if first.startswith(('+', '-')) else f'+{first}'))
        if tag == 'dc':
            return e(f'DC {parts[1] if len(parts) > 1 and parts[1] else first}')
        if tag == 'chance':
            return e(parts[1] if len(parts) > 1 and parts[1] else f'{first} percent')
        if tag == 'recharge':
            return e(f'(Recharge {first}–6)' if first and first != '6' else '(Recharge 6)')
        if tag in ('scaledice', 'scaledamage'):
            return e(parts[3] if len(parts) > 3 and parts[3] else (parts[2] if len(parts) > 2 else first))
        if tag == 'atk' or tag == 'atkr':
            words = {'m': 'Melee', 'r': 'Ranged', 'mw': 'Melee Weapon', 'rw': 'Ranged Weapon',
                     'ms': 'Melee Spell', 'rs': 'Ranged Spell', 'mw,rw': 'Melee or Ranged Weapon',
                     'ms,rs': 'Melee or Ranged Spell', 'm,r': 'Melee or Ranged'}
            kind = words.get(first, first)
            return f'<i>{e(kind)} {"Attack Roll" if tag == "atkr" else "Attack"}:</i>'
        if tag == 'h':
            return '<i>Hit:</i> '
        if tag == 'm':
            return '<i>Miss:</i> '
        if tag == 'hom':
            return '<i>Hit or Miss:</i> '
        if tag == 'actSave':
            return f'<i>{e(ABILITIES.get(first, first))} Saving Throw:</i>'
        acts = {'actSaveFail': 'Failure:', 'actSaveSuccess': 'Success:',
                'actSaveSuccessOrFail': 'Failure or Success:', 'actTrigger': 'Trigger:',
                'actResponse': 'Response:'}
        if tag in acts:
            return f'<i>{acts[tag]}</i>'
        if tag == 'actSaveFailBy':
            return f'<i>Failure by {e(first)} or More:</i>'
        if tag == 'hitYourSpellAttack':
            return e(first or 'your spell attack modifier')
        if tag == 'dcYourSpellSave':
            return e(first or 'your spell save DC')
        if tag in ('filter', 'book', 'adventure', '5etools', 'footnote', 'help', 'loader',
                   'color', 'style', 'font', 'unit', 'tip', 'coinflip', 'area', 'homebrew',
                   'ability', 'savingThrow', 'skillCheck', 'initiative', 'cite', 'comic'):
            return e(first)
        if tag == 'link':
            url = parts[1] if len(parts) > 1 else first
            return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{e(first)}</a>'
        # Entity references: name|source|display (with exceptions).
        ix = TAG_DISPLAY_ARG.get(tag, 2)
        display = parts[ix] if len(parts) > ix and parts[ix] else first
        page = TAG_PAGES.get(tag)
        if tag == 'class' or tag == 'subclass':
            page = 'classes.html'
        if not page:
            return e(display)
        src = parts[1] if len(parts) > 1 and parts[1] and tag != 'deity' else \
            TAG_DEFAULT_SOURCES.get(tag, 'PHB')
        if tag == 'deity':
            href = f'{page}#{enc(first)}_{enc(parts[1] if len(parts) > 1 and parts[1] else "forgotten realms")}_{enc(parts[2] if len(parts) > 2 and parts[2] else "PHB")}'
        else:
            href = f'{page}#{enc(first)}_{enc(src)}'
        return f'<a href="{self.site}{href}" target="_blank" rel="noopener">{e(display)}</a>'

    # Block entries.

    def entries(self, ents, depth=0):
        if ents is None:
            return ''
        if not isinstance(ents, list):
            ents = [ents]
        return ''.join(self.entry(x, depth) for x in ents)

    def entry(self, x, depth=0):
        if isinstance(x, str):
            return f'<p>{self.inline(x)}</p>'
        if isinstance(x, (int, float)):
            return f'<p>{x}</p>'
        if not isinstance(x, dict):
            return ''
        t = x.get('type', 'entries')
        name = x.get('name')
        if t in ('entries', 'section', 'inset', 'insetReadaloud', 'variant', 'variantInner',
                 'variantSub', 'optfeature', 'flowBlock', 'flowchart', 'homebrew'):
            body = x.get('entries', [])
            if not name:
                inner = self.entries(body, depth + 1)
                return f'<div class="tip-inset">{inner}</div>' if t.startswith('inset') else inner
            title = f'<b><i>{self.inline(name)}.</i></b> '
            if body and isinstance(body[0], str):
                head = f'<p>{title}{self.inline(body[0])}</p>'
                return head + self.entries(body[1:], depth + 1)
            return f'<p>{title}</p>' + self.entries(body, depth + 1)
        if t == 'list':
            items = ''.join(f'<li>{self.list_item(it, depth)}</li>' for it in x.get('items', []))
            return f'<ul>{items}</ul>'
        if t == 'options':
            items = ''.join(f'<li>{self.list_item(it, depth)}</li>' for it in x.get('entries', []))
            return f'<ul>{items}</ul>'
        if t == 'table':
            return self.table(x)
        if t in ('inline', 'inlineBlock'):
            return ''.join(self.inline(i) if isinstance(i, str) else self.entry(i, depth)
                           for i in x.get('entries', []))
        if t == 'quote':
            by = f'<p>— {self.inline(x["by"])}</p>' if x.get('by') else ''
            return f'<blockquote>{self.entries(x.get("entries"), depth + 1)}{by}</blockquote>'
        if t in ('item', 'itemSub', 'itemSpell'):
            return f'<p>{self.list_item(x, depth)}</p>'
        if t in ('refClassFeature', 'refSubclassFeature', 'refOptionalfeature'):
            ref = x.get('classFeature') or x.get('subclassFeature') or x.get('optionalfeature') or ''
            return f'<p>{self.inline(strip_src(ref))}</p>'
        if t in ('abilityDc', 'abilityAttackMod'):
            abil = ' or '.join(ABILITIES.get(a, a) for a in x.get('attributes', []))
            what = 'save DC' if t == 'abilityDc' else 'attack modifier'
            base = '8 + ' if t == 'abilityDc' else ''
            return (f'<p class="tip-center"><b>{self.inline(x.get("name", ""))} {what}</b> = '
                    f'{base}your proficiency bonus + your {abil} modifier</p>')
        if t == 'abilityGeneric':
            return f'<p class="tip-center">{self.inline(x.get("text", ""))}</p>'
        if t == 'image':
            href = x.get('href', {})
            if href.get('type') == 'internal':
                src = copy_image(self.ds.edition, href.get('path', ''))
                src = self.baseurl + src if src else None
            else:
                src = href.get('url')
            if src:
                alt = html.escape(x.get('title', ''))
                return f'<p class="tip-center"><img src="{html.escape(src)}" alt="{alt}"></p>'
            return ''
        if t == 'hr':
            return '<hr>'
        if t == 'link':
            return f'<p>{self.inline(x.get("text", ""))}</p>'
        if t in ('statblock', 'statblockInline'):
            return f'<p><i>[{html.escape(x.get("name") or x.get("tag") or "stat block")}]</i></p>'
        if 'entries' in x:
            return self.entries(x['entries'], depth + 1)
        if 'entry' in x:
            return self.entry(x['entry'], depth + 1)
        return ''

    def list_item(self, it, depth):
        if isinstance(it, str):
            return self.inline(it)
        if not isinstance(it, dict):
            return ''
        if it.get('type') in ('item', 'itemSub', 'itemSpell') or ('name' in it and 'type' not in it):
            body = it.get('entries') if 'entries' in it else it.get('entry')
            if not isinstance(body, list):
                body = [body] if body is not None else []
            head = f'<b>{self.inline(it.get("name", ""))}</b> ' if it.get('name') else ''
            first = self.inline(body[0]) if body and isinstance(body[0], str) else ''
            rest = self.entries(body[1:] if first else body, depth + 1)
            return head + first + rest
        if it.get('type') in ('refClassFeature', 'refSubclassFeature', 'refOptionalfeature'):
            ref = it.get('classFeature') or it.get('subclassFeature') or it.get('optionalfeature') or ''
            if it.get('type') == 'refOptionalfeature':
                return self.inline(f'{{@optfeature {ref}}}')
            return self.inline(strip_src(ref))
        return self.entry(it, depth)

    def table(self, x):
        out = ['<table>']
        if x.get('caption'):
            out.append(f'<caption>{self.inline(x["caption"])}</caption>')
        if x.get('colLabels'):
            out.append('<tr>' + ''.join(f'<th>{self.inline(c)}</th>' for c in x['colLabels']) + '</tr>')
        for row in x.get('rows', []):
            if isinstance(row, dict):
                row = row.get('row', [])
            out.append('<tr>' + ''.join(f'<td>{self.cell(c)}</td>' for c in row) + '</tr>')
        out.append('</table>')
        return ''.join(out)

    def cell(self, c):
        if isinstance(c, dict) and c.get('type') == 'cell':
            r = c.get('roll', {})
            if 'exact' in r:
                return str(r['exact'])
            if 'min' in r:
                return f'{r["min"]}–{r["max"]}'
            return self.entry(c.get('entry', ''))
        if isinstance(c, str):
            return self.inline(c)
        if isinstance(c, (int, float)):
            return str(c)
        return self.entry(c)

    # Entry headers.

    def meta(self, e):
        """A short description line for an entry, e.g. "1st-level evocation"."""
        d, kind = e['data'], e['kind']
        if kind == 'spell':
            lvl, school = d.get('level', 0), SCHOOLS.get(d.get('school'), d.get('school', ''))
            s = f'{school.capitalize()} cantrip' if lvl == 0 else f'{ordinal(lvl)}-level {school}'
            if d.get('meta', {}).get('ritual'):
                s += ' (ritual)'
            return s
        if kind in ('classFeature', 'classPart'):
            p = e.get('parent', e)['data']
            what = f'{p["className"]} {p.get("level", "")}'.strip()
            return f'{p["name"]} ({what})' if kind == 'classPart' else what
        if kind in ('subclassFeature', 'subclassPart'):
            p = e.get('parent', e)['data']
            what = f'{p["className"]} ({p.get("subclassShortName", "")}) {p.get("level", "")}'.strip()
            return f'{p["name"]} — {what}' if kind == 'subclassPart' else what
        if kind == 'feat':
            cat = FEAT_CATEGORIES.get(d.get('category'), 'Feat')
            pre = self.prerequisite(d)
            return f'{cat}; prerequisite: {pre}' if pre else cat
        if kind == 'optionalfeature':
            types = [FEATURE_TYPES.get(t, t) for t in d.get('featureType', [])]
            s = ', '.join(dict.fromkeys(types)) or 'Optional feature'
            pre = self.prerequisite(d)
            return f'{s}; prerequisite: {pre}' if pre else s
        if kind == 'racetrait':
            return f'{e["parent"]["name"]} trait' if e['parent']['kind'] == 'race' else \
                f'{e.get("raceName", "")} ({e["parent"]["name"]}) trait'
        if kind in ('race', 'subrace'):
            return 'Species' if self.ds.edition == '2024' and self.ds.is_modern(e) else 'Race'
        if kind == 'background':
            return 'Background'
        if kind == 'backgroundPart':
            return f'{e["parent"]["name"]} background'
        if kind in ('item', 'baseitem'):
            return self.item_meta(d)
        if kind in ('class', 'subclass'):
            return 'Class' if kind == 'class' else f'{d.get("className")} subclass'
        return kind.capitalize() if kind not in ('variantrule',) else 'Rule'

    def prerequisite(self, d):
        out = []
        for p in d.get('prerequisite', []):
            for k, v in p.items():
                if k == 'level':
                    lv = v.get('level') if isinstance(v, dict) else v
                    cls = v.get('class', {}).get('name') if isinstance(v, dict) else None
                    out.append(f'{ordinal(lv)}-level {cls}' if cls else f'Level {lv}+')
                elif k == 'ability':
                    out.append(' or '.join(f'{ABILITIES.get(a, a)} {n}+' for x in v for a, n in x.items()))
                elif k == 'race':
                    out.append(' or '.join(r['name'].title() + (f' ({r["subrace"]})' if r.get('subrace') else '')
                                           for r in v))
                elif k == 'spellcasting' or k == 'spellcasting2020' or k == 'spellcastingFeature':
                    out.append('Spellcasting or Pact Magic feature')
                elif k == 'pact':
                    out.append(f'Pact of the {v}')
                elif k == 'patron':
                    out.append(f'{v} patron')
                elif k == 'spell':
                    out.append(', '.join(strip_src(s).split('#')[0].title() for s in v))
                elif k == 'feature':
                    out.append(', '.join(v))
                elif k == 'feat':
                    out.append(', '.join(strip_src(f).title() for f in v))
                elif k == 'proficiency':
                    out.append(' or '.join(f'{p} proficiency' for x in v for p in x.values()))
                elif k == 'other':
                    out.append(v)
                elif k == 'otherSummary':
                    out.append(v.get('entrySummary') or v.get('entry', ''))
        return self.inline('; '.join(o for o in out if o))

    def item_meta(self, d):
        bits = []
        typ = ITEM_TYPES.get(strip_src(d.get('type', '')), '')
        if d.get('wondrous'):
            typ = 'Wondrous item'
        if d.get('weaponCategory'):
            typ = f'{d["weaponCategory"].capitalize()} {typ.lower() or "weapon"}'
        if typ:
            bits.append(typ)
        if d.get('rarity') and d['rarity'] not in ('none', 'unknown'):
            bits.append(d['rarity'])
        if d.get('reqAttune'):
            bits.append('requires attunement' + (f' {d["reqAttune"]}' if isinstance(d['reqAttune'], str) else ''))
        s = ', '.join(bits)
        stats = []
        if d.get('dmg1'):
            stats.append(f'{d["dmg1"]} {DMG_TYPES.get(d.get("dmgType"), "")}'.strip())
        if d.get('ac'):
            stats.append(f'AC {d["ac"]}')
        props = [ITEM_PROPS.get(strip_src(p), strip_src(p)) for p in d.get('property', [])
                 if isinstance(p, str)]
        if 'versatile' in props and d.get('dmg2'):
            props[props.index('versatile')] = f'versatile ({d["dmg2"]})'
        if d.get('range'):
            props.append(f'range {d["range"]} ft.')
        if d.get('mastery'):
            props.append('mastery: ' + ', '.join(strip_src(m) for m in d['mastery']))
        stats += props
        return s + ('; ' + ', '.join(stats) if stats else '')

    def spell_header(self, d):
        rows = []
        times = d.get('time', [])
        if times:
            rows.append(('Casting Time', ' or '.join(
                f'{t.get("number", "")} {t.get("unit", "")}'.strip() +
                (f', {t["condition"]}' if t.get('condition') else '') for t in times)))
        r = d.get('range', {})
        dist = r.get('distance', {})
        if r.get('type') == 'point':
            rng = {'self': 'Self', 'touch': 'Touch', 'sight': 'Sight', 'unlimited': 'Unlimited'}.get(
                dist.get('type'), f'{dist.get("amount", "")} {dist.get("type", "")}')
        elif r.get('type') in ('special',):
            rng = 'Special'
        elif r:
            rng = f'Self ({dist.get("amount", "")}-{dist.get("type", "").rstrip("s")} {r["type"]})'
        else:
            rng = ''
        rows.append(('Range', rng))
        c = d.get('components', {})
        comp = [k.upper() for k in ('v', 's') if c.get(k)]
        if c.get('m'):
            m = c['m']
            comp.append(f'M ({m["text"] if isinstance(m, dict) else m})' if m is not True else 'M')
        rows.append(('Components', ', '.join(comp)))
        durs = []
        for du in d.get('duration', []):
            ty = du.get('type')
            if ty == 'instant':
                durs.append('Instantaneous')
            elif ty == 'timed':
                dd = du.get('duration', {})
                n, unit = dd.get('amount', 1), dd.get('type', '')
                s = f'{n} {unit}{"s" if n != 1 else ""}'
                durs.append(f'Concentration, up to {s}' if du.get('concentration') else s)
            elif ty == 'permanent':
                ends = du.get('ends', [])
                durs.append('Until ' + ' or '.join({'dispel': 'dispelled', 'trigger': 'triggered',
                                                    'discharge': 'discharged'}.get(x, x) for x in ends)
                            if ends else 'Permanent')
            elif ty == 'special':
                durs.append('Special')
        rows.append(('Duration', ' or '.join(durs)))
        return ''.join(f'<div><b>{k}:</b> {self.inline(v)}</div>' for k, v in rows if v)

    def tip(self, e):
        """The full tooltip HTML for an entry."""
        d = e['data']
        out = [f'<div class="tip-head"><span class="tip-name">{html.escape(e["name"])}</span>'
               f'<span class="tip-src">{html.escape(e["source"])}'
               f'{" p. " + str(d["page"]) if d.get("page") else ""}</span></div>']
        meta = self.meta(e)
        if meta:
            out.append(f'<div class="tip-meta">{meta}</div>')
        if e['kind'] == 'spell':
            out.append(f'<div class="tip-stats">{self.spell_header(d)}</div>')
        body = d.get('entries')
        if body is None and 'entry' in d:
            body = [d['entry']]
        out.append(self.entries(body or []))
        if e['kind'] == 'spell' and d.get('entriesHigherLevel'):
            out.append(self.entries(d['entriesHigherLevel']))
        return ''.join(out)


# ── URLs ────────────────────────────────────────────────────────────────────

def parse_feature_ref(ref):
    """Parses a class's classFeatures item: "Name|Class|ClassSrc|Level[|Src]"."""
    if isinstance(ref, dict):
        ref, gain = ref.get('classFeature', ''), ref.get('gainSubclassFeature', False)
    else:
        gain = False
    p = ref.split('|')
    p += [''] * (5 - len(p))
    return {'name': p[0], 'level': int(p[3] or 0), 'source': p[4] or p[2] or 'PHB', 'gain': gain}


def entry_url(e, ds):
    site = SITES[ds.edition]
    d, kind = e['data'], e['kind']
    if 'parent' in e:
        return entry_url(e['parent'], ds)
    gen = lambda page: f'{site}{page}#{enc(e["name"])}_{enc(e["source"])}'  # noqa: E731
    if kind in ('classFeature', 'subclassFeature'):
        cls = ds.classes.get((norm(d['className']), norm(d.get('classSource') or 'PHB')))
        url = f'{site}classes.html#{enc(d["className"])}_{enc(d.get("classSource") or "PHB")}'
        if not cls:
            return url
        level = int(d.get('level') or 0)
        feats = [parse_feature_ref(f) for f in cls.get('classFeatures', [])]
        at_level = [f for f in feats if f['level'] == level]
        state = []
        if kind == 'subclassFeature':
            state.append(f'sub_{enc(d["subclassShortName"])}_{enc(d.get("subclassSource") or "PHB")}=b1')
            ix = next((i for i, f in enumerate(at_level) if f['gain']), None)
        else:
            ix = next((i for i, f in enumerate(at_level)
                       if norm(f['name']) == norm(e['name']) and norm(f['source']) == norm(e['source'])), None)
        if ix is not None:
            state.append(f'feature=s{level - 1}-{ix}')
        return url + (',state:' + '~'.join(state) if state else '')
    if kind == 'class':
        return gen('classes.html')
    if kind == 'subclass':
        return (f'{site}classes.html#{enc(d["className"])}_{enc(d.get("classSource") or "PHB")},'
                f'state:sub_{enc(d.get("shortName") or e["name"])}_{enc(e["source"])}=b1')
    if kind == 'subrace':
        race, sub = d.get('raceName', ''), e['name']
        m = re.match(r'^(.*?)(\(.*?\))$', race)
        name = f'{m.group(1)}({m.group(2)[1:-1]}; {sub})' if m else f'{race} ({sub})'
        return f'{site}races.html#{enc(name)}_{enc(e["source"])}'
    pages = {'spell': 'spells.html', 'feat': 'feats.html', 'optionalfeature': 'optionalfeatures.html',
             'race': 'races.html', 'background': 'backgrounds.html', 'item': 'items.html',
             'baseitem': 'items.html', 'action': 'actions.html', 'condition': 'conditionsdiseases.html',
             'disease': 'conditionsdiseases.html', 'status': 'conditionsdiseases.html',
             'variantrule': 'variantrules.html', 'language': 'languages.html'}
    if kind in pages:
        return gen(pages[kind])
    return None


# ── Site scanning ───────────────────────────────────────────────────────────

def read_page(path):
    text = path.read_text(encoding='utf-8')
    m = re.match(r'---[ \t]*\n(.*?\n)?---[ \t]*(?:\n|$)(.*)', text, re.S)
    if not m:
        return None, text
    try:
        fm = yaml.safe_load(m.group(1) or '')
    except yaml.YAMLError as ex:
        print(f'{path.relative_to(ROOT)}: bad front matter: {ex}', file=sys.stderr)
        fm = None
    return (fm if isinstance(fm, dict) else {}), m.group(2)


class Builder:
    def __init__(self, resolver, baseurl, verbose=False):
        self.resolver = resolver
        self.renderers = {ed: Renderer(ds, baseurl) for ed, ds in resolver.datasets.items()}
        self.entries = {}   # key -> {name, url, html}
        self.keys = {}      # id(entry) -> key
        self.pages = {}
        self.refs = {}      # ref -> key, from any page (for embedded GM notes)
        self.verbose = verbose
        self.unresolved = []
        self.resolved = 0

    def key_for(self, e):
        if id(e) in self.keys:
            return self.keys[id(e)]
        ds = self.resolver.datasets[e['edition']]
        d = e['data']
        bits = [e['edition'][2:], e['kind'], e['name'], e['source']]
        if d.get('className'):
            bits += [d['className'], d.get('subclassShortName', ''), str(d.get('level', ''))]
        if 'parent' in e:
            bits += [e['parent']['name'], e['parent']['data'].get('className', '')]
        base = re.sub(r'[^a-z0-9]+', '-', '-'.join(bits).lower()).strip('-')
        key, n = base, 2
        while key in self.entries:
            key, n = f'{base}-{n}', n + 1
        self.keys[id(e)] = key
        self.entries[key] = {'name': e['name'], 'url': entry_url(e, ds),
                             'html': self.renderers[e['edition']].tip(e)}
        return key

    def link(self, text, e, tips):
        key = self.key_for(e)
        tips.setdefault(key, None)
        url = self.entries[key]['url']
        t = html.escape(text, quote=False)
        if url:
            return (f'<a class="rule-ref" href="{html.escape(url)}" target="_blank" rel="noopener" '
                    f'data-tip="{key}">{t}</a>')
        return f'<span class="rule-ref" tabindex="0" data-tip="{key}">{t}</span>'

    def note(self, page, what, text, e):
        if e:
            self.resolved += 1
            if self.verbose:
                print(f'  {what}: {text!r} -> [{e["edition"]}] {e["kind"]} {e["name"]} ({e["source"]})')
        else:
            self.unresolved.append((page, what, text))

    def linkify(self, page, what, text, ctx, tips, ref=None, split=False):
        """Returns the HTML for a name (or, with split, a list of names), or
        None if nothing in it resolves."""
        text = str(text)
        if ref is not None:
            if str(ref).lower() == 'none':
                return None
            e = self.resolver.lookup_ref(str(ref), ctx)
            self.note(page, what, f'ref: {ref}', e)
            return self.link(text, e, tips) if e else None
        if split:
            pieces = split_list(text)
            out, any_hit = [], False
            for p in pieces:
                lead = p[:len(p) - len(p.lstrip())]
                name = p.strip()
                e = None
                if name:
                    if '|' in name:
                        e = self.resolver.lookup(name, ctx)
                        name = name.split('|')[0]
                    else:
                        e = self.find(clean_name(name), ctx)
                    self.note(page, what, p.strip(), e)
                out.append(lead + (self.link(name, e, tips) if e else html.escape(name, quote=False)))
                any_hit |= e is not None
            return ','.join(out) if any_hit else None
        # "Fighting Style (Archery)": the option chosen; "Sword cane (rapier)":
        # the base weapon.
        m = re.match(r'^[^()]+\(([^()]+)\)', text)
        paren_kinds = ['baseitem'] if ctx.kind == 'weapon' else ['optionalfeature']
        e = m and self.resolver.lookup(m.group(1).strip(), ctx, paren_kinds)
        if not e:
            e = self.find(clean_name(text), ctx)
        if e:
            self.note(page, what, text, e)
            return self.link(text, e, tips)
        # "Invocations: A, B, C" lists.
        m = re.match(r'^([^:()]+):\s*(.+)$', text)
        if m and ',' in m.group(2):
            inner = self.linkify(page, what, m.group(2), ctx, tips, split=True)
            if inner:
                prefix = m.group(1)
                head = self.find(clean_name(prefix), ctx)
                head_html = self.link(prefix, head, tips) if head else html.escape(prefix, quote=False)
                return f'{head_html}: {inner}'
        self.note(page, what, text, None)
        return None

    def find(self, name, ctx):
        """Looks up a cleaned name, then the parts of "Prefix: Name"."""
        if not name:
            return None
        e = self.resolver.lookup(name, ctx)
        if e:
            return e
        stripped = PREFIX_RE.sub('', name)
        if stripped != name:
            e = self.resolver.lookup(stripped, ctx)
            if e:
                return e
        if ':' in name:
            before, after = [s.strip() for s in name.split(':', 1)]
            e = self.resolver.lookup(after, ctx) or self.resolver.lookup(before, ctx)
            if e:
                return e
        # "Darkvision 90 ft.", "Javelin ×4"
        bare = re.sub(r'\s+[\u00d7x]?\d.*$', '', name)
        if bare != name:
            return self.find(bare, ctx)
        return None

    def charsheet(self, rel, fm, body):
        cs = fm.get('cs') or {}
        classes = re.findall(r'[A-Za-z][A-Za-z\' ]*', str(cs.get('class', '')))
        classes = [c.strip() for c in classes if c.strip()]
        sub = str(cs.get('subclass') or '')
        known = {norm(c['name']) for ds in self.resolver.datasets.values() for c in ds.classes.values()}
        for f in cs.get('features') or []:
            if isinstance(f, dict) and norm(f.get('source', '')) in known:
                classes.append(f['source'])
        # Pick out class names from free text like "Gestalt: Savage Bard 4 / ..."
        words = norm(' '.join(classes) + ' ' + sub)
        classes += [k for k in known if words_in(k, words)]
        try:
            level = int(cs.get('level'))
        except (TypeError, ValueError):
            level = None
        ctx = Context(cs.get('rules', 2014), classes, sub, cs.get('race', ''), level=level)
        ctx.race_ids = self.resolver.races(cs.get('race', ''), ctx.edition)
        out, tips = {}, {}

        def put(key, val):
            if val is not None:
                out[key] = val

        for f in cs.get('features') or []:
            if not isinstance(f, dict) or 'name' not in f:
                continue
            c = ctx.with_(label=f.get('source', ''), kind='feature')
            put(f'feature:{f["name"]}', self.linkify(rel, 'feature', f['name'], c, tips, f.get('ref')))
        for s in cs.get('spells') or []:
            if isinstance(s, dict) and s.get('list'):
                put(f'spells:{s["list"]}', self.linkify(rel, 'spell', s['list'], ctx.with_(kind='spell'),
                                                        tips, split=True))
        for w in cs.get('weapons') or []:
            if isinstance(w, dict) and w.get('name'):
                put(f'weapon:{w["name"]}', self.linkify(rel, 'weapon', w['name'], ctx.with_(kind='weapon'),
                                                        tips, w.get('ref')))
        for item in cs.get('equipment') or []:
            text = str(item)
            e = self.resolver.lookup(clean_name(text), ctx.with_(kind='equipment'))
            if e:
                self.note(rel, 'equipment', text, e)
                out[f'equipment:{text}'] = self.link(text, e, tips)
        for skill in ['Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception', 'History',
                      'Insight', 'Intimidation', 'Investigation', 'Medicine', 'Nature', 'Perception',
                      'Performance', 'Persuasion', 'Religion', 'Sleight of Hand', 'Stealth', 'Survival']:
            e = self.resolver.lookup(skill, ctx.with_(kind='skill'))
            if e:
                out[f'skill:{skill}'] = self.link(skill, e, tips)
        traits = cs.get('traits') or {}
        for field, kind in (('senses', 'sense'), ('languages', 'language'),
                            ('condition_immunities', 'condition')):
            if traits.get(field):
                html_ = self.list_traits(str(traits[field]), ctx.with_(kind=kind), tips)
                if html_:
                    out[f'{field}:{traits[field]}'] = html_
        return ctx, out, tips

    def list_traits(self, text, ctx, tips):
        """Links the recognizable names in a trait line ("Darkvision 90 ft.;
        ..."), silently: these are free text, so misses are expected."""
        out, hit = [], False
        for piece in re.split(r'([,;])', text):
            if piece in (',', ';'):
                out.append(piece)
                continue
            lead = piece[:len(piece) - len(piece.lstrip())]
            name = piece.strip()
            m = re.match(r"^([A-Za-z' ]+?)(\s+\d.*|\s*\(.*)?$", name)
            e = self.resolver.lookup(m.group(1), ctx) if m else None
            if e:
                hit = True
                out.append(lead + self.link(m.group(1), e, tips) + html.escape(m.group(2) or '', quote=False))
            else:
                out.append(html.escape(piece, quote=False))
        return ''.join(out) if hit else None

    def includes(self, rel, body, fm, ctx, refs, tips):
        for m in re.finditer(r'\{%-?\s*include\s+rule\s+(.*?)-?%\}', body):
            am = re.search(r'ref\s*=\s*"([^"]*)"|ref\s*=\s*\'([^\']*)\'', m.group(1))
            if not am:
                continue
            ref = am.group(1) if am.group(1) is not None else am.group(2)
            e = self.resolver.lookup_ref(ref, ctx.with_(kind='ref'))
            self.note(rel, 'include', ref, e)
            if e:
                key = self.key_for(e)
                refs[ref] = key
                self.refs.setdefault(ref, key)
                tips.setdefault(key, None)

    def scan(self):
        for path in sorted(PAGES.rglob('*.md')):
            text = path.read_text(encoding='utf-8')
            if 'charsheet' not in text and 'include rule' not in text:
                continue
            fm, body = read_page(path)
            if fm is None:
                continue
            rel = path.relative_to(ROOT).as_posix()
            is_sheet = fm.get('layout') == 'charsheet' and fm.get('cs')
            has_includes = 'include rule' in body
            if not (is_sheet or has_includes):
                continue
            if self.verbose:
                print(rel)
            if is_sheet:
                ctx, fields, tips = self.charsheet(rel, fm, body)
            else:
                ctx, fields, tips = Context(fm.get('rules', 2014)), {}, {}
            refs = {}
            self.includes(rel, body, fm, ctx, refs, tips)
            self.pages[rel] = {'html': fields, 'refs': refs, 'tips': list(tips)}

    def write(self):
        OUT_DATA.parent.mkdir(exist_ok=True)
        data = {'entries': self.entries, 'pages': self.pages, 'refs': self.refs}
        OUT_DATA.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--no-clone', action='store_true', help='never clone missing repositories')
    ap.add_argument('-v', '--verbose', action='store_true', help='list every resolved reference')
    ap.add_argument('-q', '--quiet', action='store_true', help='do not list unresolved names')
    ap.add_argument('--lookup', metavar='NAME', help='look up a name or reference, and print it')
    ap.add_argument('--edition', default='2014', choices=EDITIONS, help='edition for --lookup')
    args = ap.parse_args()

    if not args.no_clone and (PAGES / 'gm').exists():
        for ed in EDITIONS:
            for kind in ('src', 'img'):
                clone(ed, kind)
    datasets = {ed: Dataset(ed) for ed in EDITIONS if (repo_dir(ed, 'src') / 'data').exists()}
    if not datasets:
        print('No 5etools data in _external/; nothing to do.', file=sys.stderr)
        return 0
    resolver = Resolver(datasets)
    cfg = yaml.safe_load((ROOT / '_config.yml').read_text()) or {}
    builder = Builder(resolver, cfg.get('baseurl', ''), args.verbose)

    if args.lookup:
        e = resolver.lookup_ref(args.lookup, Context(args.edition))
        if not e:
            print('Not found.')
            return 1
        key = builder.key_for(e)
        print(f'[{e["edition"]}] {e["kind"]} {e["name"]} ({e["source"]})')
        print(builder.entries[key]['url'])
        print(re.sub(r'<[^>]+>', ' ', builder.entries[key]['html']))
        return 0

    if OUT_IMG.exists():
        shutil.rmtree(OUT_IMG)
    builder.scan()
    builder.write()
    print(f'{OUT_DATA.relative_to(ROOT)}: {len(builder.entries)} entries, '
          f'{builder.resolved} references resolved, {len(builder.unresolved)} not.', file=sys.stderr)
    if builder.unresolved and not args.quiet:
        print('\nNot found (homebrew? misspelled? add `ref:` or `ref: none`):', file=sys.stderr)
        last = None
        for page, what, text in builder.unresolved:
            if page != last:
                print(f'  {page}', file=sys.stderr)
                last = page
            print(f'    {what}: {text}', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
