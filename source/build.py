# -*- coding: utf-8 -*-
import os, json, re, html
from urllib.parse import quote
from content import ES, EN, COMMON, SITE_URL, NAME, BRAND, EMAIL, WHATSAPP_NUMBER, LINKEDIN, INSTAGRAM

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('SITE_ROOT') or os.path.join(HERE, '..')
CSS = open(os.path.join(HERE, 'styles.css'), encoding='utf-8').read()
JS = open(os.path.join(HERE, 'main.js'), encoding='utf-8').read()
LOGO = open(os.path.join(ROOT, 'assets', 'logo.svg'), encoding='utf-8').read()
LOGO_INLINE = LOGO.replace('<svg ', '<svg aria-hidden="true" focusable="false" ', 1).replace(' role="img" aria-label="Eros Studio"', '')
SIG = open(os.path.join(HERE, 'signature.svg.frag'), encoding='utf-8').read()
SIG_FILL = re.search(r'd="(M[^"]+)"/></svg>', SIG).group(1)
SIG_VB = re.search(r'viewBox="([^"]+)"', SIG).group(1)
SIG_STATIC = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{SIG_VB}" aria-hidden="true" focusable="false"><path fill="currentColor" fill-rule="evenodd" d="{SIG_FILL}"/></svg>'
open(os.path.join(ROOT, 'assets', 'firma-eros.svg'), 'w', encoding='utf-8').write(SIG_STATIC.replace('aria-hidden="true" focusable="false"', 'role="img" aria-label="Firma de Eros Atzin Martínez Hernández"'))

WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.87 9.87 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2m0 18.15a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.24-8.24 4.54 0 8.24 3.7 8.24 8.24s-3.7 8.24-8.24 8.24m4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.12-.17.25-.64.81-.78.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.12-.14.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.22.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.28"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


MOTIF = {
 'globe': '<svg viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="1"><circle cx="100" cy="100" r="78"/><ellipse cx="100" cy="100" rx="34" ry="78"/><ellipse cx="100" cy="100" rx="62" ry="78"/><path d="M22 100h156M34 66h132M34 134h132M58 40h84M58 160h84"/><circle cx="128" cy="76" r="4" fill="currentColor" stroke="none"/><circle cx="128" cy="76" r="10" opacity=".5"/></svg>',
 'bond': '<svg viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="1"><circle cx="76" cy="100" r="46"/><circle cx="124" cy="100" r="46"/><path d="M100 60v80" opacity=".5"/><circle cx="100" cy="100" r="4" fill="currentColor" stroke="none"/></svg>',
 'expand': '<svg viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="1"><circle cx="100" cy="100" r="6" fill="currentColor" stroke="none"/><circle cx="100" cy="100" r="30" opacity=".7"/><circle cx="100" cy="100" r="60" opacity=".45"/><circle cx="100" cy="100" r="90" opacity=".25"/><path d="M100 100L160 40M100 100L40 40M100 100l60 60M100 100l-60 60"/><path d="M148 40h12v12M52 40H40v12M148 160h12v-12M52 160H40v-12"/></svg>',
 'chart': '<svg viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="1"><path d="M30 160h140M30 160V40" opacity=".4"/><path d="M40 140l30-22 28 10 30-40 34-22" stroke-width="1.4"/><circle cx="70" cy="118" r="3" fill="currentColor" stroke="none"/><circle cx="98" cy="128" r="3" fill="currentColor" stroke="none"/><circle cx="128" cy="88" r="3" fill="currentColor" stroke="none"/><circle cx="162" cy="66" r="4" fill="currentColor" stroke="none"/><path d="M162 66v94" stroke-dasharray="2 4" opacity=".5"/></svg>',
 'horizon': '<svg viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="1"><circle cx="100" cy="112" r="26"/><path d="M20 130h160" /><path d="M30 150l40-30 30 20 26-36 44 46" stroke-width="1.2"/><path d="M100 60V48M60 74l-8-8M140 74l8-8" opacity=".6"/></svg>',
 'sun': '<svg viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="1"><circle cx="100" cy="110" r="34"/><path d="M20 110h160" stroke-width="1.2"/><path d="M100 50V38M56 66l-9-9M144 66l9-9M40 110h-14M174 110h-14" opacity=".7"/><path d="M40 150h120M60 170h80" opacity=".4"/></svg>',
 'chat': '<svg viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="1"><path d="M40 60h80a12 12 0 0 1 12 12v34a12 12 0 0 1-12 12H70l-22 18v-18h-8a12 12 0 0 1-12-12V72a12 12 0 0 1 12-12z"/><path d="M92 128h56a12 12 0 0 0 12-12V96a12 12 0 0 0-12-12h-4" opacity=".6"/><path d="M160 116l14 14v-14" opacity=".6"/><circle cx="64" cy="94" r="3" fill="currentColor" stroke="none"/><circle cx="80" cy="94" r="3" fill="currentColor" stroke="none"/><circle cx="96" cy="94" r="3" fill="currentColor" stroke="none"/></svg>',
 'funnel': '<svg viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="1"><path d="M40 50h120l-44 56v44l-32 12v-56z"/><path d="M60 50v-8M100 50v-14M140 50v-8" opacity=".6"/><circle cx="60" cy="34" r="3" fill="currentColor" stroke="none"/><circle cx="100" cy="28" r="3" fill="currentColor" stroke="none"/><circle cx="140" cy="34" r="3" fill="currentColor" stroke="none"/><path d="M100 168v14" opacity=".6"/><circle cx="100" cy="186" r="4" fill="currentColor" stroke="none"/></svg>',
}
PILLAR_MOTIF = ['globe','bond','expand','chart','horizon']
SCENE_MOTIF = ['sun','chat','funnel','chart','horizon']

def esc(s): return html.escape(s, quote=True)
def wa(L): return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(L['wa_msg'])}"
def btn_wa(L, label, cls="btn btn-wa", cta=None):
    return f'<a class="{cls} magnetic" href="{wa(L)}" target="_blank" rel="noopener" data-cta="{esc(cta or label)}">{WA_ICON}<span>{esc(label)}</span></a>'
def words(text, cls="split"):
    """Envuelve cada palabra en un span para revelarla con animación."""
    return f'<span class="{cls}" aria-label="{esc(text)}">' + " ".join(f'<span class="w"><span>{esc(w)}</span></span>' for w in text.split()) + '</span>'

def jsonld(L, faq):
    person = {"@context": "https://schema.org", "@type": "Person", "@id": SITE_URL + "/#person",
        "name": NAME, "givenName": "Eros Atzin", "familyName": "Martínez Hernández", "alternateName": ["Eros Atzin", "Eros Studio"],
        "url": SITE_URL + "/", "image": SITE_URL + "/assets/eros-retrato.webp", "email": "mailto:" + EMAIL, "telephone": "+" + WHATSAPP_NUMBER,
        "jobTitle": "Estratega de crecimiento digital" if L['lang']=='es' else "Digital growth strategist",
        "worksFor": {"@id": SITE_URL + "/#org"}, "knowsLanguage": ["es", "en", "fr"],
        "knowsAbout": ["Estrategia digital", "Marketing digital", "Diseño web", "SEO", "Turismo", "Inmobiliaria", "Construcción", "Expansión internacional"],
        "nationality": {"@type": "Country", "name": "México"}, "sameAs": [u for u in [LINKEDIN, INSTAGRAM] if u]}
    org = {"@context": "https://schema.org", "@type": "ProfessionalService", "@id": SITE_URL + "/#org",
        "name": BRAND, "founder": {"@id": SITE_URL + "/#person"}, "url": SITE_URL + "/", "logo": SITE_URL + "/assets/og-image.png", "image": SITE_URL + "/assets/og-image.png",
        "description": L['description'], "email": EMAIL, "telephone": "+" + WHATSAPP_NUMBER, "priceRange": "$$",
        "areaServed": ["MX", "US", "CA", "ES", "LATAM"], "availableLanguage": ["Spanish", "English"],
        "address": {"@type": "PostalAddress", "addressRegion": "Hidalgo", "addressCountry": "MX"}, "sameAs": [u for u in [LINKEDIN, INSTAGRAM] if u],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1], "description": s[3]}} for s in L['services']['items']]}
    site = {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/", "name": BRAND, "inLanguage": L['lang'], "publisher": {"@id": SITE_URL + "/#org"}}
    faqld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return "".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>' for d in [person, org, site, faqld])

def page(L):
    P, N, H, C = L['prefix'], L['nav'], L['hero'], COMMON
    es = L['lang'] == 'es'
    faq = L['faq']['items']
    ids = dict(manifesto="manifiesto" if es else "manifesto", problem="situacion" if es else "situation", transform="imagina" if es else "imagine",
               services="como-te-ayudo" if es else "how-i-help", cases="casos" if es else "work", about="sobre-mi" if es else "about",
               process="proceso" if es else "process", faq="faq", final="empecemos" if es else "start")
    nav_items = [("#"+ids['transform'], N['growth']), ("#"+ids['services'], N['services']), ("#"+ids['cases'], N['cases']), ("#"+ids['about'], N['about']), ("#"+ids['process'], N['process']), ("#faq", N['faq'])]
    nav_links = "".join(f'<a href="{h}">{esc(t)}</a>' for h, t in nav_items)
    wa_href = wa(L)
    chap_ids = ["main", ids['manifesto'], ids['problem'], ids['transform'], ids['services'], ids['cases'], ids['about'], ids['process'], 'faq', ids['final']]
    chapters = "".join(f'<a href="#{cid}" data-chapter="{cid}"><i>{i:02d}</i><span>{esc(t)}</span></a>' for i, (cid, t) in enumerate(zip(chap_ids, L['chapters'])))

    problem_items = "".join(f'<li class="pain reveal" data-delay="{min(i,3)}"><span class="pain-n">0{i+1}</span><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></li>' for i, (t, d) in enumerate(L['problem']['items']))
    transform_items = "".join(f'<article class="tf-item" data-i="{i}"><span class="tf-n">0{i+1}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></article>' for i, (t, d) in enumerate(L['transform']['items']))
    transform_index = "".join(f'<span class="tf-dot" data-i="{i}"></span>' for i in range(len(L['transform']['items'])))
    lab = L['services']['labels']
    items = L['services']['items']
    wheel_cards = "".join(f'''<button class="wcard" type="button" data-i="{i}" aria-label="{esc(t)}"><img src="{P}assets/img/pilar-0{i+1}.webp" alt="" width="720" height="960" loading="eager" decoding="async"><span class="wcard-motif">{MOTIF[PILLAR_MOTIF[i]]}</span><span class="wcard-n">{n}</span><span class="wcard-t">{esc(t)}</span></button>''' for i,(n,t,*_ ) in enumerate(items))
    wheel_details = "".join(f'''<article class="wdetail" data-i="{i}"><h3><span class="pillar-n">{n}</span>{esc(t)}</h3>
      <div class="pillar-grid"><div><b>{esc(lab[0])}</b><p>{esc(a)}</p></div><div><b>{esc(lab[1])}</b><p>{esc(bb)}</p></div><div class="pillar-win"><b>{esc(lab[2])}</b><p>{esc(c)}</p></div></div></article>''' for i,(n,t,a,bb,c) in enumerate(items))
    transform_items = "".join(f'<article class="tf-item" data-i="{i}"><span class="tf-n">0{i+1}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></article>' for i, (t, d) in enumerate(L['transform']['items']))
    transform_scenes = "".join(f'<figure class="tf-scene" data-i="{i}"><img src="{P}assets/img/escena-0{i+1}.webp" alt="" width="1200" height="800" loading="lazy" decoding="async"><span class="tf-motif">{MOTIF[SCENE_MOTIF[i]]}</span></figure>' for i in range(len(L['transform']['items'])))
    stats = "".join(f'<div class="stat reveal" data-delay="{i}"><span class="stat-n">{esc(v)}</span><span class="stat-l">{esc(l)}</span></div>' for i, (v, l) in enumerate(L['manifesto']['stats']))

    cs = L['cases']['items'][0]; cl = cs['labels']
    case = f'''<article class="case">
      <div class="reveal img-reveal"><div class="browser"><div class="browser-bar"><i></i><i></i><i></i><span class="url">{esc(cs['url_label'])}</span></div>
        <div class="browser-body"><div class="wire" aria-hidden="true"><i class="w-nav"></i><div class="w-hero">{esc(cs['client'])}</div><div class="w-row"><i></i><i></i><i></i></div></div>
        <img src="{P}assets/caso-tekton.webp" alt="{esc(L['cases']['placeholder'])}: {esc(cs['client'])}" loading="lazy" width="1440" height="900" onerror="this.classList.add('is-missing')"></div></div></div>
      <div class="case-body reveal" data-delay="2"><h3>{esc(cs['client'])}</h3><p class="case-sector">{esc(cs['sector'])}</p>
        <div class="case-steps"><div class="case-step"><b>{esc(cl[0])}</b><span>{esc(cs['challenge'])}</span></div><div class="case-step"><b>{esc(cl[1])}</b><span>{esc(cs['solution'])}</span></div><div class="case-step"><b>{esc(cl[2])}</b><span>{esc(cs['result'])}</span></div></div>
        <blockquote class="quote">“{esc(cs['quote'])}”<footer><b>{esc(cs['author'])}</b> · {esc(cs['role'])}</footer></blockquote>
        <div class="case-actions"><a class="link-arrow" href="{cs['url']}" target="_blank" rel="noopener">{esc(L['cases']['view'])}{ARROW}</a>{btn_wa(L, L['cases']['cta'], "btn btn-ghost", cta="caso")}</div></div></article>'''

    about_p = "".join(f"<p>{esc(p)}</p>" for p in L['about']['p'])
    facts = "".join(f"<div><b>{esc(k)}</b><span>{esc(v)}</span></div>" for k, v in L['about']['facts'])
    steps = "".join(f'<article class="step"><span class="step-n">0{i+1}</span><h3>{esc(t)}</h3><p>{esc(d)}</p><i class="step-line"></i></article>' for i, (t, d) in enumerate(L['process']['steps']))
    faq_html = "".join(f'<details{" open" if i==0 else ""}><summary>{esc(q)}<i></i></summary><div class="a"><p>{esc(a)}</p></div></details>' for i, (q, a) in enumerate(faq))
    trust_items = "".join(f"<span>{esc(t)}</span>" for t in L['trust']['items'])
    hero_trust = "".join(f"<li>{esc(t)}</li>" for t in H['trust'])
    socials = "".join(f'<li><a href="{u}" target="_blank" rel="noopener me">{n}</a></li>' for n, u in [("LinkedIn", LINKEDIN), ("Instagram", INSTAGRAM)] if u)
    alt_photo = f"{NAME}, fundador de Eros Studio, en traje negro y camisa blanca" if es else f"{NAME}, founder of Eros Studio, in a black suit and white shirt"
    home = P + 'index.html'

    return f'''<!DOCTYPE html>
<html lang="{L['lang']}" class="lock">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(L['title'])}</title>
<meta name="description" content="{esc(L['description'])}">
<meta name="keywords" content="{esc(L['keywords'])}">
<meta name="author" content="{NAME}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0B0B0C">
<link rel="canonical" href="{L['canonical']}">
<link rel="alternate" hreflang="es" href="{SITE_URL}/">
<link rel="alternate" hreflang="en" href="{SITE_URL}/en/">
<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">
<link rel="icon" href="{P}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{P}assets/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="{'es_MX' if es else 'en_US'}"><meta property="og:locale:alternate" content="{'en_US' if es else 'es_MX'}">
<meta property="og:title" content="{esc(L['title'])}"><meta property="og:description" content="{esc(L['description'])}">
<meta property="og:url" content="{L['canonical']}"><meta property="og:image" content="{SITE_URL}/assets/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{esc(NAME)} — {BRAND}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(L['title'])}">
<meta name="twitter:description" content="{esc(L['description'])}"><meta name="twitter:image" content="{SITE_URL}/assets/og-image.png">
<link rel="preload" as="image" href="{P}assets/eros-atzin-martinez-hernandez.webp" type="image/webp" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap">
{jsonld(L, faq)}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">{esc(L['skip'])}</a>
<div class="progress" aria-hidden="true"><i></i></div>

<div class="intro" aria-label="{esc(L['intro_aria'])}" role="presentation"><div class="intro-mark">{LOGO_INLINE}</div><div class="intro-bar"><i></i></div></div>

<header class="nav"><div class="container">
  <a class="brand" href="{home}" aria-label="{BRAND} — {esc(NAME)}">{LOGO_INLINE}</a>
  <nav class="nav-links" aria-label="{'Principal' if es else 'Main'}">{nav_links}</nav>
  <div class="nav-right">
    <a class="lang" href="{L['other_href']}" hreflang="{'en' if es else 'es'}" lang="{'en' if es else 'es'}" aria-label="{esc(L['other_lang_label'])}">{L['other_lang']}</a>
    {btn_wa(L, N['cta'], cta="nav")}
    <button class="burger" aria-expanded="false" aria-controls="mobile-menu" aria-label="{esc(N['menu'])}"><i></i></button>
  </div>
</div></header>
<div class="mobile-menu" id="mobile-menu"><nav aria-label="{'Menú móvil' if es else 'Mobile menu'}">{nav_links}</nav><div class="meta"><span>{esc(C['wa_display'])}</span><span>{EMAIL}</span><a class="lang" href="{L['other_href']}" style="justify-self:start">{esc(L['other_lang_label'])}</a></div></div>

<div class="paint" aria-hidden="true"><i></i><i></i><div class="paint-mark">{LOGO_INLINE}</div></div>
<div class="cursor" aria-hidden="true"><i></i></div>
<div class="cursor-glow" aria-hidden="true"></div>

<main id="main">
<div class="hero-track">
<section class="hero" aria-label="{'Presentación' if es else 'Introduction'}">
  <canvas class="hero-canvas" aria-hidden="true"></canvas><div class="hero-grain" aria-hidden="true"></div>
  <div class="hero-big" aria-hidden="true"><span>{H['big_a']}</span><span>{H['big_b']}</span></div>
  <div class="hero-figure"><img src="{P}assets/eros-atzin-martinez-hernandez.webp" srcset="{P}assets/eros-atzin-martinez-hernandez-sm.webp 307w, {P}assets/eros-atzin-martinez-hernandez.webp 614w" sizes="(min-width:960px) 42vw, 70vw" width="614" height="933" alt="{esc(alt_photo)}" fetchpriority="high" decoding="async"></div>
  <div class="hero-copy"><div class="container">
    <div>
      <p class="hero-eyebrow">{esc(H['eyebrow'])}</p>
      <h1>{words(H['h1_a'])} <em>{words(H['h1_b'])}</em> {words(H['h1_c'])}</h1>
      <p class="hero-sub">{esc(H['sub'])}</p>
      <div class="hero-ctas">{btn_wa(L, H['cta'], cta="hero")}<a class="link-arrow" href="#{ids['transform']}">{esc(H['cta2'])}{ARROW}</a></div>
      <ul class="hero-trust">{hero_trust}</ul>
    </div>
  </div></div>
  <div class="hero-scroll" aria-hidden="true">{esc(H['scroll'])}<i></i></div>
  <div class="sig-wrap" aria-label="{esc(NAME)}">{SIG}<p class="sig-line">{esc(H['sig_line'])}</p><p class="sig-name">{esc(NAME)}</p></div>
</section>
</div>

<div class="trust" aria-label="{esc(L['trust']['label'])}"><div class="container"><span class="trust-label">{esc(L['trust']['label'])}</span><div class="marquee"><div class="marquee-track">{trust_items}{trust_items}</div></div></div><p class="trust-years">{esc(L['trust']['years'])}</p></div>

<section class="manifesto" id="{ids['manifesto']}" aria-labelledby="h-manifesto">
  <div class="manifesto-art" aria-hidden="true"><img src="{P}assets/img/manifiesto.webp" alt="" width="1000" height="1000" loading="lazy" decoding="async"><span class="globe">{MOTIF['globe']}</span></div>
  <div class="container">
  <p class="eyebrow reveal">{esc(L['manifesto']['eyebrow'])}</p>
  <p class="fill-text" id="h-manifesto">{words(L['manifesto']['text'], 'fill')}</p>
  <div class="stats">{stats}</div>
</div></section>

<section class="problem" id="{ids['problem']}" aria-labelledby="h-problem"><div class="container">
  <div class="section-head"><div class="reveal"><p class="eyebrow">{esc(L['problem']['eyebrow'])}</p><h2 id="h-problem">{words(L['problem']['title'])}</h2></div></div>
  <ul class="pains">{problem_items}</ul>
  <p class="problem-close reveal">{esc(L['problem']['closing'])}</p>
  <div class="center reveal">{btn_wa(L, L['problem']['cta'], "btn btn-ghost", cta="situacion")}</div>
</div></section>

<section class="transform" id="{ids['transform']}" aria-labelledby="h-transform">
  <div class="tf-track"><div class="tf-sticky"><div class="container tf-grid">
    <div class="tf-left"><p class="eyebrow">{esc(L['transform']['eyebrow'])}</p><h2 id="h-transform">{esc(L['transform']['title'])}</h2>
      <div class="tf-visual" aria-hidden="true">{transform_scenes}<span class="tf-big">01</span></div>
      <div class="tf-index">{transform_index}</div></div>
    <div class="tf-items">{transform_items}</div>
  </div></div></div>
  <div class="container center tf-cta">{btn_wa(L, L['transform']['cta'], cta="imagina")}</div>
</section>

<section class="services light" id="{ids['services']}" aria-labelledby="h-services"><div class="container">
  <div class="section-head"><div class="reveal"><p class="eyebrow">{esc(L['services']['eyebrow'])}</p><h2 id="h-services">{words(L['services']['title'])}</h2></div><p class="lead reveal" data-delay="1">{esc(L['services']['sub'])}</p></div>
</div>
  <div class="wheel-track"><div class="wheel-sticky">
    <div class="wheel-stage"><div class="wheel">{wheel_cards}</div></div>
    <div class="container wheel-bottom">
      <div class="wheel-meta"><span class="wheel-count"><b>01</b> {esc(L['services']['wheel']['counter'])} 0{len(items)}</span><span class="wheel-hint">{esc(L['services']['wheel']['hint'])}</span></div>
      <div class="wdetails">{wheel_details}</div>
    </div>
  </div></div>
  <div class="container services-foot reveal"><p>{esc(L['services']['note'])}</p>{btn_wa(L, L['services']['cta'], cta="servicios")}</div>
</section>

<section id="{ids['cases']}" aria-labelledby="h-cases"><div class="container">
  <div class="section-head"><div class="reveal"><p class="eyebrow">{esc(L['cases']['eyebrow'])}</p><h2 id="h-cases">{words(L['cases']['title'])}</h2></div></div>
  {case}
</div></section>

<section class="about" id="{ids['about']}" aria-labelledby="h-about"><div class="container about-grid">
  <div class="about-photo reveal img-reveal" data-parallax="0.12"><img src="{P}assets/eros-retrato.webp" width="768" height="1024" loading="lazy" decoding="async" alt="{esc(alt_photo)}"><div class="sig-small">{SIG_STATIC}</div></div>
  <div class="reveal" data-delay="2"><p class="eyebrow">{esc(L['about']['eyebrow'])}</p><h2 id="h-about">{words(L['about']['title'])}</h2>{about_p}<div class="facts">{facts}</div>{btn_wa(L, L['about']['cta'], cta="sobre-mi")}</div>
</div></section>

<section class="process" id="{ids['process']}" aria-labelledby="h-process">
  <div class="container section-head"><div class="reveal"><p class="eyebrow">{esc(L['process']['eyebrow'])}</p><h2 id="h-process">{words(L['process']['title'])}</h2></div></div>
  <div class="hs-track"><div class="hs-sticky" data-label="{esc(L['process']['eyebrow'])} · {esc(L['process']['title'])}"><div class="hs-row">{steps}<div class="step step-cta"><span class="step-n">→</span><h3>{esc(L['final']['title_b'])}</h3>{btn_wa(L, L['process']['cta'], cta="proceso")}</div></div></div></div>
</section>

<section id="faq" aria-labelledby="h-faq"><div class="container">
  <div class="section-head"><div class="reveal"><p class="eyebrow">{esc(L['faq']['eyebrow'])}</p><h2 id="h-faq">{words(L['faq']['title'])}</h2></div></div>
  <div class="faq-list reveal">{faq_html}</div>
  <div class="faq-more reveal"><span>{esc(L['faq']['more'])}</span>{btn_wa(L, L['faq']['cta'], "btn btn-ghost", cta="faq")}</div>
</div></section>

<section class="final" id="{ids['final']}" aria-labelledby="h-final"><div class="final-mark" aria-hidden="true">{LOGO_INLINE}</div><div class="container">
  <h2 id="h-final" class="reveal">{esc(L['final']['title_a'])}<br><em>{esc(L['final']['title_b'])}</em></h2>
  <p class="lead reveal" data-delay="1">{esc(L['final']['sub'])}</p>
  <div class="reveal" data-delay="2">{btn_wa(L, L['final']['cta'], "btn btn-wa btn-lg", cta="final")}<p class="note">{esc(L['final']['note'])}</p></div>
</div></section>
</main>

<footer class="footer"><div class="container">
  <div class="footer-grid">
    <div><a class="brand" href="{home}" aria-label="{BRAND}">{LOGO_INLINE}</a><p>{esc(L['footer']['tag'])}</p><p style="margin-top:10px;color:var(--cream-2)">{esc(NAME)}</p></div>
    <div><h4>{esc(L['footer']['contact'])}</h4><ul><li><a href="{wa_href}" target="_blank" rel="noopener">WhatsApp · {esc(C['wa_display'])}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li>{socials}</ul></div>
    <div><h4>{esc(L['footer']['nav'])}</h4><ul>{"".join(f'<li><a href="{h}">{esc(t)}</a></li>' for h,t in nav_items)}</ul></div>
    <div><h4>{esc(L['footer']['langs'])}</h4><ul><li><a href="{P}index.html" hreflang="es">Español</a></li><li><a href="{P}en/index.html" hreflang="en">English</a></li></ul></div>
  </div>
  <div class="footer-bottom"><span>© {C['year']} {BRAND} · {esc(NAME)}. {esc(L['footer']['rights'])}</span><span>{esc(L['footer']['made'])}</span><a href="#main">{esc(L['footer']['top'])} ↑</a></div>
</div></footer>

<div class="wa-float"><span class="tip">{esc(L['float_label'])}</span><a class="bubble" href="{wa_href}" target="_blank" rel="noopener" aria-label="{esc(L['float_aria'])}" data-cta="flotante">{WA_ICON}</a></div>

<script>{JS}</script>
</body>
</html>'''

os.makedirs(os.path.join(ROOT, 'en'), exist_ok=True)
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(page(ES))
open(os.path.join(ROOT, 'en', 'index.html'), 'w', encoding='utf-8').write(page(EN))
open(os.path.join(ROOT, 'robots.txt'), 'w').write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url><loc>{SITE_URL}/</loc><lastmod>2026-09-23</lastmod><changefreq>monthly</changefreq><priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="es" href="{SITE_URL}/"/><xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}/en/"/><xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}/"/></url>
  <url><loc>{SITE_URL}/en/</loc><lastmod>2026-09-23</lastmod><changefreq>monthly</changefreq><priority>0.9</priority>
    <xhtml:link rel="alternate" hreflang="es" href="{SITE_URL}/"/><xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}/en/"/><xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}/"/></url>
</urlset>
''')
open(os.path.join(ROOT, 'assets', 'favicon.svg'), 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0B0B0C"/><text x="32" y="45" text-anchor="middle" font-family="Cormorant Garamond,Georgia,serif" font-size="40" fill="#EDEBE6">E</text><circle cx="47" cy="19" r="3" fill="#C9A96E"/></svg>')
print("built")
