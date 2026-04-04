#!/usr/bin/env python3
"""
ingest-session.py — Import a GM Assistant YAML export into the Equilibrium Jekyll wiki.

Usage:
    python _scripts/ingest_session.py <yaml_file>

Produces:
    _pages/events/case-{id}.draft.md   — Draft episode page (never overwrites existing)
    Console report of missing wiki pages for NPCs/locations/items

Requires: PyYAML  (pip install pyyaml)
"""

import sys
import re
import textwrap
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Known name aliases: GM Assistant spelling → canonical wiki slug
# Update this dict as new divergences are found.
# ---------------------------------------------------------------------------
KNOWN_ALIASES = {
    "gronia":       "grohnea",
    "sisai":        "sissae-moondrop",
    "sissae":       "sissae-moondrop",
    "orlock":       "orlok",
    "rhizopus":     "rhyzophus",
    "zaryudia":     "xaryuvia",
    "sunclaw":      "zanqaa",
    "ice palace":   "storm-stables",
    "ozborn":       "oz",
}


def slugify(name: str) -> str:
    """Convert a display name to a likely wiki slug."""
    s = name.lower().strip()
    s = re.sub(r"[''`]", "", s)          # remove apostrophes
    s = re.sub(r"[^a-z0-9]+", "-", s)   # non-alphanumeric → hyphen
    s = s.strip("-")
    return s


def resolve_slug(name: str) -> str:
    """Return the best-guess wiki slug, checking alias table first."""
    lower = name.lower().strip()
    if lower in KNOWN_ALIASES:
        return KNOWN_ALIASES[lower]
    return slugify(name)


def find_jekyll_root(start: Path) -> Path:
    """Walk up from start looking for _pages/ directory."""
    for p in [start] + list(start.parents):
        if (p / "_pages").is_dir():
            return p
    return start


def existing_slugs(pages_dir: Path, subdir: str) -> set:
    d = pages_dir / subdir
    if not d.exists():
        return set()
    return {f.stem for f in d.glob("*.md")}


def detect_case_id(title: str) -> str | None:
    """Extract case ID from a title like 'Case 17e09' → '17e09'."""
    m = re.search(r"[Cc]ase\s+(\w+)", title)
    return m.group(1).lower() if m else None


# ---------------------------------------------------------------------------
# Draft page builder
# ---------------------------------------------------------------------------

def build_featured_list(entries: list, known_slugs: set, subdir: str,
                         include_role: bool = False) -> list[str]:
    """Build a YAML front matter list for featured NPCs/locations/items."""
    yaml_lines = []
    for entry in entries:
        name = entry.get("name", "").strip()
        if not name:
            continue
        slug = resolve_slug(name)
        has_page = slug in known_slugs or slugify(name) in known_slugs
        yaml_lines.append(f"  - name: {name}")
        if has_page:
            yaml_lines.append(f"    wiki: ../{subdir}/{slug}")
        if include_role:
            desc = entry.get("description", "").strip()
            if desc:
                yaml_lines.append(f"    role: >-")
                # Indent each line of the description for YAML block scalar
                for desc_line in desc.splitlines():
                    yaml_lines.append(f"      {desc_line}")
    return yaml_lines


def format_moments(moments: list) -> list[str]:
    """Render memorable moments as markdown lines."""
    lines = []
    for m in moments:
        desc     = str(m.get("description", "")).strip()
        speaker  = m.get("speaker", "").strip()
        ctx      = str(m.get("context", "")).strip()
        mtype    = m.get("type", "").strip()
        is_quote = m.get("is_quote", False)

        if speaker and is_quote:
            lines.append(f'> **{speaker}:** "{desc}"')
        elif speaker:
            lines.append(f"**{speaker}:** {desc}")
        else:
            lines.append(f"- *[{mtype}]* {desc}")

        if ctx:
            lines.append(f">")
            lines.append(f"> *{ctx}*")
        lines.append("")
    return lines


def build_draft(data: dict, case_id: str, pages_dir: Path) -> str:
    played_at = data.get("playedAt", "YYYY-MM-DD")

    dossiers = existing_slugs(pages_dir, "dossiers")
    locales  = existing_slugs(pages_dir, "locales")
    relics   = existing_slugs(pages_dir, "relics")

    npcs      = data.get("npcs", [])
    locations = data.get("locations", [])
    items     = data.get("items", [])
    spells    = data.get("spells", [])
    moments   = data.get("memorable_moments", data.get("memorableMoments", []))
    scenes    = data.get("scenes", [])

    lines = []

    # --- Front matter ---
    lines += [
        "---",
        "layout: session",
        f'title: "[{case_id.upper()}] TITLE HERE  # TODO: give this episode a name"',
        "description: >-",
        "  TODO: one-sentence teaser",
        "datestamp: TODO  # Aecan date, e.g. 50-06-13/09",
        "when: TODO       # e.g. AC50 Vis 13",
        "session-number: TODO  # previous episode's session-number + 1",
        f"session-date: {played_at}",
    ]

    # Featured locations
    loc_lines = build_featured_list(locations, locales, "locales", include_role=False)
    if loc_lines:
        lines.append("locations_featured:")
        lines += loc_lines

    # Featured NPCs
    npc_lines = build_featured_list(npcs, dossiers, "dossiers", include_role=True)
    if npc_lines:
        lines.append("npcs_featured:")
        lines += npc_lines

    # Featured items
    item_lines = build_featured_list(items, relics, "relics", include_role=False)
    if item_lines:
        lines.append("items_featured:")
        lines += item_lines

    # Featured spells (simple name list)
    if spells:
        lines.append("spells_featured:")
        for s in spells:
            spell_name = s.get("name", s) if isinstance(s, dict) else str(s)
            lines.append(f"  - {spell_name.strip()}")

    lines += [
        "---",
        "",
        "<!--",
        "  DRAFT — generated by _bin/ingest-session.py",
        "  TODO Before publishing:",
        "    1. Rename to case-{id}.md (remove .draft)",
        "    2. Fix proper nouns (GM Assistant spellings differ — see _bin/ingest-session.py KNOWN_ALIASES dict)",
        "    3. Add wiki links to body text: [Name](../dossiers/slug), [Place](../locales/slug)",
        "    4. Fill in datestamp, when, session-number, title, description",
        "    5. Verify/trim the sidebar lists (npcs_featured, locations_featured, etc.)",
        "    6. Delete this comment block",
        "-->",
        "",
    ]

    # --- Recap section (collapsible) ---
    long_summary = data.get("summary", "").strip()
    short        = data.get("short_summary", data.get("short", "")).strip()
    classic      = data.get("classic_summary", "").strip()
    limerick     = data.get("limerick_style_summary", data.get("limerick_summary", "")).strip()
    snarky       = data.get("snarky_summary", "").strip()

    lines += [
        '<details class="session-section" open>',
        "<summary>Recap</summary>",
        '<div class="section-body">',
        "",
        "{% include tab id='long' label='Long' first=true %}",
        "",
        long_summary,
        "",
        "{% include tab id='short' label='Short' %}",
        "",
        short if short else "TODO: write short summary",
        "",
        "{% include tab id='dnd' label='Classic D&D' %}",
        "",
        classic if classic else "TODO",
        "",
        "{% include tab id='limerick' label='Limerick' %}",
        "",
        limerick if limerick else "TODO",
        "",
        "{% include tab id='snarky' label='Snarky' %}",
        "",
        snarky if snarky else "TODO",
        "",
        "{% include endtabs %}",
        "",
        "</div>",
        "</details>",
        "",
    ]

    # --- Memorable Moments section ---
    if moments:
        count = len(moments)
        lines += [
            '<details class="session-section">',
            f"<summary>Memorable Moments ({count})</summary>",
            '<div class="section-body" markdown="1">',
            "",
        ]
        lines += format_moments(moments)
        lines += [
            "</div>",
            "</details>",
            "",
        ]

    # --- Outline section ---
    if scenes:
        lines += [
            '<details class="session-section">',
            "<summary>Outline</summary>",
            '<div class="section-body" markdown="1">',
            "",
        ]
        for scene in scenes:
            scene_title = scene.get("title", "Scene").strip()
            scene_desc  = scene.get("description", "").strip()
            key_events  = scene.get("key_events", scene.get("keyEvents", []))
            lines += [f"### {scene_title}", ""]
            if scene_desc:
                lines += [scene_desc, ""]
            for ev in key_events:
                ev = ev.strip().replace("\n", " ")
                lines.append(f"- {ev}")
            lines.append("")
        lines += [
            "</div>",
            "</details>",
            "",
        ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Missing-page reporter
# ---------------------------------------------------------------------------

def report_missing(data: dict, pages_dir: Path) -> None:
    dossiers = existing_slugs(pages_dir, "dossiers")
    locales  = existing_slugs(pages_dir, "locales")
    relics   = existing_slugs(pages_dir, "relics")

    sections = [
        ("NPCs",      data.get("npcs", []),       dossiers, "dossiers"),
        ("Locations", data.get("locations", []),   locales,  "locales"),
        ("Items",     data.get("items", []),        relics,   "relics"),
    ]

    for label, entries, known_slugs, subdir in sections:
        missing = []
        for entry in entries:
            name = entry.get("name", "").strip()
            if not name:
                continue
            slug = resolve_slug(name)
            if slug not in known_slugs:
                # Also check slugify without alias resolution
                raw_slug = slugify(name)
                if raw_slug in known_slugs:
                    continue
                desc = entry.get("description", "")
                short_desc = textwrap.shorten(desc, width=90, placeholder="...")
                missing.append((name, slug, short_desc))

        if missing:
            print(f"\n⚠️  {label} with no existing wiki page ({len(missing)}):")
            for name, slug, desc in missing:
                alias_note = ""
                if resolve_slug(name) != slugify(name):
                    alias_note = f"  [alias → {resolve_slug(name)}]"
                print(f"  • {name}{alias_note}")
                print(f"    Suggested slug: _pages/{subdir}/{slug}.md")
                if desc:
                    print(f"    GM Asst desc: {desc}")

    # Spells — just list them (no dedicated pages usually)
    spells = data.get("spells", [])
    if spells:
        print(f"\nℹ️  Spells referenced this session:")
        for s in spells:
            print(f"  • {s.get('name', '?')}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python _scripts/ingest_session.py <yaml_file>")
        sys.exit(1)

    yaml_path = Path(sys.argv[1])
    if not yaml_path.exists():
        print(f"Error: file not found: {yaml_path}")
        sys.exit(1)

    with yaml_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    title    = data.get("title", "")
    case_id  = detect_case_id(title)

    if not case_id:
        print(f"⚠️  Could not detect case ID from title: '{title}'")
        case_id = input("Enter case ID (e.g. '17e09'): ").strip()

    root      = find_jekyll_root(Path.cwd())
    pages_dir = root / "_pages"
    events_dir = pages_dir / "events"
    events_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*55}")
    print(f"  GM Assistant Ingest: case-{case_id}")
    print(f"  Jekyll root: {root}")
    print(f"{'='*55}")

    final_page = events_dir / f"case-{case_id}.md"
    draft_page = events_dir / f"case-{case_id}.draft.md"

    if final_page.exists():
        print(f"\n✓ Final page already exists: {final_page.relative_to(root)}")
        print("  (Not overwriting. Draft will be created alongside for comparison.)")

    if draft_page.exists():
        answer = input(f"\nDraft already exists: {draft_page.name}. Overwrite? [y/N] ").strip().lower()
        if answer != "y":
            print("Skipping draft creation.")
            report_missing(data, pages_dir)
            return

    draft_content = build_draft(data, case_id, pages_dir)
    draft_page.write_text(draft_content, encoding="utf-8")
    print(f"\n✓ Draft written: {draft_page.relative_to(root)}")

    report_missing(data, pages_dir)

    print(f"\n{'='*55}")
    print("  Next steps:")
    print(f"  1. Edit {draft_page.relative_to(root)}")
    print("  2. Fix proper nouns (see KNOWN_ALIASES dict above)")
    print("  3. Add wiki links in body: [Name](../dossiers/slug)")
    print("  4. Verify sidebar lists (npcs_featured, locations_featured, …)")
    print("  5. Fill in datestamp / when / session-number / title / description")
    print(f"  6. Rename to case-{case_id}.md when satisfied")
    print("  ⚠️  GM Assistant spellings often differ from wiki — always verify!")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
