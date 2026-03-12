---





title: Alye'adu
image: https://i.pinimg.com/originals/1c/55/00/1c5500e20b3fdda6a0bf81f68ff68547.jpg
image-source: https://www.pinterest.com/pin/47358233562491935/
descriptions:
  - session: "13e02"
    content: |
      The SPI breached the protective veil surrounding the village and discovered it to be home to changelings and their anchors, protected by powerful priestesses.
  - session: "13e03"
    content: |
      Attacked by the centaur warlord Talos and orc shaman Andalla seeking to claim the village's shapeshifting magic.
  - session: "13e04"
    content: |
      Protected by the SPI who defeated the attackers; afterward, the party wove wild flux magic into a new entrance, transforming it into a wild magic door.
  - session: "14e00"
    content: |
      The location of the Malosi fight where the agents rescued Mallory and Cassandra.
  - session: "17e01"
    content: |
      Served as the changelings' hidden sanctuary, where the party made alliances with key figures including Anorje and discovered troubling signs that the changelings were unified by mysterious tattoos tied to a dangerous ideology.
---

The secret village of the [changelings](../creatures/changelings) and their anchors.

## Villagers

<div id="gallery">
{% assign candidates = site.pages | where_exp: "p", "p.statbox.locale contains 'alyeadu'" | sort %}
{%- for p in candidates -%}
<div style="display: inline-block">
<a href="{{site.baseurl}}{{p.url}}"><img src="{% include thumb-src src=p.image %}">
<br>{{p.nav-title | default: p.title}}</a>
</div>
{% endfor %}
</div>
