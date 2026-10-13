#!/usr/bin/env -S python3 -P
"""
Add an image to the GM image gallery (_pages/gm/gallery.md), with tags.

The image is downloaded into the local image cache (as _bin/cache-images.py
does), then shown to a local vision model (via Ollama) to suggest tags, which
are merged with any tags given on the command line.

Usage:
  _bin/ingest-image.py IMAGE [SOURCE] [TAG...]
  _bin/ingest-image.py --retag [TAG...]     # suggest more tags for existing images
  _bin/ingest-image.py --prune              # remove images already used on pages

Each argument is one of:
  - an image URL (i.pinimg.com, or a path ending in an image extension)
  - a bare Pinterest image hash, e.g. 00fe9dcf57bf11a5177df5dc24186615,
    expanded to https://i.pinimg.com/originals/00/fe/9d/<hash>.<ext>
    (the extension is found by trying jpg, png, webp and gif)
  - a Pinterest pin ID (11+ digits), e.g. 1028087421185063112,
    meaning https://www.pinterest.com/pin/<id>/
  - any other URL: the page the image came from
  - anything else: a tag

Given only a source page, the image is scraped from it (the pin's image for
Pinterest, otherwise the page's og:image). Given two URLs, the image is the
one that looks like an image (or whose server says it is one).

Examples:
  _bin/ingest-image.py 00fe9dcf57bf11a5177df5dc24186615 stone giant male necklace tattoos
  _bin/ingest-image.py 1028087421185063112 stone giant
  _bin/ingest-image.py https://www.deviantart.com/... https://images-wixmp-.../x.jpg elf

If the image is already in the gallery, the new tags are merged into its
entry. If it is already used on a wiki page, nothing is added (see --force).

Tags are lowercase and singular, with hyphens joining multi-word tags
(stone-giant). The model's suggestions favor tags the gallery already uses.

Options:
  -n, --dry-run     Show what would change without writing anything
  --no-ai           Skip the vision model; use only the given tags
  --model NAME      Ollama vision model with which to suggest tags
                    (default: $INGEST_IMAGE_MODEL, else Gemma 4 12B)
  --force           Add the image even if a wiki page already uses it
  --retag [TAG...]  Run the model over existing gallery images (those having
                    all the given tags, or all of them), adding suggestions
  --prune           Remove gallery images that a wiki page already uses

The Ollama server is $OLLAMA_HOST (default http://localhost:11434).
"""

import argparse
import base64
import collections
import importlib.util
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

import yaml

SITE_ROOT = Path(__file__).resolve().parent.parent
PAGES = SITE_ROOT / '_pages'
GALLERY = PAGES / 'gm' / 'gallery.md'
DEFAULT_MODEL = 'hf.co/google/gemma-4-12B-it-qat-q4_0-gguf'
OLLAMA = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
if '://' not in OLLAMA:
    OLLAMA = 'http://' + OLLAMA
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

PIN_HASH = re.compile(r'^[0-9a-f]{32}$')
PIN_ID = re.compile(r'^[0-9]{10}[0-9]+$')
PIN_URL = re.compile(r'pinterest\.[a-z.]+/pin/(?:[^/]*--)?(\d+)')
PINIMG = re.compile(r'//i\.pinimg\.com/[^/]+/(?:[0-9a-f]{2}/){3}([0-9a-f]{32})\.(\w+)')
IMAGE_EXTS = ('jpg', 'png', 'webp', 'gif')  # in order of commonality
IMAGE_PATH = re.compile(r'\.(jpe?g|png|webp|gif|avif)$', re.I)

# Reuse the cache layout of cache-images.py (not importable by name: hyphen).
_spec = importlib.util.spec_from_file_location('cache_images', SITE_ROOT / '_bin' / 'cache-images.py')
cache_images = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cache_images)


def log(msg):
    print(msg, file=sys.stderr)


# -- Fetching --

def request(url, method='GET'):
    req = urllib.request.Request(url, method=method, headers={'User-Agent': USER_AGENT})
    return urllib.request.urlopen(req, timeout=30)


def exists(url):
    """Whether the URL answers a HEAD request successfully."""
    try:
        with request(url, 'HEAD') as r:
            return r.status == 200
    except (urllib.error.URLError, TimeoutError):
        return False


def is_image_url(url):
    """Guess from the URL alone whether it is an image."""
    parsed = urlparse(url)
    return parsed.netloc == 'i.pinimg.com' or bool(IMAGE_PATH.search(parsed.path))


def serves_image(url):
    try:
        with request(url, 'HEAD') as r:
            return r.headers.get('Content-Type', '').startswith('image/')
    except (urllib.error.URLError, TimeoutError):
        return False


def pinimg_url(hash, scale='originals'):
    """Find the URL of a Pinterest image hash, trying each extension."""
    base = f'https://i.pinimg.com/{scale}/{hash[0:2]}/{hash[2:4]}/{hash[4:6]}/{hash}'
    for ext in IMAGE_EXTS:
        if exists(f'{base}.{ext}'):
            return f'{base}.{ext}'
    return None


def canonical_image(url):
    """Prefer the original of a scaled Pinterest image."""
    m = PINIMG.search(url)
    if m and '/originals/' not in url:
        return pinimg_url(m.group(1)) or url
    return url


def canonical_source(url):
    m = PIN_URL.search(url)
    return f'https://www.pinterest.com/pin/{m.group(1)}/' if m else url


def scrape_image(page_url):
    """Find the image shown on a page. Returns (image URL, final page URL)."""
    with request(page_url) as r:
        final = r.geturl()
        html = r.read().decode('utf-8', errors='replace')
    if PIN_URL.search(final):
        # A pin page mentions other pins' images too; its own is the most frequent.
        hashes = collections.Counter(re.findall(
            r'https://i\.pinimg\.com/originals/(?:[0-9a-f]{2}/){3}([0-9a-f]{32}\.\w+)', html))
        if hashes:
            name = hashes.most_common(1)[0][0]
            return f'https://i.pinimg.com/originals/{name[0:2]}/{name[2:4]}/{name[4:6]}/{name}', final
    for pattern in (r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
                    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']'):
        m = re.search(pattern, html)
        if m:
            return canonical_image(urljoin(final, m.group(1).replace('&amp;', '&'))), final
    return None, final


def cache(url):
    """Download url into the image cache (if not already there); return the path."""
    path = cache_images.get_local_path(url)
    if path and (path.exists() or cache_images.download_image(url, path)):
        return path
    return None


def thumb_url(url, scale='400x'):
    """The scaled Pinterest URL the gallery displays (see _includes/thumb-src)."""
    m = PINIMG.search(url)
    if not m:
        return None
    return f'https://i.pinimg.com/{scale}/{m.group(1)[0:2]}/{m.group(1)[2:4]}/{m.group(1)[4:6]}/{m.group(1)}.jpg'


# -- Gallery --

class Entry:
    def __init__(self, source, image, tags):
        self.source, self.image, self.tags = source, image, tags

    @classmethod
    def parse(cls, item):
        parts = item.split('|')
        return cls(parts[0], parts[1] if len(parts) > 1 else '',
                   parts[2].split() if len(parts) > 2 else [])

    def keys(self):
        """Identifiers by which the image may be referenced elsewhere."""
        keys = set()
        m = PINIMG.search(self.image)
        keys.add(m.group(1) if m else self.image)
        m = PIN_URL.search(self.source)
        if m:
            keys.add(m.group(1))
        return keys

    def add_tags(self, tags):
        added = [t for t in tags if t not in self.tags]
        self.tags += added
        return added

    def __str__(self):
        line = f'{self.source}|{self.image}|{" ".join(self.tags)}'.rstrip('|')
        if line.startswith(('|', '"', "'")) or ': ' in line or ' #' in line:
            line = '"' + line.replace('\\', '\\\\').replace('"', '\\"') + '"'
        return f'  - {line}'


class Gallery:
    """The images list of gallery.md, rewritten in place (keeping the rest as is)."""

    def __init__(self, path=GALLERY):
        self.path = path
        self.lines = path.read_text(encoding='utf-8').split('\n')
        end = self.lines.index('---', 1)
        start = self.lines.index('images:', 0, end) + 1
        stop = start
        while stop < end and (self.lines[stop].startswith('  - ') or not self.lines[stop].strip()):
            stop += 1
        self.start, self.stop = start, stop
        items = yaml.safe_load('\n'.join(self.lines[start:stop])) or []
        self.entries = [Entry.parse(item) for item in items]

    def find(self, entry):
        keys = entry.keys()
        return next((e for e in self.entries if e.keys() & keys), None)

    def tag_counts(self):
        return collections.Counter(t for e in self.entries for t in e.tags)

    def save(self):
        block = [str(e) for e in self.entries]
        self.lines[self.start:self.stop] = block + ['']
        self.stop = self.start + len(block) + 1
        self.path.write_text('\n'.join(self.lines), encoding='utf-8')


def usages(entry):
    """Pages (other than the gallery) that reference the entry's image or pin."""
    keys = entry.keys()
    found = []
    for page in sorted(PAGES.rglob('*.md')):
        if page == GALLERY:
            continue
        text = page.read_text(encoding='utf-8', errors='replace')
        if any(k in text for k in keys):
            found.append(page.relative_to(SITE_ROOT))
    return found


# -- Tagging --

def normalize_tags(words):
    tags = []
    for word in words:
        for t in re.split(r'[,\s]+', word.strip().lower()):
            t = re.sub(r'[^a-z0-9-]+', '-', t).strip('-')
            if t and t not in tags:
                tags.append(t)
    return tags


PROMPT = """\
You are tagging fantasy artwork for a Dungeons & Dragons game master's \
image gallery, used to find portraits and scenes for characters and places.

Suggest 6 to 12 tags describing what is visible in this image:
- the subject: creature type or D&D race (human, elf, tiefling, dragonborn, \
giant, undead, beholder...), or the kind of place or object
- apparent sex (male/female) and age (child/young/old) of a character
- role or class (wizard, warrior, pirate, priest, noble...)
- distinctive features: clothing, armor, weapons, accessories, markings, \
hair, skin color, wings, horns
- setting and mood (forest, ocean, city, dungeon, creepy, cute...)

Tags are lowercase singular nouns or adjectives; join multi-word tags with \
hyphens (stone-giant, red-hair). Do not tag artistic style or proper names.
{existing}{given}"""


def suggest_tags(image_path, model, vocabulary, given):
    existing = ''
    if vocabulary:
        existing = ('\nThe gallery already uses these tags; reuse them where they fit '
                    '(but do not use ones that are names of people or places):\n'
                    + ' '.join(vocabulary) + '\n')
    given = (f'\nThe image is already tagged: {" ".join(given)}\n' if given else '')
    body = {
        'model': model,
        'stream': False,
        'think': False,
        'format': {'type': 'object', 'required': ['tags'],
                   'properties': {'tags': {'type': 'array', 'items': {'type': 'string'}}}},
        'options': {'temperature': 0.2},
        'messages': [{
            'role': 'user',
            'content': PROMPT.format(existing=existing, given=given),
            'images': [base64.b64encode(image_path.read_bytes()).decode('ascii')],
        }],
    }
    req = urllib.request.Request(f'{OLLAMA}/api/chat', data=json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=900) as r:
        reply = json.load(r)
    return normalize_tags(json.loads(reply['message']['content']).get('tags', []))


def vocabulary(gallery):
    # Tags on at least two images, so one-off tags don't snowball.
    return sorted(t for t, n in gallery.tag_counts().items() if n >= 2)


# -- Commands --

def parse_args(words):
    """Sort the positional arguments into (image, source, tags)."""
    images, sources, tags = [], [], []
    for w in words:
        if PIN_HASH.match(w.lower()):
            url = pinimg_url(w.lower())
            if not url:
                sys.exit(f'No Pinterest image with hash {w}')
            images.append(url)
        elif PIN_ID.match(w):
            sources.append(f'https://www.pinterest.com/pin/{w}/')
        elif re.match(r'https?://', w):
            (images if is_image_url(w) else sources).append(w)
        else:
            tags.append(w)
    if len(sources) == 2 and not images:
        # Neither looks like an image: ask the servers.
        image = next((s for s in sources if serves_image(s)), None)
        if image:
            sources.remove(image)
            images.append(image)
    if len(images) > 1 or len(sources) > 1:
        sys.exit(f'Expected one image and at most one source; got images {images}, sources {sources}')
    if not images and not sources:
        sys.exit('No image given')
    image = canonical_image(images[0]) if images else None
    source = canonical_source(sources[0]) if sources else ''
    if not image:
        log(f'Finding the image on {source}')
        image, final = scrape_image(source)
        if not image:
            sys.exit(f'No image found on {source}')
        source = canonical_source(final)
    return image, source, normalize_tags(tags)


def ingest(args):
    image, source, tags = parse_args(args.words)
    entry = Entry(source, image, tags)
    log(f'Image:  {image}')
    log(f'Source: {source or "(none)"}')

    used = usages(entry)
    if used and not args.force:
        sys.exit('Already used on: ' + ', '.join(map(str, used)) + ' (use --force to add anyway)')

    path = cache(image)
    if not path:
        sys.exit(f'Could not download {image}')
    log(f'Cached: {path.relative_to(SITE_ROOT)}')
    if thumb_url(image):
        cache(thumb_url(image))  # what the gallery page shows

    gallery = Gallery()
    existing = gallery.find(entry)
    if existing:
        log(f'Already in the gallery, tagged: {" ".join(existing.tags) or "(none)"}')
        if not existing.source and source:
            existing.source = source
        entry = existing
        entry.add_tags(tags)

    if not args.no_ai:
        log(f'Asking {args.model} for tags...')
        suggested = suggest_tags(path, args.model, vocabulary(gallery), entry.tags)
        added = entry.add_tags(suggested)
        log(f'Suggested: {" ".join(f"+{t}" if t in added else t for t in suggested)}')

    if not existing:
        gallery.entries.append(entry)
    print(str(entry).strip()[2:])
    if args.dry_run:
        log('(dry run: gallery not changed)')
    else:
        gallery.save()


def retag(args):
    gallery = Gallery()
    want = normalize_tags(args.words)
    entries = [e for e in gallery.entries if all(t in e.tags for t in want)]
    vocab = vocabulary(gallery)
    log(f'Retagging {len(entries)} images with {args.model}')
    for i, entry in enumerate(entries, 1):
        path = cache(entry.image)
        if not path:
            log(f'[{i}/{len(entries)}] could not download {entry.image}')
            continue
        try:
            added = entry.add_tags(suggest_tags(path, args.model, vocab, entry.tags))
        except (urllib.error.URLError, ValueError, KeyError) as e:
            log(f'[{i}/{len(entries)}] {entry.image}: {e}')
            continue
        log(f'[{i}/{len(entries)}] {entry.image}\n    {" ".join(entry.tags)}  (+{len(added)})')
        if not args.dry_run:
            gallery.save()  # after each image, so an interrupted run keeps its work


def prune(args):
    gallery = Gallery()
    keep = []
    for entry in gallery.entries:
        used = usages(entry)
        if used:
            print(f'{entry.image}\n    used on: {", ".join(map(str, used))}')
        else:
            keep.append(entry)
    removed = len(gallery.entries) - len(keep)
    print(f'{removed} used image(s)' + (' (dry run: gallery not changed)' if args.dry_run else ' removed'))
    if removed and not args.dry_run:
        gallery.entries = keep
        gallery.save()


def main():
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options] IMAGE [SOURCE] [TAG...]',
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)
    parser.add_argument('-h', '--help', action='help')
    parser.add_argument('words', nargs='*')
    parser.add_argument('-n', '--dry-run', action='store_true')
    parser.add_argument('--no-ai', action='store_true')
    parser.add_argument('--model', default=os.environ.get('INGEST_IMAGE_MODEL', DEFAULT_MODEL))
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--retag', action='store_true')
    parser.add_argument('--prune', action='store_true')
    args = parser.parse_args()
    if args.prune:
        prune(args)
    elif args.retag:
        retag(args)
    elif args.words:
        ingest(args)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
