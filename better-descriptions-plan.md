# Session-Based Chronological Descriptions Implementation Plan

## Overview
Transform descriptions in dossiers, creatures, locales, orgs, and relics from single prose blocks into chronological, session-organized entries that show the evolution of understanding throughout the campaign. Use an append-only approach where new sessions add paragraphs rather than editing existing content.

**Scope**: 240+ items (120+ dossiers, 48 creatures, 41 locales, 20 orgs, 12 relics)
**Approach**: Manual conversion with structured YAML-markdown format
**Display**: Collapsible timeline-style cards (latest session expanded)

---

## Data Structure Format

### YAML Array with Markdown Content

```yaml
---
title: Isis Ra'ksh
statbox:
  race: [elf (wood), changeling]
  case: ["02", "12"]
descriptions:
  - session: "02"
    content: |
      Isis Ra'ksh is a druid believed to have orchestrated the theft
      of the Necronomicon relic. Initially appeared as antagonist in
      the Exchange and Extortion case.
  - session: "12e08"
    content: ""  # Placeholder - to be expanded
  - session: "17e09"
    content: |
      Following the bloom curse incident at Grohnea's cottage, the SPI
      learned through Sissae's memories that Isis deliberately sacrificed
      herself to break the White Crane's hold on Peregrine Shackleton.
---
```

### Key Principles
- **Sessions**: Use case/episode IDs matching session log naming (e.g., "02", "12e08", "17e09")
- **Placeholders**: For items with multiple cases (e.g., `case: ["01", "09", "10"]`), create placeholder entries with `content: ""` for sessions not yet detailed
- **Markdown**: Use `content: |` for multi-line YAML string with full markdown support
- **Chronological**: Sessions listed oldest to newest
- **Append-only**: Never edit existing session content, only add new entries

---

## Implementation Steps

### Step 1: Create Display Component (2-3 hours)

**File**: `_includes/sessions`

```liquid
{% if page.descriptions %}
<div class="sessions">
  <h2>Chronicle</h2>
  {% assign sorted = page.descriptions | sort: "session" %}
  {% for desc in sorted %}
    {% unless desc.content == "" %}
      <details class="session-card" {% if forloop.last %}open{% endif %}>
        <summary>
          <span class="session-tag">Session {{ desc.session }}</span>
        </summary>
        <div class="session-content">
          {{ desc.content | markdownify }}
        </div>
      </details>
    {% endunless %}
  {% endfor %}
</div>
{% endif %}
```

**Features**:
- Skip empty placeholders in display (`unless desc.content == ""`)
- Latest session expanded by default (`{% if forloop.last %}open{% endif %}`)
- Chronological order (oldest to newest)
- Markdown rendering for rich prose

### Step 2: Add CSS Styling (1 hour)

**File**: `assets/css/style.css`

Add styles that match existing timeline component aesthetic:

```css
.sessions {
  margin: 2em 0;
  border-left: 3px solid sandybrown;
  padding-left: 1em;
}

.session-card {
  margin-bottom: 0.75em;
  background: #f5f5f5;
  border-radius: 8px;
  padding: 0.75em 1em;
  border: 1px solid #ddd;
}

.session-card[open] {
  background: #fff;
}

.session-card summary {
  cursor: pointer;
  font-variant: small-caps;
  color: sandybrown;
  font-weight: bold;
  user-select: none;
}

.session-card summary:hover {
  color: #b8733f;
}

.session-tag {
  font-size: 1.1em;
}

.session-content {
  margin-top: 0.75em;
  padding-top: 0.5em;
  border-top: 1px solid #eee;
  line-height: 1.6;
}

/* Mobile responsive */
@media (max-width: 600px) {
  .sessions {
    padding-left: 0.5em;
  }

  .session-card {
    padding: 0.5em;
  }
}
```

### Step 3: Integrate Component into Layout (30 min)

**File**: `_layouts/page.html`

Update the page layout to conditionally display session-based descriptions or traditional content:

```liquid
<article>
  <h1>{{ page.title }}</h1>

  {% include statbox %}

  {% if page.descriptions %}
    {% include sessions %}
  {% else %}
    {{ content }}
  {% endif %}

  {% include gm %}
</article>
```

This ensures backward compatibility - items without `descriptions:` field continue to display traditional markdown body.

### Step 4: Manual Conversion Workflow (Ongoing)

For each item to convert:

1. **Review session logs** in `_pages/gm/events/` to identify which sessions mention the item
2. **Determine sessions** from the `case:` field in front matter (e.g., `case: ["02", "12"]`)
3. **Create descriptions array** with:
   - Entry for each session in `case:` field
   - First session gets existing description content
   - Later sessions get placeholder `content: ""` or initial content if known
4. **Move existing body** into first session's `content:` block
5. **Add future sessions** as you review session logs and write updates

**Example workflow for Isis Ra'ksh**:
```bash
# 1. Open file
vim _pages/dossiers/isis-raksh.md

# 2. Note case field shows: case: ["02", "12"]

# 3. Add descriptions array to front matter:
descriptions:
  - session: "02"
    content: |
      [move existing body content here]
  - session: "12e08"
    content: ""  # Placeholder for later

# 4. Delete old body content below front matter (now in session "02")

# 5. Save and preview in browser
```

### Step 5: Establish Conversion Priority (Optional)

Suggested order for manual conversion:
1. **High-priority NPCs/items** mentioned in recent sessions (cases 15-17)
2. **Recurring characters** with multiple case appearances
3. **Major locations** and organizations
4. **One-off items** as time permits

This allows you to see benefits immediately on most-viewed pages while spreading the conversion work over time.

### Step 6: Create Editor Snippets (30 min)

**For VS Code** - create `.vscode/snippets.code-snippets`:

```json
{
  "Session Description Entry": {
    "prefix": "sess",
    "scope": "yaml",
    "body": [
      "- session: \"$1\"",
      "  content: |",
      "    $0"
    ],
    "description": "Add new session description entry"
  },

  "Session Placeholder": {
    "prefix": "sessph",
    "scope": "yaml",
    "body": [
      "- session: \"$1\"",
      "  content: \"\""
    ],
    "description": "Add session placeholder"
  }
}
```

**Usage**: Type `sess` then Tab to insert a new session entry template.

---

## Verification & Testing

### Testing Checklist

**Phase 1: Component Testing**
- [ ] Create `_includes/sessions` component
- [ ] Add CSS to `assets/css/style.css`
- [ ] Update `_layouts/page.html` to include component
- [ ] Run `bundle exec jekyll serve` to start local server
- [ ] Verify no build errors

**Phase 2: Prototype Testing**
- [ ] Convert 2-3 test items manually (suggested: isis-raksh, necronomicon, sennik-cromwell)
- [ ] Verify collapsible behavior works (click to open/close)
- [ ] Confirm latest session is expanded by default
- [ ] Test markdown rendering in content blocks (bold, links, lists)
- [ ] Check mobile responsive design (resize browser)

**Phase 3: Cross-Type Testing**
- [ ] Test at least one item from each type:
  - Dossier (e.g., isis-raksh.md)
  - Creature (e.g., elves.md)
  - Locale (e.g., cognitutus.md)
  - Organization (e.g., spi.md)
  - Relic (e.g., necronomicon.md)
- [ ] Verify backward compatibility (unconverted items still display normally)

**Phase 4: Content Verification**
- [ ] Compare before/after in browser for converted items
- [ ] Verify no content loss during conversion
- [ ] Check that internal links still work
- [ ] Verify images and other media render correctly

**Phase 5: Build Performance**
- [ ] Note Jekyll build time before changes
- [ ] Re-measure after converting 10-20 items
- [ ] Ensure build time increase is acceptable (<20% increase)

### Success Criteria
✅ All existing content preserved
✅ New session updates display chronologically
✅ Collapsible UI works smoothly
✅ Latest session expanded by default
✅ Mobile-friendly responsive design
✅ Consistent with existing site aesthetic
✅ Backward compatible with unconverted items

---

## Critical Files

### To Create
- `_includes/sessions` - Core display component for chronological descriptions

### To Modify
- `assets/css/style.css` - Add sessions styling (append to end of file)
- `_layouts/page.html` - Integrate component (line ~19, after statbox include)

### For Testing/Prototyping
- `_pages/dossiers/isis-raksh.md` - Multi-session character (cases 02, 12)
- `_pages/relics/necronomicon.md` - Complex narrative item
- `_pages/dossiers/sennik-cromwell.md` - Character with many appearances (cases 01, 09, 10)

### Reference
- `_includes/timeline` - Existing timeline component to reference for styling consistency
- `_pages/gm/events/case-*.md` - Session logs to review when writing new descriptions
- `_pages/index.md` - Example of conditional display logic

---

## Ongoing Workflow (After Implementation)

After each gaming session:

1. **Review session log** (e.g., `case-17e10.md`)
2. **Identify mentioned items** (dossiers, creatures, locales, orgs, relics)
3. **For each item**:
   - Open the markdown file
   - Add new entry to `descriptions:` array
   - Write session update in `content:` block
4. **Commit changes**: `git commit -m "Add session 17e10 updates for [items]"`

**Estimated time**: 30-60 minutes per session

---

## Notes & Considerations

- **Manual review approach**: Allows you to thoughtfully attribute existing content to appropriate sessions and write meaningful updates
- **Incremental conversion**: No need to convert all 240+ items immediately - can convert as items become relevant in new sessions
- **Placeholder benefits**: Empty placeholders (`content: ""`) show which sessions mention an item even before detailed description is written
- **YAML syntax**: Be careful with indentation (2 spaces per level) and use `|` for multi-line content
- **Git-friendly**: Each session's updates are clearly visible in diffs when new entries are added
