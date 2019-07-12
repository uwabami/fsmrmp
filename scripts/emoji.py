# -*- coding:utf-8 -*-
## Twitter Color Emoji or Symbola

from os.path import basename, splitext
import fontforge
import psMat

ASCENT = 1650
DESCENT = 398
OLD_EM = 2048
EM = ASCENT + DESCENT
SCALE_DOWN = 0.98
X_TO_CENTER = EM * (1 - SCALE_DOWN) / 2
OBLIQUE_SKEW = 0.2

def modify(in_file):
    font = fontforge.open(in_file)
    _set_new_em(font)
    _set_proportion(font)
    out_file = "tmp/modified-" + basename(in_file)
    print "Generate " + out_file
    font.generate(out_file, flags=("opentype",))
    return 0

def oblique(in_file):
    font = fontforge.open(in_file)
    _make_oblique(font)
    style = "oblique"
    out_file = "tmp/modified-TwitterColorEmoji-SVGinOT-oblique.ttf"
    print "Generate " + out_file
    font.generate(out_file, flags=("opentype",))
    return 0

def _set_new_em(font):
    """
    This sets new ascent & descent and scale glyphs.  This sets new ascent &
    descent before it sets em.  When in inverse, it does not change ascent &
    descent.
    """
    font.selection.all()
    font.unlinkReferences()
    font.ascent = float(ASCENT) / EM * OLD_EM
    font.descent = float(DESCENT) / EM * OLD_EM
    font.em = EM

def _set_proportion(font):
    scale = psMat.scale(SCALE_DOWN)
    font.selection.all()
    for glyph in list(font.selection.byGlyphs):
        x_to_center = X_TO_CENTER
        trans = psMat.translate(x_to_center, 0)
        mat = psMat.compose(scale, trans)
        glyph.transform(mat)
        glyph.width = EM

def _make_oblique(font):
    mat = psMat.skew(OBLIQUE_SKEW)
    font.selection.all()
    font.transform(mat)
    font.removeOverlap()
