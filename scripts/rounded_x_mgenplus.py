# -*- coding:utf-8 -*-
## rounded mgen plus
# Ascent: 881
# Descent: 143
# Width: 1024
# EM: 1024

from os.path import basename, splitext
import fontforge
import psMat

ASCENT = 1650
DESCENT = 398
OLD_EM = 1024
EM = ASCENT + DESCENT
SCALE_DOWN = 0.94 # 1650/(881*2.0)
X_TO_CENTER = EM * (1 - SCALE_DOWN) / 2
HANKAKU_KANA = (0xFF61, 0xFF9F)
OBLIQUE_SKEW = 0.2

def modify(in_file):
    font = fontforge.open(in_file)
    _set_new_em(font)
    _set_proportion(font)
    _zenkaku_space(font)
    out_file = "tmp/modified-" + basename(in_file)
    print("Generate " + out_file)
    font.generate(out_file, flags=("opentype",))
    return 0

def oblique(in_file):
    font = fontforge.open(in_file)
    _make_oblique(font)
    name, ext = splitext(basename(in_file))
    in_style = name.split("-")[-1]
    style = "oblique" if in_style == "regular" else "bold-oblique"
    out_file = "tmp/modified-rounded-x-mgenplus-1mn-{0}{1}".format(style, ext)
    print("Generate " + out_file)
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
    font.ascent = round(float(ASCENT) / EM * OLD_EM)
    font.descent = round(float(DESCENT) / EM * OLD_EM)
    font.em = EM


def _set_proportion(font):
    scale = psMat.scale(SCALE_DOWN)
    font.selection.all()
    for glyph in list(font.selection.byGlyphs):
        is_hankaku_kana = glyph.encoding in range(*HANKAKU_KANA)
        x_to_center = X_TO_CENTER / 2 if is_hankaku_kana else X_TO_CENTER
        trans = psMat.translate(x_to_center, 0)
        mat = psMat.compose(scale, trans)
        glyph.transform(mat)
        glyph.width = round(EM / 2) if is_hankaku_kana else EM


def _zenkaku_space(font):
    font.selection.none()
    font.selection.select(0x2610)  # ☐  BALLOT BOX
    font.copy()
    font.selection.select(0x3000)  # 　 IDEOGRAPHIC SPACE
    font.paste()
    font.selection.select(0x271A)  # ✚  HEAVY GREEK CROSS
    font.copy()
    font.selection.select(0x3000)
    font.pasteInto()
    font.intersect()


def _make_oblique(font):
    mat = psMat.skew(OBLIQUE_SKEW)
    font.selection.all()
    font.transform(mat)
    font.removeOverlap()
