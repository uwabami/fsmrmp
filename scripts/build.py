#! /usr/bin/python
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
import rounded_x_mgenplus
import fantasque_sans_mono
import fsmrmp
import emoji
import font_patcher

RMGEN = [
    ["sourceFonts/rounded-x-mgenplus-1mn-regular.ttf"],
    ["sourceFonts/rounded-x-mgenplus-1mn-bold.ttf"]
]
FSM = [
    ["sourceFonts/FantasqueSansMono-Regular.ttf"],
    ["sourceFonts/FantasqueSansMono-Bold.ttf"],
    ["sourceFonts/FantasqueSansMono-Italic.ttf"],
    ["sourceFonts/FantasqueSansMono-BoldItalic.ttf"],
]
EMOJI = [
    ["sourceFonts/TwitterColorEmoji-SVGinOT-ThickFallback.ttf"]
]
FSM_RMGEN = [
    ["tmp/modified-FantasqueSansMono-Regular.ttf",
     "tmp/modified-rounded-x-mgenplus-1mn-regular.ttf",
     "tmp/modified-TwitterColorEmoji-SVGinOT-ThickFallback.ttf"],
    ["tmp/modified-FantasqueSansMono-Bold.ttf",
     "tmp/modified-rounded-x-mgenplus-1mn-bold.ttf",
     "tmp/modified-TwitterColorEmoji-SVGinOT-ThickFallback.ttf"],
    ["tmp/modified-FantasqueSansMono-Italic.ttf",
     "tmp/modified-rounded-x-mgenplus-1mn-oblique.ttf",
     "tmp/modified-TwitterColorEmoji-SVGinOT-ThickFallback.ttf"],
    ["tmp/modified-FantasqueSansMono-BoldItalic.ttf",
     "tmp/modified-rounded-x-mgenplus-1mn-bold-oblique.ttf",
     "tmp/modified-TwitterColorEmoji-SVGinOT-ThickFallback.ttf"],
]
FSM_RMGEN_PLUS = [
    ["tmp/FSMRMP-Regular.ttf", "dists"],
    ["tmp/FSMRMP-Bold.ttf", "dists"],
    ["tmp/FSMRMP-RegularItalic.ttf", "dists"],
    ["tmp/FSMRMP-BoldItalic.ttf", "dists"],
]

def build(version):
    print("---- modifying rounded-x-mgenplus ----")
    if concurrent_execute(rounded_x_mgenplus.modify, RMGEN):
        return 1
    print("---- modifying fantasque_sans_mono ----")
    if concurrent_execute(fantasque_sans_mono.modify, FSM):
        return 1
    print("---- making oblique version of rounded-x-mgenplus ----")
    if concurrent_execute(rounded_x_mgenplus.oblique, RMGEN):
        return 1
    print("---- modifying Twitter Color Emoji ----")
    if concurrent_execute(emoji.modify, EMOJI):
        return 1
    print("---- generate Fantasque Sans Mono Rounded Mgen+  ----")
    args = [a + [version] for a in FSM_RMGEN]
    if concurrent_execute(fsmrmp.generate, args):
        return 1
    print("---- adding Icons ----")
    if concurrent_execute(font_patcher.patch, FSM_RMGEN_PLUS):
        return 1
    return 0

def concurrent_execute(func, args):
    executor = ProcessPoolExecutor()
    futures = [executor.submit(func, *a) for a in args]
    return 1 if any([r.result() for r in as_completed(futures)]) else 0
