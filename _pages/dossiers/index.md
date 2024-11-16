---
title: Dossiers
---

<style>
#filters label {
  margin-left: 1em;
}
#filters select {
  margin-bottom: 1em;
}
#filters .item {
  white-space: nowrap;
}
</style>
<div id="filters">
  <span class="item">
    <label for="case">Case</label>
    <select id="case" name="case" onchange="refreshVisibleItems()">
      <option value="all">All</option>
      <option value="01">[01] Petrification and Putrifaction | RUP: Haven</option>
      <option value="02">[02] Exchange and Extortion | RUP: Haven</option>
      <option value="03">[03] Punctuality and Perpetuity | Mountain</option>
      <option value="04">[04] Ingestion and Incoherency | Trell: Euphoria</option>
      <option value="05">[05] Tumbling and Transcendence | Zephyr: Porta</option>
      <option value="06">[06] Mutilation and Metamorphosis | Selva</option>
      <option value="07">[07] Hazards and Harbingers | Arallu</option>
      <option value="08">[08] Revelry and Revenge | RUP: Sanctum</option>
      <option value="09">[09] Amalgamation and Anathema | Flux</option>
      <option value="10">[10] Capers and Calamity | RUP: Oasis</option>
      <option value="11">[11] Hardships and Homecomings | Cognitutus</option>
      <option value="12">[12] Burglary and Blight | Elyria: Estanesse</option>
      <option value="13">[13] Facts and Facsimiles | Selva/Veldt: Alye'adu</option>
      <option value="14">[14] Animus and Annihilation | Arallu: Evershroud Manor</option>
      <option value="15">[15] Halflings and Hemophilia | Arallu: Sepulchralis</option>
      <option value="16">[16] Tunnels and Turpitude | The Underworld?</option>
    </select>
  </span>
  <span class="item">
    <label for="race">Race</label>
    <select id="race" name="race" onchange="refreshVisibleItems()">
      <option value="all">All</option>
      <option value="changeling">Changeling</option>
      <option value="devil">Devil</option>
      <option value="dragon">Dragon</option>
      <option value="dragonborn">Dragonborn</option>
      <option value="dwarf">Dwarf</option>
      <option value="elf">Elf</option>
      <option value="eternal">Eternal</option>
      <option value="fey">Fey</option>
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
    <select id="gender" name="gender" onchange="refreshVisibleItems()">
      <option value="all">All</option>
      <option value="female">Female</option>
      <option value="male">Male</option>
      <option value="non-binary">Non-binary</option>
    </select>
  </span>
</div>

{% include gallery %}

<script>
function hasClass(item, cls) {
  for (var i=0; i<item.classList.length; i++) {
    if (cls == item.classList[i] || item.classList[i].startsWith(`${cls}-`)) return true;
  }
  return false;
}

function hasOtherRace(item) {
  // Build the set of races this item has.
  var races = new Set();
  for (var i=0; i<item.classList.length; i++) {
    var race = item.classList[i];
    if (!race.startsWith("race-")) continue;
    race = race.substring(5);
    var dash = race.indexOf("-");
    if (dash >= 0) race = race.substring(0, dash);
    races.add(race);
  }

  // Remove selectable races from the set.
  var races_selector = document.getElementById('race');
  for (var i=0; i<races_selector.children.length; i++) {
    races.delete(races_selector.children[i].value);
  }

  // If there are any races left in the set, this item has an "other" race.
  return races.size > 0;
}

function refreshVisibleItems() {
  var caseNo = document.getElementById('case').value;
  var race = document.getElementById('race').value;
  var gender = document.getElementById('gender').value;

  document.getElementById('gallery').querySelectorAll('div').forEach(function(item) {
    var enabled = true;

    // filter by case
    if (caseNo != 'all' && !hasClass(item, `case-${caseNo}`)) enabled = false;

    // filter by race
    if (race != 'all' && race != 'other' && !hasClass(item, `race-${race}`)) enabled = false;
    if (race == 'other' && !hasOtherRace(item)) enabled = false;

    // filter by gender
    var isMale = hasClass(item, 'gender-male');
    var isFemale = hasClass(item, 'gender-female');
    if (gender == 'male' && !isMale) enabled = false;
    if (gender == 'female' && !isFemale) enabled = false;
    if (gender == 'non-binary' && (isMale || isFemale)) enabled = false;

    item.style.display = enabled ? 'inline-block' : 'none';
  });
}
</script>
