#!/usr/bin/env python
# coding=utf8
import dbf
import sys
import os
import shutil



if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print 'usage: ' + sys.argv[0] + ' input.dbf'
        sys.exit(1)

    table = dbf.Table(sys.argv[1])
    table.open()
    
    #print table
    
    for field in table.field_names :
        print field + ", ",
    print ""
    
    for record in table:
        for name in record:
            print str(name) + ", ",
        print ""
