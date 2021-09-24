#! /usr/bin/python
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
import rounded_x_mgenplus
import agave
import armp
import emoji
import font_patcher

RMGEN = [
    ["sourceFonts/rounded-x-mgenplus-1mn-regular.ttf"],
    ["sourceFonts/rounded-x-mgenplus-1mn-bold.ttf"]
]
AGV = [
    ["sourceFonts/Agave-Regular.ttf"],
    ["sourceFonts/Agave-Bold.ttf"],
]
EMOJI = [
    ["sourceFonts/TwitterColorEmoji-SVGinOT-ThickFallback.ttf"]
]
AGV_RMGEN = [
    ["tmp/modified-Agave-Regular.ttf",
     "tmp/modified-rounded-x-mgenplus-1mn-regular.ttf",
     "tmp/modified-TwitterColorEmoji-SVGinOT-ThickFallback.ttf"],
    ["tmp/modified-Agave-Bold.ttf",
     "tmp/modified-rounded-x-mgenplus-1mn-bold.ttf",
     "tmp/modified-TwitterColorEmoji-SVGinOT-ThickFallback.ttf"],
]
AGV_RMGEN_PLUS = [
    ["tmp/ARMP-Regular.ttf", "dists"],
    ["tmp/ARMP-Bold.ttf", "dists"],
]

def build(version):
    print("---- modifying rounded-x-mgenplus ----")
    if concurrent_execute(rounded_x_mgenplus.modify, RMGEN):
        return 1
    print("---- modifying agave ----")
    if concurrent_execute(agave.modify, AGV):
        return 1
    print("---- modifying Twitter Color Emoji ----")
    if concurrent_execute(emoji.modify, EMOJI):
        return 1
    print("---- generate AGV Rounded Mgen+  ----")
    args = [a + [version] for a in AGV_RMGEN]
    if concurrent_execute(agvrmp.generate, args):
        return 1
    print("---- adding Icons ----")
    if concurrent_execute(font_patcher.patch, AGV_RMGEN_PLUS):
        return 1
    return 0

def concurrent_execute(func, args):
    executor = ProcessPoolExecutor()
    futures = [executor.submit(func, *a) for a in args]
    return 1 if any([r.result() for r in as_completed(futures)]) else 0
