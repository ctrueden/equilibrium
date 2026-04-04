#!/usr/bin/env python3
"""
ingest-actor.py — Convert a Foundry VTT actor JSON export to a Jekyll character sheet page.

Usage:
    _bin/ingest-actor.py path/to/fvtt-Actor-name-XXXX.json [output_dir]

Produces:
    _pages/gm/charsheets/<slug>.draft.md

Requires: PyYAML (pip install pyyaml)
"""

import sys
import json
import math
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ABILITY_NAMES = {
    'str': 'STR', 'dex': 'DEX', 'con': 'CON',
    'int': 'INT', 'wis': 'WIS', 'cha': 'CHA',
}

ABILITY_FULL = {
    'str': 'Strength', 'dex': 'Dexterity', 'con': 'Constitution',
    'int': 'Intelligence', 'wis': 'Wisdom', 'cha': 'Charisma',
}

SKILL_DATA = [
    # (key, full_name, ability_key)
    ('acr', 'Acrobatics',       'dex'),
    ('ani', 'Animal Handling',  'wis'),
    ('arc', 'Arcana',           'int'),
    ('ath', 'Athletics',        'str'),
    ('dec', 'Deception',        'cha'),
    ('his', 'History',          'int'),
    ('ins', 'Insight',          'wis'),
    ('itm', 'Intimidation',     'cha'),
    ('inv', 'Investigation',    'int'),
    ('med', 'Medicine',         'wis'),
    ('nat', 'Nature',           'int'),
    ('prc', 'Perception',       'wis'),
    ('prf', 'Performance',      'cha'),
    ('per', 'Persuasion',       'cha'),
    ('rel', 'Religion',         'int'),
    ('slt', 'Sleight of Hand',  'dex'),
    ('ste', 'Stealth',          'dex'),
    ('sur', 'Survival',         'wis'),
]

PROPERTY_NAMES = {
    'ada': 'Adamantine', 'amm': 'Ammunition', 'bru': 'Brutal',
    'fin': 'Finesse', 'fir': 'Firearm', 'foc': 'Focus',
    'hvy': 'Heavy', 'lgt': 'Light', 'lod': 'Loading',
    'mgc': 'Magical', 'rch': 'Reach', 'ret': 'Returning',
    'sil': 'Silver', 'spc': 'Special', 'thr': 'Thrown',
    'two': 'Two-handed', 'ver': 'Versatile',
}

DAMAGE_TYPE_NAMES = {
    'acid': 'acid', 'bludgeoning': 'bludgeoning', 'cold': 'cold',
    'fire': 'fire', 'force': 'force', 'lightning': 'lightning',
    'necrotic': 'necrotic', 'piercing': 'piercing', 'poison': 'poison',
    'psychic': 'psychic', 'radiant': 'radiant', 'slashing': 'slashing',
    'thunder': 'thunder',
}

CONDITION_NAMES = {
    'blinded': 'Blinded', 'charmed': 'Charmed', 'deafened': 'Deafened',
    'exhaustion': 'Exhaustion', 'frightened': 'Frightened', 'grappled': 'Grappled',
    'incapacitated': 'Incapacitated', 'invisible': 'Invisible', 'paralyzed': 'Paralyzed',
    'petrified': 'Petrified', 'poisoned': 'Poisoned', 'prone': 'Prone',
    'restrained': 'Restrained', 'stunned': 'Stunned', 'unconscious': 'Unconscious',
}

RECOVERY_PERIODS = {
    'sr': 'SR', 'lr': 'LR', 'day': 'day',
    'turn': 'turn', 'round': 'round',
}

ARMOR_PROFICIENCY_NAMES = {
    'lgt': 'Light armor', 'med': 'Medium armor', 'hvy': 'Heavy armor',
    'shl': 'Shields', 'natural': 'Natural armor',
}

WEAPON_PROFICIENCY_NAMES = {
    'sim': 'Simple weapons', 'mar': 'Martial weapons',
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[''`]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def find_jekyll_root(start: Path) -> Path:
    for p in [start] + list(start.parents):
        if (p / "_pages").is_dir():
            return p
    return start


def signed(n: int) -> str:
    return f"+{n}" if n >= 0 else str(n)


def mod(score: int) -> int:
    return (score - 10) // 2


def prof_bonus(level: int) -> int:
    return 2 + (level - 1) // 4


def strip_html(html: str) -> str:
    """Strip HTML tags, Foundry markup, decode entities, normalize whitespace."""
    if not html:
        return ""
    # Foundry inline dice rolls: [[/r d12]] → d12, [[/damage 1d6]] → 1d6
    text = re.sub(r'\[\[/(?:r|damage|save|check)\s+([^\]]+)\]\]', r'\1', html)
    # Foundry @spell[name], @action[name], @condition[name], etc. → just the name
    text = re.sub(r'@[a-zA-Z]+\[([^\]|]+)(?:\|[^\]]*)?\]', r'\1', text)
    # Foundry &Reference[...] and &amp;Reference[...] (HTML-encoded) → just the value part
    text = re.sub(r'(?:&amp;|&)[A-Z][a-zA-Z]+\[(?:[^=\]]*=)?([^\]]+)\]', r'\1', text)
    # Also handle HTML-encoded &amp;Reference after entity decode happens later:
    # (Pre-decode any &amp; that precede Reference to catch double-encoding)
    text = text.replace('&amp;Reference', '&Reference')
    # @variantrule[text|source|...] → drop entirely (too verbose)
    text = re.sub(r'@variantrule\[[^\]]*\]', '', text)
    # Block-level tags become newlines
    text = re.sub(r'</(p|div|li|h[1-6])>', '\n', text, flags=re.I)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.I)
    # Strip remaining tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode entities
    entities = {
        '&amp;': '&', '&lt;': '<', '&gt;': '>', '&nbsp;': ' ',
        '&quot;': '"', '&#39;': "'", '&#42;': '*', '&#149;': '•',
        '&mdash;': '—', '&ndash;': '–', '&hellip;': '…',
    }
    for ent, char in entities.items():
        text = text.replace(ent, char)
    text = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)
    # Normalize whitespace but preserve paragraph breaks
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in text.split('\n')]
    # Remove blank line runs
    result = []
    prev_blank = False
    for line in lines:
        if not line:
            if not prev_blank:
                result.append('')
            prev_blank = True
        else:
            result.append(line)
            prev_blank = False
    return '\n'.join(result).strip()


def resolve_scale(uses_max: str, scales: dict, level: int, prof: int = 0) -> str:
    """Resolve @scale.class.id and @prof references."""
    if not uses_max:
        return ''
    s = str(uses_max).strip()
    if s == '@prof':
        return str(prof) if prof else s
    if not s.startswith('@scale.'):
        return s
    # @scale.barbarian.rages → look up in scales dict
    # Strip leading '@scale.' prefix
    key = s[len('@scale.'):]
    if key in scales:
        scale_table = scales[key]
        val = None
        for lv in sorted(scale_table.keys()):
            if lv <= level:
                val = scale_table[lv]
        if val is not None:
            return str(val)
    return s  # fallback


def build_scale_table(items: list) -> dict:
    """Build {class.scale_id: {level: value}} from class advancement."""
    scales = {}
    for item in items:
        if item['type'] not in ('class', 'subclass'):
            continue
        class_id = item['system'].get('identifier', item['name'].lower().replace(' ', '-'))
        for adv in item['system'].get('advancement', []):
            if adv.get('type') != 'ScaleValue':
                continue
            cfg = adv.get('configuration', {})
            scale_id = cfg.get('identifier', '')
            scale = cfg.get('scale', {})
            table = {}
            for lv_str, val_obj in scale.items():
                try:
                    lv = int(lv_str)
                    val = val_obj.get('value') if isinstance(val_obj, dict) else val_obj
                    table[lv] = val
                except (ValueError, TypeError):
                    pass
            if scale_id and table:
                key = f"{class_id}.{scale_id}"
                scales[key] = table
    return scales


def collect_proficiencies(items: list) -> dict:
    """Collect armor/weapon/tool proficiency grants from advancement."""
    armor_profs = set()
    weapon_profs = set()
    tool_profs = set()
    save_profs = set()
    skill_profs = set()

    for item in items:
        if item['type'] not in ('class', 'subclass', 'race', 'background', 'feat'):
            continue
        for adv in item['system'].get('advancement', []):
            if adv.get('type') != 'Trait':
                continue
            cfg = adv.get('configuration', {})
            # grants: ["armor:lgt", "weapon:sim", "saves:str", "skills:ath", ...]
            for grant in cfg.get('grants', []):
                _apply_trait_grant(grant, armor_profs, weapon_profs, tool_profs, save_profs, skill_profs)
            # chosen values (for choice-based)
            for chosen in adv.get('value', {}).get('chosen', []):
                _apply_trait_grant(chosen, armor_profs, weapon_profs, tool_profs, save_profs, skill_profs)

    return {
        'armor': armor_profs,
        'weapon': weapon_profs,
        'tool': tool_profs,
        'save': save_profs,
        'skill': skill_profs,
    }


def _apply_trait_grant(grant, armor_profs, weapon_profs, tool_profs, save_profs, skill_profs):
    if ':' not in grant:
        return
    category, value = grant.split(':', 1)
    if category == 'armor':
        armor_profs.add(value)
    elif category == 'weapon':
        weapon_profs.add(value)
    elif category == 'tool':
        tool_profs.add(value)
    elif category == 'saves':
        save_profs.add(value)
    elif category == 'skills':
        skill_profs.add(value)


def is_weapon_proficient(weapon_item: dict, weapon_profs: set) -> bool:
    """Check if character is proficient with this weapon."""
    w_type = weapon_item['system'].get('type', {}).get('value', '')
    base_item = weapon_item['system'].get('type', {}).get('baseItem', '')
    # martialM/martialR → need 'mar'
    # simpleM/simpleR → need 'sim'
    if w_type.startswith('simple') and 'sim' in weapon_profs:
        return True
    if w_type.startswith('martial') and 'mar' in weapon_profs:
        return True
    # Specific weapon proficiency
    if base_item and base_item in weapon_profs:
        return True
    return False


def compute_ac(items: list, abilities: dict, level: int) -> int:
    """Compute AC from equipped armor or Unarmored Defense."""
    dex_mod = mod(abilities['dex']['value'])
    con_mod = mod(abilities['con']['value'])
    wis_mod = mod(abilities['wis']['value'])

    # Check for equipped armor
    for item in items:
        if item['type'] == 'equipment':
            armor_type = item['system'].get('type', {}).get('value', '')
            if armor_type in ('light', 'medium', 'heavy') and item['system'].get('equipped', False):
                base_ac = item['system'].get('armor', {}).get('value', 10)
                if armor_type == 'light':
                    return base_ac + dex_mod
                elif armor_type == 'medium':
                    return base_ac + min(dex_mod, 2)
                else:  # heavy
                    return base_ac

    # Check for Unarmored Defense (Barbarian: 10 + DEX + CON)
    has_barb_ud = any(
        item['name'] == 'Unarmored Defense' and
        item['system'].get('type', {}).get('value') == 'class'
        for item in items if item['type'] == 'feat'
    )
    if has_barb_ud:
        return 10 + dex_mod + con_mod

    # Check for Unarmored Defense (Monk: 10 + DEX + WIS)
    has_monk_ud = any(
        item['name'] == 'Unarmored Defense' and
        item['system'].get('requirements', '').lower().startswith('monk')
        for item in items if item['type'] == 'feat'
    )
    if has_monk_ud:
        return 10 + dex_mod + wis_mod

    # Default: 10 + DEX
    return 10 + dex_mod


def compute_speed(items: list, sys_movement: dict) -> str:
    """Compute walking speed from race movement + class bonuses."""
    walk = sys_movement.get('walk') or 0
    fly = sys_movement.get('fly') or 0
    swim = sys_movement.get('swim') or 0
    climb = sys_movement.get('climb') or 0

    # Race movement overrides if actor walk is 0
    if not walk:
        for item in items:
            if item['type'] == 'race':
                mv = item['system'].get('movement', {})
                walk = mv.get('walk') or 30
                fly = fly or (mv.get('fly') or 0)
                swim = swim or (mv.get('swim') or 0)
                climb = climb or (mv.get('climb') or 0)
                break
        if not walk:
            walk = 30

    # Class bonuses: Barbarian Fast Movement (+10)
    for item in items:
        if item['type'] == 'feat' and item['name'] == 'Fast Movement':
            walk += 10
            break

    parts = [f"{walk} ft."]
    if fly:
        parts.append(f"fly {fly} ft.")
    if swim:
        parts.append(f"swim {swim} ft.")
    if climb:
        parts.append(f"climb {climb} ft.")
    return ", ".join(parts)


def weapon_attack_string(weapon_item: dict, abilities: dict, prof: int, weapon_profs: set) -> tuple:
    """Return (attack_bonus_str, damage_str) for a weapon."""
    sys_data = weapon_item['system']
    props = set(sys_data.get('properties', []))
    w_type = sys_data.get('type', {}).get('value', '')
    is_ranged = 'R' in w_type.upper() and not ('M' in w_type.upper())

    str_mod = mod(abilities['str']['value'])
    dex_mod = mod(abilities['dex']['value'])

    # Determine ability used
    if 'fin' in props:
        ability_mod_val = max(str_mod, dex_mod)
    elif is_ranged:
        ability_mod_val = dex_mod
    else:
        ability_mod_val = str_mod

    proficient = is_weapon_proficient(weapon_item, weapon_profs)
    atk_bonus = ability_mod_val + (prof if proficient else 0)

    # Damage
    base_dmg = sys_data.get('damage', {}).get('base', {})
    custom = base_dmg.get('custom', {})
    num = base_dmg.get('number')
    denom = base_dmg.get('denomination')
    bonus_str = (base_dmg.get('bonus') or '').strip()
    dmg_types = base_dmg.get('types', [])
    type_str = dmg_types[0].capitalize() if dmg_types else ''

    if custom.get('enabled') and custom.get('formula'):
        formula = custom['formula'].strip()
        # '@mod' in bonus means add ability modifier
        if '@mod' in bonus_str:
            if formula.lstrip('-').isdigit():
                flat = int(formula) + ability_mod_val
                dmg = str(flat)
            else:
                dmg = f"{formula}+{ability_mod_val}" if ability_mod_val >= 0 else f"{formula}{ability_mod_val}"
        else:
            dmg = formula
    elif num and denom:
        die_str = f"{num}d{denom}"
        if ability_mod_val != 0:
            dmg = f"{die_str}{signed(ability_mod_val)}"
        else:
            dmg = die_str
    else:
        dmg = "—"

    if type_str:
        dmg = f"{dmg} {type_str}"

    # Range string
    rng_data = sys_data.get('range', {})
    rng_val = rng_data.get('value') or 5
    rng_long = rng_data.get('long')
    rng_units = rng_data.get('units') or 'ft'
    if rng_long:
        range_str = f"{rng_val}/{rng_long} {rng_units}."
    else:
        range_str = f"{rng_val} {rng_units}."

    # Properties display
    prop_names = [PROPERTY_NAMES.get(p, p) for p in sorted(props) if p in PROPERTY_NAMES]

    return signed(atk_bonus), dmg, range_str, ", ".join(prop_names)


def build_uses_str(uses_data: dict, scales: dict, level: int, prof: int = 0) -> str:
    """Build a human-readable uses string like '4/LR' or '1/SR'."""
    if not uses_data:
        return ''
    max_val = uses_data.get('max', '')
    if not max_val:
        return ''
    resolved = resolve_scale(str(max_val), scales, level, prof)
    recovery = uses_data.get('recovery', [])
    if recovery:
        period = recovery[0].get('period', '')
        period_str = RECOVERY_PERIODS.get(period, period.upper())
        return f"{resolved}/{period_str}"
    return resolved


# ---------------------------------------------------------------------------
# Main build function
# ---------------------------------------------------------------------------

def build_charsheet(actor: dict) -> dict:
    """Extract and compute all character sheet data from a Foundry actor."""
    sys_data = actor.get('system', {})
    items = actor.get('items', [])
    abilities = sys_data.get('abilities', {})
    skills_data = sys_data.get('skills', {})
    attrs = sys_data.get('attributes', {})
    details = sys_data.get('details', {})
    traits = sys_data.get('traits', {})
    currency = sys_data.get('currency', {})

    # --- Identity ---
    name = actor.get('name', 'Unknown')
    actor_type = actor.get('type', 'npc')

    # Class, subclass, race
    class_item = next((i for i in items if i['type'] == 'class'), None)
    subclass_item = next((i for i in items if i['type'] == 'subclass'), None)
    race_item = next((i for i in items if i['type'] == 'race'), None)

    class_name = class_item['name'] if class_item else ''
    subclass_name = subclass_item['name'] if subclass_item else ''
    race_name = race_item['name'] if race_item else details.get('race', '')
    level = class_item['system'].get('levels', 0) if class_item else 0
    hd_denom = class_item['system']['hd']['denomination'] if class_item else 'd8'

    background = details.get('background', {})
    if isinstance(background, dict):
        background = background.get('name', '')
    alignment = details.get('alignment', '')
    xp = details.get('xp', {})
    if isinstance(xp, dict):
        xp = xp.get('value', 0)

    cr = details.get('cr', '')

    # --- Proficiency bonus ---
    prof = prof_bonus(level) if level else 2

    # --- Build scale tables ---
    scales = build_scale_table(items)

    # --- Collect proficiencies from advancement ---
    profs = collect_proficiencies(items)

    # --- Ability scores ---
    abil_list = []
    abil_mods = {}
    for key in ('str', 'dex', 'con', 'int', 'wis', 'cha'):
        score = abilities.get(key, {}).get('value', 10)
        m = mod(score)
        abil_mods[key] = m
        abil_list.append({
            'key': key,
            'name': ABILITY_NAMES[key],
            'score': score,
            'mod': signed(m),
        })

    # --- Saving throws ---
    # Proficient saves come from class advancement 'saves:*' grants
    save_prof_keys = profs['save']
    # Also check system.abilities[key].proficient directly
    for key in ('str', 'dex', 'con', 'int', 'wis', 'cha'):
        if abilities.get(key, {}).get('proficient', 0):
            save_prof_keys.add(key)

    saves_list = []
    for key in ('str', 'dex', 'con', 'int', 'wis', 'cha'):
        is_prof = key in save_prof_keys
        bonus = abil_mods[key] + (prof if is_prof else 0)
        saves_list.append({
            'name': ABILITY_FULL[key],
            'bonus': signed(bonus),
            'prof': is_prof,
        })

    # --- Skills ---
    skill_list = []
    for skill_key, skill_name, ability_key in SKILL_DATA:
        skill_entry = skills_data.get(skill_key, {})
        prof_level = skill_entry.get('value', 0)  # 0, 0.5, 1, 2
        a_mod = abil_mods.get(ability_key, 0)

        if prof_level == 2:
            bonus_val = a_mod + 2 * prof
            marker = '●●'
        elif prof_level == 1:
            bonus_val = a_mod + prof
            marker = '●'
        elif prof_level == 0.5:
            bonus_val = a_mod + math.floor(prof / 2)
            marker = '◐'
        else:
            bonus_val = a_mod
            marker = ''

        skill_list.append({
            'name': skill_name,
            'ability': ABILITY_NAMES.get(ability_key, ability_key.upper()),
            'bonus': signed(bonus_val),
            'marker': marker,
        })

    # Passive Perception
    prc_entry = next((s for s in skill_list if s['name'] == 'Perception'), None)
    prc_bonus = int(prc_entry['bonus']) if prc_entry else abil_mods.get('wis', 0)
    passive_perception = 10 + prc_bonus

    # --- Combat stats ---
    hp = attrs.get('hp', {}).get('max', attrs.get('hp', {}).get('value', 0))
    hp_current = attrs.get('hp', {}).get('value', hp)
    hit_dice = f"{level}{hd_denom}" if level else hd_denom

    ac = compute_ac(items, abilities, level)
    speed = compute_speed(items, attrs.get('movement', {}))
    initiative = signed(abil_mods.get('dex', 0))

    # Spellcasting
    spell_ability_key = attrs.get('spellcasting', '')
    spell_mod = abil_mods.get(spell_ability_key, 0) if spell_ability_key else 0
    spell_dc = 8 + prof + spell_mod if spell_ability_key else 0
    spell_atk = signed(prof + spell_mod) if spell_ability_key else ''

    # --- Weapons ---
    weapon_profs = profs['weapon']
    weapons_list = []
    for item in items:
        if item['type'] != 'weapon':
            continue
        qty = item['system'].get('quantity', 1)
        display_name = item['name']
        if qty > 1:
            display_name = f"{display_name} ×{qty}"
        atk, dmg, rng, props_str = weapon_attack_string(item, abilities, prof, weapon_profs)
        weapons_list.append({
            'name': display_name,
            'atk': atk,
            'dmg': dmg,
            'range': rng,
            'props': props_str,
        })

    # --- Traits ---
    size_map = {
        'tiny': 'Tiny', 'sm': 'Small', 'med': 'Medium',
        'lg': 'Large', 'huge': 'Huge', 'grg': 'Gargantuan',
    }
    size = size_map.get(traits.get('size', 'med'), 'Medium')

    def trait_list(trait_key):
        t = traits.get(trait_key, {})
        vals = [v.capitalize() for v in t.get('value', [])]
        custom = t.get('custom', '')
        if custom:
            vals.append(custom)
        return ', '.join(vals) if vals else ''

    resistances = trait_list('dr')
    immunities = trait_list('di')
    vulnerabilities = trait_list('dv')
    condition_immunities_raw = traits.get('ci', {}).get('value', [])
    condition_imm = ', '.join(CONDITION_NAMES.get(c, c.capitalize()) for c in condition_immunities_raw)
    if traits.get('ci', {}).get('custom'):
        condition_imm = (condition_imm + ', ' + traits['ci']['custom']).strip(', ')

    lang_vals = [v.capitalize() for v in traits.get('languages', {}).get('value', [])]
    lang_custom = traits.get('languages', {}).get('custom', '')
    if lang_custom:
        lang_vals.append(lang_custom)
    languages = ', '.join(lang_vals)

    senses_data = attrs.get('senses', {})
    sense_parts = []
    for s in ('darkvision', 'blindsight', 'tremorsense', 'truesight'):
        val = senses_data.get(s)
        if val:
            units = senses_data.get('units') or 'ft'
            sense_parts.append(f"{s.capitalize()} {val} {units}.")
    if senses_data.get('special'):
        sense_parts.append(senses_data['special'])
    senses_str = ', '.join(sense_parts)

    # --- Proficiency display ---
    armor_prof_list = [ARMOR_PROFICIENCY_NAMES.get(a, a) for a in sorted(profs['armor'])]
    weapon_prof_list = [WEAPON_PROFICIENCY_NAMES.get(w, w) for w in sorted(profs['weapon'])]
    tool_prof_list = sorted(profs['tool'])

    # --- Features ---
    features_list = []
    features_descriptions = {}  # name → description text

    # Features are feats of various types: 'race', 'class', 'background', 'feat', 'monster'
    source_order = ['race', 'class', 'background', 'feat', 'monster', '']
    feat_items = [i for i in items if i['type'] == 'feat']
    feat_items.sort(key=lambda i: (
        source_order.index(i['system'].get('type', {}).get('value', ''))
        if i['system'].get('type', {}).get('value', '') in source_order else len(source_order),
        i.get('sort', 0)
    ))

    for item in feat_items:
        feat_source = item['system'].get('type', {}).get('value', 'feat').capitalize()
        uses_data = item['system'].get('uses', {})
        uses_str = build_uses_str(uses_data, scales, level, prof)

        feat_entry = {
            'name': item['name'],
            'source': feat_source,
        }
        if uses_str:
            feat_entry['uses'] = uses_str

        features_list.append(feat_entry)

        # Description for body text
        desc_html = item['system'].get('description', {}).get('value', '')
        desc_text = strip_html(desc_html)
        if desc_text:
            features_descriptions[item['name']] = desc_text

    # --- Spells ---
    spell_items = [i for i in items if i['type'] == 'spell']
    spells_by_level = {}
    for sp in spell_items:
        lv = sp['system'].get('level', 0)
        spells_by_level.setdefault(lv, []).append(sp['name'])

    # --- Equipment ---
    equipment_list = []
    for item in items:
        if item['type'] in ('container', 'loot', 'consumable', 'equipment'):
            # Skip equipped armor (already handled in combat stats)
            if item['type'] == 'equipment':
                armor_type = item['system'].get('type', {}).get('value', '')
                if armor_type in ('light', 'medium', 'heavy'):
                    continue
            qty = item['system'].get('quantity', 1)
            name_str = item['name']
            if qty > 1:
                name_str = f"{name_str} ×{qty}"
            equipment_list.append(name_str)

    # --- Currency ---
    currency_data = {
        'pp': currency.get('pp', 0),
        'gp': currency.get('gp', 0),
        'ep': currency.get('ep', 0),
        'sp': currency.get('sp', 0),
        'cp': currency.get('cp', 0),
    }

    return {
        # Identity
        'name': name,
        'actor_type': actor_type,
        'race': race_name,
        'class': class_name,
        'subclass': subclass_name,
        'level': level,
        'background': background or '',
        'alignment': alignment or '',
        'xp': xp or 0,
        'cr': cr,
        # Derived
        'proficiency': signed(prof),
        'ac': ac,
        'initiative': initiative,
        'speed': speed,
        'hp': hp_current,
        'hp_max': hp,
        'hit_dice': hit_dice,
        'passive_perception': passive_perception,
        # Spellcasting
        'spell_ability': ABILITY_FULL.get(spell_ability_key, '') if spell_ability_key else '',
        'spell_dc': spell_dc if spell_ability_key else '',
        'spell_atk': spell_atk,
        'spells_by_level': spells_by_level,
        # Lists
        'abilities': abil_list,
        'saves': saves_list,
        'skills': skill_list,
        'weapons': weapons_list,
        'features': features_list,
        'features_descriptions': features_descriptions,
        'equipment': equipment_list,
        'currency': currency_data,
        # Traits
        'traits': {
            'size': size,
            'resistances': resistances,
            'immunities': immunities,
            'vulnerabilities': vulnerabilities,
            'condition_immunities': condition_imm,
            'languages': languages,
            'senses': senses_str,
        },
        'proficiencies': {
            'armor': ', '.join(armor_prof_list) if armor_prof_list else '',
            'weapons': ', '.join(weapon_prof_list) if weapon_prof_list else '',
            'tools': ', '.join(tool_prof_list) if tool_prof_list else '',
        },
    }


# ---------------------------------------------------------------------------
# Output generation
# ---------------------------------------------------------------------------

def build_class_line(cs: dict) -> str:
    parts = [cs['class']]
    if cs['level']:
        parts[0] += f" {cs['level']}"
    if cs['subclass']:
        parts.append(f"({cs['subclass']})")
    return ' '.join(parts)


def generate_page(cs: dict) -> str:
    class_line = build_class_line(cs)
    title_parts = [cs['name']]
    if class_line:
        title_parts.append(class_line)
    page_title = ' — '.join(title_parts)

    lines = ['---']
    lines.append(f'layout: charsheet')
    lines.append(f'title: "{page_title}"')
    lines.append('')
    lines.append('cs:')

    def y(key, val, indent=2):
        """Emit a YAML key: value line."""
        prefix = ' ' * indent
        if val is None or val == '':
            lines.append(f'{prefix}{key}: ""')
        elif isinstance(val, bool):
            lines.append(f'{prefix}{key}: {"true" if val else "false"}')
        elif isinstance(val, (int, float)):
            lines.append(f'{prefix}{key}: {val}')
        else:
            # Quote strings that need it
            s = str(val)
            if any(c in s for c in ':#{}[]|>&*!,?@`\'"') or s.startswith(' ') or s in ('true', 'false', 'null', ''):
                escaped = s.replace('"', '\\"')
                lines.append(f'{prefix}{key}: "{escaped}"')
            else:
                lines.append(f'{prefix}{key}: {s}')

    # Identity
    y('name', cs['name'])
    y('actor_type', cs['actor_type'])
    y('race', cs['race'])
    y('class', cs['class'])
    y('subclass', cs['subclass'])
    y('level', cs['level'])
    if cs['cr']:
        y('cr', cs['cr'])
    y('background', cs['background'])
    y('alignment', cs['alignment'])
    lines.append('')

    # Combat stats
    y('proficiency', cs['proficiency'])
    y('ac', cs['ac'])
    y('initiative', cs['initiative'])
    y('speed', cs['speed'])
    y('hp', cs['hp'])
    y('hp_max', cs['hp_max'])
    y('hit_dice', cs['hit_dice'])
    y('passive_perception', cs['passive_perception'])
    lines.append('')

    # Spellcasting (only if present)
    if cs['spell_ability']:
        y('spell_ability', cs['spell_ability'])
        y('spell_dc', cs['spell_dc'])
        y('spell_atk', cs['spell_atk'])
        lines.append('')

    # Abilities
    lines.append('  abilities:')
    for a in cs['abilities']:
        lines.append(f'    - {{key: {a["key"]}, name: {a["name"]}, score: {a["score"]}, mod: "{a["mod"]}\"}}')

    lines.append('')

    # Saves
    lines.append('  saves:')
    for s in cs['saves']:
        prof_str = 'true' if s['prof'] else 'false'
        lines.append(f'    - {{name: {s["name"]}, bonus: "{s["bonus"]}", prof: {prof_str}}}')

    lines.append('')

    # Skills
    lines.append('  skills:')
    for sk in cs['skills']:
        marker = sk['marker']
        lines.append(
            f'    - {{name: "{sk["name"]}", ability: {sk["ability"]}, '
            f'bonus: "{sk["bonus"]}", marker: "{marker}"}}'
        )

    lines.append('')

    # Weapons
    lines.append('  weapons:')
    if cs['weapons']:
        for w in cs['weapons']:
            n = w['name'].replace('"', '\\"')
            d = w['dmg'].replace('"', '\\"')
            r = w['range'].replace('"', '\\"')
            p = w['props'].replace('"', '\\"')
            lines.append(f'    - {{name: "{n}", atk: "{w["atk"]}", dmg: "{d}", range: "{r}", props: "{p}"}}')
    else:
        lines.append('    []')

    lines.append('')

    # Features (names and sources only)
    lines.append('  features:')
    if cs['features']:
        for f in cs['features']:
            n = f['name'].replace('"', '\\"')
            s = f['source']
            uses = f.get('uses', '')
            if uses:
                lines.append(f'    - {{name: "{n}", source: {s}, uses: "{uses}"}}')
            else:
                lines.append(f'    - {{name: "{n}", source: {s}}}')
    else:
        lines.append('    []')

    lines.append('')

    # Traits
    lines.append('  traits:')
    t = cs['traits']
    y('size', t['size'], 4)
    y('resistances', t['resistances'], 4)
    y('immunities', t['immunities'], 4)
    y('vulnerabilities', t['vulnerabilities'], 4)
    y('condition_immunities', t['condition_immunities'], 4)
    y('languages', t['languages'], 4)
    y('senses', t['senses'], 4)

    lines.append('')

    # Proficiencies
    lines.append('  proficiencies:')
    p = cs['proficiencies']
    y('armor', p['armor'], 4)
    y('weapons', p['weapons'], 4)
    y('tools', p['tools'], 4)

    lines.append('')

    # Equipment
    lines.append('  equipment:')
    if cs['equipment']:
        for item in cs['equipment']:
            item_str = item.replace('"', '\\"')
            lines.append(f'    - "{item_str}"')
    else:
        lines.append('    []')

    lines.append('')

    # Currency
    lines.append('  currency:')
    cur = cs['currency']
    for coin in ('pp', 'gp', 'ep', 'sp', 'cp'):
        lines.append(f'    {coin}: {cur.get(coin, 0)}')

    lines.append('---')
    lines.append('')

    # Markdown body: feature descriptions
    if cs['features_descriptions'] or cs['spells_by_level']:
        class_line = build_class_line(cs)

        # Group features by source
        race_feats = [f for f in cs['features'] if f['source'] == 'Race']
        class_feats = [f for f in cs['features'] if f['source'] == 'Class']
        other_feats = [f for f in cs['features'] if f['source'] not in ('Race', 'Class')]

        def write_feature_group(feat_list, heading):
            group_lines = []
            had_desc = False
            for feat in feat_list:
                desc = cs['features_descriptions'].get(feat['name'], '')
                if desc:
                    group_lines.append(f"### {feat['name']}")
                    group_lines.append('')
                    group_lines.append(desc)
                    group_lines.append('')
                    had_desc = True
            if had_desc:
                return [f'## {heading}', ''] + group_lines
            return []

        body_sections = []

        if race_feats:
            race_heading = f"Race: {cs['race']}" if cs['race'] else "Racial Features"
            section = write_feature_group(race_feats, race_heading)
            if section:
                body_sections.extend(section)

        if class_feats:
            class_heading = class_line if class_line else "Class Features"
            section = write_feature_group(class_feats, class_heading)
            if section:
                body_sections.extend(section)

        if other_feats:
            section = write_feature_group(other_feats, "Other Features")
            if section:
                body_sections.extend(section)

        # Spells
        if cs['spells_by_level']:
            body_sections.append('## Spells')
            body_sections.append('')
            for lv in sorted(cs['spells_by_level'].keys()):
                label = 'Cantrips' if lv == 0 else f'Level {lv}'
                body_sections.append(f'### {label}')
                body_sections.append('')
                for sp in sorted(cs['spells_by_level'][lv]):
                    body_sections.append(f'- {sp}')
                body_sections.append('')

        if body_sections:
            lines.extend(body_sections)

    return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: ingest-actor.py <actor.json> [output_dir]")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.exists():
        print(f"Error: {json_path} not found")
        sys.exit(1)

    with open(json_path) as f:
        actor = json.load(f)

    jekyll_root = find_jekyll_root(Path.cwd())

    if len(sys.argv) > 2:
        output_dir = Path(sys.argv[2])
    else:
        output_dir = jekyll_root / "_pages/gm/charsheets"

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Processing: {actor.get('name', '?')} ({actor.get('type', '?')})")
    cs = build_charsheet(actor)

    slug = slugify(cs['name'])
    output_file = output_dir / f"{slug}.draft.md"

    if output_file.exists():
        print(f"ERROR: {output_file} already exists. Remove it first.")
        sys.exit(1)

    content = generate_page(cs)
    output_file.write_text(content, encoding='utf-8')
    print(f"Wrote: {output_file}")
    print()

    # Report
    class_line = build_class_line(cs)
    print(f"  {cs['name']} — {class_line}, {cs['race']}")
    print(f"  Level {cs['level']} | Prof {cs['proficiency']} | AC {cs['ac']} | HP {cs['hp']}/{cs['hp_max']}")
    print(f"  Speed: {cs['speed']} | Initiative: {cs['initiative']}")
    print()
    print(f"  Weapons: {len(cs['weapons'])}")
    print(f"  Features: {len(cs['features'])}")
    print(f"  Equipment items: {len(cs['equipment'])}")
    print()
    print("Post-ingest checklist:")
    print("  [ ] Rename .draft.md to .md when satisfied")
    print("  [ ] Verify AC (especially if armor/shields involved)")
    print("  [ ] Verify speed (check for race/item bonuses)")
    print("  [ ] Verify uses/resources (check @scale formulas)")
    print("  [ ] Fill in background, alignment if missing")
    print("  [ ] Review feature descriptions for accuracy")


if __name__ == '__main__':
    main()
