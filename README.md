# www.bfksystems.cz

Firemní web **BFK Systems s.r.o.** – commissioning velkých FVE, dispečerské řízení a SVR,
rekonstrukce VN a trafostanic, komerční a velké FVE, bateriová úložiště, simulační zkoušky
(ověření souladu s RfG) a servis. Statický web bez backendu.

Nahrazuje původní jednostránkový web (Tailwind, přepínač CS/EN/DE, formulář přes
`send_email.php`). Zatím **jen česky** – angličtina a němčina přijdou po schválení
českého obsahu.

Komponenty, písmo a titulní fotka jsou převzaté z webu **simulacni-zkousky.cz**
(`../simulacni-zkousky`): oranžová `#F08A00`, Roboto hostované na webu (`assets/fonts/`,
SIL Open Font License). Web nenačítá nic z cizích serverů – hlídá to `kontrola.py`.

**Vlastní téma „technický, tmavý“** (vybrané 17. 9. 2026 z návrhů A/B, snímky jsou
v `podklady/navrhy-grafiky-2026-09-17/`) odlišuje BFK od webů BF technology
a simulacni-zkousky.cz, které mají stejnou kostru. Je na konci `assets/style.css`:
grafitová hlavička, patička a záhlaví podstránek (`section.page-head`), hero rozdělené na text
a fotku se šikmým řezem, čísla jako bílé dlaždice přes hranu fotky, jemná technická mřížka,
popisky systémovým neproporcionálním písmem (`--mono`, nic se nestahuje), nadpisy bez
verzálek, ostré rohy a ikony v tmavých čtvercích. V hlavičce a patičce je proto bílé logo.

## Stránky se GENERUJÍ – needituj `.html` v kořeni

```bash
python3 nastroje/build.py                 # vygeneruje všechny .html + sitemap.xml
python3 nastroje/kontrola.py              # odkazy, kotvy, meta, JSON-LD, verzálky, zastaralé formulace
python3 nastroje/kontrola.py --externi    # navíc ověří externí odkazy (chodí na síť)
python3 nastroje/kontrola.py --produkce   # před spuštěním: bez PLACEHOLDER, robots bez Disallow, CNAME
python3 nastroje/obrazky.py               # fotky referencí a favicon (po výměně originálů)
```

**Obsah je v `nastroje/obsah.py`**, šablona, menu a patička v `nastroje/build.py`.

```
.
├── nastroje/
│   ├── obsah.py      # ← TADY se edituje obsah (1 položka STRANKY = 1 stránka)
│   ├── build.py      # šablona, menu, patička, JSON-LD, sitemap
│   ├── kontrola.py   # kontrola před publikací
│   └── obrazky.py    # náhledy a větší verze fotek referencí, favicon
├── assets/
│   ├── style.css     # styly ze simulacni-zkousky.cz, doplňky firemního webu, na konci téma BFK
│   ├── nav.js        # rozbalovací menu Služby + mobilní menu
│   ├── form.js       # odeslání poptávkového formuláře (Web3Forms)
│   ├── fonts/        # Roboto woff2
│   ├── reference/    # fotky referencí: -800 (výřez 4 : 3) a -1600, WebP + JPG
│   ├── bfk-logo*, bfk-znacka-*, favicon*
│   └── title-photo*  # titulní fotka (stejná jako na simulacni-zkousky.cz)
├── podklady/         # originály fotek (v .gitignore, až 4,5 MB na fotku)
├── index.html … 404.html   # GENEROVANÉ
├── sitemap.xml       # GENEROVANÁ
├── robots.txt        # ZATÍM ZAKAZUJE indexaci (staging)
└── CNAME.disabled    # www.bfksystems.cz – aktivovat až při spuštění
```

## Struktura webu

| Menu | Stránka | Obsah |
|---|---|---|
| Služby ▾ | `sluzby.html` | commissioning, řízení a SVR, VN a trafostanice, komerční a velké FVE, simulační zkoušky, BESS, servis (kotvy `#commissioning`, `#rizeni`, `#vn`, `#fve`, `#rfg`, `#bess`, `#servis`) |
| Simulační zkoušky | `simulacni-zkousky.html` | přehled ověření souladu s RfG, tabulka kategorií, odkazy na simulacni-zkousky.cz |
| Bateriová úložiště | `bateriova-uloziste.html` | oživení, řízení podle spotových cen, integrace s FVE, dispečerské řízení, ověření souladu, doplnění baterie |
| Reference | `reference.html` | 8 fotek z původního webu + 3 projekty ověření souladu |
| O nás | `o-nas.html` | mise, tým (texty z původního webu), co nás odlišuje, skupina BF technology, firemní údaje |
| Kontakt | `kontakt.html` | kontakty, poptávkový formulář, fakturační údaje |
| mimo menu | `index.html`, `zasady-zpracovani-osobnich-udaju.html`, `404.html` | |
| přepínač CS / EN / DE | `en.html`, `de.html` | zástupné stránky „verzi připravujeme“ s přehledem služeb a kontaktem (noindex, mimo sitemap); až budou překlady, nahradí je plné verze |

Úvodní stránka má sekce Služby, Simulační zkoušky, Bateriová úložiště, Reference,
Servis a O nás. Texty o RfG jsou převzaté z ověřeného webu simulacni-zkousky.cz – když se
tam změní, je potřeba je srovnat i tady (stránky s řádkem „Aktualizováno … Zdroje“).

**Verzálky:** v tématu BFK zůstal velkými písmeny jen popisek nad H1 v hero
(`.hero-eyebrow`). Zkratky a jednotky (RfG, kV, MWp, EG.D) do něj nepatří – `kontrola.py`
to hlídá.

**Fotky referencí:** originály jsou v `podklady/reference-original`. Výřez 4 : 3 se u vysokých
fotek nastavuje ručně v `nastroje/obrazky.py` (střed výřezu), aby zůstalo vidět to podstatné.

## Před spuštěním je potřeba dořešit

1. **Klíč poptávkového formuláře.** V `nastroje/obsah.py` (`FORMULAR`) je
   `PLACEHOLDER-DOPLNIT-KLIC-WEB3FORMS`. Ve Web3Forms založit formulář s příjemcem
   `info@bfksystems.cz` (adresu je potřeba nejdřív propojit a ověřit) a klíč doplnit.
2. **Hosting a DNS.** Současný web běží na 195.181.248.157 (nginx), DNS je u Webglobe.
   Nový web může jít na GitHub Pages stejně jako simulacni-zkousky.cz.
3. **robots.txt** přepnout podle komentáře v souboru, `CNAME.disabled` přejmenovat na `CNAME`.
4. **Zásady zpracování osobních údajů** – datum účinnosti nastavit na den spuštění.
5. **`python3 nastroje/kontrola.py --produkce` musí projít.**
