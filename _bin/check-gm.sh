#!/bin/sh

# Reports mismatches between player-facing and GM-facing page names.

cd "$(dirname "$0")/.."

find _pages -name '*.md' | while read pp
do
  p=${pp#_pages/}
  gp="_pages/gm/$p"
  test -f "$gp" || echo "$p: No GM content"
done

echo "------------------------------------------"

find _pages/gm -name '*.md' | while read gp
do
  p=${gp#_pages/gm/}
  pp="_pages/$p"
  test -f "$pp" || echo "$p: No public content"
done
