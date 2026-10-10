# Gera o ícone da app (Bíblia Memória) para Android. Corre no GitHub Actions depois de "cap add android".
# Uso: python3 make-icons.py            -> escreve em android/app/src/main/res
#      python3 make-icons.py --preview  -> escreve pré-visualizações em ./icons
import os, sys
from PIL import Image, ImageDraw

GREEN = (31, 90, 70, 255)
GREEN_DARK = (20, 62, 48, 255)
GOLD = (222, 184, 78, 255)
CREAM = (248, 243, 228, 255)
INK = (150, 160, 150, 255)
SS = 4  # supersampling

def art(size):
    """Livro aberto com cruz, desenhado dentro da zona segura (cerca de 60% do centro)."""
    S = size * SS
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    P = lambda x, y: (x * S, y * S)
    # capa dourada (por baixo)
    d.polygon([P(.24, .40), P(.50, .46), P(.50, .79), P(.24, .73)], fill=GOLD)
    d.polygon([P(.76, .40), P(.50, .46), P(.50, .79), P(.76, .73)], fill=GOLD)
    # páginas
    d.polygon([P(.265, .385), P(.495, .445), P(.495, .765), P(.265, .705)], fill=CREAM)
    d.polygon([P(.735, .385), P(.505, .445), P(.505, .765), P(.735, .705)], fill=CREAM)
    # linhas de texto
    for k in range(4):
        y = .475 + k * .052
        d.line([P(.31, y - .018), P(.46, y + .012)], fill=INK, width=int(S * .008))
        d.line([P(.69, y - .018), P(.54, y + .012)], fill=INK, width=int(S * .008))
    # cruz
    r = S * .012
    d.rounded_rectangle([P(.478, .12), P(.522, .38)], radius=r, fill=GOLD)
    d.rounded_rectangle([P(.41, .19), P(.59, .233)], radius=r, fill=GOLD)
    return im.resize((size, size), Image.LANCZOS)

def full(size, shape):
    """Ícone clássico (quadrado arredondado ou círculo)."""
    S = size * SS
    bg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(bg)
    if shape == "round":
        d.ellipse([0, 0, S - 1, S - 1], fill=GREEN)
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * .22), fill=GREEN)
    bg = bg.resize((size, size), Image.LANCZOS)
    bg.alpha_composite(art(size))
    return bg

def foreground(size):
    """Camada de frente do ícone adaptativo (fundo transparente)."""
    return art(size)

DENS = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}

def main():
    if "--preview" in sys.argv:
        os.makedirs("icons", exist_ok=True)
        full(512, "square").save("icons/icon-512.png")
        full(512, "round").save("icons/icon-round-512.png")
        foreground(432).save("icons/icon-foreground-432.png")
        full(64, "square").save("icons/favicon-64.png")
        return
    res = "android/app/src/main/res"
    if not os.path.isdir(res):
        sys.exit("Pasta android/app/src/main/res não encontrada. Corre 'npx cap add android' primeiro.")
    for name, px in DENS.items():
        folder = os.path.join(res, "mipmap-" + name)
        os.makedirs(folder, exist_ok=True)
        full(px, "square").save(os.path.join(folder, "ic_launcher.png"))
        full(px, "round").save(os.path.join(folder, "ic_launcher_round.png"))
        foreground(px * 108 // 48).save(os.path.join(folder, "ic_launcher_foreground.png"))
    os.makedirs(os.path.join(res, "values"), exist_ok=True)
    with open(os.path.join(res, "values", "ic_launcher_background.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#1F5A46</color>\n</resources>\n')
    print("Ícones gerados.")

main()
