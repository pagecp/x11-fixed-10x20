#!/usr/bin/env python3
"""Convert X.Org's 10x20 PCF bitmap font to a pixel-faithful outline TTF."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont


UNITS_PER_EM = 1000
PIXEL = 50  # 20 bitmap rows map exactly to one em.


def rectangle(pen: TTGlyphPen, x: int, y: int) -> None:
    x0, y0 = x * PIXEL, y * PIXEL
    x1, y1 = x0 + PIXEL, y0 + PIXEL
    pen.moveTo((x0, y0))
    pen.lineTo((x0, y1))
    pen.lineTo((x1, y1))
    pen.lineTo((x1, y0))
    pen.closePath()


def metric(metrics: object, short: str, long: str) -> int:
    return getattr(metrics, short, getattr(metrics, long, 0))


def glyph_from_bitmap(bitmap: object, metrics: object) -> object:
    width, height = metrics.width, metrics.height
    data = bitmap.imageData
    pen = TTGlyphPen(None)
    for row in range(height):
        for column in range(width):
            bit_index = row * width + column
            byte = data[bit_index // 8]
            if byte & (0x80 >> (bit_index % 8)):
                x = metric(metrics, "BearingX", "horiBearingX") + column
                y = metric(metrics, "BearingY", "horiBearingY") - row - 1
                rectangle(pen, x, y)
    return pen.glyph()


def build(source: Path, destination: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="x11-fixed-") as temporary:
        otb = Path(temporary) / "10x20.otb"
        subprocess.run(
            ["fonttosfnt", "-o", str(otb), str(source)], check=True
        )
        bitmap_font = TTFont(otb)
        glyph_order = bitmap_font.getGlyphOrder()
        strike = bitmap_font["EBDT"].strikeData[0]
        metric_map = {}
        for subtable in bitmap_font["EBLC"].strikes[0].indexSubTables:
            shared = getattr(subtable, "metrics", None)
            for name in subtable.names:
                item = strike[name]
                if shared is None:
                    item.ensureDecompiled()
                    metric_map[name] = item.metrics
                else:
                    metric_map[name] = shared
        cmap = {}
        for table in bitmap_font["cmap"].tables:
            if table.isUnicode():
                cmap.update(table.cmap)

        glyphs = {
            name: glyph_from_bitmap(strike[name], metric_map[name])
            for name in glyph_order
        }
        metrics = {}
        for name in glyph_order:
            item_metrics = metric_map[name]
            advance = metric(item_metrics, "Advance", "horiAdvance")
            bearing = metric(item_metrics, "BearingX", "horiBearingX")
            metrics[name] = (advance * PIXEL, bearing * PIXEL)

        builder = FontBuilder(UNITS_PER_EM, isTTF=True)
        builder.setupGlyphOrder(glyph_order)
        builder.setupCharacterMap(cmap)
        builder.setupGlyf(glyphs)
        builder.setupHorizontalMetrics(metrics)
        builder.setupHorizontalHeader(ascent=800, descent=-200)
        builder.setupNameTable({
            "familyName": "X11 Fixed 10x20",
            "styleName": "Regular",
            "uniqueFontIdentifier": "X11 Fixed 10x20 Regular 1.0",
            "fullName": "X11 Fixed 10x20 Regular",
            "psName": "X11Fixed10x20-Regular",
            "version": "Version 1.0",
            "description": "Pixel-faithful outline conversion of X.Org Misc Fixed 10x20",
            "vendorURL": "https://www.x.org/",
            "designer": "Network Computing Devices, Inc. (1989)",
            "licenseDescription": "NCD permissive license; see LICENSE",
        })
        builder.setupOS2(
            sTypoAscender=800,
            sTypoDescender=-200,
            sTypoLineGap=0,
            usWinAscent=800,
            usWinDescent=200,
            sxHeight=500,
            sCapHeight=650,
            xAvgCharWidth=500,
        )
        builder.setupPost(isFixedPitch=1)
        builder.setupMaxp()
        destination.parent.mkdir(parents=True, exist_ok=True)
        builder.save(destination)
        print(f"Built {destination} with {len(cmap)} encoded glyphs")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    build(args.source, args.destination)


if __name__ == "__main__":
    main()
