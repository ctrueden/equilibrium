---
title: Titans
image: https://i.pinimg.com/originals/bb/93/37/bb9337e3c7adab6142576ea18352f559.png
image-source: https://www.pinterest.com/pin/985231160206081/
---

The titans are a legendary group of twelve powerful entities that some say gave rise to [the gods](eternals) themselves. How much of that story is really true is a source of frequent debate amongst religious scholars.

### Table of titans

{% assign link-sites = "Wikipedia" | split: "|" -%}

<style>
th.rotate {
  white-space: nowrap;
}

th.rotate > div {
  transform: rotate(-90deg);
  width: 1em;
}
</style>
<table style="margin-top: 4em">
<thead>
<tr>
  <th>Name</th>
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
    {%- assign races = p.statbox.race | split: "WE-ARE-THE-KNIGHTS-WHO-SAY-NI" -%}
  {%- endif -%}
  {%- unless races contains 'titan' -%} {%- continue -%} {%- endunless -%}
  <tr>
    <td><a href="{{site.baseurl}}{{p.url}}">{{p.title}}</a></td>
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

### List of titans

{% include charlist race="titan" %}
