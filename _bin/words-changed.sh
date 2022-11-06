# Credit: https://gist.github.com/MilesCranmer/5c7d86c8740219355d2dfdb184910711
total=0
daysAgo=$1
test "$daysAgo" || daysAgo=0
for sha in $(git rev-list --after="$((daysAgo+1)) days ago" --before="$daysAgo days ago" main | sed -e '$ d'); do
    added=$(git diff --word-diff=porcelain $sha~1..$sha|grep -e"^+[^+]"|wc -w|xargs)
    deleted=$(git diff --word-diff=porcelain $sha~1..$sha|grep -e"^-[^-]"|wc -w|xargs)
    duplicated=$(git diff $sha~1..$sha|grep -e"^+[^+]" -e"^-[^-]"|sed -e's/.//'|sort|uniq -d|wc -w|xargs)
    if [ "$added" -eq "0" ]; then
        changed=$deleted
        total=$((total+deleted))
        echo "added:" $added, "deleted:" $deleted, "duplicated:"\
             $duplicated, "changed:" $changed
    elif [ "$(echo "$duplicated/$added > 0.8" | bc -l)" -eq "1" ]; then
        echo "added:" $added, "deleted:" $deleted, "duplicated:"\
             $duplicated, "changes counted:" 0
    else
        changed=$((added+deleted))
        total=$((total+changed))
        echo "added:" $added, "deleted:" $deleted, "duplicated:"\
             $duplicated, "changes counted:" $changed
    fi
done
echo "Total changed: $total"
