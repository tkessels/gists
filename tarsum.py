#!/usr/bin/python3 -u
import tarfile
import sys
import hashlib
#ask for parameters
#1 = hashtype or md5 by defualt
#2 = filename of tarfile
try:
    if len(sys.argv) == 3:
        hashtype=sys.argv[1]
        tarfilename=sys.argv[2]
    else:
        hashtype="md5"
        tarfilename=sys.argv[1]

    h=hashlib.new(hashtype)
    tf=tarfile.open(tarfilename,'r')
#print usage if anything goes wrong
except Exception as e :
    print(e)
    print("usage: tarsum.py [hashtype] tarfile.tgz")
    print("hashtype can be:")
    print(hashlib.algorithms_available)
    print("md5 is default")
    exit(1)

for file in tf:
    if file.isfile():
        h=hashlib.new(hashtype)
        extracted_file=tf.extractfile(file)
        for chunk in iter(lambda: extracted_file.read(h.block_size),b''):
            h.update(chunk)
        print("{1}  {0}".format(file.name,h.hexdigest()))
