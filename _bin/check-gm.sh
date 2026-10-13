#!/bin/sh

# Reports mismatches between player-facing and GM-facing page names.
# GM pages with `gm-only: true` in their front matter are not reported
# as lacking public content. (A public page that shadows one is fine.)

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
  test -f "$pp" && continue
  # Note: pages marked `gm-only: true` are intentionally without public content.
  awk 'NR==1 && /^---$/ {fm=1; next} fm && /^---$/ {exit} fm && /^gm-only:[ ]*true[ ]*$/ {found=1} END {exit !found}' "$gp" ||
    echo "$p: No public content"
done
