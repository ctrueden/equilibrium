#!/usr/bin/env -S python3 -P
"""
Download and cache all external images referenced by the built site into /assets/cache

Scans the generated HTML (rather than the markdown sources), so that every
image URL produced by includes and layouts (e.g. scaled Pinterest thumbnails
from the img include) is covered exactly as rendered.

Usage:
  ./_bin/cache-images.py                # Download all images
  ./_bin/cache-images.py --check        # Check which images are missing
  ./_bin/cache-images.py --site DIR     # Scan DIR instead of _site
"""

import sys
import urllib.request
import urllib.error
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

# Site root is the parent of _bin
SITE_ROOT = Path(__file__).parent.parent
CACHE_DIR = SITE_ROOT / 'assets' / 'cache'

class ImageSrcParser(HTMLParser):
    """Collect the src attribute of every img tag."""

    def __init__(self):
        super().__init__()
        self.srcs = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            src = dict(attrs).get('src')
            if src:
                self.srcs.append(src.strip())

def extract_image_urls(html_file):
    """Extract external image URLs from an HTML file."""
    try:
        parser = ImageSrcParser()
        parser.feed(html_file.read_text(encoding='utf-8'))
        return [s for s in parser.srcs if s.startswith(('http://', 'https://'))]
    except Exception as e:
        print(f"Error parsing {html_file}: {e}", file=sys.stderr)
        return []

def download_image(url, output_path):
    """Download an image from URL to output_path."""
    # Create directory structure
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Check if file already exists
        if output_path.exists():
            return True

        # Download with a user agent (some sites block requests without one)
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())

        print(f"  ✓ Downloaded: {output_path.relative_to(SITE_ROOT)}")
        return True

    except urllib.error.HTTPError as e:
        print(f"  ✗ HTTP {e.code}: {url}", file=sys.stderr)
        return False
    except urllib.error.URLError as e:
        print(f"  ✗ URL error: {url} - {e.reason}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  ✗ Error: {url} - {e}", file=sys.stderr)
        return False

def get_local_path(url):
    """Convert a URL to a local cache path."""
    try:
        parsed = urlparse(url)
        # Strip leading underscores from each path component: Jekyll excludes any
        # file/directory whose name starts with '_' at any depth of the source tree.
        parts = parsed.path.lstrip('/').split('/')
        sanitized = '/'.join(p.lstrip('_') for p in parts)
        # Create path like /assets/cache/domain.com/path/to/image.jpg
        local_path = CACHE_DIR / parsed.netloc / sanitized
        return local_path
    except Exception:
        return None

def main():
    check_mode = '--check' in sys.argv
    site_dir = SITE_ROOT / '_site'
    if '--site' in sys.argv:
        site_dir = Path(sys.argv[sys.argv.index('--site') + 1])

    print(f"Site root: {SITE_ROOT}")
    print(f"Built site: {site_dir}")
    print(f"Cache dir: {CACHE_DIR}")
    print(f"Mode: {'Check' if check_mode else 'Download'}\n")

    if not site_dir.exists():
        print(f"Error: {site_dir} not found; build the site first", file=sys.stderr)
        sys.exit(1)

    # Find all generated HTML files, skipping the cache itself
    html_files = [f for f in site_dir.rglob('*.html') if 'assets' not in f.relative_to(site_dir).parts]
    print(f"Found {len(html_files)} HTML files\n")

    urls_to_cache = set()  # Use set to avoid duplicates
    for html_file in sorted(html_files):
        urls_to_cache.update(extract_image_urls(html_file))

    print(f"Found {len(urls_to_cache)} unique image URLs\n")

    missing_count = 0
    failed_count = 0
    for url in sorted(urls_to_cache):
        local_path = get_local_path(url)

        if not local_path:
            print(f"✗ Could not parse URL: {url}", file=sys.stderr)
            continue

        if check_mode:
            if not local_path.exists():
                print(f"✗ Missing: {local_path.relative_to(SITE_ROOT)} <- {url}")
                missing_count += 1
        elif not download_image(url, local_path):
            failed_count += 1

    if check_mode:
        print(f"\n{missing_count} images missing from cache")
        if missing_count > 0:
            sys.exit(1)
    else:
        print(f"\nCache update complete; {failed_count} downloads failed. Run with --check to verify.")
        if failed_count > 0:
            sys.exit(1)

if __name__ == '__main__':
    main()
