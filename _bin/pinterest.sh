#!/bin/sh
while [ $# -gt 0 ]
do
  pin=$(grep -oh 'data-savepage-href="ios-app://[0-9]*/pinterest/pin/[0-9]*' "$1" | sed 's_.*/\([0-9]*\)$_\1_')
  img=$(grep -oh 'https://i.pinimg.com/\(originals\|736x\)/[^"]*' -- "$1" | head -n1)
  test "$pin" -a "$img" &&
    echo "https://www.pinterest.com/pin/$pin/|$img" ||
    echo "[FAIL] $1"
  shift
done
