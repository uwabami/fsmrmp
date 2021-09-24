# -*- coding:utf-8 -*-
from datetime import datetime
from os.path import splitext

import fontforge

FAMILY = "ARMP"
FULLNAME = "ARMP"
FILENAME = "ARMP"
FONTFORGE = "FontForge 2.0"
ITALIC = "Italic"
ITALIC_ANGLE = -10
ASCENT = 1650
DESCENT = 398
ENCODING = "UnicodeFull"
UNDERLINE_POS = -250
UNDERLINE_HEIGHT = 100
STYLE_PROPERTY = {
    "Regular": {
        "weight": "Book",
        "os2_weight": 400,
        "panose_weight": 5,
        "panose_letterform": 2,
    },
    "Bold": {
        "weight": "Bold",
        "os2_weight": 700,
        "panose_weight": 8,
        "panose_letterform": 2,
    },
    "RegularItalic": {
        "weight": "Book",
        "os2_weight": 400,
        "panose_weight": 5,
        "panose_letterform": 9,
    },
    "BoldItalic": {
        "weight": "Bold",
        "os2_weight": 700,
        "panose_weight": 8,
        "panose_letterform": 9,
    },
}
COPYRIGHT = """Copyright (c) 2019 Youhei SASAKI <uwabami@gfd-dennou.org>
Copyright (c) 2018 JINNOUCHI Yasushi <delphinus@remora.cx>
Copyright (c) 2016-2017 Apple Inc. All rights reserved.
Copyright (c) 2015 itouhiro
Copyright (c) 2015 M+ FONTS PROJECT
SIL Open Font License Version 1.1 (http://scripts.sil.org/ofl)"""  # noqa


def generate(hankaku, zenkaku, emoji, version):
    opts = read_opts(hankaku, zenkaku, emoji, version)
    font = new_font(opts)
    _merge(font, opts)
    font.selection.all()
    # TODO: remove this to avoid sementation fault
    # font.removeOverlap()
    font.autoHint()
    font.autoInstr()
    print("Generate " + opts["out_file"])
    font.generate("tmp/" + opts["out_file"], flags=("opentype",))
    return 0


def read_opts(hankaku, zenkaku, emoji, version):
    (name, _) = splitext(hankaku)
    filename_style = name.split("-")[-1]
    if filename_style == "Italic":
        filename_style = "RegularItalic"
        style = "Regular Italic"
    else:
        style = filename_style.replace(ITALIC, " " + ITALIC)
    fontname = FILENAME + "-" + filename_style
    return {
        "hankaku": hankaku,
        "zenkaku": zenkaku,
        "emoji": emoji,
        "version": version,
        "filename_style": filename_style,
        "style": style,
        "fullname": FULLNAME + " " + style,
        "fontname": fontname,
        "out_file": fontname + ".ttf",
    }


def new_font(opts):
    prop = STYLE_PROPERTY[opts["filename_style"]]
    font = fontforge.font()
    font.ascent = ASCENT
    font.descent = DESCENT
    font.italicangle = ITALIC_ANGLE
    font.upos = UNDERLINE_POS
    font.uwidth = UNDERLINE_HEIGHT
    font.familyname = FULLNAME
    font.copyright = COPYRIGHT
    font.encoding = ENCODING
    font.fontname = opts["fontname"]
    font.fullname = opts["fullname"]
    font.version = opts["version"]
    font.appendSFNTName("English (US)", "SubFamily", opts["style"])
    font.appendSFNTName(
        "English (US)",
        "UniqueID",
        " : ".join(
            [
                FONTFORGE,
                opts["fullname"],
                opts["version"],
                datetime.today().strftime("%d-%m-%Y"),
            ]
        ),
    )
    font.weight = prop["weight"]
    font.os2_weight = prop["os2_weight"]
    font.os2_width = 5  # Medium (w/h = 1.000)
    font.os2_fstype = 4  # Printable Document (suitable for SF Mono)
    font.os2_vendor = "delp"  # me
    font.os2_family_class = 2057  # SS Typewriter Gothic
    font.os2_panose = (
        2,  # Latin: Text and Display
        11,  # Nomal Sans
        prop["panose_weight"],
        9,  # Monospaced
        2,  # None
        2,  # No Variation
        3,  # Straight Arms/Wedge
        prop["panose_letterform"],
        2,  # Standard/Trimmed
        7,  # Ducking/Large
    )
    # winascent & windescent is for setting the line height for Windows.
    font.os2_winascent = ASCENT
    font.os2_windescent = DESCENT
    # the `_add` version is for setting offsets.
    font.os2_winascent_add = 0
    font.os2_windescent_add = 0
    # hhea_ascent, hhea_descent is the macOS version for winascent &
    # windescent.
    font.hhea_ascent = ASCENT
    font.hhea_descent = -DESCENT
    font.hhea_ascent_add = 0
    font.hhea_descent_add = 0
    # typoascent, typodescent is generic version for above.
    font.os2_typoascent = ASCENT
    font.os2_typodescent = -DESCENT
    font.os2_typoascent_add = 0
    font.os2_typodescent_add = 0
    # linegap is for gap between lines.  The `hhea_` version is for macOS.
    font.os2_typolinegap = 0
    font.hhea_linegap = 0
    return font

def _merge(font, opts):
    font.mergeFonts(opts["hankaku"])
    font.mergeFonts(opts["zenkaku"])
    font.mergeFonts(opts["emoji"])
