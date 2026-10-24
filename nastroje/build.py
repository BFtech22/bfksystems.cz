#!/usr/bin/env python3
"""Generator webu bfksystems.cz (BFK Systems s.r.o.).

Sablona a komponenty vychazeji z webu simulacni-zkousky.cz (stejna barevnost,
pismo Roboto hostovane u nas, stejne CSS). Vsechny stranky maji spolecnou
hlavicku, paticku a menu, proto se generuji:

    python3 nastroje/build.py

Obsah stranek je v nastroje/obsah.py, sablona a menu tady. Vygenerovane .html
soubory v korenu se needituji rucne – build je pri dalsim spusteni prepise.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
from datetime import date
from pathlib import Path

import obsah

KOREN = Path(__file__).resolve().parent.parent
DOMENA = "https://www.bfksystems.cz"
ZNACKA = "BFK Systems"
FIRMA = "BFK Systems s.r.o."

TEL = "+420 776 111 100"
TEL_HREF = "+420776111100"
MAIL = "info@bfksystems.cz"
WEB_SZ = "https://www.simulacni-zkousky.cz/"
WEB_BFT = "https://www.bftechnology.cz/"

# ---------------------------------------------------------------- menu -----
# (nazev, klic pro zvyrazneni, polozky | odkaz)
NAV = [
    ("Služby", "sluzby", [
        ("Přehled služeb", "sluzby.html"),
        ("Commissioning FVE", "sluzby.html#commissioning"),
        ("Dispečerské řízení a SVR", "sluzby.html#rizeni"),
        ("VN a trafostanice", "sluzby.html#vn"),
        ("Komerční a velké FVE", "sluzby.html#fve"),
        ("Servis a servisní smlouvy", "sluzby.html#servis"),
    ]),
    ("Simulační zkoušky", "rfg", "simulacni-zkousky.html"),
    ("Bateriová úložiště", "bess", "bateriova-uloziste.html"),
    ("Reference", "reference", "reference.html"),
    ("O nás", "onas", "o-nas.html"),
    ("Kontakt", "kontakt", "kontakt.html"),
]

# Prepinac jazyku. EN a DE zatim vedou na zastupne stranky („verzi pripravujeme“),
# ktere se neindexuji – az budou preklady, nahradi je plne verze.
JAZYKY = [("cs", "CS", "index.html", "Česky"),
          ("en", "EN", "en.html", "English"),
          ("de", "DE", "de.html", "Deutsch")]


def prepinac(aktivni: str, trida: str = "lang") -> str:
    odkazy = []
    for kod, zkratka, href, nazev in JAZYKY:
        aktualni = ' aria-current="true"' if kod == aktivni else ""
        odkazy.append(f'<a href="{href}" lang="{kod}" hreflang="{kod}" title="{nazev}"{aktualni}>{zkratka}</a>')
    popis = {"cs": "Jazyk", "en": "Language", "de": "Sprache"}[aktivni]
    return f'<div class="{trida}" role="navigation" aria-label="{popis}">' + "".join(odkazy) + "</div>"


# Hlavicka i paticka jsou tmave (tema „technicky, tmavy“) – proto bile logo.
LOGO_IMG = """<picture>
          <source type="image/webp" srcset="assets/bfk-logo-white-210.webp 210w, assets/bfk-logo-white-420.webp 420w" sizes="{sizes}">
          <img src="assets/bfk-logo-white-420.png" alt="BFK Systems s.r.o." width="420" height="170" srcset="assets/bfk-logo-white-210.png 210w, assets/bfk-logo-white-420.png 420w" sizes="{sizes}">
        </picture>"""

IKONA_TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.35 1.79.68 2.64a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.44-1.25a2 2 0 0 1 2.11-.45c.85.33 1.74.56 2.64.68A2 2 0 0 1 22 16.92z"/></svg>'
IKONA_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>'


# ------------------------------------------------------------- sablona -----
def hlavicka(aktivni: str) -> str:
    """Sticky hlavicka s rozbalovacim menu sluzeb."""
    polozky = []
    for nazev, klic, cil in NAV:
        if isinstance(cil, str):
            tridy = ' class="active"' if klic == aktivni else ""
            aria = ' aria-current="page"' if klic == aktivni else ""
            polozky.append(f'      <a{tridy} href="{cil}"{aria}>{nazev}</a>')
            continue
        je_aktivni = klic == aktivni
        podpolozky = "\n".join(f'          <a href="{href}">{txt}</a>' for txt, href in cil)
        polozky.append(
            f'      <div class="has-sub{" is-active" if je_aktivni else ""}">\n'
            f'        <button class="sub-toggle" type="button" aria-expanded="false">\n'
            f'          {nazev} <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>\n'
            f'        </button>\n'
            f'        <div class="sub">\n{podpolozky}\n        </div>\n'
            f'      </div>'
        )
    menu = "\n".join(polozky)

    mobil = []
    for nazev, _klic, cil in NAV:
        if isinstance(cil, str):
            mobil.append(f'  <a href="{cil}">{nazev}</a>')
        else:
            mobil.append(f'  <p class="m-group">{nazev}</p>')
            mobil.extend(f'  <a class="m-sub" href="{href}">{txt}</a>' for txt, href in cil)
    mobil.append('  <a class="cta-mobile" href="kontakt.html#formular">Nezávazná poptávka</a>')
    mobil.append("  " + prepinac("cs", "m-lang"))
    mobilni = "\n".join(mobil)

    return f"""<!-- HLAVICKA (generovano z nastroje/build.py) -->
<header class="site-header">
  <div class="container row">
    <div class="brand-wrap">
      <a class="brand" href="index.html" aria-label="BFK Systems – úvodní stránka">
        {LOGO_IMG.format(sizes='128px')}
      </a>
    </div>
    <nav class="primary" aria-label="Hlavní navigace">
{menu}
      <a class="header-cta" href="kontakt.html#formular"><span class="dlouhy">Nezávazná poptávka</span><span class="kratky">Poptávka</span></a>
    </nav>
    {prepinac("cs")}
    <button class="hamburger" id="menu-open" type="button" aria-label="Otevřít menu" aria-expanded="false" aria-controls="mmenu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
  </div>
</header>

<div class="mobile-menu" id="mmenu" role="dialog" aria-modal="true" aria-label="Hlavní navigace">
  <button class="close" id="menu-close" type="button" aria-label="Zavřít menu">
    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
  </button>
{mobilni}
</div>
"""


def paticka() -> str:
    sluzby = next(cil for nazev, _k, cil in NAV if nazev == "Služby")
    odkazy_sluzeb = "\n".join(f'      <a href="{href}">{txt}</a>' for txt, href in sluzby[1:])
    return f"""<!-- PATICKA -->
<footer class="site">
  <div class="container grid">
    <div class="logo-cell">
      {LOGO_IMG.format(sizes='150px')}
      <span class="foot-claim">Partner pro velké FVE projekty a bateriová úložiště po celé ČR.</span>
    </div>
    <div>
      <h4>Kontakt</h4>
      <div><span class="lbl">Tel</span><a href="tel:{TEL_HREF}" style="display:inline">{TEL}</a></div>
      <div><span class="lbl">Mail</span><a href="mailto:{MAIL}" style="display:inline">{MAIL}</a></div>
      <div style="margin-top:10px">Obchodní 455/12<br>Děčín V-Rozbělesy<br>405 02 Děčín</div>
      <div style="margin-top:10px">IČO 23571853<br>DIČ CZ23571853</div>
    </div>
    <div>
      <h4>Služby</h4>
{odkazy_sluzeb}
      <a href="simulacni-zkousky.html">Simulační zkoušky</a>
      <a href="bateriova-uloziste.html">Bateriová úložiště</a>
    </div>
    <div>
      <h4>Společnost</h4>
      <a href="reference.html">Reference</a>
      <a href="o-nas.html">O nás</a>
      <a href="kontakt.html">Kontakt</a>
      <h4 class="dalsi">Naše weby</h4>
      <a href="{WEB_SZ}" target="_blank" rel="noopener">simulacni-zkousky.cz</a>
      <a href="{WEB_BFT}" target="_blank" rel="noopener">bftechnology.cz</a>
    </div>
  </div>
  <div class="copy">
    <div class="container row">
      <span>© <span id="year">{date.today().year}</span> {FIRMA} – všechna práva vyhrazena</span>
      <span><a href="zasady-zpracovani-osobnich-udaju.html">Zásady zpracování osobních údajů</a></span>
      <span>www.bfksystems.cz</span>
    </div>
  </div>
</footer>

<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
<script src="assets/nav.js"></script>
"""


def hlavicka_cizi(jazyk: str, slug: str) -> str:
    """Hlavicka zastupne stranky EN/DE: logo a prepinac, bez ceskeho menu."""
    popis = {"en": "BFK Systems – English version", "de": "BFK Systems – deutsche Version"}[jazyk]
    return f"""<!-- HLAVICKA {jazyk.upper()} (generovano z nastroje/build.py) -->
<header class="site-header">
  <div class="container row">
    <div class="brand-wrap">
      <a class="brand" href="{slug}" aria-label="{popis}">
        {LOGO_IMG.format(sizes='128px')}
      </a>
    </div>
    {prepinac(jazyk)}
  </div>
</header>
"""


def paticka_cizi(jazyk: str) -> str:
    texty = {
        "en": ("Company ID", "VAT ID", "All rights reserved", "Czech Republic"),
        "de": ("Firmen-ID (IČO)", "USt-IdNr.", "Alle Rechte vorbehalten", "Tschechische Republik"),
    }[jazyk]
    return f"""<!-- PATICKA {jazyk.upper()} -->
<footer class="site site-cizi">
  <div class="container grid">
    <div class="logo-cell">
      {LOGO_IMG.format(sizes='150px')}
    </div>
    <div>
      <div><b>{FIRMA}</b></div>
      <div>Obchodní 455/12, 405 02 Děčín, {texty[3]}</div>
      <div>{texty[0]} 23571853 · {texty[1]} CZ23571853</div>
    </div>
    <div>
      <div><a href="tel:{TEL_HREF}">{TEL}</a></div>
      <div><a href="mailto:{MAIL}">{MAIL}</a></div>
    </div>
  </div>
  <div class="copy">
    <div class="container row">
      <span>© {date.today().year} {FIRMA} – {texty[2]}</span>
      <span>www.bfksystems.cz</span>
    </div>
  </div>
</footer>
"""


def drobecky(cesta: list[tuple[str, str]], nazev: str) -> tuple[str, str]:
    """HTML drobeckove navigace + JSON-LD BreadcrumbList."""
    kusy = ['      <a href="index.html">Úvod</a> <span>›</span>']
    body = [{"@type": "ListItem", "position": 1, "name": "Úvod", "item": f"{DOMENA}/"}]
    for i, (txt, href) in enumerate(cesta, start=2):
        kusy.append(f'      <a href="{href}">{txt}</a> <span>›</span>')
        body.append({"@type": "ListItem", "position": i, "name": txt, "item": f"{DOMENA}/{href}"})
    kusy.append(f'      <span aria-current="page">{nazev}</span>')
    body.append({"@type": "ListItem", "position": len(body) + 1, "name": nazev})
    html_nav = ('    <nav class="breadcrumb" aria-label="Drobečková navigace">\n'
                + "\n".join(kusy) + "\n    </nav>")
    ld = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                     "itemListElement": body}, ensure_ascii=False, indent=2)
    return html_nav, ld


def prosty_text(html_text: str) -> str:
    """Text odpovedi pro JSON-LD: bez znacek, bez odkazu „… →“, bez zdvojenych mezer.

    kontrola.py pouziva stejne pravidlo, aby overila, ze FAQ v JSON-LD odpovida
    viditelnemu textu stranky.
    """
    t = re.sub(r"<a [^>]*>[^<]*→</a>", "", html_text)
    t = re.sub(r"</?(p|br|li|ul|ol)\b[^>]*>", " ", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"\s+", " ", html.unescape(t))
    return re.sub(r"\s+([,.;:!?)])", r"\1", t).strip()


def faq_blok(polozky: list[tuple[str, str]], nadpis: str = "Časté dotazy") -> tuple[str, str]:
    """Akordeon + JSON-LD FAQPage."""
    if not polozky:
        return "", ""
    radky = []
    for i, (otazka, odpoved) in enumerate(polozky):
        otevreno = " open" if i == 0 else ""
        radky.append(
            f'      <details{otevreno}>\n'
            f'        <summary>{otazka}</summary>\n'
            f'        <div class="answer">{odpoved}</div>\n'
            f'      </details>'
        )
    blok = f"""<section class="block" id="faq">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Ptáte se</p>
      <h2>{nadpis}</h2>
    </div>
    <div class="faq">
{chr(10).join(radky)}
    </div>
  </div>
</section>"""
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": o,
             "acceptedAnswer": {"@type": "Answer", "text": prosty_text(a)}}
            for o, a in polozky
        ],
    }, ensure_ascii=False, indent=2)
    return blok, ld


def organizace() -> str:
    """Organization JSON-LD – jen na domovske strance."""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": f"{DOMENA}/#organizace",
        "name": FIRMA,
        "alternateName": ZNACKA,
        "url": f"{DOMENA}/",
        "logo": f"{DOMENA}/assets/bfk-logo.png",
        "image": f"{DOMENA}/assets/title-photo.jpg",
        "description": obsah.POPIS_FIRMY,
        "email": MAIL,
        "telephone": TEL,
        "vatID": "CZ23571853",
        "taxID": "23571853",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Obchodní 455/12",
            "addressLocality": "Děčín V-Rozbělesy, Děčín",
            "postalCode": "405 02",
            "addressCountry": "CZ",
        },
        "areaServed": {"@type": "Country", "name": "Česko"},
    }, ensure_ascii=False, indent=2)


def web() -> str:
    """WebSite JSON-LD – jen na domovske strance."""
    return json.dumps({
        "@context": "https://schema.org", "@type": "WebSite",
        "@id": f"{DOMENA}/#web", "name": ZNACKA, "url": f"{DOMENA}/", "inLanguage": "cs",
        "publisher": {"@id": f"{DOMENA}/#organizace"},
    }, ensure_ascii=False, indent=2)


def sluzba(nazev: str, popis: str, url: str) -> str:
    """Service JSON-LD pro stranky sluzeb (obsah.SLUZBY)."""
    return json.dumps({
        "@context": "https://schema.org", "@type": "Service",
        "name": nazev, "serviceType": nazev, "description": popis, "url": url,
        "areaServed": {"@type": "Country", "name": "Česko"},
        "provider": {"@type": "Organization", "@id": f"{DOMENA}/#organizace", "name": FIRMA},
    }, ensure_ascii=False, indent=2)


def stranka(p: dict) -> str:
    """Slozi celou HTML stranku z jednoho zaznamu obsahu."""
    slug = p["slug"]
    url = f"{DOMENA}/" if slug == "index.html" else f"{DOMENA}/{slug}"
    titulek = p["title"] if slug == "index.html" else f'{p["title"]} | {ZNACKA}'

    bc_html, bc_ld = ("", "")
    if p.get("breadcrumb") is not None and slug != "index.html":
        bc_html, bc_ld = drobecky(p.get("breadcrumb", []), p.get("bc_nazev", p["h1"]))

    faq_html, faq_ld = faq_blok(p.get("faq", []), p.get("faq_nadpis", "Časté dotazy"))

    ldjson = ""
    specialni = [organizace(), web()] if slug == "index.html" else []
    if p.get("sluzba"):
        specialni.append(sluzba(p["sluzba"], p["desc"], url))
    for data in (*specialni, bc_ld, faq_ld):
        if data:
            ldjson += f'\n<script type="application/ld+json">\n{data}\n</script>'

    robots = '\n<meta name="robots" content="noindex">' if p.get("noindex") else ""
    jazyk = p.get("jazyk", "cs")
    locale = {"cs": "cs_CZ", "en": "en_GB", "de": "de_DE"}[jazyk]
    preskocit = {"cs": "Přeskočit na hlavní obsah", "en": "Skip to main content",
                 "de": "Zum Hauptinhalt springen"}[jazyk]
    hlava = f"""<!DOCTYPE html>
<html lang="{jazyk}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no, viewport-fit=cover">
<title>{titulek}</title>
<meta name="description" content="{html.escape(p["desc"], quote=True)}">{robots}
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
<link rel="apple-touch-icon" href="assets/favicon.png">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{FIRMA}">
<meta property="og:title" content="{html.escape(p["title"], quote=True)}">
<meta property="og:description" content="{html.escape(p["desc"], quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMENA}/assets/title-photo.jpg">
<meta property="og:locale" content="{locale}">
<meta name="theme-color" content="#17181A">

<link rel="preload" href="assets/fonts/roboto-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/roboto-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/style.css">{ldjson}
</head>

<body>
<a class="skip-link" href="#obsah">{preskocit}</a>
"""

    uvod = ""
    if p.get("h1"):
        claim = f'\n      <p class="h1-claim">{p["claim"]}</p>' if p.get("claim") else ""
        eyebrow = f'\n      <p class="eyebrow">{p["eyebrow"]}</p>' if p.get("eyebrow") else ""
        uvod = f"""<section class="block page-head">
  <div class="container">
{bc_html}
    <div class="section-head">{eyebrow}
      <h1>{p["h1"]}</h1>{claim}
      {p.get("intro", "")}
    </div>
    {p.get("anchors", "")}
  </div>
</section>
"""

    pruh = ""
    if p.get("stats"):
        dlazdice = "\n".join(
            f'      <div><div class="num">{c}</div><div class="label">{l}</div></div>'
            for c, l in p["stats"]
        )
        cols = ' cols-2' if len(p["stats"]) == 2 else ""
        pruh = f'<div class="stats-band">\n  <div class="container grid{cols}">\n{dlazdice}\n  </div>\n</div>\n'

    cross = ""
    if p.get("cross"):
        odkazy = "\n".join(f'      <a href="{h}">{t}</a>' for t, h in p["cross"])
        cross = f"""<section class="block{' alt' if p.get('cross_alt') else ''}">
  <div class="container">
    <div class="crosslinks">
      <span class="t">Související stránky</span>
{odkazy}
    </div>
  </div>
</section>
"""

    zdroj = ""
    if p.get("zdroj"):
        datum, dokumenty = p["zdroj"]
        zdroj = (f'<section class="block zdroj">\n  <div class="container">\n'
                 f'    <p class="spec-note"><b>Aktualizováno {datum}.</b> Zdroje: {dokumenty}</p>\n'
                 f'  </div>\n</section>\n')

    kontakt = "" if p.get("bez_kontaktu") else KONTAKT_PRUH
    if jazyk != "cs":
        return (hlava + hlavicka_cizi(jazyk, slug) + '<main id="obsah">\n'
                + uvod + p["body"] + "</main>\n" + paticka_cizi(jazyk) + "\n</body>\n</html>\n")
    return (hlava + hlavicka(p.get("nav", "")) + '<main id="obsah">\n'
            + uvod + pruh + p["body"] + faq_html + cross + zdroj + kontakt + "</main>\n"
            + paticka() + "\n</body>\n</html>\n")


# Vyzva ke kontaktu nad patickou – na kazde strance krome kontaktu.
KONTAKT_PRUH = f"""<section class="contact-section" id="poptavka">
  <div class="bg"><picture>
    <source type="image/webp" srcset="assets/title-photo-1024.webp 1024w, assets/title-photo.webp 2048w" sizes="(max-width: 980px) 100vw, 33vw">
    <img src="assets/title-photo.jpg" alt="" aria-hidden="true" loading="lazy" width="2048" height="1536" srcset="assets/title-photo-1024.jpg 1024w, assets/title-photo.jpg 2048w" sizes="(max-width: 980px) 100vw, 33vw">
  </picture></div>
  <div class="container contact-grid">
    <div class="contact-aside">
      <p class="eyebrow">Poptávka</p>
      <h2>Máte projekt?<br>Probereme ho.</h2>
      <p>Máte zájem o spolupráci nebo potřebujete konzultaci? Napište nám, co řešíte – ozveme se do dvou pracovních dnů.</p>
      <div class="quick">
        <a href="tel:{TEL_HREF}">
          <span class="ico">{IKONA_TEL}</span>
          {TEL}
        </a>
        <a href="mailto:{MAIL}">
          <span class="ico">{IKONA_MAIL}</span>
          {MAIL}
        </a>
      </div>
      <div class="firm">
        <b>{FIRMA}</b><br>
        Obchodní 455/12, Děčín V-Rozbělesy, 405 02 Děčín<br>
        IČO 23571853 · DIČ CZ23571853
      </div>
    </div>
    <div class="contact-form-card">
      <h3 style="margin:0 0 14px;font-size:20px;color:#222">Co nám napsat</h3>
      <p style="margin:0 0 18px;font-size:15px">Čím více toho víme předem, tím přesněji odpovíme. Hodí se místo realizace, výkon elektrárny nebo úložiště, distributor a termín, se kterým počítáte.</p>
      <a class="btn btn-primary" href="kontakt.html#formular">Přejít na poptávkový formulář</a>
    </div>
  </div>
</section>
"""


def posledni_zmena(slug: str, dnes: str) -> str:
    """Datum posledni skutecne zmeny stranky (posledni commit, ktery na soubor sahl).

    Kdyz se soubor prave ted zmenil, nebo git neni k dispozici, plati dnesek.
    """
    try:
        zmeneno = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", slug],
                                 cwd=KOREN, capture_output=True).returncode
        if zmeneno:
            return dnes
        r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", slug],
                           cwd=KOREN, capture_output=True, text=True)
        return r.stdout.strip() or dnes
    except (OSError, subprocess.SubprocessError):
        return dnes


def sitemap(stranky: list[dict]) -> str:
    dnes = date.today().isoformat()
    radky = []
    for p in stranky:
        if p.get("noindex"):
            continue
        slug = p["slug"]
        loc = f"{DOMENA}/" if slug == "index.html" else f"{DOMENA}/{slug}"
        priorita = "1.0" if slug == "index.html" else p.get("prio", "0.7")
        radky.append(f"  <url>\n    <loc>{loc}</loc>\n"
                     f"    <lastmod>{posledni_zmena(slug, dnes)}</lastmod>\n"
                     f"    <priority>{priorita}</priority>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(radky) + "\n</urlset>\n")


def main() -> None:
    stranky = obsah.PAGES
    slugy = [p["slug"] for p in stranky]
    if len(slugy) != len(set(slugy)):
        raise SystemExit("duplicitni slug v obsah.PAGES")
    nezname = sorted(set(getattr(obsah, "ZDROJE", {})) - set(slugy))
    if nezname:
        raise SystemExit("obsah.ZDROJE odkazuji na neexistujici stranky: " + ", ".join(nezname))

    for p in stranky:
        cil = KOREN / p["slug"]
        cil.write_text(stranka(p), encoding="utf-8")
        print(f"  {p['slug']:42s} {cil.stat().st_size // 1024:3d} kB")

    (KOREN / "sitemap.xml").write_text(sitemap(stranky), encoding="utf-8")
    print(f"\n{len(stranky)} stránek + sitemap.xml")


if __name__ == "__main__":
    main()
