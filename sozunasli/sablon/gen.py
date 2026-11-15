"""Sözün Aslı — görsel üretici.
Kullanım: python3 sozunasli/sablon/gen.py <girdi.json> <çıktı_klasörü>
Her 'dosyalar' öğesi için <çıktı_klasörü>/<ad>.jpg üretir (gönderi 1080x1350, hikâye 1080x1920).
Tipler: kapak, metin, soru, story. Örnekler: sozunasli/sablon/ornek/"""
import json, sys, pathlib, subprocess

R = pathlib.Path(__file__).parent
HEAD = '<html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>{css}</style></head><body><div class="grain"></div>{body}</body></html>'

CSS_POST = """
.wrap{position:absolute;inset:90px 90px 80px 90px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;font-weight:700;font-size:26px;letter-spacing:6px;color:var(--kiremit)}
.top .no{color:var(--soluk);font-weight:500}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center}
.word{font-family:PF;font-weight:900;font-size:250px;line-height:.95;letter-spacing:-4px}
.tur{font-family:PF;font-style:italic;font-size:40px;color:var(--soluk);margin:18px 0 60px 8px}
.yol{display:flex;align-items:center;gap:28px;font-family:PF;font-size:52px}
.yol .eski{font-style:italic;color:var(--kiremit)}
.yol .ok{font-size:44px;color:var(--altin)}
.dil{font-size:24px;letter-spacing:4px;color:var(--soluk);margin-top:10px;display:flex;gap:150px}
.teaser{font-family:PF;font-size:46px;line-height:1.35;margin-top:80px;max-width:860px}
.bot{display:flex;justify-content:space-between;align-items:center;border-top:2px solid var(--murekkep);padding-top:28px;font-size:28px}
.bot b{font-weight:700}.bot .r{color:var(--kiremit);font-weight:700;letter-spacing:2px}
.etiket{font-weight:700;font-size:26px;letter-spacing:6px;color:var(--kiremit);margin-bottom:40px}
.baslik{font-family:PF;font-weight:900;font-size:96px;line-height:1.05;margin-bottom:50px}
.metin{font-family:PF;font-size:46px;line-height:1.45;max-width:880px}
.metin em{color:var(--kiremit)}
.not{margin-top:50px;padding:30px 36px;border-left:6px solid var(--altin);font-size:32px;line-height:1.5;background:rgba(201,165,92,.12)}
.dark{position:absolute;inset:0;background:var(--murekkep)}
body.koyu{color:var(--kagit)} body.koyu .bot{border-color:var(--kagit)} body.koyu .metin em{color:var(--altin)}
.secenek{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:20px}
.secenek div{border:3px solid var(--murekkep);padding:28px 30px;font-family:PF;font-weight:700;font-size:58px;display:flex;gap:22px;align-items:baseline}
.secenek span{font-family:IN;font-size:28px;color:var(--kiremit);font-weight:700}
"""

CSS_STORY = """
body{height:1920px}
.wrap{position:absolute;inset:220px 90px 260px 90px;display:flex;flex-direction:column}
.top{font-weight:700;font-size:30px;letter-spacing:6px;color:var(--kiremit)}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center}
.soru{font-family:PF;font-size:62px;line-height:1.3;margin-bottom:50px}
.word{font-family:PF;font-weight:900;font-size:220px;line-height:1;margin-bottom:70px;letter-spacing:-3px}
.sec{display:flex;flex-direction:column;gap:28px}
.sec div{border:3px solid var(--murekkep);border-radius:80px;padding:30px 50px;font-size:46px;font-weight:500;display:flex;gap:30px}
.sec div b{color:var(--kiremit)}
.sec div.dogru{background:var(--murekkep);color:var(--kagit)} .sec div.dogru b{color:var(--altin)}
.alt{font-family:PF;font-style:italic;font-size:44px;color:var(--soluk);margin-top:60px;line-height:1.4}
.bot{font-weight:700;font-size:30px}
"""

def bot(sag="KAYDIR ⟶"):
    return f'<div class="bot"><b>@sozunasli_</b><span class="r">{sag}</span></div>'

def slide_kapak(d, s):
    return f"""<div class="wrap"><div class="top"><span>SÖZÜN ASLI</span><span class="no">No. {d['no']}</span></div>
<div class="mid"><div class="word">{d['kelime']}</div><div class="tur">{d['tur']}</div>
<div class="yol"><span class="eski">{d['eski']}</span><span class="ok">⟶</span><span>{d['kelime']}</span></div>
<div class="dil"><span>{d['dil1']}</span><span>{d['dil2']}</span></div>
<div class="teaser">{d['teaser']}</div></div>{bot()}</div>"""

def slide_metin(d, s):
    notu = f'<div class="not">{s["not"]}</div>' if s.get("not") else ""
    return f"""<div class="wrap"><div class="top"><span>{s.get('etiket','')}</span><span class="no">{s['sayfa']}</span></div>
<div class="mid"><div class="baslik">{s['baslik']}</div><div class="metin">{s['metin']}</div>{notu}</div>
{bot(s.get('sag','KAYDIR ⟶'))}</div>"""

def slide_soru(d, s):
    sec = "".join(f"<div><span>{h}</span>{t}</div>" for h, t in s["secenekler"])
    return f"""<div class="wrap"><div class="top"><span>{s.get('etiket','')}</span><span class="no">{s.get('sayfa','')}</span></div>
<div class="mid"><div class="baslik">{s['baslik']}</div><div class="metin" style="margin-bottom:40px">{s.get('metin','')}</div>
<div class="secenek">{sec}</div></div>{bot(s.get('sag','YORUMA YAZ ↓'))}</div>"""

def story(d, s):
    sec = "".join(f'<div class="{"dogru" if s.get("dogru")==h else ""}"><b>{h}</b>{t}</div>' for h, t in s.get("secenekler", []))
    w = f'<div class="word">{s["kelime"]}</div>' if s.get("kelime") else ""
    return f"""<div class="wrap"><div class="top">{s['etiket']}</div><div class="mid">
<div class="soru">{s['soru']}</div>{w}<div class="sec">{sec}</div><div class="alt">{s.get('alt','')}</div></div>
<div class="bot">@sozunasli_</div></div>"""

KIND = {"kapak": slide_kapak, "metin": slide_metin, "soru": slide_soru, "story": story}

def render(spec, outdir):
    d = json.loads(pathlib.Path(spec).read_text())
    out = pathlib.Path(outdir).resolve(); out.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(d["dosyalar"], 1):
        body = KIND[s["tip"]](d, s)
        cls = ' class="koyu"' if s.get("koyu") else ""
        css = CSS_STORY if s["tip"] == "story" else CSS_POST
        html = HEAD.format(css=css, body=('<div class="dark"></div>' if s.get("koyu") else "") + body).replace("<body>", f"<body{cls}>")
        h = R / f"_tmp_{i}.html"; h.write_text(html)
        w, hh = (1080, 1920) if s["tip"] == "story" else (1080, 1350)
        png = out / f"{s['ad']}.png"
        subprocess.run(["python3", str(R / "shot.py"), str(h), str(png), str(w), str(hh)], check=True)
        subprocess.run(["python3", "-c", f"from PIL import Image;Image.open('{png}').convert('RGB').save('{png.with_suffix('.jpg')}',quality=92)"], check=True)
        png.unlink(); h.unlink()
    print("ok", out)

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
