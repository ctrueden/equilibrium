---
title: Gear
js: [sorttable]
---

## Tattoos

### Hammer

This tattoo in the shape of ... has a faint red glow while energized.

One per turn, as part of an unarmed strike, natural attack, or melee touch attack (a melee attack with proficiency that deals no damage), you charge your limb with the force of a sledgehammer. If the attack hits, it deals an additional 3d8 points of damage. This damage is not increased or decreased by your Strength modifier. If the attack misses, the charge is wasted, expelled into the open air.

Each activation depletes the tattoo's energy by 25%; the tattoo's energy recharges at a rate of 25% every 15 minutes.

*GM's note: adapted from [hammer].*

### Hustle

This tattoo in the shape of ... has a faint orange glow while energized.

*GM's note: adapted from [hustle].*

Once activated, the tattoo's energy is expended for one hour.

### Time Hop

This tattoo in the shape of ... has a faint yellow glow while energized.

*GM's note: adapted from [time hop].*

Once activated, the tattoo's energy is expended for one hour.

### Biofeedback

This tattoo in the shape of ... has a faint green glow while energized.

*GM's note: adapted from [biofeedback].*

Once activated, the tattoo's energy is expended for one hour.

### Defy Gravity

This tattoo in the shape of ... has a faint blue glow while energized.

*GM's note: adapted from [defy gravity].*

Once activated, the tattoo's energy is expended for one hour.

### Vigor

This tattoo in the shape of ... has a faint violet glow while energized.

As a bonus action, you can activate this tattoo to draw from its reservoir of life energy, gaining 20 temporary hit points for 7 minutes.

Once activated, the tattoo's energy is expended for one hour.

*GM's note: adapted from [vigor].*

### Truevenom

This tattoo of a grinning skull glows darkly while energized.

As a bonus action, you can activate this tattoo to produce a horrible poison that coats a melee weapon you are currently wielding. On your next successful melee attack with the weapon, the poison deals 1d3 points of Constitution damage per round for 6 rounds. Poisoned creatures can make a Constitution save (DC 15) each round to negate the damage and end the affliction. A creature with Constitution damage decreases their current and maximum hit point total according to their reduced score. A creature with a Constitution score of 0 immediately dies. If the poison is not delivered within 5 minutes, it evaporates harmlessly from the weapon.

After four uses, the tattoo's energy is expended for one hour.

*GM's note: adapted from [truevenom].*


| Color  | Power          | Activation                    | Notes                                  |
|--------|----------------|-------------------------------|----------------------------------------|
| Red    | [hammer]       | as part of an attack (1/turn) | 4 touches at 3d8 each                  |
| Orange | [hustle]       | free action                   | extra bonus action OR extra movement   |
| Yellow | [time hop]     | bonus action                  | 5 rounds forward, Wisdom DC 15 negates |
| Green  | [biofeedback]  | bonus action                  | DR 4/- for 7 min.                      |
| Blue   | [defy gravity] | bonus action                  | 1 hour, self only                      |
| Violet | [vigor]        | bonus action                  | 20 temporary HP for 7 min.             |
| Black  | [truevenom]    | bonus action                  | Constitution save DC 15                |

## Magical Items

### Arkenstab

TODO

### Arrow of Tidal Force

When this arrow strikes a target, a 10-foot tall, 5-foot wide wall of water is unleashed, rushing forward 120 feet through and beyond the target. Any creature caught in the wave, either initially or when later entering the stream, must succeed on a DC 15 Dexterity saving throw or take 4d8 bludgeoning damage, be pushed 15 feet, and be knocked prone. Creatures who succeed take half the damage, and are not pushed or knocked prone. The stream of water extinguishes any exposed flames in its path, and persists for one round.

*GM's note: adapted from [this homebrew item](https://www.reddit.com/r/DnD/comments/1194wgy/oc_tidal_wave_arrow/).*

### Celestial Hand

TODO

### Hornblade

TODO

### Magic Emerald of Spell Focus

TODO

### Shirt of Terran Power

This breathable, short-sleeved shirt is decorated with a pattern of mossy stones and imbued with the primal strength of the earth. Though it is considered regular clothing rather than armor, its supple resilience grants the wearer a base AC of 12.

### Sword of Retribution

TODO

### Underwater Candle

TODO

### Wand of Wonder

TODO

*See also [Wand of Wonder](https://5e.tools/items.html#wand%20of%20wonder_dmg)*

### Whip of Rescue

TODO

## Index

<table class="sortable">
<thead>
<tr>
  <th>Item</th>
  <th>Source</th>
  <th>Owner</th>
  <th>Rarity</th>
  <th>Value</th>
</tr>
</thead>
<tbody>
{%- for p in site.pages -%}
{%- unless p.magic-items -%} {%- continue -%} {%- endunless -%}
{%- for m in p.magic-items %}
<tr>
  <td>{% if m.link %}<a href="{{m.link}}">{{m.name}}</a>{% else %}{{m.name}}{% endif %}</td>
  <td>{{m.source}}</td>
  <td><a href="{{site.baseurl}}{{p.url}}">{{p.title}}</a></td>
  <td>{{m.rarity}}</td>
  <td>{{m.value}}</td>
</tr>
{% endfor -%}
{%- endfor -%}
</tbody>
</table>

------------------------

[hammer]: https://www.d20pfsrd.com/alternative-rule-systems/psionics-unleashed/psionic-powers/h/hammer
[hustle]: https://www.d20pfsrd.com/alternative-rule-systems/psionics-unleashed/psionic-powers/h/hustle
[biofeedback]: https://www.d20pfsrd.com/alternative-rule-systems/psionics-unleashed/psionic-powers/b/biofeedback/
[defy gravity]: https://www.d20pfsrd.com/alternative-rule-systems/psionics-unleashed/psionic-powers/d/defy-gravity
[time hop]: https://www.d20pfsrd.com/alternative-rule-systems/psionics-unleashed/psionic-powers/t/time-hop/
[vigor]: https://www.d20pfsrd.com/alternative-rule-systems/psionics-unleashed/psionic-powers/v/vigor/
[truevenom]: https://www.d20pfsrd.com/alternative-rule-systems/psionics-unleashed/psionic-powers/t/truevenom/
