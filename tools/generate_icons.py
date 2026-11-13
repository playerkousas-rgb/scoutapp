"""Generate the nine G11 TW7 icon files from a small vector-like scene.

Pillow is a development dependency only. The output uses a fixed palette so
all nine files stay well below the 260 KB icon budget.
"""
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "static" / "icons"
OUT.mkdir(parents=True, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PALETTE = Image.Resampling.LANCZOS

SKY = "#79C9C3"
SUN = "#F4B942"
HILL_BACK = "#40916C"
HILL_FRONT = "#24533F"
CREAM = "#FFF4D6"
INK = "#18392E"
TRAIL = "#E8C47A"
RED = "#D95D4F"


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size)


def square_scene(size: int = 1024) -> Image.Image:
    im = Image.new("RGB", (size, size), SKY)
    d = ImageDraw.Draw(im)
    s = size
    # High-contrast sun remains recognisable at favicon scale.
    d.ellipse((.08*s, .07*s, .38*s, .37*s), fill=SUN)
    # Full-bleed hills and path make this a scene rather than a logo tile.
    d.polygon([(0,.53*s),(.19*s,.38*s),(.39*s,.54*s),(.62*s,.32*s),(.83*s,.50*s),(s,.37*s),(s,s),(0,s)], fill=HILL_BACK)
    d.polygon([(0,.68*s),(.18*s,.55*s),(.39*s,.68*s),(.61*s,.51*s),(.84*s,.67*s),(s,.56*s),(s,s),(0,s)], fill=HILL_FRONT)
    d.polygon([(.42*s,s),(.48*s,.66*s),(.54*s,.66*s),(.68*s,s)], fill=TRAIL)
    # Neutral temporary TW7 mark, wholly inside the central 66% maskable zone.
    d.ellipse((.225*s,.225*s,.775*s,.775*s), fill=CREAM, outline=INK, width=max(4,round(.022*s)))
    # Four simple compass points reinforce the Scout/outdoor context.
    cx=cy=.5*s
    for pts in [
        [(cx,.255*s),(.46*s,.38*s),(.54*s,.38*s)],
        [(cx,.745*s),(.46*s,.62*s),(.54*s,.62*s)],
        [(.255*s,cy),(.38*s,.46*s),(.38*s,.54*s)],
        [(.745*s,cy),(.62*s,.46*s),(.62*s,.54*s)],
    ]:
        d.polygon(pts, fill=RED)
    label="TW7"
    f=font(round(.19*s))
    box=d.textbbox((0,0),label,font=f)
    d.text(((s-(box[2]-box[0]))/2,(s-(box[3]-box[1]))/2-box[1]),label,font=f,fill=INK)
    return im


def quantized(im: Image.Image, colors: int) -> Image.Image:
    return im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)


def save_png(im: Image.Image, path: Path, colors: int = 32) -> None:
    quantized(im.convert("RGB"), colors).save(path, optimize=True)


def tiny_icon() -> Image.Image:
    """Hand-drawn 16px scene: sky, sun, central tent/mark and ground."""
    im=Image.new("P",(16,16),0)
    palette=[]
    for color in (SKY,HILL_FRONT,SUN,CREAM,INK,RED,TRAIL,HILL_BACK):
        palette.extend(tuple(int(color[i:i+2],16) for i in (1,3,5)))
    palette.extend([0]*(768-len(palette)))
    im.putpalette(palette)
    d=ImageDraw.Draw(im)
    d.rectangle((0,10,15,15),fill=1)
    d.ellipse((1,1,6,6),fill=2)
    d.polygon([(8,3),(14,13),(2,13)],fill=3)
    d.polygon([(8,7),(11,13),(5,13)],fill=4)
    d.rectangle((7,7,8,9),fill=5)
    return im


def og_scene() -> Image.Image:
    base=square_scene(1260)
    # Crop to landscape, then add a quiet text panel over the right side.
    im=base.crop((0,315,1260,945)).resize((1200,630),PALETTE)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((560,105,1145,525),radius=34,fill=CREAM,outline=INK,width=8)
    d.text((620,165),"TW7",font=font(120),fill=INK)
    d.text((620,320),"7th Tsuen Wan",font=font(42),fill=INK)
    d.text((620,377),"Scout Group",font=font(42),fill=INK)
    d.rectangle((620,455,1060,469),fill=RED)
    return im


def main() -> None:
    master=square_scene()
    tiny=tiny_icon()
    tiny.save(OUT/"favicon-16.png",optimize=True)
    files={
        "favicon-32.png":(32,24),
        "apple-touch-icon.png":(180,32),
        "icon-192.png":(192,32),
        "icon-512.png":(512,48),
        "icon-maskable-192.png":(192,32),
        "icon-maskable-512.png":(512,48),
    }
    generated={}
    for name,(size,colors) in files.items():
        image=master.resize((size,size),PALETTE)
        save_png(image,OUT/name,colors)
        generated[size]=image
    # ICO contains the hand-drawn 16px layer plus 32px and 48px scene layers.
    convert=shutil.which("convert") or shutil.which("magick")
    if convert:
        with tempfile.TemporaryDirectory() as tmp:
            p16=Path(tmp)/"16.png"; p32=Path(tmp)/"32.png"; p48=Path(tmp)/"48.png"
            tiny.save(p16,optimize=True)
            save_png(master.resize((32,32),PALETTE),p32,24)
            save_png(master.resize((48,48),PALETTE),p48,24)
            subprocess.run([convert,str(p16),str(p32),str(p48),str(OUT/"favicon.ico")],check=True)
    else:
        # Portable fallback still produces all required ICO sizes. Release
        # generation uses ImageMagick so its 16px layer is the hand-drawn one.
        master.resize((48,48),PALETTE).save(OUT/"favicon.ico",format="ICO",sizes=[(16,16),(32,32),(48,48)])
    save_png(og_scene(),OUT/"og-image.png",64)
    total=sum(p.stat().st_size for p in OUT.iterdir() if p.is_file())
    print(f"generated 9 files: {total} bytes")


if __name__ == "__main__":
    main()
