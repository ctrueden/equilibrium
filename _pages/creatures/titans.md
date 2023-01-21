---
title: Titans
image: https://i.pinimg.com/originals/bb/93/37/bb9337e3c7adab6142576ea18352f559.png
image-source: https://www.pinterest.com/pin/985231160206081/
---

The titans are a legendary group of twelve powerful entities that some say gave rise to [the gods](eternals) themselves. How much of that story is really true is a source of frequent debate amongst religious scholars.

{% assign titans = "oceanus|koios|crius|hyperion|iapetus|theia|rhea|themis|mnemosyne|phoebe|tethys|cronus" | split: "|" -%}
{%- for titan in titans -%}
{% assign url = "/dossiers/" | append: titan %}
{% assign t = site.pages | where: "url", url -%}
<div style="display: inline-block; max-width: 192px; padding-right: 1em; text-align: center; vertical-align: top"><p>
  <a href="{{site.baseurl}}{{t[0].url}}"><img src="{{t[0].image}}" title="{{t[0].title}}" alt="{{t[0].title}}" style="max-height: 192px" /><br />{{t[0].nav-title}}</a>
{%- for link in t[0].links -%}
  {%- assign l = link | split: "|" -%}
  {%- unless l[0] == "Wikipedia" -%} {%- continue -%} {%- endunless -%}
  <a href="{{l[1]}}">*</a>
  {%- break -%}
{%- endfor %}
</p></div>
{% comment -%} {%- endcomment -%}
{%- endfor %}

### List of titans

{% include charlist race="titan (sky)" %}
