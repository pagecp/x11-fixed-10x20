#!/usr/bin/env python3
"""Generate specimens from Christian Pagé's original 20 px Mac bitmap."""

from __future__ import annotations

import tempfile
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.DefaultTable import DefaultTable


ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / "fonts/ttf/Fixed20-Original.ttf"
OUT = ROOT / "specimens"
GREEN = "#39ff14"
MAGENTA = "#ff00ff"


def metric(metrics: object, short: str, long: str) -> int:
    return getattr(metrics, short, getattr(metrics, long, 0))


class Fixed20:
    def __init__(self) -> None:
        # Apple used bdat/bloc tags; temporarily expose their byte-identical
        # OpenType names so FontTools can decode the strike.
        source = TTFont(FONT)
        for old, new in (("bdat", "EBDT"), ("bloc", "EBLC")):
            table = DefaultTable(new)
            table.data = source[old].data
            source[new] = table
            del source[old]
        temporary = tempfile.NamedTemporaryFile(suffix=".ttf", delete=False)
        temporary.close()
        source.save(temporary.name)
        self.font = TTFont(temporary.name)
        Path(temporary.name).unlink()
        self.strike = self.font["EBDT"].strikeData[0]
        self.metrics = {}
        for subtable in self.font["EBLC"].strikes[0].indexSubTables:
            shared = getattr(subtable, "metrics", None)
            for name in subtable.names:
                item = self.strike[name]
                if shared is None:
                    item.ensureDecompiled()
                    self.metrics[name] = item.metrics
                else:
                    self.metrics[name] = shared
        self.cmap = {}
        for table in self.font["cmap"].tables:
            if table.isUnicode():
                self.cmap.update(table.cmap)

    def text(self, image: Image.Image, xy: tuple[int, int], value: str,
             colour: str) -> None:
        x, top = xy
        baseline = top + 16
        pixels = image.load()
        rgb = ImageColor.getrgb(colour)
        for character in value:
            name = self.cmap.get(ord(character))
            if name is None:
                x += 10
                continue
            glyph = self.strike[name]
            glyph.ensureDecompiled()
            metrics = self.metrics[name]
            width, height = metrics.width, metrics.height
            bearing_x = metric(metrics, "BearingX", "horiBearingX")
            bearing_y = metric(metrics, "BearingY", "horiBearingY")
            row_aligned = type(glyph).__name__.endswith("_1")
            row_bytes = (width + 7) // 8
            for row in range(height):
                for column in range(width):
                    bit = (row * row_bytes * 8 + column
                           if row_aligned else row * width + column)
                    if glyph.imageData[bit // 8] & (0x80 >> (bit % 8)):
                        px = x + bearing_x + column
                        py = baseline - bearing_y + row
                        if 0 <= px < image.width and 0 <= py < image.height:
                            pixels[px, py] = rgb
            x += metric(metrics, "Advance", "horiAdvance")


def terminal(font: Fixed20) -> None:
    image = Image.new("RGB", (700, 430), "black")
    lines = [
        "X11 Fixed 10x20 - since 1989",
        "",
        "page@kamari:~ % uname -m",
        "arm64",
        "page@kamari:~ % python3 --version",
        "Python 3.14",
        "",
        "The quick brown fox jumps over the lazy dog.",
        "0123456789  . , : ; ! ?  () [] {} <>",
        "0 O o   1 l I |   / \\   + - * = != ==",
        "",
        "def readable_since(year=1990):",
        "    return year <= 2026  # still true",
        "",
        "CPU load  #######...   GPU load  ####......",
    ]
    y = 20
    for line in lines:
        font.text(image, (20, y), line, GREEN)
        y += 24
    ImageDraw.Draw(image).line((20, 407, 680, 407), fill=MAGENTA, width=1)
    image.resize((1400, 860), Image.Resampling.NEAREST).save(
        OUT / "terminal-green-on-black.png"
    )


def punctuation(font: Fixed20) -> None:
    image = Image.new("RGB", (720, 360), "#111111")
    font.text(image, (20, 16), "THE ORIGINAL PUNCTUATION", "white")
    native = Image.new("RGB", (50, 25), "black")
    font.text(native, (0, 0), ".,", "white")
    enlarged = native.resize((400, 200), Image.Resampling.NEAREST)
    image.paste(enlarged, (150, 80))
    draw = ImageDraw.Draw(image)
    draw.rectangle((150, 80, 550, 280), outline=MAGENTA, width=2)
    font.text(image, (20, 310), "Period and comma - preserved pixel for pixel",
              GREEN)
    image.save(OUT / "period-and-comma.png")


def social_preview(font: Fixed20) -> None:
    native = Image.new("RGB", (640, 320), "black")
    font.text(native, (30, 30), "X11 FIXED 10x20", GREEN)
    font.text(native, (30, 90), "THE TERMINAL FONT THAT", MAGENTA)
    font.text(native, (30, 115), "NEVER NEEDED REPLACING.", MAGENTA)
    font.text(native, (30, 220), "1989 NCD -> 1990 X TERM -> 2026 M4 MAX", GREEN)
    ImageDraw.Draw(native).line((30, 275, 610, 275), fill=MAGENTA)
    native.resize((1280, 640), Image.Resampling.NEAREST).save(
        ROOT / "docs/assets/social-preview.png"
    )


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    fixed = Fixed20()
    terminal(fixed)
    punctuation(fixed)
    social_preview(fixed)
