# From an X terminal to Apple Silicon

`10x20` is part of the classic X11 **Misc Fixed** bitmap family. Its BDF
metadata identifies Network Computing Devices, Inc. as the 1989 copyright
holder. The cell is exactly 10 pixels wide and 20 pixels high, with a
16-pixel ascent and 4-pixel descent.

Christian Pagé adopted it on a black-and-white X terminal around 1990 and
never found another terminal face as readable. When Mac OS X arrived, he
converted the font for use in Terminal with FontLab 3 in 2003 and continued
using it for shells, development and system monitoring. That conversion is a
20 px Apple bitmap SFNT named `FixedRegular`, stored inside a classic FOND
resource fork. In 2026, it was recovered intact and paired with a modern
Unicode companion for use on an Apple M4 Max.

The appeal is practical, not merely nostalgic: compact monospace rhythm,
clear operators and brackets, stable alignment and almost no ornamental
noise. Its acknowledged weak spot is the subtle distinction between period
and comma. This project preserves that original first; any revised punctuation
will be offered only as an explicitly named alternative.
