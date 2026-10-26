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
import obsah_cizi

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

NAV_EN = [
    ("Services", "sluzby", [
        ("Services overview", "en-services.html"),
        ("PV commissioning", "en-services.html#commissioning"),
        ("Remote control and balancing services", "en-services.html#rizeni"),
        ("MV switchgear and substations", "en-services.html#vn"),
        ("Commercial and utility-scale PV", "en-services.html#fve"),
        ("Service and maintenance", "en-services.html#servis"),
    ]),
    ("Grid compliance", "rfg", "en-grid-compliance.html"),
    ("Battery storage", "bess", "en-battery-storage.html"),
    ("References", "reference", "en-references.html"),
    ("About us", "onas", "en-about.html"),
    ("Contact", "kontakt", "en-contact.html"),
]

NAV_DE = [
    ("Leistungen", "sluzby", [
        ("Überblick", "de-leistungen.html"),
        ("Inbetriebnahme von PV-Anlagen", "de-leistungen.html#commissioning"),
        ("Leitstellenanbindung und Regelleistung", "de-leistungen.html#rizeni"),
        ("Mittelspannung und Trafostationen", "de-leistungen.html#vn"),
        ("Gewerbliche und große PV-Anlagen", "de-leistungen.html#fve"),
        ("Service und Wartung", "de-leistungen.html#servis"),
    ]),
    ("Netzkonformität", "rfg", "de-netzkonformitaet.html"),
    ("Batteriespeicher", "bess", "de-batteriespeicher.html"),
    ("Referenzen", "reference", "de-referenzen.html"),
    ("Über uns", "onas", "de-ueber-uns.html"),
    ("Kontakt", "kontakt", "de-kontakt.html"),
]

NAVIGACE = {"cs": NAV, "en": NAV_EN, "de": NAV_DE}

# Protejsky stranek mezi jazyky – podle nich se sklada prepinac i hreflang.
EKVIVALENTY = [
    ("index.html", "en.html", "de.html"),
    ("sluzby.html", "en-services.html", "de-leistungen.html"),
    ("simulacni-zkousky.html", "en-grid-compliance.html", "de-netzkonformitaet.html"),
    ("bateriova-uloziste.html", "en-battery-storage.html", "de-batteriespeicher.html"),
    ("reference.html", "en-references.html", "de-referenzen.html"),
    ("o-nas.html", "en-about.html", "de-ueber-uns.html"),
    ("kontakt.html", "en-contact.html", "de-kontakt.html"),
    ("zasady-zpracovani-osobnich-udaju.html", "en-privacy.html", "de-datenschutz.html"),
]
POZICE = {"cs": 0, "en": 1, "de": 2}

# Popisky sablony v jednotlivych jazycich (menu, paticka, vyzva ke kontaktu).
TEXTY = {
    "cs": {"faq": "Ptáte se", "jazyk": "Jazyk", "nav": "Hlavní navigace", "uvod": "Úvod",
           "cta": "Nezávazná poptávka", "cta_kratky": "Poptávka",
           "otevrit": "Otevřít menu", "zavrit": "Zavřít menu",
           "uvodni_stranka": "BFK Systems – úvodní stránka",
           "paticka_claim": "Partner pro velké FVE projekty a bateriová úložiště po celé ČR.",
           "kontakt": "Kontakt", "sluzby": "Služby", "spolecnost": "Společnost",
           "nase_weby": "Naše weby", "prava": "všechna práva vyhrazena",
           "zasady": "Zásady zpracování osobních údajů", "souvisejici": "Související stránky",
           "ico": "IČO", "dic": "DIČ", "zeme": "Česká republika"},
    "en": {"faq": "You asked", "jazyk": "Language", "nav": "Main navigation", "uvod": "Home",
           "cta": "Request a quote", "cta_kratky": "Enquiry",
           "otevrit": "Open menu", "zavrit": "Close menu",
           "uvodni_stranka": "BFK Systems – home",
           "paticka_claim": "Partner for utility-scale PV projects and battery storage across Czechia.",
           "kontakt": "Contact", "sluzby": "Services", "spolecnost": "Company",
           "nase_weby": "Our websites", "prava": "all rights reserved",
           "zasady": "Privacy policy", "souvisejici": "Related pages",
           "ico": "Company ID", "dic": "VAT ID", "zeme": "Czech Republic"},
    "de": {"faq": "Sie fragen", "jazyk": "Sprache", "nav": "Hauptnavigation", "uvod": "Startseite",
           "cta": "Unverbindliche Anfrage", "cta_kratky": "Anfrage",
           "otevrit": "Menü öffnen", "zavrit": "Menü schließen",
           "uvodni_stranka": "BFK Systems – Startseite",
           "paticka_claim": "Partner für große PV-Projekte und Batteriespeicher in ganz Tschechien.",
           "kontakt": "Kontakt", "sluzby": "Leistungen", "spolecnost": "Unternehmen",
           "nase_weby": "Unsere Websites", "prava": "alle Rechte vorbehalten",
           "zasady": "Datenschutz", "souvisejici": "Verwandte Seiten",
           "ico": "Firmen-ID (IČO)", "dic": "USt-IdNr.", "zeme": "Tschechische Republik"},
}

JAZYKY = [("cs", "CS", "Česky"), ("en", "EN", "English"), ("de", "DE", "Deutsch")]


def protejsky(slug: str) -> dict[str, str]:
    """Pro dany slug vrati slugy stejne stranky ve vsech jazycich."""
    for radek in EKVIVALENTY:
        if slug in radek:
            return {kod: radek[POZICE[kod]] for kod in POZICE}
    return {kod: radek[POZICE[kod]] for kod in POZICE for radek in [EKVIVALENTY[0]]}


def domovska(jazyk: str) -> str:
    return EKVIVALENTY[0][POZICE[jazyk]]


def prepinac(aktivni: str, trida: str = "lang", slug: str = "index.html") -> str:
    cile = protejsky(slug)
    odkazy = []
    for kod, zkratka, nazev in JAZYKY:
        aktualni = ' aria-current="true"' if kod == aktivni else ""
        odkazy.append(f'<a href="{cile[kod]}" lang="{kod}" hreflang="{kod}" title="{nazev}"{aktualni}>{zkratka}</a>')
    return (f'<div class="{trida}" role="navigation" aria-label="{TEXTY[aktivni]["jazyk"]}">'
            + "".join(odkazy) + "</div>")


# Hlavicka i paticka jsou tmave (tema „technicky, tmavy“) – proto bile logo.
LOGO_IMG = """<picture>
          <source type="image/webp" srcset="assets/bfk-logo-white-210.webp 210w, assets/bfk-logo-white-420.webp 420w" sizes="{sizes}">
          <img src="assets/bfk-logo-white-420.png" alt="BFK Systems s.r.o." width="420" height="170" srcset="assets/bfk-logo-white-210.png 210w, assets/bfk-logo-white-420.png 420w" sizes="{sizes}">
        </picture>"""

IKONA_TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.35 1.79.68 2.64a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.44-1.25a2 2 0 0 1 2.11-.45c.85.33 1.74.56 2.64.68A2 2 0 0 1 22 16.92z"/></svg>'
IKONA_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>'


# ------------------------------------------------------------- sablona -----
def hlavicka(aktivni: str, jazyk: str = "cs", slug: str = "index.html") -> str:
    """Sticky hlavicka s rozbalovacim menu sluzeb."""
    t = TEXTY[jazyk]
    kontakt_slug = protejsky("kontakt.html")[jazyk]
    polozky = []
    for nazev, klic, cil in NAVIGACE[jazyk]:
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
    for nazev, _klic, cil in NAVIGACE[jazyk]:
        if isinstance(cil, str):
            mobil.append(f'  <a href="{cil}">{nazev}</a>')
        else:
            mobil.append(f'  <p class="m-group">{nazev}</p>')
            mobil.extend(f'  <a class="m-sub" href="{href}">{txt}</a>' for txt, href in cil)
    mobil.append(f'  <a class="cta-mobile" href="{kontakt_slug}#formular">{t["cta"]}</a>')
    mobil.append("  " + prepinac(jazyk, "m-lang", slug))
    mobilni = "\n".join(mobil)

    return f"""<!-- HLAVICKA (generovano z nastroje/build.py) -->
<header class="site-header">
  <div class="container row">
    <div class="brand-wrap">
      <a class="brand" href="{domovska(jazyk)}" aria-label="{t["uvodni_stranka"]}">
        {LOGO_IMG.format(sizes='128px')}
      </a>
    </div>
    <nav class="primary" aria-label="{t["nav"]}">
{menu}
      <a class="header-cta" href="{kontakt_slug}#formular"><span class="dlouhy">{t["cta"]}</span><span class="kratky">{t["cta_kratky"]}</span></a>
    </nav>
    {prepinac(jazyk, "lang", slug)}
    <button class="hamburger" id="menu-open" type="button" aria-label="{t["otevrit"]}" aria-expanded="false" aria-controls="mmenu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
  </div>
</header>

<div class="mobile-menu" id="mmenu" role="dialog" aria-modal="true" aria-label="{t["nav"]}">
  <button class="close" id="menu-close" type="button" aria-label="{t["zavrit"]}">
    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
  </button>
{mobilni}
</div>
"""


def paticka(jazyk: str = "cs") -> str:
    t = TEXTY[jazyk]
    nav = NAVIGACE[jazyk]
    pro = lambda cs: protejsky(cs)[jazyk]
    sluzby = next(cil for _n, klic, cil in nav if klic == "sluzby")
    odkazy_sluzeb = "\n".join(f'      <a href="{href}">{txt}</a>' for txt, href in sluzby[1:])
    dalsi = [(nazev, cil) for nazev, klic, cil in nav
             if klic in ("rfg", "bess") and isinstance(cil, str)]
    odkazy_dalsi = "\n".join(f'      <a href="{href}">{txt}</a>' for txt, href in dalsi)
    spolecnost = [(nazev, cil) for nazev, klic, cil in nav
                  if klic in ("reference", "onas", "kontakt") and isinstance(cil, str)]
    odkazy_spolecnost = "\n".join(f'      <a href="{href}">{txt}</a>' for txt, href in spolecnost)
    return f"""<!-- PATICKA {jazyk.upper()} -->
<footer class="site">
  <div class="container grid">
    <div class="logo-cell">
      {LOGO_IMG.format(sizes='150px')}
      <span class="foot-claim">{t["paticka_claim"]}</span>
    </div>
    <div>
      <h4>{t["kontakt"]}</h4>
      <div><span class="lbl">Tel</span><a href="tel:{TEL_HREF}" style="display:inline">{TEL}</a></div>
      <div><span class="lbl">Mail</span><a href="mailto:{MAIL}" style="display:inline">{MAIL}</a></div>
      <div style="margin-top:10px">Obchodní 455/12<br>Děčín V-Rozbělesy<br>405 02 Děčín</div>
      <div style="margin-top:10px">{t["ico"]} 23571853<br>{t["dic"]} CZ23571853</div>
    </div>
    <div>
      <h4>{t["sluzby"]}</h4>
{odkazy_sluzeb}
{odkazy_dalsi}
    </div>
    <div>
      <h4>{t["spolecnost"]}</h4>
{odkazy_spolecnost}
      <h4 class="dalsi">{t["nase_weby"]}</h4>
      <a href="{WEB_SZ}" target="_blank" rel="noopener">simulacni-zkousky.cz</a>
      <a href="{WEB_BFT}" target="_blank" rel="noopener">bftechnology.cz</a>
    </div>
  </div>
  <div class="copy">
    <div class="container row">
      <span>© <span id="year">{date.today().year}</span> {FIRMA} – {t["prava"]}</span>
      <span><a href="{pro("zasady-zpracovani-osobnich-udaju.html")}">{t["zasady"]}</a></span>
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


def drobecky(cesta: list[tuple[str, str]], nazev: str, jazyk: str = "cs") -> tuple[str, str]:
    """HTML drobeckove navigace + JSON-LD BreadcrumbList."""
    dom = domovska(jazyk)
    uvod = TEXTY[jazyk]["uvod"]
    adresa = f"{DOMENA}/" if jazyk == "cs" else f"{DOMENA}/{dom}"
    kusy = [f'      <a href="{dom}">{uvod}</a> <span>›</span>']
    body = [{"@type": "ListItem", "position": 1, "name": uvod, "item": adresa}]
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


def faq_blok(polozky: list[tuple[str, str]], nadpis: str = "Časté dotazy",
             jazyk: str = "cs") -> tuple[str, str]:
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
      <p class="eyebrow">{TEXTY[jazyk]["faq"]}</p>
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
    jazyk = p.get("jazyk", "cs")
    if p.get("breadcrumb") is not None and slug != domovska(jazyk):
        bc_html, bc_ld = drobecky(p.get("breadcrumb", []), p.get("bc_nazev", p["h1"]), jazyk)

    faq_html, faq_ld = faq_blok(p.get("faq", []), p.get("faq_nadpis", "Časté dotazy"),
                                p.get("jazyk", "cs"))

    ldjson = ""
    specialni = [organizace(), web()] if slug == "index.html" else []
    if p.get("sluzba"):
        specialni.append(sluzba(p["sluzba"], p["desc"], url))
    for data in (*specialni, bc_ld, faq_ld):
        if data:
            ldjson += f'\n<script type="application/ld+json">\n{data}\n</script>'

    robots = '\n<meta name="robots" content="noindex">' if p.get("noindex") else ""
    locale = {"cs": "cs_CZ", "en": "en_GB", "de": "de_DE"}[jazyk]
    preskocit = {"cs": "Přeskočit na hlavní obsah", "en": "Skip to main content",
                 "de": "Zum Hauptinhalt springen"}[jazyk]
    cile = protejsky(slug)
    alternativy = ""
    for kod in ("cs", "en", "de"):
        cil = cile[kod]
        adresa = f"{DOMENA}/" if cil == "index.html" else f"{DOMENA}/{cil}"
        alternativy += f'\n<link rel="alternate" hreflang="{kod}" href="{adresa}">'
    alternativy += f'\n<link rel="alternate" hreflang="x-default" href="{DOMENA}/">'

    hlava = f"""<!DOCTYPE html>
<html lang="{jazyk}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no, viewport-fit=cover">
<title>{titulek}</title>
<meta name="description" content="{html.escape(p["desc"], quote=True)}">{robots}
<link rel="canonical" href="{url}">{alternativy}
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
      <span class="t">{TEXTY[jazyk]["souvisejici"]}</span>
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

    kontakt = "" if p.get("bez_kontaktu") else kontakt_pruh(jazyk)
    return (hlava + hlavicka(p.get("nav", ""), jazyk, slug) + '<main id="obsah">\n'
            + uvod + pruh + p["body"] + faq_html + cross + zdroj + kontakt + "</main>\n"
            + paticka(jazyk) + "\n</body>\n</html>\n")


# Vyzva ke kontaktu nad patickou – na kazde strance krome kontaktu.
VYZVA = {
    "cs": ("Poptávka", "Máte projekt?<br>Probereme ho.",
           "Máte zájem o spolupráci nebo potřebujete konzultaci? Napište nám, co řešíte – ozveme se do dvou pracovních dnů.",
           "Co nám napsat",
           "Čím více toho víme předem, tím přesněji odpovíme. Hodí se místo realizace, výkon elektrárny nebo úložiště, distributor a termín, se kterým počítáte.",
           "Přejít na poptávkový formulář"),
    "en": ("Enquiry", "Got a project?<br>Let's go through it.",
           "Looking for a partner or a second opinion? Tell us what you are solving – we reply within two working days.",
           "What to tell us",
           "The more we know up front, the more precise our answer is. Useful details: site location, plant or storage capacity, the distribution operator and your target date.",
           "Go to the enquiry form"),
    "de": ("Anfrage", "Sie haben ein Projekt?<br>Reden wir darüber.",
           "Sie suchen einen Partner oder eine zweite Meinung? Schreiben Sie uns, worum es geht – wir antworten innerhalb von zwei Arbeitstagen.",
           "Was uns hilft",
           "Je mehr wir vorab wissen, desto genauer ist unsere Antwort. Nützlich sind Standort, Leistung der Anlage oder des Speichers, der Verteilnetzbetreiber und Ihr Wunschtermin.",
           "Zum Anfrageformular"),
}


def kontakt_pruh(jazyk: str = "cs") -> str:
    eyebrow, nadpis, text, karta_h, karta_p, tlacitko = VYZVA[jazyk]
    kontakt_slug = protejsky("kontakt.html")[jazyk]
    return f"""<section class="contact-section" id="poptavka">
  <div class="bg"><picture>
    <source type="image/webp" srcset="assets/title-photo-1024.webp 1024w, assets/title-photo.webp 2048w" sizes="(max-width: 980px) 100vw, 33vw">
    <img src="assets/title-photo.jpg" alt="" aria-hidden="true" loading="lazy" width="2048" height="1536" srcset="assets/title-photo-1024.jpg 1024w, assets/title-photo.jpg 2048w" sizes="(max-width: 980px) 100vw, 33vw">
  </picture></div>
  <div class="container contact-grid">
    <div class="contact-aside">
      <p class="eyebrow">{eyebrow}</p>
      <h2>{nadpis}</h2>
      <p>{text}</p>
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
        {TEXTY[jazyk]["ico"]} 23571853 · {TEXTY[jazyk]["dic"]} CZ23571853
      </div>
    </div>
    <div class="contact-form-card">
      <h3 style="margin:0 0 14px;font-size:20px;color:#222">{karta_h}</h3>
      <p style="margin:0 0 18px;font-size:15px">{karta_p}</p>
      <a class="btn btn-primary" href="{kontakt_slug}#formular">{tlacitko}</a>
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


# Apache na Webglobe. Vedle webu z repozitare tam lezi RfG portal, dotaznik
# a stary formular, deploy je nesmi prepsat. Soubor proto resi jen vlastni
# chybovou stranku a poradi uvodnich souboru - v public_html/ zustava i stary
# index.php, ktery by jinak mohl vyhrat nad novym index.html.
HTACCESS = """# bfksystems.cz na Webglobe. Nasazuje GitHub Actions (SFTP) z repozitáře BFtech22/bfksystems.cz.
# Generuje nastroje/build.py – needituj ručně.
# RfG/, dotaznik/, PHPMailer/, send_email.php jsou na serveru mimo repozitář – nemazat.
# HTTP -> HTTPS přesměrovává hosting, tady se neřeší.
DirectoryIndex index.html index.php
ErrorDocument 404 /404.html
"""


def absolutni_odkazy(kod: str) -> str:
    """Cesty od korene pro stranku 404.

    Chybova stranka se zobrazi i na adrese typu /RfG/neexistuje. Relativni odkaz
    by se tam hledal v podslozce, takze by zmizel styl i obrazky a menu by vedlo
    na neexistujici stranky.
    """
    def od_korene(adresa: str) -> str:
        if re.match(r"^(?:[a-zA-Z][\w+.-]*:|//|/|#|\?)", adresa):
            return adresa
        return "/" + adresa

    def srcset(m: re.Match) -> str:
        polozky = []
        for kus in m.group(1).split(","):
            kus = kus.strip()
            if not kus:
                continue
            adresa, _, popis = kus.partition(" ")
            polozky.append(" ".join(filter(None, (od_korene(adresa), popis.strip()))))
        return 'srcset="' + ", ".join(polozky) + '"'

    kod = re.sub(r'srcset="([^"]+)"', srcset, kod)
    return re.sub(r'\b(href|src)="([^"]+)"', lambda m: f'{m.group(1)}="{od_korene(m.group(2))}"', kod)


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
    stranky = obsah.PAGES + obsah_cizi.PAGES
    slugy = [p["slug"] for p in stranky]
    if len(slugy) != len(set(slugy)):
        raise SystemExit("duplicitni slug v obsah.PAGES")
    nezname = sorted(set(getattr(obsah, "ZDROJE", {})) - set(slugy))
    if nezname:
        raise SystemExit("obsah.ZDROJE odkazuji na neexistujici stranky: " + ", ".join(nezname))

    for p in stranky:
        cil = KOREN / p["slug"]
        kod = stranka(p)
        if p["slug"] == "404.html":
            kod = absolutni_odkazy(kod)
        cil.write_text(kod, encoding="utf-8")
        print(f"  {p['slug']:42s} {cil.stat().st_size // 1024:3d} kB")

    (KOREN / "sitemap.xml").write_text(sitemap(stranky), encoding="utf-8")
    (KOREN / ".htaccess").write_text(HTACCESS, encoding="utf-8")
    print(f"\n{len(stranky)} stránek + sitemap.xml + .htaccess")


if __name__ == "__main__":
    main()
