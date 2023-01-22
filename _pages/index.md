---
title: Equilibrium
---

## Introduction

This is the Equilibrium campaign, a story about an international crime solving
team, the Supernatural Phenomena Investigators (SPI), set in a fantasy world of
eight nations hanging in the balance.

## Logistics

**Why?** To have fun, relax, solve mysteries and beat bad guys.

**Setting.** I decided not to set in an existing D&D campaign world (Forgotten
Realms, Greyhawk, etc.), but have reused many aspects of them for pragmatic
reasons. The political landscape is rather important to the culture that has
enabled a dedicated supernatural crime-solving organization to exist.
See [below](#setting) for further details on the setting.

**Rules.** We use the Dungeons & Dragons Fifth Edition (D&D5E) rules,
which are available online:
* [5e.tools](https://5e.tools) &ndash;
  A wealth of D&D5E rules in one place.
* [dndbeyond.com](https://www.dndbeyond.com/) &ndash;
  The official Wizards site for D&D5E rules.
* [5esrd.com](https://www.5esrd.com/) &ndash;
  A large subset of the core rules plus third party materials.
* [dnd5e.wikidot.com](https://dnd5e.wikidot.com/) &ndash; The DND 5th Edition
  community wiki, with even more rules, including from splat books, such as the
  class archetypes from *Xanathar's Guide to Everything*.

**Characters.** Main points of character creation:
* Try to hail from a unique territory and/or race. This helps diversity and world-building.
* Have a reason in mind for why you are part of (or being recruited for) the SPI.
* Have an unsolved mystery in your backstory.
* SPI agents are currently 10th level. Anything in the 5E Player's Handbook or
  [Xanathar's Guide to
  Everything](https://www.amazon.com/Xanathars-Guide-Everything-Wizards-Team/dp/0786966114)
  is fair game.

The current player characters are:

{% assign chars = "bec|cal|callie|freki|oz|vondal" | split: "|" -%}
{%- for p in site.pages -%}
{%- for char in chars -%}
{%- assign char-url = "/dossiers/" | append: char -%}
{%- if p.url == char-url -%}
<div style="display: inline-block; max-width: 128px; padding-right: 1em; text-align: center; vertical-align: top" markdown=1>
[![{{p.title}}]({{p.image}}){:style="max-height: 128px"}<br>{{p.title}}]({{site.baseurl}}{{p.url}})
</div>
{% comment -%} {%- endcomment -%}
{%- endif -%}
{%- endfor -%}
{%- endfor %}

For sweet sweet loot, see [Gear](gear).

For all characters in the story including NPCs, see the [Dossiers](dossiers).

## Setting

The known world is a single large continent called Aecus, with various
phenomena at the periphery which have hindered exploration, due to the
increasing inhospitality of the environment.

[![](assets/images/aecus-map.jpg){:style="max-width: 100%; max-height: 80vh"}](assets/images/aecus-map.jpg)

There are several countries which have enjoyed an uneasy peace for the past
half century. One of D&D's primary conceits is that there are [many intelligent
life forms](creatures), which tend to differ culturally, not always getting along.
As such, territories are often divided on racial lines, and this campaign is no
exception.

* \[N\] [The Zephyr Federation](locales/zephyr) -
  A windy and increasingly mountainous region to the north, inhabited by
  diverse [dragonborn](creatures/dragonborn) races. Further north,
  [dragons](creatures/dragons) dwell in the endless sky.
* \[S\] [Elyria](locales/elyria) -
  A sprawling forest in the deep south, home to [elves](creatures/elves) and other
  sylvan races.
* \[E\] [The Mountain and the Veldt](locales/mountain) -
  A volcano and surrounding lands where [dwarves](creatures/dwarves) dwell.
* \[NE\] [The Radiant Union of Pelor (RUP)](locales/rup) -
  Inhospitable desert lands in the northeast governed by a benevolent
  [paladin](https://dungeonsdragons.fandom.com/wiki/Paladin)
  order known as the [Luminous Defenders](orgs/luminous-defenders).
* \[W\] [Cognitutus](locales/cognitutus) -
  A great [gnomish](creatures/gnomes) city, which disappeared during the
  [War of Countless Dead](events/war-of-countless-dead).
* \[SE\] [The Selva Tribes](locales/selva) -
  [Orcish](creatures/orcs) tribes that vie for control of southeast rainforest
  territory.
* \[NW\] [The Archipelago of Trell](locales/trell) -
  A [fiendish](creatures/devils) island territory off the northwestern coast.
* \[SW\] [Arallu](locales/arallu) -
  A terrifying [undead](creatures/undead) realm to the southwest, about which
  little is known.
* [The Flux](locales/flux) - An uninhabitable zone bordering the nations.

## The War of Countless Dead, and the Aecus Concord

For decades, the world was at war. The initial cause of the conflict is a topic
of frequent historical debate&mdash;every nation tells it differently. After
all, every country has reasons they hate the others&mdash;especially their
neighbors. But there are a few facts upon which everyone agrees:

* All the nations of the world were involved.
* No one's hands were clean.
* The death toll was immeasurable.

Fifty years ago, the war ended&mdash;suddenly. All the soldiers fighting on the
warfront vanished without a trace, never to be seen again. After that, the
whole area became warped and twisted, resulting in what is now called the Flux.

With no armies left to deploy, the war was effectively over. The seven nations
still standing quickly met to sign a monumental peace treaty, the Aecus
Concord. One of the stipulations of the treaty was the foundation of an
international peacekeeping organization, consisting of individuals from all the
involved nations, also dubbed the Aecus Concord. It consists of three subunits:

* [**Supernatural Phenomena Investigation (SPI)**](orgs/spi), about whom this
  story is concerned. These are the people who are called in when the situation
  is too weird for the country's usual police force. Part detectives and part
  spies, SPI is the "[Interpol](https://en.wikipedia.org/wiki/Interpol)" of the
  A.C. However, their central focus is not on mundane crime, politics or
  intrigue, but only dangerous magic which might somehow threaten world peace.
* [**Military Aid and Defense (MAD)**](orgs/mad), a mixed force offering benign
  services to nations that request it. Members are volunteers from the armed
  forces of constituent nations. MAD is the "[U.N.
  Peacekeeping](https://en.wikipedia.org/wiki/United_Nations_peacekeeping)"
  force of the A.C.
* [**Trade, Enforcement, Arbitration and Mediation (TEAM)**](orgs/team), the
  diplomatic arm of the A.C., facilitating diplomatic relations and fair trade
  between the nations. It enforces its
  [arbitration](https://en.wikipedia.org/wiki/International_arbitration)
  decisions, as well as international regulations, largely via threat of trade
  sanctions and embargoes, should a nation fail to comply. Which so far has
  been rare.

The A.C. have created teleportation circles between major cities across Aecus,
which all three branches regularly utilize in service to their goals. The
teleportation circle spell can transport someone from any location to a
permanent circle. A relatively common item known as a teleport crystal also
exists (typically worth 10 gp) which anyone can use to activate a circle
without spellcasting; in this way, the cities stay connected and in touch with
one another. While it is not cost effective to use the circles for mass trade
of goods, or to commute between cities on a daily basis, they do provide many
diplomatic opportunities, as well as offering a rich courier market when the
goods or information being transported are of significant enough value.

## The Supernatural Phenomena Investigators (SPI)

The use of magic seems to affect people's memories. The stronger the magic, the
harder it is to recall later exactly what happened. People know magic exists,
and can describe cantrips. But memory becomes hazy surrounding higher levels of
magic. The only exception is the caster of the spell in question: they are
often unaffected, perhaps because it was their will manifest.

As such, magic and spellcasters are highly distrusted by most people. So much
so, that when something magical is going on, the local authorities almost never
want to deal with it. That's where the SPI comes in: an international, elite
team of agents with unique magical skills and know-how. Leading the team is
Mallory, the hard-boiled boss who's been running the operation for decades. The
way he tells it, the SPI never used to get any respect, but he's worked very
hard for a long time to change that. Finally, people are starting to take them
seriously.

Unfortunately, a few weeks ago, all veteran SPI teams disappeared during their
respective missions. All resurrection attempts fail. And meanwhile, the SPI
headquarters in the Mountain was obliterated by fire, destroying their files.
Most of the existing SPI staff escaped, but it was a close call. Mallory and
the remaining staff do know something about previous investigations, but with
magic involved, it's always tough to remember the details. The SPI is
recruiting new investigators now, and operating from a temporary but secure
location until something more permanent can be reestablished.
