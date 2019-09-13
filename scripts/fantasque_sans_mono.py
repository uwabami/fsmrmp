# -*- coding:utf-8 -*-
## Fantasque Sans Mono
# Ascent: 1650
# Descent: 398
# Width: 1060
# EM: 2048

from os.path import basename, splitext
import fontforge
import psMat

OLD_WIDTH = 1060
WIDTH = 1024
SCALE_DOWN = float(WIDTH) / OLD_WIDTH

def modify(in_file):
    name, ext = splitext(in_file)
    font = fontforge.open(in_file)
    _set_proportion(font)
    font.removeOverlap()
    out_file = "tmp/modified-" + basename(in_file)
    print("Generate " + out_file)
    font.generate(out_file, flags=("opentype",))
    return 0


def _set_proportion(font):
    mat = psMat.scale(SCALE_DOWN)
    font.selection.all()
    for glyph in list(font.selection.byGlyphs):
        glyph.transform(mat)
        glyph.width = WIDTH
