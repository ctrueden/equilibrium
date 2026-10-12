#!/bin/sh
cd "$(dirname "$0")/.."
rm -rf _site
# Rules tooltips (GM builds only; see _bin/fivetools.py).
test -d _pages/gm && _bin/fivetools.py -q
bundle exec jekyll serve --incremental $@
