#!/bin/sh

# Reports bad internal Markdown-style links.

cd "$(dirname "$0")/.."
git grep -o '\[[^]]*\]([^)]*)' '*.md' | while read line
do
  # format of each line is page:match
  page=${line%%:*}
  match=${line#*:}
  # format of each match is [label](link)
  link=${match##*\(}
  link=${link%\)}
  link=${link%#*} # strip anchors
  case "$link" in
    http*)
      ;; # external link
    *)
      name="${page%/*}/$link"
      test -f "$name.md" -o -f "$name/index.md" || echo "[ERROR] $page: $link"
  esac
done
