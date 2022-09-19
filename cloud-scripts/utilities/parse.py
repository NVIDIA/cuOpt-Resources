#!/usr/bin/python

# Reds a JSON dictionary and writes out in "key=value" format
# that can be sourced by bash. This is only for a dicitonary of strings!

import json
import sys

with open(sys.argv[1]) as f:
    values=json.load(f)

with open(sys.argv[2], "w") as f:
    for key, value in values.items():
        f.write("%s=%s\n" % (key, value))
    
