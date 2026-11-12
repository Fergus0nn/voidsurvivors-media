"""Vyřízne Kaie (6 výrazů) z kai_vyrazy.png a logo z titulní obrazovky -> PNG s průhledností."""
import sys
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

src, title, out = sys.argv[1], sys.argv[2], sys.argv[3]

im = np.asarray(Image.open(src).convert("RGB")).astype(np.int32)
H, W, _ = im.shape
# pozadí je svislý přechod -> barva pozadí pro každý řádek z levého okraje
row_bg = np.median(im[:, 0:6, :], axis=1)            # (H,3)
dist = np.sqrt(((im - row_bg[:, None, :]) ** 2).sum(axis=2))
bglike = dist < 16

# flood fill z horního, levého a pravého okraje přes pixely podobné pozadí
bg = np.zeros((H, W), bool)
q = deque()
for x in range(W):
    if bglike[0, x]:
        bg[0, x] = True; q.append((0, x))
for y in range(H):
    for x in (0, W - 1):
        if bglike[y, x] and not bg[y, x]:
            bg[y, x] = True; q.append((y, x))
while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < H and 0 <= nx < W and not bg[ny, nx] and bglike[ny, nx]:
            bg[ny, nx] = True; q.append((ny, nx))

alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8))
alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
rgba = Image.open(src).convert("RGBA")
rgba.putalpha(alpha)
for i in range(6):
    tile = rgba.crop((i * 250, 380, i * 250 + 250, 700))
    tile = tile.crop(tile.getbbox())
    tile.save(f"{out}/kai_{i}.png")
    print("kai", i, tile.size)

# logo: jasné na tmavém -> alfa podle jasu
t = Image.open(title).convert("RGB").crop((58, 50, 402, 182))
a = np.asarray(t).astype(np.float32)
lum = a.max(axis=2)
al = np.clip((lum - 40) / 90.0, 0, 1) * 255
logo = t.convert("RGBA")
logo.putalpha(Image.fromarray(al.astype(np.uint8)))
logo = logo.resize((logo.width * 3, logo.height * 3), Image.LANCZOS)
logo.save(f"{out}/logo.png")
print("logo", logo.size)
