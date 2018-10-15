#!/usr/bin/env python
# coding=utf8

import sys

package_remap = {
    "C_0603": "*C0603",
    "C_0805": "*C0805",
    "C_1808": "*C1808",
    "C_1206": "*C1206",
    "R_0603": "*R0603",
    "R_0805": "*R0805",
    "R_1206": "*R1206",
    "R_2512": "*R2512",
    "LQFP-48_7x": "*QFP48",
    "LQFP-100_1": "*QFP100",
    "SOT-23": "*SOT23",
    "SOT-223": "*SOT223",
    "SOT-23-6": "*SOT23",
    "SOD-123": "*D1406",
    "Crystal_SM": "*C6032",
    "SOIC-8-N": "*SOP8P",
    "USB_Micro-": "*MUSB",
    "SMA_Standa": "*SMA",
    "D_SMA": "*SMA",    
    "LED-0805": "*C0805",
    "LED-0805-S": "*C0805",
    "SOIC-7": "*SOP8P",
    "NPI31W": "*NPI31W",
    "SMD_INDUCT": "*IND3225",
    "AC": "",
    "Package": "",
    "SOLDER_JUM": "",
    "ESD": "",
    "Symbol_OSH": "",
    "Symbol_Hig": "",
    "Symbol_Dan": "",
    "Measuremen": "",
    "Fiducial_1": "",
#     "Fiducial": "",#GPN
#     "18650Holde": "",
#     "LDR-5mm": "",
#     "SWITCH_THT": "",
#     "IR_LED": "",#ir
#     "TL1838": "",#ir
#     "HDR1X4H_wo": "",
#     "R-0603-M": "R0603",
#     "C-0603-M": "C0603",
#     "C-0603-H": "C0603",
#     "C-0805-M": "C0805",
#     "ESP8266_AN": "",
#     "SOT23-5": "SOT23",
#     "SOT23-6": "SOT23",
#     "SOT23-3": "SOT23",
#     "AO-SOT23-3": "SOT23",
#     "LCD": "",
#     "R-1206-M": "R1206",
# #    "SLAB-QFN-2": "",#TODO: kommt dienstag
#     "VIBRATOR_S": "",
#     "SOT89-150P": "SOT89",
#     "BNO-055":""#bno weg
 }

parts = {}

if len(sys.argv) < 3:
    print "usage: " + sys.argv[0] + " input.ssv output.ssv feeder.ssv"
    sys.exit(1)

in_file = open(sys.argv[1], 'r')
out_file = open(sys.argv[2], 'w')

if len(sys.argv) == 4:
    feeder_file = open(sys.argv[3], 'r')
    for part in feeder_file:
        p = part.split()
        if len(p) == 2:
            partid, feeder = p
            parts[partid] = feeder
        if len(p) == 3:
            partid, feeder, rot = p
            parts[partid] = feeder
    feeder_file.close()

for line in in_file:
    l = line.split()
    if len(l) == 7 and l[0][0] != '#':
        name, value, package, x, y, c, side  = l
        name = name.replace("µ", "u").replace("–", "-").encode('ascii', errors='ignore')[:10]
        value = value.replace("µ", "u").replace("–", "-").encode('ascii', errors='ignore')[:10]
        package = package.replace("µ", "u").replace("–", "-").encode('ascii', errors='ignore')[:10]

        if side == "bottom" or side == "b" or side == "B" or side == "Bottom" or side == "BOTTOM" or side == "bot" or side == "Bot" or side == "BOT" or side == "back" or side == "Back" or side == "BACK" or side == "BottomLayer":
            side = "b"
        else:
            side = "t"
        package = package_remap.get(package, package)
        if package != "":
            out_file.write(name + " " + value + " " + package + " " + x + " " + y + " " + c + " " + side + "\n")

            partid = package + ":" + value
            if partid not in parts:
                parts[partid] = ""

if len(sys.argv) == 4:
    feeder_file = open(sys.argv[3], 'w')
    for partid in parts:
        feeder_file.write(partid + " " + parts[partid] + "\n")
    feeder_file.close()

in_file.close()
out_file.close()

sys.exit(1)
