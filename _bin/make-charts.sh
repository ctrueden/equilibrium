#!/bin/sh
cd "$(dirname "$0")"
targetDir=../assets/images
mkdir -p "$targetDir"
for dot in *.dot
do
  dot "$dot" -Tsvg > "$targetDir/${dot%.dot}.svg"
done
