#!/bin/sh
cd "$(dirname "$0")/.."
rm -rf _site
_bin/make-charts.sh
bundle exec jekyll serve --incremental
