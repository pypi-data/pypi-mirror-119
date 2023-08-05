# This file is in the Public Domain.

import time

from .obj import Cfg, keys, fmt
from .run import elapsed, listfiles, find, fntime

def fnd(event):
    if not event.args:
        fls = listfiles(Cfg.wd)
        if fls:
            event.reply(",".join(sorted({x.split(".")[-1].lower() for x in fls})))
        return
    otype = event.args[0]
    nr = -1
    args = list(event.gets)
    try:
        args.extend(event.args[1:])
    except IndexError:
        pass
    got = False
    for fn, o in find(otype, event.gets, event.index, event.timed):
        nr += 1
        txt = "%s %s" % (str(nr), fmt(o, args or keys(o), skip=keys(event.skip)))
        if "t" in event.opts:
            txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
        got = True
        event.reply(txt)
    if not got:
        event.reply("no result")
