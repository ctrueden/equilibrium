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

Episode pages are GM Assistant YAML exports used directly as front matter
(see "GM Assistant YAML Ingestion" below), plus a few wiki fields:
```yaml
---
title: "[17e09] Soul Toll"
description: >-
  One-sentence teaser shown in indexes.
datestamp: 50-06-13/09      # Aecan in-world date (format: YY-MM-DD/episode)
when: AC50 Vis 13           # Human-readable Aecan date
session-number: 96          # Cumulative session number across all cases
session-date: 2026-01-17    # Real-world session date (ISO)
layout: session
reviewed: false             # shows a "not yet reviewed" banner until vetted
summary: >-                 # Long recap tab (Markdown; links allowed)
  ...
short_summary: >-           # Short tab; also classic_summary, snarky_summary,
  ...                       # limerick_style_summary, notes, callie_journal
memorable_moments:          # [{type, description, context, is_quote, speaker}]
scenes:                     # [{title, description, key_events: [...]}]
npcs:                       # right sidebar lists: {name, description, wiki}
  - name: Ulgrim
    description: >-
      Bear shaman who performed a protective ritual on Ozborn.
    wiki: ../dossiers/ulgrim  # no wiki field = no link
locations: [...]
items: [...]
spells: [...]
---
```
Older episodes instead have hand-written Markdown bodies (with the
`{% include tab %}` recap tabs described below); both forms render with
the **session layout**: case/episode navigation on the left, prev/next
episode links, collapsible content sections, and the reference sidebar.

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
containing the tab system. (This applies to older, hand-written episodes; for GM Assistant episodes,
the layout builds the same sections from the front matter.)

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

## Images

Embed images with the `img` include rather than markdown image syntax, so
the generated HTML can be adjusted site-wide in one place:
```liquid
{% include img page="dossiers/serelda-voth" width=200 %}
{% include img page="dossiers/freki" variant="beast" height=250 %}
{% include img pinimg="505ee23c6213467229a3e6a5b3f45e82.jpg" pin=593841900839915800 alt="Preen" width=200 %}
```
- `page` pulls `image`/`image-source`/`title` from that page's front matter
  (`variant="x"` uses `image-x`/`image-x-source`); clicking goes to the page,
  or to the image source when the page is the current page.
- When an image depicts something with its own page, add it to that page's
  front matter as a variant and reference it with `page`/`variant`, rather
  than inlining the URL. Front matter image URLs are always full URLs
  (local images as `/equilibrium/assets/images/...`). Public pages must not
  reference `gm/` pages, which do not exist in the public build.
- `pinimg` is a Pinterest image file name: the include derives the full
  `i.pinimg.com` URL from it. Use `src` for any other image URL.
- `pin=ID` is shorthand for `source=https://www.pinterest.com/pin/ID/`.
- `width`/`height` are max pixel sizes, and select a suitably downscaled
  Pinterest variant. Also: `link` (`page`/`source`/`none`/URL), `caption`
  (text, or `true` for the page title), `align` (`left`/`right`/`center`),
  `alt`, `class`, `style`. See `_includes/img` for details.

External images are cached for local development by `_bin/cache-images.py`,
which scans the built `_site` for `<img>` URLs (so build the site first).

### GM image gallery

`_pages/gm/gallery.md` holds prospective images, as `images:` entries of
the form `source|image|tag tag tag` (lowercase singular tags, multi-word
ones hyphenated: `stone-giant`); the page filters them by tag. Once an
image is used on a page, it is removed from the gallery.

```bash
_bin/ingest-image.py 00fe9dcf57bf11a5177df5dc24186615 stone-giant male  # Pinterest image hash
_bin/ingest-image.py 1028087421185063112 giant      # pin ID: image scraped from the pin
_bin/ingest-image.py PAGE_URL IMAGE_URL elf         # any source page + image
_bin/ingest-image.py --retag giant                  # model-tag existing images tagged giant
_bin/ingest-image.py --prune                        # drop images already used on pages
```
It caches the image (as `cache-images.py` does), asks a local Ollama vision
model for tags (`--no-ai` to skip, `--model` to choose), merges them with
the given tags, and adds or updates the gallery entry. `-n` is a dry run.

---

## GM Assistant YAML Ingestion

GM Assistant exports session notes as YAML closely matching the episode
schema above, so ingestion is: save the export as
`_pages/events/case-NNeNN.md` between `---` lines, then add `title`,
`description`, `datestamp`, `when`, `session-number`, `session-date`,
`layout: session` and `reviewed: false`.

**GM Assistant often misspells names** (transcription from audio). Known
misspellings are recorded as `aliases:` in the front matter of the page
they refer to (e.g. `aliases: [Kerwin Ovas]` on `dossiers/kerwin-ulvas.md`),
so that tools recognize them.

### Reviewing a session: `_bin/review-session.py`

```bash
_bin/review-session.py                    # dry run over all `reviewed: false` pages
_bin/review-session.py case-18e06.md      # one page
_bin/review-session.py --fix "Zarlis=Xarlus" --fix "Gallic=Galloc" --apply case-18e06.md
```
It (1) links the first mention of each known entity in each recap field
(each is its own tab), in the scenes and in the Markdown body; (2) fills in
missing `wiki:` links in the npcs/locations/items sidebars; and (3) flags
capitalized names with no wiki page, suggesting close matches as probable
misspellings. Fix misspellings with `--fix OLD=NEW` (or by hand), and add
recurring ones to the target page's `aliases:`. Names come from
`_bin/entities.py`: page titles, `nav-title`, `aliases`, and distinctive
first/last names (ordinary words like "Holly" are never linked alone).
Nothing is written without `--apply`.

**Review checklist:**
1. Run the review script; fix misspellings; rerun with `--apply`
2. Read the recap against GM notes; fix factual errors
3. Trim sidebar lists — remove minor walk-ons; fix their `description`s
4. Fill in `datestamp`, `when`, `session-number`, `description`, `title`
5. Create any missing dossier/locale stubs for names worth a page
6. Update the case summary page (`case-NN.md`) if the arc concluded
7. Remove `reviewed: false`

---

## Character Sheets

Character sheets live in `_pages/gm/charsheets/<slug>.md` (GM-only) and use
the `charsheet` layout (`_layouts/charsheet.html`), with all data nested
under `cs:` in the front matter. `_pages/gm/charsheets/index.md` lists them.
Link to a sheet from a GM dossier as
`[character sheet]({{site.baseurl}}/gm/charsheets/<slug>)` (GM dossiers are
embedded into public pages, so relative links would break).

Sheets store only the *inputs*; the layout computes everything derivable
(in Liquid, so it works on stock GitHub Pages), using the ability/skill
tables in `_data/dnd.yml`. `_bin/charsheet.py` mirrors the computation in
Python, for scripts that need to check or report the numbers.

```yaml
cs:
  name: Vex Morradine
  race: Tiefling
  class: Rogue 10 / Ranger 3    # free text; level is not repeated if it has digits
  subclass: Inquisitive / Gloom Stalker
  level: 13                     # total level: drives the proficiency bonus
  cr: 10                        # used for proficiency only when level is absent
  # proficiency: 5              # override (e.g. house-ruled epic NPCs)
  background: ...
  alignment: Lawful neutral
  # rules: 2024                 # rules tooltips prefer the 2024 rules (default 2014)

  abilities: {str: 10, dex: 20, con: 12, int: 16, wis: 16, cha: 14}
  saves: [dex, int]                       # proficient saves
  skills: [athletics, intimidation]       # proficient skills ("Sleight of Hand" or sleightofhand)
  expertise: [insight, stealth]           # double proficiency
  jack_of_all_trades: false               # half proficiency on other checks + initiative
  bonuses:                                # flat adjustments, all optional
    saves: 1               # all saves (ring/cloak of protection...)
    checks: 0              # all ability checks (stone of good luck...)
    skills: {arcana: 3}    # individual skills
    initiative: 8          # Alert, Dread Ambusher...
    passive_perception: 5  # Observant
    spell: 3               # spell attack and save DC (rod of the pact keeper...)

  ac: 18
  ac_note: studded leather +1          # shown under the AC box
  speed: 30 ft.
  hp_max: 84
  # hp: 60                             # current HP, if different from max
  hit_dice: 10d8 + 3d10
  # initiative / passive_perception / spell_dc / spell_atk: overrides

  spell_ability: wis       # => spell DC and attack bonus
  spells:
    - {level: "1st (3 slots)", list: "Absorb Elements, Hunter's Mark"}

  weapons:
    # ability: str/dex/con/int/wis/cha, finesse (better of STR/DEX), or spell.
    # Attack = mod + proficiency (unless prof: false) + magic + atk_bonus.
    # Damage = dice + mod (not for spells unless dmg_mod: true) + magic + dmg_bonus,
    # then type and extra. Literal atk/dmg strings override; save: dex shows "DC N Dex".
    - {name: Sword cane, ability: dex, dice: 1d8, type: Piercing, dmg_bonus: 2, range: 5 ft., props: Dueling}
    - {name: Eldritch Blast, ability: spell, dice: 1d10, type: Force, dmg_mod: true, range: 120 ft.}
    - {name: Sneak Attack, dmg: +5d6, props: Once per turn}

  features:
    - {name: Favored Foe, source: Ranger, uses: 3/LR}
    - {name: Archdruid Wild Shape, source: Druid, ref: "classFeature:Archdruid|Druid||20"}
  traits: {size, senses, resistances, immunities, vulnerabilities, condition_immunities, languages}
  proficiencies: {armor, weapons, tools}
  equipment: [...]
  currency: {gp: 60}
```

The markdown body (tactics, feature descriptions, notes) renders below the
sheet in two columns.

### Rules tooltips (5etools)

In local GM builds, the names on a sheet (features, spells, weapons,
equipment, skills, senses, languages, condition immunities) link to their
rules on 2014.5e.tools / 5e.tools, with the rules text in a hover tooltip.
`_bin/5e.py` (run by `_bin/go.sh`; rerun it after editing a sheet)
resolves the names against the 5etools data and writes the gitignored
`_data/dnd5e.json` (plus any images, in `assets/5etools/`). The 5etools
data is NOT redistributable: the script clones it into the gitignored
`_external/` (never commit it, nor anything generated from it). Without the
data file (GitHub Pages), sheets render as plain text.

- Names are matched leniently: `(notes)`, `[notes]`, trailing `*`,
  `Feat:`-style prefixes and quantities are ignored, and the sheet's
  classes, subclass, race and each feature's `source` pick between
  same-named entries; "Fighting Style (Archery)" links to Archery.
- `rules: 2024` makes a sheet prefer the 2024 rules; names missing from one
  edition are looked up in the other.
- Pin a feature/weapon with `ref: "[kind:]Name[|args]"` using 5etools tag
  arguments (`spell:Revivify|XPHB`, `feat:Alert`, `optfeature:Agonizing Blast`,
  `classFeature:Cunning Action|Rogue||2`,
  `subclassFeature:Ear for Deceit|Rogue||Inquisitive|XGE|3`), or opt out
  with `ref: none`. In a spell list, pin one spell with `Name|SOURCE`.
- The script lists every name it could not resolve (homebrew, typos);
  `-v` lists every match, and `--lookup REF [--edition 2024]` tests a reference.
- In any page's prose: `{% include rule ref="Eye for Detail" %}` (optional
  `text="..."`); see `_includes/rule`.

### Foundry actor ingestion

`_bin/ingest-actor.py path/to/fvtt-Actor-name-XXXX.json` converts a Foundry
VTT actor export into `_pages/gm/charsheets/<slug>.draft.md` in the schema
above. It computes values from the Foundry data (proficiencies, AC from
armor or Unarmored Defense, speed, uses via `@scale`/`@prof`) and then
expresses anything the layout would not derive on its own as `bonuses`,
printing a NOTE for each discrepancy so it can be checked.

**Post-ingest checklist:**
1. Rename `.draft.md` to `.md` when satisfied
2. Review the NOTE lines (unexpected bonuses usually mean missed proficiencies)
3. Verify AC (especially shields/magic items) and speed (race traits, items)
4. Check uses/resources for complex `@scale` formulas
5. Fill in `background` and `alignment` if not in Foundry
6. Review feature descriptions for Foundry-specific markup that wasn't cleaned up
7. Remove `spell_ability` if the character is not truly a spellcaster

---

## Common Tasks Claude Code Can Help With

- **Review a session:**
  `_bin/review-session.py <page>` and review output
- **Review entity blurbs for a session** (the per-session `descriptions:` on
  dossiers/locales/orgs/creatures/relics, shown as each page's Chronicle):
  `_bin/descriptions.py show 17e09` prints the episode, its GM notes and all
  blurbs; write a YAML of corrections and `_bin/descriptions.py apply edits.yaml`.
  Blurbs must not reveal GM-only notes; length should track involvement.
- **Check rules tooltips on charsheets:**
  `_bin/5e.py` and review the unresolved names (add `ref:`s, fix typos)
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
