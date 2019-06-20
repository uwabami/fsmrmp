# -*- coding=utf8 -*-

import errno
import os
import fontforge
import psMat

PATCH_SET = [
    {
        "name": "Icons In Terminal",
        "filename": "icons-in-terminal.ttf",
        "sym_start": 0xE0A0,
        "sym_end": 0xEEE0,
        "src_start": None,
    },
    {
        "name": "Symbola",
        "filename": "Symbola_Hinted.ttf",
        "sym_start": 0x1F000,
        "sym_end": 0x1FA95,
        "src_start": None,
    }
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
    print("Generated " + out_file)
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

    if info["name"] == "Symbola":
        x_ratio = 0.98
        y_ratio = 0.98
        x_diff =  0
        y_diff =  0
    elif info["name"] == "Icons In Terminal":
        x_ratio = 0.95
        y_ratio = 0.88
        x_diff = 0
        y_diff = -30
    # if info["name"] == "Seti-UI + Custom":
    #     x_ratio = 1.1
    #     y_ratio = 1.1
    #     x_diff = -100
    #     y_diff = -450
    # elif info["name"] in ["Powerline Symbols", "Powerline Extra Symbols"]:
    #     x_ratio = 0.95
    #     y_ratio = 0.88
    #     x_diff = 0
    #     y_diff = -30
    # elif info["name"] == "Font Linux":
    #     y_diff = -120
    # elif info["name"] == "Font Awesome Extension":
    #     y_diff = -400
    # elif info["name"] == "Pomicons":
    #     x_ratio = 1.2
    #     y_ratio = 1.2
    #     x_diff = -200
    #     y_diff = -300
    # elif info["name"] == "Octicons":
    #     x_ratio = 0.95
    #     y_ratio = 0.95
    #     x_diff = 30
    #     y_diff = -100
    # elif info["name"] == "Material":
    #     x_ratio = 1.1
    #     y_ratio = 1.1
    #     x_diff = -50
    #     y_diff = -250
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
