"""Sabah Gündemi kartı üretici (Gazete tasarımı, 1080x1350 JPEG).

Kullanım:
    python3 uret.py girdi.json cikti.jpg

girdi.json örneği:
{
  "tarih": "14 KASIM 2026",
  "etiket": "ÖDÜL · BOOKER 2026",
  "baslik": "Booker’ın en yaşlı kazananı: M. John Harrison",
  "ozet": "The End of Everything, felaket sonrası bir İngiltere’yi kara mizahla anlatıyor.",
  "rakamlar": [["81", "yaşında"], ["198", "sayfa"], ["13.", "kitabı"]],
  "kaynak": "Kaynak: Diken, Euronews"
}

Gereksinimler: playwright (python), /usr/bin/google-chrome, Pillow, npm.
Yazı tipleri ilk çalıştırmada npm'den /tmp/fonts altına indirilir.
"""
import json, os, subprocess, sys, tempfile

FONTS = "/tmp/fonts"
PKGS = ["@fontsource/playfair-display", "@fontsource/inter"]
HERE = os.path.dirname(os.path.abspath(__file__))


def fontlari_hazirla():
    os.makedirs(FONTS, exist_ok=True)
    for pkg in PKGS:
        ad = "fontsource-" + pkg.split("/")[1]
        if any(d.startswith(ad + "-") and os.path.isdir(os.path.join(FONTS, d)) for d in os.listdir(FONTS)):
            continue
        subprocess.run(["npm", "pack", pkg + "@5.3.0"], cwd=FONTS, check=True, capture_output=True)
        tgz = ad + "-5.3.0.tgz"
        subprocess.run(["tar", "xzf", tgz, "--one-top-level"], cwd=FONTS, check=True)


def uret(veri, cikti):
    from playwright.sync_api import sync_playwright
    from PIL import Image
    fontlari_hazirla()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.goto("file://" + os.path.join(HERE, "sablon.html"))
        pg.evaluate("document.fonts.ready")
        pg.evaluate("d => render(d)", veri)
        pg.evaluate("async () => { await document.fonts.ready; }")
        pg.wait_for_timeout(600)
        sigdi = pg.evaluate("() => fit()")
        tmp = tempfile.mktemp(suffix=".png")
        pg.locator("#a").screenshot(path=tmp)
        b.close()
    Image.open(tmp).convert("RGB").save(cikti, quality=92)
    if not sigdi:
        print("UYARI: başlık/özet alana sığmadı, metni kısaltın.", file=sys.stderr)
    return sigdi


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        veri = json.load(f)
    uret(veri, sys.argv[2])
    print("hazır:", sys.argv[2])
