"""Build the coloring book PDF from every image in pages/ (sorted by name).

Usage: python3 build_book.py   -> writes interior.pdf, cover.png, preview.png
Each page is centered on 8.5x11in at 300dpi with a blank back so markers don't bleed.
"""
import glob, os
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 2550, 3300  # 8.5x11 in at 300 dpi
MARGIN = 150
TITLE = "The Raven Moon"
SUBTITLE = "An Ornate Gothic Coloring Book"


def font(size, italic=False):
    names = ["DejaVuSerif-Italic.ttf", "DejaVuSerif.ttf"] if italic else ["DejaVuSerif.ttf"]
    for f in ("/usr/share/fonts/truetype/dejavu/" + n for n in names):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def blank():
    return Image.new("RGB", (W, H), "white")


def art_page(path):
    img = ImageOps.grayscale(Image.open(path))
    img.thumbnail((W - 2 * MARGIN, H - 2 * MARGIN), Image.LANCZOS)
    page = blank()
    page.paste(img.convert("RGB"), ((W - img.width) // 2, (H - img.height) // 2))
    return page


def centered(d, y, text, f, fill="black"):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)


def belongs_page():
    p = blank(); d = ImageDraw.Draw(p)
    d.rounded_rectangle((200, 200, W - 200, H - 200), 60, outline="black", width=10)
    d.rounded_rectangle((250, 250, W - 250, H - 250), 40, outline="black", width=4)
    centered(d, 1100, "THIS BOOK BELONGS TO", font(90))
    d.line((500, 1500, W - 500, 1500), fill="black", width=5)
    centered(d, 2000, "Embrace the Darkness", font(70, True))
    return p


def tester_page():
    p = blank(); d = ImageDraw.Draw(p)
    centered(d, 350, "COLOR TEST PAGE", font(100))
    centered(d, 520, "Try your markers & pencils here first", font(60, True))
    for r in range(7):
        for c in range(5):
            x, y = 330 + c * 390, 800 + r * 330
            d.rounded_rectangle((x, y, x + 300, y + 230), 30, outline="black", width=6)
    return p


def cover(pages):
    c = Image.new("RGB", (W, H), (11, 11, 13)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((80, 80, W - 80, H - 80), 30, outline=(184, 181, 192), width=6)
    d.rounded_rectangle((115, 115, W - 115, H - 115), 20, outline=(117, 69, 163), width=3)
    originals = sorted(glob.glob(os.path.join(HERE, "originals", "*")))
    if originals:
        art = Image.open(originals[0]).convert("RGB")
        art = art.resize((1900, round(1900 * art.height / art.width)), Image.LANCZOS)
        c.paste(art, ((W - art.width) // 2, 420))
    centered(d, 250, TITLE.upper(), font(110), fill=(231, 221, 213))
    centered(d, 2500, SUBTITLE, font(95), fill=(231, 221, 213))
    centered(d, 2700, f"{len(pages)} designs to color", font(65, True), fill=(184, 181, 192))
    return c


def main():
    pages = sorted(glob.glob(os.path.join(HERE, "pages", "*.png")) + glob.glob(os.path.join(HERE, "pages", "*.jpg")))
    interior = [belongs_page(), blank(), tester_page(), blank()]
    for p in pages:
        interior += [art_page(p), blank()]
    interior[0].save(os.path.join(HERE, "interior.pdf"), save_all=True, append_images=interior[1:], resolution=300)
    cover(pages).save(os.path.join(HERE, "cover.png"))
    # preview: cover + each design
    thumbs = [cover(pages)] + [art_page(p) for p in pages]
    tw, th = 510, 660
    cols = min(len(thumbs), 6)
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 30) + 30, rows * (th + 30) + 30), (11, 11, 13))
    for i, t in enumerate(thumbs):
        t = t.resize((tw, th), Image.LANCZOS)
        sheet.paste(t, (30 + (i % cols) * (tw + 30), 30 + (i // cols) * (th + 30)))
    sheet.save(os.path.join(HERE, "preview.png"))
    print(f"{len(pages)} designs, {len(interior)} interior pages")


if __name__ == "__main__":
    main()
