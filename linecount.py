#Count the number of lines in a python program
#exclude comments, blanks.
import string
import re

def Count(workfile):
    #count of lines
    linecount = 0

    #open the workfile read only
    f = open(workfile,'r')

    for line in f:
        line = line.strip()
        if (line == "") or (line[0] == "#"):
            linecount = linecount
        else:
            linecount = linecount+1
            print line
    print linecount
Count("C:\Users\DKenefick\Desktop\Person\person.py")
