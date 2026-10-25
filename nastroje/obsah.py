#!/usr/bin/env python3
"""Obsah webu bfksystems.cz – jedna polozka STRANKY = jedna stranka.

Vznik 17. 9. 2026 jako nahrada jednostrankoveho webu bfksystems.cz (Tailwind,
prepinac CS/EN/DE, formular pres send_email.php). Z puvodniho webu prevzato:
specializace (commissioning, dispecerske rizeni a SVR, VN a trafostanice,
komercni a velke FVE), servis, osm referenci s fotkami a sekce O nas vcetne
tymu. Nove pribyly stranky Simulacni zkousky (RfG) a Bateriova uloziste.

Vecny podklad: puvodni web bfksystems.cz a overene texty webu
simulacni-zkousky.cz (05_Webovky/simulacni-zkousky). Na web ZAMERNE NEDAVAT:
ceny, pocty projektu a roky praxe, ktere nikdo nedolozil, certifikace, jmena
investoru. Zatim jen cesky – EN a DE az po schvaleni ceskeho obsahu.

Zkratky: UPOS a UTP BEZ carky (tak je pise PPDS priloha 4).
"""

# ---------------------------------------------------------------- ikony ----
_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">{}</svg>')
I = {k: _SVG.format(v) for k, v in {
    "dok": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h4"/>',
    "graf": '<path d="M3 3v18h18"/><path d="m7 15 4-6 3 3 4-7"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/>',
    "blesk": '<path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/>',
    "sit": '<rect x="9" y="2" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="16" y="16" width="6" height="6" rx="1"/><path d="M12 8v4M5 16v-2h14v2"/>',
    "hodiny": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "stit": '<path d="M12 3l8 3v6c0 4.5-3.2 8.3-8 9.5C7.2 20.3 4 16.5 4 12V6z"/><path d="m9 12 2 2 4-4"/>',
    "baterie": '<rect x="2" y="7" width="17" height="10" rx="2"/><path d="M22 11v2M6 11v2M10 11v2M14 11v2"/>',
    "lupa": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "tovarna": '<path d="M3 21V10l6 4V10l6 4V7l6 4v10z"/><path d="M3 21h18"/>',
    "klic": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "lide": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "clovek": '<circle cx="12" cy="8" r="4"/><path d="M4 21v-1a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v1"/>',
    "mapa": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "panel": '<rect x="3" y="10" width="18" height="11" rx="1"/><path d="M3 15.5h18M9 10v11M15 10v11M12 2v3M5.6 4.6l1.4 1.4M18.4 4.6 17 6"/>',
    "rizeni": '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>',
    "cena": '<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "smlouva": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
}.items()}


# ------------------------------------------------------------- pomocnici ---
def sekce(nadpis, telo, eyebrow=None, uvod=None, alt=False, kotva=None):
    hlavicka = ""
    if nadpis or uvod:
        eb = f'\n      <p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
        h2 = f"\n      <h2>{nadpis}</h2>" if nadpis else ""
        u = f"\n      {uvod}" if uvod else ""
        hlavicka = f'    <div class="section-head">{eb}{h2}{u}\n    </div>\n'
    ida = f' id="{kotva}"' if kotva else ""
    return (f'<section class="block{" alt" if alt else ""}"{ida}>\n  <div class="container">\n'
            f'{hlavicka}{telo}\n  </div>\n</section>\n')


def karty(polozky, sloupce=2):
    """polozky = [(ikona, nadpis, html_telo, odkaz|None)]"""
    kusy = []
    for p in polozky:
        ikona, nadpis, telo = p[0], p[1], p[2]
        odkaz = p[3] if len(p) > 3 else None
        if odkaz:
            cil = ' target="_blank" rel="noopener"' if odkaz.startswith("http") else ""
            kusy.append(
                f'      <a class="svc" href="{odkaz}"{cil}>\n'
                f'        <h3 class="hdr">{ikona}{nadpis}</h3>\n'
                f'        <div class="body">{telo}<span class="go">Otevřít →</span></div>\n'
                f'      </a>')
        else:
            kusy.append(
                f'      <article class="svc">\n'
                f'        <h3 class="hdr">{ikona}{nadpis}</h3>\n'
                f'        <div class="body">{telo}</div>\n'
                f'      </article>')
    trida = "services" + (" cols-2" if sloupce == 2 else "")
    return f'    <div class="{trida}">\n' + "\n".join(kusy) + "\n    </div>"


def tabulka(zahlavi, radky, poznamky=(), min_sirka=None):
    """Zahlavi s prazdnymi retezci = tabulka bez hlavicky (klic–hodnota)."""
    th = "".join(f"<th>{h}</th>" for h in zahlavi)
    hlava = "" if not any(zahlavi) else f"        <thead>\n          <tr>{th}</tr>\n        </thead>\n"
    tr = "\n".join(
        "          <tr>" + "".join(f"<td>{b}</td>" for b in r) + "</tr>" for r in radky)
    styl = f' style="min-width:{min_sirka}px"' if min_sirka else ""
    pozn = "\n".join(f'    <p class="spec-note">{p}</p>' for p in poznamky)
    return (f'    <div class="spec-table">\n      <table{styl}>\n{hlava}'
            f'        <tbody>\n{tr}\n        </tbody>\n      </table>\n    </div>\n{pozn}')


def seznam(polozky):
    return ('    <ul class="checklist">\n'
            + "\n".join(f"      <li>{p}</li>" for p in polozky) + "\n    </ul>")


def cta(text, tlacitko="Nezávazná poptávka", href="kontakt.html#formular"):
    cil = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    return (f'    <div class="seg-note">\n      <p>{text}</p>\n'
            f'      <a class="btn btn-primary" href="{href}"{cil}>{tlacitko}</a>\n    </div>')


def callout(titul, text):
    return (f'    <div class="callout">\n'
            f'      <span class="t">{titul}</span>\n      {text}\n    </div>')


def kotvy(polozky):
    return ('<ul class="anchor-nav">\n'
            + "\n".join(f'      <li><a href="#{h}">{t}</a></li>' for t, h in polozky)
            + "\n    </ul>")


def foto(nazev, alt):
    """Fotka reference pres <picture> (WebP + JPG), odkaz na vetsi verzi."""
    return (f'<a class="foto" href="assets/reference/{nazev}-1600.jpg">\n'
            f'          <picture>\n'
            f'            <source type="image/webp" srcset="assets/reference/{nazev}-800.webp 800w, '
            f'assets/reference/{nazev}-1600.webp 1600w" sizes="(max-width: 880px) 100vw, 40vw">\n'
            f'            <img src="assets/reference/{nazev}-800.jpg" alt="{alt}" width="800" height="600" '
            f'loading="lazy">\n'
            f'          </picture>\n'
            f'        </a>')


def rozdeleni(text, nazev_fotky, reverse=False):
    """Text vedle fotky reference (na mobilu pod sebou)."""
    alt = REFERENCE[nazev_fotky][2]
    return (f'    <div class="split{" reverse" if reverse else ""}">\n'
            f'      <div class="txt">\n{text}\n      </div>\n'
            f'      <div class="ph">\n        {foto(nazev_fotky, alt)}\n      </div>\n'
            f'    </div>')


def galerie(nazvy, sloupce=4):
    kusy = []
    for n in nazvy:
        nadpis, popis, alt = REFERENCE[n]
        kusy.append(f'      <figure>\n        {foto(n, alt)}\n'
                    f'        <figcaption><b>{nadpis}</b><span>{popis}</span></figcaption>\n'
                    f'      </figure>')
    trida = "gallery" + (" cols-3" if sloupce == 3 else "")
    return f'    <div class="{trida}">\n' + "\n".join(kusy) + "\n    </div>"


# Osm referenci z puvodniho webu (nadpis, popis, alt fotky).
REFERENCE = {
    "bess": ("Oživení BESS",
             "Řízení podle spotových cen a integrace FVE.",
             "Otevřený kontejner bateriového úložiště s bateriovými moduly"),
    "fve-strechy": ("Instalace FVE (Sungrow)",
                    "Dispečerské řízení, SCADA, řízení vytápění a nabíjecích stanic.",
                    "Fotovoltaické panely na střeše průmyslové haly a sousední budovy"),
    "rtu-vn": ("Dispečerské řízení VN 35 kV",
               "Implementace RTU (komponenty Weidmüller) a řídicího systému pro FVE na vysokém napětí.",
               "Rozvaděč RTU s komponenty Weidmüller"),
    "stridace-sungrow": ("Průmyslová FVE",
                         "Instalace střídačů Sungrow a AC rozvaděčů pro průmyslový provoz.",
                         "Střídače Sungrow a AC rozvaděče na stěně haly"),
    "fve-solaredge": ("Komerční FVE (SolarEdge)",
                      "Realizace FVE s technologií SolarEdge včetně dispečerského řízení.",
                      "Střídače SolarEdge a rozvaděč na nosné konstrukci u budovy"),
    "rozvadec-ac": ("Výroba AC rozvaděče",
                    "AC rozvaděč pro sdružení výkonu čtyř střídačů Sungrow.",
                    "Otevřený AC rozvaděč s přípojnicemi a jističi"),
    "vn-rozvadece": ("Výměna VN rozvaděčů",
                     "Instalace nových VN polí podle připojovacích podmínek (3× měření).",
                     "Technici osazují nové VN rozvaděče"),
    "trafostanice": ("Rekonstrukce trafostanice",
                     "Kompletní rekonstrukce a osazení kioskové trafostanice VN 35 kV.",
                     "Jeřáb usazuje kioskovou trafostanici"),
}

POPIS_FIRMY = ("Commissioning velkých fotovoltaických elektráren, dispečerské řízení a SVR, "
               "rekonstrukce VN a trafostanic, bateriová úložiště a ověření souladu výroben s RfG "
               "po celé České republice.")

WEB_SZ = "https://www.simulacni-zkousky.cz/"

# Tym – texty z puvodniho webu, u Fencla a Kovare doplnena specializace
# na simulace a RfG (stejne jako na simulacni-zkousky.cz).
TYM = [
    ("Bc. Petr Fencl", "Technický ředitel, specialista na simulace a RfG",
     "Specialista na průmyslovou automatizaci, FVE a MES/ERP integrace. Zkušenosti z klíčových "
     "projektů pro ČEZ a ČEPS. Jeho doménou jsou inovace, integrace AI a technicky "
     "„neřešitelné“ projekty."),
    ("PhDr. Jan Böhme", "Obchodní a finanční ředitel",
     "Expert na management, ekonomii a finance s praxí z vedení franšíz O2 a CZC. Zajišťuje "
     "finanční stabilitu projektů, vyjednávání s investory a strategický marketing."),
    ("Michal Kovář", "Specialista VN a řízení FVE, simulace a RfG",
     "Špičkový odborník na VN projekty, průmyslové řízení a SCADA aplikace. Má za sebou desítky FVE "
     "projektů v Evropě i zámoří (Austrálie, Chile). Zkušenosti s plovoucími FVE "
     "a agrivoltaikou."),
]


def tym_karty(zkracene=False):
    polozky = []
    for jmeno, role, text in TYM:
        telo = f'<p class="role">{role}</p>'
        telo += f"<p>{text.split('. ')[0].rstrip('.')}.</p>" if zkracene else f"<p>{text}</p>"
        polozky.append((I["clovek"], jmeno, telo))
    return karty(polozky, sloupce=3).replace('class="services', 'class="team services', 1)


SERVIS = [
    (I["mapa"], "Tým po celé ČR",
     "<p>Náš tým servisních techniků pokrývá celou Českou republiku a je připraven rychle reagovat "
     "na vaše požadavky, ať jste kdekoli.</p>"),
    (I["hodiny"], "Operativní servisní zásahy",
     "<p>Chápeme, že každá hodina výpadku se počítá. Proto se zaměřujeme na maximálně rychlé "
     "a efektivní servisní zásahy.</p>"),
    (I["smlouva"], "Servisní smlouvy",
     "<p>Nabízíme individuálně nastavené servisní smlouvy, které vám zajistí pravidelnou údržbu, "
     "prioritní servis a klid na duši.</p>"),
]

STRANKY = []

# =========================================================== DOMOVSKA ======
HERO = """<!-- HERO -->
<section class="hero">
  <div class="photo">
    <picture>
      <source type="image/webp" srcset="assets/title-photo-1024.webp 1024w, assets/title-photo.webp 2048w" sizes="100vw">
      <img class="snimek je-videt" src="assets/title-photo.jpg" alt="Fotovoltaická elektrárna na průmyslové střeše" width="2048" height="1536" fetchpriority="high" srcset="assets/title-photo-1024.jpg 1024w, assets/title-photo.jpg 2048w" sizes="100vw">
    </picture>
    <picture>
      <source type="image/webp" srcset="assets/hero-2-1024.webp 1024w, assets/hero-2.webp 2000w" sizes="100vw">
      <img class="snimek" src="assets/hero-2.jpg" alt="Panely pozemní fotovoltaické elektrárny při západu slunce" width="2000" height="1125" loading="lazy" srcset="assets/hero-2-1024.jpg 1024w, assets/hero-2.jpg 2000w" sizes="100vw">
    </picture>
    <picture>
      <source type="image/webp" srcset="assets/hero-3-1024.webp 1024w, assets/hero-3.webp 1600w" sizes="100vw">
      <img class="snimek" src="assets/hero-3.jpg" alt="Montážní tým BFK Systems před dokončenou pozemní elektrárnou" width="1600" height="1200" loading="lazy" srcset="assets/hero-3-1024.jpg 1024w, assets/hero-3.jpg 1600w" sizes="100vw">
    </picture>
  </div>
  <div class="gradient-overlay"></div>
  <div class="content">
    <p class="hero-eyebrow">BFK Systems &middot; experti na velké FVE projekty</p>
    <h1>Partner pro velké FVE a&nbsp;bateriová úložiště</h1>
    <p class="hero-claim-big">Poskytujeme komplexní služby od commissioningu a dispečerského řízení až po operativní servis po celé ČR.</p>
    <p class="hero-lead">Uvádíme do provozu velké fotovoltaické elektrárny, zapojujeme je do dispečerského řízení a rekonstruujeme VN a trafostanice. Oživujeme bateriová úložiště a soulad výroben s&nbsp;RfG dokládáme simulacemi i zkouškami na místě.</p>
    <div class="cta-row">
      <a class="btn btn-primary" href="kontakt.html#formular">Nezávazná poptávka</a>
      <a class="btn btn-light" href="sluzby.html">Naše služby</a>
    </div>
  </div>
</section>
<script src="assets/hero.js" defer></script>
"""

STRANKY.append({
    "slug": "index.html",
    "nav": "",
    "title": "BFK Systems – velké FVE, dispečerské řízení, VN a bateriová úložiště",
    "desc": "BFK Systems s.r.o.: commissioning velkých FVE, dispečerské řízení a SVR, rekonstrukce "
            "VN a trafostanic, bateriová úložiště a simulační zkoušky RfG po celé ČR.",
    "body": HERO + sekce(
        "Naše specializace",
        karty([
            (I["blesk"], "Commissioning FVE",
             "<p>Zajišťujeme profesionální uvedení velkých fotovoltaických elektráren do provozu, "
             "včetně veškerých testů a revizí.</p>", "sluzby.html#commissioning"),
            (I["rizeni"], "Dispečerské řízení a SVR",
             "<p>Implementujeme moderní systémy pro efektivní řízení, regulaci a zapojení vaší "
             "elektrárny do energetické sítě.</p>", "sluzby.html#rizeni"),
            (I["tovarna"], "Rekonstrukce VN a trafostanic",
             "<p>Modernizujeme a rekonstruujeme vysokonapěťové části a trafostanice pro maximální "
             "výkon a bezpečnost FVE.</p>", "sluzby.html#vn"),
            (I["panel"], "Komerční a velké FVE",
             "<p>Jsme vaším partnerem pro komplexní realizaci rozsáhlých fotovoltaických parků "
             "a průmyslových instalací.</p>", "sluzby.html#fve"),
            (I["graf"], "Simulační zkoušky",
             "<p>Ověření souladu výroben s RfG – simulace na modelu výrobny, zkoušky na místě "
             "a dokumentace pro distributora.</p>", "simulacni-zkousky.html"),
            (I["baterie"], "Bateriová úložiště",
             "<p>Oživení úložiště, řízení podle spotových cen, spolupráce s fotovoltaikou "
             "a ověření souladu pro distributora.</p>", "bateriova-uloziste.html"),
        ], sloupce=3),
        eyebrow="Služby",
        uvod="<p class=\"lead\">Zaměřujeme se na komerční a průmyslové fotovoltaické systémy "
             "a bateriová úložiště s působností po celé České republice.</p>",
        kotva="sluzby",
    ) + sekce(
        "Simulační zkoušky a ověření souladu",
        karty([
            (I["graf"], "Simulace souladu",
             "<p>Požadavky, které metodika umožňuje nebo vyžaduje ověřit simulací, prokážeme na "
             "modelu výrobny v prostředí DIgSILENT PowerFactory.</p>"),
            (I["lupa"], "Zkoušky na místě",
             "<p>Ověření regulace činného a jalového výkonu, ochran, dálkového řízení a opětovného "
             "připojení přímo na výrobně.</p>"),
            (I["dok"], "Dokumentace pro distributora",
             "<p>Žádosti o UPOS a UTP, protokoly a Dokument výrobního modulu až do konečného "
             "provozního oznámení.</p>"),
        ], sloupce=3)
        + cta("Kategorie A1 až D, postup, lhůty a podklady podrobně popisujeme na našem "
              "specializovaném webu.", "simulacni-zkousky.cz", WEB_SZ),
        eyebrow="Ověření souladu",
        uvod="<p class=\"lead\">Bez doloženého souladu s RfG nevydá distributor souhlas s trvalým "
             "provozem výrobny. Od kategorie B1, tedy od 100 kW, se část požadavků ověřuje simulací "
             "a část zkouškami přímo na výrobně. Děláme obojí – i pro elektrárny, které jsme "
             "nestavěli. <a href=\"simulacni-zkousky.html\">Více o simulačních zkouškách</a></p>",
        alt=True, kotva="rfg",
    ) + sekce(
        "Bateriová úložiště",
        rozdeleni(
            "        <p class=\"lead\">Úložiště musí správně spolupracovat s fotovoltaikou, sítí "
            "distributora i trhem s elektřinou. Oživíme ho, nastavíme řízení a doložíme "
            "distributorovi, co potřebuje.</p>\n"
            + seznam([
                "oživení a uvedení úložiště do provozu",
                "řízení podle spotových cen a integrace s FVE",
                "dispečerské řízení a přenos dat do dispečinku",
                "ověření souladu úložiště s RfG a formuláře distributora",
            ])
            + '\n        <p><a class="btn btn-primary" href="bateriova-uloziste.html">Bateriová úložiště</a></p>',
            "bess"),
        eyebrow="BESS", kotva="bess",
    ) + sekce(
        "Naše reference",
        galerie(["bess", "rtu-vn", "vn-rozvadece", "trafostanice"])
        + cta("Další realizace – průmyslové a komerční FVE, AC rozvaděče i projekty ověření souladu.",
              "Všechny reference", "reference.html"),
        eyebrow="Reference",
        uvod="<p>Výběr našich úspěšně realizovaných projektů.</p>",
        alt=True, kotva="reference",
    ) + sekce(
        "Spolehlivý servis a podpora",
        karty(SERVIS, sloupce=3),
        eyebrow="Servis",
        uvod="<p>Kromě špičkového know-how v realizaci projektů přinášíme i flexibilitu "
             "a spolehlivost v následné péči.</p>",
        kotva="servis",
    ) + sekce(
        "Náš tým expertů",
        tym_karty(zkracene=True)
        + cta("Kdo jsme, co nás odlišuje a s kým spolupracujeme.", "O nás", "o-nas.html"),
        eyebrow="O nás",
        uvod="<p class=\"lead\">BFK Systems tvoří sehraný tým specialistů, kteří spojili své "
             "dlouholeté zkušenosti z energetiky, průmyslové automatizace a financí.</p>",
        alt=True, kotva="o-nas",
    ),
})

# ============================================================ SLUZBY ======
STRANKY.append({
    "slug": "sluzby.html", "nav": "sluzby",
    "title": "Služby – commissioning FVE, dispečerské řízení, VN a servis",
    "desc": "Commissioning velkých FVE, dispečerské řízení a SVR, rekonstrukce VN a trafostanic, "
            "komerční a průmyslové FVE, simulační zkoušky, bateriová úložiště a servis po celé ČR.",
    "eyebrow": "Co děláme", "h1": "Služby",
    "claim": "Komerční a průmyslové FVE a bateriová úložiště po celé ČR.",
    "bc_nazev": "Služby", "breadcrumb": [],
    "intro": "<p>Od uvedení elektrárny do provozu přes řízení, VN a trafostanice až po servis. "
             "Soustředíme se na velké a technologicky náročné projekty.</p>",
    "anchors": kotvy([("Commissioning", "commissioning"), ("Řízení a SVR", "rizeni"),
                      ("VN a trafostanice", "vn"), ("Komerční a velké FVE", "fve"),
                      ("Simulační zkoušky", "rfg"), ("Bateriová úložiště", "bess"),
                      ("Servis", "servis")]),
    "body": sekce(
        "Commissioning FVE",
        rozdeleni(
            "        <p class=\"lead\">Zajišťujeme profesionální uvedení velkých fotovoltaických "
            "elektráren do provozu, včetně veškerých testů a revizí.</p>\n"
            + seznam([
                "uvedení elektrárny do provozu a oživení technologie",
                "testy a revize před spuštěním",
                "nastavení komunikace a řízení",
                "součinnost při zkouškách souladu s RfG a při jednání s distributorem",
            ]),
            "fve-strechy"),
        eyebrow="Uvedení do provozu", kotva="commissioning",
    ) + sekce(
        "Dispečerské řízení a SVR",
        rozdeleni(
            "        <p class=\"lead\">Implementujeme moderní systémy pro efektivní řízení, regulaci "
            "a zapojení vaší elektrárny do energetické sítě.</p>\n"
            + seznam([
                "RTU a řídicí systém pro FVE na vysokém napětí (komponenty Weidmüller)",
                "napojení výrobny na dispečink distributora",
                "SCADA, řízení vytápění a nabíjecích stanic",
                "řízení podle spotových cen",
                "zapojení do služeb výkonové rovnováhy (SVR) a agregace",
            ]),
            "rtu-vn", reverse=True),
        eyebrow="Řízení", alt=True, kotva="rizeni",
    ) + sekce(
        "Rekonstrukce VN a trafostanic",
        rozdeleni(
            "        <p class=\"lead\">Modernizujeme a rekonstruujeme vysokonapěťové části "
            "a trafostanice pro maximální výkon a bezpečnost FVE.</p>\n"
            + seznam([
                "výměna VN rozvaděčů a instalace nových VN polí podle připojovacích podmínek, "
                "včetně měření",
                "kompletní rekonstrukce a osazení kioskových trafostanic VN 35 kV",
            ]),
            "vn-rozvadece"),
        eyebrow="Vysoké napětí", kotva="vn",
    ) + sekce(
        "Komerční a velké FVE",
        rozdeleni(
            "        <p class=\"lead\">Jsme vaším partnerem pro komplexní realizaci rozsáhlých "
            "fotovoltaických parků a průmyslových instalací.</p>\n"
            + seznam([
                "instalace střídačů a AC rozvaděčů pro průmyslový provoz (Sungrow, SolarEdge)",
                "výroba AC rozvaděčů – například pro sdružení výkonu čtyř střídačů",
                "dispečerské řízení jako součást dodávky",
                "se sesterskou společností BF technology pokryjeme stavbu i inženýrskou část",
            ]),
            "stridace-sungrow", reverse=True),
        eyebrow="Realizace", alt=True, kotva="fve",
    ) + sekce(
        "Simulační zkoušky a ověření souladu",
        karty([
            (I["graf"], "Simulace souladu",
             "<p>Model výrobny a protokol s vyhodnocením splněno / nesplněno u každého "
             "požadavku.</p>", "simulacni-zkousky.html"),
            (I["lupa"], "Zkoušky na místě",
             "<p>Regulace činného a jalového výkonu, ochrany, dálkové řízení a opětovné "
             "připojení.</p>", "simulacni-zkousky.html"),
            (I["dok"], "Dokumentace a jednání s distributorem",
             "<p>Žádosti o UPOS a UTP, Dokument výrobního modulu a vypořádání připomínek.</p>",
             "simulacni-zkousky.html"),
        ], sloupce=3),
        eyebrow="Ověření souladu", kotva="rfg",
        uvod="<p>Soulad výroben od kategorie B1 (od 100 kW) dokládáme distributorovi simulacemi, "
             "zkouškami na místě a dokumentací.</p>",
    ) + sekce(
        "Bateriová úložiště",
        karty([
            (I["blesk"], "Oživení a uvedení do provozu",
             "<p>Úložiště uvedeme do provozu včetně testů a nastavení komunikace.</p>",
             "bateriova-uloziste.html"),
            (I["cena"], "Řízení a integrace s FVE",
             "<p>Řízení podle spotových cen a spolupráce s fotovoltaikou.</p>",
             "bateriova-uloziste.html"),
            (I["stit"], "Ověření souladu",
             "<p>Úložiště od 100 kW prochází ověřením souladu obdobně jako výrobna.</p>",
             "bateriova-uloziste.html"),
        ], sloupce=3),
        eyebrow="BESS", alt=True, kotva="bess",
    ) + sekce(
        "Servis a servisní smlouvy",
        karty(SERVIS, sloupce=3),
        eyebrow="Servis", kotva="servis",
        uvod="<p>Kromě špičkového know-how v realizaci projektů přinášíme i flexibilitu "
             "a spolehlivost v následné péči.</p>",
    ),
    "cross": [("Reference", "reference.html"), ("Simulační zkoušky", "simulacni-zkousky.html"),
              ("Bateriová úložiště", "bateriova-uloziste.html"), ("Kontakt", "kontakt.html")],
    "cross_alt": True,
})

# ================================================= SIMULACNI ZKOUSKY ======
KAT = WEB_SZ + "kategorie-{}.html"
STRANKY.append({
    "slug": "simulacni-zkousky.html", "nav": "rfg", "prio": "0.8",
    "title": "Simulační zkoušky a ověření souladu s RfG",
    "desc": "Ověření souladu výroben a bateriových úložišť s RfG: simulace souladu, zkoušky na "
            "místě, Dokument výrobního modulu a žádosti o UPOS a UTP. Od kategorie B1, tedy od 100 kW.",
    "eyebrow": "Ověření souladu", "h1": "Simulační zkoušky a ověření souladu s RfG",
    "claim": "Simulace, zkoušky na místě a dokumentace pro distributora – od jedné firmy.",
    "bc_nazev": "Simulační zkoušky", "breadcrumb": [],
    "intro": "<p>Bez doloženého souladu s RfG nevydá provozovatel distribuční soustavy (dále také "
             "distributor) souhlas s trvalým provozem výrobny. Od kategorie B1, tedy od 100 kW, se "
             "část požadavků ověřuje simulací a část zkouškami přímo na výrobně. Děláme obojí – "
             "včetně žádostí o UPOS a UTP.</p>",
    "body": sekce(
        "Co pro vás uděláme",
        karty([
            (I["graf"], "Simulace souladu",
             "<p>Požadavky, které metodika umožňuje nebo vyžaduje ověřit simulací, prokážeme na modelu "
             "výrobny – typicky odezvu při změnách frekvence a napětí a chování při poruchách. "
             "Počítáme v prostředí DIgSILENT PowerFactory.</p>", WEB_SZ + "simulace-souladu.html"),
            (I["lupa"], "Zkoušky na místě",
             "<p>Ověření regulace činného a jalového výkonu, ochran, dálkového řízení a opětovného "
             "připojení přímo na výrobně. Rozsah podle smlouvy o připojení.</p>",
             WEB_SZ + "zkousky-na-miste.html"),
            (I["dok"], "Dokumentace a jednání s distributorem",
             "<p>Žádost o UPOS, protokoly, Dokument výrobního modulu, žádost o UTP a vypořádání "
             "připomínek distributora až do konečného provozního oznámení.</p>",
             WEB_SZ + "proces-pripojeni.html"),
            (I["baterie"], "Bateriová úložiště",
             "<p>Nové úložiště i doplnění baterie ke stávající fotovoltaice – ověření provozu při "
             "nabíjení i vybíjení a vlastní formuláře distributora.</p>", "bateriova-uloziste.html"),
        ], sloupce=2),
        eyebrow="Služby",
        uvod="<p>Pojem „simulační zkoušky“ používáme jako souhrnné označení služeb. Odborně jde "
             "o <b>ověření souladu výrobny s nařízením (EU) 2016/631 (RfG)</b>, při kterém se "
             "požadavky dokládají simulacemi souladu, zkouškami souladu, nebo certifikáty zařízení – "
             "podle příslušné metodiky.</p>",
    ) + sekce(
        "Kategorie výrobních modulů",
        tabulka(
            ["Kategorie", "Výkon", "Zkoušky na místě", "Simulace"],
            [[f'<a href="{KAT.format("a1")}" target="_blank" rel="noopener">A1</a>', "0,8 až 11 kW",
              "standardně ne", "standardně ne"],
             [f'<a href="{KAT.format("a2")}" target="_blank" rel="noopener">A2</a>', "nad 11 kW, pod 100 kW",
              "standardně ne", "standardně ne"],
             [f'<a href="{KAT.format("b1")}" target="_blank" rel="noopener">B1</a>', "100 kW až pod 1 MW",
              "ano", "vybrané body"],
             [f'<a href="{KAT.format("b2")}" target="_blank" rel="noopener">B2</a>', "1 MW až pod 30 MW",
              "ano", "širší rozsah"],
             [f'<a href="{KAT.format("c-d")}" target="_blank" rel="noopener">C</a>', "30 MW až pod 75 MW",
              "ano", "nejširší rozsah"],
             [f'<a href="{KAT.format("c-d")}" target="_blank" rel="noopener">D</a>',
              "od 75 MW, nebo připojení na 110 kV", "ano", "nejširší rozsah"]],
            poznamky=[
                "<b>Kategorii najdete ve smlouvě o připojení</b> a ta je vždy rozhodující. U bateriových "
                "úložišť se zařazení a způsob ověření řídí aktuálními podmínkami příslušného distributora.",
                "<b>Pozor na jednotky:</b> výkon panelů v kWp není výkon, podle kterého se kategorie "
                "určuje. Rozhoduje jmenovitý činný výkon výrobního modulu – 698 kWp panelů může být "
                "modul s P<sub>n</sub> 550 kW.",
            ],
            min_sirka=640,
        ),
        eyebrow="Do které kategorie spadáte",
        uvod="<p>Rozsah ověření se odvíjí od kategorie výrobního modulu. Podrobnosti ke každé kategorii "
             "najdete na webu simulacni-zkousky.cz.</p>",
        alt=True, kotva="kategorie",
    ) + sekce(
        "Tři cesty, jak požadavek doložit",
        karty([
            (I["lupa"], "Zkouška na místě",
             "<p>Ověření na hotové výrobně a protokol. Některé požadavky jinak doložit nejde – "
             "u kategorie B1 jich je šest.</p>"),
            (I["graf"], "Simulace",
             "<p>Model výrobny a protokol s vyhodnocením splněno / nesplněno. U kategorie B2 a vyšších "
             "kategorií je rozsah simulací podstatně širší.</p>"),
            (I["dok"], "Certifikát zařízení",
             "<p>Vydává ho certifikátor pro konkrétní zařízení – náš protokol ze zkoušky nebo simulace "
             "certifikát není. Nahradí zkoušku nebo simulaci jen tam, kde to Dokument výrobního modulu "
             "připouští.</p>"),
        ], sloupce=3)
        + cta("Kategorie, distributory, postup, lhůty a podklady podrobně popisujeme na našem "
              "specializovaném webu simulacni-zkousky.cz.", "Přejít na simulacni-zkousky.cz", WEB_SZ),
        eyebrow="Klíčový koncept",
    ),
    "faq": [
        ("Co jsou „simulační zkoušky“?",
         "<p>Běžné označení pro ověření souladu výrobny s RfG. Tvoří ho <b>simulace souladu</b> "
         "(výpočet na modelu výrobny) a <b>zkoušky na místě</b> (ověření na hotové elektrárně). "
         "Rozsah obojího určuje kategorie výrobny.</p>"),
        ("Od jakého výkonu se mě to týká?",
         "<p>Zkoušky na místě a simulace přicházejí od kategorie <b>B1, tedy od 100 kW</b>. Menší "
         "výrobny (A1, A2) dokládají soulad doklady ke střídači a instalačním dokumentem.</p>"),
        ("Jak zjistím kategorii své výrobny?",
         "<p>Najdete ji ve <b>smlouvě o připojení</b>. Orientačně ji poznáte podle výkonu z tabulky "
         "výše. Když si nejste jistí, pošlete nám smlouvu.</p>"),
        ("Děláte to i pro elektrárny, které jste nestavěli?",
         "<p>Ano, je to velká část naší práce. Studie a zkoušky děláme pro jiné dodavatele "
         "fotovoltaiky i pro investory, kteří si stavbu zajistili sami. Potřebujeme podklady, "
         "ne vlastní stavbu.</p>"),
    ],
    "cross": [("simulacni-zkousky.cz", WEB_SZ), ("Bateriová úložiště", "bateriova-uloziste.html"),
              ("Reference", "reference.html"), ("Kontakt", "kontakt.html")],
    "cross_alt": True,
})

# ============================================================== BESS ======
STRANKY.append({
    "slug": "bateriova-uloziste.html", "nav": "bess", "prio": "0.8",
    "title": "Bateriová úložiště – oživení, řízení a ověření souladu",
    "desc": "Bateriová úložiště (BESS): oživení a uvedení do provozu, řízení podle spotových cen, "
            "integrace s fotovoltaikou, dispečerské řízení a ověření souladu s RfG.",
    "eyebrow": "BESS", "h1": "Bateriová úložiště",
    "claim": "Oživení, řízení a ověření souladu pro distributora.",
    "bc_nazev": "Bateriová úložiště", "breadcrumb": [],
    "intro": "<p>Bateriové úložiště musí správně spolupracovat s fotovoltaikou, sítí distributora "
             "i trhem s elektřinou. Úložiště oživujeme, nastavujeme jeho řízení, zapojujeme ho "
             "do dispečerského řízení a dokládáme distributorovi soulad s RfG.</p>",
    "body": sekce(
        "Co pro úložiště děláme",
        karty([
            (I["blesk"], "Oživení a uvedení do provozu",
             "<p>Úložiště uvedeme do provozu včetně testů a nastavení komunikace.</p>"),
            (I["cena"], "Řízení podle spotových cen",
             "<p>Nabíjení a vybíjení podle cen elektřiny na spotovém trhu.</p>"),
            (I["panel"], "Integrace s fotovoltaikou",
             "<p>Úložiště spolupracuje s FVE – ať jde o nový projekt, nebo o doplnění baterie "
             "ke stávající elektrárně.</p>"),
            (I["rizeni"], "Dispečerské řízení a telemetrie",
             "<p>U úložišť s požadavkem na dispečerské řízení se přenáší také stav nabití "
             "a distributor může požadovat omezení dodávky i odběru činného výkonu. Řídicí systém "
             "a RTU zapojíme.</p>"),
            (I["stit"], "Ověření souladu",
             "<p>Zařazení úložiště a způsob prokázání souladu se řídí pravidly provozování "
             "distribučních soustav (PPDS) a dokumenty distributora. Od 100 kW je postup obdobný "
             "jako u výrobny: UPOS, zkoušky a simulace a žádost o UTP.</p>"),
            (I["klic"], "Servis",
             "<p>Operativní zásahy a servisní smlouvy platí i pro úložiště – po celé ČR.</p>"),
        ], sloupce=3),
        eyebrow="Služby",
    ) + sekce(
        "Ověřuje se v obou směrech",
        rozdeleni(
            "        <p class=\"lead\">To je hlavní rozdíl proti fotovoltaice. Požadavky se prokazují "
            "při <b>vybíjení i nabíjení</b>, včetně přechodů mezi nimi. Podpora napětí jalovým "
            "výkonem se posuzuje pro oba směry činného výkonu.</p>\n"
            "        <p>K úložišti se vyplňuje vlastní dokument ověřování souladu. ČEZ Distribuce "
            "k 1. 9. 2025 vydala dodatky k připojovacím podmínkám pro zařízení pro ukládání "
            "elektřiny.</p>\n"
            f'        <p><a href="{WEB_SZ}bateriova-uloziste-zue.html" target="_blank" rel="noopener">'
            "Ověření souladu úložišť podrobně na simulacni-zkousky.cz →</a></p>",
            "bess"),
        eyebrow="Nabíjení i vybíjení", alt=True,
    ) + sekce(
        "Doplnění baterie ke stávající FVE",
        seznam([
            "<b>Posouzení připojitelnosti.</b> Doplnění úložiště distributor posuzuje znovu.",
            "<b>Úprava smlouvy o připojení.</b> Úložiště se k připojení doplňuje, zpravidla dodatkem "
            "ke smlouvě.",
            "<b>Ověření souladu úložiště.</b> Vlastní dokument ověřování souladu a ověření provozu při "
            "nabíjení i vybíjení.",
            "<b>Rozšíření telemetrie.</b> Vyžaduje-li distributor dispečerské řízení, doplní se signály "
            "úložiště a znovu se ověří přenos dat do dispečinku.",
        ])
        + cta("Pošlete nám výkon a kapacitu úložiště a jestli jde o nový projekt, nebo doplnění ke "
              "stávající FVE. Řekneme, co vás čeká."),
        eyebrow="Častý případ",
        uvod="<p>Samotná montáž je rychlá. Administrativně jde ale o změnu zařízení, kterou je "
             "potřeba projednat s distributorem – a právě ta bývá časově náročnější než montáž.</p>",
    ),
    "faq": [
        ("Platí pro baterii stejné zkoušky jako pro fotovoltaiku?",
         "<p>Postup je obdobný, ale ne totožný. Ověřuje se provoz při nabíjení i vybíjení, úložiště "
         "má vlastní dokument ověřování souladu a zařazení se řídí podmínkami příslušného "
         "distributora.</p>"),
        ("Můžeme s baterií poskytovat podpůrné služby?",
         "<p>Podmínky pro podpůrné služby jsou nad rámec ověření souladu a řeší se zvlášť – "
         "s distributorem, provozovatelem přenosové soustavy a agregátorem.</p>"),
        ("Přijdu doplněním baterie o konečné provozní oznámení?",
         "<p>Provozní oznámení se váže k výrobně v původní konfiguraci. Doplněním úložiště se "
         "konfigurace mění, proto se uvedení do provozu pro nové zařízení opakuje v rozsahu, "
         "který stanoví distributor.</p>"),
    ],
    "cross": [("Simulační zkoušky", "simulacni-zkousky.html"), ("Reference", "reference.html"),
              ("Služby", "sluzby.html"), ("Kontakt", "kontakt.html")],
    "cross_alt": True,
})

# ========================================================= REFERENCE ======
STRANKY.append({
    "slug": "reference.html", "nav": "reference",
    "title": "Reference – FVE, VN, trafostanice a bateriová úložiště",
    "desc": "Vybrané realizace BFK Systems: oživení BESS, dispečerské řízení VN 35 kV, průmyslové "
            "a komerční FVE, AC rozvaděče, VN rozvaděče, trafostanice a projekty ověření souladu.",
    "eyebrow": "Co máme za sebou", "h1": "Reference",
    "claim": "Výběr našich úspěšně realizovaných projektů.",
    "bc_nazev": "Reference", "breadcrumb": [],
    "intro": "<p>Většina investorů si nepřeje být jmenována, proto projekty uvádíme bez názvů – "
             "s tím, co jsme na nich dělali. Fotku zvětšíte kliknutím.</p>",
    "body": sekce(
        "Realizace",
        galerie(list(REFERENCE)),
        eyebrow="Fotky z projektů",
    ) + sekce(
        "Ověření souladu výroben",
        karty([
            (I["tovarna"], "Fotovoltaika, kategorie D",
             "<p><b>Výkon:</b> 36 MWp panelů, do sítě přibližně 30 MW, připojení na 110 kV<br>"
             "<b>Distributor:</b> EG.D<br>"
             "<b>Předmět:</b> simulace souladu, model výrobny, dokumentace<br>"
             "<b>Stav:</b> zpracováno</p>"),
            (I["blesk"], "Fotovoltaika, kategorie B1",
             "<p><b>Výkon:</b> 698 kWp (P<sub>n</sub> 550 kW)<br><b>Distributor:</b> ČEZ Distribuce<br>"
             "<b>Předmět:</b> zkoušky na místě, protokoly, Dokument výrobního modulu</p>"),
            (I["baterie"], "Fotovoltaika s baterií",
             "<p><b>Výkon:</b> 60 kWp + bateriové úložiště<br><b>Distributor:</b> EG.D<br>"
             "<b>Předmět:</b> etapizace fotovoltaiky a doplnění akumulace</p>"),
        ], sloupce=3)
        + cta("Projekty ověření souladu podrobněji popisujeme na webu simulacni-zkousky.cz.",
              "Reference na simulacni-zkousky.cz", WEB_SZ + "reference.html"),
        eyebrow="Simulační zkoušky", alt=True,
    ) + sekce(
        "Chcete referenci na konkrétní typ projektu?",
        "<p class=\"lead\">Řekněte si o ni – po dohodě s investorem ji rádi doložíme "
        "podrobněji.</p>",
        eyebrow="Na vyžádání",
    ),
    "cross": [("Služby", "sluzby.html"), ("Bateriová úložiště", "bateriova-uloziste.html"),
              ("O nás", "o-nas.html"), ("Kontakt", "kontakt.html")],
    "cross_alt": True,
})

# ============================================================= O NAS ======
STRANKY.append({
    "slug": "o-nas.html", "nav": "onas",
    "title": "O nás – tým BFK Systems",
    "desc": "BFK Systems s.r.o. z Děčína: tým specialistů z energetiky, průmyslové automatizace "
            "a financí. Velké a technologicky náročné FVE projekty, bateriová úložiště a servis po celé ČR.",
    "eyebrow": "BFK Systems s.r.o.", "h1": "O nás",
    "claim": "Velké a technologicky náročné projekty.",
    "bc_nazev": "O nás", "breadcrumb": [],
    "intro": "<p>BFK Systems tvoří sehraný tým specialistů, kteří spojili své dlouholeté zkušenosti "
             "z energetiky, průmyslové automatizace a financí. Naší misí je poskytovat technicky "
             "precizní a spolehlivá řešení, která maximalizují efektivitu a návratnost investic do "
             "obnovitelných zdrojů. Soustředíme se na to, co umíme nejlépe: velké a technologicky "
             "náročné projekty.</p>",
    "body": sekce(
        "Náš tým expertů",
        tym_karty(),
        eyebrow="Tým", kotva="tym",
    ) + sekce(
        "Co nás odlišuje",
        karty([
            (I["tovarna"], "Velké a náročné projekty",
             "<p>Komerční a průmyslové fotovoltaiky, VN a trafostanice, bateriová úložiště. "
             "Zpracovali jsme i fotovoltaiku 36 MWp připojenou na 110 kV.</p>"),
            (I["lide"], "Energetika, automatizace a finance",
             "<p>Tým spojuje zkušenosti z energetiky, průmyslové automatizace a financí – technické "
             "řešení i jeho návratnost řešíme společně.</p>"),
            (I["rizeni"], "Inženýrská část pod jednou střechou",
             "<p>Commissioning, dispečerské řízení, simulace a zkoušky souladu s RfG i jednání "
             "s distributorem zajistíme sami.</p>"),
            (I["mapa"], "Servis po celé ČR",
             "<p>Náš tým servisních techniků pokrývá celou Českou republiku a je připraven rychle "
             "reagovat, ať jste kdekoli.</p>"),
        ], sloupce=2),
        eyebrow="Jak pracujeme", alt=True,
    ) + sekce(
        "Skupina BF technology",
        "<p class=\"lead\">Se sesterskou společností "
        "<a href=\"https://www.bftechnology.cz/\" target=\"_blank\" rel=\"noopener\">BF technology</a> "
        "tvoříme jednu skupinu. BF technology staví fotovoltaické elektrárny, BFK Systems dělá "
        "inženýrskou část – projekty, commissioning, řízení, simulace, zkoušky a jednání "
        "s distributory. Zkušenosti máme z projektů pro energetiku, petrochemii i automobilový "
        "průmysl.</p>"
        + karty([
            (I["graf"], "simulacni-zkousky.cz",
             "<p>Náš specializovaný web o ověřování souladu výroben s RfG – kategorie, distributoři, "
             "postup a lhůty.</p>", WEB_SZ),
            (I["panel"], "bftechnology.cz",
             "<p>Sesterská společnost BF technology – stavba fotovoltaických elektráren.</p>",
             "https://www.bftechnology.cz/"),
        ], sloupce=2),
        eyebrow="Skupina",
    ) + sekce(
        "Firemní údaje",
        tabulka(
            ["", ""],
            [["Obchodní firma", "BFK Systems s.r.o."],
             ["Sídlo", "Obchodní 455/12, Děčín V-Rozbělesy, 405 02 Děčín"],
             ["IČO", "23571853"],
             ["DIČ", "CZ23571853"],
             ["Zápis v OR", "Krajský soud v Ústí nad Labem, oddíl C, vložka 54375"]],
            min_sirka=520,
        ),
        eyebrow="Údaje", alt=True,
    ),
    "cross": [("Služby", "sluzby.html"), ("Reference", "reference.html"), ("Kontakt", "kontakt.html")],
})

# =========================================================== KONTAKT ======
FORMULAR = """<section class="contact-section" id="poptavka">
  <div class="bg"><picture>
    <source type="image/webp" srcset="assets/title-photo-1024.webp 1024w, assets/title-photo.webp 2048w" sizes="(max-width: 980px) 100vw, 33vw">
    <img src="assets/title-photo.jpg" alt="" aria-hidden="true" loading="lazy" width="2048" height="1536" srcset="assets/title-photo-1024.jpg 1024w, assets/title-photo.jpg 2048w" sizes="(max-width: 980px) 100vw, 33vw">
  </picture></div>
  <div class="container contact-grid">
    <div class="contact-aside">
      <p class="eyebrow">Kontakt</p>
      <h2>Napište nám,<br>co řešíte.</h2>
      <p>Ozveme se do dvou pracovních dnů. Projektovou dokumentaci, schéma nebo smlouvu o připojení nám pošlete e-mailem na info@bfksystems.cz – formulář přílohy nepřenese.</p>
      <div class="quick">
        <a href="tel:+420776111100">
          <span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.35 1.79.68 2.64a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.44-1.25a2 2 0 0 1 2.11-.45c.85.33 1.74.56 2.64.68A2 2 0 0 1 22 16.92z"/></svg></span>
          +420 776 111 100
        </a>
        <a href="mailto:info@bfksystems.cz">
          <span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg></span>
          info@bfksystems.cz
        </a>
      </div>
      <div class="firm">
        <b>BFK Systems s.r.o.</b><br>
        Obchodní 455/12, Děčín V-Rozbělesy, 405 02 Děčín<br>
        IČO 23571853 &middot; DIČ CZ23571853
      </div>
    </div>

    <div class="contact-form-card" id="formular">
      <div id="contact-status" role="status"></div>
      <!-- Odesila se pres fetch(), pole "redirect" je zalozni cesta bez JavaScriptu. -->
      <form class="contact-form" id="contact-form" action="https://api.web3forms.com/submit" method="post" autocomplete="on">
        <input type="hidden" name="access_key" value="PLACEHOLDER-DOPLNIT-KLIC-WEB3FORMS">
        <input type="hidden" name="subject" value="Nová poptávka z webu bfksystems.cz">
        <input type="hidden" name="from_name" value="Poptávkový formulář bfksystems.cz">
        <input type="hidden" name="replyto" value="">
        <input type="hidden" name="redirect" value="https://www.bfksystems.cz/kontakt.html?sent=1#formular">
        <div class="hp-field" aria-hidden="true">
          <label for="botcheck">Nevyplňujte</label>
          <input type="checkbox" id="botcheck" name="botcheck" tabindex="-1" autocomplete="off">
        </div>
        <div class="row">
          <div class="field">
            <label for="f-name">Jméno a příjmení *</label>
            <input type="text" id="f-name" name="Jméno a příjmení" required>
          </div>
          <div class="field">
            <label for="f-phone">Telefon *</label>
            <input type="tel" id="f-phone" name="Telefon" required>
          </div>
          <div class="field">
            <label for="f-email">E-mail *</label>
            <input type="email" id="f-email" name="E-mail" required>
          </div>
          <div class="field">
            <label for="f-firma">Firma</label>
            <input type="text" id="f-firma" name="Firma">
          </div>
          <div class="field">
            <label for="f-misto">Místo realizace</label>
            <input type="text" id="f-misto" name="Místo realizace" placeholder="obec nebo okres">
          </div>
          <div class="field">
            <label for="f-vykon">Výkon</label>
            <input type="text" id="f-vykon" name="Výkon" placeholder="např. 2 MWp, úložiště 1 MWh">
          </div>
          <div class="field full">
            <label for="f-zajem">Mám zájem o</label>
            <select id="f-zajem" name="Zájem o">
              <option value="">– vyberte –</option>
              <option>Commissioning FVE</option>
              <option>Dispečerské řízení a SVR</option>
              <option>Rekonstrukce VN a trafostanic</option>
              <option>Komerční a velké FVE</option>
              <option>Bateriové úložiště</option>
              <option>Simulační zkoušky a ověření souladu s RfG</option>
              <option>Servis a servisní smlouvu</option>
              <option>Konzultaci / jiné</option>
            </select>
          </div>
          <div class="field full">
            <label for="f-message">Zpráva</label>
            <textarea id="f-message" name="Zpráva" placeholder="Co řešíte, v jaké fázi je projekt, termín…"></textarea>
          </div>
          <input type="hidden" name="Odesláno z webu" value="bfksystems.cz">
          <div class="field full">
            <p class="gdpr">Odesláním formuláře berete na vědomí zpracování osobních údajů za účelem vyřízení poptávky. K odeslání formuláře využíváme externí službu jako zpracovatele. Podrobnosti najdete v <a href="zasady-zpracovani-osobnich-udaju.html">zásadách zpracování osobních údajů</a>.</p>
            <button type="submit">Odeslat poptávku</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</section>

<script src="assets/form.js"></script>
"""

STRANKY.append({
    "slug": "kontakt.html", "nav": "kontakt", "bez_kontaktu": True,
    "title": "Kontakt – BFK Systems s.r.o., Děčín",
    "desc": "BFK Systems s.r.o., Obchodní 455/12, Děčín. Telefon +420 776 111 100, "
            "info@bfksystems.cz. Poptávka na FVE, dispečerské řízení, VN, úložiště a simulační zkoušky.",
    "eyebrow": "Kontakt", "h1": "Kontaktujte nás",
    "bc_nazev": "Kontakt", "breadcrumb": [],
    "intro": "<p>Máte zájem o spolupráci nebo potřebujete konzultaci? Neváhejte se nám ozvat – "
             "telefonem, e-mailem, nebo přes formulář níže.</p>",
    "body": sekce(
        "Kontaktní údaje",
        karty([
            (I["mapa"], "BFK Systems s.r.o.",
             "<p>Obchodní 455/12<br>Děčín V-Rozbělesy, 405 02 Děčín</p>"
             "<p>IČO 23571853<br>DIČ CZ23571853</p>"),
            (I["sit"], "Spojení",
             '<p><a href="tel:+420776111100">+420 776 111 100</a><br>'
             '<a href="mailto:info@bfksystems.cz">info@bfksystems.cz</a></p>'
             '<p>Ověření souladu s RfG: <a href="https://www.simulacni-zkousky.cz/" target="_blank" '
             'rel="noopener">www.simulacni-zkousky.cz</a></p>'),
        ], sloupce=2),
        eyebrow="Kde nás najdete",
    ) + FORMULAR + sekce(
        "Fakturační a identifikační údaje",
        tabulka(
            ["", ""],
            [["Obchodní firma", "BFK Systems s.r.o."],
             ["Sídlo", "Obchodní 455/12, Děčín V-Rozbělesy, 405 02 Děčín"],
             ["IČO", "23571853"],
             ["DIČ", "CZ23571853"],
             ["Zápis v OR", "Krajský soud v Ústí nad Labem, oddíl C, vložka 54375"],
             ["Telefon", '<a href="tel:+420776111100">+420 776 111 100</a>'],
             ["E-mail", '<a href="mailto:info@bfksystems.cz">info@bfksystems.cz</a>']],
            min_sirka=520,
        ),
        eyebrow="Údaje", kotva="udaje",
    ),
    "cross": [("Služby", "sluzby.html"), ("Reference", "reference.html"), ("O nás", "o-nas.html")],
})

# ======================================================== GDPR a 404 ======
STRANKY.append({
    "slug": "zasady-zpracovani-osobnich-udaju.html", "nav": "", "prio": "0.2",
    "title": "Zásady zpracování osobních údajů",
    "desc": "Jak BFK Systems s.r.o. zpracovává osobní údaje z poptávkového formuláře na webu "
            "bfksystems.cz: účely, právní základ, doba uchování, příjemci a vaše práva.",
    "eyebrow": "Právní informace", "h1": "Zásady zpracování osobních údajů",
    "bc_nazev": "Zásady zpracování osobních údajů", "breadcrumb": [],
    "intro": "<p>Tyto zásady popisují, jak nakládáme s osobními údaji, které nám pošlete přes web "
             "www.bfksystems.cz.</p>",
    "body": sekce("", """    <div class="legal">
      <p class="updated">Účinné od 17. 9. 2026</p>

      <h2>1. Kdo údaje zpracovává</h2>
      <p>Správcem osobních údajů je <b>BFK Systems s.r.o.</b>, IČO 23571853, se sídlem Obchodní 455/12,
      Děčín V-Rozbělesy, 405 02 Děčín, zapsaná v obchodním rejstříku vedeném Krajským soudem v Ústí nad
      Labem, oddíl C, vložka 54375.</p>
      <p>Kontakt ve věcech ochrany osobních údajů: <a href="mailto:info@bfksystems.cz">info@bfksystems.cz</a>,
      telefon <a href="tel:+420776111100">+420 776 111 100</a>. Pověřence pro ochranu osobních údajů
      jsme nejmenovali, protože nám tato povinnost ze zákona nevyplývá.</p>

      <h2>2. Jaké údaje a proč</h2>
      <table>
        <tr><th>Účel</th><th>Údaje</th><th>Právní základ</th><th>Doba uchování</th></tr>
        <tr>
          <td>Vyřízení poptávky odeslané formulářem</td>
          <td>jméno a příjmení, telefon, e-mail, firma, údaje o projektu uvedené ve zprávě</td>
          <td>opatření před uzavřením smlouvy na vaši žádost (čl. 6 odst. 1 písm. b) GDPR)</td>
          <td>3 roky od poslední komunikace, pokud nedojde k uzavření smlouvy</td>
        </tr>
        <tr>
          <td>Plnění smlouvy a související dokumentace</td>
          <td>identifikační a kontaktní údaje, údaje o zařízení a projektu</td>
          <td>plnění smlouvy (čl. 6 odst. 1 písm. b) GDPR)</td>
          <td>po dobu trvání smlouvy a 10 let poté (zákonné archivační lhůty)</td>
        </tr>
        <tr>
          <td>Plnění zákonných povinností – účetnictví a daně</td>
          <td>fakturační údaje</td>
          <td>právní povinnost (čl. 6 odst. 1 písm. c) GDPR)</td>
          <td>podle zákona o účetnictví a daňových předpisů, zpravidla 10 let</td>
        </tr>
      </table>
      <p>Vyplnění formuláře je dobrovolné. Bez kontaktních údajů vám ale nemůžeme odpovědět.</p>

      <h2>3. Komu se údaje předávají</h2>
      <p>Osobní údaje nepředáváme nikomu k vlastním účelům. Zapojujeme však zpracovatele, kteří pro
      nás zajišťují technické služby:</p>
      <ul>
        <li>poskytovatel služby pro odeslání a doručení formuláře (odeslaná zpráva prochází jeho
        serverem a je přeposlána na naši e-mailovou adresu);</li>
        <li>poskytovatel webhostingu, na kterém běží tento web;</li>
        <li>poskytovatel e-mailových služeb.</li>
      </ul>
      <p>Údaje mohou být dále předány osobám, kterým to ukládá právní předpis, a v nezbytném rozsahu
      provozovateli distribuční soustavy, pokud je to potřebné k vyřízení vaší zakázky (například
      k podání žádosti o provoz výrobny vaším jménem).</p>

      <h2>4. Předávání mimo EU</h2>
      <p>Někteří zpracovatelé mohou zpracovávat údaje na serverech mimo Evropskou unii. V takovém
      případě se předání opírá o rozhodnutí Evropské komise o odpovídající ochraně, nebo o standardní
      smluvní doložky schválené Evropskou komisí.</p>

      <h2>5. Cookies a analytika</h2>
      <p>Tento web nepoužívá analytické ani reklamní cookies a nesleduje chování návštěvníků.
      Písma i ostatní části stránky se načítají přímo z tohoto webu, ne z externích služeb.</p>

      <h2>6. Vaše práva</h2>
      <ul>
        <li>právo na přístup k osobním údajům,</li>
        <li>právo na opravu nepřesných údajů,</li>
        <li>právo na výmaz, pokud odpadl důvod zpracování,</li>
        <li>právo na omezení zpracování,</li>
        <li>právo na přenositelnost údajů,</li>
        <li>právo vznést námitku proti zpracování založenému na oprávněném zájmu,</li>
        <li>právo podat stížnost u Úřadu pro ochranu osobních údajů, Pplk. Sochora 27, 170 00 Praha 7,
        <a href="https://www.uoou.cz" target="_blank" rel="noopener">www.uoou.cz</a>.</li>
      </ul>
      <p>Svá práva uplatníte na adrese <a href="mailto:info@bfksystems.cz">info@bfksystems.cz</a>.
      Odpovíme nejpozději do jednoho měsíce.</p>

      <h2>7. Zabezpečení</h2>
      <p>Přenos dat mezi vaším prohlížečem a webem je šifrovaný. Přístup k údajům mají jen pracovníci,
      kteří je potřebují k vyřízení vaší poptávky nebo zakázky.</p>

      <h2>8. Změny</h2>
      <p>Zásady můžeme aktualizovat, pokud se změní způsob zpracování nebo právní úprava. Aktuální
      verze je vždy dostupná na této stránce.</p>
    </div>"""),
    "bez_kontaktu": True,
})

STRANKY.append({
    "slug": "404.html", "nav": "", "noindex": True, "bez_kontaktu": True,
    "title": "Stránka nenalezena",
    "desc": "Požadovaná stránka na webu bfksystems.cz neexistuje nebo byla přesunuta.",
    "eyebrow": "Chyba 404", "h1": "Tuhle stránku jsme nenašli",
    "breadcrumb": None,
    "intro": "<p>Odkaz může být zastaralý, nebo v adrese chybí písmeno. Zkuste některý z rozcestníků "
             "níže – nebo nám rovnou zavolejte na +420 776 111 100.</p>",
    "body": sekce(
        "Kam dál",
        karty([
            (I["blesk"], "Služby",
             "<p>Commissioning, dispečerské řízení, VN a trafostanice, velké FVE a servis.</p>",
             "sluzby.html"),
            (I["graf"], "Simulační zkoušky",
             "<p>Ověření souladu výroben s RfG.</p>", "simulacni-zkousky.html"),
            (I["baterie"], "Bateriová úložiště",
             "<p>Oživení, řízení a ověření souladu.</p>", "bateriova-uloziste.html"),
            (I["info"], "Reference",
             "<p>Fotky z našich realizací.</p>", "reference.html"),
        ]),
    ),
})

# ===================================================== EN a DE (zatim) ======
# Zastupne stranky pro prepinac jazyku – preklad webu prijde po schvaleni ceske
# verze. Neindexuji se (noindex) a nejsou v sitemape. Texty odpovidaji ceskym.
KONTAKT_EN = ('Contact us: <a href="tel:+420776111100">+420 776 111 100</a> · '
              '<a href="mailto:info@bfksystems.cz">info@bfksystems.cz</a>')
KONTAKT_DE = ('Kontakt: <a href="tel:+420776111100">+420 776 111 100</a> · '
              '<a href="mailto:info@bfksystems.cz">info@bfksystems.cz</a>')

STRANKY.append({
    "slug": "en.html", "nav": "", "jazyk": "en", "noindex": True, "bez_kontaktu": True,
    "title": "BFK Systems – English version coming soon",
    "desc": "The English version of the BFK Systems website is being prepared. Commissioning of large PV "
            "plants, dispatch control, MV substations and battery storage in the Czech Republic.",
    "eyebrow": "BFK Systems s.r.o.", "h1": "English version coming soon",
    "breadcrumb": None,
    "intro": "<p>We are preparing the English version of our website. Until it is ready, please get in "
             "touch directly – we will be glad to hear about your project.</p>",
    "body": sekce(
        "What we do",
        karty([
            (I["blesk"], "Commissioning of large PV plants",
             "<p>Professional commissioning of large photovoltaic power plants, including all tests "
             "and inspections.</p>"),
            (I["rizeni"], "Dispatch control and balancing",
             "<p>Modern systems for control, regulation and connection of your power plant to the grid, "
             "including balancing services.</p>"),
            (I["tovarna"], "MV switchgear and substations",
             "<p>Modernisation and reconstruction of medium-voltage equipment and transformer "
             "stations.</p>"),
            (I["panel"], "Commercial and utility-scale PV",
             "<p>Complete delivery of large solar parks and industrial installations.</p>"),
            (I["baterie"], "Battery energy storage",
             "<p>Commissioning, spot-price based control, integration with PV and compliance "
             "verification.</p>"),
            (I["graf"], "RfG compliance",
             "<p>Model simulations, on-site tests and documentation for the distribution system "
             "operator. Service technicians across the whole Czech Republic.</p>"),
        ], sloupce=3)
        + cta(KONTAKT_EN, "Czech version", "index.html"),
        eyebrow="Services",
    ),
})

STRANKY.append({
    "slug": "de.html", "nav": "", "jazyk": "de", "noindex": True, "bez_kontaktu": True,
    "title": "BFK Systems – deutsche Version in Vorbereitung",
    "desc": "Die deutsche Version der Website von BFK Systems wird vorbereitet. Inbetriebnahme großer "
            "PV-Anlagen, Fernsteuerung, Mittelspannung und Batteriespeicher in Tschechien.",
    "eyebrow": "BFK Systems s.r.o.", "h1": "Deutsche Version in Vorbereitung",
    "breadcrumb": None,
    "intro": "<p>Wir bereiten die deutsche Version unserer Website vor. Bis dahin sprechen Sie uns gerne "
             "direkt an – wir freuen uns auf Ihr Projekt.</p>",
    "body": sekce(
        "Was wir machen",
        karty([
            (I["blesk"], "Inbetriebnahme von PV-Großanlagen",
             "<p>Professionelle Inbetriebnahme großer Photovoltaikanlagen einschließlich aller "
             "Prüfungen und Revisionen.</p>"),
            (I["rizeni"], "Fernsteuerung und Regelenergie",
             "<p>Moderne Systeme für Steuerung, Regelung und Netzanbindung Ihrer Anlage – "
             "einschließlich Regelenergie.</p>"),
            (I["tovarna"], "Mittelspannung und Trafostationen",
             "<p>Modernisierung und Umbau von Mittelspannungsanlagen und Transformatorstationen.</p>"),
            (I["panel"], "Gewerbliche PV und Solarparks",
             "<p>Komplette Realisierung großer Solarparks und industrieller Anlagen.</p>"),
            (I["baterie"], "Batteriespeicher",
             "<p>Inbetriebnahme, Steuerung nach Spotmarktpreisen, Einbindung in die PV-Anlage und "
             "Konformitätsnachweis.</p>"),
            (I["graf"], "Konformitätsnachweis nach RfG",
             "<p>Simulationen am Anlagenmodell, Prüfungen vor Ort und Dokumentation für den "
             "Verteilnetzbetreiber. Servicetechniker in ganz Tschechien.</p>"),
        ], sloupce=3)
        + cta(KONTAKT_DE, "Tschechische Version", "index.html"),
        eyebrow="Leistungen",
    ),
})

# ================================================ ZDROJE A DATUM AKTUALIZACE ======
# (datum, dokumenty) – vypisuje se dole na strance jako „Aktualizováno … Zdroje: …“.
# Texty o RfG jsou prevzate z webu simulacni-zkousky.cz, kde byly naposledy
# zkontrolovane 14. 9. 2026. Datum menit jen po skutecne kontrole obsahu.
P4 = "PPDS, příloha 4 (2025)"
METODIKY = "(ČEZ Distribuce, EG.D, PREdistribuce)"
ZDROJE = {
    "simulacni-zkousky.html": ("14. 9. 2026",
        "nařízení Komise (EU) 2016/631 (RfG) · " + P4 + ", Tab. 1 · metodiky ověřování souladu B1, "
        "B2, C a D " + METODIKY + ", platné od 1. 2. 2025"),
    "bateriova-uloziste.html": ("14. 9. 2026",
        P4 + " · dodatky č. 1 a 2 k připojovacím podmínkám ČEZ Distribuce pro zařízení pro ukládání "
        "elektřiny, platné od 1. 9. 2025 · metodika ověřování souladu ZUE typu D " + METODIKY
        + ", platná od 1. 9. 2025"),
}

# Stranky sluzeb dostanou JSON-LD Service.
SLUZBY = {
    "simulacni-zkousky.html": "Simulační zkoušky a ověření souladu výroben s RfG",
    "bateriova-uloziste.html": "Oživení, řízení a ověření souladu bateriových úložišť",
}

for _p in STRANKY:
    if _p["slug"] in ZDROJE:
        _p["zdroj"] = ZDROJE[_p["slug"]]
    if _p["slug"] in SLUZBY:
        _p["sluzba"] = SLUZBY[_p["slug"]]

PAGES = STRANKY
