#!/usr/bin/env python
"""The sbrew-shell.

The sbrew-shell... wouldn't it be great if I could
use sbrew from a terminal with the same utility that
airline agents use their terminals?

FIXME - Should this be tweaked so we instead use the
sbrew methods as part of ipython or similar?
"""
from sbrew import *

prompt = {'sb': 'sbsh> ', 'py': '>>> '}
input_mode = 'sb'


def parse_input(i, lastval=None):
    """Parse terminal input."""
    try:
        c = eval(i, globals(), {'c': lastval})
    except Exception as e:
        print(str(e))
        c = lastval
    return(c)

# Everything is based around a single recipe, that starts empty
r = Recipe()
r.name = 'untitled'

print(r)
c = None
while (1):
    i = raw_input(prompt[input_mode])
    c = parse_input(i, lastval=c)
    print("c = " + str(c))
    if (i == 'q' or i == 'quit'):
        break
    elif (i in prompt.keys()):
        input_mode = i
    elif (i == 'help'):
        print("sbrewsh - sbrew shell\n q - quit\n sb - sbrew input\n py - python input\n help - this help\n")
print("sbrew go bye bye")
