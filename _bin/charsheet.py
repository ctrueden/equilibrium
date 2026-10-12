"""
charsheet.py — Shared logic for Equilibrium character sheets (layout: charsheet).

Character sheets store only the *inputs* (ability scores, proficiency lists,
bonuses); the charsheet layout computes the derived values (modifiers, saves,
skills, initiative, passive Perception, spell DC/attack, weapon attack/damage).

This module mirrors the layout's computation in Python, so that scripts can
check sheets and report the numbers they will display, and it provides an
emitter that writes the `cs:` front matter in a consistent, compact style.
"""

import json
import re
from collections import Counter

import yaml

ABILITIES = ['str', 'dex', 'con', 'int', 'wis', 'cha']

ABILITY_NAMES = {
    'str': 'Strength', 'dex': 'Dexterity', 'con': 'Constitution',
    'int': 'Intelligence', 'wis': 'Wisdom', 'cha': 'Charisma',
}

SKILLS = [
    # (key, name, ability)
    ('acrobatics', 'Acrobatics', 'dex'),
    ('animalhandling', 'Animal Handling', 'wis'),
    ('arcana', 'Arcana', 'int'),
    ('athletics', 'Athletics', 'str'),
    ('deception', 'Deception', 'cha'),
    ('history', 'History', 'int'),
    ('insight', 'Insight', 'wis'),
    ('intimidation', 'Intimidation', 'cha'),
    ('investigation', 'Investigation', 'int'),
    ('medicine', 'Medicine', 'wis'),
    ('nature', 'Nature', 'int'),
    ('perception', 'Perception', 'wis'),
    ('performance', 'Performance', 'cha'),
    ('persuasion', 'Persuasion', 'cha'),
    ('religion', 'Religion', 'int'),
    ('sleightofhand', 'Sleight of Hand', 'dex'),
    ('stealth', 'Stealth', 'dex'),
    ('survival', 'Survival', 'wis'),
]
SKILL_NAMES = {key: name for key, name, _ in SKILLS}


def skill_key(name):
    return re.sub(r'[\s_\-]', '', str(name).lower())


def ability_key(name):
    return str(name).lower()[:3]


def mod(score):
    return (int(score) - 10) // 2


def signed(n):
    return f'+{n}' if n >= 0 else str(n)


def to_int(v):
    """Lenient number parsing, like Liquid's: '+5' -> 5, None -> 0."""
    if v is None or v == '':
        return 0
    if isinstance(v, (int, float)):
        return int(v)
    m = re.match(r'\s*([+-]?\d+)', str(v))
    return int(m.group(1)) if m else 0


def proficiency(cs):
    if cs.get('proficiency') not in (None, ''):
        return to_int(cs['proficiency'])
    basis = max(1, to_int(cs.get('level') or cs.get('cr')))
    return (basis - 1) // 4 + 2


def compute(cs):
    """Compute the derived values the charsheet layout will display."""
    b = cs.get('bonuses') or {}
    scores = cs.get('abilities') or {}
    mods = {a: mod(scores.get(a, 10)) for a in ABILITIES}
    prof = proficiency(cs)
    half = prof // 2
    checks = to_int(b.get('checks'))

    prof_saves = {ability_key(s) for s in cs.get('saves') or []}
    saves = {a: mods[a] + to_int(b.get('saves')) + (prof if a in prof_saves else 0)
             for a in ABILITIES}

    prof_skills = {skill_key(s) for s in cs.get('skills') or []}
    expert = {skill_key(s) for s in cs.get('expertise') or []}
    skill_bonus = {skill_key(k): to_int(v) for k, v in (b.get('skills') or {}).items()}
    skills = {}
    for key, _, ab in SKILLS:
        v = mods[ab] + checks
        if key in expert:
            v += 2 * prof
        elif key in prof_skills:
            v += prof
        elif cs.get('jack_of_all_trades'):
            v += half
        skills[key] = v + skill_bonus.get(key, 0)

    if cs.get('initiative') not in (None, ''):
        initiative = str(cs['initiative'])
    else:
        init = mods['dex'] + checks + to_int(b.get('initiative'))
        if cs.get('jack_of_all_trades'):
            init += half
        initiative = signed(init)

    if cs.get('passive_perception') not in (None, ''):
        passive = to_int(cs['passive_perception'])
    else:
        passive = 10 + skills['perception'] + to_int(b.get('passive_perception'))

    result = {
        'prof': prof, 'mods': mods, 'saves': saves, 'skills': skills,
        'initiative': initiative, 'passive_perception': passive,
    }

    spell_mod = spell_atk_val = spell_dc = None
    if cs.get('spell_ability'):
        spell_mod = mods[ability_key(cs['spell_ability'])]
        spell_atk_val = spell_mod + prof + to_int(b.get('spell'))
        spell_dc = cs.get('spell_dc') or spell_atk_val + 8
        result['spell_atk'] = cs.get('spell_atk') or signed(spell_atk_val)
        result['spell_dc'] = spell_dc

    weapons = []
    for w in cs.get('weapons') or []:
        ab = str(w.get('ability') or '').lower()
        if ab == 'finesse':
            ab = 'dex' if scores.get('dex', 10) > scores.get('str', 10) else 'str'
        if ab == 'spell':
            w_mod, w_atk = spell_mod or 0, spell_atk_val or 0
        else:
            w_mod = mods.get(ab[:3], -5) if ab else 0
            w_atk = w_mod + (0 if w.get('prof') is False else prof)
        w_atk += to_int(w.get('magic')) + to_int(w.get('atk_bonus'))
        if w.get('atk') not in (None, ''):
            atk = str(w['atk'])
        elif w.get('save'):
            atk = f"DC {spell_dc} {str(w['save']).capitalize()}"
        elif w.get('ability'):
            atk = signed(w_atk)
        else:
            atk = ''
        if w.get('dmg') not in (None, ''):
            dmg = str(w['dmg'])
        elif w.get('dice'):
            dm = 0
            if w.get('ability') and w.get('dmg_mod') is not False:
                if ab != 'spell' or w.get('dmg_mod'):
                    dm = w_mod
            dm += to_int(w.get('magic')) + to_int(w.get('dmg_bonus'))
            dmg = str(w['dice']) + (f'+{dm}' if dm > 0 else str(dm) if dm < 0 else '')
            if w.get('type'):
                dmg += f" {w['type']}"
            if w.get('extra'):
                dmg += f" {w['extra']}"
        else:
            dmg = ''
        weapons.append({'name': w.get('name'), 'atk': atk, 'dmg': dmg})
    result['weapons'] = weapons
    return result


# ---------------------------------------------------------------------------
# Converting verbose sheets
# ---------------------------------------------------------------------------

DMG_RE = re.compile(r'^(\d+d\d+)\s*([+-]\s*\d+)?\s*(.*)$')


def compact(old):
    """Convert a verbose sheet (precomputed values, as produced by older
    versions of ingest-actor.py) into the compact schema. Differences between
    the precomputed values and what the layout would compute are expressed as
    bonuses where possible, and described in the returned report."""
    report = []
    cs = {k: old[k] for k in IDENTITY_KEYS if k in old and old[k] not in (None, '')}
    cs.pop('proficiency', None)
    abil = {a['key']: a['score'] for a in old['abilities']}
    cs['abilities'] = abil
    cs['saves'] = [s['name'][:3].lower() for s in old['saves'] if s.get('prof')]
    skills, expertise = [], []
    for sk in old['skills']:
        k = skill_key(sk['name'])
        if sk.get('marker') in ('◉', '●●'):
            expertise.append(k)
        elif sk.get('marker') == '●':
            skills.append(k)
    cs['skills'] = skills
    if expertise:
        cs['expertise'] = expertise
    old_prof = to_int(old.get('proficiency'))
    if old_prof != proficiency(cs):
        cs['proficiency'] = old_prof
        report.append(f'proficiency override {old_prof} (computed {proficiency(cs)})')
    bonuses = {}
    cs['bonuses'] = bonuses
    r = compute(cs)
    # saves
    deltas = {s['name'][:3].lower(): to_int(s['bonus']) - r['saves'][s['name'][:3].lower()] for s in old['saves']}
    common = Counter(deltas.values()).most_common(1)[0][0]
    if common:
        bonuses['saves'] = common
    odd = {k: v - common for k, v in deltas.items() if v != common}
    if odd:
        report.append(f'save discrepancies (old - computed): {odd}')
    # skills
    r = compute(cs)
    deltas = {skill_key(s['name']): to_int(s['bonus']) - r['skills'][skill_key(s['name'])] for s in old['skills']}
    common = Counter(deltas.values()).most_common(1)[0][0]
    if common:
        bonuses['checks'] = common
    odd = {k: v - common for k, v in deltas.items() if v != common}
    if odd:
        report.append(f'skill discrepancies (old - computed): {odd}')
        bonuses['skills'] = odd
    # combat
    for k in ('ac', 'speed', 'hp_max', 'hit_dice'):
        if old.get(k) not in (None, ''):
            cs[k] = old[k]
    if old.get('hp') not in (None, '') and old.get('hp') != old.get('hp_max'):
        cs['hp'] = old['hp']
    r = compute(cs)
    di = to_int(old.get('initiative')) - to_int(r['initiative'])
    if di:
        bonuses['initiative'] = di
        report.append(f'initiative bonus {di}')
    r = compute(cs)
    dp = to_int(old.get('passive_perception')) - r['passive_perception']
    if dp:
        bonuses['passive_perception'] = dp
        report.append(f'passive perception bonus {dp}')
    # spells
    if old.get('spell_ability'):
        cs['spell_ability'] = ability_key(old['spell_ability'])
        r = compute(cs)
        da = to_int(old.get('spell_atk')) - to_int(r['spell_atk'])
        if da:
            bonuses['spell'] = da
            report.append(f'spell bonus {da}')
        r = compute(cs)
        if to_int(old.get('spell_dc')) != to_int(r['spell_dc']):
            cs['spell_dc'] = old['spell_dc']
            report.append(f"spell DC override {old['spell_dc']} (computed {r['spell_dc']})")
        if old.get('spells'):
            cs['spells'] = old['spells']
    # weapons
    r = compute(cs)
    weapons = []
    for w in old.get('weapons') or []:
        nw = convert_weapon(w, cs, r, report)
        weapons.append(nw)
    if weapons:
        cs['weapons'] = weapons
    for k in ('features', 'traits', 'proficiencies', 'equipment', 'currency'):
        if old.get(k):
            cs[k] = old[k]
    if not bonuses:
        del cs['bonuses']
    return cs, report


def convert_weapon(w, cs, r, report):
    """Try to express a weapon via ability + dice; fall back to literals."""
    atk_s = str(w.get('atk') or '').strip()
    dmg_s = str(w.get('dmg') or '').strip()
    base = {k: v for k, v in w.items() if k in ('range', 'props') and v not in (None, '')}
    literal = dict({'name': w['name']}, **{k: w[k] for k in ('atk', 'dmg') if w.get(k) not in (None, '')}, **base)
    md = re.fullmatch(r'DC (\d+) (\w+)', atk_s)
    if md and cs.get('spell_ability') and int(md.group(1)) == to_int(r['spell_dc']):
        return dict({'name': w['name'], 'save': md.group(2).lower()}, **({'dmg': dmg_s} if dmg_s else {}), **base)
    if not re.fullmatch(r'[+-]\d+', atk_s):
        return literal
    atk = int(atk_s)
    m = DMG_RE.match(dmg_s)
    prof = r['prof']
    sa = ability_key(cs['spell_ability']) if cs.get('spell_ability') else None
    others = [a for a in ('con', 'int', 'wis', 'cha') if a != sa]
    # (ability, proficient) pairs, most plausible first.
    candidates = [('str', True), ('dex', True), ('str', False), ('dex', False)]
    if sa:
        candidates += [('spell', True), (sa, True)]
    candidates += [(a, True) for a in others] + [(a, False) for a in others]
    for magic in range(0, 4):
        for ab, proficient in candidates:
            if ab == 'spell':
                a_mod = r['mods'][sa]
                a_atk = to_int(r['spell_atk'])
            else:
                a_mod = r['mods'][ab]
                a_atk = a_mod + (prof if proficient else 0)
            if a_atk + magic != atk:
                continue
            nw = {'name': w['name'], 'ability': ab}
            if not proficient:
                nw['prof'] = False
            if magic:
                nw['magic'] = magic
            if not m:
                if dmg_s:
                    nw['dmg'] = dmg_s
            else:
                dice, dm, rest = m.group(1), to_int((m.group(2) or '0').replace(' ', '')), m.group(3).strip()
                nw['dice'] = dice
                used = (a_mod if ab != 'spell' else 0) + magic
                if ab == 'spell' and dm == a_mod + magic and a_mod:
                    nw['dmg_mod'] = True
                    used = dm
                if dm - used:
                    nw['dmg_bonus'] = dm - used
                if rest:
                    parts = rest.split(None, 1)
                    nw['type'] = parts[0]
                    if len(parts) > 1:
                        nw['extra'] = parts[1]
            nw.update(base)
            return nw
    report.append(f"weapon {w['name']!r}: atk {atk_s} matches no ability; kept literal")
    return literal


# ---------------------------------------------------------------------------
# Emitting front matter
# ---------------------------------------------------------------------------

def scalar(v, flow=False):
    """Render a YAML scalar on one line, quoting only when needed.
    In flow context ({...} or [...]), commas and brackets also need quoting."""
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if flow and re.search(r'[,\[\]{}]', s):
        return json.dumps(s, ensure_ascii=False)
    out = yaml.safe_dump(s, default_flow_style=True, width=10**9, allow_unicode=True).strip()
    if out.endswith('...'):
        out = out[:-3].strip()
    return out


def flow_map(d):
    return '{' + ', '.join(f'{k}: {scalar(v, True)}' for k, v in d.items()) + '}'


def flow_list(items):
    return '[' + ', '.join(scalar(i, True) for i in items) + ']'


IDENTITY_KEYS = ['name', 'race', 'class', 'subclass', 'level', 'cr',
                 'proficiency', 'background', 'alignment']
PROF_KEYS = ['saves', 'skills', 'expertise', 'jack_of_all_trades']
COMBAT_KEYS = ['ac', 'ac_note', 'initiative', 'speed', 'hp_max', 'hp',
               'hit_dice', 'passive_perception']
SPELL_KEYS = ['spell_ability', 'spell_dc', 'spell_atk']
WEAPON_KEYS = ['name', 'ability', 'atk', 'save', 'dice', 'type', 'magic',
               'atk_bonus', 'dmg_bonus', 'dmg_mod', 'prof', 'extra', 'dmg',
               'range', 'props']


def emit_cs(cs):
    """Emit a `cs:` mapping as YAML lines, in canonical order and style."""
    lines = ['cs:']
    seen = set()

    def simple(keys):
        for k in keys:
            if k in cs and cs[k] not in (None, ''):
                lines.append(f'  {k}: {scalar(cs[k])}')
            seen.add(k)

    def blank():
        if lines[-1] != '':
            lines.append('')

    simple(IDENTITY_KEYS)
    blank()

    if cs.get('abilities'):
        lines.append('  abilities: ' + flow_map({a: cs['abilities'][a] for a in ABILITIES
                                                  if a in cs['abilities']}))
    seen.add('abilities')
    for k in PROF_KEYS:
        v = cs.get(k)
        if isinstance(v, list) and v:
            lines.append(f'  {k}: {flow_list(v)}')
        elif v not in (None, '', [], False):
            lines.append(f'  {k}: {scalar(v)}')
        seen.add(k)
    if cs.get('bonuses'):
        lines.append('  bonuses:')
        for k, v in cs['bonuses'].items():
            if isinstance(v, dict):
                lines.append(f'    {k}: {flow_map(v)}')
            else:
                lines.append(f'    {k}: {scalar(v)}')
    seen.add('bonuses')
    blank()

    simple(COMBAT_KEYS)
    blank()

    if cs.get('spell_ability'):
        simple(SPELL_KEYS)
        if cs.get('spells'):
            lines.append('  spells:')
            for s in cs['spells']:
                lines.append(f'    - {flow_map(s)}')
        blank()
    seen.update(SPELL_KEYS + ['spells'])

    if cs.get('weapons'):
        lines.append('  weapons:')
        for w in cs['weapons']:
            ordered = {k: w[k] for k in WEAPON_KEYS if k in w and w[k] not in (None, '')}
            ordered.update({k: v for k, v in w.items() if k not in ordered and v not in (None, '')})
            lines.append(f'    - {flow_map(ordered)}')
        blank()
    seen.add('weapons')

    if cs.get('features'):
        lines.append('  features:')
        for f in cs['features']:
            lines.append(f'    - {flow_map({k: v for k, v in f.items() if v not in (None, "")})}')
        blank()
    seen.add('features')

    for block in ('traits', 'proficiencies'):
        d = {k: v for k, v in (cs.get(block) or {}).items() if v not in (None, '')}
        if d:
            lines.append(f'  {block}:')
            for k, v in d.items():
                lines.append(f'    {k}: {scalar(v)}')
            blank()
        seen.add(block)

    if cs.get('equipment'):
        lines.append('  equipment:')
        for e in cs['equipment']:
            lines.append(f'    - {scalar(e)}')
        blank()
    seen.add('equipment')

    cur = {k: v for k, v in (cs.get('currency') or {}).items() if v}
    if cur:
        lines.append(f'  currency: {flow_map(cur)}')
    seen.add('currency')

    # Anything else, verbatim.
    rest = {k: v for k, v in cs.items() if k not in seen}
    if rest:
        blank()
        dumped = yaml.safe_dump(rest, sort_keys=False, allow_unicode=True, width=1000)
        lines.extend('  ' + l for l in dumped.rstrip().split('\n'))

    while lines[-1] == '':
        lines.pop()
    return '\n'.join(lines)


def emit_page(title, cs, body, extra_front=None):
    front = ['---', 'layout: charsheet', f'title: {scalar(title)}']
    for k, v in (extra_front or {}).items():
        front.append(f'{k}: {scalar(v)}')
    front.append('')
    front.append(emit_cs(cs))
    front.append('---')
    return '\n'.join(front) + '\n\n' + body.strip() + '\n'
