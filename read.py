#!/usr/bin/python3
import fileinput
import sys
import os

files=set()
for param in sys.argv[1:]:
    if os.path.isfile(str(param)):
#        print(param,"is file")
        files.add(param)
#   else:
#        print(param,"NOT a file")


print("all files:", files)
files.add("-")
for line in fileinput.input(files if len(files)>0 else "-"):
    print(fileinput.filename(),":",line)
