---
title: Eternals
image: https://static.wikia.nocookie.net/forgottenrealms/images/f/f2/Mulhorandi_pantheon_I.jpg
image-source: https://forgottenrealms.fandom.com/wiki/Deity
---

The eternals, commonly worshipped as deities[*](https://dungeonsdragons.fandom.com/wiki/Deity), are the beings that built the modern world. Many continue to participate in its growth and development. Some are newcomers seeking to claim a place amongst the divinity.

## Table of eternals

{% assign eternals = "" | split: "," -%}
{%- for p in site.pages -%}
  {%- if p.statbox.race.first -%}
    {%- comment -%} Value is a list; use it as is. {%- endcomment -%}
    {%- assign races = p.statbox.race -%}
  {%- else -%}
    {%- comment -%} Value is a scalar; convert to a single-element list. {%- endcomment -%}
    {%- assign races = p.statbox.race | split: "WE-DEMAND-ANOTHER-SHRUBBERY" -%}
  {%- endif -%}
  {%- unless races contains 'eternal' -%} {%- continue -%} {%- endunless -%}
  {%- assign eternals = eternals | push: p -%}
{%- endfor -%}

{%- assign link-sites = "4E|D&D wiki|Greyhawk|Forgotten Realms|FRC|FRC 2|Eberron|Evenfall|Critical Role|Thieves Guild|Thieves Guild 2|Thieves Guild 3|Thieves Guild 4|Thieves Guild 5|Wikipedia|5E Exandria|5E Exandria 2|5E Racial|5E Dawn War|5E Greyhawk|5E Faerun|5E Greek|5E Greek 2|5E Greek 3" | split: "|" -%}

<style>
th.rotate {
  white-space: nowrap;
}

th.rotate > div {
  transform: rotate(-90deg);
  width: 1em;
}
</style>
<table style="margin-top: 9em">
<thead>
<tr>
  <th>Name</th>
  <th>Domains</th>
  <th>Month</th>
{% for link-site in link-sites -%}
  <th class="rotate"><div>{{link-site}}</div></th>
{%- endfor %}
</tr>
</thead>
<tbody>
{%- for p in eternals -%}
  <tr>
    <td><a href="{{site.baseurl}}{{p.url}}">{{p.nav-title}}</a></td>
    <td>{{p.statbox.domains | join: ", "}}</td>
    <td>{{p.statbox.month | default: "-"}}</td>
    {% for link-site in link-sites -%}
      {%- assign found = false -%}
      {%- for link in p.links -%}
        {%- assign l = link | split: "|" -%}
        {%- unless l[0] == link-site -%} {%- continue -%} {%- endunless -%}
        {%- assign found = true -%}
        <td style="text-align: center"><a href="{{l[1]}}">🔵</a></td>
        {%- break -%}
      {%- endfor -%}
      {%- unless found -%} <td style="text-align: center">-</td> {%- endunless -%}
    {%- endfor %}
  </tr>
{%- endfor -%}
</tbody>
</table>

### Domains

Each eternal sits at the intersection of two of the eight domains:

|        Domain | Knowledge         | Tempest       | Trickery          | Life       | Light      | War       | Nature     | Death     |
|--------------:|:-----------------:|:-------------:|:-----------------:|:----------:|:----------:|:---------:|:----------:|:---------:|
| **Knowledge** | -                 | ?             | [Ioun], [Sardior] | ?          | [Moradin]  | [Erathis] | ?          | [Vecna]   |
|   **Tempest** | ?                 | -             | [Brandobaris]     | ?          | ?          | [Kord]    | [Melora]   | ?         |
|  **Trickery** | [Ioun], [Sardior] | [Brandobaris] | -                 | [Avandra]  | ?          | [Lolth]   | [Sehanine] | ?         |
|      **Life** | ?                 | ?             | [Avandra]         | -          | [Pelor]    | [Bahamut] | [Yondalla] | [Nerull]  |
|     **Light** | [Moradin]         | ?             | ?                 | [Pelor]    | -          | [Sune]    | [Corellon] | ?         |
|       **War** | [Erathis]         | [Kord]        | [Lolth]           | [Bahamut]  | [Sune]     | -         | [Gruumsh]  | [Tiamat]  |
|    **Nature** | ?                 | [Melora]      | [Sehanine]        | [Yondalla] | [Corellon] | [Gruumsh] | -          | ?         |
|     **Death** | [Vecna]           | ?             | ?                 | [Nerull]   | ?          | [Tiamat]  | ?          | -         |

Religious scholars postulate that deities gravitate toward their distinct niches, because multiple eternals occupying the same combination of domains could produce deific friction, or even an erosion of the distinctions between them in the minds of their worshippers.

### Alliances and rivalries

<center><figure>
<a href="../assets/images/eternals.svg"><img src="../assets/images/eternals.svg" style="max-width: 100%; max-height: 500px"></a>
</figure></center>

<table style="margin-top: 9em">
<thead>
<tr>
  <th>Being</th>
{% for p in eternals -%}
  <th class="rotate"><div>{{p.nav-title}}</div></th>
{%- endfor %}
</tr>
</thead>
<tbody>
{%- for p in eternals -%}
  <tr>
    <td><a href="{{site.baseurl}}{{p.url}}">{{p.nav-title}}</a></td>
    {%- for q in eternals -%}
      <td style="text-align: center">
        {%- if p == q -%} ➖
        {%- elsif p.statbox.allies contains q.nav-title -%} 👍
          {%- unless q.statbox.allies contains p.nav-title -%} 🪲 {%- endunless -%}
        {%- elsif p.statbox.enemies contains q.nav-title -%} 💢
          {%- unless q.statbox.enemies contains p.nav-title -%} 🪲 {%- endunless -%}
        {%- else -%} -
        {%- endif -%}
      </td>
    {%- endfor -%}
  </tr>
{%- endfor -%}
</tbody>
</table>

### List of eternals

{% include charlist race="eternal" %}

[Avandra]: ../dossiers/avandra
[Bahamut]: ../dossiers/bahamut
[Brandobaris]: ../dossiers/brandobaris
[Corellon]: ../dossiers/corellon
[Erathis]: ../dossiers/erathis
[Gruumsh]: ../dossiers/gruumsh
[Ioun]: ../dossiers/ioun
[Kord]: ../dossiers/kord
[Lolth]: ../dossiers/lolth
[Melora]: ../dossiers/melora
[Moradin]: ../dossiers/moradin
[Nerull]: ../dossiers/nerull
[Pelor]: ../dossiers/pelor
[Raven Queen]: ../dossiers/nerull
[Sardior]: ../dossiers/sardior
[Sehanine]: ../dossiers/sehanine
[Sune]: ../dossiers/sune
[Tiamat]: ../dossiers/tiamat
[Vecna]: ../dossiers/vecna
[Yondalla]: ../dossiers/yondalla
