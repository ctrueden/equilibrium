#!/usr/bin/env python3
"""
Download and cache all external images from front matter into /assets/cache

Usage:
  ./_bin/cache-images.py          # Download all images
  ./_bin/cache-images.py --check  # Check which images are missing
"""

import os
import sys
import re
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import urlparse

# Site root is the parent of _bin
SITE_ROOT = Path(__file__).parent.parent
PAGES_DIR = SITE_ROOT / '_pages'
CACHE_DIR = SITE_ROOT / 'assets' / 'cache'

def extract_front_matter(file_path):
    """Extract front matter from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match front matter between --- delimiters
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {}

        front_matter = {}
        for line in match.group(1).split('\n'):
            # Match yaml key: value pairs (handle quoted strings)
            fm_match = re.match(r'^(\w+):\s+(.+)$', line)
            if fm_match:
                key, value = fm_match.groups()
                # Remove quotes and strip whitespace
                value = value.strip('"\'').strip()
                front_matter[key] = value

        return front_matter
    except Exception as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        return {}

def download_image(url, output_path):
    """Download an image from URL to output_path."""
    # Create directory structure
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Check if file already exists
        if output_path.exists():
            print(f"  ✓ Already cached: {output_path.relative_to(SITE_ROOT)}")
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

def get_pinterest_400x_url(url):
    """
    Convert a Pinterest originals URL to a 400x thumbnail.

    https://i.pinimg.com/originals/xx/yy/zz.ext -> https://i.pinimg.com/400x/xx/yy/zz.jpg
    Returns None if not a Pinterest URL.
    """
    if 'i.pinimg.com/originals/' not in url:
        return None

    # Replace /originals/ with /400x/ and convert extension to .jpg
    url_400x = url.replace('/originals/', '/400x/')
    # Convert all image extensions to jpg
    url_400x = re.sub(r'\.(png|webp|gif)($|\?)', r'.jpg\2', url_400x, flags=re.IGNORECASE)

    return url_400x

def main():
    check_mode = '--check' in sys.argv

    print(f"Site root: {SITE_ROOT}")
    print(f"Cache dir: {CACHE_DIR}")
    print(f"Mode: {'Check' if check_mode else 'Download'}\n")

    if not PAGES_DIR.exists():
        print(f"Error: {PAGES_DIR} not found", file=sys.stderr)
        sys.exit(1)

    # Find all markdown files
    md_files = list(PAGES_DIR.rglob('*.md'))
    print(f"Found {len(md_files)} markdown files\n")

    urls_to_cache = set()  # Use set to avoid duplicates
    missing_count = 0

    # Collect all image URLs from front matter
    for md_file in sorted(md_files):
        front_matter = extract_front_matter(md_file)

        if 'image' in front_matter:
            url = front_matter['image']
            if url.startswith('http://') or url.startswith('https://'):
                urls_to_cache.add(url)

    print(f"Found {len(urls_to_cache)} unique image URLs\n")

    # Process each URL
    for url in sorted(urls_to_cache):
        local_path = get_local_path(url)

        if not local_path:
            print(f"✗ Could not parse URL: {url}", file=sys.stderr)
            continue

        if check_mode:
            if not local_path.exists():
                print(f"✗ Missing: {local_path.relative_to(SITE_ROOT)} <- {url}")
                missing_count += 1
            else:
                print(f"✓ Cached:  {local_path.relative_to(SITE_ROOT)}")
        else:
            download_image(url, local_path)

        # For Pinterest images, also cache the 400x thumbnail version
        url_400x = get_pinterest_400x_url(url)
        if url_400x:
            local_path_400x = get_local_path(url_400x)

            if check_mode:
                if not local_path_400x.exists():
                    print(f"✗ Missing: {local_path_400x.relative_to(SITE_ROOT)} <- {url_400x}")
                    missing_count += 1
                else:
                    print(f"✓ Cached:  {local_path_400x.relative_to(SITE_ROOT)}")
            else:
                download_image(url_400x, local_path_400x)

    if check_mode:
        print(f"\n{missing_count} images missing from cache")
        if missing_count > 0:
            sys.exit(1)
    else:
        print(f"\nCache update complete. Run with --check to verify.")

if __name__ == '__main__':
    main()
