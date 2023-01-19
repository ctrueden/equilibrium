#!/bin/sh
cd "${0%/*}/../_pages"
clear
echo "== Duplicate images =="
grep -ohIR 'http[^ ]*pinterest.com/pin/[0-9]*/' *.md creatures dossiers events locales orgs relics rules gm/* | sort | uniq -d | while read pin
do
echo
echo "[$pin]"
grep -IRF "$pin" .
done
