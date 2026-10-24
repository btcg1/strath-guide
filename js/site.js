/* Strath Field Guide: hero strip, trip map, live exchange rate, places preview, photo lightbox, entrances. */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const phone = matchMedia('(max-width: 720px)');
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  /* Entrances: each section's parts arrive in order, once. */
  const reveal = (els) => {
    if (!('IntersectionObserver' in window)) { els.forEach((e) => e.classList.add('is-in')); return; }
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
    els.forEach((el) => io.observe(el));
  };
  $$('section').forEach((sec) => $$('[data-reveal]', sec).forEach((el, i) => el.style.setProperty('--d', `${Math.min(i, 6) * 80}ms`)));
  reveal($$('[data-reveal]'));
  // A fast jump can carry an element past the viewport between two frames; anything already passed is shown too.
  let pending = $$('[data-reveal]'), ticking = false;
  const sweep = () => {
    ticking = false;
    pending = pending.filter((el) => { if (el.getBoundingClientRect().top < innerHeight) { el.classList.add('is-in'); return false; } return true; });
    if (!pending.length) removeEventListener('scroll', onScroll);
  };
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(sweep); } };
  addEventListener('scroll', onScroll, { passive: true });
  const staggerGrid = (sel) => { const els = $$(sel); els.forEach((el, i) => el.style.setProperty('--d', `${(i % 4) * 70}ms`)); reveal(els); };
  staggerGrid('.wall figure');
  staggerGrid('.food__pics figure');
  // Food and Shopping additions: dishes, section photos and the meal-deal rows (their dots slide to the price)
  const enter = (sel, step = 80) => { const els = $$(sel); els.forEach((el, i) => { el.setAttribute('data-reveal', ''); el.style.setProperty('--d', `${(i % 6) * step}ms`); }); reveal(els); pending.push(...els); };
  enter('.menu__pics li'); enter('.menu__list li'); enter('.tsec__pic'); enter('.dots__row', 90);

  /* Top bar: tinted once the page scrolls; on phones a three-line button opens the tabs and this page's sections. */
  const nav = $('.topnav');
  if (nav) {
    const tint = () => nav.classList.toggle('is-scrolled', scrollY > 8);
    tint(); addEventListener('scroll', tint, { passive: true });
    const btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'menu-btn';
    btn.setAttribute('aria-expanded', 'false'); btn.setAttribute('aria-controls', 'menu'); 
    btn.innerHTML = '<span class="menu-btn__bars" aria-hidden="true"><i></i><i></i><i></i></span><span class="menu-btn__label">Menu</span>';
    const panel = document.createElement('div');
    panel.className = 'menu'; panel.id = 'menu';
    const tabs = $('.tabs', nav), links = $('.topnav__links', nav);
    panel.innerHTML = '<p class="menu__label">Pages</p>' + tabs.outerHTML.replace('class="tabs"', 'class="menu__tabs"')
      + (links ? '<p class="menu__label">On this page</p>' + links.outerHTML.replace('class="topnav__links"', 'class="menu__links"') : '');
    nav.prepend(btn); nav.append(panel);
    const set = (open) => { btn.setAttribute('aria-expanded', String(open)); panel.classList.toggle('is-open', open); panel.inert = !open; document.documentElement.classList.toggle('menu-open', open); };
    set(false);
    btn.addEventListener('click', () => set(!panel.classList.contains('is-open')));
    panel.addEventListener('click', (e) => { if (e.target.closest('a')) set(false); });
    addEventListener('keydown', (e) => { if (e.key === 'Escape' && panel.classList.contains('is-open')) { set(false); btn.focus(); } });
    document.addEventListener('click', (e) => { if (panel.classList.contains('is-open') && !nav.contains(e.target)) set(false); });
  }

  /* Where am I: the section in view is marked in the top bar and in the phone menu. */
  const spy = $$('.topnav__links a[href^="#"]');
  if (spy.length && 'IntersectionObserver' in window) {
    const secs = spy.map((a) => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
    const mark = (id) => $$('.topnav__links a, .menu__links a').forEach((a) => { if (a.getAttribute('href') === '#' + id) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    const seen = new Map();
    const io = new IntersectionObserver((es) => {
      es.forEach((e) => seen.set(e.target.id, e.isIntersecting ? e.intersectionRect.height : 0));
      let best = null, h = 0;
      seen.forEach((v, k) => { if (v > h) { h = v; best = k; } });
      if (best) mark(best); else mark('');
    }, { threshold: [0, 0.25, 0.5, 0.75, 1], rootMargin: '-64px 0px 0px 0px' });
    secs.forEach((s) => io.observe(s));
  }

  /* Hero strip: the missing word cycles through photos. */
  const strip = $('[data-strip]');
  const caps = $$('[data-strip-caption]');
  if (strip) {
    const imgs = $$('img', strip);
    const useMobile = () => imgs.forEach((im) => { if (phone.matches && im.dataset.mobile && !im.dataset.swapped) { im.src = im.dataset.mobile; im.dataset.swapped = '1'; } });
    useMobile(); phone.addEventListener('change', useMobile);
    let i = 0, timer = null, paused = false, held = false;
    const show = (n) => {
      imgs[i].classList.remove('is-on');
      i = (n + imgs.length) % imgs.length;
      imgs[i].classList.add('is-on');
      caps.forEach((c) => { c.textContent = imgs[i].dataset.cap; });
    };
    const start = () => { if (!reduce && !timer) timer = setInterval(() => { if (!paused && !held && !document.hidden) show(i + 1); }, 3400); };
    strip.parentElement.addEventListener('pointerenter', () => { paused = true; });
    strip.parentElement.addEventListener('pointerleave', () => { paused = false; });
    setTimeout(start, 1600);
    // WCAG 2.2.2: anything that moves on its own for more than 5 seconds can be paused
    const cap = strip.parentElement.querySelector('.hero__photo');
    if (cap && !reduce) {
      const pb = document.createElement('button');
      pb.type = 'button'; pb.className = 'hero__pause'; pb.textContent = 'Pause'; pb.setAttribute('aria-pressed', 'false');
      pb.addEventListener('click', () => { held = !held; pb.textContent = held ? 'Play' : 'Pause'; pb.setAttribute('aria-pressed', String(held)); });
      cap.append(pb);
    }
  }

  /* Live exchange rate, with the checked rate as fallback. */
  let RATE = 1.71;
  const gbp = $('#gbp'), sgd = $('#sgd');
  const conv = () => { const v = parseFloat(gbp.value); sgd.textContent = Number.isFinite(v) && v >= 0 ? `S$${(v * RATE).toFixed(2)}` : 'S$–'; };
  if (gbp) { gbp.addEventListener('input', conv); conv(); }
  const setRate = (r, when) => {
    RATE = r; if (gbp) conv();
    const [a, b] = r.toFixed(2).split('.');
    const ii = $('[data-fx-int]'), dd = $('[data-fx-dec]'), ww = $('[data-fx-when]');
    if (ii) ii.textContent = a; if (dd) dd.textContent = `.${b}`;
    if (ww) ww.textContent = `today (rate of ${when})`;
  };
  const fmt = (d) => d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
  if (gbp || $('[data-fx-int]')) fetch('https://open.er-api.com/v6/latest/GBP').then((r) => r.json()).then((j) => {
    if (j && j.rates && j.rates.SGD) setRate(j.rates.SGD, fmt(new Date(j.time_last_update_unix * 1000))); else throw 0;
  }).catch(() => fetch('https://api.frankfurter.app/latest?from=GBP&to=SGD').then((r) => r.json()).then((j) => {
    if (j && j.rates && j.rates.SGD) setRate(j.rates.SGD, fmt(new Date(j.date)));
  })).catch(() => {});

  /* Trip map: one trip at a time, scrubbed in date order. */
  const trips = window.TRIPS || [], C = window.COORDS || {};
  const tripBox = $('[data-trip]');
  const mapEl = $('#map');
  const cards = $$('.trip-card', tripBox || document);
  const weeks = $('[data-weeks]');
  const slider = $('#week');
  const START = new Date('2025-09-08');
  const weekOf = (iso) => Math.floor((new Date(iso) - START) / 6048e5) + 1;
  if (!mapEl || !trips.length) {
    if (tripBox) tripBox.classList.add('no-map');
  } else {
    /* Our own SVG map: no tiles, no network. Zooming animates the viewBox; pins keep a constant screen size. */
    weeks.hidden = false;
    slider.min = 1; slider.max = trips.length;
    $('.weeks__label').innerHTML = 'Trip <output id="weekOut"></output> of ' + trips.length + ', <span data-week-dates></span>';
    const P = window.MAPPROJ;
    const xy = (key) => { const [lat, lon] = C[key]; return [(lon - P.lon0) * P.k * 100, -(lat - P.lat0) * 100]; };
    const pins = $$('.mpin', mapEl), home = $('.mhome', mapEl), route = $('.mroute', mapEl), label = $('.mlabel', mapEl), towns = $$('.mtown', mapEl);
    const homeXY = xy('strath');
    let vb = mapEl.getAttribute('viewBox').split(' ').map(Number), cur = -1, anim = 0;
    const upp = () => vb[2] / (mapEl.clientWidth || 1);          // map units per screen pixel
    const paint = () => {
      mapEl.setAttribute('viewBox', vb.map((n) => n.toFixed(2)).join(' '));
      const u = upp();
      pins.forEach((c) => c.setAttribute('r', (c.classList.contains('is-now') ? 7 : 4.5) * u));
      home.setAttribute('x', homeXY[0] - 5 * u); home.setAttribute('y', homeXY[1] - 5 * u);
      home.setAttribute('width', 10 * u); home.setAttribute('height', 10 * u);
      route.style.strokeDasharray = `${4 * u} ${5 * u}`;
      label.setAttribute('font-size', 15 * u); label.style.strokeWidth = 4 * u;
      towns.forEach((t) => t.setAttribute('font-size', 12 * u));
      if (label.dataset.x) { label.setAttribute('x', +label.dataset.x + 10 * u); label.setAttribute('y', +label.dataset.y + 5 * u); }
    };
    const fit = (pts) => {
      const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
      let x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
      let w = Math.max(x1 - x0, 160), h = Math.max(y1 - y0, 160);
      const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
      w *= 1.6; h *= 1.6;
      const aspect = (mapEl.clientWidth || 4) / (mapEl.clientHeight || 3);
      if (w / h < aspect) w = h * aspect; else h = w / aspect;
      return [cx - w / 2, cy - h / 2, w, h];
    };
    const zoomTo = (target, animate) => {
      cancelAnimationFrame(anim);
      if (!animate || reduce) { vb = target; paint(); return; }
      const from = vb.slice(), t0 = performance.now(), D = 650;
      const ease = (t) => 1 - Math.pow(1 - t, 4);
      const step = (now) => {
        const t = Math.min(1, (now - t0) / D), e = ease(t);
        vb = from.map((v, i) => v + (target[i] - v) * e); paint();
        if (t < 1) anim = requestAnimationFrame(step);
      };
      anim = requestAnimationFrame(step);
    };
    const select = (idx, animate) => {
      cur = idx; slider.value = idx + 1;
      const t = trips[idx];
      $('#weekOut').textContent = idx + 1;
      $('[data-week-dates]').textContent = `week ${weekOf(t.date)} of the semester`;
      cards.forEach((c) => c.classList.toggle('is-current', c.dataset.id === t.id));
      const shown = cards.find((c) => c.dataset.id === t.id);
      if (shown) $$('img', shown).forEach((im, k) => { im.classList.remove('is-in'); im.style.setProperty('--d', `${k * 70}ms`); requestAnimationFrame(() => requestAnimationFrame(() => im.classList.add('is-in'))); });
      pins.forEach((c) => { const j = +c.dataset.i; c.classList.toggle('is-now', j === idx); c.classList.toggle('is-past', j < idx); });
      const pts = t.pins.filter((p) => C[p]).map(xy);
      route.setAttribute('d', 'M' + [homeXY, ...pts].map((p) => p.map((n) => n.toFixed(1)).join(',')).join('L'));
      label.textContent = t.name; label.dataset.x = pts[0][0]; label.dataset.y = pts[0][1];
      zoomTo(fit([homeXY, ...pts]), animate);
    };
    pins.forEach((c) => c.addEventListener('click', () => select(+c.dataset.i, true)));
    slider.addEventListener('input', () => select(+slider.value - 1, true));
    $('[data-prev]').addEventListener('click', () => select((cur - 1 + trips.length) % trips.length, true));
    $('[data-next]').addEventListener('click', () => select((cur + 1) % trips.length, true));
    select(trips.findIndex((t) => t.id === 'skye'), false);
    new ResizeObserver(() => { if (cur >= 0) { const t = trips[cur]; vb = fit([homeXY, ...t.pins.filter((p) => C[p]).map(xy)]); paint(); } }).observe(mapEl);
  }

  /* Places: a sticky photo beside the list follows the row you point at, or the row in the middle of the screen. */
  const index = $('.index');
  if (index) {
    const pic = $('.index__frame img', index), cap = $('.index__framecap', index);
    const rows = $$('.index__row[data-preview]', index);
    let shown = null, hovering = false, warmed = false;
    const show = (row) => {
      if (!row || row === shown) return;
      shown = row;
      if (!warmed) { warmed = true; rows.forEach((r) => { new Image().src = r.dataset.preview; }); }
      if (reduce) { pic.src = row.dataset.preview; cap.textContent = row.dataset.name; return; }
      pic.classList.add('is-swapping');
      setTimeout(() => { pic.src = row.dataset.preview; cap.textContent = row.dataset.name; pic.classList.remove('is-swapping'); }, 140);
    };
    rows.forEach((row) => {
      row.addEventListener('pointerenter', () => { hovering = true; show(row); });
      row.addEventListener('focusin', () => show(row));
    });
    index.addEventListener('pointerleave', () => { hovering = false; });
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        if (hovering) return;
        const hit = entries.filter((e) => e.isIntersecting).map((e) => e.target)[0];
        if (hit) show(hit);
      }, { rootMargin: '-45% 0px -45% 0px' });
      rows.forEach((r) => io.observe(r));
    }
  }

  /* Photo wall: show the rest on request. */
  const more = $('[data-wall-more]');
  if (more) {
    more.addEventListener('click', () => {
      const hidden = $$('.wall figure[hidden]');
      hidden.forEach((f) => { f.hidden = false; f.classList.add('is-in'); });
      more.parentElement.hidden = true;
      if (hidden[0]) hidden[0].querySelector('img').focus?.();
    });
  }

  /* Lightbox for any photo with a large version. */
  const lb = $('[data-lightbox]');
  if (lb && lb.showModal) {
    const lbImg = $('img', lb), lbCap = $('figcaption', lb);
    let list = [], at = 0;
    const open = (items, n) => { list = items; at = n; paint(); if (!lb.open) lb.showModal(); };
    const paint = () => {
      const el = list[at];
      const src = el.dataset.large || el.querySelector('[data-large]')?.dataset.large;
      const im = el.tagName === 'IMG' ? el : el.querySelector('img');
      lbImg.src = src; lbImg.alt = im ? im.alt : '';
      lbCap.textContent = `${im ? im.alt : ''}  (${at + 1} of ${list.length})`;
    };
    const step = (d) => { at = (at + d + list.length) % list.length; paint(); };
    const groups = [() => $$('.album figure'), () => $$('.print'), () => $$('.food__pics figure'), () => $$('.menu__pics figure'), () => $$('.tsec__pic'), () => $$('.trip-card.is-current img')];
    groups.forEach((get) => {
      document.addEventListener('click', (e) => {
        const items = get();
        const hit = items.find((it) => it.contains(e.target));
        if (hit) open(items, items.indexOf(hit));
      });
    });
    $('[data-lb-close]').addEventListener('click', () => lb.close());
    $('[data-lb-prev]').addEventListener('click', () => step(-1));
    $('[data-lb-next]').addEventListener('click', () => step(1));
    lb.addEventListener('click', (e) => { if (e.target === lb || e.target.tagName === 'FIGURE') lb.close(); });
    lb.addEventListener('keydown', (e) => { if (e.key === 'ArrowLeft') step(-1); if (e.key === 'ArrowRight') step(1); });
  }
})();
