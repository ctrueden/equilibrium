---
title: Titans
image: https://i.pinimg.com/originals/bb/93/37/bb9337e3c7adab6142576ea18352f559.png
image-source: https://www.pinterest.com/pin/985231160206081/
---

The titans are a legendary group of powerful entities that some say gave rise to [the gods](eternals) themselves. The ones most known to mortalkind today are the Titans of the Sky, although their lineage and history is not well understood. Legend has it that the titans *were* deities, but largely passed down their power during the [Titanomachy](../events/titanomachy) and [its aftermath](../events/age-02). They remain immortal beings, but some became aspects of [Aecus](../locales/aecus) itself, and the rest walk the earth in giant form without divine essence. How much of that story is really true is a source of frequent speculation, rumor and debate amongst religious scholars and storytellers.

Those from the [Arallu](../locales/arallu) region are likely to know a few additional details about the Titans:

* There are nine living Titans of the Sky across the [Glacier](../locales/glacier). Some are allies and some are rivals, but all are unified against [the undead](../creatures/undead).

* Titans are immortal in two ways: 1) They do not die of old age; 2) They can be slain, but typically their form is reborn afterwards. To truly and permanently "kill" a Titan would require some epic effort and/or magic.

* Even though the Titans are extremely powerful, their power is waning&mdash;and there are other things in the world that can match them. The reason is that they passed on the bulk of their divinity to successors, with only lingering remnants empowering them anymore.

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
