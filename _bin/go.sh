#!/bin/sh
cd "$(dirname "$0")/.."
rm -rf _site
bundle exec jekyll serve --incremental $@
