#!/usr/bin/env python3
import os
import hashlib
BLOCKSIZE=65536
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    md5=hashlib.md5()
    with open(f,'rb') as fd:
        fb=fd.read(BLOCKSIZE)
        while len(fb)>0:
            md5.update(fb)
            fb=fd.read(BLOCKSIZE)
    os.rename(f,md5.hexdigest())
