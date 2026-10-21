/* Mutschenhof – kleine, abhängigkeitsfreie Interaktionen.
   Ohne JavaScript bleibt die Seite vollständig lesbar. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  root.classList.add('js');
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Kopfzeile: transparent über dem Hero, danach solide */
  var header = $('.site-header');
  function onScroll() {
    if (!header) return;
    var solid = d.body.classList.contains('no-hero') || window.scrollY > 40;
    header.classList.toggle('is-solid', solid);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* Navigation: Untermenüs (Klick/Tastatur) */
  var subs = $$('.has-sub');
  function closeSubs(except) {
    subs.forEach(function (li) {
      if (li === except) return;
      li.classList.remove('is-open');
      var b = $('.nav-link', li); if (b) b.setAttribute('aria-expanded', 'false');
    });
  }
  subs.forEach(function (li) {
    var btn = $('.nav-link', li);
    btn.addEventListener('click', function (e) {
      if (window.innerWidth <= 1100) return;
      var open = !li.classList.contains('is-open');
      closeSubs(li);
      li.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
      e.stopPropagation();
    });
  });
  d.addEventListener('click', function () { closeSubs(); });
  d.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeSubs();
      if (d.body.classList.contains('menu-open')) setMenu(false);
    }
  });

  /* Mobiles Menü */
  var toggle = $('.menu-toggle');
  function setMenu(open) {
    d.body.classList.toggle('menu-open', open);
    if (toggle) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
    }
    if (header) header.classList.toggle('is-solid', open ? false : (d.body.classList.contains('no-hero') || window.scrollY > 40));
  }
  if (toggle) {
    toggle.addEventListener('click', function () { setMenu(!d.body.classList.contains('menu-open')); });
    $$('.nav a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    window.addEventListener('resize', function () { if (window.innerWidth > 1100) setMenu(false); });
  }

  /* Einblenden beim Scrollen */
  var rev = $$('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rev.forEach(function (el) { io.observe(el); });
  } else { rev.forEach(function (el) { el.classList.add('is-in'); }); }

  /* Lightbox (natives <dialog>) */
  var links = $$('a.lb');
  if (links.length && 'HTMLDialogElement' in window) {
    var dlg = d.createElement('dialog');
    dlg.className = 'lightbox';
    dlg.setAttribute('aria-label', 'Bildansicht');
    dlg.innerHTML =
      '<div class="lb-stage"><img alt=""></div><p class="lb-cap"></p>' +
      '<button class="lb-btn lb-close" type="button" aria-label="Schließen"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' +
      '<button class="lb-btn lb-prev" type="button" aria-label="Vorheriges Bild"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg></button>' +
      '<button class="lb-btn lb-next" type="button" aria-label="Nächstes Bild"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg></button>';
    d.body.appendChild(dlg);
    var im = $('img', dlg), cap = $('.lb-cap', dlg), group = [], idx = 0, opener = null;
    function show(i) {
      idx = (i + group.length) % group.length;
      var a = group[idx];
      im.src = a.getAttribute('href');
      im.alt = a.getAttribute('data-alt') || '';
      cap.textContent = a.getAttribute('data-caption') || '';
      var multi = group.length > 1;
      $('.lb-prev', dlg).style.display = $('.lb-next', dlg).style.display = multi ? '' : 'none';
    }
    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        opener = a;
        var g = a.getAttribute('data-group');
        group = links.filter(function (x) { return x.getAttribute('data-group') === g; });
        show(group.indexOf(a));
        dlg.showModal();
      });
    });
    $('.lb-close', dlg).addEventListener('click', function () { dlg.close(); });
    $('.lb-prev', dlg).addEventListener('click', function () { show(idx - 1); });
    $('.lb-next', dlg).addEventListener('click', function () { show(idx + 1); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.classList.contains('lb-stage')) dlg.close(); });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
    dlg.addEventListener('close', function () { if (opener) opener.focus(); });
  }

  /* Externe Inhalte erst nach Klick laden (2-Klick-Lösung) */
  $$('.embed[data-src]').forEach(function (box) {
    var btn = $('.embed-load', box);
    if (!btn) return;
    btn.addEventListener('click', function () {
      var f = d.createElement('iframe');
      f.src = box.getAttribute('data-src');
      f.title = box.getAttribute('data-title') || 'Externer Inhalt';
      f.loading = 'lazy';
      f.allow = box.hasAttribute('data-video') ? 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen' : '';
      if (box.hasAttribute('data-video')) f.setAttribute('allowfullscreen', '');
      box.appendChild(f);
      box.classList.add('is-loaded');
      $$('.embed-inner,.embed-bg', box).forEach(function (n) { n.remove(); });
    });
  });

  /* Anfrageformulare → vorbereitete E-Mail (kein Server nötig) */
  $$('form[data-mailto]').forEach(function (form) {
    var status = $('.form-status', form);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var lines = [], seen = {};
      $$('input,select,textarea', form).forEach(function (el) {
        if (!el.name || el.type === 'submit' || el.name === 'dsgvo') return;
        if ((el.type === 'radio' || el.type === 'checkbox') && !el.checked) return;
        var label = el.getAttribute('data-label') || el.name;
        var v = (el.value || '').trim();
        if (!v) return;
        if (seen[el.name] && (el.type === 'checkbox')) { lines[seen[el.name] - 1] += ', ' + v; return; }
        lines.push(label + ': ' + v);
        if (el.type === 'checkbox') seen[el.name] = lines.length;
      });
      var to = form.getAttribute('data-mailto');
      var subject = form.getAttribute('data-subject') || 'Anfrage';
      var body = 'Guten Tag,\n\nich möchte gern anfragen:\n\n' + lines.join('\n') + '\n\nViele Grüße';
      var href = 'mailto:' + to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      window.location.href = href;
      if (status) {
        status.hidden = false;
        status.innerHTML = 'Ihr E-Mail-Programm öffnet sich jetzt mit der vorbereiteten Anfrage – bitte dort noch auf „Senden“ klicken. ' +
          'Falls sich nichts öffnet, schreiben Sie uns direkt an <a href="mailto:' + to + '">' + to + '</a>.';
        status.focus && status.setAttribute('tabindex', '-1');
        status.focus && status.focus();
      }
    });
  });

  /* Zähler-Felder (+/−) */
  $$('.stepper').forEach(function (s) {
    var input = $('input', s);
    $$('button', s).forEach(function (b) {
      b.addEventListener('click', function () {
        var v = parseInt(input.value || '0', 10) + parseInt(b.getAttribute('data-step'), 10);
        var min = parseInt(input.min || '0', 10), max = parseInt(input.max || '99', 10);
        input.value = Math.max(min, Math.min(max, v));
        input.dispatchEvent(new Event('change', { bubbles: true }));
      });
    });
  });

  /* Kahnfahrt: Hinweis zu den möglichen Wochentagen */
  var dayInput = $('input[data-weekdays]');
  if (dayInput) {
    var hint = $('#day-hint');
    dayInput.addEventListener('change', function () {
      if (!dayInput.value || !hint) return;
      var wd = new Date(dayInput.value + 'T12:00:00').getDay();      // 0=So … 6=Sa
      var ok = dayInput.getAttribute('data-weekdays').split(',').indexOf(String(wd)) > -1;
      hint.hidden = ok;
    });
  }

  /* Schlachttermine: nächster Termin + Countdown */
  $$('[data-dates]').forEach(function (cd) {
    var dates = JSON.parse(cd.getAttribute('data-dates')).map(function (s) { return new Date(s + 'T08:00:00'); })
      .sort(function (a, b) { return a - b; });
    var now = new Date();
    var next = dates.filter(function (x) { return x.getTime() + 36e5 * 12 > now.getTime(); })[0];
    var yes = $('.cd-yes', cd), no = $('.cd-no', cd);
    if (next) {
      yes.hidden = false; no.hidden = true;
      $('.next-date', cd).textContent = next.toLocaleDateString('de-DE', { weekday: 'long', day: '2-digit', month: 'long', year: 'numeric' });
      var el = { d: $('[data-u=d]', cd), h: $('[data-u=h]', cd), m: $('[data-u=m]', cd), s: $('[data-u=s]', cd) };
      var tick = function () {
        var ms = Math.max(0, next - new Date()), s = Math.floor(ms / 1000);
        el.d.textContent = Math.floor(s / 86400);
        el.h.textContent = String(Math.floor(s % 86400 / 3600)).padStart(2, '0');
        el.m.textContent = String(Math.floor(s % 3600 / 60)).padStart(2, '0');
        el.s.textContent = String(s % 60).padStart(2, '0');
      };
      tick(); setInterval(tick, 1000);
    } else { yes.hidden = true; no.hidden = false; }
    var fb = $('.cd-fallback', cd); if (fb) fb.hidden = true;
  });

  /* Jahreszahl im Footer */
  $$('[data-year]').forEach(function (n) { n.textContent = new Date().getFullYear(); });
})();
