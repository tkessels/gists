#!/usr/bin/python3
import chardet
from chardet import UniversalDetector
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l",help="list all encoding changes in file",action='store_true')
parser.add_argument("-d",help="try to decode all Lines",action='store_true')
parser.add_argument('filename')
args = parser.parse_args()


with open(args.filename,'rb') as infile:
    det=UniversalDetector()
    if args.l:
        print("listing encodings of file \"{}\"".format(args.filename))
        encoding=None
        for nl,line in enumerate(infile.readlines()):
            det.reset()
            det.feed(line)
            det.close()
            res=det.result
            if encoding != res["encoding"]:
                encoding=res["encoding"]
                if args.d:
                    print("{}#{}#{}({})".format(nl,line.decode(res["encoding"]),res["encoding"],res["confidence"]))
                else:
                    print("{}#{}#{}({})".format(nl,line,res["encoding"],res["confidence"]))
    else:
        i=1000
        for line in infile.readlines():
            i-=1
            det.feed(line)
            if det.done or i==0:
                break
        det.close()
        res=det.result
        print("{}:{}({})".format(sys.argv[1],res["encoding"],res["confidence"]))
