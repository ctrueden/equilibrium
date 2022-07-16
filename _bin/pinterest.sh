#!/bin/sh
while [ $# -gt 0 ]
do
  pin=$(grep -oh 'related-pins:[0-9]*' -- "$1" | sed 's/^related-pins://')
  img=$(grep -oh 'https://i.pinimg.com/originals/[^"]*' -- "$1" | head -n1)
  test "$pin" -a "$img" &&
    echo "https://www.pinterest.com/pin/$pin/|$img" ||
    echo "[FAIL] $1"
  shift
done
