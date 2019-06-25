#! /usr/bin/python
# -*- coding=utf8 -*-

from concurrent.futures import ProcessPoolExecutor, as_completed
import errno
import os
import fontforge
import psMat

FSM_RMGEN_PLUS = [
    ["tmp/FSMRMP-Regular.ttf", "dists"],
    ["tmp/FSMRMP-Bold.ttf", "dists"],
    ["tmp/FSMRMP-RegularItalic.ttf", "dists"],
    ["tmp/FSMRMP-BoldItalic.ttf", "dists"],
]

PATCH_SET = [
    ## Power Symbols: 0x23FB - 0x23FE, 3 glyph
    {
        "name": "Power Symbols",
        "filename": "Unicode_IEC_symbol_font.otf",
        # Heavy Circle (aka Power Off)
        "sym_start": 0x23FB,
        "sym_end": 0x23FE,
        "src_start": None,
    },
    ## Power Symbols: 0x2B58 - 0x2B58, 3 glyph
    {
        "name": "Power Symbols",
        "filename": "Unicode_IEC_symbol_font.otf",
        "sym_start": 0x2B58,
        "sym_end": 0x2B58,
        "src_start": None,
    },
    ## Pomicon: 0xE000 - 0xE00A, 12 glyph
    # {
    #     "name": "Pomicons",
    #     "filename": "Pomicons.otf",
    #     "sym_start": 0xE000,
    #     "sym_end": 0xE00A,
    #     "src_start": None,
    # },
    ## Powerline Symbols: 0xE0A0 - 0xE0A2, 3 glyph
    {
        "name": "Powerline Symbols",
        "filename": "PowerlineSymbols.otf",
        "sym_start": 0xE0A0,
        "sym_end": 0xE0A2,
        "src_start": None,
    },
    ## Powerline Extra Symbols: 0xE0A3 - 0xE0A3, 1 glyph
    {
        "name": "Powerline Extra Symbols",
        "filename": "PowerlineExtraSymbols.otf",
        "sym_start": 0xE0A3,
        "sym_end": 0xE0A3,
        "src_start": None,
    },
    ## Powerline Symbols: 0xE0B0 - 0xE0B3, 3 glyph
    {
        "name": "Powerline Symbols",
        "filename": "PowerlineSymbols.otf",
        "sym_start": 0xE0B0,
        "sym_end": 0xE0B3,
        "src_start": None,
    },
    ## Powerline Extra Symbols: 0xE0B4 - 0xE0C8, 20 glyph
    {
        "name": "Powerline Extra Symbols",
        "filename": "PowerlineExtraSymbols.otf",
        "sym_start": 0xE0B4,
        "sym_end": 0xE0C8,
        "src_start": None,
    },
    ## Powerline Extra Symbols: 0xE0CA - 0xE0CA, 1 glyph
    {
        "name": "Powerline Extra Symobls",
        "filename": "PowerlineExtraSymbols.otf",
        "sym_start": 0xE0CA,
        "sym_end": 0xE0CA,
        "src_start": None,
    },
    ## Powerline Extra Symbols: 0xE0CC - 0xE0D4, 8 glyph
    {
        "name": "Powerline Extra Symobls",
        "filename": "PowerlineExtraSymbols.otf",
        "sym_start": 0xE0CC,
        "sym_end": 0xE0D4,
        "src_start": None,
    },
    ## Font Awesome Extensions: 0xE200 - 0xE2A9, 169 glyph
    {
        "name": "Font Awesome Extension",
        "filename": "font-awesome-extension.ttf",
        "sym_start": 0xE000,
        "sym_end": 0xE0A9,
        "src_start": 0xE200,
    },
    ## Weather Icons: 0xE300 - 0xE3EB, 235 glpyh
    {
        "name": "Weather Icons",
        "filename": "weathericons-regular-webfont.ttf",
        "sym_start": 0xF000,
        "sym_end": 0xF0EB,
        "src_start": 0xE300,
    },
    ## All the icon's original: 0xE400 - 0xE436, 54 glyph
    {
        "name": "All the Icons",
        "filename": "all-the-icons.ttf",
        "sym_start": 0xE903,
        "sym_end": 0xE941,
        "src_start": 0xE400,
    },
    ## Nerd original: 0xE5FA - 0xE52E, 52 glpyh
    {
        "name": "Seti-UI + Custom",
        "filename": "nerd-original-sources.otf",
        "sym_start": 0xE4FA,
        "sym_end": 0xE52E,
        "src_start": 0xE5FA,
    },
    ## Devicons: 0xE700 - 0xE7C5, 197 glyph
    {
        "name": "Devicons",
        "filename": "devicons.ttf",
        "sym_start": 0xE600,
        "sym_end": 0xE6C5,
        "src_start": 0xE700,
    },
    ## Material Design: 0xE800 - 0xEFFF, 2047 glyph
    {
        "name": "Material",
        "filename": "materialdesignicons-webfont.ttf",
        "sym_start": 0xF001,
        "sym_end": 0xF800,
        "src_start": 0xE800,
    },
    ## Font Awesome: 0xF000 - 0xF2E0, 736 glyph
    {
        "name": "Font Awesome",
        "filename": "FontAwesome.otf",
        "sym_start": 0xF000,
        "sym_end": 0xF2E0,
        "src_start": None,
    },
    ##  Font Logo: 0xF300 - 0xF31C, 28 glpyh
    {
        "name": "Font Logo",
        "filename": "font-logos.ttf",
        "sym_start": 0xF100,
        "sym_end": 0xF11C,
        "src_start": 0xF300,
    },
    ## Octicons: 0xF400 - 0xF4E8, 232 glpyh
    {
        "name": "Octicons",
        "filename": "octicons.ttf",
        "sym_start": 0xF000,
        "sym_end": 0xF0E8,
        "src_start": 0xF400,
    },
    ## Octicons: 0xF4E9 - 0xF4ED, 4 glpyh
    {
        "name": "Octicons",
        "filename": "octicons.ttf",
        "sym_start": 0xF101,
        "sym_end": 0xF105,
        "src_start": 0xF4E9,
    },
    ## Material Design: 0xF500 - 0xF546, 71 glyph
    {
        "name": "Material",
        "filename": "materialdesignicons-webfont.ttf",
        "sym_start": 0xF801,
        "sym_end": 0xF847,
        "src_start": 0xF500,
    },
    ## Octicons, misc.
    # 0x2665, BLACK HEART SUIT
    {
        "name": "Octicons",
        "filename": "octicons.ttf",
        "sym_start": 0x2665,
        "sym_end": 0x2665,
        "src_start": None,
    },
    # 0x26A1, High Voltage
    {
        "name": "Octicons",
        "filename": "octicons.ttf",
        "sym_start": 0x26A1,
        "sym_end": 0x26A1,
        "src_start": None,
    },
    ## Desktop: 0xF4A9
    {
        "name": "Octicons",
        "filename": "octicons.ttf",
        "sym_start": 0xF27C,
        "sym_end": 0xF27C,
        "src_start": 0xF4A9,
    },
]

def patch(in_file, out_dir):
    font = fontforge.open(in_file)
    _patch(font)
    try:
        os.makedirs(out_dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    out_file = os.path.join(out_dir, os.path.basename(in_file))
    print "Generated " + out_file
    font.generate(out_file)
    return 0


def _patch(font):
    # Prevent opening and closing the fontforge font. Makes things faster when
    # patching multiple ranges using the same symbol font.
    previous_symbol_filename = ""
    symfont = None

    for info in PATCH_SET:
        if previous_symbol_filename != info["filename"]:
            # We have a new symbol font, so close the previous one if it exists
            if symfont:
                symfont.close()
                symfont = None
            symfont = fontforge.open("sourceFonts/" + info["filename"])
            # Match the symbol font size to the source font size
            symfont.em = font.em
            previous_symbol_filename = info["filename"]

        _copy_glyphs(font, symfont, info)
    if symfont:
        symfont.close()

def _transform_sym(symfont, info):

    x_ratio = 1.0
    y_ratio = 1.0
    x_diff = 0
    y_diff = 0

    if info["name"] == "Seti-UI + Custom":
        x_ratio = 1.1
        y_ratio = 1.1
        x_diff = -100
        y_diff = -250

    elif info["name"] == "Devicons":
        x_ratio = 1.05
        y_ratio = 1.05
        x_diff = -100
        y_diff = -250

    elif info["name"] in ["Powerline Symbols", "Powerline Extra Symbols"]:
        x_ratio = 0.95
        y_ratio = 0.88
        x_diff = 0
        y_diff = -30

    elif info["name"] == "Font Logo":
        y_diff = -120

    elif info["name"] == "Font Awesome Extension":
        y_diff = -400

    elif info["name"] == "Pomicons":
        x_ratio = 1.2
        y_ratio = 1.2
        x_diff = -200
        y_diff = -300

    elif info["name"] == "Octicons":
        x_ratio = 0.95
        y_ratio = 0.95
        x_diff = 30
        y_diff = -100

    elif info["name"] == "Material":
        x_ratio = 1.1
        y_ratio = 1.1
        x_diff = -50
        y_diff = -250

    elif info["name"] == "All the Icons":
        x_ratio = 1.2
        y_ratio = 1.2
        x_diff = 0
        y_diff = 0

    # elif info["name"] == "Noto Emoji":
    #     x_ratio = 0.85
    #     y_ratio = 0.85
    #     x_diff = -40
    #     y_diff = 0

    scale = psMat.scale(x_ratio, y_ratio)
    translate = psMat.translate(x_diff, y_diff)
    transform = psMat.compose(scale, translate)
    symfont.transform(transform)


def _copy_glyphs(font, symfont, info):
    for encoding in range(info["sym_start"], info["sym_end"] + 1):
        src_encoding = encoding
        if info["src_start"]:
            src_encoding += info["src_start"] - info["sym_start"]
        symfont.selection.select(encoding)
        _transform_sym(symfont, info)
        symfont.copy()
        font.selection.select(src_encoding)
        font.paste()
    return

def concurrent_execute(func, args):
    executor = ProcessPoolExecutor()
    futures = [executor.submit(func, *a) for a in args]
    return 1 if any([r.result() for r in as_completed(futures)]) else 0

def build():
    print "---- adding Emoji, Icons, Symols ... ----"
    if concurrent_execute(patch, FSM_RMGEN_PLUS):
        return 1
    return 0
