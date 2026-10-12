#!/bin/sh
cd "$(dirname "$0")/.."
rm -rf _site
# Rules tooltips (GM builds only; see _bin/5e.py).
test -d _pages/gm && uv run _bin/5e.py -q
bundle exec jekyll serve --incremental $@
