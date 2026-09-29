(function(){
  'use strict';
  const $ = (s, c=document) => c.querySelector(s);
  const $$ = (s, c=document) => Array.from(c.querySelectorAll(s));
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  const desktop = () => window.matchMedia('(min-width:960px)').matches;
  const clamp = (v,a,b) => Math.min(b, Math.max(a, v));
  const vh = () => window.innerHeight;

  /* ---------- INTRO: la marca sube y luego vuela al navbar (siempre, en cada carga) ---------- */
  const intro = $('.intro'), introMark = $('.intro-mark'), navBrand = $('.nav .brand'), heroH1 = $('.hero h1');
  const startHero = () => { $$('.split', heroH1 || document.body).forEach(s => s.classList.add('is-in')); };
  if (intro && reduce) { intro.classList.add('is-done'); document.documentElement.classList.remove('lock'); startHero(); }
  else if (intro) {
    window.scrollTo(0, 0);
    document.documentElement.classList.add('lock');
    navBrand.classList.add('is-hidden');
    setTimeout(() => {
      const a = introMark.getBoundingClientRect(), b = navBrand.getBoundingClientRect();
      const svg = introMark.querySelector('svg');
      introMark.classList.add('is-flying');
      svg.style.transform = `translate(${b.left - a.left}px, ${b.top - a.top}px) scale(${b.width / a.width})`;
      intro.classList.add('is-leaving');
      setTimeout(startHero, 350);
      setTimeout(() => { navBrand.classList.remove('is-hidden'); intro.classList.add('is-done'); document.documentElement.classList.remove('lock'); }, 950);
    }, 1750);
  } else startHero();

  /* ---------- NAV ---------- */
  const nav = $('.nav');
  const onScrollNav = () => nav.classList.toggle('is-scrolled', window.scrollY > 24);
  onScrollNav();
  const burger = $('.burger'), menu = $('.mobile-menu');
  if (burger) {
    const toggle = (open) => {
      const o = open ?? burger.getAttribute('aria-expanded') !== 'true';
      burger.setAttribute('aria-expanded', String(o)); menu.classList.toggle('is-open', o);
      document.documentElement.classList.toggle('lock', o);
    };
    burger.addEventListener('click', () => toggle());
    $$('a', menu).forEach(a => a.addEventListener('click', () => toggle(false)));
    window.addEventListener('keydown', e => { if (e.key === 'Escape') toggle(false); });
  }

  /* ---------- FONDO INTERACTIVO DEL HERO (sigue al mouse / giroscopio) ---------- */
  const canvas = $('.hero-canvas');
  if (canvas && !reduce) {
    const ctx = canvas.getContext('2d');
    let W, H, dpr = Math.min(window.devicePixelRatio || 1, 2);
    const mouse = {x:.5, y:.45, tx:.5, ty:.45};
    const orbs = [
      {c:'201,169,110', r:.42, ox:-.18, oy:-.12, k:.8, a:.22},
      {c:'237,235,230', r:.30, ox:.22, oy:.10, k:1.2, a:.09},
      {c:'37,211,102',  r:.24, ox:.05, oy:.28, k:1.6, a:.06},
    ];
    const resize = () => { W = canvas.clientWidth; H = canvas.clientHeight; canvas.width = W*dpr; canvas.height = H*dpr; ctx.setTransform(dpr,0,0,dpr,0,0); };
    resize(); window.addEventListener('resize', resize);
    const move = (x, y) => { mouse.tx = clamp(x / W, -.2, 1.2); mouse.ty = clamp(y / H, -.2, 1.2); };
    window.addEventListener('pointermove', e => move(e.clientX, e.clientY), {passive:true});
    window.addEventListener('deviceorientation', e => { if (e.gamma != null) move(W*(.5 + e.gamma/60), H*(.45 + (e.beta - 45)/90)); }, {passive:true});
    let t = 0, visible = true;
    const io = new IntersectionObserver(en => { const was = visible; visible = en[0].isIntersecting; if (visible && !was) loop(); }, {threshold:0});
    io.observe(canvas);
    const loop = () => {
      if (!visible) return;
      t += .006;
      mouse.x += (mouse.tx - mouse.x) * .06; mouse.y += (mouse.ty - mouse.y) * .06;
      ctx.clearRect(0, 0, W, H);
      const gap = W < 600 ? 34 : 42, mx = mouse.x*W, my = mouse.y*H;
      for (let x = gap/2; x < W; x += gap) for (let y = gap/2; y < H; y += gap) {
        const d = Math.hypot(x-mx, y-my), f = Math.max(0, 1 - d/360);
        ctx.fillStyle = `rgba(237,235,230,${.04 + f*.28})`;
        const s = 1 + f*1.6; ctx.fillRect(x - s/2, y - s/2, s, s);
      }
      orbs.forEach((o, i) => {
        const px = W*(mouse.x + o.ox) + Math.sin(t*o.k + i)*W*.05, py = H*(mouse.y + o.oy) + Math.cos(t*o.k*.8 + i)*H*.05, r = Math.max(W,H)*o.r;
        const g = ctx.createRadialGradient(px,py,0,px,py,r); g.addColorStop(0, `rgba(${o.c},${o.a})`); g.addColorStop(1, `rgba(${o.c},0)`);
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(px,py,r,0,Math.PI*2); ctx.fill();
      });
      requestAnimationFrame(loop);
    };
    loop();
  }

  /* ---------- CURSOR PERSONALIZADO + GLOW (solo puntero fino) ---------- */
  const cursor = $('.cursor'), glow = $('.cursor-glow');
  if (fine && !reduce && cursor) {
    let cx = innerWidth/2, cy = innerHeight/2, tx = cx, ty = cy, gx = cx, gy = cy;
    window.addEventListener('pointermove', e => { tx = e.clientX; ty = e.clientY; }, {passive:true});
    (function anim(){
      cx += (tx-cx)*.28; cy += (ty-cy)*.28; gx += (tx-gx)*.1; gy += (ty-gy)*.1;
      cursor.style.transform = `translate(${cx}px,${cy}px)`;
      if (glow) glow.style.transform = `translate(${gx}px,${gy}px) translate(-50%,-50%)`;
      requestAnimationFrame(anim);
    })();
    const linkSel = 'a,button,summary,.pain,.wcard';
    document.addEventListener('pointerover', e => { const el = e.target.closest(linkSel); cursor.classList.toggle('is-link', !!el); }, {passive:true});
    document.addEventListener('pointerout', e => { if (e.target.closest(linkSel)) cursor.classList.remove('is-link'); }, {passive:true});
  }

  /* ---------- BOTONES MAGNÉTICOS ---------- */
  if (fine && !reduce) $$('.magnetic').forEach(el => {
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      const x = (e.clientX - r.left - r.width/2) * .28, y = (e.clientY - r.top - r.height/2) * .28;
      el.style.transform = `translate(${x}px,${y}px)`;
    });
    el.addEventListener('pointerleave', () => { el.style.transform = ''; });
  });

  /* ---------- REVELADO POR PALABRAS ---------- */
  $$('.split').forEach(s => $$('.w', s).forEach((w, i) => w.style.setProperty('--i', i)));
  const splitIO = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); splitIO.unobserve(e.target); } }), {threshold:.2});
  $$('.split').forEach(s => { if (!s.closest('.hero')) splitIO.observe(s); });

  /* ---------- REVEAL genérico ---------- */
  const rio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); rio.unobserve(e.target); } }), {threshold:.12, rootMargin:'0px 0px -6% 0px'});
  $$('.reveal').forEach(el => rio.observe(el));

  /* ---------- ESCENAS LIGADAS AL SCROLL (una sola pasada por frame) ---------- */
  const track = $('.hero-track'), fig = $('.hero-figure'), figImg = $('.hero-figure img'), copy = $('.hero-copy'), big = $('.hero-big'),
        hint = $('.hero-scroll'), side = $('.hero-side'), sig = $('.sig-wrap'), progress = $('.progress i');
  const fillWords = $$('.fill .w'), fillEl = $('.fill-text');
  const tfTrack = $('.tf-track'), tfItems = $$('.tf-item'), tfDots = $$('.tf-dot'), tfBig = $('.tf-big');
  const hsTrack = $('.hs-track'), hsRow = $('.hs-row'), hsSteps = $$('.hs-row .step');
  const parallaxEls = $$('[data-parallax]');
  const tfScenes = $$('.tf-scene');
  const wheelTrack = $('.wheel-track'), wheel = $('.wheel'), wcards = $$('.wcard'), wdetails = $$('.wdetail'), wcount = $('.wheel-count b');
  let sigStarted = false, tfCurrent = -1, hsW = 0, figShift = 0, wCurrent = -1, wStep = 16, wR = 900, holding = false;
  if (wheelTrack) wheelTrack.style.setProperty('--wheel-n', wcards.length);

  if (tfTrack) tfTrack.style.setProperty('--tf-n', tfItems.length);

  const measure = () => {
    if (wheel && wcards.length) {
      const cs = getComputedStyle(document.documentElement);
      const cardW = wcards[0].getBoundingClientRect().width || 200;
      wR = parseFloat(cs.getPropertyValue('--wheel-r')) / 100 * vh();
      const gap = innerWidth < 760 ? 26 : 36;
      wStep = 2 * Math.asin(Math.min(.5, (cardW + gap) / (2 * wR))) * 180 / Math.PI;
      wCurrent = -1;
    }
    if (hsRow && innerWidth >= 1024) {
      hsRow.style.transform = 'none';
      hsW = hsRow.scrollWidth; hsTrack.style.setProperty('--hs-w', hsW + 'px');
    } else if (hsRow) { hsRow.style.transform = ''; hsTrack.style.removeProperty('--hs-w'); }
  };

  const frame = () => {
    const y = window.scrollY, H = vh();
    onScrollNav();
    if (progress) { const max = document.documentElement.scrollHeight - H; progress.style.transform = `scaleX(${max > 0 ? y/max : 0})`; }

    // HERO: la foto se reduce (y en móvil se centra y oscurece), la firma se dibuja
    if (track) {
      const rect = track.getBoundingClientRect(), total = track.offsetHeight - H;
      const p = clamp(-rect.top / total, 0, 1), k = Math.min(1, p / .7);
      const isD = desktop();
      figShift = fig.offsetWidth / 2 - (isD ? .44 : .62) * innerWidth;   // centro real de la figura → centro de pantalla
      const s = 1 - (isD ? .58 : .45) * k;
      const tx = figShift * k, ty = isD ? 6 * k : 36 * k;
      fig.style.transform = `translate(${tx}px, ${ty}vh) scale(${s})`;
      if (figImg) figImg.style.filter = `brightness(${1 - .6 * k})`;
      const fade = 1 - clamp(p / .35, 0, 1);
      [copy, big, hint, side].forEach(el => { if (el) { el.style.opacity = fade; el.style.pointerEvents = fade < .2 ? 'none' : ''; } });
      if (sig) {
        const show = p > .38;
        sig.classList.toggle('is-visible', show);
        if (show && !sigStarted) { sigStarted = true; holdForSignature(rect.top + window.scrollY + total * .72); }
      }
    }

    // MANIFIESTO: las palabras se iluminan conforme bajas
    if (fillEl && fillWords.length) {
      const r = fillEl.getBoundingClientRect();
      const p = clamp((H * .85 - r.top) / (r.height + H * .35), 0, 1);
      const lit = Math.round(p * fillWords.length);
      fillWords.forEach((w, i) => w.classList.toggle('is-lit', i < lit));
    }

    // IMAGINA ESTO: escena anclada, un beneficio a la vez
    if (tfTrack && tfItems.length) {
      const r = tfTrack.getBoundingClientRect(), total = tfTrack.offsetHeight - H;
      const p = clamp(-r.top / total, 0, 1);
      const idx = clamp(Math.floor(p * tfItems.length), 0, tfItems.length - 1);
      if (idx !== tfCurrent) {
        tfCurrent = idx;
        tfItems.forEach((it, i) => { it.classList.toggle('is-active', i === idx); it.classList.toggle('is-past', i < idx); });
        tfDots.forEach((d, i) => d.classList.toggle('is-active', i === idx));
        tfScenes.forEach((sc, i) => sc.classList.toggle('is-active', i === idx));
        if (tfBig) { tfBig.classList.add('is-swap'); setTimeout(() => { tfBig.textContent = String(idx + 1).padStart(2, '0'); tfBig.classList.remove('is-swap'); }, 220); }
      }
    }

    // RUEDA DE FRENTES: las tarjetas orbitan con el scroll
    if (wheelTrack && wcards.length) {
      const r = wheelTrack.getBoundingClientRect(), total = wheelTrack.offsetHeight - H;
      const p = clamp(-r.top / total, 0, 1);
      const n = wcards.length, pos = p * (n - 1);            // posición continua 0..n-1
      const idx = clamp(Math.round(pos), 0, n - 1);
      wcards.forEach((c, i) => {
        const a = (i - pos) * wStep;                          // ángulo respecto al centro superior
        c.style.transform = `rotate(${a}deg) translateY(${-wR}px) rotate(${-a}deg) scale(${1 - Math.min(.22, Math.abs(i - pos) * .12)})`;
        c.style.zIndex = String(100 - Math.round(Math.abs(i - pos) * 10));
        c.style.opacity = String(clamp(1 - (Math.abs(i - pos) - 2.2) * .8, 0, 1));
      });
      if (idx !== wCurrent) {
        wCurrent = idx;
        wcards.forEach((c, i) => c.classList.toggle('is-active', i === idx));
        wdetails.forEach((d, i) => d.classList.toggle('is-active', i === idx));
        if (wcount) wcount.textContent = String(idx + 1).padStart(2, '0');
      }
    }

    // PROCESO: desplazamiento horizontal anclado (solo desktop)
    if (hsRow && innerWidth >= 1024 && hsW) {
      const r = hsTrack.getBoundingClientRect(), total = hsTrack.offsetHeight - H;
      const p = clamp(-r.top / total, 0, 1);
      const x = -(hsW - innerWidth) * p;
      hsRow.style.transform = `translate3d(${x}px,0,0)`;
      const center = innerWidth * .45;
      hsSteps.forEach(st => { const b = st.getBoundingClientRect(); st.classList.toggle('is-active', b.left < center && b.right > center * .5); });
    }

    // PARALLAX sutil en imágenes
    parallaxEls.forEach(el => {
      const r = el.getBoundingClientRect(); if (r.bottom < 0 || r.top > H) return;
      const f = parseFloat(el.dataset.parallax) || .1, img = el.querySelector('img');
      const off = ((r.top + r.height/2) - H/2) * f;
      if (img) img.style.transform = `translateY(${off}px) scale(1.12)`;
    });
  };

  /* ---------- FIRMA: llevar la pantalla al punto exacto y sostenerla mientras se dibuja ---------- */
  const block = e => { e.preventDefault(); };
  const blockKeys = e => { if ([' ','PageDown','PageUp','ArrowDown','ArrowUp','Home','End'].includes(e.key)) e.preventDefault(); };
  const lockScroll = () => { holding = true; window.addEventListener('wheel', block, {passive:false}); window.addEventListener('touchmove', block, {passive:false}); window.addEventListener('keydown', blockKeys); };
  const unlockScroll = () => { holding = false; window.removeEventListener('wheel', block); window.removeEventListener('touchmove', block); window.removeEventListener('keydown', blockKeys); };
  const glide = (to, ms) => new Promise(res => { const from = window.scrollY, t0 = performance.now(); const ease = t => 1 - Math.pow(1 - t, 3);
    (function step(now){ const t = clamp((now - t0) / ms, 0, 1); window.scrollTo({top: from + (to - from) * ease(t), behavior: 'instant'}); frame(); if (t < 1) requestAnimationFrame(step); else res(); })(t0); });
  function holdForSignature(target) {
    if (reduce) { sig.classList.add('is-drawing'); return; }
    lockScroll();
    glide(target, 650).then(() => {
      sig.classList.add('is-drawing');
      setTimeout(unlockScroll, 3600);   // ≈ duración del trazo + lectura de la frase
    });
  }

  /* ---------- NAVEGACIÓN CON "PINTADO" DE PANTALLA ---------- */
  const paint = $('.paint');
  let painting = false;
  const goTo = (hash) => {
    const el = document.querySelector(hash); if (!el) return;
    if (reduce || !paint) { el.scrollIntoView({behavior:'smooth'}); history.replaceState(null, '', hash); return; }
    if (painting || holding) return; painting = true;
    paint.classList.remove('is-out'); paint.classList.add('is-in');
    setTimeout(() => {
      const y = el.getBoundingClientRect().top + window.scrollY - (el.classList.contains('services') || el.classList.contains('transform') || el.classList.contains('process') ? 0 : 0);
      window.scrollTo({top: y, behavior:'instant' in window ? 'instant' : 'auto'});
      history.replaceState(null, '', hash);
      frame();
      $$('.reveal, .split', el).forEach(r => r.classList.add('is-in'));
      paint.classList.remove('is-in'); paint.classList.add('is-out');
      setTimeout(() => { paint.classList.remove('is-out'); painting = false; }, 750);
    }, 780);
  };
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const hash = a.getAttribute('href'); if (!hash || hash === '#' || hash === '#main') return;
    e.preventDefault();
    if (menu && menu.classList.contains('is-open')) { burger.setAttribute('aria-expanded','false'); menu.classList.remove('is-open'); document.documentElement.classList.remove('lock'); }
    goTo(hash);
  }));

  let ticking = false;
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { frame(); ticking = false; }); } };
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', () => { measure(); frame(); });
  window.addEventListener('load', () => { measure(); frame(); });
  if (figImg) figImg.addEventListener('load', frame);
  measure(); frame();

  /* ---------- Clic en tarjeta de la rueda: la lleva al frente ---------- */
  wcards.forEach((c, i) => c.addEventListener('click', () => {
    const total = wheelTrack.offsetHeight - vh(); const top = wheelTrack.getBoundingClientRect().top + window.scrollY;
    glide(top + total * (i / (wcards.length - 1)), 700);
  }));

  /* ---------- Cambio de idioma: conserva la sección en la que estás ---------- */
  $$('a.lang').forEach(a => a.addEventListener('click', () => { if (location.hash) a.href = a.getAttribute('href').split('#')[0] + location.hash; }));

  /* ---------- WhatsApp flotante ---------- */
  const fl = $('.wa-float');
  if (fl) {
    let shown = false;
    const show = () => { if (!shown) { shown = true; fl.classList.add('is-visible'); } };
    setTimeout(show, 4000);
    window.addEventListener('scroll', () => { if (scrollY > 200) show(); }, {passive:true});
  }

  /* ---------- FAQ: solo uno abierto ---------- */
  const faqs = $$('.faq-list details');
  faqs.forEach(d => d.addEventListener('toggle', () => { if (d.open) faqs.forEach(o => { if (o !== d) o.open = false; }); }));

  /* ---------- Eventos de conversión (GA4 si existe) ---------- */
  $$('a[href*="wa.me"]').forEach(a => a.addEventListener('click', () => {
    if (typeof gtag === 'function') gtag('event', 'whatsapp_click', {cta: a.dataset.cta || a.textContent.trim()});
  }));
})();
