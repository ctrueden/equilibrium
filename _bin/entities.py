"""
entities.py — Index of wiki entities (dossiers, locales, orgs, creatures,
relics) by the names they are likely to be mentioned by in session text.

Names come from each page's front matter:
- `title` (e.g. "Atlas, Titan of Endurance"), and `nav-title`
- the title without its epithet ("Atlas") or quoted nickname
  ('Belarra "Bela" Underleaf' -> "Belarra Underleaf", "Bela")
- `aliases`: alternate names and known misspellings (e.g. the spellings
  GM Assistant transcriptions tend to produce)
- for people (dossiers): the first or last name alone, when unambiguous
  and not an ordinary word (so "Kerwin" and "Mallory", but not "Holly")

Names that would map to more than one page are ambiguous, and are not
used for linking.
"""

import re
from pathlib import Path

import yaml

ENTITY_DIRS = ['dossiers', 'locales', 'orgs', 'creatures', 'relics']

HONORIFICS = {'king', 'queen', 'lord', 'lady', 'sir', 'dame', 'captain',
              'prince', 'princess', 'duke', 'duchess', 'count', 'countess',
              'contessa', 'master', 'mistress', 'father', 'mother', 'brother',
              'sister', 'saint', 'st.', 'the', 'doctor', 'dr.', 'professor'}

# Words that are names of entities but far more often just words.
# These are never linked or treated as names by themselves.
COMMON_WORDS = {
    'the', 'a', 'an', 'and', 'of', 'in', 'on', 'at', 'to', 'for', 'with',
    'he', 'she', 'they', 'it', 'his', 'her', 'their', 'its', 'we', 'i', 'you',
}


def read_front_matter(path):
    text = Path(path).read_text(encoding='utf-8')
    m = re.match(r'---\s*\n(.*?)\n---\s*\n', text, re.S)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, text[m.end():]


class Entity:
    def __init__(self, kind, slug, title, front):
        self.kind = kind
        self.slug = slug
        self.title = title
        self.front = front

    @property
    def link(self):
        return f'../{self.kind}/{self.slug}'

    def __repr__(self):
        return f'{self.kind}/{self.slug}'


def name_variants(entity):
    """Yield (name, strength) pairs: 'full' names are always safe to link;
    'short' names (first names) only when unambiguous."""
    fm = entity.front
    titles = [entity.title]
    if fm.get('nav-title'):
        titles.append(str(fm['nav-title']))
    for t in titles:
        yield t, 'full'
        base = t.split(',')[0].strip()           # drop ", Titan of Endurance"
        yield base, 'full'
        nick = re.search(r'"([^"]+)"', base)
        if nick:
            yield nick.group(1), 'full'
            base = re.sub(r'\s*"[^"]+"\s*', ' ', base).strip()
            yield base, 'full'
        base = re.sub(r'\s*\([^)]*\)', '', base).strip()  # drop "(the elder)"
        yield base, 'full'
        words = base.split()
        while words and words[0].lower() in HONORIFICS:
            words = words[1:]
            yield ' '.join(words), 'full'
        if entity.kind == 'dossiers' and len(words) > 1:
            yield words[0], 'short'
            if all(w[:1].isupper() for w in words):
                yield words[-1], 'short'  # surname, e.g. "Mallory"

    aliases = fm.get('aliases') or []
    if isinstance(aliases, str):
        aliases = [aliases]
    for a in aliases:
        yield str(a), 'alias'


def english_words(root):
    """Lowercase words that are ordinary vocabulary: those in the system
    dictionary (if any), plus those the wiki uses more often in lowercase
    than capitalized (GM notes are excluded: they are often informal)."""
    words = set()
    for d in ('/usr/share/dict/words', '/usr/share/dict/american-english'):
        if Path(d).exists():
            words.update(w.strip() for w in open(d, encoding='utf-8', errors='ignore')
                         if w.strip().islower())
            break
    lower, upper = {}, {}
    pages = Path(root) / '_pages'
    for path in pages.rglob('*.md'):
        if 'gm' in path.relative_to(pages).parts:
            continue
        # Skip slugs, paths and URLs (kerwin-ulvas, dossiers/freki, freki.jpg).
        text = re.sub(r"\S*[/_]\S*|\S+\.(?:jpe?g|png|gif|webp|md|html)\b", " ", path.read_text(encoding='utf-8'))
        for w in re.findall(r"(?<![\w\-])[A-Za-z][a-z']+(?![\w\-])", text):
            table = lower if w[0].islower() else upper
            table[w.lower()] = table.get(w.lower(), 0) + 1
    words.update(w for w, n in lower.items() if n >= 3 and n > upper.get(w, 0))
    return words


class Index:
    def __init__(self, root):
        self.root = Path(root)
        self.vocabulary = english_words(root)
        self.entities = []
        self.by_name = {}       # name -> set of entities (full names)
        self.by_short = {}      # name -> set of entities (first names)
        for kind in ENTITY_DIRS:
            for path in sorted((self.root / '_pages' / kind).glob('*.md')):
                if path.stem == 'index':
                    continue
                fm, _ = read_front_matter(path)
                title = str(fm.get('title') or path.stem)
                e = Entity(kind, path.stem, title, fm)
                self.entities.append(e)
                for name, strength in name_variants(e):
                    name = name.strip()
                    if not name or name.lower() in COMMON_WORDS:
                        continue
                    if len(name) < 3 and strength != 'alias':
                        continue  # explicit aliases may be short, e.g. "Oz"
                    if strength == 'alias':
                        strength = 'full'
                    if strength == 'short' and name.lower() in self.vocabulary:
                        continue  # e.g. "Holly", "Victor", "Great"
                    target = self.by_name if strength == 'full' else self.by_short
                    target.setdefault(name, set()).add(e)

    def lookup(self, name):
        """Return the unique entity for a name, or None."""
        hits = self.by_name.get(name)
        if hits is None:
            hits = self.by_short.get(name)
            if hits and name in self.by_name:
                return None
        if hits and len(hits) == 1:
            return next(iter(hits))
        return None

    def linkable_names(self):
        """All unambiguous names, longest first (so longer names win)."""
        names = {}
        for table in (self.by_short, self.by_name):  # full names override
            for name, hits in table.items():
                if len(hits) == 1:
                    names[name] = next(iter(hits))
                elif name in names:
                    del names[name]
        # A first name that is also someone's full name is ambiguous.
        for name, hits in self.by_short.items():
            full = self.by_name.get(name)
            if full and (len(full) > 1 or full != hits):
                names.pop(name, None)
        return sorted(names.items(), key=lambda kv: -len(kv[0]))

    def ambiguous(self):
        out = {}
        for table in (self.by_name, self.by_short):
            for name, hits in table.items():
                if len(hits) > 1:
                    out.setdefault(name, set()).update(hits)
        return out

    def all_names(self):
        return set(self.by_name) | set(self.by_short)
