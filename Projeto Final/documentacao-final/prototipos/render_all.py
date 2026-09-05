#!/usr/bin/env python3
# Renderiza as telas com Chrome --screenshot e recorta o excesso com PIL.
import subprocess, tempfile, os, sys
from PIL import Image, ImageChops

BASE = os.path.dirname(os.path.abspath(__file__))
CHROME = "google-chrome-stable"
SCALE = 2
INJECT = "<style>.app{min-height:0 !important}html,body{background:#f5f7fb}</style>"

# (arquivo, saida, largura, altura_janela, recortar?)
JOBS = [
    ("T-01-login.html",      "shot-T-01.png", 1440, 950,  False),
    ("Home-professor.html",  "shot-Home.png", 1440, 2400, True),
    ("T-02-notas.html",      "shot-T-02.png", 1440, 6200, True),
    ("T-03-frequencia.html", "shot-T-03.png", 1440, 2400, True),
    ("T-04-periodos.html",   "shot-T-04.png", 1440, 6200, True),
]

def render(src, out, w, h):
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
        f"--force-device-scale-factor={SCALE}", f"--window-size={w},{h}",
        "--default-background-color=FFFFFFFF", f"--screenshot={out}",
        f"file://{src}",
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def crop(path, pad=20):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    bg = im.getpixel((4, H - 4))            # canto inferior-esq = fundo do body
    diff = ImageChops.difference(im, Image.new("RGB", im.size, bg))
    bbox = diff.getbbox()
    if not bbox:
        return im.size
    l, t, r, b = bbox
    p = pad * SCALE
    box = (max(0, l - p), max(0, t - p), min(W, r + p), min(H, b + p))
    im.crop(box).save(path)
    return im.crop(box).size

for src, out, w, h, do_crop in JOBS:
    srcpath = os.path.join(BASE, src)
    outpath = os.path.join(BASE, out)
    if do_crop:
        html = open(srcpath, encoding="utf-8").read().replace("</head>", INJECT + "</head>", 1)
        tf = tempfile.NamedTemporaryFile("w", suffix=".html", dir=BASE, delete=False, encoding="utf-8")
        tf.write(html); tf.close()
        try:
            render(tf.name, outpath, w, h)
            size = crop(outpath)
        finally:
            os.unlink(tf.name)
    else:
        render(srcpath, outpath, w, h)
        size = Image.open(outpath).size
    print(f"{out}: {size[0]}x{size[1]} px")
