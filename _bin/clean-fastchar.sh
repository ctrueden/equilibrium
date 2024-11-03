# This script cleans up fastcharacter.com-generated character sheets
# saved as HTML documents, so that they can be embedded in other websites.

while [ $# -gt 0 ]
do
  arg=$1
  shift
  perl -0777 -i \
    -pe 's/\n<script.*\n<\/script>//igs;' \
    -pe 's/\n<div id="charsheet02">.*<\/body>/\n<\/div>\n<\/body>/igs' \
    "$arg"
done
