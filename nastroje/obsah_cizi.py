#!/usr/bin/env python3
"""Anglicka a nemecka verze webu bfksystems.cz.

Stranky maji stejnou strukturu i komponenty jako ceske (obsah.py), jen jiny
jazyk. Slugy a menu drzi build.py (EKVIVALENTY, NAV_EN, NAV_DE) – kdyz se tady
prida stranka, musi dostat protejsek i tam.

Zdroj pravdy pro obsah je ceska verze. Preklad je volnejsi tam, kde cesky text
mluvi o ceskych pravidlech (PPDS, UPOS/UTP) – cizojazycnemu ctenari se radeji
vysvetli, co ten pojem znamena, nez aby se prelozil doslova.
"""

from __future__ import annotations

from obsah import I, callout, cta, foto, karty, kotvy, sekce, seznam, tabulka

STRANKY: list[dict] = []

TEL = "+420 776 111 100"
MAIL = "info@bfksystems.cz"
WEB_SZ = "https://www.simulacni-zkousky.cz/"


def galerie(polozky, sloupce=4):
    """Mrizka fotek referenci s prelozenymi popisky: (soubor, nadpis, popis, alt)."""
    kusy = []
    for nazev, nadpis, popis, alt in polozky:
        kusy.append(f'      <figure>\n        {foto(nazev, alt)}\n'
                    f'        <figcaption><b>{nadpis}</b><span>{popis}</span></figcaption>\n'
                    f'      </figure>')
    trida = "gallery" + (" cols-3" if sloupce == 3 else "")
    return f'    <div class="{trida}">\n' + "\n".join(kusy) + "\n    </div>"


def hero(eyebrow, h1, claim, lead, tlacitko1, href1, tlacitko2, href2):
    """Uvodni banner se stridanim tri fotek – stejny jako na ceske titulce."""
    return f"""<!-- HERO -->
<section class="hero">
  <div class="photo">
    <picture>
      <source type="image/webp" srcset="assets/title-photo-1024.webp 1024w, assets/title-photo.webp 2048w" sizes="100vw">
      <img class="snimek je-videt" src="assets/title-photo.jpg" alt="{lead[0]}" width="2048" height="1536" fetchpriority="high" srcset="assets/title-photo-1024.jpg 1024w, assets/title-photo.jpg 2048w" sizes="100vw">
    </picture>
    <picture>
      <source type="image/webp" srcset="assets/hero-2-1024.webp 1024w, assets/hero-2.webp 2000w" sizes="100vw">
      <img class="snimek" src="assets/hero-2.jpg" alt="{lead[1]}" width="2000" height="1125" loading="lazy" srcset="assets/hero-2-1024.jpg 1024w, assets/hero-2.jpg 2000w" sizes="100vw">
    </picture>
    <picture>
      <source type="image/webp" srcset="assets/hero-3-1024.webp 1024w, assets/hero-3.webp 1600w" sizes="100vw">
      <img class="snimek" src="assets/hero-3.jpg" alt="{lead[2]}" width="1600" height="960" loading="lazy" srcset="assets/hero-3-1024.jpg 1024w, assets/hero-3.jpg 1600w" sizes="100vw">
    </picture>
  </div>
  <div class="gradient-overlay"></div>
  <div class="content">
    <p class="hero-eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="hero-claim-big">{claim}</p>
    <p class="hero-lead">{lead[3]}</p>
    <div class="cta-row">
      <a class="btn btn-primary" href="{href1}">{tlacitko1}</a>
      <a class="btn btn-light" href="{href2}">{tlacitko2}</a>
    </div>
  </div>
</section>
<script src="assets/hero.js" defer></script>
"""


def formular(jazyk, popisky):
    """Poptavkovy formular. Klic Web3Forms zatim chybi i v ceske verzi."""
    (nadpis, uvod, jmeno, firma, mail, telefon, tema, zprava, zprava_hint,
     souhlas, odeslat, temata) = popisky
    moznosti = "\n".join(f'              <option>{t}</option>' for t in temata)
    zdroj = {"en": "BFK Systems – English contact page",
             "de": "BFK Systems – deutsche Kontaktseite"}[jazyk]
    return f"""<section class="contact-section" id="formular">
  <div class="container">
    <div class="section-head">
      <h2>{nadpis}</h2>
      <p class="lead">{uvod}</p>
    </div>
    <form class="contact-form" id="contact-form" action="https://api.web3forms.com/submit" method="post" autocomplete="on">
      <input type="hidden" name="access_key" value="PLACEHOLDER-DOPLNIT-KLIC-WEB3FORMS">
      <input type="hidden" name="subject" value="{zdroj}">
      <input type="hidden" name="from_name" value="bfksystems.cz">
      <input type="hidden" name="replyto" value="">
      <div class="hp-field" aria-hidden="true">
        <label for="botcheck">Leave empty</label>
        <input type="checkbox" id="botcheck" name="botcheck" tabindex="-1" autocomplete="off">
      </div>
      <div class="row">
        <div class="field">
          <label for="f-name">{jmeno} *</label>
          <input type="text" id="f-name" name="{jmeno}" required>
        </div>
        <div class="field">
          <label for="f-company">{firma}</label>
          <input type="text" id="f-company" name="{firma}">
        </div>
        <div class="field">
          <label for="f-email">{mail} *</label>
          <input type="email" id="f-email" name="{mail}" required>
        </div>
        <div class="field">
          <label for="f-phone">{telefon}</label>
          <input type="tel" id="f-phone" name="{telefon}">
        </div>
        <div class="field full">
          <label for="f-topic">{tema}</label>
          <select id="f-topic" name="{tema}">
{moznosti}
          </select>
        </div>
        <div class="field full">
          <label for="f-message">{zprava}</label>
          <textarea id="f-message" name="{zprava}" placeholder="{zprava_hint}"></textarea>
        </div>
        <div class="field full">
          <p class="gdpr">{souhlas}</p>
          <button type="submit">{odeslat}</button>
        </div>
      </div>
      <input type="hidden" name="{'Sent from' if jazyk == 'en' else 'Gesendet von'}" value="{zdroj}">
    </form>
    <div id="contact-status" role="status"></div>
  </div>
</section>
<script src="assets/form.js" defer></script>
"""


# ============================================================== ENGLISH ======
EN_HERO_ALT = [
    "Photovoltaic plant on an industrial roof",
    "Ground-mounted PV plant at sunset",
    "BFK Systems installation team in front of a completed ground-mounted plant",
    "We commission utility-scale PV plants, connect them to dispatch control and rebuild "
    "medium-voltage switchgear and substations. We commission battery storage and prove "
    "grid compliance by simulation and on-site testing.",
]

STRANKY.append({
    "slug": "en.html", "nav": "", "jazyk": "en",
    "title": "BFK Systems – utility-scale PV, dispatch control, MV and battery storage",
    "desc": "BFK Systems s.r.o.: commissioning of utility-scale PV plants, dispatch control and "
            "balancing services, MV switchgear and substations, battery storage and RfG "
            "compliance testing across the Czech Republic.",
    "body": hero(
        "BFK Systems · experts in utility-scale PV projects",
        "Partner for utility-scale PV and&nbsp;battery storage",
        "From commissioning and dispatch control to on-call service – anywhere in Czechia.",
        EN_HERO_ALT,
        "Request a quote", "en-contact.html#formular", "Our services", "en-services.html",
    ) + sekce(
        "What we specialise in",
        karty([
            (I["blesk"], "PV commissioning",
             "<p>Professional commissioning of utility-scale photovoltaic plants, including all "
             "tests and electrical inspections.</p>", "en-services.html#commissioning"),
            (I["rizeni"], "Dispatch control and balancing",
             "<p>Control and telemetry systems that connect your plant to the distribution "
             "operator and to balancing markets.</p>", "en-services.html#rizeni"),
            (I["tovarna"], "MV switchgear and substations",
             "<p>Rebuilds and upgrades of medium-voltage sections and transformer stations for "
             "maximum output and safety.</p>", "en-services.html#vn"),
            (I["panel"], "Commercial and utility-scale PV",
             "<p>A partner for the full delivery of large photovoltaic parks and industrial "
             "rooftop installations.</p>", "en-services.html#fve"),
            (I["graf"], "Grid compliance (RfG)",
             "<p>Compliance of generating modules with grid code requirements – by simulation, "
             "by on-site testing or by equipment certificate.</p>", "en-grid-compliance.html"),
            (I["baterie"], "Battery storage",
             "<p>Commissioning, control by spot prices, integration with PV and proof of "
             "compliance for storage facilities.</p>", "en-battery-storage.html"),
        ], sloupce=3),
        eyebrow="Services",
        uvod='<p class="lead">We focus on commercial and industrial photovoltaic systems and '
             'battery storage, with a reach across the whole Czech Republic.</p>',
    ) + sekce(
        "Why clients work with us",
        karty([
            (I["sit"], "The engineering side under one roof",
             "<p>Commissioning, dispatch control, MV works and compliance evidence come from one "
             "team, so nothing falls between suppliers.</p>"),
            (I["hodiny"], "Large and demanding projects",
             "<p>Plants on medium voltage, container battery storage, substations – the kind of "
             "work that needs grid-code knowledge, not just a mounting crew.</p>"),
            (I["klic"], "Service across the country",
             "<p>Our own technicians cover the whole Czech Republic, with service contracts and "
             "on-call response for operators.</p>"),
        ], sloupce=3),
        alt=True,
    ) + sekce(
        "Part of the BF technology group",
        '<p>BFK Systems s.r.o. works alongside <b>BF technology s.r.o.</b>, which delivers '
        'photovoltaics for family houses, apartment buildings and companies, and alongside the '
        f'<a href="{WEB_SZ}" target="_blank" rel="noopener">simulacni-zkousky.cz</a> team '
        'dedicated to RfG compliance. Together we cover a project from the first study to '
        'permanent operation.</p>'
        + cta("Tell us what you are planning and we will say what it takes.",
              "Request a quote", "en-contact.html#formular"),
        eyebrow="Group",
    ),
})

STRANKY.append({
    "slug": "en-services.html", "nav": "sluzby", "jazyk": "en",
    "title": "Services – PV commissioning, dispatch control, MV and service",
    "desc": "Commissioning of utility-scale PV plants, dispatch control and balancing, MV "
            "switchgear and substations, commercial PV, compliance testing, battery storage "
            "and service across the Czech Republic.",
    "eyebrow": "What we do", "h1": "Services",
    "claim": "Commercial and industrial PV plants and battery storage across Czechia.",
    "bc_nazev": "Services", "breadcrumb": [],
    "intro": "<p>From commissioning through control systems, medium voltage and substations to "
             "service. We concentrate on large and technically demanding projects.</p>",
    "anchors": kotvy([("Commissioning", "commissioning"), ("Dispatch control", "rizeni"),
                      ("MV and substations", "vn"), ("Commercial PV", "fve"),
                      ("Compliance testing", "rfg"), ("Battery storage", "bess"),
                      ("Service", "servis")]),
    "body": sekce(
        "PV commissioning",
        "<p>We put utility-scale photovoltaic plants into operation – from functional tests of "
        "inverters and protection devices to electrical inspection reports and handover "
        "documentation.</p>"
        + seznam(["commissioning of inverters, transformers and protection relays",
                  "settings according to the connection conditions of the grid operator",
                  "electrical inspection and commissioning records",
                  "handover documentation and training of the operator"]),
        eyebrow="Commissioning", kotva="commissioning",
    ) + sekce(
        "Dispatch control and balancing",
        "<p>We implement control and telemetry systems that let the plant follow the distribution "
        "operator, the market, or both.</p>"
        + seznam(["RTU and control system for MV plants (Weidmüller components)",
                  "connection of the plant to the distribution operator's dispatch centre",
                  "SCADA, control of heating and charging stations",
                  "control by spot prices",
                  "participation in balancing services and aggregation"]),
        eyebrow="Control", kotva="rizeni", alt=True,
    ) + sekce(
        "MV switchgear and substations",
        "<p>We rebuild and extend medium-voltage sections – from a single switchgear panel to a "
        "complete kiosk substation.</p>"
        + seznam(["replacement and extension of MV switchgear panels",
                  "rebuilds of transformer stations including measurement",
                  "work according to the connection conditions of the grid operator",
                  "coordination with the operator up to energisation"]),
        eyebrow="Medium voltage", kotva="vn",
    ) + sekce(
        "Commercial and utility-scale PV",
        "<p>We deliver large rooftop and ground-mounted plants for industrial clients and "
        "investors, including the parts that usually cause delays: grid connection, protection "
        "settings and compliance evidence.</p>"
        + seznam(["design, delivery and installation of the plant",
                  "MV connection, transformer station, measurement",
                  "control system and remote supervision",
                  "compliance evidence and permanent operation"]),
        eyebrow="PV plants", kotva="fve", alt=True,
    ) + sekce(
        "Compliance testing and grid code",
        karty([
            (I["graf"], "Compliance simulation",
             "<p>A model of the plant in DIgSILENT PowerFactory and the set of studies the "
             "operator requires.</p>"),
            (I["lupa"], "On-site testing",
             "<p>Functional tests of the generating module directly at the plant, with recorded "
             "waveforms.</p>"),
            (I["dok"], "Documentation and negotiation",
             "<p>We compile the evidence and handle the exchange with the distribution "
             "operator.</p>"),
        ], sloupce=3)
        + cta('Grid compliance has its own page with categories, deadlines and frequent '
              'questions.', "Grid compliance in detail", "en-grid-compliance.html"),
        eyebrow="RfG", kotva="rfg",
    ) + sekce(
        "Battery storage",
        karty([
            (I["baterie"], "Commissioning",
             "<p>We put the storage system into operation, including the battery management "
             "system and the link to the inverters.</p>"),
            (I["rizeni"], "Control and PV integration",
             "<p>Charging by spot prices, use of surplus production, peak shaving.</p>"),
            (I["graf"], "Compliance",
             "<p>Storage is a generating module too – we provide the evidence for both "
             "directions of power flow.</p>"),
        ], sloupce=3)
        + cta("How storage is commissioned, controlled and proven.",
              "Battery storage in detail", "en-battery-storage.html"),
        eyebrow="Storage", kotva="bess", alt=True,
    ) + sekce(
        "Service and maintenance",
        karty([
            (I["klic"], "Technicians across Czechia",
             "<p>Our own service team, not a subcontracted one.</p>"),
            (I["hodiny"], "Response when it stops",
             "<p>Fault diagnosis, repair or replacement of inverters, protection devices and "
             "communication units.</p>"),
            (I["dok"], "Service contracts",
             "<p>Regular inspections, remote supervision and agreed response times.</p>"),
        ], sloupce=3),
        eyebrow="Service", kotva="servis",
    ),
})

STRANKY.append({
    "slug": "en-grid-compliance.html", "nav": "rfg", "jazyk": "en",
    "title": "Grid compliance (RfG) – simulations and on-site testing",
    "desc": "Compliance of generating modules with the grid code: simulations in DIgSILENT "
            "PowerFactory, on-site testing, documentation for the distribution operator. "
            "Categories A1 to D, PV plants and battery storage.",
    "eyebrow": "Compliance", "h1": "Grid compliance and RfG testing",
    "claim": "Simulation, on-site testing and the paperwork that goes with it.",
    "bc_nazev": "Grid compliance", "breadcrumb": [],
    "intro": "<p>Every generating module connected to the Czech grid has to prove that it meets "
             "the requirements of the European network code RfG and the national grid code. We "
             "provide that proof – by simulation, by testing at the plant, or by both.</p>",
    "anchors": kotvy([("What we do", "co"), ("Categories", "kategorie"),
                      ("Three routes", "cesty"), ("Questions", "faq")]),
    "body": sekce(
        "What we do for you",
        karty([
            (I["graf"], "Compliance simulation",
             "<p>A model of the plant in DIgSILENT PowerFactory and the studies required by the "
             "distribution operator, with a pass / fail assessment.</p>"),
            (I["lupa"], "On-site testing",
             "<p>Functional tests on the finished plant with recorded waveforms – for category "
             "B1 there are six requirements that cannot be proven any other way.</p>"),
            (I["dok"], "Documentation and negotiation",
             "<p>We compile the evidence into the form the operator expects and handle the "
             "correspondence until approval.</p>"),
            (I["baterie"], "Battery storage",
             "<p>Storage is a generating module as well. Classification and the way compliance "
             "is proven follow the current rules of the relevant operator.</p>"),
        ], sloupce=2),
        eyebrow="Scope", kotva="co",
    ) + sekce(
        "Categories of generating modules",
        "<p>The scope of verification follows the category of the generating module.</p>"
        + tabulka(
            ["Category", "Capacity", "On-site tests", "Simulations"],
            [["A1", "0.8 kW to 11 kW", "normally no", "normally no"],
             ["A2", "above 11 kW, below 100 kW", "normally no", "normally no"],
             ["B1", "100 kW to below 1 MW", "yes", "selected points"],
             ["B2", "1 MW to below 30 MW", "yes", "wider scope"],
             ["C", "30 MW to below 75 MW", "yes", "widest scope"],
             ["D", "from 75 MW, or connection at 110 kV", "yes", "widest scope"]],
            poznamky=["<b>The category is stated in the connection agreement</b> and that document "
                      "always prevails.",
                      "<b>Mind the units:</b> the kWp of the panels is not the figure that "
                      "determines the category. What counts is the rated active power of the "
                      "generating module – 698 kWp of panels can be a module with P<sub>n</sub> "
                      "550 kW."],
        ),
        eyebrow="Rules", kotva="kategorie", alt=True,
    ) + sekce(
        "Three routes to proving a requirement",
        karty([
            (I["lupa"], "On-site test",
             "<p>Verification on the finished plant and a test report. Some requirements cannot "
             "be proven in any other way.</p>"),
            (I["graf"], "Simulation",
             "<p>A model of the plant and a report with a pass / fail assessment. For category "
             "B2 and above the scope of simulation is considerably wider.</p>"),
            (I["stit"], "Equipment certificate",
             "<p>Issued by a certification body for a specific device. Our test or simulation "
             "report is not a certificate; a certificate replaces a test only where the "
             "generating module document allows it.</p>"),
        ], sloupce=3)
        + cta("Categories, operators, deadlines and the required documents are described in "
              "detail on our dedicated website.",
              "Go to simulacni-zkousky.cz", WEB_SZ),
        eyebrow="Key concept", kotva="cesty",
    ),
    "faq_nadpis": "Frequently asked questions",
    "faq": [
        ("Do we need testing for a plant below 100 kW?",
         "<p>Modules in categories A1 and A2 are normally proven by documentation and an "
         "equipment certificate, not by on-site testing. The connection agreement and the "
         "operator's current rules decide.</p>"),
        ("What do you need from us to start?",
         "<p>The connection agreement, the single-line diagram, inverter and protection data "
         "sheets and the protection settings. For testing we also agree a date when the plant "
         "can be operated freely for a few hours.</p>"),
        ("Do you also handle the communication with the distribution operator?",
         "<p>Yes. We prepare the evidence in the required form and resolve comments with the "
         "operator until the module is approved.</p>"),
        ("Does a battery storage system need the same evidence?",
         "<p>Storage is assessed as a generating module too, and the verification covers both "
         "directions of power flow – charging and discharging.</p>"),
    ],
    "cross": [("Services", "en-services.html"), ("Battery storage", "en-battery-storage.html"),
              ("References", "en-references.html")],
})

STRANKY.append({
    "slug": "en-battery-storage.html", "nav": "bess", "jazyk": "en",
    "title": "Battery storage – commissioning, control and compliance",
    "desc": "Commissioning of battery energy storage, control by spot prices, integration with "
            "photovoltaics, dispatch control, telemetry and proof of grid compliance.",
    "eyebrow": "Storage", "h1": "Battery energy storage",
    "claim": "From commissioning to control by spot prices and compliance evidence.",
    "bc_nazev": "Battery storage", "breadcrumb": [],
    "intro": "<p>We commission container and indoor storage systems, connect them to control "
             "systems and prove their compliance with the grid code. For the operator the point "
             "is simple: the storage has to earn money and stay within the rules.</p>",
    "anchors": kotvy([("What we do", "co"), ("Compliance", "soulad"),
                      ("Adding storage to an existing plant", "doplneni"), ("Questions", "faq")]),
    "body": sekce(
        "What we do for storage systems",
        karty([
            (I["blesk"], "Commissioning",
             "<p>Putting the system into operation including the battery management system, "
             "inverters and protection devices.</p>"),
            (I["cena"], "Control by spot prices",
             "<p>Charging when electricity is cheap, discharging when it is expensive – with "
             "limits that respect the connection agreement.</p>"),
            (I["panel"], "Integration with photovoltaics",
             "<p>Using surplus production, peak shaving and backup of selected circuits.</p>"),
            (I["rizeni"], "Dispatch control and telemetry",
             "<p>Connection to the operator's dispatch centre, RTU, SCADA and remote "
             "supervision.</p>"),
            (I["graf"], "Compliance",
             "<p>Simulations and tests for the storage as a generating module.</p>"),
            (I["klic"], "Service",
             "<p>Inspections, firmware updates, diagnostics of weak cells and repairs.</p>"),
        ], sloupce=3),
        eyebrow="Scope", kotva="co",
    ) + sekce(
        "Compliance is verified in both directions",
        "<p>A storage system both draws power and feeds it back, so the operator wants evidence "
        "for charging and for discharging. The classification and the required scope follow the "
        "current rules of the relevant distribution operator – which is why we settle this "
        "before the equipment is ordered, not after it is installed.</p>"
        + callout("Watch the ratings",
                  "<p>The usable capacity in kWh says nothing about the category. What counts is "
                  "the rated active power of the module at the connection point.</p>"),
        eyebrow="Grid code", kotva="soulad", alt=True,
    ) + sekce(
        "Adding storage to an existing plant",
        "<p>Adding a battery to a plant that is already running is not only a technical job. "
        "Depending on the size and the operator it may mean a change to the connection "
        "agreement, new protection settings and fresh compliance evidence.</p>"
        + seznam(["review of the existing connection agreement and protection settings",
                  "proposal of capacity and power that fits the consumption profile",
                  "wiring, commissioning and control settings",
                  "documentation for the operator and permanent operation"])
        + cta("Tell us the plant size and the consumption profile and we will say what adding "
              "storage would require.", "Request a quote", "en-contact.html#formular"),
        eyebrow="Upgrades", kotva="doplneni",
    ),
    "faq_nadpis": "Frequently asked questions",
    "faq": [
        ("Does storage pay off without photovoltaics?",
         "<p>It can, if the site has a suitable tariff and consumption profile – the margin then "
         "comes from the price spread during the day. We calculate it on your real consumption "
         "data, not on a general assumption.</p>"),
        ("Will the storage keep the site running during an outage?",
         "<p>Only if it is designed for it. Backup operation needs the right inverter topology "
         "and a defined set of backed-up circuits; it is a design decision, not a setting.</p>"),
        ("Who is responsible for the batteries themselves?",
         "<p>The warranty is with the manufacturer. We commission the system, document faults "
         "and handle the claim with the supplier.</p>"),
    ],
    "cross": [("Grid compliance", "en-grid-compliance.html"), ("Services", "en-services.html"),
              ("References", "en-references.html")],
})

EN_GALERIE = [
    ("bess", "BESS commissioning", "Control by spot prices and integration with PV.",
     "Open battery storage container with battery modules"),
    ("fve-strechy", "PV installation (Sungrow)",
     "Dispatch control, SCADA, control of heating and charging stations.",
     "Photovoltaic panels on the roof of an industrial hall and a neighbouring building"),
    ("rtu-vn", "Dispatch control, MV 35 kV",
     "RTU (Weidmüller components) and control system for a medium-voltage PV plant.",
     "RTU cabinet with Weidmüller components"),
    ("stridace-sungrow", "Industrial PV plant",
     "Installation of Sungrow inverters and AC distribution boards.",
     "Sungrow inverters and AC boards on the wall of a hall"),
    ("fve-solaredge", "Commercial PV (SolarEdge)",
     "PV plant with SolarEdge technology including dispatch control.",
     "SolarEdge inverters and a distribution board on a support structure"),
    ("rozvadec-ac", "AC board manufacturing",
     "AC board combining the output of four Sungrow inverters.",
     "Open AC distribution board with busbars and circuit breakers"),
    ("vn-rozvadece", "MV switchgear replacement",
     "New MV panels installed according to the connection conditions (3× metering).",
     "Technicians installing new MV switchgear"),
    ("trafostanice", "Substation rebuild",
     "Complete rebuild and installation of a 35 kV kiosk substation.",
     "Crane placing a kiosk substation"),
]

STRANKY.append({
    "slug": "en-references.html", "nav": "reference", "jazyk": "en",
    "title": "References – PV plants, MV, substations and battery storage",
    "desc": "Selected projects of BFK Systems: battery storage commissioning, dispatch control "
            "on medium voltage, MV switchgear and substation rebuilds, commercial PV plants and "
            "compliance verification.",
    "eyebrow": "Project photos", "h1": "References",
    "claim": "A selection of what we have put into operation.",
    "bc_nazev": "References", "breadcrumb": [],
    "intro": "<p>Photographs from our own projects – commissioning, control systems, medium "
             "voltage and storage. Client names are not published; we are happy to give "
             "specific references on request.</p>",
    "body": sekce("Projects", galerie(EN_GALERIE), eyebrow="Our work")
    + sekce(
        "Compliance verification",
        karty([
            (I["graf"], "PV plant, category D",
             "<p>Simulations and on-site testing for a plant connected at 110 kV.</p>"),
            (I["lupa"], "PV plant, category B1",
             "<p>On-site testing of the six requirements that cannot be proven otherwise, plus "
             "selected simulations.</p>"),
            (I["baterie"], "PV plant with battery",
             "<p>Verification of the module in both directions of power flow.</p>"),
        ], sloupce=3)
        + cta("Would you like a reference for a specific type of project? Tell us what you are "
              "planning and we will send relevant examples.",
              "Request a quote", "en-contact.html#formular"),
        eyebrow="Grid code", alt=True,
    ),
    "cross": [("Services", "en-services.html"), ("Grid compliance", "en-grid-compliance.html"),
              ("About us", "en-about.html")],
})

STRANKY.append({
    "slug": "en-about.html", "nav": "onas", "jazyk": "en",
    "title": "About us – BFK Systems s.r.o., Děčín",
    "desc": "BFK Systems s.r.o. from Děčín: a team with background in power engineering, "
            "industrial automation and finance, focused on utility-scale PV, medium voltage "
            "and battery storage.",
    "eyebrow": "Who we are", "h1": "About us",
    "claim": "A team that covers the engineering side of a PV project.",
    "bc_nazev": "About us", "breadcrumb": [],
    "intro": "<p>BFK Systems s.r.o. is based in Děčín and works across the whole Czech Republic. "
             "We focus on projects where the demanding part is not the mounting system but the "
             "grid connection, control and compliance.</p>",
    "body": sekce(
        "Our team",
        karty([
            (I["clovek"], "Bc. Petr Fencl",
             "<p>Commissioning, control systems and grid compliance. Leads the technical side of "
             "projects.</p>"),
            (I["clovek"], "PhDr. Jan Böhme",
             "<p>Sales and project management, contracts and financing of installations.</p>"),
            (I["clovek"], "Michal Kovář",
             "<p>Medium voltage, substations and site management of installation teams.</p>"),
        ], sloupce=3),
        eyebrow="People",
    ) + sekce(
        "What sets us apart",
        karty([
            (I["tovarna"], "Large and demanding projects",
             "<p>Medium-voltage plants, container storage and substations – work that needs grid "
             "code knowledge.</p>"),
            (I["sit"], "Power engineering, automation and finance",
             "<p>Three fields that a large project needs at the same time.</p>"),
            (I["klic"], "Engineering under one roof",
             "<p>Commissioning, control, MV and compliance evidence from one team.</p>"),
            (I["mapa"], "Service across the country",
             "<p>Our own technicians, service contracts and agreed response times.</p>"),
        ], sloupce=2),
        alt=True,
    ) + sekce(
        "Part of the BF technology group",
        karty([
            (I["graf"], "simulacni-zkousky.cz",
             "<p>A dedicated team for RfG compliance – simulations, on-site testing and "
             "negotiations with distribution operators.</p>", WEB_SZ),
            (I["panel"], "bftechnology.cz",
             "<p>Photovoltaics for family houses, apartment buildings and companies, including "
             "battery storage and wallboxes.</p>", "https://www.bftechnology.cz/"),
        ], sloupce=2),
        eyebrow="Group",
    ) + sekce(
        "Company details",
        tabulka(["Item", "Value"],
                [["Company", "BFK Systems s.r.o."],
                 ["Registered office", "Obchodní 455/12, Děčín V-Rozbělesy, 405 02 Děčín"],
                 ["Company ID", "23571853"],
                 ["VAT ID", "CZ23571853"],
                 ["Phone", TEL],
                 ["E-mail", MAIL]]),
        alt=True,
    ),
    "cross": [("References", "en-references.html"), ("Services", "en-services.html"),
              ("Contact", "en-contact.html")],
})

EN_FORMULAR = (
    "Tell us what you are solving.",
    "The more we know up front, the more precise our answer is.",
    "Name", "Company", "E-mail", "Phone", "Topic", "Message",
    "Site location, plant or storage capacity, distribution operator, target date…",
    "By submitting the form you acknowledge that your data will be processed in order to answer "
    'your enquiry. We use Web3Forms as a processor. See our <a href="en-privacy.html">privacy '
    "policy</a> for details.",
    "Send enquiry",
    ["Commissioning of a PV plant", "Dispatch control and balancing",
     "MV switchgear or substation", "Grid compliance (RfG)", "Battery storage",
     "Service or service contract", "Something else"],
)

STRANKY.append({
    "slug": "en-contact.html", "nav": "kontakt", "jazyk": "en",
    "title": "Contact – BFK Systems s.r.o.",
    "desc": "Contact BFK Systems s.r.o., Děčín: phone +420 776 111 100, info@bfksystems.cz, "
            "enquiry form for PV commissioning, MV works, battery storage and RfG compliance.",
    "eyebrow": "Contact", "h1": "Get in touch",
    "claim": "We reply within two working days.",
    "bc_nazev": "Contact", "breadcrumb": [], "bez_kontaktu": True,
    "intro": "<p>The fastest way is a phone call or an e-mail. If you prefer, use the form "
             "below – it reaches the same inbox.</p>",
    "body": sekce(
        "Contact details",
        karty([
            (I["info"], "BFK Systems s.r.o.",
             "<p>Obchodní 455/12<br>Děčín V-Rozbělesy<br>405 02 Děčín<br>Czech Republic</p>"
             "<p>Company ID 23571853<br>VAT ID CZ23571853</p>"),
            (I["klic"], "Reach us",
             f'<p><a href="tel:+420776111100">{TEL}</a><br>'
             f'<a href="mailto:{MAIL}">{MAIL}</a></p>'
             "<p>Monday to Friday, 8:00–16:00 CET</p>"),
        ], sloupce=2),
        eyebrow="Where to find us",
    ) + formular("en", EN_FORMULAR),
    "cross": [("Services", "en-services.html"), ("Grid compliance", "en-grid-compliance.html"),
              ("About us", "en-about.html")],
})

STRANKY.append({
    "slug": "en-privacy.html", "nav": "", "jazyk": "en",
    "title": "Privacy policy",
    "desc": "How BFK Systems s.r.o. processes personal data submitted through the enquiry form "
            "and by e-mail: purpose, legal basis, processors and your rights.",
    "eyebrow": "Legal", "h1": "Privacy policy",
    "bc_nazev": "Privacy policy", "breadcrumb": [], "prio": "0.3",
    "intro": "<p>This page explains how BFK Systems s.r.o. handles the personal data you send "
             "us. The Czech version of this policy is the binding one; this translation is "
             "provided for convenience.</p>",
    "body": sekce(
        "Controller",
        "<p><b>BFK Systems s.r.o.</b>, Obchodní 455/12, Děčín V-Rozbělesy, 405 02 Děčín, Czech "
        f'Republic, Company ID 23571853. Contact: <a href="mailto:{MAIL}">{MAIL}</a>, '
        f'<a href="tel:+420776111100">{TEL}</a>.</p>',
    ) + sekce(
        "What we process and why",
        tabulka(["Data", "Purpose", "Legal basis"],
                [["Name, company, e-mail, phone", "Answering your enquiry and preparing a quote",
                  "Steps prior to a contract (Art. 6(1)(b) GDPR)"],
                 ["Content of your message", "Understanding what you need",
                  "Steps prior to a contract"],
                 ["Correspondence after the enquiry", "Project documentation",
                  "Legitimate interest (Art. 6(1)(f) GDPR)"]]),
        alt=True,
    ) + sekce(
        "Processors",
        "<p>The enquiry form is operated by <b>Web3Forms</b>, which forwards the message to our "
        "mailbox – it therefore acts as a processor. Our e-mail runs on <b>Google Workspace</b>. "
        "The website is hosted on <b>GitHub Pages</b>; the host records standard access logs. "
        "We do not pass your data to anyone else and we do not use it for marketing.</p>",
    ) + sekce(
        "How long we keep it",
        "<p>Enquiries that do not lead to a contract are kept for up to two years, so that we "
        "can follow up on an earlier conversation. Project correspondence is kept for the "
        "duration of the contract and for the statutory periods that follow.</p>",
        alt=True,
    ) + sekce(
        "Cookies",
        "<p>The website uses no analytics, advertising or tracking cookies. Nothing is stored in "
        "your browser beyond what is needed to display the page.</p>",
    ) + sekce(
        "Your rights",
        "<p>You may request access to your data, correction, erasure, restriction of processing "
        "or portability, and you may object to processing based on legitimate interest. Write to "
        f'<a href="mailto:{MAIL}">{MAIL}</a>. You also have the right to lodge a complaint with '
        "the Czech Office for Personal Data Protection (Úřad pro ochranu osobních údajů).</p>",
        alt=True,
    ),
})


# ============================================================== DEUTSCH ======
DE_HERO_ALT = [
    "Photovoltaikanlage auf einem Industriedach",
    "Freiflächen-Photovoltaikanlage bei Sonnenuntergang",
    "Montageteam von BFK Systems vor einer fertigen Freiflächenanlage",
    "Wir nehmen große Photovoltaikanlagen in Betrieb, binden sie an die Leitstelle an und "
    "sanieren Mittelspannungsteile und Trafostationen. Batteriespeicher setzen wir in Betrieb "
    "und weisen die Netzkonformität per Simulation und Vor-Ort-Prüfung nach.",
]

STRANKY.append({
    "slug": "de.html", "nav": "", "jazyk": "de",
    "title": "BFK Systems – große PV-Anlagen, Leitstellenanbindung, Mittelspannung und Speicher",
    "desc": "BFK Systems s.r.o.: Inbetriebnahme großer PV-Anlagen, Leitstellenanbindung und "
            "Regelleistung, Mittelspannung und Trafostationen, Batteriespeicher und "
            "Netzkonformität nach RfG – in ganz Tschechien.",
    "body": hero(
        "BFK Systems · Spezialisten für große PV-Projekte",
        "Partner für große PV-Anlagen und&nbsp;Batteriespeicher",
        "Von der Inbetriebnahme über die Leitstellenanbindung bis zum Service – in ganz Tschechien.",
        DE_HERO_ALT,
        "Unverbindliche Anfrage", "de-kontakt.html#formular", "Unsere Leistungen", "de-leistungen.html",
    ) + sekce(
        "Unsere Schwerpunkte",
        karty([
            (I["blesk"], "Inbetriebnahme von PV-Anlagen",
             "<p>Professionelle Inbetriebnahme großer Photovoltaikanlagen samt aller Prüfungen "
             "und Revisionen.</p>", "de-leistungen.html#commissioning"),
            (I["rizeni"], "Leitstellenanbindung und Regelleistung",
             "<p>Steuerungs- und Fernwirktechnik, die Ihre Anlage mit dem Verteilnetzbetreiber "
             "und den Regelleistungsmärkten verbindet.</p>", "de-leistungen.html#rizeni"),
            (I["tovarna"], "Mittelspannung und Trafostationen",
             "<p>Sanierung und Modernisierung von Mittelspannungsteilen und Trafostationen für "
             "volle Leistung und Sicherheit.</p>", "de-leistungen.html#vn"),
            (I["panel"], "Gewerbliche und große PV-Anlagen",
             "<p>Partner für die komplette Umsetzung großer Solarparks und industrieller "
             "Dachanlagen.</p>", "de-leistungen.html#fve"),
            (I["graf"], "Netzkonformität (RfG)",
             "<p>Nachweis der Konformität von Erzeugungsanlagen – per Simulation, Vor-Ort-Prüfung "
             "oder Anlagenzertifikat.</p>", "de-netzkonformitaet.html"),
            (I["baterie"], "Batteriespeicher",
             "<p>Inbetriebnahme, Steuerung nach Spotpreisen, Integration mit PV und "
             "Konformitätsnachweis.</p>", "de-batteriespeicher.html"),
        ], sloupce=3),
        eyebrow="Leistungen",
        uvod='<p class="lead">Wir konzentrieren uns auf gewerbliche und industrielle '
             'Photovoltaik sowie Batteriespeicher – mit Einsatzgebiet in ganz Tschechien.</p>',
    ) + sekce(
        "Warum Kunden mit uns arbeiten",
        karty([
            (I["sit"], "Technik aus einer Hand",
             "<p>Inbetriebnahme, Leitstellenanbindung, Mittelspannung und Konformitätsnachweis "
             "kommen aus einem Team – nichts fällt zwischen die Gewerke.</p>"),
            (I["hodiny"], "Große und anspruchsvolle Projekte",
             "<p>Anlagen auf Mittelspannung, Container-Speicher, Trafostationen – Arbeiten, die "
             "Kenntnis der Netzanschlussregeln verlangen.</p>"),
            (I["klic"], "Service im ganzen Land",
             "<p>Eigene Techniker, Wartungsverträge und vereinbarte Reaktionszeiten.</p>"),
        ], sloupce=3),
        alt=True,
    ) + sekce(
        "Teil der Gruppe BF technology",
        '<p>BFK Systems s.r.o. arbeitet eng mit <b>BF technology s.r.o.</b> zusammen, die '
        'Photovoltaik für Ein- und Mehrfamilienhäuser sowie Unternehmen liefert, und mit dem '
        f'Team von <a href="{WEB_SZ}" target="_blank" rel="noopener">simulacni-zkousky.cz</a>, '
        'das sich auf Netzkonformität spezialisiert. Gemeinsam decken wir ein Projekt von der '
        'ersten Studie bis zum Dauerbetrieb ab.</p>'
        + cta("Schreiben Sie uns, was Sie planen – wir sagen Ihnen, was dafür nötig ist.",
              "Unverbindliche Anfrage", "de-kontakt.html#formular"),
        eyebrow="Gruppe",
    ),
})

STRANKY.append({
    "slug": "de-leistungen.html", "nav": "sluzby", "jazyk": "de",
    "title": "Leistungen – Inbetriebnahme, Leitstellenanbindung, Mittelspannung und Service",
    "desc": "Inbetriebnahme großer PV-Anlagen, Leitstellenanbindung und Regelleistung, "
            "Mittelspannung und Trafostationen, gewerbliche PV, Konformitätsnachweise, "
            "Batteriespeicher und Service in ganz Tschechien.",
    "eyebrow": "Was wir tun", "h1": "Leistungen",
    "claim": "Gewerbliche und industrielle PV-Anlagen und Batteriespeicher in ganz Tschechien.",
    "bc_nazev": "Leistungen", "breadcrumb": [],
    "intro": "<p>Von der Inbetriebnahme über Steuerung, Mittelspannung und Trafostationen bis "
             "zum Service. Wir konzentrieren uns auf große und technisch anspruchsvolle "
             "Projekte.</p>",
    "anchors": kotvy([("Inbetriebnahme", "commissioning"), ("Leitstelle", "rizeni"),
                      ("Mittelspannung", "vn"), ("Gewerbliche PV", "fve"),
                      ("Netzkonformität", "rfg"), ("Batteriespeicher", "bess"),
                      ("Service", "servis")]),
    "body": sekce(
        "Inbetriebnahme von PV-Anlagen",
        "<p>Wir nehmen große Photovoltaikanlagen in Betrieb – von Funktionsprüfungen der "
        "Wechselrichter und Schutzeinrichtungen bis zu Prüfberichten und "
        "Übergabedokumentation.</p>"
        + seznam(["Inbetriebnahme von Wechselrichtern, Trafos und Schutzrelais",
                  "Parametrierung nach den Anschlussbedingungen des Netzbetreibers",
                  "Revision und Inbetriebnahmeprotokolle",
                  "Übergabedokumentation und Einweisung des Betreibers"]),
        eyebrow="Inbetriebnahme", kotva="commissioning",
    ) + sekce(
        "Leitstellenanbindung und Regelleistung",
        "<p>Wir implementieren Steuerungs- und Fernwirktechnik, mit der die Anlage dem "
        "Netzbetreiber, dem Markt oder beidem folgt.</p>"
        + seznam(["RTU und Steuerungssystem für Anlagen auf Mittelspannung (Weidmüller)",
                  "Anbindung der Anlage an die Leitstelle des Verteilnetzbetreibers",
                  "SCADA, Steuerung von Heizung und Ladestationen",
                  "Steuerung nach Spotpreisen",
                  "Teilnahme an Regelleistung und Aggregation"]),
        eyebrow="Steuerung", kotva="rizeni", alt=True,
    ) + sekce(
        "Mittelspannung und Trafostationen",
        "<p>Wir sanieren und erweitern Mittelspannungsteile – vom einzelnen Schaltfeld bis zur "
        "kompletten Kompaktstation.</p>"
        + seznam(["Austausch und Erweiterung von MS-Schaltfeldern",
                  "Sanierung von Trafostationen samt Messung",
                  "Ausführung nach den Anschlussbedingungen des Netzbetreibers",
                  "Abstimmung mit dem Netzbetreiber bis zur Zuschaltung"]),
        eyebrow="Mittelspannung", kotva="vn",
    ) + sekce(
        "Gewerbliche und große PV-Anlagen",
        "<p>Wir realisieren große Dach- und Freiflächenanlagen für Industrie und Investoren – "
        "einschließlich der Punkte, an denen Projekte sonst hängen bleiben: Netzanschluss, "
        "Schutzparametrierung und Konformitätsnachweis.</p>"
        + seznam(["Planung, Lieferung und Montage der Anlage",
                  "Mittelspannungsanschluss, Trafostation, Messung",
                  "Steuerungssystem und Fernüberwachung",
                  "Konformitätsnachweis und Dauerbetrieb"]),
        eyebrow="PV-Anlagen", kotva="fve", alt=True,
    ) + sekce(
        "Netzkonformität und Prüfungen",
        karty([
            (I["graf"], "Simulation",
             "<p>Modell der Anlage in DIgSILENT PowerFactory und die vom Netzbetreiber "
             "geforderten Studien.</p>"),
            (I["lupa"], "Vor-Ort-Prüfung",
             "<p>Funktionsprüfungen direkt an der fertigen Anlage mit aufgezeichneten "
             "Verläufen.</p>"),
            (I["dok"], "Dokumentation und Abstimmung",
             "<p>Wir stellen die Nachweise zusammen und führen den Schriftwechsel mit dem "
             "Netzbetreiber.</p>"),
        ], sloupce=3)
        + cta("Zur Netzkonformität gibt es eine eigene Seite mit Kategorien und häufigen Fragen.",
              "Netzkonformität im Detail", "de-netzkonformitaet.html"),
        eyebrow="RfG", kotva="rfg",
    ) + sekce(
        "Batteriespeicher",
        karty([
            (I["baterie"], "Inbetriebnahme",
             "<p>Wir nehmen den Speicher in Betrieb, inklusive Batteriemanagement und Anbindung "
             "an die Wechselrichter.</p>"),
            (I["rizeni"], "Steuerung und PV-Integration",
             "<p>Laden nach Spotpreisen, Nutzung von Überschüssen, Lastspitzenkappung.</p>"),
            (I["graf"], "Konformitätsnachweis",
             "<p>Auch ein Speicher ist eine Erzeugungsanlage – wir weisen beide Richtungen "
             "nach.</p>"),
        ], sloupce=3)
        + cta("Wie ein Speicher in Betrieb genommen, gesteuert und nachgewiesen wird.",
              "Batteriespeicher im Detail", "de-batteriespeicher.html"),
        eyebrow="Speicher", kotva="bess", alt=True,
    ) + sekce(
        "Service und Wartungsverträge",
        karty([
            (I["klic"], "Techniker in ganz Tschechien",
             "<p>Eigenes Serviceteam, keine Subunternehmer.</p>"),
            (I["hodiny"], "Reaktion im Störfall",
             "<p>Fehlersuche, Reparatur oder Austausch von Wechselrichtern, Schutzgeräten und "
             "Kommunikationseinheiten.</p>"),
            (I["smlouva"], "Wartungsverträge",
             "<p>Regelmäßige Prüfungen, Fernüberwachung und vereinbarte Reaktionszeiten.</p>"),
        ], sloupce=3),
        eyebrow="Service", kotva="servis",
    ),
})

STRANKY.append({
    "slug": "de-netzkonformitaet.html", "nav": "rfg", "jazyk": "de",
    "title": "Netzkonformität (RfG) – Simulationen und Vor-Ort-Prüfungen",
    "desc": "Konformitätsnachweis für Erzeugungsanlagen: Simulationen in DIgSILENT "
            "PowerFactory, Vor-Ort-Prüfungen, Dokumentation für den Verteilnetzbetreiber. "
            "Kategorien A1 bis D, PV-Anlagen und Batteriespeicher.",
    "eyebrow": "Konformität", "h1": "Netzkonformität und RfG-Prüfungen",
    "claim": "Simulation, Prüfung an der Anlage und der Papierkram dazu.",
    "bc_nazev": "Netzkonformität", "breadcrumb": [],
    "intro": "<p>Jede Erzeugungsanlage am tschechischen Netz muss nachweisen, dass sie die "
             "Anforderungen der europäischen Verordnung RfG und der nationalen Netzanschluss"
             "regeln erfüllt. Diesen Nachweis liefern wir – per Simulation, per Prüfung an der "
             "Anlage oder beides.</p>",
    "anchors": kotvy([("Leistungen", "co"), ("Kategorien", "kategorie"),
                      ("Drei Wege", "cesty"), ("Fragen", "faq")]),
    "body": sekce(
        "Was wir für Sie übernehmen",
        karty([
            (I["graf"], "Simulation",
             "<p>Modell der Anlage in DIgSILENT PowerFactory und die vom Netzbetreiber "
             "geforderten Studien mit Bewertung erfüllt / nicht erfüllt.</p>"),
            (I["lupa"], "Vor-Ort-Prüfung",
             "<p>Funktionsprüfungen an der fertigen Anlage mit aufgezeichneten Verläufen – in "
             "Kategorie B1 gibt es sechs Anforderungen, die anders nicht nachweisbar sind.</p>"),
            (I["dok"], "Dokumentation und Abstimmung",
             "<p>Wir bringen die Nachweise in die Form, die der Netzbetreiber erwartet, und "
             "führen den Schriftwechsel bis zur Freigabe.</p>"),
            (I["baterie"], "Batteriespeicher",
             "<p>Auch ein Speicher ist eine Erzeugungsanlage. Einstufung und Nachweisweg richten "
             "sich nach den aktuellen Regeln des jeweiligen Netzbetreibers.</p>"),
        ], sloupce=2),
        eyebrow="Umfang", kotva="co",
    ) + sekce(
        "Kategorien von Erzeugungsanlagen",
        "<p>Der Prüfumfang richtet sich nach der Kategorie der Erzeugungsanlage.</p>"
        + tabulka(
            ["Kategorie", "Leistung", "Vor-Ort-Prüfungen", "Simulationen"],
            [["A1", "0,8 kW bis 11 kW", "in der Regel nein", "in der Regel nein"],
             ["A2", "über 11 kW, unter 100 kW", "in der Regel nein", "in der Regel nein"],
             ["B1", "100 kW bis unter 1 MW", "ja", "ausgewählte Punkte"],
             ["B2", "1 MW bis unter 30 MW", "ja", "größerer Umfang"],
             ["C", "30 MW bis unter 75 MW", "ja", "größter Umfang"],
             ["D", "ab 75 MW oder Anschluss an 110 kV", "ja", "größter Umfang"]],
            poznamky=["<b>Die Kategorie steht im Netzanschlussvertrag</b> – dieser ist immer "
                      "maßgeblich.",
                      "<b>Achtung bei den Einheiten:</b> die kWp der Module sind nicht die "
                      "Größe, nach der sich die Kategorie richtet. Maßgeblich ist die "
                      "Nennwirkleistung der Erzeugungsanlage – 698 kWp Module können eine "
                      "Anlage mit P<sub>n</sub> 550 kW sein."],
        ),
        eyebrow="Regeln", kotva="kategorie", alt=True,
    ) + sekce(
        "Drei Wege, eine Anforderung nachzuweisen",
        karty([
            (I["lupa"], "Vor-Ort-Prüfung",
             "<p>Nachweis an der fertigen Anlage und Prüfprotokoll. Manche Anforderungen lassen "
             "sich anders nicht belegen.</p>"),
            (I["graf"], "Simulation",
             "<p>Modell der Anlage und Protokoll mit Bewertung. Ab Kategorie B2 ist der Umfang "
             "deutlich größer.</p>"),
            (I["stit"], "Anlagenzertifikat",
             "<p>Wird von einer Zertifizierungsstelle für ein konkretes Gerät ausgestellt. Unser "
             "Prüf- oder Simulationsprotokoll ist kein Zertifikat; es ersetzt eine Prüfung nur "
             "dort, wo das Anlagendokument es zulässt.</p>"),
        ], sloupce=3)
        + cta("Kategorien, Netzbetreiber, Fristen und Unterlagen beschreiben wir ausführlich auf "
              "unserer Spezialseite.", "Zu simulacni-zkousky.cz", WEB_SZ),
        eyebrow="Kernidee", kotva="cesty",
    ),
    "faq_nadpis": "Häufige Fragen",
    "faq": [
        ("Braucht eine Anlage unter 100 kW eine Prüfung?",
         "<p>Anlagen der Kategorien A1 und A2 werden in der Regel über Dokumentation und "
         "Anlagenzertifikat nachgewiesen, nicht über Vor-Ort-Prüfungen. Entscheidend sind der "
         "Netzanschlussvertrag und die aktuellen Regeln des Netzbetreibers.</p>"),
        ("Was brauchen Sie von uns für den Start?",
         "<p>Netzanschlussvertrag, einpoliges Schema, Datenblätter von Wechselrichtern und "
         "Schutzeinrichtungen sowie die Schutzparameter. Für Prüfungen vereinbaren wir zusätzlich "
         "einen Termin, an dem die Anlage einige Stunden frei gefahren werden kann.</p>"),
        ("Übernehmen Sie auch die Abstimmung mit dem Netzbetreiber?",
         "<p>Ja. Wir bereiten die Nachweise in der geforderten Form auf und klären Rückfragen bis "
         "zur Freigabe der Anlage.</p>"),
        ("Gilt für Batteriespeicher dasselbe?",
         "<p>Ein Speicher wird ebenfalls als Erzeugungsanlage bewertet, der Nachweis umfasst "
         "beide Leistungsrichtungen – Laden und Entladen.</p>"),
    ],
    "cross": [("Leistungen", "de-leistungen.html"), ("Batteriespeicher", "de-batteriespeicher.html"),
              ("Referenzen", "de-referenzen.html")],
})

STRANKY.append({
    "slug": "de-batteriespeicher.html", "nav": "bess", "jazyk": "de",
    "title": "Batteriespeicher – Inbetriebnahme, Steuerung und Nachweis",
    "desc": "Inbetriebnahme von Batteriespeichern, Steuerung nach Spotpreisen, Integration mit "
            "Photovoltaik, Leitstellenanbindung, Fernwirktechnik und Konformitätsnachweis.",
    "eyebrow": "Speicher", "h1": "Batteriespeicher",
    "claim": "Von der Inbetriebnahme über die Spotpreissteuerung bis zum Nachweis.",
    "bc_nazev": "Batteriespeicher", "breadcrumb": [],
    "intro": "<p>Wir nehmen Container- und Innenraumspeicher in Betrieb, binden sie an "
             "Steuerungssysteme an und weisen ihre Netzkonformität nach. Für den Betreiber zählt "
             "am Ende zweierlei: der Speicher muss Geld verdienen und innerhalb der Regeln "
             "bleiben.</p>",
    "anchors": kotvy([("Leistungen", "co"), ("Nachweis", "soulad"),
                      ("Nachrüstung", "doplneni"), ("Fragen", "faq")]),
    "body": sekce(
        "Was wir für Speicher übernehmen",
        karty([
            (I["blesk"], "Inbetriebnahme",
             "<p>Inbetriebnahme samt Batteriemanagement, Wechselrichtern und "
             "Schutzeinrichtungen.</p>"),
            (I["cena"], "Steuerung nach Spotpreisen",
             "<p>Laden, wenn Strom billig ist, entladen, wenn er teuer ist – innerhalb der "
             "Grenzen des Netzanschlussvertrags.</p>"),
            (I["panel"], "Integration mit Photovoltaik",
             "<p>Nutzung von Überschüssen, Lastspitzenkappung und Notstrom für ausgewählte "
             "Stromkreise.</p>"),
            (I["rizeni"], "Leitstelle und Fernwirktechnik",
             "<p>Anbindung an die Leitstelle des Netzbetreibers, RTU, SCADA und "
             "Fernüberwachung.</p>"),
            (I["graf"], "Konformitätsnachweis",
             "<p>Simulationen und Prüfungen für den Speicher als Erzeugungsanlage.</p>"),
            (I["klic"], "Service",
             "<p>Prüfungen, Firmware-Updates, Diagnose schwacher Zellen und Reparaturen.</p>"),
        ], sloupce=3),
        eyebrow="Umfang", kotva="co",
    ) + sekce(
        "Nachgewiesen wird in beide Richtungen",
        "<p>Ein Speicher bezieht Leistung und speist sie wieder ein – der Netzbetreiber verlangt "
        "deshalb Nachweise für das Laden und für das Entladen. Einstufung und Umfang richten sich "
        "nach den aktuellen Regeln des jeweiligen Verteilnetzbetreibers. Genau deshalb klären wir "
        "das vor der Bestellung der Technik und nicht nach der Montage.</p>"
        + callout("Achtung bei den Angaben",
                  "<p>Die nutzbare Kapazität in kWh sagt nichts über die Kategorie aus. "
                  "Maßgeblich ist die Nennwirkleistung am Anschlusspunkt.</p>"),
        eyebrow="Netzregeln", kotva="soulad", alt=True,
    ) + sekce(
        "Speicher zu einer bestehenden Anlage",
        "<p>Eine Batterie zu einer laufenden Anlage zu ergänzen ist nicht nur Technik. Je nach "
        "Größe und Netzbetreiber bedeutet es eine Änderung des Netzanschlussvertrags, neue "
        "Schutzparameter und einen neuen Konformitätsnachweis.</p>"
        + seznam(["Prüfung des bestehenden Netzanschlussvertrags und der Schutzparameter",
                  "Auslegung von Kapazität und Leistung nach dem Lastgang",
                  "Verkabelung, Inbetriebnahme und Parametrierung der Steuerung",
                  "Dokumentation für den Netzbetreiber und Dauerbetrieb"])
        + cta("Nennen Sie uns Anlagengröße und Lastgang – wir sagen Ihnen, was eine Nachrüstung "
              "erfordert.", "Unverbindliche Anfrage", "de-kontakt.html#formular"),
        eyebrow="Nachrüstung", kotva="doplneni",
    ),
    "faq_nadpis": "Häufige Fragen",
    "faq": [
        ("Lohnt sich ein Speicher ohne Photovoltaik?",
         "<p>Das kann sich rechnen, wenn Tarif und Lastgang passen – die Marge kommt dann aus der "
         "Preisspanne im Tagesverlauf. Wir rechnen es mit Ihren echten Verbrauchsdaten, nicht mit "
         "Annahmen.</p>"),
        ("Läuft der Betrieb bei einem Netzausfall weiter?",
         "<p>Nur wenn der Speicher dafür ausgelegt ist. Notstrombetrieb verlangt die passende "
         "Wechselrichter-Topologie und definierte Stromkreise – das ist eine Frage der Planung, "
         "nicht der Einstellung.</p>"),
        ("Wer haftet für die Batterien selbst?",
         "<p>Die Gewährleistung liegt beim Hersteller. Wir nehmen die Anlage in Betrieb, "
         "dokumentieren Fehler und wickeln die Reklamation mit dem Lieferanten ab.</p>"),
    ],
    "cross": [("Netzkonformität", "de-netzkonformitaet.html"), ("Leistungen", "de-leistungen.html"),
              ("Referenzen", "de-referenzen.html")],
})

DE_GALERIE = [
    ("bess", "Inbetriebnahme BESS", "Steuerung nach Spotpreisen und Integration mit PV.",
     "Offener Batteriespeicher-Container mit Batteriemodulen"),
    ("fve-strechy", "PV-Installation (Sungrow)",
     "Leitstellenanbindung, SCADA, Steuerung von Heizung und Ladestationen.",
     "Photovoltaikmodule auf dem Dach einer Industriehalle und eines Nachbargebäudes"),
    ("rtu-vn", "Leitstellenanbindung MS 35 kV",
     "RTU (Weidmüller) und Steuerungssystem für eine PV-Anlage auf Mittelspannung.",
     "RTU-Schrank mit Weidmüller-Komponenten"),
    ("stridace-sungrow", "Industrielle PV-Anlage",
     "Montage von Sungrow-Wechselrichtern und AC-Verteilern.",
     "Sungrow-Wechselrichter und AC-Verteiler an der Hallenwand"),
    ("fve-solaredge", "Gewerbliche PV (SolarEdge)",
     "PV-Anlage mit SolarEdge-Technik samt Leitstellenanbindung.",
     "SolarEdge-Wechselrichter und Verteiler auf einer Tragkonstruktion"),
    ("rozvadec-ac", "Fertigung eines AC-Verteilers",
     "AC-Verteiler zur Zusammenführung von vier Sungrow-Wechselrichtern.",
     "Offener AC-Verteiler mit Sammelschienen und Leitungsschutzschaltern"),
    ("vn-rozvadece", "Austausch von MS-Schaltfeldern",
     "Neue Mittelspannungsfelder nach den Anschlussbedingungen (3× Messung).",
     "Techniker montieren neue Mittelspannungsschaltfelder"),
    ("trafostanice", "Sanierung einer Trafostation",
     "Komplette Sanierung und Aufstellung einer 35-kV-Kompaktstation.",
     "Kran setzt eine Kompaktstation ab"),
]

STRANKY.append({
    "slug": "de-referenzen.html", "nav": "reference", "jazyk": "de",
    "title": "Referenzen – PV-Anlagen, Mittelspannung, Trafostationen und Speicher",
    "desc": "Ausgewählte Projekte von BFK Systems: Inbetriebnahme von Batteriespeichern, "
            "Leitstellenanbindung auf Mittelspannung, Sanierung von Schaltfeldern und "
            "Trafostationen, gewerbliche PV-Anlagen und Konformitätsnachweise.",
    "eyebrow": "Fotos aus Projekten", "h1": "Referenzen",
    "claim": "Eine Auswahl dessen, was wir in Betrieb genommen haben.",
    "bc_nazev": "Referenzen", "breadcrumb": [],
    "intro": "<p>Fotos aus eigenen Projekten – Inbetriebnahme, Steuerung, Mittelspannung und "
             "Speicher. Kundennamen veröffentlichen wir nicht; konkrete Referenzen nennen wir "
             "auf Anfrage gerne.</p>",
    "body": sekce("Projekte", galerie(DE_GALERIE), eyebrow="Unsere Arbeit")
    + sekce(
        "Konformitätsnachweise",
        karty([
            (I["graf"], "PV-Anlage, Kategorie D",
             "<p>Simulationen und Vor-Ort-Prüfungen für eine Anlage am 110-kV-Netz.</p>"),
            (I["lupa"], "PV-Anlage, Kategorie B1",
             "<p>Vor-Ort-Prüfung der sechs Anforderungen, die anders nicht nachweisbar sind, "
             "plus ausgewählte Simulationen.</p>"),
            (I["baterie"], "PV-Anlage mit Speicher",
             "<p>Nachweis der Anlage in beiden Leistungsrichtungen.</p>"),
        ], sloupce=3)
        + cta("Brauchen Sie eine Referenz zu einem bestimmten Projekttyp? Schreiben Sie uns, was "
              "Sie planen – wir schicken passende Beispiele.",
              "Unverbindliche Anfrage", "de-kontakt.html#formular"),
        eyebrow="Netzregeln", alt=True,
    ),
    "cross": [("Leistungen", "de-leistungen.html"), ("Netzkonformität", "de-netzkonformitaet.html"),
              ("Über uns", "de-ueber-uns.html")],
})

STRANKY.append({
    "slug": "de-ueber-uns.html", "nav": "onas", "jazyk": "de",
    "title": "Über uns – BFK Systems s.r.o., Děčín",
    "desc": "BFK Systems s.r.o. aus Děčín: ein Team mit Hintergrund in Energietechnik, "
            "Industrieautomation und Finanzen, spezialisiert auf große PV-Anlagen, "
            "Mittelspannung und Batteriespeicher.",
    "eyebrow": "Wer wir sind", "h1": "Über uns",
    "claim": "Ein Team, das die technische Seite eines PV-Projekts abdeckt.",
    "bc_nazev": "Über uns", "breadcrumb": [],
    "intro": "<p>BFK Systems s.r.o. sitzt in Děčín und arbeitet in ganz Tschechien. Wir "
             "konzentrieren uns auf Projekte, bei denen nicht die Unterkonstruktion die "
             "Herausforderung ist, sondern Netzanschluss, Steuerung und Nachweise.</p>",
    "body": sekce(
        "Unser Team",
        karty([
            (I["clovek"], "Bc. Petr Fencl",
             "<p>Inbetriebnahme, Steuerungstechnik und Netzkonformität. Leitet die technische "
             "Seite der Projekte.</p>"),
            (I["clovek"], "PhDr. Jan Böhme",
             "<p>Vertrieb und Projektleitung, Verträge und Finanzierung von Anlagen.</p>"),
            (I["clovek"], "Michal Kovář",
             "<p>Mittelspannung, Trafostationen und Führung der Montageteams.</p>"),
        ], sloupce=3),
        eyebrow="Menschen",
    ) + sekce(
        "Was uns unterscheidet",
        karty([
            (I["tovarna"], "Große und anspruchsvolle Projekte",
             "<p>Anlagen auf Mittelspannung, Container-Speicher und Trafostationen – Arbeiten, "
             "die Kenntnis der Netzregeln verlangen.</p>"),
            (I["sit"], "Energietechnik, Automation und Finanzen",
             "<p>Drei Bereiche, die ein großes Projekt gleichzeitig braucht.</p>"),
            (I["klic"], "Technik aus einer Hand",
             "<p>Inbetriebnahme, Steuerung, Mittelspannung und Nachweise aus einem Team.</p>"),
            (I["mapa"], "Service im ganzen Land",
             "<p>Eigene Techniker, Wartungsverträge und vereinbarte Reaktionszeiten.</p>"),
        ], sloupce=2),
        alt=True,
    ) + sekce(
        "Teil der Gruppe BF technology",
        karty([
            (I["graf"], "simulacni-zkousky.cz",
             "<p>Spezialisiertes Team für Netzkonformität – Simulationen, Vor-Ort-Prüfungen und "
             "Abstimmung mit Verteilnetzbetreibern.</p>", WEB_SZ),
            (I["panel"], "bftechnology.cz",
             "<p>Photovoltaik für Ein- und Mehrfamilienhäuser sowie Unternehmen, samt "
             "Batteriespeichern und Wallboxen.</p>", "https://www.bftechnology.cz/"),
        ], sloupce=2),
        eyebrow="Gruppe",
    ) + sekce(
        "Firmendaten",
        tabulka(["Angabe", "Wert"],
                [["Firma", "BFK Systems s.r.o."],
                 ["Sitz", "Obchodní 455/12, Děčín V-Rozbělesy, 405 02 Děčín"],
                 ["Firmen-ID (IČO)", "23571853"],
                 ["USt-IdNr.", "CZ23571853"],
                 ["Telefon", TEL],
                 ["E-Mail", MAIL]]),
        alt=True,
    ),
    "cross": [("Referenzen", "de-referenzen.html"), ("Leistungen", "de-leistungen.html"),
              ("Kontakt", "de-kontakt.html")],
})

DE_FORMULAR = (
    "Schreiben Sie uns, worum es geht.",
    "Je mehr wir vorab wissen, desto genauer ist unsere Antwort.",
    "Name", "Firma", "E-Mail", "Telefon", "Thema", "Nachricht",
    "Standort, Leistung der Anlage oder des Speichers, Netzbetreiber, Wunschtermin…",
    "Mit dem Absenden nehmen Sie zur Kenntnis, dass Ihre Daten zur Beantwortung der Anfrage "
    'verarbeitet werden. Wir nutzen Web3Forms als Auftragsverarbeiter. Details im '
    '<a href="de-datenschutz.html">Datenschutz</a>.',
    "Anfrage senden",
    ["Inbetriebnahme einer PV-Anlage", "Leitstellenanbindung und Regelleistung",
     "Mittelspannung oder Trafostation", "Netzkonformität (RfG)", "Batteriespeicher",
     "Service oder Wartungsvertrag", "Etwas anderes"],
)

STRANKY.append({
    "slug": "de-kontakt.html", "nav": "kontakt", "jazyk": "de",
    "title": "Kontakt – BFK Systems s.r.o.",
    "desc": "Kontakt zu BFK Systems s.r.o., Děčín: Telefon +420 776 111 100, "
            "info@bfksystems.cz, Anfrageformular für Inbetriebnahme, Mittelspannung, "
            "Batteriespeicher und Netzkonformität.",
    "eyebrow": "Kontakt", "h1": "Sprechen Sie uns an",
    "claim": "Wir antworten innerhalb von zwei Arbeitstagen.",
    "bc_nazev": "Kontakt", "breadcrumb": [], "bez_kontaktu": True,
    "intro": "<p>Am schnellsten geht es per Telefon oder E-Mail. Wenn Sie lieber schreiben, "
             "nutzen Sie das Formular – es landet im selben Postfach.</p>",
    "body": sekce(
        "Kontaktdaten",
        karty([
            (I["info"], "BFK Systems s.r.o.",
             "<p>Obchodní 455/12<br>Děčín V-Rozbělesy<br>405 02 Děčín<br>Tschechische "
             "Republik</p><p>Firmen-ID 23571853<br>USt-IdNr. CZ23571853</p>"),
            (I["klic"], "Erreichbarkeit",
             f'<p><a href="tel:+420776111100">{TEL}</a><br>'
             f'<a href="mailto:{MAIL}">{MAIL}</a></p>'
             "<p>Montag bis Freitag, 8:00–16:00 Uhr MEZ</p>"),
        ], sloupce=2),
        eyebrow="Wo Sie uns finden",
    ) + formular("de", DE_FORMULAR),
    "cross": [("Leistungen", "de-leistungen.html"), ("Netzkonformität", "de-netzkonformitaet.html"),
              ("Über uns", "de-ueber-uns.html")],
})

STRANKY.append({
    "slug": "de-datenschutz.html", "nav": "", "jazyk": "de",
    "title": "Datenschutz",
    "desc": "Wie BFK Systems s.r.o. personenbezogene Daten aus dem Anfrageformular und per "
            "E-Mail verarbeitet: Zweck, Rechtsgrundlage, Auftragsverarbeiter und Ihre Rechte.",
    "eyebrow": "Rechtliches", "h1": "Datenschutz",
    "bc_nazev": "Datenschutz", "breadcrumb": [], "prio": "0.3",
    "intro": "<p>Diese Seite erklärt, wie BFK Systems s.r.o. mit den Daten umgeht, die Sie uns "
             "senden. Verbindlich ist die tschechische Fassung; diese Übersetzung dient der "
             "Verständlichkeit.</p>",
    "body": sekce(
        "Verantwortlicher",
        "<p><b>BFK Systems s.r.o.</b>, Obchodní 455/12, Děčín V-Rozbělesy, 405 02 Děčín, "
        f'Tschechische Republik, Firmen-ID 23571853. Kontakt: <a href="mailto:{MAIL}">{MAIL}</a>, '
        f'<a href="tel:+420776111100">{TEL}</a>.</p>',
    ) + sekce(
        "Was wir verarbeiten und warum",
        tabulka(["Daten", "Zweck", "Rechtsgrundlage"],
                [["Name, Firma, E-Mail, Telefon", "Beantwortung der Anfrage und Angebot",
                  "Vorvertragliche Maßnahmen (Art. 6 Abs. 1 lit. b DSGVO)"],
                 ["Inhalt der Nachricht", "Verständnis Ihres Anliegens",
                  "Vorvertragliche Maßnahmen"],
                 ["Schriftwechsel nach der Anfrage", "Projektdokumentation",
                  "Berechtigtes Interesse (Art. 6 Abs. 1 lit. f DSGVO)"]]),
        alt=True,
    ) + sekce(
        "Auftragsverarbeiter",
        "<p>Das Anfrageformular betreibt <b>Web3Forms</b> und leitet die Nachricht an unser "
        "Postfach weiter – es handelt daher als Auftragsverarbeiter. Unsere E-Mail läuft über "
        "<b>Google Workspace</b>. Die Website liegt auf <b>GitHub Pages</b>; der Hoster führt "
        "übliche Zugriffsprotokolle. Weiter geben wir Ihre Daten nicht und nutzen sie nicht für "
        "Werbung.</p>",
    ) + sekce(
        "Speicherdauer",
        "<p>Anfragen ohne Vertragsabschluss bewahren wir bis zu zwei Jahre auf, um an ein "
        "früheres Gespräch anknüpfen zu können. Projektkorrespondenz bewahren wir für die Dauer "
        "des Vertrags und die anschließenden gesetzlichen Fristen auf.</p>",
        alt=True,
    ) + sekce(
        "Cookies",
        "<p>Die Website nutzt keine Analyse-, Werbe- oder Tracking-Cookies. In Ihrem Browser "
        "wird nichts gespeichert, was über die Anzeige der Seite hinausgeht.</p>",
    ) + sekce(
        "Ihre Rechte",
        "<p>Sie können Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung oder "
        "Datenübertragbarkeit verlangen und der Verarbeitung auf Grundlage berechtigten "
        f'Interesses widersprechen. Schreiben Sie an <a href="mailto:{MAIL}">{MAIL}</a>. Zudem '
        "steht Ihnen das Recht auf Beschwerde beim tschechischen Amt für Datenschutz (Úřad pro "
        "ochranu osobních údajů) zu.</p>",
        alt=True,
    ),
})

PAGES = STRANKY
