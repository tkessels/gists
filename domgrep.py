#!/usr/bin/env python3
import re
import sys
from urllib.parse import urlparse

pattern=re.compile(r'\d+\.\d+\.\d+\.\d+')
for line in sys.stdin:
    line=line.strip()
    if not line.lower().startswith('http'):
        line="http://"+line
    try:
        p=urlparse(line)
        if not pattern.search(p.netloc):
            if ":" in p.netloc:
                print(p.netloc.split(":")[0])
            else:
                print(p.netloc)
    except Exception as e:
        print(e)
        pass
