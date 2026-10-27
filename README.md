# www.bfksystems.cz

Firemní web **BFK Systems s.r.o.** – commissioning velkých FVE, dispečerské řízení a SVR,
rekonstrukce VN a trafostanic, komerční a velké FVE, bateriová úložiště, simulační zkoušky
(ověření souladu s RfG) a servis. Statický web bez backendu.

Nahrazuje původní jednostránkový web (Tailwind, přepínač CS/EN/DE, formulář přes
`send_email.php`). Hotové jsou všechny tři jazyky – česká, anglická a německá verze
mají po osmi stránkách a jsou provázané přes `hreflang`.

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
python3 nastroje/kontrola.py --produkce   # před nasazením: bez PLACEHOLDER, robots bez Disallow,
                                          # .htaccess, otisky podpisů, nic ze serveru, žádný CNAME
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
├── .github/workflows/
│   └── deploy-webglobe.yml  # nasazení na Webglobe přes SFTP
├── podklady/         # originály fotek (v .gitignore, až 4,5 MB na fotku)
├── LOGO.png          # ← obrázky e-mailových podpisů, neměnit ani nepřejmenovávat
├── podpis/           #   (hlídá je kontrola.py přes SHA-256)
├── index.html … 404.html   # GENEROVANÉ
├── sitemap.xml       # GENEROVANÁ
├── .htaccess         # GENEROVANÝ (404 a pořadí úvodních souborů)
└── robots.txt        # indexaci povoluje
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
| přepínač CS / EN / DE | `en*.html`, `de*.html` | plné anglické a německé verze všech osmi stránek, provázané přes `hreflang` |

Úvodní stránka má sekce Služby, Simulační zkoušky, Bateriová úložiště, Reference,
Servis a O nás. Texty o RfG jsou převzaté z ověřeného webu simulacni-zkousky.cz – když se
tam změní, je potřeba je srovnat i tady (stránky s řádkem „Aktualizováno … Zdroje“).

**Verzálky:** v tématu BFK zůstal velkými písmeny jen popisek nad H1 v hero
(`.hero-eyebrow`). Zkratky a jednotky (RfG, kV, MWp, EG.D) do něj nepatří – `kontrola.py`
to hlídá.

**Fotky referencí:** originály jsou v `podklady/reference-original`. Výřez 4 : 3 se u vysokých
fotek nastavuje ručně v `nastroje/obrazky.py` (střed výřezu), aby zůstalo vidět to podstatné.

## Nasazení

Web běží na hostingu **Webglobe** (`195.181.248.157`) pod `bfksystems.cz`
i `www.bfksystems.cz`, DNS je u Webglobe a mění ho Petr. GitHub slouží jen k vývoji.
Nasazuje GitHub Actions (`.github/workflows/deploy-webglobe.yml`) přes **SFTP na portu 222**
do `public_html/`. GitHub Pages jsou vypnuté, náhled se pouští lokálně:

```bash
python3 -m http.server 8765      # v kořeni webu
```

Spuštění: **Actions → „Nasazení na Webglobe" → Run workflow**. Přepínač `dry_run`
jen vypíše, co by se nahrálo. Workflow nejdřív spustí `kontrola.py --produkce`, ověří
otisk klíče serveru a pak nahraje soubory přes `lftp mirror -R`.

**Deploy nikdy nic nemaže** – `--delete` se do `mirror` nesmí přidat. V `public_html/`
leží vedle webu věci, které v repozitáři nejsou a být nesmí:

| Na serveru mimo repozitář | Proč |
|---|---|
| `RfG/` | portál simulací a zkoušek, v `RfG/p/…/docs/` jsou protokoly zákazníků |
| `send_email.php`, `PHPMailer/` | formulář starého webu |
| `REFERENCE/`, `index.php`, `hero2_up.jpg` | starý web, smaže Petr po nasazení |

`RfG/` ani `dotaznik/` **nikdy nedávej do repozitáře** – a to i kdyby byl soukromý.
`kontrola.py --produkce` jejich přítomnost hlásí jako chybu a nasazení neproběhne.

**Hesla nepatří do repozitáře ani do logu.** Přihlášení k SFTP je v GitHub Secrets
(`SFTP_USERNAME`, `SFTP_PASSWORD`), veřejné klíče serveru v proměnné `SFTP_KNOWN_HOSTS`.
Ověřování klíče serveru se nevypíná a na nešifrované FTP se nepřechází.

**`LOGO.png` a `podpis/*.png`** jsou obrázky e-mailových podpisů. Odkazují na ně
už odeslané zprávy, takže se nesmí přejmenovat ani změnit – `kontrola.py --produkce`
kontroluje jejich SHA-256. Poznámky k nim patří sem do README, ne do `podpis/`:
cokoli v té složce je veřejně na webu.

Formulář zatím odesílá přes Web3Forms. Nahradí ho vlastní zpracování na Webglobe
(samostatný úkol), pak je potřeba upravit i zásady zpracování osobních údajů ve všech
třech jazycích.
