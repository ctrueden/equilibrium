// Rules tooltips: shows the rule text of a `.rule-ref[data-tip]` link,
// taken from its <template id="tip-KEY">, when it is hovered or focused.
// On touch screens, the first tap shows the tooltip, and the second
// follows the link. See _includes/5e and _bin/dnd5e.py.
(function () {
  'use strict';
  if (window.ruleTips) return;
  window.ruleTips = true;

  var SHOW_DELAY = 150, HIDE_DELAY = 250, GAP = 6;
  var tip = null, current = null, showTimer = null, hideTimer = null;
  var lastPointer = 'mouse';

  function tipElement() {
    if (!tip) {
      tip = document.createElement('div');
      tip.className = 'rule-tip';
      tip.setAttribute('role', 'tooltip');
      tip.hidden = true;
      tip.addEventListener('mouseenter', function () { clearTimeout(hideTimer); });
      tip.addEventListener('mouseleave', scheduleHide);
      document.body.appendChild(tip);
    }
    return tip;
  }

  function refOf(el) {
    return el && el.closest ? el.closest('.rule-ref[data-tip]') : null;
  }

  function show(ref) {
    clearTimeout(showTimer);
    clearTimeout(hideTimer);
    var tpl = document.getElementById('tip-' + ref.getAttribute('data-tip'));
    if (!tpl) return;
    var t = tipElement();
    if (current !== ref) {
      t.innerHTML = '';
      t.appendChild(tpl.content.cloneNode(true));
      t.scrollTop = 0;
      current = ref;
    }
    t.hidden = false;
    position(ref, t);
  }

  function position(ref, t) {
    var r = ref.getBoundingClientRect();
    var vw = document.documentElement.clientWidth, vh = window.innerHeight;
    t.style.left = '0px';
    t.style.top = '0px';
    var w = t.offsetWidth, h = t.offsetHeight;
    var left = Math.min(Math.max(GAP, r.left), vw - w - GAP);
    var below = vh - r.bottom, above = r.top;
    var top = (below >= h + GAP || below >= above) ? r.bottom + GAP : r.top - h - GAP;
    t.style.left = Math.max(GAP, left) + window.scrollX + 'px';
    t.style.top = Math.max(GAP, top) + window.scrollY + 'px';
  }

  function hide() {
    clearTimeout(showTimer);
    clearTimeout(hideTimer);
    if (tip) tip.hidden = true;
    current = null;
  }

  function scheduleHide() {
    clearTimeout(showTimer);
    clearTimeout(hideTimer);
    hideTimer = setTimeout(hide, HIDE_DELAY);
  }

  document.addEventListener('pointerdown', function (e) {
    lastPointer = e.pointerType || 'mouse';
  }, true);

  document.addEventListener('mouseover', function (e) {
    if (lastPointer === 'touch') return;
    var ref = refOf(e.target);
    if (!ref) return;
    clearTimeout(hideTimer);
    if (ref === current && tip && !tip.hidden) return;
    clearTimeout(showTimer);
    showTimer = setTimeout(function () { show(ref); }, SHOW_DELAY);
  });

  document.addEventListener('mouseout', function (e) {
    var ref = refOf(e.target);
    if (ref && !ref.contains(e.relatedTarget)) scheduleHide();
  });

  document.addEventListener('focusin', function (e) {
    // Keyboard focus only: a tap focuses the link too, before its click.
    var ref = refOf(e.target);
    if (ref && ref.matches(':focus-visible')) show(ref);
  });

  document.addEventListener('focusout', function (e) {
    if (refOf(e.target) && !(tip && tip.contains(e.relatedTarget))) scheduleHide();
  });

  document.addEventListener('click', function (e) {
    var ref = refOf(e.target);
    if (ref && lastPointer !== 'mouse' && ref !== current) {
      // First tap on a touch screen: show the tooltip instead.
      e.preventDefault();
      show(ref);
    } else if (!ref && tip && !tip.hidden && !tip.contains(e.target)) {
      hide();
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') hide();
  });

  window.addEventListener('resize', function () {
    if (current && tip && !tip.hidden) position(current, tip);
  });
})();
