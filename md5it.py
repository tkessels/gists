#!/usr/bin/env python3
import os
import hashlib
import magic

extensions={
    "message_rfc822":"eml",
    "application_x-7z-compressed":"7z",
    "text_html":"html"
    }

def get_md5(filename):
    md5=hashlib.md5()
    with open(f,'rb') as fd:
        fb=fd.read(BLOCKSIZE)
        while len(fb)>0:
            md5.update(fb)
            fb=fd.read(BLOCKSIZE)
    return md5.hexdigest()

def get_magic(filename):
    magic_string=magic.from_file(filename, mime=True)
    magic_string=magic_string.replace("/","_")
    if magic_string in extensions:
        magic_string=extensions[magic_string]
    return magic_string

BLOCKSIZE=65536
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    os.rename(f,get_md5(f)+"."+get_magic(f))
