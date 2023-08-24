#! /usr/bin/python3

from concurrent.futures import ProcessPoolExecutor, as_completed
import errno
import os
import fontforge
import psMat

ASCENT = 1638
DESCENT = 410
OLD_EM = 2048
EM = ASCENT + DESCENT
SCALE_DOWN = 0.96
X_TO_CENTER = EM * (1 - SCALE_DOWN) / 2

PATCH_SET = [
    {
        # Seti-UI + Custom
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE5FA,
        "sym_end": 0xE6AC,
        "src_start": 0xE5FA,
    },
    {
        # Devicons
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE700,
        "sym_end": 0xE7C5,
        "src_start": 0xE700,
    },
    {
        # Font Awesome
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xF000,
        "sym_end": 0xF2E0,
        "src_start": 0xF000,
    },
    {
        # Font Awesome Extension
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE200,
        "sym_end": 0xE2A9,
        "src_start": 0xE200,
    },
    {
        # Material Design Icon
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xF0001,
        "sym_end": 0xF1AF0,
        "src_start": 0xF0001,
    },
    {
        # Weather
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE300,
        "sym_end": 0xE3E3,
        "src_start": 0xE300,
    },
    {
        # Octicons
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xF400,
        "sym_end": 0xF532,
        "src_start": 0xF400,
    },
    {
        # Octicons
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0x2665,
        "sym_end": 0x2665,
        "src_start": 0x2665,
    },
    {
        # Octicons
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0x26A1,
        "sym_end": 0x26A1,
        "src_start": 0x26A1,
    },
    {
        # Powerline Symbols
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE0A0,
        "sym_end": 0xE0A2,
        "src_start": 0xE0A0,
    },
    {
        # Powerline Symbols
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE0B0,
        "sym_end": 0xE0B3,
        "src_start": 0xE0B0,
    },
    {
        # Powerline Extra Symbols
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE0A3,
        "sym_end": 0xE0A3,
        "src_start": 0xE0A3,
    },
    {
        # Powerline Extra Symbols
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE0B4,
        "sym_end": 0xE0C8,
        "src_start": 0xE0B4,
    },
    {
        # Powerline Extra Symbols
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE0CA,
        "sym_end": 0xE0CA,
        "src_start": 0xE0CA,
    },
    {
        # Powerline Extra Symbols
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE0CC,
        "sym_end": 0xE0D4,
        "src_start": 0xE0CC,
    },
    {
        # IEC Power Symbols
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0x23FB,
        "sym_end": 0x23FE,
        "src_start": 0x23FB,
    },
    {
        # IEC Power Symbols
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0x2B58,
        "sym_end": 0x2B58,
        "src_start": 0x2B58,
    },
    {
        # Font Logos
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xF300,
        "sym_end": 0xF32F,
        "src_start": 0xF300,
    },
    {
        # Pomicons
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE000,
        "sym_end": 0xE00A,
        "src_start": 0xE000,
    },
    {
        # Codicons
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xEA60,
        "sym_end": 0xEBEB,
        "src_start": 0xEA60,
    },
    {
        # Additional: Heavy Angle Brackets
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE276C,
        "sym_end": 0xE2771,
        "src_start": 0xE276C,
    },
    {
        # Additional: Box Drawing Char
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE2500,
        "sym_end": 0xE259F,
        "src_start": 0xE2500,
    },
    {
        # All the icons
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE0E0,
        "sym_end": 0xE11D,
        "src_start": 0xE0E0,
    },
    {
        # File Icons
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xEC48,
        "sym_end": 0xEFE9,
        "src_start": 0xEC48,
    },
    {
        # Google Material Design Icons
        "name": "isfit+",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xF2000,
        "sym_end": 0xF28BB,
        "src_start": 0xF2000
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
    scale = psMat.scale(SCALE_DOWN)
    x_to_center = X_TO_CENTER
    translate = psMat.translate(x_to_center, 0)
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
