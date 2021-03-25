#!/usr/bin/env python3
import re
import json
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--preserve", action='store_true', help="preserve original logline in dict")
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
args = parser.parse_args()

data = args.infile.readlines()

kv_pat = re.compile('(?P<key>[^= ]+)=(?P<value>"[^"]+"|\S+)')

log=[]
for line in data:
    line_dict={}
    line = line.strip()
    matches=kv_pat.findall(line)
    for match in matches:
        line_dict[match[0]] = match[1].strip('"')
    if args.preserve:
        line_dict['original_logline'] = line
    log.append(line_dict) 

json.dump(log,args.outfile)