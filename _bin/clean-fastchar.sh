# This script cleans up fastcharacter.com-generated character sheets
# saved as HTML documents, so that they can be embedded in other websites.

while [ $# -gt 0 ]
do
  arg=$1
  shift
  perl -0777 -i \
    -pe 's/\n<script[^\n]*<\/script>//igs;' \
    -pe 's/\n<script id="savepage-shadowloader".*\n<\/script>//igs;' \
    -pe 's/<a name="footer"><\/a>\n<div id="footer">.*<\/body>/\n<\/div>\n<\/body>/igs' \
    "$arg"
done
