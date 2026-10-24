#!/usr/bin/env python3
"""Obrazky pro web bfksystems.cz.

Originaly fotek referenci jsou v podklady/reference-original – stazene 17. 9. 2026
z puvodniho webu (bfksystems.cz/REFERENCE). Do gitu se nedavaji, maji az 4,5 MB.
Web dostane nahled 4 : 3 (800 x 600 px) a vetsi verzi (delsi strana 1600 px),
obe jako WebP a JPG. Favicon je ctvercova znacka z loga BFK.

Titulni fotka (assets/title-photo*) je stejna jako na simulacni-zkousky.cz,
jeji varianty se uz negeneruji – zkopirovane jsou hotove.

Spousti se rucne po vymene nektereho z originalu:

    python3 nastroje/obrazky.py
"""

from pathlib import Path

from PIL import Image, ImageOps

KOREN = Path(__file__).resolve().parent.parent
ZDROJ = KOREN / "podklady" / "reference-original"
CIL = KOREN / "assets" / "reference"
ASSETS = KOREN / "assets"

# (original, nazev na webu, svisla poloha stredu vyrezu 0–1)
# Stred vyrezu je nastaveny rucne podle fotky – u vysokych fotek by vyrez
# ze stredu uriznul to podstatne (u rozvadece pristroje, u VN lidi).
FOTKY = [
    ("1_BESS.jpg", "bess", 0.45),
    ("2_PANELY_OBRISTVI_2.jpg", "fve-strechy", 0.58),
    ("3_RTU.jpg", "rtu-vn", 0.40),
    ("4_SUNGROW_STRIDACE.jpg", "stridace-sungrow", 0.5),
    ("5_SOLAREDGE.jpg", "fve-solaredge", 0.5),
    ("6_ROZVADEC_AC.jpg", "rozvadec-ac", 0.40),
    ("7_VN.jpg", "vn-rozvadece", 0.55),
    ("8_TRAFOSTANICE2.jpg", "trafostanice", 0.5),
]


def uloz(img: Image.Image, cesta: Path, kvalita: int = 82) -> None:
    if cesta.suffix == ".webp":
        img.save(cesta, "WEBP", quality=kvalita, method=6)
    elif cesta.suffix == ".jpg":
        img.convert("RGB").save(cesta, "JPEG", quality=kvalita, optimize=True, progressive=True)
    else:
        img.save(cesta, optimize=True)
    print(f"  {cesta.relative_to(KOREN)}  {cesta.stat().st_size // 1024} kB")


def vyrez_4_3(img: Image.Image, stred_y: float) -> Image.Image:
    sirka, vyska = img.size
    if sirka / vyska > 4 / 3:          # siroka fotka – orizni boky
        nova = round(vyska * 4 / 3)
        x = (sirka - nova) // 2
        return img.crop((x, 0, x + nova, vyska))
    nova = round(sirka * 3 / 4)         # vysoka fotka – orizni nahore a dole
    y = max(0, min(vyska - nova, round(stred_y * vyska - nova / 2)))
    return img.crop((0, y, sirka, y + nova))


def reference() -> None:
    CIL.mkdir(parents=True, exist_ok=True)
    for soubor, nazev, stred in FOTKY:
        zdroj = ZDROJ / soubor
        if not zdroj.exists():
            print(f"! chybi {zdroj}")
            continue
        print(soubor)
        img = ImageOps.exif_transpose(Image.open(zdroj)).convert("RGB")
        nahled = vyrez_4_3(img, stred).resize((800, 600), Image.LANCZOS)
        uloz(nahled, CIL / f"{nazev}-800.webp", 78)
        uloz(nahled, CIL / f"{nazev}-800.jpg", 80)
        velka = img.copy()
        velka.thumbnail((1600, 1600), Image.LANCZOS)
        uloz(velka, CIL / f"{nazev}-1600.webp", 80)
        uloz(velka, CIL / f"{nazev}-1600.jpg", 82)


def favicon() -> None:
    """Ctvercova znacka z leve casti velkeho loga BFK (slunce nad panely)."""
    orig = Image.open(ASSETS / "bfk-logo.png").convert("RGBA")
    znacka = orig.crop((0, 0, orig.height, orig.height))
    znacka = znacka.crop(znacka.getbbox())
    print("favicon ze značky BFK")
    for velikost, jmeno in ((180, "favicon.png"), (32, "favicon-32.png")):
        uloz(znacka.resize((velikost, velikost), Image.LANCZOS), ASSETS / jmeno)


if __name__ == "__main__":
    reference()
    favicon()
