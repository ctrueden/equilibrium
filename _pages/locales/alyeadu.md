---
title: Alye'adu
image: https://i.pinimg.com/originals/1c/55/00/1c5500e20b3fdda6a0bf81f68ff68547.jpg
image-source: https://www.pinterest.com/pin/47358233562491935/
---

The secret village of the [changelings](../creatures/changelings) and their anchors.

## Villagers

<div id="gallery">
{% assign candidates = site.pages | where_exp: "p", "p.statbox.locale contains 'alyeadu'" | sort %}
{%- for p in candidates -%}
<div style="display: inline-block" markdown=1>
[![]({{p.image}})]({{site.baseurl}}{{p.url}})
<br>{{p.title}}
</div>
{% endfor %}
</div>
