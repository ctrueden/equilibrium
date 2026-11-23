---
title: Dossiers
---

<div id="filters">
  {% include filter-case %}
  <span class="item">
    <label for="race">Race</label>
    <select id="race" name="race">
      <option value="all">All</option>
      <option value="changeling">Changeling</option>
      <option value="devil">Devil</option>
      <option value="dragon">Dragon</option>
      <option value="dragonborn">Dragonborn</option>
      <option value="dwarf">Dwarf</option>
      <option value="elf">Elf</option>
      <option value="eternal">Eternal</option>
      <option value="fey">Fey</option>
      <option value="giant">Giant</option>
      <option value="githzerai">Githzerai</option>
      <option value="gnoll">Gnoll</option>
      <option value="gnome">Gnome</option>
      <option value="halfling">Halfling</option>
      <option value="human">Human</option>
      <option value="lizardfolk">Lizardfolk</option>
      <option value="merfolk">Merfolk</option>
      <option value="orc">Orc</option>
      <option value="spirit">Spirit</option>
      <option value="tiefling">Tiefling</option>
      <option value="titan">Titan</option>
      <option value="undead">Undead</option>
      <option value="undead-vampire">Vampire</option>
      <option value="other">Other</option>
    </select>
  </span>
  <span class="item">
    <label for="gender">Gender</label>
    <select id="gender" name="gender">
      <option value="all">All</option>
      <option value="female">Female</option>
      <option value="male">Male</option>
      <option value="other">Non-binary</option>
    </select>
  </span>
</div>

{% include gallery %}

{% include gallery-filters %}
