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
    <select id="case" name="case">
      <option value="all">All</option>
      <option value="01">[01] Petrification and Putrifaction</option>
      <option value="02">[02] Exchange and Extortion</option>
      <option value="03">[03] Punctuality and Perpetuity</option>
      <option value="04">[04] Ingestion and Incoherency</option>
      <option value="05">[05] Tumbling and Transcendence</option>
      <option value="06">[06] Mutilation and Metamorphosis</option>
      <option value="07">[07] Hazards and Harbingers</option>
      <option value="08">[08] Revelry and Revenge</option>
      <option value="09">[09] Amalgamation and Anathema</option>
      <option value="10">[10] Capers and Calamity</option>
      <option value="11">[11] Hardships and Homecomings</option>
      <option value="12">[12] Burglary and Blight</option>
    </select>
  </span>
  <span class="item">
    <label for="race">Race</label>
    <select id="race" name="race">
      <option value="all">All</option>
      <option value="dwarf">Dwarf</option>
      <option value="elf">Elf</option>
      <option value="human">Human</option>
      <option value="aarakocra">Aarakocra</option>
      <option value="demon">Demon</option>
      <option value="devil">Devil</option>
      <option value="dragon">Dragon</option>
      <option value="dragonborn">Dragonborn</option>
      <option value="eternal">Eternal</option>
      <option value="gargoyle">Gargoyle</option>
      <option value="githzerai">Githzerai</option>
      <option value="gnoll">Gnoll</option>
      <option value="gnome">Gnome</option>
      <option value="halfling">Halfling</option>
      <option value="kenku">Kenku</option>
      <option value="kobold">Kobold</option>
      <option value="lizardfolk">Lizardfolk</option>
      <option value="lycan">Lycan</option>
      <option value="orc">Orc</option>
      <option value="samsaran">Samsaran</option>
      <option value="undead">Undead</option>
      <option value="yikarian">Yikarian</option>
      <option value="other">Other</option>
    </select>
  </span>
  <span class="item">
    <label for="gender">Gender</label>
    <select id="gender" name="gender">
      <option value="all">All</option>
      <option value="female">Female</option>
      <option value="male">Male</option>
      <option value="non-binary">Non-binary</option>
    </select>
  </span>
</div>

{% include gallery %}

<script>
// CTR START HERE: Redo this code to work with the above filters.

function allFilters() {
  return document.getElementById('filters').querySelectorAll('select');
}

function hasClass(item, cls) {
  for (var i=0; i<item.classList.length; i++) {
    if (cls == item.classList[i]) return true;
  }
  return false;
}

function refreshVisibleItems() {
  var caseNo = document.getElementById('case').value;
  var race = document.getElementById('race').value;
  var gender = document.getElementById('gender').value;

  // Populate a hashset with the enabled gallery items.
  var catset = [];
  allCheckboxes().forEach(function(box) {
    if (box.checked) catset[box.id.replace('toggle-', 'category-')] = 1;
  });
  console.log('catset:');
  console.log(catset);
  for (var cat in catset) {
    console.log(`- ${cat}`);
  }
  console.log("and that's it");

  document.getElementById('list-of-extensions').querySelectorAll('li').forEach(function(item) {
    var enabled;
    if (allMode) {
      // Discern whether the item includes all checked categories.
      enabled = true;
      for (var cat in catset) {
        if (!hasClass(item, cat)) { enabled = false; break; }
      }
    }
    else {
      // Discern whether the item includes any checked category.
      enabled = false;
      for (var i=0; i<item.classList.length; i++) {
        if (item.classList[i] in catset) { enabled = true; break; }
      }
    }
    item.style.display = enabled ? 'block' : 'none';
  });
}

function toggleAllCategories(checked, refresh) {
  allCheckboxes().forEach(function(box) { box.checked = checked });
  if (refresh) refreshVisibleItems();
}

/* Credit: https://css-tricks.com/snippets/javascript/get-url-variables/ */
function getQueryVariable(variable) {
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0; i<vars.length; i++) {
    var pair = vars[i].split("=");
    if (pair[0] == variable) return pair[1];
  }
  return false;
}

var mode = getQueryVariable("mode");
var category = getQueryVariable("category");
var categories = getQueryVariable("categories");
if (mode || category || categories) {
  if (mode == "all") document.getElementById('filter-mode-all').checked = true;
  toggleAllCategories(false, false);
  if (category) {
    var box = document.getElementById(`toggle-${category}`);
    if (box) box.checked = true;
  }
  if (categories) {
    var category_array = categories.split(',');
    for (var i=0; i<category_array.length; i++) {
      var cat = category_array[i];
      var box = document.getElementById(`toggle-${cat}`);
      if (box) box.checked = true;
    }
  }
  refreshVisibleItems();
}
</script>
