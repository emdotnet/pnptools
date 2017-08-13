#!/usr/bin/env python
# coding=utf8
import dbf
import sys
import os
import shutil


placeid = 0

x_offset = 0
y_offset = 0

def place(feeder,x,y,r,name): #switch xy,
    global placeid
    global x_offset
    global y_offset
    placeid = placeid + 1
    return (str(feeder), '', '0', '0', '0', '', '', (float(r) + 90) % 360, '', '', str(name), str(float(y) + y_offset), str(float(x) + x_offset), placeid)

def feederindex(f):
    feeder2index = {
        'A':(2,16),
        'B':(24,16),
        'C':(46,16),
        'D':(68,16),
        'E':(262,22),
        'F':(284,22),
        'Q':(222,20),
        'K':(242,20)
    }
    rack = f[0]
    num = int(f[1:])-1
    return feeder2index[rack][0] + num % feeder2index[rack][1]

feeders = {}

#feeder start id:
#A 2   A01-A16 vorne links
#B 24  B01-B16 vorne rechts
#C 46  C01-C16 hinten rechts
#D 68  D01-D16 hinten links
#E 262 E01-E22 rechts
#F 284 F01-F22 links
#Q 222 Q01-Q20 IC-Tray, 4.4.2
#K 242 K01-K20 Bauteil-Tray/Halbautomatischer Zubringer 4.4.3


#components not to place
blacklist = []

#packages to place
packages = ['R0603', 'C0603','C0805', 'R0805', 'SOD123', 'SO8', 'SOT223', 'SOT23', 'SOT23-6', 'CTS406', 'LQFP48']

tplace = []
bplace = []

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print 'usage: ' + sys.argv[0] + ' input.ssv feeder.ssv'
        sys.exit(1)

    #TODO: truncate filename, not path

    
    table = dbf.Table(sys.argv[1])
    table.open()
    print len(table)
    table[len(table) - 1].delete_record()
    sys.exit(1)
