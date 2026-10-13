// Adds draggable grippers between the columns of #session-layout.
// Widths are stored as CSS variables (--nav-w, --side-w) and remembered.
(function () {
  var KEY = 'equilibrium-column-widths';
  var MIN = 120;      // Minimum sidebar width, in px.
  var MIN_MAIN = 300; // Minimum central column width, in px.

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; }
    catch (e) { return {}; }
  }

  function save(widths) {
    try { localStorage.setItem(KEY, JSON.stringify(widths)); }
    catch (e) { /* Storage unavailable. */ }
  }

  function init() {
    var layout = document.getElementById('session-layout');
    var nav = document.getElementById('session-nav');
    var side = document.getElementById('session-sidebar');
    if (!layout || !nav) return;

    var widths = load();
    if (widths.nav) layout.style.setProperty('--nav-w', widths.nav + 'px');
    if (side && widths.side) layout.style.setProperty('--side-w', widths.side + 'px');

    var navGrip = makeGripper('nav');
    var sideGrip = side ? makeGripper('side') : null;

    function makeGripper(which) {
      var g = document.createElement('div');
      g.className = 'column-gripper';
      g.title = 'Drag to resize (double-click to reset)';
      layout.appendChild(g);

      g.addEventListener('pointerdown', function (e) {
        e.preventDefault();
        g.setPointerCapture(e.pointerId);
        g.classList.add('dragging');
        document.body.classList.add('column-resizing');
        var startX = e.clientX;
        var startW = (which === 'nav' ? nav : side).getBoundingClientRect().width;
        var gap = parseFloat(getComputedStyle(layout).columnGap) || 0;
        var other = which === 'nav' ? side : nav;
        var otherW = other ? other.getBoundingClientRect().width : 0;
        var max = layout.clientWidth - otherW - gap * 2 - MIN_MAIN;

        function move(ev) {
          var dx = ev.clientX - startX;
          var w = which === 'nav' ? startW + dx : startW - dx;
          w = Math.round(Math.max(MIN, Math.min(max, w)));
          layout.style.setProperty('--' + which + '-w', w + 'px');
          widths[which] = w;
          position();
        }
        function up() {
          g.classList.remove('dragging');
          document.body.classList.remove('column-resizing');
          g.removeEventListener('pointermove', move);
          g.removeEventListener('pointerup', up);
          g.removeEventListener('pointercancel', up);
          save(widths);
        }
        g.addEventListener('pointermove', move);
        g.addEventListener('pointerup', up);
        g.addEventListener('pointercancel', up);
      });

      g.addEventListener('dblclick', function () {
        layout.style.removeProperty('--' + which + '-w');
        delete widths[which];
        save(widths);
        position();
      });
      return g;
    }

    // Center each gripper in the gap beside its column.
    function position() {
      var base = layout.getBoundingClientRect().left;
      var gap = parseFloat(getComputedStyle(layout).columnGap) || 0;
      var nr = nav.getBoundingClientRect();
      navGrip.style.left = (nr.right - base + gap / 2 - navGrip.offsetWidth / 2) + 'px';
      if (sideGrip) {
        var sr = side.getBoundingClientRect();
        sideGrip.style.left = (sr.left - base - gap / 2 - sideGrip.offsetWidth / 2) + 'px';
      }
    }

    window.addEventListener('resize', position);
    if (window.ResizeObserver) new ResizeObserver(position).observe(layout);
    position();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
