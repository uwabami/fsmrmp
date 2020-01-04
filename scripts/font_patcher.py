#! /usr/bin/python

from concurrent.futures import ProcessPoolExecutor, as_completed
import errno
import os
import fontforge
import psMat

ASCENT = 1650
DESCENT = 398
OLD_EM = 1024
EM = ASCENT + DESCENT
SCALE_DOWN = 0.96
X_TO_CENTER = EM * (1 - SCALE_DOWN) / 2

PATCH_SET = [
    {
        "name": "Icon Symbol Font In Terminal Plus",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xE000,
        "sym_end": 0xEEFF,
        "src_start": None,
    },
    {
        "name": "Icon Symbol Font In Terminal Plus",
        "filename": "isfit-plus.ttf",
        "sym_start": 0xF000,
        "sym_end": 0xF8FF,
        "src_start": None,
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

def concurrent_execute(func, args):
    executor = ProcessPoolExecutor()
    futures = [executor.submit(func, *a) for a in args]
    return 1 if any([r.result() for r in as_completed(futures)]) else 0
