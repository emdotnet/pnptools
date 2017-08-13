#!/usr/bin/env python
# coding=utf8
import dbf
import sys
import os
import shutil


placeid = 0

x_offset = 345
y_offset = 255
x_invert = -1.0#war -1
y_invert = -1.0#war -1

# IPC -> PA908
rotation_remap = {
    "*SOT23": 90.0,
    "*SOT223": 90.0,
    "*SOP8P": 90.0,
    "*C6032": 270.0,
    "*QFP48": 90.0,
    "*QFP100": 90.0,
    "*NPI31W": 180.0,
    "*IND3225": 180.0,
    "*MUSB": 90.0,
    "*SMA": 180.0,
}

def place(feeder,x,y,r,name): #switch xy,
    global placeid
    global x_offset
    global y_offset
    placeid = placeid + 1
    return (str(feeder), '', '0', '0', '0', '', '', (float(r) + 360.0) % 360, '', '', str(name), str(float(x) * float(x_invert) + float(x_offset)), str(float(y) * float(y_invert) + float(y_offset)), placeid)

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
blacklist = ["VR1", "U3"]

#packages to place
#packages = ['R0603', 'C0603','C0805', 'R0805', 'SOD123', 'SO8', 'SOT223', 'SOT23', 'SOT23-6', 'CTS406', 'LQFP48', 'MICROUSB']

tplace = []
bplace = []

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print 'usage: ' + sys.argv[0] + ' input.ssv feeder.ssv'
        sys.exit(1)

    #TODO: truncate filename, not path
    database = os.path.splitext(sys.argv[1])[0][:8]+'.DBF'#name database like brd file, truncate filename to length 8
    dir_name = os.path.dirname(sys.argv[0])
    if dir_name == "":
        dir_name = "."
    shutil.copyfile(dir_name + '/template.dbf',database)

    board = open(sys.argv[1])
    feeder_file = open(sys.argv[2])

    for part in feeder_file:
        p = part.split()
        if len(p) == 2:
            partid, feeder = p
            feeders[partid] = (feeder, 0)
        if len(p) == 3:
            partid, feeder, tape_rot = p
            feeders[partid] = (feeder, tape_rot)
    feeder_file.close()

    table = dbf.Table(database)
    table.open()


    #print "parts:"
    for part in board:
        name, value, package, x, y, c, side = part.split()
        c = (float(c) + rotation_remap.get(package, 0.0)) % 360.0
        partid = package + ':' + value

        if name not in blacklist:
            foo = (partid, package, value, name, x, y, c)
            if side == 'b':#bottom layer
                bplace.append(foo)
            else:#top layer
                tplace.append(foo)

    p = tplace #TODO invert c and x for bplace

    for part in p:
        partid, package, value, name, x, y, c = part
        if partid in feeders: #part has assigned feeder
            feeder = feeders[partid][0]
            tape_rot = feeders[partid][1]

            fd = feederindex(feeder) - 1

            pick_rot = str((float(tape_rot) - rotation_remap.get(package, 0.0)) % 360.0)

            with table[fd]:
                table[fd].component = str(value)
                table[fd].typ = '1'
                table[fd].bbbb = package
                table[fd].dddd = pick_rot
            table.append(place(feeder, x, y, c, name))

        else: #feeder missing
            print "feeder not assigned: " + name + " " + partid

    with table[1]: #1. fid
        table[1].place_x = -27.0 * x_invert + x_offset
        table[1].place_y = -1.5 * y_invert + y_offset
        table[1].no = 1

    with table[106]: #2. fid
        table[106].place_x = -86.75 * x_invert + x_offset
        table[106].place_y = -98.75 * y_invert + y_offset
        table[106].no = 1
        table[106].typ = "1"
        table[106].image = "1"

#x panel spacing 35.255


#    with table[305]:
#        table[305].qfp_hgt = 6.3 #pcb
