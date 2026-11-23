---
title: Locales
---

<div id="filters">
  {% include filter-case %}
  <span class="item">
    <label for="type">Type</label>
    <select id="type" name="type">
      <option value="all">All</option>
      <option value="nation">Nation</option>
      <option value="region">Region</option>
      <option value="island">Island</option>
      <option value="city">City/town</option>
      <option value="site">Site</option>
      <option value="plane">Plane</option>
      <option value="other">Other</option>
    </select>
  </span>
  <span class="item">
    <label for="nation">Nation</label>
    <select id="nation" name="nation">
      <option value="all">All</option>
      <option value="zephyr">Zephyr Federation</option>
      <option value="rup">Radiant Union of Pelor</option>
      <option value="mountain">Great Mountain</option>
      <option value="selva">Selva</option>
      <option value="elyria">Elyria</option>
      <option value="arallu">Arallu</option>
      <option value="cognitutus">Cognitutus</option>
      <option value="trell">Trell</option>
      <option value="other">Other/unknown</option>
    </select>
  </span>
</div>

{% include gallery %}

{% include gallery-filters %}
