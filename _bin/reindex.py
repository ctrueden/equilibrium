import json
import os
import re
from frontmatter import Frontmatter  # pip install --user frontmatter
from pathlib import Path

basedir = Path(__file__).parent.parent / "_pages"
baselen = len(str(basedir)) + 1

print("Reading .md files...")

index = []
for md_path in basedir.rglob("*.md"):
    short_path = str(md_path)[baselen:-3]
    if short_path.startswith("gm"): continue  # no spoilers! :-P
    doc = Frontmatter.read_file(md_path)
    attrs = doc["attributes"]
    entry = {}
    if attrs: entry.update(attrs)
    # Strip unwanted markup from document body.
    pattern = (
        "|<style.*?</style>"  # <style> block
        "|<script.*?</script>"  # <script> block
        "{{[^}]*}}"  # liquid variable
        "|{%[^}]*%}"  # liquid directive
        "|<[a-zA-Z/!].*?>"  # HTML tag
    )
    entry["body"] = re.sub(pattern, "", doc["body"], flags=re.DOTALL)
    entry["id"] = short_path
    index.append(entry)

def encode(o):
    return o if type(o) in (str, int, float, bool) else str(o)

print("Writing docs.json file...")
with open(basedir.parent / "assets" / "docs.json", "w") as f:
    json.dump(index, f, default=encode)
