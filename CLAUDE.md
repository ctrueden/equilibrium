# Equilibrium Campaign Wiki

This is the source repository for the **Equilibrium** tabletop RPG campaign
wiki, a D&D 5E campaign about SPI (Supernatural Phenomena Investigation)
agents solving supernatural mysteries. The site is built with Jekyll and
served publicly. All content is plain Markdown with YAML front matter,
which is the deliberate long-term archival format.

---

## Directory Structure

```
_pages/
  calendar/        # Aecan calendar reference
  creatures/       # Creature type lore pages
  dossiers/        # NPC and entity profiles
  events/          # Historical events and session episode pages
  gm/              # GM-ONLY content (not public-facing)
    creatures/
    dossiers/
    events/
    future/
    ideas/
    locales/
    orgs/
    relics/
    religion/
    rules/
  gear.md          # Equipment reference
  glossary.md
  index.md
  locales/         # Locations
  orgs/            # Organizations
  relics/          # Magic items
  religion.md
  rules/           # Game mechanics reference
_bin/              # Utility scripts
_layouts/
_includes/
```

**Naming conventions:**
- File names: lowercase, hyphenated (`durak-greyshore.md`, `storm-stables.md`)
- Episode pages: `case-{case_id}.md` for case summaries, `case-{case_id}e{ep}.md` for episodes
  - Example: `case-17.md` (Case 17 summary), `case-17e09.md` (Case 17, episode 9)
- To make URLs more concise, dossier slugs for PCs differ from display names
  (e.g. `oz.md` for the PC named "Ozborn/Oz")

---

## Front Matter Schemas

### Episode event page (`_pages/events/case-NNeNN.md`)
```yaml
---
layout: session
title: "[17e09] Blooms of Remembrance"
description: >-
  One-sentence teaser shown in indexes.
datestamp: 50-06-13/09      # Aecan in-world date (format: YY-MM-DD/episode)
when: AC50 Vis 13           # Human-readable Aecan date
session-number: 96          # Cumulative session number across all cases
session-date: 2026-01-17    # Real-world session date (ISO)
locations_featured:
  - name: Grohnea's Cottage
    wiki: ../locales/grohneas-cottage
npcs_featured:
  - name: Ulgrim
    role: >-
      Bear shaman who performed a protective ritual on Ozborn
    wiki: ../dossiers/ulgrim
items_featured:
  - name: Ward of Returning
    wiki: ../relics/ward-of-returning
  - name: Egret Orchid        # no wiki field = no link
spells_featured:
  - Eldritch Blast
  - Wish
---
```
Content uses the **session layout** with collapsible `<details>` sections (see below).
The `layout: session` key enables the three-column layout with a session nav sidebar
and a reference sidebar (Locations, NPCs, Items, Spells built from front matter lists).
All four sidebar lists are optional; omit any that aren't relevant.

### Case summary page (`_pages/events/case-NN.md`)
```yaml
---
title: "[Case 17] Misery and Mending"
description: >-
  Brief arc description.
datestamp: 50-06-09/00a
when: AC50 Vis 09 - AC50 Vis 13
---
```

### Dossier (`_pages/dossiers/name.md`)
```yaml
---
title: Grohnea
---
```
Content is free-form Markdown, often with sections like
Background, Personality, Notes, etc.

### Locale (`_pages/locales/name.md`)
```yaml
---
title: Storm Stables
---
```

### GM-only pages mirror the public structure under `_pages/gm/`, e.g.:
- `_pages/gm/events/case-17e09.md` — GM notes for an episode
- `_pages/gm/dossiers/grohnea.md` — GM-only NPC secrets

---

## Session Page Body Structure

Episode pages use collapsible `<details>` sections, with the recap section
containing the tab system. **The ingest script generates this automatically.**

```markdown
<details class="session-section" open>
<summary>Recap</summary>
<div class="section-body">

{% include tab id='long' label='Long' first=true %}

[Long narrative recap — just the prose, no Outline or Moments here]

{% include tab id='short' label='Short' %}

[Short recap]

{% include tab id='dnd' label='Classic D&D' %}

[Classic D&D style]

{% include tab id='limerick' label='Limerick' %}

[Limerick]

{% include tab id='snarky' label='Snarky' %}

[Snarky recap]

{% include endtabs %}

</div>
</details>

<details class="session-section">
<summary>Memorable Moments (4)</summary>
<div class="section-body" markdown="1">

> **Freki:** "I'm healing you!"
>
> *Yelled while backing away at high speed*

</div>
</details>

<details class="session-section">
<summary>Outline</summary>
<div class="section-body" markdown="1">

### Scene Title

Scene description.

- Key event bullet
- Another key event

</div>
</details>
```

All episode pages must have at minimum Long and Short tabs in the Recap section.
The other tabs are nice-to-have (GM Assistant generates them automatically).

---

## Wiki Link Format

Internal links use relative paths from the current page:
```markdown
[Grohnea](../dossiers/grohnea)
[Storm Stables](../locales/storm-stables)
[giants](../creatures/giants)
[Case 17](../events/case-17)
```
Note: no `.md` extension in links.

---

## ⚠️ Name Alias Warning (GM Assistant vs. Wiki)

**GM Assistant may sometimes use different spellings than the wiki.**
Always verify names before publishing. Known divergences are declared
in `_bin/ingest-session.py` in the `KNOWN_ALIASES` dictionary.

This list grows over time. When ingesting a session, always check NPC and
location names against existing `_pages/dossiers/` and `_pages/locales/` files.

---

## GM Assistant YAML Ingestion

The primary utility script is `_bin/ingest-session.py`. It converts a
GM Assistant YAML export into a draft Jekyll episode page.

**Usage:**
```bash
_bin/ingest-session.py path/to/session-DATE.yaml
```

**What it produces:**
- `_pages/events/case-{id}.draft.md` — draft episode page with:
  - `layout: session` and all sidebar front matter pre-populated
  - Collapsible Recap (with all tab variants), Memorable Moments, and Outline sections
- Console report of NPCs/locations that don't have existing wiki pages yet

**What it does NOT do (requires human follow-up):**
- Correct proper noun spelling differences (see alias table above)
- Add wiki links in body text (`[Name](../dossiers/slug)` format)
- Fill in `datestamp` and `when` (requires Aecan calendar lookup)
- Fill in `session-number` (check the previous episode's front matter + 1)
- Trim or polish the auto-generated sidebar lists
- Create dossier/locale stubs (do this manually,
  or ask Claude Code to scaffold them)
- Overwrite existing pages

**Post-ingest checklist:**
1. Rename `.draft.md` to `.md` when satisfied
2. Correct all proper nouns (especially check alias table)
3. Add wiki links throughout body text
4. Trim sidebar lists — remove minor walk-ons, keep featured NPCs/locations
5. Fill in `datestamp`, `when`, `session-number`
6. Write the `description` field (one teaser sentence)
7. Create any missing dossier/locale stubs flagged in the console output
8. Update the case summary page (`case-NN.md`) if the arc concluded

---

## Foundry Actor Ingestion (Character Sheets)

The script `_bin/ingest-actor.py` converts a Foundry VTT actor JSON export into a
Jekyll character sheet page using the `charsheet` layout.

**Usage:**
```bash
_bin/ingest-actor.py path/to/fvtt-Actor-name-XXXX.json
```

**What it produces:**
- `_pages/gm/charsheets/<slug>.draft.md` — draft character sheet with:
  - `layout: charsheet` and all stats pre-computed in YAML front matter
  - Ability scores, saving throws, skills, weapons, features, equipment
  - Feature descriptions as markdown body text (rendered as a two-column section)

**What it computes automatically:**
- Proficiency bonus (from class level)
- Ability modifiers
- Saving throw and skill bonuses (with proficiency detection)
- AC (from equipped armor, or Barbarian/Monk Unarmored Defense)
- Speed (race base + class bonuses like Fast Movement)
- Weapon attack/damage strings (per-weapon ability, proficiency, damage type)
- Uses/resources (resolves `@scale.*` and `@prof` formulas)
- Feature list grouped by source (Race, Class, etc.)

**Post-ingest checklist:**
1. Rename `.draft.md` to `.md` when satisfied
2. Verify AC (check console checklist — especially shields/magic items)
3. Verify speed (race traits, magic items may add more)
4. Check uses/resources for complex `@scale` formulas
5. Fill in `background` and `alignment` if not in Foundry
6. Review feature descriptions for Foundry-specific markup that wasn't cleaned up
7. Remove `spell_ability`/`spell_dc`/`spell_atk` fields if character is not truly a spellcaster

**Front matter schema:** `layout: charsheet` with all data nested under `cs:`.
**Layout file:** `_layouts/charsheet.html`
**Output directory:** `_pages/gm/charsheets/`

---

## Common Tasks Claude Code Can Help With

- **Run session ingest:**
  `_bin/ingest-session.py <yaml>` and review output
- **Run actor ingest:**
  `_bin/ingest-actor.py <json>` and review output
- **Scaffold a new dossier stub:**
  create `_pages/dossiers/<slug>.md` with front matter + sections
- **Scaffold a new locale stub:**
  create `_pages/locales/<slug>.md` with front matter + sections
- **Find an NPC slug:**
  `grep -rl "title: NAME" _pages/dossiers/`
- **Check what pages link to an NPC:**
  `grep -rl "dossiers/slug" _pages/`
- **Add wiki links to a draft:**
  read draft, find NPC/location names, resolve slugs, insert links
- **Update the alias table in this file**
  when new divergences are discovered

---

## Longevity Principles

- The wiki is the **canonical source of truth**. Foundry VTT, GM Assistant,
  and Claude.ai are all upstream drafting/display tools.
  Content always flows *into* the wiki, never out.
- Never store campaign-critical content only in Foundry journals.
- GM Assistant exports (YAML) are raw material; the processed wiki page is the archive.
- All GM-only content lives under `_pages/gm/` and is excluded from the public build.
