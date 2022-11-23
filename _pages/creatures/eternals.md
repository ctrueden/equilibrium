---
title: Eternals
image: https://static.wikia.nocookie.net/forgottenrealms/images/f/f2/Mulhorandi_pantheon_I.jpg
image-source: https://forgottenrealms.fandom.com/wiki/Deity
---

The eternals, commonly worshipped as deities, are the beings that built the modern world. Many continue to participate in its growth and development. Some are newcomers seeking to claim a place amongst the divinity.

{% assign link-sites = "4E|D&D wiki|Greyhawk|Forgotten Realms|Evenfall|Critical Role|Wikipedia" | split: "|" -%}

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
{%- for p in site.pages -%}
  {%- if p.statbox.race.first -%}
    {%- comment -%} Value is a list; use it as is. {%- endcomment -%}
    {%- assign races = p.statbox.race -%}
  {%- else -%}
    {%- comment -%} Value is a scalar; convert to a single-element list. {%- endcomment -%}
    {%- assign races = p.statbox.race | split: "WE-DEMAND-ANOTHER-SHRUBBERY" -%}
  {%- endif -%}
  {%- unless races contains 'eternal' -%} {%- continue -%} {%- endunless -%}
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

<center><figure>
<a href="../assets/images/eternals.svg"><img src="../assets/images/eternals.svg" style="max-width: 100%; max-height: 500px"></a>
<figcaption style="text-align: center">Alliances and rivalries</figcaption>
</figure></center>

### List of eternals

{% include charlist race="eternal" %}
