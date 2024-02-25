---
title: Gear
---

## Tattoos

| Color  | Power          | Activation                    | Notes                                  |
|--------|----------------|-------------------------------|----------------------------------------|
| Red    | [hammer]       | as part of an attack (1/turn) | 4 touches at 3d8 each                  |
| Orange | [hustle]       | free action                   | extra bonus action OR extra movement   |
| Yellow | [time hop]     | bonus action                  | 5 rounds forward, Wisdom DC 15 negates |
| Green  | [biofeedback]  | bonus action                  | DR 4/- for 7 min.                      |
| Blue   | [defy gravity] | bonus action                  | 1 hour, self only                      |
| Violet | [vigor]        | bonus action                  | 20 temporary HP for 7 min.             |
| Black  | [truevenom]    | bonus action                  | Constitution save DC 15                |

## Magic Items

<table>
<thead>
<tr>
  <th>Item</th>
  <th>Source</th>
  <th>Owner</th>
  <th>Rarity</th>
  <th>Value</th>
  <th>Page</th>
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
  <td>{{m.page}}</td>
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
