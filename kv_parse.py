#!/usr/bin/env python3
import re
import json
import sys

with open(sys.argv[1],'rt') as infile:
    data = infile.readlines()

kv_pat = re.compile('(?P<key>[^= ]+)=(?P<value>"[^"]+"|\S+)')

log=[]
for line in data:
    line_dict={}
    line = line.strip()
    matches=kv_pat.findall(line)
    for match in matches:
        line_dict[match[0]] = match[1].strip('"')
    log.append(line_dict) 

print(json.dumps(log))
# with open('log.json','wt') as outfile:
#     json.dump(log,outfile)
    

