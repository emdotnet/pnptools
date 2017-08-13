#!/usr/bin/env python
# coding=utf8

import sys
import csv

if len(sys.argv) < 3:
    print "usage: " + sys.argv[0] + " input.csv output.ssv"
    sys.exit(1)

in_file = open(sys.argv[1], 'r')
out_file = open(sys.argv[2], 'w')

csv = csv.DictReader(in_file)
#{'Comment': '1M', 'Layer': 'TopLayer', 'Description': 'Resistor 1', 'Footprint Description': 'Chip Resistor, Body 1.6x0.8mm, IPC Medium Density', 'Designator': 'R33', 'ComponentKind': 'Standard', 'Ref-X(mm)': '291.604', 'Height(mm)': '0.600', 'Ref-Y(mm)': '79.777', 'Variation': 'Fitted', 'Pad-X(mm)': '291.604', 'Footprint': 'R-0603-M', 'Center-Y(mm)': '79.777', 'Pad-Y(mm)': '80.577', 'Rotation': '270', 'Center-X(mm)': '291.604'}
for row in csv:
   name, value, package, x, y, c, side = [row['Designator'], row['Comment'], row['Footprint'], row['Center-X(mm)'], row['Center-Y(mm)'], row['Rotation'], row['Layer']]
   out_file.write(name.replace(" ", "_") + " " + value.replace(" ", "_") + " " + package.replace(" ", "_") + " " + x + " " + y + " " + c + " " + side + "\n")

in_file.close()
out_file.close()

sys.exit(1)
