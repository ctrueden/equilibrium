---
title: Calendar
---

<style>
:root {
  --edge-margin: 2px;
  --day-margin-tb: 0.5rem;
  --day-margin-lr: 1.25rem;
}

.month {
  background: lightblue;
  padding: 0.3rem;
}
table {
  border-collapse: separate;
  border-spacing: 0.75rem;
}
td {
  padding: var(--day-margin-tb) var(--day-margin-lr) !important;
  vertical-align: top;
  text-align: center;
  position: relative;
  white-space: nowrap;
  width: 10rem;
  border-color: #555 !important;
}
.edge {
  font-size: 0.6rem;
  position: absolute;
  padding: 0;
  margin: 0;
}
@media screen and (max-width: 1000px) {
  .elyria { display: none; }
  td { font-size: 0.9em; }
}
@media screen and (max-width: 875px) {
  .trell, .ignan { display: none; }
  td { font-size: 0.8em; }
}
@media screen and (max-width: 675px) {
  .aquan, .selva { display: none; }
  td { font-size: 0.7em; }
}

.day {
  top: 0;
  font-size: 0.7rem;
  font-weight: bold;
  width: calc(100% - 2*var(--day-margin-lr));
  text-align: center !important;
}
.trell {
  top: var(--edge-margin);
  left: var(--edge-margin);
  text-align: right !important;
  color: gray;
}
.ignan {
  top: var(--edge-margin);
  right: var(--edge-margin);
  text-align: right !important;
  color: gray;
}
.aquan {
  bottom: var(--edge-margin);
  left: var(--edge-margin);
  text-align: left !important;
  color: gray;
}
.elyria {
  bottom: var(--edge-margin);
  width: calc(100% - 2*var(--day-margin-lr));
  text-align: center !important;
  color: gray;
}
.selva {
  bottom: var(--edge-margin);
  right: var(--edge-margin);
  text-align: right !important;
  color: gray;
}

th {
  padding: 1em;
}
th .corner {
  margin-left: 0;
  font-weight: normal;
}
tr.spacing, tr.spacing td {
  border: none;
  background-color: white;
}
div.column {
  display: inline-block;
  padding-top: 0.5em;
  padding-left: 0.5em;
  padding-right: 0.5em;
}
</style>

For an overview of Aecan calendars, see [Calendar Systems](systems).

For a detailed calculation of Aecan dates including the solar and lunar cycles, see the
[Equilibrium calendar spreadsheet](https://docs.google.com/spreadsheets/d/1nPtq4H6Hc4krrQXcpF5PJNLf2_-q9p11HShezd5jquc/edit).


## AC50

<table>
<tr><th>Skyday</th><th>Forgeday</th><th>Woodsday</th><th>Kinsday</th><th>Evensday</th></tr>
<tr><th class="month" colspan=5>01 - Gyrus</th></tr>
<tr>
<td>
<div class="edge day">1</div>
<div class="edge trell">Pharast 2</div>
<div class="edge ignan">Sunsebb 2</div>
<div class="edge aquan">Eyre 7</div>
<div class="edge elyria">Flamerule 17</div>
<div class="edge selva">Bog 1</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">2</div>
<div class="edge trell">Pharast 3</div>
<div class="edge ignan">Sunsebb 3</div>
<div class="edge aquan">Eyre 8</div>
<div class="edge elyria">Flamerule 18</div>
<div class="edge selva">Bog 2</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">3</div>
<div class="edge trell">Pharast 4</div>
<div class="edge ignan">Sunsebb 4</div>
<div class="edge aquan">Eyre 9</div>
<div class="edge elyria">Flamerule 19</div>
<div class="edge selva">Bog 3</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">4</div>
<div class="edge trell">Pharast 5</div>
<div class="edge ignan">Sunsebb 5</div>
<div class="edge aquan">Eyre 10</div>
<div class="edge elyria">Flamerule 20</div>
<div class="edge selva">Bog 4</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">5</div>
<div class="edge trell">Pharast 6</div>
<div class="edge ignan">Sunsebb 6</div>
<div class="edge aquan">Eyre 11</div>
<div class="edge elyria">Flamerule 21</div>
<div class="edge selva">Bog 5</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">6</div>
<div class="edge trell">Pharast 7</div>
<div class="edge ignan">Sunsebb 7</div>
<div class="edge aquan">Eyre 12</div>
<div class="edge elyria">Flamerule 22</div>
<div class="edge selva">Bog 6</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">7</div>
<div class="edge trell">Pharast 8</div>
<div class="edge ignan">Sunsebb 8</div>
<div class="edge aquan">Eyre 13</div>
<div class="edge elyria">Flamerule 23</div>
<div class="edge selva">Bog 7</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">8</div>
<div class="edge trell">Pharast 9</div>
<div class="edge ignan">Sunsebb 9</div>
<div class="edge aquan">Eyre 14</div>
<div class="edge elyria">Flamerule 24</div>
<div class="edge selva">Bog 8</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">9</div>
<div class="edge trell">Pharast 10</div>
<div class="edge ignan">Sunsebb 10</div>
<div class="edge aquan">Eyre 15</div>
<div class="edge elyria">Flamerule 25</div>
<div class="edge selva">Bog 9</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">10</div>
<div class="edge trell">Pharast 11</div>
<div class="edge ignan">Sunsebb 11</div>
<div class="edge aquan">Eyre 16</div>
<div class="edge elyria">Flamerule 26</div>
<div class="edge selva">Bog 10</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">11</div>
<div class="edge trell">Pharast 12</div>
<div class="edge ignan">Sunsebb 12</div>
<div class="edge aquan">Eyre 17</div>
<div class="edge elyria">Flamerule 27</div>
<div class="edge selva">Bog 11</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">12</div>
<div class="edge trell">Pharast 13</div>
<div class="edge ignan">Sunsebb 13</div>
<div class="edge aquan">Eyre 18</div>
<div class="edge elyria">Flamerule 28</div>
<div class="edge selva">Bog 12</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">13</div>
<div class="edge trell">Pharast 14</div>
<div class="edge ignan">Sunsebb 14</div>
<div class="edge aquan">Eyre 19</div>
<div class="edge elyria">Flamerule 29</div>
<div class="edge selva">Bog 13</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">14</div>
<div class="edge trell">Pharast 15</div>
<div class="edge ignan">Sunsebb 15</div>
<div class="edge aquan">Eyre 20</div>
<div class="edge elyria">Flamerule 30</div>
<div class="edge selva">Bog 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">15</div>
<div class="edge trell">Pharast 16</div>
<div class="edge ignan">Sunsebb 16</div>
<div class="edge aquan">Eyre 21</div>
<div class="edge elyria"><strong>Midsummer</strong></div>
<div class="edge selva">Bog 15</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">16</div>
<div class="edge trell">Pharast 17</div>
<div class="edge ignan">Sunsebb 17</div>
<div class="edge aquan">Eyre 22</div>
<div class="edge elyria"><strong>Shieldmeet</strong></div>
<div class="edge selva">Bog 16</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">17</div>
<div class="edge trell">Pharast 18</div>
<div class="edge ignan">Sunsebb 18</div>
<div class="edge aquan">Eyre 23</div>
<div class="edge elyria">Eleasis 1</div>
<div class="edge selva">Bog 17</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">18</div>
<div class="edge trell">Pharast 19</div>
<div class="edge ignan">Sunsebb 19</div>
<div class="edge aquan">Eyre 24</div>
<div class="edge elyria">Eleasis 2</div>
<div class="edge selva">Bog 18</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">19</div>
<div class="edge trell">Pharast 20</div>
<div class="edge ignan">Sunsebb 20</div>
<div class="edge aquan">Eyre 25</div>
<div class="edge elyria">Eleasis 3</div>
<div class="edge selva">Bog 19</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">20</div>
<div class="edge trell">Pharast 21</div>
<div class="edge ignan">Sunsebb 21</div>
<div class="edge aquan">Eyre 26</div>
<div class="edge elyria">Eleasis 4</div>
<div class="edge selva">Bog 20</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">21</div>
<div class="edge trell">Pharast 22</div>
<div class="edge ignan">Sunsebb 22</div>
<div class="edge aquan">Eyre 27</div>
<div class="edge elyria">Eleasis 5</div>
<div class="edge selva">Bog 21</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">22</div>
<div class="edge trell">Pharast 23</div>
<div class="edge ignan">Sunsebb 23</div>
<div class="edge aquan">Eyre 28</div>
<div class="edge elyria">Eleasis 6</div>
<div class="edge selva">Bog 22</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">23</div>
<div class="edge trell">Pharast 24</div>
<div class="edge ignan">Sunsebb 24</div>
<div class="edge aquan">Dravago 1</div>
<div class="edge elyria">Eleasis 7</div>
<div class="edge selva">Bog 23</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">24</div>
<div class="edge trell">Pharast 25</div>
<div class="edge ignan">Sunsebb 25</div>
<div class="edge aquan">Dravago 2</div>
<div class="edge elyria">Eleasis 8</div>
<div class="edge selva">Swarm 1</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">25</div>
<div class="edge trell">Pharast 26</div>
<div class="edge ignan">Sunsebb 26</div>
<div class="edge aquan">Dravago 3</div>
<div class="edge elyria">Eleasis 9</div>
<div class="edge selva">Swarm 2</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">26</div>
<div class="edge trell">Pharast 27</div>
<div class="edge ignan">Sunsebb 27</div>
<div class="edge aquan">Dravago 4</div>
<div class="edge elyria">Eleasis 10</div>
<div class="edge selva">Swarm 3</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">27</div>
<div class="edge trell">Pharast 28</div>
<div class="edge ignan">Sunsebb 28</div>
<div class="edge aquan">Dravago 5</div>
<div class="edge elyria">Eleasis 11</div>
<div class="edge selva">Swarm 4</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">28</div>
<div class="edge trell">Pharast 29</div>
<div class="edge ignan"><em>Needfest 1</em></div>
<div class="edge aquan">Dravago 6</div>
<div class="edge elyria">Eleasis 12</div>
<div class="edge selva">Swarm 5</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">29</div>
<div class="edge trell">Pharast 30</div>
<div class="edge ignan"><em>Needfest 2</em></div>
<div class="edge aquan">Dravago 7</div>
<div class="edge elyria">Eleasis 13</div>
<div class="edge selva">Swarm 6</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">30</div>
<div class="edge trell">Pharast 31</div>
<div class="edge ignan"><em>Needfest 3</em></div>
<div class="edge aquan">Dravago 8</div>
<div class="edge elyria">Eleasis 14</div>
<div class="edge selva">Swarm 7</div>
&nbsp;<br>
&nbsp;
</td>
</tr>

<tr class="spacing"><td colspan=5></td></tr>
<tr>
<td style="border: none">&nbsp;</td>
<td colspan=3>
<div class="edge trell">Gozran 1</div>
<div class="edge ignan"><em>Needfest 4</em></div>
<div class="edge aquan">Dravago 9</div>
<div class="edge elyria">Eleasis 15</div>
<div class="edge selva">Swarm 8</div>
<strong>🧊 Glacian Apex</strong><br>
<div class="column">
Spring Equinox (Trell)<br>
Summer Solstice (Arallu)
</div>
<div class="column">
Autumn Equinox (Selva)<br>
Winter Solstice (RUP)
</div>
<div>
Ignan Winterday<br>
&nbsp;
</div>
</td>
<td style="border: none">&nbsp;</td>
</tr>
<tr class="spacing"><td colspan=5></td></tr>

<tr><th class="month" colspan=5>02 - Fons</th></tr>
<tr>
<td>
<div class="edge day">1</div>
<div class="edge trell">Gozran 2</div>
<div class="edge ignan"><em>Needfest 5</em></div>
<div class="edge aquan">Dravago 10</div>
<div class="edge elyria">Eleasis 16</div>
<div class="edge selva">Swarm 9</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">2</div>
<div class="edge trell">Gozran 3</div>
<div class="edge ignan"><em>Needfest 6</em></div>
<div class="edge aquan">Dravago 11</div>
<div class="edge elyria">Eleasis 17</div>
<div class="edge selva">Swarm 10</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">3</div>
<div class="edge trell">Gozran 4</div>
<div class="edge ignan"><em>Needfest 7</em></div>
<div class="edge aquan">Dravago 12</div>
<div class="edge elyria">Eleasis 18</div>
<div class="edge selva">Swarm 11</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">4</div>
<div class="edge trell">Gozran 5</div>
<div class="edge ignan"><em>Needfest 8</em></div>
<div class="edge aquan">Dravago 13</div>
<div class="edge elyria">Eleasis 19</div>
<div class="edge selva">Swarm 12</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">5</div>
<div class="edge trell">Gozran 6</div>
<div class="edge ignan">Fireseek 1</div>
<div class="edge aquan">Dravago 14</div>
<div class="edge elyria">Eleasis 20</div>
<div class="edge selva">Swarm 13</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">6</div>
<div class="edge trell">Gozran 7</div>
<div class="edge ignan">Fireseek 2</div>
<div class="edge aquan">Dravago 15</div>
<div class="edge elyria">Eleasis 21</div>
<div class="edge selva">Swarm 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">7</div>
<div class="edge trell">Gozran 8</div>
<div class="edge ignan">Fireseek 3</div>
<div class="edge aquan">Dravago 16</div>
<div class="edge elyria">Eleasis 22</div>
<div class="edge selva">Swarm 15</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">8</div>
<div class="edge trell">Gozran 9</div>
<div class="edge ignan">Fireseek 4</div>
<div class="edge aquan">Dravago 17</div>
<div class="edge elyria">Eleasis 23</div>
<div class="edge selva">Swarm 16</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">9</div>
<div class="edge trell">Gozran 10</div>
<div class="edge ignan">Fireseek 5</div>
<div class="edge aquan">Dravago 18</div>
<div class="edge elyria">Eleasis 24</div>
<div class="edge selva">Swarm 17</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">10</div>
<div class="edge trell">Gozran 11</div>
<div class="edge ignan">Fireseek 6</div>
<div class="edge aquan">Dravago 19</div>
<div class="edge elyria">Eleasis 25</div>
<div class="edge selva">Swarm 18</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">11</div>
<div class="edge trell">Gozran 12</div>
<div class="edge ignan">Fireseek 7</div>
<div class="edge aquan">Dravago 20</div>
<div class="edge elyria">Eleasis 26</div>
<div class="edge selva">Swarm 19</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">12</div>
<div class="edge trell">Gozran 13</div>
<div class="edge ignan">Fireseek 8</div>
<div class="edge aquan">Dravago 21</div>
<div class="edge elyria">Eleasis 27</div>
<div class="edge selva">Swarm 20</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">13</div>
<div class="edge trell">Gozran 14</div>
<div class="edge ignan">Fireseek 9</div>
<div class="edge aquan">Dravago 22</div>
<div class="edge elyria">Eleasis 28</div>
<div class="edge selva">Swarm 21</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">14</div>
<div class="edge trell">Gozran 15</div>
<div class="edge ignan">Fireseek 10</div>
<div class="edge aquan">Dravago 23</div>
<div class="edge elyria">Eleasis 29</div>
<div class="edge selva">Swarm 22</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">15</div>
<div class="edge trell">Gozran 16</div>
<div class="edge ignan">Fireseek 11</div>
<div class="edge aquan">Dravago 24</div>
<div class="edge elyria">Eleasis 30</div>
<div class="edge selva">Swarm 23</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">16</div>
<div class="edge trell">Gozran 17</div>
<div class="edge ignan">Fireseek 12</div>
<div class="edge aquan">Dravago 25</div>
<div class="edge elyria">Eleint 1</div>
<div class="edge selva">Hunt 1</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">17</div>
<div class="edge trell">Gozran 18</div>
<div class="edge ignan">Fireseek 13</div>
<div class="edge aquan">Dravago 26</div>
<div class="edge elyria">Eleint 2</div>
<div class="edge selva">Hunt 2</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">18</div>
<div class="edge trell">Gozran 19</div>
<div class="edge ignan">Fireseek 14</div>
<div class="edge aquan">Dravago 27</div>
<div class="edge elyria">Eleint 3</div>
<div class="edge selva">Hunt 3</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">19</div>
<div class="edge trell">Gozran 20</div>
<div class="edge ignan">Fireseek 15</div>
<div class="edge aquan">Dravago 28</div>
<div class="edge elyria">Eleint 4</div>
<div class="edge selva">Hunt 4</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">20</div>
<div class="edge trell">Gozran 21</div>
<div class="edge ignan">Fireseek 16</div>
<div class="edge aquan"><strong>Summerday</strong></div>
<div class="edge elyria">Eleint 5</div>
<div class="edge selva">Hunt 5</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">21</div>
<div class="edge trell">Gozran 22</div>
<div class="edge ignan">Fireseek 17</div>
<div class="edge aquan">Nymm 1</div>
<div class="edge elyria">Eleint 6</div>
<div class="edge selva">Hunt 6</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">22</div>
<div class="edge trell">Gozran 23</div>
<div class="edge ignan">Fireseek 18</div>
<div class="edge aquan">Nymm 2</div>
<div class="edge elyria">Eleint 7</div>
<div class="edge selva">Hunt 7</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">23</div>
<div class="edge trell">Gozran 24</div>
<div class="edge ignan">Fireseek 19</div>
<div class="edge aquan">Nymm 3</div>
<div class="edge elyria">Eleint 8</div>
<div class="edge selva">Hunt 8</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">24</div>
<div class="edge trell">Gozran 25</div>
<div class="edge ignan">Fireseek 20</div>
<div class="edge aquan">Nymm 4</div>
<div class="edge elyria">Eleint 9</div>
<div class="edge selva">Hunt 9</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">25</div>
<div class="edge trell">Gozran 26</div>
<div class="edge ignan">Fireseek 21</div>
<div class="edge aquan">Nymm 5</div>
<div class="edge elyria">Eleint 10</div>
<div class="edge selva">Hunt 10</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">26</div>
<div class="edge trell">Gozran 27</div>
<div class="edge ignan">Fireseek 22</div>
<div class="edge aquan">Nymm 6</div>
<div class="edge elyria">Eleint 11</div>
<div class="edge selva">Hunt 11</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">27</div>
<div class="edge trell">Gozran 28</div>
<div class="edge ignan">Fireseek 23</div>
<div class="edge aquan">Nymm 7</div>
<div class="edge elyria">Eleint 12</div>
<div class="edge selva">Hunt 12</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">28</div>
<div class="edge trell">Gozran 29</div>
<div class="edge ignan">Fireseek 24</div>
<div class="edge aquan">Nymm 8</div>
<div class="edge elyria">Eleint 13</div>
<div class="edge selva">Hunt 13</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">29</div>
<div class="edge trell">Gozran 30</div>
<div class="edge ignan">Fireseek 25</div>
<div class="edge aquan">Nymm 9</div>
<div class="edge elyria">Eleint 14</div>
<div class="edge selva">Hunt 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">30</div>
<div class="edge trell">Desnus 1</div>
<div class="edge ignan">Fireseek 26</div>
<div class="edge aquan">Nymm 10</div>
<div class="edge elyria">Eleint 15</div>
<div class="edge selva">Hunt 15</div>
&nbsp;<br>
&nbsp;
</td>
</tr>

<tr class="spacing"><td colspan=5></td></tr>
<tr>
<td style="border: none">&nbsp;</td>
<td colspan=3>
<div class="edge trell">Desnus 2</div>
<div class="edge ignan">Fireseek 27</div>
<div class="edge aquan">Nymm 11</div>
<div class="edge elyria">Eleint 16</div>
<div class="edge selva">Hunt 16</div>
<strong>🌊 Aquan Apex</strong><br>
<div class="column">
Spring Equinox (Zephyr)<br>
Summer Solstice (Ocean)
</div>
<div class="column">
Autumn Equinox (Elyria)<br>
Winter Solstice (Mountain)
</div>
<div>
&nbsp;
</div>
</td>
<td style="border: none">&nbsp;</td>
</tr>
<tr class="spacing"><td colspan=5></td></tr>

<tr><th class="month" colspan=5>03 - Solis</th></tr>
<tr>
<td>
<div class="edge day">1</div>
<div class="edge trell">Desnus 3</div>
<div class="edge ignan">Fireseek 28</div>
<div class="edge aquan">Nymm 12</div>
<div class="edge elyria">Eleint 17</div>
<div class="edge selva">Hunt 17</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">2</div>
<div class="edge trell">Desnus 4</div>
<div class="edge ignan">Readying 1</div>
<div class="edge aquan">Nymm 13</div>
<div class="edge elyria">Eleint 18</div>
<div class="edge selva">Hunt 18</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">3</div>
<div class="edge trell">Desnus 5</div>
<div class="edge ignan">Readying 2</div>
<div class="edge aquan">Nymm 14</div>
<div class="edge elyria">Eleint 19</div>
<div class="edge selva">Hunt 19</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">4</div>
<div class="edge trell">Desnus 6</div>
<div class="edge ignan">Readying 3</div>
<div class="edge aquan">Nymm 15</div>
<div class="edge elyria">Eleint 20</div>
<div class="edge selva">Hunt 20</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">5</div>
<div class="edge trell">Desnus 7</div>
<div class="edge ignan">Readying 4</div>
<div class="edge aquan">Nymm 16</div>
<div class="edge elyria">Eleint 21</div>
<div class="edge selva">Hunt 21</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">6</div>
<div class="edge trell">Desnus 8</div>
<div class="edge ignan">Readying 5</div>
<div class="edge aquan">Nymm 17</div>
<div class="edge elyria">Eleint 22</div>
<div class="edge selva">Hunt 22</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">7</div>
<div class="edge trell">Desnus 9</div>
<div class="edge ignan">Readying 6</div>
<div class="edge aquan">Nymm 18</div>
<div class="edge elyria">Eleint 23</div>
<div class="edge selva">Hunt 23</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">8</div>
<div class="edge trell">Desnus 10</div>
<div class="edge ignan">Readying 7</div>
<div class="edge aquan">Nymm 19</div>
<div class="edge elyria">Eleint 24</div>
<div class="edge selva">Dark 1</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">9</div>
<div class="edge trell">Desnus 11</div>
<div class="edge ignan">Readying 8</div>
<div class="edge aquan">Nymm 20</div>
<div class="edge elyria">Eleint 25</div>
<div class="edge selva">Dark 2</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">10</div>
<div class="edge trell">Desnus 12</div>
<div class="edge ignan">Readying 9</div>
<div class="edge aquan">Nymm 21</div>
<div class="edge elyria">Eleint 26</div>
<div class="edge selva">Dark 3</div>
&nbsp;<br>
Case <a href="../events/case-01">01</a><br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">11</div>
<div class="edge trell">Desnus 13</div>
<div class="edge ignan">Readying 10</div>
<div class="edge aquan">Nymm 22</div>
<div class="edge elyria">Eleint 27</div>
<div class="edge selva">Dark 4</div>
&nbsp;<br>
Case <a href="../events/case-02">02</a> (pt <a href="../events/case-02e01">01</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">12</div>
<div class="edge trell">Desnus 14</div>
<div class="edge ignan">Readying 11</div>
<div class="edge aquan">Nymm 23</div>
<div class="edge elyria">Eleint 28</div>
<div class="edge selva">Dark 5</div>
&nbsp;<br>
Case <a href="../events/case-02">02</a> (pt <a href="../events/case-02e02">02</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">13</div>
<div class="edge trell">Desnus 15</div>
<div class="edge ignan">Readying 12</div>
<div class="edge aquan">Nymm 24</div>
<div class="edge elyria">Eleint 29</div>
<div class="edge selva">Dark 6</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">14</div>
<div class="edge trell">Desnus 16</div>
<div class="edge ignan">Readying 13</div>
<div class="edge aquan">Nymm 25</div>
<div class="edge elyria">Eleint 30</div>
<div class="edge selva">Dark 7</div>
&nbsp;<br>
Case <a href="../events/case-03">03</a><br>
&nbsp;
</td>
<td>
<div class="edge day">15</div>
<div class="edge trell">Desnus 17</div>
<div class="edge ignan">Readying 14</div>
<div class="edge aquan">Nymm 26</div>
<div class="edge elyria"><strong>Highharvestide</strong></div>
<div class="edge selva">Dark 8</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">16</div>
<div class="edge trell">Desnus 18</div>
<div class="edge ignan">Readying 15</div>
<div class="edge aquan">Nymm 27</div>
<div class="edge elyria">Marpenoth 1</div>
<div class="edge selva">Dark 9</div>
&nbsp;<br>
Case <a href="../events/case-04">04</a><br>
&nbsp;
</td>
<td>
<div class="edge day">17</div>
<div class="edge trell">Desnus 19</div>
<div class="edge ignan">Readying 16</div>
<div class="edge aquan">Nymm 28</div>
<div class="edge elyria">Marpenoth 2</div>
<div class="edge selva">Dark 10</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">18</div>
<div class="edge trell">Desnus 20</div>
<div class="edge ignan">Readying 17</div>
<div class="edge aquan">Lharvion 1</div>
<div class="edge elyria">Marpenoth 3</div>
<div class="edge selva">Dark 11</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">19</div>
<div class="edge trell">Desnus 21</div>
<div class="edge ignan">Readying 18</div>
<div class="edge aquan">Lharvion 2</div>
<div class="edge elyria">Marpenoth 4</div>
<div class="edge selva">Dark 12</div>
&nbsp;<br>
Case <a href="../events/case-05">05</a><br>
&nbsp;
</td>
<td>
<div class="edge day">20</div>
<div class="edge trell">Desnus 22</div>
<div class="edge ignan">Readying 19</div>
<div class="edge aquan">Lharvion 3</div>
<div class="edge elyria">Marpenoth 5</div>
<div class="edge selva">Dark 13</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">21</div>
<div class="edge trell">Desnus 23</div>
<div class="edge ignan">Readying 20</div>
<div class="edge aquan">Lharvion 4</div>
<div class="edge elyria">Marpenoth 6</div>
<div class="edge selva">Dark 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">22</div>
<div class="edge trell">Desnus 24</div>
<div class="edge ignan">Readying 21</div>
<div class="edge aquan">Lharvion 5</div>
<div class="edge elyria">Marpenoth 7</div>
<div class="edge selva">Dark 15</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">23</div>
<div class="edge trell">Desnus 25</div>
<div class="edge ignan">Readying 22</div>
<div class="edge aquan">Lharvion 6</div>
<div class="edge elyria">Marpenoth 8</div>
<div class="edge selva">Dark 16</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">24</div>
<div class="edge trell">Desnus 26</div>
<div class="edge ignan">Readying 23</div>
<div class="edge aquan">Lharvion 7</div>
<div class="edge elyria">Marpenoth 9</div>
<div class="edge selva">Dark 17</div>
&nbsp;<br>
Case <a href="../events/case-06">06</a> (pt <a href="../events/case-06e01">01</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">25</div>
<div class="edge trell">Desnus 27</div>
<div class="edge ignan">Readying 24</div>
<div class="edge aquan">Lharvion 8</div>
<div class="edge elyria">Marpenoth 10</div>
<div class="edge selva">Dark 18</div>
&nbsp;<br>
Case <a href="../events/case-06">06</a> (pts <a href="../events/case-06e02">02</a>, <a href="../events/case-06e03">03</a>)<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">26</div>
<div class="edge trell">Desnus 28</div>
<div class="edge ignan">Readying 25</div>
<div class="edge aquan">Lharvion 9</div>
<div class="edge elyria">Marpenoth 11</div>
<div class="edge selva">Dark 19</div>
&nbsp;<br>
&larr; Case <a href="../events/case-06">06</a> (pt <a href="../events/case-06e03">03</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">27</div>
<div class="edge trell">Desnus 29</div>
<div class="edge ignan">Readying 26</div>
<div class="edge aquan">Lharvion 10</div>
<div class="edge elyria">Marpenoth 12</div>
<div class="edge selva">Dark 20</div>
&nbsp;<br>
&larr; Case <a href="../events/case-06">06</a> (pt <a href="../events/case-06e03">03</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">28</div>
<div class="edge trell">Desnus 30</div>
<div class="edge ignan">Readying 27</div>
<div class="edge aquan">Lharvion 11</div>
<div class="edge elyria">Marpenoth 13</div>
<div class="edge selva">Dark 21</div>
&nbsp;<br>
Case <a href="../events/case-06">06</a> (pts <a href="../events/case-06e03">03</a>, <a href="../events/case-06e04">04</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">29</div>
<div class="edge trell">Desnus 31</div>
<div class="edge ignan">Readying 28</div>
<div class="edge aquan">Lharvion 12</div>
<div class="edge elyria">Marpenoth 14</div>
<div class="edge selva">Dark 22</div>
&nbsp;<br>
&larr; Case <a href="../events/case-06">06</a> (pt <a href="../events/case-06e04">04</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">30</div>
<div class="edge trell"><strong>Taurus</strong></div>
<div class="edge ignan">Coldeven 1</div>
<div class="edge aquan">Lharvion 13</div>
<div class="edge elyria">Marpenoth 15</div>
<div class="edge selva">Dark 23</div>
&nbsp;<br>
&larr; Case <a href="../events/case-06">06</a> (pt <a href="../events/case-06e04">04</a>) &rarr;<br>
&nbsp;
</td>
</tr>

<tr class="spacing"><td colspan=5></td></tr>
<tr>
<td style="border: none">&nbsp;</td>
<td colspan=3>
<div class="edge trell">Sarenith 1</div>
<div class="edge ignan">Coldeven 2</div>
<div class="edge aquan">Lharvion 14</div>
<div class="edge elyria">Marpenoth 16</div>
<div class="edge selva">Black 1</div>
<strong>🌀 Procellan Apex</strong><br>
<div class="column">
Spring Equinox (RUP)<br>
Summer Solstice (Trell)
</div>
<div class="column">
Autumn Equinox (Arallu)<br>
Winter Solstice (Selva)
</div>
<div>
&larr; Case <a href="../events/case-06">06</a> (pt <a href="../events/case-06e04">04</a>) &rarr;<br>
&nbsp;
</div>
</td>
<td style="border: none">&nbsp;</td>
</tr>
<tr class="spacing"><td colspan=5></td></tr>

<tr><th class="month" colspan=5>04 - Cudo</th></tr>
<tr>
<td>
<div class="edge day">1</div>
<div class="edge trell">Sarenith 2</div>
<div class="edge ignan">Coldeven 3</div>
<div class="edge aquan">Lharvion 15</div>
<div class="edge elyria">Marpenoth 17</div>
<div class="edge selva">Black 2</div>
&nbsp;<br>
&larr; Case <a href="../events/case-06">06</a> (pt <a href="../events/case-06e04">04</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">2</div>
<div class="edge trell">Sarenith 3</div>
<div class="edge ignan">Coldeven 4</div>
<div class="edge aquan">Lharvion 16</div>
<div class="edge elyria">Marpenoth 18</div>
<div class="edge selva">Black 3</div>
&nbsp;<br>
&larr; Case <a href="../events/case-06">06</a> (pt <a href="../events/case-06e04">04</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">3</div>
<div class="edge trell">Sarenith 4</div>
<div class="edge ignan">Coldeven 5</div>
<div class="edge aquan">Lharvion 17</div>
<div class="edge elyria">Marpenoth 19</div>
<div class="edge selva">Black 4</div>
&nbsp;<br>
&larr; Case <a href="../events/case-06">06</a> (pt <a href="../events/case-06e04">04</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">4</div>
<div class="edge trell">Sarenith 5</div>
<div class="edge ignan">Coldeven 6</div>
<div class="edge aquan">Lharvion 18</div>
<div class="edge elyria">Marpenoth 20</div>
<div class="edge selva">Black 5</div>
&nbsp;<br>
&larr; Case <a href="../events/case-06">06</a> (pt <a href="../events/case-06e04">04</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">5</div>
<div class="edge trell">Sarenith 6</div>
<div class="edge ignan">Coldeven 7</div>
<div class="edge aquan">Lharvion 19</div>
<div class="edge elyria">Marpenoth 21</div>
<div class="edge selva">Black 6</div>
&nbsp;<br>
&larr; Case <a href="../events/case-06">06</a> (pt <a href="../events/case-06e04">04</a>) &rarr;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">6</div>
<div class="edge trell">Sarenith 7</div>
<div class="edge ignan">Coldeven 8</div>
<div class="edge aquan">Lharvion 20</div>
<div class="edge elyria">Marpenoth 22</div>
<div class="edge selva">Black 7</div>
&nbsp;<br>
&larr; Case <a href="../events/case-06">06</a> (pt <a href="../events/case-06e04">04</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">7</div>
<div class="edge trell">Sarenith 8</div>
<div class="edge ignan">Coldeven 9</div>
<div class="edge aquan">Lharvion 21</div>
<div class="edge elyria">Marpenoth 23</div>
<div class="edge selva">Black 8</div>
&nbsp;<br>
Case <a href="../events/case-06">06</a> (pts <a href="../events/case-06e04">04</a>, <a href="../events/case-06e05">05</a>, <a href="../events/case-06e06">06</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">8</div>
<div class="edge trell">Sarenith 9</div>
<div class="edge ignan">Coldeven 10</div>
<div class="edge aquan">Lharvion 22</div>
<div class="edge elyria">Marpenoth 24</div>
<div class="edge selva">Black 9</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">9</div>
<div class="edge trell">Sarenith 10</div>
<div class="edge ignan">Coldeven 11</div>
<div class="edge aquan">Lharvion 23</div>
<div class="edge elyria">Marpenoth 25</div>
<div class="edge selva">Black 10</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">10</div>
<div class="edge trell">Sarenith 11</div>
<div class="edge ignan">Coldeven 12</div>
<div class="edge aquan">Lharvion 24</div>
<div class="edge elyria">Marpenoth 26</div>
<div class="edge selva">Black 11</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">11</div>
<div class="edge trell">Sarenith 12</div>
<div class="edge ignan">Coldeven 13</div>
<div class="edge aquan">Lharvion 25</div>
<div class="edge elyria">Marpenoth 27</div>
<div class="edge selva">Black 12</div>
&nbsp;<br>
Case <a href="../events/case-07">07</a> (pt <a href="../events/case-07e01">01</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">12</div>
<div class="edge trell">Sarenith 13</div>
<div class="edge ignan">Coldeven 14</div>
<div class="edge aquan">Lharvion 26</div>
<div class="edge elyria">Marpenoth 28</div>
<div class="edge selva">Black 13</div>
&nbsp;<br>
&larr; Case <a href="../events/case-07">07</a> (pt <a href="../events/case-07e01">01</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">13</div>
<div class="edge trell">Sarenith 14</div>
<div class="edge ignan">Coldeven 15</div>
<div class="edge aquan">Lharvion 27</div>
<div class="edge elyria">Marpenoth 29</div>
<div class="edge selva">Black 14</div>
&nbsp;<br>
Case <a href="../events/case-07">07</a> (pts <a href="../events/case-07e01">1</a>, <a href="../events/case-07e02">2</a>, <a href="../events/case-07e03">3</a>, <a href="../events/case-07e04">4</a>, <a href="../events/case-07e05">5</a>, <a href="../events/case-07e06">6</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">14</div>
<div class="edge trell">Sarenith 15</div>
<div class="edge ignan">Coldeven 16</div>
<div class="edge aquan">Lharvion 28</div>
<div class="edge elyria">Marpenoth 30</div>
<div class="edge selva">Black 15</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">15</div>
<div class="edge trell">Sarenith 16</div>
<div class="edge ignan">Coldeven 17</div>
<div class="edge aquan">Barrakas 1</div>
<div class="edge elyria">Uktar 1</div>
<div class="edge selva">Black 16</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">16</div>
<div class="edge trell">Sarenith 17</div>
<div class="edge ignan">Coldeven 18</div>
<div class="edge aquan">Barrakas 2</div>
<div class="edge elyria">Uktar 2</div>
<div class="edge selva">Black 17</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">17</div>
<div class="edge trell">Sarenith 18</div>
<div class="edge ignan">Coldeven 19</div>
<div class="edge aquan">Barrakas 3</div>
<div class="edge elyria">Uktar 3</div>
<div class="edge selva">Black 18</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">18</div>
<div class="edge trell">Sarenith 19</div>
<div class="edge ignan">Coldeven 20</div>
<div class="edge aquan">Barrakas 4</div>
<div class="edge elyria">Uktar 4</div>
<div class="edge selva">Black 19</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">19</div>
<div class="edge trell">Sarenith 20</div>
<div class="edge ignan">Coldeven 21</div>
<div class="edge aquan">Barrakas 5</div>
<div class="edge elyria">Uktar 5</div>
<div class="edge selva">Black 20</div>
&nbsp;<br>
Case <a href="../events/case-08">08</a> (pts <a href="../events/case-08e01">1</a>, <a href="../events/case-08e02">2</a>, <a href="../events/case-08e03">3</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">20</div>
<div class="edge trell">Sarenith 21</div>
<div class="edge ignan">Coldeven 22</div>
<div class="edge aquan">Barrakas 6</div>
<div class="edge elyria">Uktar 6</div>
<div class="edge selva">Black 21</div>
&nbsp;<br>
Case <a href="../events/case-09">09</a> (pt <a href="../events/case-09e01">1</a>)<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">21</div>
<div class="edge trell">Sarenith 22</div>
<div class="edge ignan">Coldeven 23</div>
<div class="edge aquan">Barrakas 7</div>
<div class="edge elyria">Uktar 7</div>
<div class="edge selva">Black 22</div>
&nbsp;<br>
&larr; Case <a href="../events/case-09">09</a> (pt <a href="../events/case-09e01">1</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">22</div>
<div class="edge trell">Sarenith 23</div>
<div class="edge ignan">Coldeven 24</div>
<div class="edge aquan">Barrakas 8</div>
<div class="edge elyria">Uktar 8</div>
<div class="edge selva">Black 23</div>
&nbsp;<br>
&larr; Case <a href="../events/case-09">09</a> (pt <a href="../events/case-09e01">1</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">23</div>
<div class="edge trell">Sarenith 24</div>
<div class="edge ignan">Coldeven 25</div>
<div class="edge aquan">Barrakas 9</div>
<div class="edge elyria">Uktar 9</div>
<div class="edge selva">Cold 1</div>
&nbsp;<br>
&larr; Case <a href="../events/case-09">09</a> (pt <a href="../events/case-09e01">1</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">24</div>
<div class="edge trell">Sarenith 25</div>
<div class="edge ignan">Coldeven 26</div>
<div class="edge aquan">Barrakas 10</div>
<div class="edge elyria">Uktar 10</div>
<div class="edge selva">Cold 2</div>
&nbsp;<br>
&larr; Case <a href="../events/case-09">09</a> (pt <a href="../events/case-09e01">1</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">25</div>
<div class="edge trell">Sarenith 26</div>
<div class="edge ignan">Coldeven 27</div>
<div class="edge aquan">Barrakas 11</div>
<div class="edge elyria">Uktar 11</div>
<div class="edge selva">Cold 3</div>
&nbsp;<br>
Case <a href="../events/case-09">09</a> (pts <a href="../events/case-09e01">1</a>, <a href="../events/case-09e02">2</a>, <a href="../events/case-09e03">3</a>, <a href="../events/case-09e04">4</a>)<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">26</div>
<div class="edge trell">Sarenith 27</div>
<div class="edge ignan">Coldeven 28</div>
<div class="edge aquan">Barrakas 12</div>
<div class="edge elyria">Uktar 12</div>
<div class="edge selva">Cold 4</div>
&nbsp;<br>
&larr; Case <a href="../events/case-09">09</a> (pt <a href="../events/case-09e04">4</a>)<br>
Case <a href="../events/case-10">10</a> (pts <a href="../events/case-10e01">1</a>, <a href="../events/case-10e02">2</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">27</div>
<div class="edge trell">Sarenith 28</div>
<div class="edge ignan"><em>Growfest 1</em></div>
<div class="edge aquan">Barrakas 13</div>
<div class="edge elyria">Uktar 13</div>
<div class="edge selva">Cold 5</div>
&nbsp;<br>
&larr; Case <a href="../events/case-10">10</a> (pt <a href="../events/case-10e02">2</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">28</div>
<div class="edge trell">Sarenith 29</div>
<div class="edge ignan"><em>Growfest 2</em></div>
<div class="edge aquan">Barrakas 14</div>
<div class="edge elyria">Uktar 14</div>
<div class="edge selva">Cold 6</div>
&nbsp;<br>
&larr; Case <a href="../events/case-10">10</a> (pt <a href="../events/case-10e02">2</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">29</div>
<div class="edge trell">Sarenith 30</div>
<div class="edge ignan"><em>Growfest 3</em></div>
<div class="edge aquan">Barrakas 15</div>
<div class="edge elyria">Uktar 15</div>
<div class="edge selva">Cold 7</div>
&nbsp;<br>
&larr; Case <a href="../events/case-10">10</a> (pt <a href="../events/case-10e02">2</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">30</div>
<div class="edge trell">Erastus 1</div>
<div class="edge ignan"><em>Growfest 4</em></div>
<div class="edge aquan">Barrakas 16</div>
<div class="edge elyria">Uktar 16</div>
<div class="edge selva">Cold 8</div>
&nbsp;<br>
&larr; Case <a href="../events/case-10">10</a> (pt <a href="../events/case-10e02">2</a>) &rarr;<br>
🌓 Waxing Half-Moon<br>
Ignan Greenday<br>
&nbsp;
</td>
</tr>

<tr class="spacing"><td colspan=5></td></tr>

<tr><th class="month" colspan=5>05 - Rixa</th></tr>
<tr>
<td>
<div class="edge day">1</div>
<div class="edge trell">Erastus 2</div>
<div class="edge ignan"><em>Growfest 5</em></div>
<div class="edge aquan">Barrakas 17</div>
<div class="edge elyria">Uktar 17</div>
<div class="edge selva">Cold 9</div>
&nbsp;<br>
&larr; Case <a href="../events/case-10">10</a> (pt <a href="../events/case-10e02">2</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">2</div>
<div class="edge trell">Erastus 3</div>
<div class="edge ignan"><em>Growfest 6</em></div>
<div class="edge aquan">Barrakas 18</div>
<div class="edge elyria">Uktar 18</div>
<div class="edge selva">Cold 10</div>
&nbsp;<br>
Case <a href="../events/case-10">10</a> (pts <a href="../events/case-10e02">2</a>, <a href="../events/case-10e03">3</a>, <a href="../events/case-10e04">4</a>, <a href="../events/case-10e05">5</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">3</div>
<div class="edge trell">Erastus 4</div>
<div class="edge ignan"><em>Growfest 7</em></div>
<div class="edge aquan">Barrakas 19</div>
<div class="edge elyria">Uktar 19</div>
<div class="edge selva">Cold 11</div>
&nbsp;<br>
&larr; Case <a href="../events/case-10">10</a> (pt <a href="../events/case-10e05">5</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">4</div>
<div class="edge trell">Erastus 5</div>
<div class="edge ignan"><em>Growfest 8</em></div>
<div class="edge aquan">Barrakas 20</div>
<div class="edge elyria">Uktar 20</div>
<div class="edge selva">Cold 12</div>
&nbsp;<br>
&larr; Case <a href="../events/case-10">10</a> (pt <a href="../events/case-10e05">5</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">5</div>
<div class="edge trell">Erastus 6</div>
<div class="edge ignan">Planting 1</div>
<div class="edge aquan">Barrakas 21</div>
<div class="edge elyria">Uktar 21</div>
<div class="edge selva">Cold 13</div>
&nbsp;<br>
&larr; Case <a href="../events/case-10">10</a> (pt <a href="../events/case-10e05">5</a>) &rarr;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">6</div>
<div class="edge trell">Erastus 7</div>
<div class="edge ignan">Planting 2</div>
<div class="edge aquan">Barrakas 22</div>
<div class="edge elyria">Uktar 22</div>
<div class="edge selva">Cold 14</div>
&nbsp;<br>
Case <a href="../events/case-10">10</a> (pts <a href="../events/case-10e05">5</a>, <a href="../events/case-10e06">6</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">7</div>
<div class="edge trell">Erastus 8</div>
<div class="edge ignan">Planting 3</div>
<div class="edge aquan">Barrakas 23</div>
<div class="edge elyria">Uktar 23</div>
<div class="edge selva">Cold 15</div>
&nbsp;<br>
&larr; Case <a href="../events/case-10">10</a> (pt <a href="../events/case-10e06">6</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">8</div>
<div class="edge trell">Erastus 9</div>
<div class="edge ignan">Planting 4</div>
<div class="edge aquan">Barrakas 24</div>
<div class="edge elyria">Uktar 24</div>
<div class="edge selva">Cold 16</div>
&nbsp;<br>
&larr; Case <a href="../events/case-10">10</a> (pt <a href="../events/case-10e06">6</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">9</div>
<div class="edge trell">Erastus 10</div>
<div class="edge ignan">Planting 5</div>
<div class="edge aquan">Barrakas 25</div>
<div class="edge elyria">Uktar 25</div>
<div class="edge selva">Cold 17</div>
&nbsp;<br>
&larr; Case <a href="../events/case-10">10</a> (pt <a href="../events/case-10e06">6</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">10</div>
<div class="edge trell">Erastus 11</div>
<div class="edge ignan">Planting 6</div>
<div class="edge aquan">Barrakas 26</div>
<div class="edge elyria">Uktar 26</div>
<div class="edge selva">Cold 18</div>
&nbsp;<br>
&larr; Case <a href="../events/case-10">10</a> (pt <a href="../events/case-10e06">6</a>)<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">11</div>
<div class="edge trell">Erastus 12</div>
<div class="edge ignan">Planting 7</div>
<div class="edge aquan">Barrakas 27</div>
<div class="edge elyria">Uktar 27</div>
<div class="edge selva">Cold 19</div>
&nbsp;<br>
Case <a href="../events/case-11">11</a> (pts <a href="../events/case-11e01">1</a>, <a href="../events/case-11e02">2</a>, <a href="../events/case-11e03">3</a>, <a href="../events/case-11e04">4</a>, <a href="../events/case-11e05">5</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">12</div>
<div class="edge trell">Erastus 13</div>
<div class="edge ignan">Planting 8</div>
<div class="edge aquan">Barrakas 28</div>
<div class="edge elyria">Uktar 28</div>
<div class="edge selva">Cold 20</div>
&nbsp;<br>
&larr; Case <a href="../events/case-11">11</a> (pt <a href="../events/case-11e05">5</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">13</div>
<div class="edge trell">Erastus 14</div>
<div class="edge ignan">Planting 9</div>
<div class="edge aquan">Rhaan 1</div>
<div class="edge elyria">Uktar 29</div>
<div class="edge selva">Cold 21</div>
&nbsp;<br>
&larr; Case <a href="../events/case-11">11</a> (pt <a href="../events/case-11e05">5</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">14</div>
<div class="edge trell">Erastus 15</div>
<div class="edge ignan">Planting 10</div>
<div class="edge aquan">Rhaan 2</div>
<div class="edge elyria">Uktar 30</div>
<div class="edge selva">Cold 22</div>
&nbsp;<br>
&larr; Case <a href="../events/case-11">11</a> (pt <a href="../events/case-11e05">5</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">15</div>
<div class="edge trell">Erastus 16</div>
<div class="edge ignan">Planting 11</div>
<div class="edge aquan">Rhaan 3</div>
<div class="edge elyria"><strong>Moon Feast</strong></div>
<div class="edge selva">Cold 23</div>
&nbsp;<br>
&larr; Case <a href="../events/case-11">11</a> (pt <a href="../events/case-11e05">5</a>) &rarr;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">16</div>
<div class="edge trell">Erastus 17</div>
<div class="edge ignan">Planting 12</div>
<div class="edge aquan">Rhaan 4</div>
<div class="edge elyria">Nightal 1</div>
<div class="edge selva">Long 1</div>
&nbsp;<br>
&larr; Case <a href="../events/case-11">11</a> (pt <a href="../events/case-11e05">5</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">17</div>
<div class="edge trell">Erastus 18</div>
<div class="edge ignan">Planting 13</div>
<div class="edge aquan">Rhaan 5</div>
<div class="edge elyria">Nightal 2</div>
<div class="edge selva">Long 2</div>
&nbsp;<br>
&larr; Case <a href="../events/case-11">11</a> (pt <a href="../events/case-11e05">5</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">18</div>
<div class="edge trell">Erastus 19</div>
<div class="edge ignan">Planting 14</div>
<div class="edge aquan">Rhaan 6</div>
<div class="edge elyria">Nightal 3</div>
<div class="edge selva">Long 3</div>
&nbsp;<br>
&larr; Case <a href="../events/case-11">11</a> (pt <a href="../events/case-11e05">5</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">19</div>
<div class="edge trell">Erastus 20</div>
<div class="edge ignan">Planting 15</div>
<div class="edge aquan">Rhaan 7</div>
<div class="edge elyria">Nightal 4</div>
<div class="edge selva">Long 4</div>
&nbsp;<br>
&larr; Case <a href="../events/case-11">11</a> (pt <a href="../events/case-11e05">5</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">20</div>
<div class="edge trell">Erastus 21</div>
<div class="edge ignan">Planting 16</div>
<div class="edge aquan">Rhaan 8</div>
<div class="edge elyria">Nightal 5</div>
<div class="edge selva">Long 5</div>
&nbsp;<br>
&larr; Case <a href="../events/case-11">11</a> (pt <a href="../events/case-11e05">5</a>) &rarr;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">21</div>
<div class="edge trell">Erastus 22</div>
<div class="edge ignan">Planting 17</div>
<div class="edge aquan">Rhaan 9</div>
<div class="edge elyria">Nightal 6</div>
<div class="edge selva">Long 6</div>
&nbsp;<br>
Case <a href="../events/case-11">11</a> (pts <a href="../events/case-11e05">5</a>, <a href="../events/case-11e06">6</a>, <a href="../events/case-11e07">7</a>, <a href="../events/case-11e08">8</a>, <a href="../events/case-11e09">9</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">22</div>
<div class="edge trell">Erastus 23</div>
<div class="edge ignan">Planting 18</div>
<div class="edge aquan">Rhaan 10</div>
<div class="edge elyria">Nightal 7</div>
<div class="edge selva">Long 7</div>
&nbsp;<br>
&larr; Case <a href="../events/case-11">11</a> (pt <a href="../events/case-11e09">9</a>) &rarr;<br>
&nbsp;
</td>
<td>
<div class="edge day">23</div>
<div class="edge trell">Erastus 24</div>
<div class="edge ignan">Planting 19</div>
<div class="edge aquan">Rhaan 11</div>
<div class="edge elyria">Nightal 8</div>
<div class="edge selva">Long 8</div>
&nbsp;<br>
&larr; Case <a href="../events/case-11">11</a> (pt <a href="../events/case-11e09">9</a>)<br>
Case <a href="../events/case-12">12</a> (pts <a href="../events/case-12e01">1</a>, <a href="../events/case-12e02">2</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">24</div>
<div class="edge trell">Erastus 25</div>
<div class="edge ignan">Planting 20</div>
<div class="edge aquan">Rhaan 12</div>
<div class="edge elyria">Nightal 9</div>
<div class="edge selva">Long 9</div>
&nbsp;<br>
Case <a href="../events/case-12">12</a> (pts <a href="../events/case-12e02">2</a>, <a href="../events/case-12e03">3</a>, <a href="../events/case-12e04">4</a>, <a href="../events/case-12e05">5</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">25</div>
<div class="edge trell">Erastus 26</div>
<div class="edge ignan">Planting 21</div>
<div class="edge aquan">Rhaan 13</div>
<div class="edge elyria">Nightal 10</div>
<div class="edge selva">Long 10</div>
&nbsp;<br>
Case <a href="../events/case-12">12</a> (pts <a href="../events/case-12e05">5</a>, <a href="../events/case-12e06">6</a>, <a href="../events/case-12e07">7</a>,<br>
<a href="../events/case-12e08">8</a>, <a href="../events/case-12e09">9</a>, <a href="../events/case-12e10">10</a>, <a href="../events/case-12e11">11</a>, <a href="../events/case-12e12">12</a>)<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">26</div>
<div class="edge trell">Erastus 27</div>
<div class="edge ignan">Planting 22</div>
<div class="edge aquan">Rhaan 14</div>
<div class="edge elyria">Nightal 11</div>
<div class="edge selva">Long 11</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">27</div>
<div class="edge trell">Erastus 28</div>
<div class="edge ignan">Planting 23</div>
<div class="edge aquan">Rhaan 15</div>
<div class="edge elyria">Nightal 12</div>
<div class="edge selva">Long 12</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">28</div>
<div class="edge trell">Erastus 29</div>
<div class="edge ignan">Planting 24</div>
<div class="edge aquan">Rhaan 16</div>
<div class="edge elyria">Nightal 13</div>
<div class="edge selva">Long 13</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">29</div>
<div class="edge trell">Erastus 30</div>
<div class="edge ignan">Planting 25</div>
<div class="edge aquan">Rhaan 17</div>
<div class="edge elyria">Nightal 14</div>
<div class="edge selva">Long 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">30</div>
<div class="edge trell">Erastus 31</div>
<div class="edge ignan">Planting 26</div>
<div class="edge aquan">Rhaan 18</div>
<div class="edge elyria">Nightal 15</div>
<div class="edge selva">Long 15</div>
&nbsp;<br>
&nbsp;
</td>
</tr>

<tr class="spacing"><td colspan=5></td></tr>
<tr>
<td style="border: none">&nbsp;</td>
<td colspan=3>
<div class="edge trell">Arodus 1</div>
<div class="edge ignan">Planting 27</div>
<div class="edge aquan">Rhaan 19</div>
<div class="edge elyria">Nightal 16</div>
<div class="edge selva">Long 16</div>
<strong>🌪 Auran Apex</strong><br>
<div class="column">
Spring Equinox (Mountain)<br>
Summer Solstice (Zephyr)
</div>
<div class="column">
Autumn Equinox (Ocean)<br>
Winter Solstice (Elyria)
</div>
<div>
Case <a href="../events/case-13">13</a> (pts <a href="../events/case-13e01">1</a>, <a href="../events/case-13e02">2</a>, <a href="../events/case-13e03">3</a>, <a href="../events/case-13e04">4</a>)<br>
&nbsp;
</div>
</td>
<td style="border: none">&nbsp;</td>
</tr>
<tr class="spacing"><td colspan=5></td></tr>

<tr><th class="month" colspan=5>06 - Vis</th></tr>
<tr>
<td>
<div class="edge day">1</div>
<div class="edge trell">Arodus 2</div>
<div class="edge ignan">Planting 28</div>
<div class="edge aquan">Rhaan 20</div>
<div class="edge elyria">Nightal 17</div>
<div class="edge selva">Long 17</div>
&nbsp;<br>
Case <a href="../events/case-14">14</a> (pt <a href="../events/case-14e00">0</a>) &rarr;<br>
</td>
<td>
<div class="edge day">2</div>
<div class="edge trell">Arodus 3</div>
<div class="edge ignan">Flocktime 1</div>
<div class="edge aquan">Rhaan 21</div>
<div class="edge elyria">Nightal 18</div>
<div class="edge selva">Long 18</div>
&nbsp;<br>
&larr; Case <a href="../events/case-14">14</a> (pt <a href="../events/case-14e00">0</a>)<br>
</td>
<td>
<div class="edge day">3</div>
<div class="edge trell">Arodus 4</div>
<div class="edge ignan">Flocktime 2</div>
<div class="edge aquan">Rhaan 22</div>
<div class="edge elyria">Nightal 19</div>
<div class="edge selva">Long 19</div>
&nbsp;<br>
Case <a href="../events/case-14">14</a> (pts <a href="../events/case-14e01">1</a>, <a href="../events/case-14e02">2</a>, <a href="../events/case-14e03">3</a>, <a href="../events/case-14e04">4</a>, <a href="../events/case-14e05">5</a>)<br>
Case <a href="../events/case-15">15</a> (pt <a href="../events/case-15e00">0</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">4</div>
<div class="edge trell">Arodus 5</div>
<div class="edge ignan">Flocktime 3</div>
<div class="edge aquan">Rhaan 23</div>
<div class="edge elyria">Nightal 20</div>
<div class="edge selva">Long 20</div>
&nbsp;<br>
Case <a href="../events/case-15">15</a> (pts <a href="../events/case-15e01">1</a>, <a href="../events/case-15e02">2</a>,<br>
<a href="../events/case-15e03">3</a>, <a href="../events/case-15e04">4</a>, <a href="../events/case-15e05">5</a>, <a href="../events/case-15e06">6</a>, <a href="../events/case-15e07">7</a>, <a href="../events/case-15e08">8</a>, <a href="../events/case-15e09">9</a>)<br>
</td>
<td>
<div class="edge day">5</div>
<div class="edge trell">Arodus 6</div>
<div class="edge ignan">Flocktime 4</div>
<div class="edge aquan">Rhaan 24</div>
<div class="edge elyria">Nightal 21</div>
<div class="edge selva">Long 21</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">6</div>
<div class="edge trell">Arodus 7</div>
<div class="edge ignan">Flocktime 5</div>
<div class="edge aquan">Rhaan 25</div>
<div class="edge elyria">Nightal 22</div>
<div class="edge selva">Long 22</div>
&nbsp;<br>
Case <a href="../events/case-16">16</a> (pts <a href="../events/case-16e01">1</a>, <a href="../events/case-16e02">2</a>, <a href="../events/case-16e03">3</a>, <a href="../events/case-16e04">4</a>, <a href="../events/case-16e05">5</a>)<br>
&nbsp;
</td>
<td>
<div class="edge day">7</div>
<div class="edge trell">Arodus 8</div>
<div class="edge ignan">Flocktime 6</div>
<div class="edge aquan">Rhaan 26</div>
<div class="edge elyria">Nightal 23</div>
<div class="edge selva">Long 23</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">8</div>
<div class="edge trell">Arodus 9</div>
<div class="edge ignan">Flocktime 7</div>
<div class="edge aquan">Rhaan 27</div>
<div class="edge elyria">Nightal 24</div>
<div class="edge selva">Fated 1</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">9</div>
<div class="edge trell">Arodus 10</div>
<div class="edge ignan">Flocktime 8</div>
<div class="edge aquan">Rhaan 28</div>
<div class="edge elyria">Nightal 25</div>
<div class="edge selva">Fated 2</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">10</div>
<div class="edge trell">Arodus 11</div>
<div class="edge ignan">Flocktime 9</div>
<div class="edge aquan"><strong>Autumnday</strong></div>
<div class="edge elyria">Nightal 26</div>
<div class="edge selva">Fated 3</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">11</div>
<div class="edge trell">Arodus 12</div>
<div class="edge ignan">Flocktime 10</div>
<div class="edge aquan">Sypheros 1</div>
<div class="edge elyria">Nightal 27</div>
<div class="edge selva">Fated 4</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">12</div>
<div class="edge trell">Arodus 13</div>
<div class="edge ignan">Flocktime 11</div>
<div class="edge aquan">Sypheros 2</div>
<div class="edge elyria">Nightal 28</div>
<div class="edge selva">Fated 5</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">13</div>
<div class="edge trell">Arodus 14</div>
<div class="edge ignan">Flocktime 12</div>
<div class="edge aquan">Sypheros 3</div>
<div class="edge elyria">Nightal 29</div>
<div class="edge selva">Fated 6</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">14</div>
<div class="edge trell">Arodus 15</div>
<div class="edge ignan">Flocktime 13</div>
<div class="edge aquan">Sypheros 4</div>
<div class="edge elyria">Nightal 30</div>
<div class="edge selva">Fated 7</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">15</div>
<div class="edge trell">Arodus 16</div>
<div class="edge ignan">Flocktime 14</div>
<div class="edge aquan">Sypheros 5</div>
<div class="edge elyria">Hammer 1</div>
<div class="edge selva">Fated 8</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">16</div>
<div class="edge trell">Arodus 17</div>
<div class="edge ignan">Flocktime 15</div>
<div class="edge aquan">Sypheros 6</div>
<div class="edge elyria">Hammer 2</div>
<div class="edge selva">Fated 9</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">17</div>
<div class="edge trell">Arodus 18</div>
<div class="edge ignan">Flocktime 16</div>
<div class="edge aquan">Sypheros 7</div>
<div class="edge elyria">Hammer 3</div>
<div class="edge selva">Fated 10</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">18</div>
<div class="edge trell">Arodus 19</div>
<div class="edge ignan">Flocktime 17</div>
<div class="edge aquan">Sypheros 8</div>
<div class="edge elyria">Hammer 4</div>
<div class="edge selva">Fated 11</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">19</div>
<div class="edge trell">Arodus 20</div>
<div class="edge ignan">Flocktime 18</div>
<div class="edge aquan">Sypheros 9</div>
<div class="edge elyria">Hammer 5</div>
<div class="edge selva">Fated 12</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">20</div>
<div class="edge trell">Arodus 21</div>
<div class="edge ignan">Flocktime 19</div>
<div class="edge aquan">Sypheros 10</div>
<div class="edge elyria">Hammer 6</div>
<div class="edge selva">Fated 13</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">21</div>
<div class="edge trell">Arodus 22</div>
<div class="edge ignan">Flocktime 20</div>
<div class="edge aquan">Sypheros 11</div>
<div class="edge elyria">Hammer 7</div>
<div class="edge selva">Fated 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">22</div>
<div class="edge trell">Arodus 23</div>
<div class="edge ignan">Flocktime 21</div>
<div class="edge aquan">Sypheros 12</div>
<div class="edge elyria">Hammer 8</div>
<div class="edge selva">Fated 15</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">23</div>
<div class="edge trell">Arodus 24</div>
<div class="edge ignan">Flocktime 22</div>
<div class="edge aquan">Sypheros 13</div>
<div class="edge elyria">Hammer 9</div>
<div class="edge selva">Fated 16</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">24</div>
<div class="edge trell">Arodus 25</div>
<div class="edge ignan">Flocktime 23</div>
<div class="edge aquan">Sypheros 14</div>
<div class="edge elyria">Hammer 10</div>
<div class="edge selva">Fated 17</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">25</div>
<div class="edge trell">Arodus 26</div>
<div class="edge ignan">Flocktime 24</div>
<div class="edge aquan">Sypheros 15</div>
<div class="edge elyria">Hammer 11</div>
<div class="edge selva">Fated 18</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">26</div>
<div class="edge trell">Arodus 27</div>
<div class="edge ignan">Flocktime 25</div>
<div class="edge aquan">Sypheros 16</div>
<div class="edge elyria">Hammer 12</div>
<div class="edge selva">Fated 19</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">27</div>
<div class="edge trell">Arodus 28</div>
<div class="edge ignan">Flocktime 26</div>
<div class="edge aquan">Sypheros 17</div>
<div class="edge elyria">Hammer 13</div>
<div class="edge selva">Fated 20</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">28</div>
<div class="edge trell">Arodus 29</div>
<div class="edge ignan">Flocktime 27</div>
<div class="edge aquan">Sypheros 18</div>
<div class="edge elyria">Hammer 14</div>
<div class="edge selva">Fated 21</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">29</div>
<div class="edge trell">Arodus 30</div>
<div class="edge ignan">Flocktime 28</div>
<div class="edge aquan">Sypheros 19</div>
<div class="edge elyria">Hammer 15</div>
<div class="edge selva">Fated 22</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">30</div>
<div class="edge trell">Arodus 31</div>
<div class="edge ignan">Wealsun 1</div>
<div class="edge aquan">Sypheros 20</div>
<div class="edge elyria">Hammer 16</div>
<div class="edge selva">Fated 23</div>
&nbsp;<br>
&nbsp;
</td>
</tr>

<tr class="spacing"><td colspan=5></td></tr>
<tr>
<td style="border: none">&nbsp;</td>
<td colspan=3>
<div class="edge trell">Rova 1</div>
<div class="edge ignan">Wealsun 2</div>
<div class="edge aquan">Sypheros 21</div>
<div class="edge elyria">Hammer 17</div>
<div class="edge selva">Birth 1</div>
<strong>⏳ Arenan Apex</strong><br>
<div class="column">
Spring Equinox (Selva)<br>
Summer Solstice (RUP)
</div>
<div class="column">
Autumn Equinox (Trell)<br>
Winter Solstice (Arallu)
</div>
<div>
&nbsp;
</div>
</td>
<td style="border: none">&nbsp;</td>
</tr>
<tr class="spacing"><td colspan=5></td></tr>

<tr><th class="month" colspan=5>07 - Avium</th></tr>
<tr>
<td>
<div class="edge day">1</div>
<div class="edge trell">Rova 2</div>
<div class="edge ignan">Wealsun 3</div>
<div class="edge aquan">Sypheros 22</div>
<div class="edge elyria">Hammer 18</div>
<div class="edge selva">Birth 2</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">2</div>
<div class="edge trell">Rova 3</div>
<div class="edge ignan">Wealsun 4</div>
<div class="edge aquan">Sypheros 23</div>
<div class="edge elyria">Hammer 19</div>
<div class="edge selva">Birth 3</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">3</div>
<div class="edge trell">Rova 4</div>
<div class="edge ignan">Wealsun 5</div>
<div class="edge aquan">Sypheros 24</div>
<div class="edge elyria">Hammer 20</div>
<div class="edge selva">Birth 4</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">4</div>
<div class="edge trell">Rova 5</div>
<div class="edge ignan">Wealsun 6</div>
<div class="edge aquan">Sypheros 25</div>
<div class="edge elyria">Hammer 21</div>
<div class="edge selva">Birth 5</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">5</div>
<div class="edge trell">Rova 6</div>
<div class="edge ignan">Wealsun 7</div>
<div class="edge aquan">Sypheros 26</div>
<div class="edge elyria">Hammer 22</div>
<div class="edge selva">Birth 6</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">6</div>
<div class="edge trell">Rova 7</div>
<div class="edge ignan">Wealsun 8</div>
<div class="edge aquan">Sypheros 27</div>
<div class="edge elyria">Hammer 23</div>
<div class="edge selva">Birth 7</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">7</div>
<div class="edge trell">Rova 8</div>
<div class="edge ignan">Wealsun 9</div>
<div class="edge aquan">Sypheros 28</div>
<div class="edge elyria">Hammer 24</div>
<div class="edge selva">Birth 8</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">8</div>
<div class="edge trell">Rova 9</div>
<div class="edge ignan">Wealsun 10</div>
<div class="edge aquan">Aryth 1</div>
<div class="edge elyria">Hammer 25</div>
<div class="edge selva">Birth 9</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">9</div>
<div class="edge trell">Rova 10</div>
<div class="edge ignan">Wealsun 11</div>
<div class="edge aquan">Aryth 2</div>
<div class="edge elyria">Hammer 26</div>
<div class="edge selva">Birth 10</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">10</div>
<div class="edge trell">Rova 11</div>
<div class="edge ignan">Wealsun 12</div>
<div class="edge aquan">Aryth 3</div>
<div class="edge elyria">Hammer 27</div>
<div class="edge selva">Birth 11</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">11</div>
<div class="edge trell">Rova 12</div>
<div class="edge ignan">Wealsun 13</div>
<div class="edge aquan">Aryth 4</div>
<div class="edge elyria">Hammer 28</div>
<div class="edge selva">Birth 12</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">12</div>
<div class="edge trell">Rova 13</div>
<div class="edge ignan">Wealsun 14</div>
<div class="edge aquan">Aryth 5</div>
<div class="edge elyria">Hammer 29</div>
<div class="edge selva">Birth 13</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">13</div>
<div class="edge trell">Rova 14</div>
<div class="edge ignan">Wealsun 15</div>
<div class="edge aquan">Aryth 6</div>
<div class="edge elyria">Hammer 30</div>
<div class="edge selva">Birth 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">14</div>
<div class="edge trell">Rova 15</div>
<div class="edge ignan">Wealsun 16</div>
<div class="edge aquan">Aryth 7</div>
<div class="edge elyria"><strong>Midwinter</strong></div>
<div class="edge selva">Birth 15</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">15</div>
<div class="edge trell">Rova 16</div>
<div class="edge ignan">Wealsun 17</div>
<div class="edge aquan">Aryth 8</div>
<div class="edge elyria">Alturiak 1</div>
<div class="edge selva">Birth 16</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">16</div>
<div class="edge trell">Rova 17</div>
<div class="edge ignan">Wealsun 18</div>
<div class="edge aquan">Aryth 9</div>
<div class="edge elyria">Alturiak 2</div>
<div class="edge selva">Birth 17</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">17</div>
<div class="edge trell">Rova 18</div>
<div class="edge ignan">Wealsun 19</div>
<div class="edge aquan">Aryth 10</div>
<div class="edge elyria">Alturiak 3</div>
<div class="edge selva">Birth 18</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">18</div>
<div class="edge trell">Rova 19</div>
<div class="edge ignan">Wealsun 20</div>
<div class="edge aquan">Aryth 11</div>
<div class="edge elyria">Alturiak 4</div>
<div class="edge selva">Birth 19</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">19</div>
<div class="edge trell">Rova 20</div>
<div class="edge ignan">Wealsun 21</div>
<div class="edge aquan">Aryth 12</div>
<div class="edge elyria">Alturiak 5</div>
<div class="edge selva">Birth 20</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">20</div>
<div class="edge trell">Rova 21</div>
<div class="edge ignan">Wealsun 22</div>
<div class="edge aquan">Aryth 13</div>
<div class="edge elyria">Alturiak 6</div>
<div class="edge selva">Birth 21</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">21</div>
<div class="edge trell">Rova 22</div>
<div class="edge ignan">Wealsun 23</div>
<div class="edge aquan">Aryth 14</div>
<div class="edge elyria">Alturiak 7</div>
<div class="edge selva">Birth 22</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">22</div>
<div class="edge trell">Rova 23</div>
<div class="edge ignan">Wealsun 24</div>
<div class="edge aquan">Aryth 15</div>
<div class="edge elyria">Alturiak 8</div>
<div class="edge selva">Birth 23</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">23</div>
<div class="edge trell">Rova 24</div>
<div class="edge ignan">Wealsun 25</div>
<div class="edge aquan">Aryth 16</div>
<div class="edge elyria">Alturiak 9</div>
<div class="edge selva">Rain 1</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">24</div>
<div class="edge trell">Rova 25</div>
<div class="edge ignan">Wealsun 26</div>
<div class="edge aquan">Aryth 17</div>
<div class="edge elyria">Alturiak 10</div>
<div class="edge selva">Rain 2</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">25</div>
<div class="edge trell">Rova 26</div>
<div class="edge ignan">Wealsun 27</div>
<div class="edge aquan">Aryth 18</div>
<div class="edge elyria">Alturiak 11</div>
<div class="edge selva">Rain 3</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">26</div>
<div class="edge trell">Rova 27</div>
<div class="edge ignan">Wealsun 28</div>
<div class="edge aquan">Aryth 19</div>
<div class="edge elyria">Alturiak 12</div>
<div class="edge selva">Rain 4</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">27</div>
<div class="edge trell">Rova 28</div>
<div class="edge ignan"><em>Richfest 1</em></div>
<div class="edge aquan">Aryth 20</div>
<div class="edge elyria">Alturiak 13</div>
<div class="edge selva">Rain 5</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">28</div>
<div class="edge trell">Rova 29</div>
<div class="edge ignan"><em>Richfest 2</em></div>
<div class="edge aquan">Aryth 21</div>
<div class="edge elyria">Alturiak 14</div>
<div class="edge selva">Rain 6</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">29</div>
<div class="edge trell">Rova 30</div>
<div class="edge ignan"><em>Richfest 3</em></div>
<div class="edge aquan">Aryth 22</div>
<div class="edge elyria">Alturiak 15</div>
<div class="edge selva">Rain 7</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">30</div>
<div class="edge trell">Lamashan 1</div>
<div class="edge ignan"><em>Richfest 4</em></div>
<div class="edge aquan">Aryth 23</div>
<div class="edge elyria">Alturiak 16</div>
<div class="edge selva">Rain 8</div>
&nbsp;<br>
🌕 Full Moon<br>
Ignan Moonpeak<br>
&nbsp;
</td>
</tr>

<tr class="spacing"><td colspan=5></td></tr>

<tr><th class="month" colspan=5>08 - Luna</th></tr>
<tr>
<td>
<div class="edge day">1</div>
<div class="edge trell">Lamashan 2</div>
<div class="edge ignan"><em>Richfest 5</em></div>
<div class="edge aquan">Aryth 24</div>
<div class="edge elyria">Alturiak 17</div>
<div class="edge selva">Rain 9</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">2</div>
<div class="edge trell">Lamashan 3</div>
<div class="edge ignan"><em>Richfest 6</em></div>
<div class="edge aquan">Aryth 25</div>
<div class="edge elyria">Alturiak 18</div>
<div class="edge selva">Rain 10</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">3</div>
<div class="edge trell">Lamashan 4</div>
<div class="edge ignan"><em>Richfest 7</em></div>
<div class="edge aquan">Aryth 26</div>
<div class="edge elyria">Alturiak 19</div>
<div class="edge selva">Rain 11</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">4</div>
<div class="edge trell">Lamashan 5</div>
<div class="edge ignan"><em>Richfest 8</em></div>
<div class="edge aquan">Aryth 27</div>
<div class="edge elyria">Alturiak 20</div>
<div class="edge selva">Rain 12</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">5</div>
<div class="edge trell">Lamashan 6</div>
<div class="edge ignan">Reaping 1</div>
<div class="edge aquan">Aryth 28</div>
<div class="edge elyria">Alturiak 21</div>
<div class="edge selva">Rain 13</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">6</div>
<div class="edge trell">Lamashan 7</div>
<div class="edge ignan">Reaping 2</div>
<div class="edge aquan">Vult 1</div>
<div class="edge elyria">Alturiak 22</div>
<div class="edge selva">Rain 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">7</div>
<div class="edge trell">Lamashan 8</div>
<div class="edge ignan">Reaping 3</div>
<div class="edge aquan">Vult 2</div>
<div class="edge elyria">Alturiak 23</div>
<div class="edge selva">Rain 15</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">8</div>
<div class="edge trell">Lamashan 9</div>
<div class="edge ignan">Reaping 4</div>
<div class="edge aquan">Vult 3</div>
<div class="edge elyria">Alturiak 24</div>
<div class="edge selva">Rain 16</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">9</div>
<div class="edge trell">Lamashan 10</div>
<div class="edge ignan">Reaping 5</div>
<div class="edge aquan">Vult 4</div>
<div class="edge elyria">Alturiak 25</div>
<div class="edge selva">Rain 17</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">10</div>
<div class="edge trell">Lamashan 11</div>
<div class="edge ignan">Reaping 6</div>
<div class="edge aquan">Vult 5</div>
<div class="edge elyria">Alturiak 26</div>
<div class="edge selva">Rain 18</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">11</div>
<div class="edge trell">Lamashan 12</div>
<div class="edge ignan">Reaping 7</div>
<div class="edge aquan">Vult 6</div>
<div class="edge elyria">Alturiak 27</div>
<div class="edge selva">Rain 19</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">12</div>
<div class="edge trell">Lamashan 13</div>
<div class="edge ignan">Reaping 8</div>
<div class="edge aquan">Vult 7</div>
<div class="edge elyria">Alturiak 28</div>
<div class="edge selva">Rain 20</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">13</div>
<div class="edge trell">Lamashan 14</div>
<div class="edge ignan">Reaping 9</div>
<div class="edge aquan">Vult 8</div>
<div class="edge elyria">Alturiak 29</div>
<div class="edge selva">Rain 21</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">14</div>
<div class="edge trell">Lamashan 15</div>
<div class="edge ignan">Reaping 10</div>
<div class="edge aquan">Vult 9</div>
<div class="edge elyria">Alturiak 30</div>
<div class="edge selva">Rain 22</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">15</div>
<div class="edge trell">Lamashan 16</div>
<div class="edge ignan">Reaping 11</div>
<div class="edge aquan">Vult 10</div>
<div class="edge elyria"><strong>Dokkalfar</strong></div>
<div class="edge selva">Rain 23</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">16</div>
<div class="edge trell">Lamashan 17</div>
<div class="edge ignan">Reaping 12</div>
<div class="edge aquan">Vult 11</div>
<div class="edge elyria">Ches 1</div>
<div class="edge selva">Storm 1</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">17</div>
<div class="edge trell">Lamashan 18</div>
<div class="edge ignan">Reaping 13</div>
<div class="edge aquan">Vult 12</div>
<div class="edge elyria">Ches 2</div>
<div class="edge selva">Storm 2</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">18</div>
<div class="edge trell">Lamashan 19</div>
<div class="edge ignan">Reaping 14</div>
<div class="edge aquan">Vult 13</div>
<div class="edge elyria">Ches 3</div>
<div class="edge selva">Storm 3</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">19</div>
<div class="edge trell">Lamashan 20</div>
<div class="edge ignan">Reaping 15</div>
<div class="edge aquan">Vult 14</div>
<div class="edge elyria">Ches 4</div>
<div class="edge selva">Storm 4</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">20</div>
<div class="edge trell">Lamashan 21</div>
<div class="edge ignan">Reaping 16</div>
<div class="edge aquan">Vult 15</div>
<div class="edge elyria">Ches 5</div>
<div class="edge selva">Storm 5</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">21</div>
<div class="edge trell">Lamashan 22</div>
<div class="edge ignan">Reaping 17</div>
<div class="edge aquan">Vult 16</div>
<div class="edge elyria">Ches 6</div>
<div class="edge selva">Storm 6</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">22</div>
<div class="edge trell">Lamashan 23</div>
<div class="edge ignan">Reaping 18</div>
<div class="edge aquan">Vult 17</div>
<div class="edge elyria">Ches 7</div>
<div class="edge selva">Storm 7</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">23</div>
<div class="edge trell">Lamashan 24</div>
<div class="edge ignan">Reaping 19</div>
<div class="edge aquan">Vult 18</div>
<div class="edge elyria">Ches 8</div>
<div class="edge selva">Storm 8</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">24</div>
<div class="edge trell">Lamashan 25</div>
<div class="edge ignan">Reaping 20</div>
<div class="edge aquan">Vult 19</div>
<div class="edge elyria">Ches 9</div>
<div class="edge selva">Storm 9</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">25</div>
<div class="edge trell">Lamashan 26</div>
<div class="edge ignan">Reaping 21</div>
<div class="edge aquan">Vult 20</div>
<div class="edge elyria">Ches 10</div>
<div class="edge selva">Storm 10</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">26</div>
<div class="edge trell">Lamashan 27</div>
<div class="edge ignan">Reaping 22</div>
<div class="edge aquan">Vult 21</div>
<div class="edge elyria">Ches 11</div>
<div class="edge selva">Storm 11</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">27</div>
<div class="edge trell">Lamashan 28</div>
<div class="edge ignan">Reaping 23</div>
<div class="edge aquan">Vult 22</div>
<div class="edge elyria">Ches 12</div>
<div class="edge selva">Storm 12</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">28</div>
<div class="edge trell">Lamashan 29</div>
<div class="edge ignan">Reaping 24</div>
<div class="edge aquan">Vult 23</div>
<div class="edge elyria">Ches 13</div>
<div class="edge selva">Storm 13</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">29</div>
<div class="edge trell">Lamashan 30</div>
<div class="edge ignan">Reaping 25</div>
<div class="edge aquan">Vult 24</div>
<div class="edge elyria">Ches 14</div>
<div class="edge selva">Storm 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">30</div>
<div class="edge trell">Lamashan 31</div>
<div class="edge ignan">Reaping 26</div>
<div class="edge aquan">Vult 25</div>
<div class="edge elyria">Ches 15</div>
<div class="edge selva">Storm 15</div>
&nbsp;<br>
&nbsp;
</td>
</tr>

<tr class="spacing"><td colspan=5></td></tr>
<tr>
<td style="border: none">&nbsp;</td>
<td colspan=3>
<div class="edge trell">Neth 1</div>
<div class="edge ignan">Reaping 27</div>
<div class="edge aquan">Vult 26</div>
<div class="edge elyria">Ches 16</div>
<div class="edge selva">Storm 16</div>
<strong>🔥 Ignan Apex</strong><br>
<div class="column">
Spring Equinox (Elyria)<br>
Summer Solstice (Mountain)
</div>
<div class="column">
Autumn Equinox (Zephyr)<br>
Winter Solstice (Ocean)
</div>
<div>
&nbsp;
</div>
</td>
<td style="border: none">&nbsp;</td>
</tr>
<tr class="spacing"><td colspan=5></td></tr>

<tr><th class="month" colspan=5>09 - Casus</th></tr>
<tr>
<td>
<div class="edge day">1</div>
<div class="edge trell">Neth 2</div>
<div class="edge ignan">Reaping 28</div>
<div class="edge aquan">Vult 27</div>
<div class="edge elyria">Ches 17</div>
<div class="edge selva">Storm 17</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">2</div>
<div class="edge trell">Neth 3</div>
<div class="edge ignan">Goodmonth 1</div>
<div class="edge aquan">Vult 28</div>
<div class="edge elyria">Ches 18</div>
<div class="edge selva">Storm 18</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">3</div>
<div class="edge trell">Neth 4</div>
<div class="edge ignan">Goodmonth 2</div>
<div class="edge aquan"><strong>Winterday</strong></div>
<div class="edge elyria">Ches 19</div>
<div class="edge selva">Storm 19</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">4</div>
<div class="edge trell">Neth 5</div>
<div class="edge ignan">Goodmonth 3</div>
<div class="edge aquan">Xendrik 1</div>
<div class="edge elyria">Ches 20</div>
<div class="edge selva">Storm 20</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">5</div>
<div class="edge trell">Neth 6</div>
<div class="edge ignan">Goodmonth 4</div>
<div class="edge aquan">Xendrik 2</div>
<div class="edge elyria">Ches 21</div>
<div class="edge selva">Storm 21</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">6</div>
<div class="edge trell">Neth 7</div>
<div class="edge ignan">Goodmonth 5</div>
<div class="edge aquan">Xendrik 3</div>
<div class="edge elyria">Ches 22</div>
<div class="edge selva">Storm 22</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">7</div>
<div class="edge trell">Neth 8</div>
<div class="edge ignan">Goodmonth 6</div>
<div class="edge aquan">Xendrik 4</div>
<div class="edge elyria">Ches 23</div>
<div class="edge selva">Storm 23</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">8</div>
<div class="edge trell">Neth 9</div>
<div class="edge ignan">Goodmonth 7</div>
<div class="edge aquan">Xendrik 5</div>
<div class="edge elyria">Ches 24</div>
<div class="edge selva">Flood 1</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">9</div>
<div class="edge trell">Neth 10</div>
<div class="edge ignan">Goodmonth 8</div>
<div class="edge aquan">Xendrik 6</div>
<div class="edge elyria">Ches 25</div>
<div class="edge selva">Flood 2</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">10</div>
<div class="edge trell">Neth 11</div>
<div class="edge ignan">Goodmonth 9</div>
<div class="edge aquan">Xendrik 7</div>
<div class="edge elyria">Ches 26</div>
<div class="edge selva">Flood 3</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">11</div>
<div class="edge trell">Neth 12</div>
<div class="edge ignan">Goodmonth 10</div>
<div class="edge aquan">Xendrik 8</div>
<div class="edge elyria">Ches 27</div>
<div class="edge selva">Flood 4</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">12</div>
<div class="edge trell">Neth 13</div>
<div class="edge ignan">Goodmonth 11</div>
<div class="edge aquan">Xendrik 9</div>
<div class="edge elyria">Ches 28</div>
<div class="edge selva">Flood 5</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">13</div>
<div class="edge trell">Neth 14</div>
<div class="edge ignan">Goodmonth 12</div>
<div class="edge aquan">Xendrik 10</div>
<div class="edge elyria">Ches 29</div>
<div class="edge selva">Flood 6</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">14</div>
<div class="edge trell">Neth 15</div>
<div class="edge ignan">Goodmonth 13</div>
<div class="edge aquan">Xendrik 11</div>
<div class="edge elyria">Ches 30</div>
<div class="edge selva">Flood 7</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">15</div>
<div class="edge trell">Neth 16</div>
<div class="edge ignan">Goodmonth 14</div>
<div class="edge aquan">Xendrik 12</div>
<div class="edge elyria">Tarsakh 1</div>
<div class="edge selva">Flood 8</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">16</div>
<div class="edge trell">Neth 17</div>
<div class="edge ignan">Goodmonth 15</div>
<div class="edge aquan">Xendrik 13</div>
<div class="edge elyria">Tarsakh 2</div>
<div class="edge selva">Flood 9</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">17</div>
<div class="edge trell">Neth 18</div>
<div class="edge ignan">Goodmonth 16</div>
<div class="edge aquan">Xendrik 14</div>
<div class="edge elyria">Tarsakh 3</div>
<div class="edge selva">Flood 10</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">18</div>
<div class="edge trell">Neth 19</div>
<div class="edge ignan">Goodmonth 17</div>
<div class="edge aquan">Xendrik 15</div>
<div class="edge elyria">Tarsakh 4</div>
<div class="edge selva">Flood 11</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">19</div>
<div class="edge trell">Neth 20</div>
<div class="edge ignan">Goodmonth 18</div>
<div class="edge aquan">Xendrik 16</div>
<div class="edge elyria">Tarsakh 5</div>
<div class="edge selva">Flood 12</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">20</div>
<div class="edge trell">Neth 21</div>
<div class="edge ignan">Goodmonth 19</div>
<div class="edge aquan">Xendrik 17</div>
<div class="edge elyria">Tarsakh 6</div>
<div class="edge selva">Flood 13</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">21</div>
<div class="edge trell">Neth 22</div>
<div class="edge ignan">Goodmonth 20</div>
<div class="edge aquan">Xendrik 18</div>
<div class="edge elyria">Tarsakh 7</div>
<div class="edge selva">Flood 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">22</div>
<div class="edge trell">Neth 23</div>
<div class="edge ignan">Goodmonth 21</div>
<div class="edge aquan">Xendrik 19</div>
<div class="edge elyria">Tarsakh 8</div>
<div class="edge selva">Flood 15</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">23</div>
<div class="edge trell">Neth 24</div>
<div class="edge ignan">Goodmonth 22</div>
<div class="edge aquan">Xendrik 20</div>
<div class="edge elyria">Tarsakh 9</div>
<div class="edge selva">Flood 16</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">24</div>
<div class="edge trell">Neth 25</div>
<div class="edge ignan">Goodmonth 23</div>
<div class="edge aquan">Xendrik 21</div>
<div class="edge elyria">Tarsakh 10</div>
<div class="edge selva">Flood 17</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">25</div>
<div class="edge trell">Neth 26</div>
<div class="edge ignan">Goodmonth 24</div>
<div class="edge aquan">Xendrik 22</div>
<div class="edge elyria">Tarsakh 11</div>
<div class="edge selva">Flood 18</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">26</div>
<div class="edge trell">Neth 27</div>
<div class="edge ignan">Goodmonth 25</div>
<div class="edge aquan">Xendrik 23</div>
<div class="edge elyria">Tarsakh 12</div>
<div class="edge selva">Flood 19</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">27</div>
<div class="edge trell">Neth 28</div>
<div class="edge ignan">Goodmonth 26</div>
<div class="edge aquan">Xendrik 24</div>
<div class="edge elyria">Tarsakh 13</div>
<div class="edge selva">Flood 20</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">28</div>
<div class="edge trell">Neth 29</div>
<div class="edge ignan">Goodmonth 27</div>
<div class="edge aquan">Xendrik 25</div>
<div class="edge elyria">Tarsakh 14</div>
<div class="edge selva">Flood 21</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">29</div>
<div class="edge trell">Neth 30</div>
<div class="edge ignan">Goodmonth 28</div>
<div class="edge aquan">Xendrik 26</div>
<div class="edge elyria">Tarsakh 15</div>
<div class="edge selva">Flood 22</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">30</div>
<div class="edge trell">Kuthona 1</div>
<div class="edge ignan">Harvester 1</div>
<div class="edge aquan">Xendrik 27</div>
<div class="edge elyria">Tarsakh 16</div>
<div class="edge selva">Flood 23</div>
&nbsp;<br>
🌗 Waning Half-Moon<br>
&nbsp;
</td>
</tr>

<tr class="spacing"><td colspan=5></td></tr>

<tr><th class="month" colspan=5>10 - Fatum</th></tr>
<tr>
<td>
<div class="edge day">1</div>
<div class="edge trell">Kuthona 2</div>
<div class="edge ignan">Harvester 2</div>
<div class="edge aquan">Xendrik 28</div>
<div class="edge elyria">Tarsakh 17</div>
<div class="edge selva">Growth 1</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">2</div>
<div class="edge trell">Kuthona 3</div>
<div class="edge ignan">Harvester 3</div>
<div class="edge aquan">Zarantyr 1</div>
<div class="edge elyria">Tarsakh 18</div>
<div class="edge selva">Growth 2</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">3</div>
<div class="edge trell">Kuthona 4</div>
<div class="edge ignan">Harvester 4</div>
<div class="edge aquan">Zarantyr 2</div>
<div class="edge elyria">Tarsakh 19</div>
<div class="edge selva">Growth 3</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">4</div>
<div class="edge trell">Kuthona 5</div>
<div class="edge ignan">Harvester 5</div>
<div class="edge aquan">Zarantyr 3</div>
<div class="edge elyria">Tarsakh 20</div>
<div class="edge selva">Growth 4</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">5</div>
<div class="edge trell">Kuthona 6</div>
<div class="edge ignan">Harvester 6</div>
<div class="edge aquan">Zarantyr 4</div>
<div class="edge elyria">Tarsakh 21</div>
<div class="edge selva">Growth 5</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">6</div>
<div class="edge trell">Kuthona 7</div>
<div class="edge ignan">Harvester 7</div>
<div class="edge aquan">Zarantyr 5</div>
<div class="edge elyria">Tarsakh 22</div>
<div class="edge selva">Growth 6</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">7</div>
<div class="edge trell">Kuthona 8</div>
<div class="edge ignan">Harvester 8</div>
<div class="edge aquan">Zarantyr 6</div>
<div class="edge elyria">Tarsakh 23</div>
<div class="edge selva">Growth 7</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">8</div>
<div class="edge trell">Kuthona 9</div>
<div class="edge ignan">Harvester 9</div>
<div class="edge aquan">Zarantyr 7</div>
<div class="edge elyria">Tarsakh 24</div>
<div class="edge selva">Growth 8</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">9</div>
<div class="edge trell">Kuthona 10</div>
<div class="edge ignan">Harvester 10</div>
<div class="edge aquan">Zarantyr 8</div>
<div class="edge elyria">Tarsakh 25</div>
<div class="edge selva">Growth 9</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">10</div>
<div class="edge trell">Kuthona 11</div>
<div class="edge ignan">Harvester 11</div>
<div class="edge aquan">Zarantyr 9</div>
<div class="edge elyria">Tarsakh 26</div>
<div class="edge selva">Growth 10</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">11</div>
<div class="edge trell">Kuthona 12</div>
<div class="edge ignan">Harvester 12</div>
<div class="edge aquan">Zarantyr 10</div>
<div class="edge elyria">Tarsakh 27</div>
<div class="edge selva">Growth 11</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">12</div>
<div class="edge trell">Kuthona 13</div>
<div class="edge ignan">Harvester 13</div>
<div class="edge aquan">Zarantyr 11</div>
<div class="edge elyria">Tarsakh 28</div>
<div class="edge selva">Growth 12</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">13</div>
<div class="edge trell">Kuthona 14</div>
<div class="edge ignan">Harvester 14</div>
<div class="edge aquan">Zarantyr 12</div>
<div class="edge elyria">Tarsakh 29</div>
<div class="edge selva">Growth 13</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">14</div>
<div class="edge trell">Kuthona 15</div>
<div class="edge ignan">Harvester 15</div>
<div class="edge aquan">Zarantyr 13</div>
<div class="edge elyria">Tarsakh 30</div>
<div class="edge selva">Growth 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">15</div>
<div class="edge trell">Kuthona 16</div>
<div class="edge ignan">Harvester 16</div>
<div class="edge aquan">Zarantyr 14</div>
<div class="edge elyria"><strong>Greengrass</strong></div>
<div class="edge selva">Growth 15</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">16</div>
<div class="edge trell">Kuthona 17</div>
<div class="edge ignan">Harvester 17</div>
<div class="edge aquan">Zarantyr 15</div>
<div class="edge elyria">Mirtul 1</div>
<div class="edge selva">Growth 16</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">17</div>
<div class="edge trell">Kuthona 18</div>
<div class="edge ignan">Harvester 18</div>
<div class="edge aquan">Zarantyr 16</div>
<div class="edge elyria">Mirtul 2</div>
<div class="edge selva">Growth 17</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">18</div>
<div class="edge trell">Kuthona 19</div>
<div class="edge ignan">Harvester 19</div>
<div class="edge aquan">Zarantyr 17</div>
<div class="edge elyria">Mirtul 3</div>
<div class="edge selva">Growth 18</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">19</div>
<div class="edge trell">Kuthona 20</div>
<div class="edge ignan">Harvester 20</div>
<div class="edge aquan">Zarantyr 18</div>
<div class="edge elyria">Mirtul 4</div>
<div class="edge selva">Growth 19</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">20</div>
<div class="edge trell">Kuthona 21</div>
<div class="edge ignan">Harvester 21</div>
<div class="edge aquan">Zarantyr 19</div>
<div class="edge elyria">Mirtul 5</div>
<div class="edge selva">Growth 20</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">21</div>
<div class="edge trell">Kuthona 22</div>
<div class="edge ignan">Harvester 22</div>
<div class="edge aquan">Zarantyr 20</div>
<div class="edge elyria">Mirtul 6</div>
<div class="edge selva">Growth 21</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">22</div>
<div class="edge trell">Kuthona 23</div>
<div class="edge ignan">Harvester 23</div>
<div class="edge aquan">Zarantyr 21</div>
<div class="edge elyria">Mirtul 7</div>
<div class="edge selva">Growth 22</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">23</div>
<div class="edge trell">Kuthona 24</div>
<div class="edge ignan">Harvester 24</div>
<div class="edge aquan">Zarantyr 22</div>
<div class="edge elyria">Mirtul 8</div>
<div class="edge selva">Growth 23</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">24</div>
<div class="edge trell">Kuthona 25</div>
<div class="edge ignan">Harvester 25</div>
<div class="edge aquan">Zarantyr 23</div>
<div class="edge elyria">Mirtul 9</div>
<div class="edge selva">Bloom 1</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">25</div>
<div class="edge trell">Kuthona 26</div>
<div class="edge ignan">Harvester 26</div>
<div class="edge aquan">Zarantyr 24</div>
<div class="edge elyria">Mirtul 10</div>
<div class="edge selva">Bloom 2</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">26</div>
<div class="edge trell">Kuthona 27</div>
<div class="edge ignan">Harvester 27</div>
<div class="edge aquan">Zarantyr 25</div>
<div class="edge elyria">Mirtul 11</div>
<div class="edge selva">Bloom 3</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">27</div>
<div class="edge trell">Kuthona 28</div>
<div class="edge ignan">Harvester 28</div>
<div class="edge aquan">Zarantyr 26</div>
<div class="edge elyria">Mirtul 12</div>
<div class="edge selva">Bloom 4</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">28</div>
<div class="edge trell">Kuthona 29</div>
<div class="edge ignan"><em>Brewfest 1</em></div>
<div class="edge aquan">Zarantyr 27</div>
<div class="edge elyria">Mirtul 13</div>
<div class="edge selva">Bloom 5</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">29</div>
<div class="edge trell">Kuthona 30</div>
<div class="edge ignan"><em>Brewfest 2</em></div>
<div class="edge aquan">Zarantyr 28</div>
<div class="edge elyria">Mirtul 14</div>
<div class="edge selva">Bloom 6</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">30</div>
<div class="edge trell">Kuthona 31</div>
<div class="edge ignan"><em>Brewfest 3</em></div>
<div class="edge aquan">Olarune 1</div>
<div class="edge elyria">Mirtul 15</div>
<div class="edge selva">Bloom 7</div>
&nbsp;<br>
&nbsp;
</td>
</tr>

<tr class="spacing"><td colspan=5></td></tr>
<tr>
<td style="border: none">&nbsp;</td>
<td colspan=3>
<div class="edge trell"><strong>Ursa</strong></div>
<div class="edge ignan"><em>Brewfest 4</em></div>
<div class="edge aquan">Olarune 2</div>
<div class="edge elyria">Mirtul 16</div>
<div class="edge selva">Bloom 8</div>
<strong>🌋 Magman Apex</strong><br>
<div class="column">
Spring Equinox (Arallu)<br>
Summer Solstice (Selva)
</div>
<div class="column">
Autumn Equinox (RUP)<br>
Winter Solstice (Trell)
</div>
<div>
Ignan Feastday<br>
&nbsp;
</div>
</td>
<td style="border: none">&nbsp;</td>
</tr>
<tr class="spacing"><td colspan=5></td></tr>

<tr><th class="month" colspan=5>11 - Mysteria</th></tr>
<tr>
<td>
<div class="edge day">1</div>
<div class="edge trell">Abadius 1</div>
<div class="edge ignan"><em>Brewfest 5</em></div>
<div class="edge aquan">Olarune 3</div>
<div class="edge elyria">Mirtul 17</div>
<div class="edge selva">Bloom 9</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">2</div>
<div class="edge trell">Abadius 2</div>
<div class="edge ignan"><em>Brewfest 6</em></div>
<div class="edge aquan">Olarune 4</div>
<div class="edge elyria">Mirtul 18</div>
<div class="edge selva">Bloom 10</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">3</div>
<div class="edge trell">Abadius 3</div>
<div class="edge ignan"><em>Brewfest 7</em></div>
<div class="edge aquan">Olarune 5</div>
<div class="edge elyria">Mirtul 19</div>
<div class="edge selva">Bloom 11</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">4</div>
<div class="edge trell">Abadius 4</div>
<div class="edge ignan"><em>Brewfest 8</em></div>
<div class="edge aquan">Olarune 6</div>
<div class="edge elyria">Mirtul 20</div>
<div class="edge selva">Bloom 12</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">5</div>
<div class="edge trell">Abadius 5</div>
<div class="edge ignan">Patchwall 1</div>
<div class="edge aquan">Olarune 7</div>
<div class="edge elyria">Mirtul 21</div>
<div class="edge selva">Bloom 13</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">6</div>
<div class="edge trell">Abadius 6</div>
<div class="edge ignan">Patchwall 2</div>
<div class="edge aquan">Olarune 8</div>
<div class="edge elyria">Mirtul 22</div>
<div class="edge selva">Bloom 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">7</div>
<div class="edge trell">Abadius 7</div>
<div class="edge ignan">Patchwall 3</div>
<div class="edge aquan">Olarune 9</div>
<div class="edge elyria">Mirtul 23</div>
<div class="edge selva">Bloom 15</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">8</div>
<div class="edge trell">Abadius 8</div>
<div class="edge ignan">Patchwall 4</div>
<div class="edge aquan">Olarune 10</div>
<div class="edge elyria">Mirtul 24</div>
<div class="edge selva">Bloom 16</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">9</div>
<div class="edge trell">Abadius 9</div>
<div class="edge ignan">Patchwall 5</div>
<div class="edge aquan">Olarune 11</div>
<div class="edge elyria">Mirtul 25</div>
<div class="edge selva">Bloom 17</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">10</div>
<div class="edge trell">Abadius 10</div>
<div class="edge ignan">Patchwall 6</div>
<div class="edge aquan">Olarune 12</div>
<div class="edge elyria">Mirtul 26</div>
<div class="edge selva">Bloom 18</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">11</div>
<div class="edge trell">Abadius 11</div>
<div class="edge ignan">Patchwall 7</div>
<div class="edge aquan">Olarune 13</div>
<div class="edge elyria">Mirtul 27</div>
<div class="edge selva">Bloom 19</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">12</div>
<div class="edge trell">Abadius 12</div>
<div class="edge ignan">Patchwall 8</div>
<div class="edge aquan">Olarune 14</div>
<div class="edge elyria">Mirtul 28</div>
<div class="edge selva">Bloom 20</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">13</div>
<div class="edge trell">Abadius 13</div>
<div class="edge ignan">Patchwall 9</div>
<div class="edge aquan">Olarune 15</div>
<div class="edge elyria">Mirtul 29</div>
<div class="edge selva">Bloom 21</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">14</div>
<div class="edge trell">Abadius 14</div>
<div class="edge ignan">Patchwall 10</div>
<div class="edge aquan">Olarune 16</div>
<div class="edge elyria">Mirtul 30</div>
<div class="edge selva">Bloom 22</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">15</div>
<div class="edge trell">Abadius 15</div>
<div class="edge ignan">Patchwall 11</div>
<div class="edge aquan">Olarune 17</div>
<div class="edge elyria"><strong>Ljosalfar</strong></div>
<div class="edge selva">Bloom 23</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">16</div>
<div class="edge trell">Abadius 16</div>
<div class="edge ignan">Patchwall 12</div>
<div class="edge aquan">Olarune 18</div>
<div class="edge elyria">Kythorn 1</div>
<div class="edge selva">Fruit 1</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">17</div>
<div class="edge trell">Abadius 17</div>
<div class="edge ignan">Patchwall 13</div>
<div class="edge aquan">Olarune 19</div>
<div class="edge elyria">Kythorn 2</div>
<div class="edge selva">Fruit 2</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">18</div>
<div class="edge trell">Abadius 18</div>
<div class="edge ignan">Patchwall 14</div>
<div class="edge aquan">Olarune 20</div>
<div class="edge elyria">Kythorn 3</div>
<div class="edge selva">Fruit 3</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">19</div>
<div class="edge trell">Abadius 19</div>
<div class="edge ignan">Patchwall 15</div>
<div class="edge aquan">Olarune 21</div>
<div class="edge elyria">Kythorn 4</div>
<div class="edge selva">Fruit 4</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">20</div>
<div class="edge trell">Abadius 20</div>
<div class="edge ignan">Patchwall 16</div>
<div class="edge aquan">Olarune 22</div>
<div class="edge elyria">Kythorn 5</div>
<div class="edge selva">Fruit 5</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">21</div>
<div class="edge trell">Abadius 21</div>
<div class="edge ignan">Patchwall 17</div>
<div class="edge aquan">Olarune 23</div>
<div class="edge elyria">Kythorn 6</div>
<div class="edge selva">Fruit 6</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">22</div>
<div class="edge trell">Abadius 22</div>
<div class="edge ignan">Patchwall 18</div>
<div class="edge aquan">Olarune 24</div>
<div class="edge elyria">Kythorn 7</div>
<div class="edge selva">Fruit 7</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">23</div>
<div class="edge trell">Abadius 23</div>
<div class="edge ignan">Patchwall 19</div>
<div class="edge aquan">Olarune 25</div>
<div class="edge elyria">Kythorn 8</div>
<div class="edge selva">Fruit 8</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">24</div>
<div class="edge trell">Abadius 24</div>
<div class="edge ignan">Patchwall 20</div>
<div class="edge aquan">Olarune 26</div>
<div class="edge elyria">Kythorn 9</div>
<div class="edge selva">Fruit 9</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">25</div>
<div class="edge trell">Abadius 25</div>
<div class="edge ignan">Patchwall 21</div>
<div class="edge aquan">Olarune 27</div>
<div class="edge elyria">Kythorn 10</div>
<div class="edge selva">Fruit 10</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">26</div>
<div class="edge trell">Abadius 26</div>
<div class="edge ignan">Patchwall 22</div>
<div class="edge aquan">Olarune 28</div>
<div class="edge elyria">Kythorn 11</div>
<div class="edge selva">Fruit 11</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">27</div>
<div class="edge trell">Abadius 27</div>
<div class="edge ignan">Patchwall 23</div>
<div class="edge aquan"><strong>Springday</strong></div>
<div class="edge elyria">Kythorn 12</div>
<div class="edge selva">Fruit 12</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">28</div>
<div class="edge trell">Abadius 28</div>
<div class="edge ignan">Patchwall 24</div>
<div class="edge aquan">Therendor 1</div>
<div class="edge elyria">Kythorn 13</div>
<div class="edge selva">Fruit 13</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">29</div>
<div class="edge trell">Abadius 29</div>
<div class="edge ignan">Patchwall 25</div>
<div class="edge aquan">Therendor 2</div>
<div class="edge elyria">Kythorn 14</div>
<div class="edge selva">Fruit 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">30</div>
<div class="edge trell">Abadius 30</div>
<div class="edge ignan">Patchwall 26</div>
<div class="edge aquan">Therendor 3</div>
<div class="edge elyria">Kythorn 15</div>
<div class="edge selva">Fruit 15</div>
&nbsp;<br>
&nbsp;
</td>
</tr>

<tr class="spacing"><td colspan=5></td></tr>
<tr>
<td style="border: none">&nbsp;</td>
<td colspan=3>
<div class="edge trell">Abadius 31</div>
<div class="edge ignan">Patchwall 27</div>
<div class="edge aquan">Therendor 4</div>
<div class="edge elyria">Kythorn 16</div>
<div class="edge selva">Fruit 16</div>
<strong>🌳 Terran Apex</strong><br>
<div class="column">
Spring Equinox (Ocean)<br>
Summer Solstice (Elyria)
</div>
<div class="column">
Autumn Equinox (Mountain)<br>
Winter Solstice (Zephyr)
</div>
<div>
&nbsp;
</div>
</td>
<td style="border: none">&nbsp;</td>
</tr>
<tr class="spacing"><td colspan=5></td></tr>

<tr><th class="month" colspan=5>12 - Idea</th></tr>
<tr>
<td>
<div class="edge day">1</div>
<div class="edge trell">Calistril 1</div>
<div class="edge ignan">Patchwall 28</div>
<div class="edge aquan">Therendor 5</div>
<div class="edge elyria">Kythorn 17</div>
<div class="edge selva">Fruit 17</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">2</div>
<div class="edge trell">Calistril 2</div>
<div class="edge ignan">Ready'reat 1</div>
<div class="edge aquan">Therendor 6</div>
<div class="edge elyria">Kythorn 18</div>
<div class="edge selva">Fruit 18</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">3</div>
<div class="edge trell">Calistril 3</div>
<div class="edge ignan">Ready'reat 2</div>
<div class="edge aquan">Therendor 7</div>
<div class="edge elyria">Kythorn 19</div>
<div class="edge selva">Fruit 19</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">4</div>
<div class="edge trell">Calistril 4</div>
<div class="edge ignan">Ready'reat 3</div>
<div class="edge aquan">Therendor 8</div>
<div class="edge elyria">Kythorn 20</div>
<div class="edge selva">Fruit 20</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">5</div>
<div class="edge trell">Calistril 5</div>
<div class="edge ignan">Ready'reat 4</div>
<div class="edge aquan">Therendor 9</div>
<div class="edge elyria">Kythorn 21</div>
<div class="edge selva">Fruit 21</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">6</div>
<div class="edge trell">Calistril 6</div>
<div class="edge ignan">Ready'reat 5</div>
<div class="edge aquan">Therendor 10</div>
<div class="edge elyria">Kythorn 22</div>
<div class="edge selva">Fruit 22</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">7</div>
<div class="edge trell">Calistril 7</div>
<div class="edge ignan">Ready'reat 6</div>
<div class="edge aquan">Therendor 11</div>
<div class="edge elyria">Kythorn 23</div>
<div class="edge selva">Fruit 23</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">8</div>
<div class="edge trell">Calistril 8</div>
<div class="edge ignan">Ready'reat 7</div>
<div class="edge aquan">Therendor 12</div>
<div class="edge elyria">Kythorn 24</div>
<div class="edge selva">Sweat 1</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">9</div>
<div class="edge trell">Calistril 9</div>
<div class="edge ignan">Ready'reat 8</div>
<div class="edge aquan">Therendor 13</div>
<div class="edge elyria">Kythorn 25</div>
<div class="edge selva">Sweat 2</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">10</div>
<div class="edge trell">Calistril 10</div>
<div class="edge ignan">Ready'reat 9</div>
<div class="edge aquan">Therendor 14</div>
<div class="edge elyria">Kythorn 26</div>
<div class="edge selva">Sweat 3</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">11</div>
<div class="edge trell">Calistril 11</div>
<div class="edge ignan">Ready'reat 10</div>
<div class="edge aquan">Therendor 15</div>
<div class="edge elyria">Kythorn 27</div>
<div class="edge selva">Sweat 4</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">12</div>
<div class="edge trell">Calistril 12</div>
<div class="edge ignan">Ready'reat 11</div>
<div class="edge aquan">Therendor 16</div>
<div class="edge elyria">Kythorn 28</div>
<div class="edge selva">Sweat 5</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">13</div>
<div class="edge trell">Calistril 13</div>
<div class="edge ignan">Ready'reat 12</div>
<div class="edge aquan">Therendor 17</div>
<div class="edge elyria">Kythorn 29</div>
<div class="edge selva">Sweat 6</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">14</div>
<div class="edge trell">Calistril 14</div>
<div class="edge ignan">Ready'reat 13</div>
<div class="edge aquan">Therendor 18</div>
<div class="edge elyria">Kythorn 30</div>
<div class="edge selva">Sweat 7</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">15</div>
<div class="edge trell">Calistril 15</div>
<div class="edge ignan">Ready'reat 14</div>
<div class="edge aquan">Therendor 19</div>
<div class="edge elyria">Flamerule 1</div>
<div class="edge selva">Sweat 8</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">16</div>
<div class="edge trell">Calistril 16</div>
<div class="edge ignan">Ready'reat 15</div>
<div class="edge aquan">Therendor 20</div>
<div class="edge elyria">Flamerule 2</div>
<div class="edge selva">Sweat 9</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">17</div>
<div class="edge trell">Calistril 17</div>
<div class="edge ignan">Ready'reat 16</div>
<div class="edge aquan">Therendor 21</div>
<div class="edge elyria">Flamerule 3</div>
<div class="edge selva">Sweat 10</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">18</div>
<div class="edge trell">Calistril 18</div>
<div class="edge ignan">Ready'reat 17</div>
<div class="edge aquan">Therendor 22</div>
<div class="edge elyria">Flamerule 4</div>
<div class="edge selva">Sweat 11</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">19</div>
<div class="edge trell">Calistril 19</div>
<div class="edge ignan">Ready'reat 18</div>
<div class="edge aquan">Therendor 23</div>
<div class="edge elyria">Flamerule 5</div>
<div class="edge selva">Sweat 12</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">20</div>
<div class="edge trell">Calistril 20</div>
<div class="edge ignan">Ready'reat 19</div>
<div class="edge aquan">Therendor 24</div>
<div class="edge elyria">Flamerule 6</div>
<div class="edge selva">Sweat 13</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">21</div>
<div class="edge trell">Calistril 21</div>
<div class="edge ignan">Ready'reat 20</div>
<div class="edge aquan">Therendor 25</div>
<div class="edge elyria">Flamerule 7</div>
<div class="edge selva">Sweat 14</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">22</div>
<div class="edge trell">Calistril 22</div>
<div class="edge ignan">Ready'reat 21</div>
<div class="edge aquan">Therendor 26</div>
<div class="edge elyria">Flamerule 8</div>
<div class="edge selva">Sweat 15</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">23</div>
<div class="edge trell">Calistril 23</div>
<div class="edge ignan">Ready'reat 22</div>
<div class="edge aquan">Therendor 27</div>
<div class="edge elyria">Flamerule 9</div>
<div class="edge selva">Sweat 16</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">24</div>
<div class="edge trell">Calistril 24</div>
<div class="edge ignan">Ready'reat 23</div>
<div class="edge aquan">Therendor 28</div>
<div class="edge elyria">Flamerule 10</div>
<div class="edge selva">Sweat 17</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">25</div>
<div class="edge trell">Calistril 25</div>
<div class="edge ignan">Ready'reat 24</div>
<div class="edge aquan">Eyre 1</div>
<div class="edge elyria">Flamerule 11</div>
<div class="edge selva">Sweat 18</div>
&nbsp;<br>
&nbsp;
</td>
</tr>
<tr>
<td>
<div class="edge day">26</div>
<div class="edge trell">Calistril 26</div>
<div class="edge ignan">Ready'reat 25</div>
<div class="edge aquan">Eyre 2</div>
<div class="edge elyria">Flamerule 12</div>
<div class="edge selva">Sweat 19</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">27</div>
<div class="edge trell">Calistril 27</div>
<div class="edge ignan">Ready'reat 26</div>
<div class="edge aquan">Eyre 3</div>
<div class="edge elyria">Flamerule 13</div>
<div class="edge selva">Sweat 20</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">28</div>
<div class="edge trell">Calistril 28</div>
<div class="edge ignan">Ready'reat 27</div>
<div class="edge aquan">Eyre 4</div>
<div class="edge elyria">Flamerule 14</div>
<div class="edge selva">Sweat 21</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">29</div>
<div class="edge trell">Calistril 29</div>
<div class="edge ignan">Ready'reat 28</div>
<div class="edge aquan">Eyre 5</div>
<div class="edge elyria">Flamerule 15</div>
<div class="edge selva">Sweat 22</div>
&nbsp;<br>
&nbsp;
</td>
<td>
<div class="edge day">30</div>
<div class="edge trell">Pharast 1</div>
<div class="edge ignan">Sunsebb 1</div>
<div class="edge aquan">Eyre 6</div>
<div class="edge elyria">Flamerule 16</div>
<div class="edge selva">Sweat 23</div>
&nbsp;<br>
🌑 New Moon<br>
&nbsp;
</td>
</tr>

</table>
