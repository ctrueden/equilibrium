---





title: Alye'adu
image: https://i.pinimg.com/originals/1c/55/00/1c5500e20b3fdda6a0bf81f68ff68547.jpg
image-source: https://www.pinterest.com/pin/47358233562491935/
descriptions:
  - session: "13e02"
    content: |
      A hidden village protected by an invisible veil, which Callie and Ozborn tore open by speaking its name and stabbing it. Sentries quickly found the agents, and their leader, resembling a powerful priestess of Sehanine, came out to talk.
  - session: "13e03"
    content: |
      Invaded by Talos and Andalla, who sought the changelings' shapeshifting power. The agents learned that Mallory had lain comatose in the village for the past four months.
  - session: "13e04"
    content: |
      Talos yielded and promised not to harm the village. Its changelings, who had been unable to act during the battle, learned of Isis's death; Vondal wove Flux into a wild magic door to replace the one the agents had torn.
  - session: "14e00"
    content: |
      After the Malosi fight, the agents healed Mallory there, and had a drink at the pub.
  - session: "17e01"
    content: |
      The agents teleported in with the village's memorized sigil sequence, and later reentered by speaking its name without breaking the door. They sought Grohnea's counterpart Anorje, promised help to a goblin princess, and found most villagers bearing white crane tattoos.
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
