#!/usr/bin/python3 -u
import tarfile
import hashlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infile', type=argparse.FileType('rb'))
parser.add_argument('-c','--hashtype', default="md5" , choices=hashlib.algorithms_available )
args = parser.parse_args()

tf=tarfile.open(fileobj=args.infile)

for file in tf:
    if file.isfile():
        h=hashlib.new(args.hashtype)
        extracted_file=tf.extractfile(file)
        for chunk in iter(lambda: extracted_file.read(h.block_size),b''):
            h.update(chunk)
        print("{1}  {0}".format(file.name,h.hexdigest()))
