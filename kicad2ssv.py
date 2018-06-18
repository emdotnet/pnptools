#!/usr/bin/env python
# coding=utf8

import sys

if len(sys.argv) < 3:
    print "usage: " + sys.argv[0] + " input.csv output.ssv"
    sys.exit(1)

in_file = open(sys.argv[1], 'r')
out_file = open(sys.argv[2], 'w')

for line in in_file:
    l = line.split(",")
    if len(l) == 7 and l[0][0] != '#':
        name, value, package, x, y, c, side  = l
        out_file.write(name.replace(" ", "_").replace('"', '') + " " + value.replace(" ", "_").replace('"', '') + " " + package.replace(" ", "_").replace('"', '') + " " + x + " " + y + " " + c + " " + side)


in_file.close()
out_file.close()

sys.exit(1)
