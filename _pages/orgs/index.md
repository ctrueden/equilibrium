---
title: Organizations
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
      <option value="16">[16] Tunnels and Turpitude | The Afterworld?</option>
      <option value="17">[17] Misery and Mending | Arallu: Acrid Marshes</option>
      <option value="18">[18] Curses and Carafes | Trell: Minauros</option>
    </select>
  </span>
  <span class="item">
    <label for="type">Type</label>
    <select id="type" name="type" onchange="refreshVisibleItems()">
      <option value="all">All</option>
      <option value="company">Company</option>
      <option value="cult">Cult</option>
      <option value="family">Family</option>
      <option value="government">Government</option>
      <option value="law-firm">Law firm</option>
      <option value="military-order">Military order</option>
      <option value="monastic-order">Monastic order</option>
      <option value="syndicate">Syndicate</option>
      <option value="tribe">Tribe</option>
      <option value="vampire-clan">Vampire clan</option>
      <option value="other">Other</option>
    </select>
  </span>
  <span class="item">
    <label for="locale">Locale</label>
    <select id="locale" name="locale" onchange="refreshVisibleItems()">
      <option value="all">All</option>
      <option value="aecus">International</option>
      <option value="zephyr">Zephyr Federation</option>
      <option value="rup">Radiant Union of Pelor</option>
      <option value="mountain">The Mountain</option>
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

<script>
function hasClass(item, cls) {
  for (var i=0; i<item.classList.length; i++) {
    if (cls == item.classList[i] || item.classList[i].startsWith(`${cls}-`)) return true;
  }
  return false;
}

// Whether the item matches the given filter selection. The "other" choice
// matches items with none of the selector's listed values.
function matches(item, key, value) {
  if (value == 'all') return true;
  if (value != 'other') return item.classList.contains(`${key}-${value}`);
  var options = document.getElementById(key).children;
  for (var i=0; i<options.length; i++) {
    var v = options[i].value;
    if (v != 'all' && v != 'other' && item.classList.contains(`${key}-${v}`)) return false;
  }
  return true;
}

function refreshVisibleItems() {
  var caseNo = document.getElementById('case').value;
  var type = document.getElementById('type').value;
  var locale = document.getElementById('locale').value;

  document.getElementById('gallery').querySelectorAll('div').forEach(function(item) {
    var enabled = (caseNo == 'all' || hasClass(item, `case-${caseNo}`)) &&
      matches(item, 'type', type) && matches(item, 'locale', locale);
    item.style.display = enabled ? 'inline-block' : 'none';
  });
}
</script>
