# -*- coding:utf-8 -*-
import sys

from concurrent.futures import ProcessPoolExecutor, as_completed

import rounded_x_mgenplus
import fsm
import font_patcher

RMGEN = [
    ["sourceFonts/rounded-x-mgenplus-1mn-regular.ttf"],
    ["sourceFonts/rounded-x-mgenplus-1mn-bold.ttf"]
]
RMGEN_MODIFIED=[
    ["tmp/modified-rounded-x-mgenplus-1mn-regular.ttf"],
    ["tmp/modified-rounded-x-mgenplus-1mn-bold.ttf"]
]
FSM_RMGEN = [
    ["sourceFonts/FantasqueSansMono-Regular.ttf",
     "tmp/modified-rounded-x-mgenplus-1mn-regular.ttf"],
    ["sourceFonts/FantasqueSansMono-Bold.ttf",
     "tmp/modified-rounded-x-mgenplus-1mn-bold.ttf"],
]
FSM_RMGEN_PLUS = [
    ["tmp/FSMRMP-Regular.ttf", "dists"],
    ["tmp/FSMRMP-Bold.ttf", "dists"],
]

def build(version):
    print("---- modifying rounded-x-mgenplus ----")
    if concurrent_execute(rounded_x_mgenplus.modify, RMGEN):
        return 1
    # print("---- making oblique version of rounded-x-mgenplus ----")
    # if concurrent_execute(rounded_x_mgenplus.oblique, RMGEN):
    #     return 1
    print("---- generate Fantasque Sans Mono Rounded Mgen+  ----")
    args = [a + [version] for a in FSM_RMGEN]
    if concurrent_execute(fsm.generate, args):
        return 1
    print("---- adding Emoji(Symbola), Icons in terminal, ... ----")
    if concurrent_execute(font_patcher.patch, FSM_RMGEN_PLUS):
        return 1
    return 0

def concurrent_execute(func, args):
    executor = ProcessPoolExecutor()
    futures = [executor.submit(func, *a) for a in args]
    return 1 if any([r.result() for r in as_completed(futures)]) else 0
