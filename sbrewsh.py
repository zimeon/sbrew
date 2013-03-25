#!/usr/bin/env python
#
# The sbrew-shell... wouldn't it be great if I could
# use sbrew from a terminal with the same utility that
# airline agents use their terminals?
#
from sbrew import *

prompt = { 'sb': 'sbsh> ', 'py': '>>>' }
input_mode = 'sb'

def parse_input(i):
    return(i)

# Everything is based around a single recipe, that starts empty
r = Recipe()
r.name = 'untitled'

print r
while (1):
    i = raw_input(prompt[input_mode])
    print "Got " + i
    c = parse_input(i)
    if (i == 'q' or i=='quit'):
        break
    elif (i in prompt.keys()):
        input_mode = i
print "sbrew go bye bye"


    
