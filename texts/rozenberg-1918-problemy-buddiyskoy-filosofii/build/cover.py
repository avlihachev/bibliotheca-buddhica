from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, pathlib

W, H = 1600, 2400
PAPER = (232, 224, 205)
INK = (52, 42, 32)
CINNABAR = (140, 47, 31)
MUTED = (108, 94, 76)

F = "/System/Library/Fonts/Supplemental/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

reg, bold, ital = "Georgia.ttf", "Georgia Bold.ttf", "Georgia Italic.ttf"

img = Image.new("RGB", (W, H), PAPER)

# paper grain
random.seed(7)
noise = Image.new("L", (W // 2, H // 2))
noise.putdata([random.randint(112, 143) for _ in range(noise.width * noise.height)])
noise = noise.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.6))
img = Image.blend(img, Image.merge("RGB", (noise, noise, noise)), 0.055)

# subtle vignette so edges read as aged board
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.rectangle([0, 0, W, H], fill=90)
vd.rectangle([70, 70, W - 70, H - 70], fill=0)
vig = vig.filter(ImageFilter.GaussianBlur(70))
img = Image.composite(Image.new("RGB", (W, H), (176, 164, 142)), img, vig)

d = ImageDraw.Draw(img)


def tracked(draw, y, text, fnt, fill, track=0, center=W // 2, anchor_top=True):
    """draw text with manual letter-spacing, centered on `center`"""
    widths = [draw.textlength(c, font=fnt) for c in text]
    total = sum(widths) + track * (len(text) - 1)
    x = center - total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=fnt, fill=fill, anchor="la" if anchor_top else "ls")
        x += w + track
    return total


# double rule border
d.rectangle([88, 88, W - 88, H - 88], outline=INK, width=4)
d.rectangle([112, 112, W - 112, H - 112], outline=INK, width=1)

# --- author
tracked(d, 320, "О. О. РОЗЕНБЕРГ", font(reg, 60), INK, track=13)

d.line([(W // 2 - 190, 430), (W // 2 + 190, 430)], fill=CINNABAR, width=3)

# --- title
ty = 620
for line, size in (("ПРОБЛЕМЫ", 138), ("БУДДИЙСКОЙ", 138), ("ФИЛОСОФИИ", 138)):
    tracked(d, ty, line, font(bold, size), INK, track=6)
    ty += 186

# --- ornament: three cinnabar lozenges
oy = ty + 90
for dx in (-52, 0, 52):
    cx = W // 2 + dx
    d.polygon([(cx, oy - 13), (cx + 13, oy), (cx, oy + 13), (cx - 13, oy)],
              fill=CINNABAR if dx == 0 else INK)

# --- imprint block
iy = oy + 190
tracked(d, iy, "Издание Факультета восточных языков", font(ital, 52), MUTED)
tracked(d, iy + 78, "Петроградского университета", font(ital, 52), MUTED)

# --- foot
d.line([(W // 2 - 120, H - 560), (W // 2 + 120, H - 560)], fill=INK, width=1)
tracked(d, H - 500, "ПЕТРОГРАД", font(reg, 58), INK, track=16)
tracked(d, H - 400, "1918", font(reg, 58), CINNABAR, track=16)

tracked(d, H - 250, "с примечаниями автора", font(ital, 40), MUTED)

here = pathlib.Path(__file__).parent
img.save(here / "cover.png", "PNG")
img.save(here / "cover.jpg", "JPEG", quality=90, optimize=True, progressive=True)
print("cover.png / cover.jpg", img.size)
