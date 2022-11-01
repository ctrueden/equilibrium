#!/bin/zsh

# Reports word counts!

t=0

words() {
  w=$(cat "$1" | sed -e 's/<[^>]*>//g' | grep -o "\b[A-Za-z'-]\+\b" | wc -w)
  t=$((t+w))
  echo "$w" "$1"
}

if [ $# -gt 0 ]
then
  for f in $@
  do
    words "$f"
  done
else
  cd "$(dirname "$0")/.."
  for f in _pages/**/*.md
  do
    words "$f"
  done
fi
echo "$t total"
