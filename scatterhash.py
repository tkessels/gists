#!/usr/bin/python3
import sys
import hashlib
import os
import numpy as np
import math
import argparse

def even_select(N, M):
    if M > N/2:
        cut = np.zeros(N, dtype=int)
        q, r = divmod(N, N-M)
        indices = [q*i + min(i, r) for i in range(N-M)]
        cut[indices] = True
    else:
        cut = np.ones(N, dtype=int)
        q, r = divmod(N, M)
        indices = [q*i + min(i, r) for i in range(M)]
        cut[indices] = False
    return cut

def get_offsets(blocksize, blockcount,blocks_to_hash):
    selection = even_select(blockcount,blocks_to_hash)
    for i in range(0,blockcount):
        if selection[i] == 0:
            offset = int(blocksize*i)
            yield offset

def get_hash(file,hashalgo,spread):
    h=hashlib.new(hashalgo)
    filesize = os.path.getsize(file.name)
    blocksize = h.block_size*65535
    blockcount = math.ceil(filesize/blocksize)
    blocks_to_hash = math.ceil(blockcount*spread/100)
    if filesize>blocksize:
        for of in get_offsets(blocksize,blockcount,blocks_to_hash):
            infile.seek(of)
            h.update(file.read(blocksize))
    else:
        h.update(file.read(blocksize))
    result="{};{};{};{};{}".format(h.hexdigest(),spread,filesize,hashalgo,file.name)
    return result

parser = argparse.ArgumentParser(description='Sparsly hash large files. Only a given percentage of the file is actualy hashed.')
parser.add_argument('-p',metavar='N', action="store",dest="spread",type=int, nargs='?',default=10,help='percentage of file to hash. 0 < N < 100 (default=10)')
parser.add_argument('-c', action="store",dest="hashalgo",nargs='?',default="md5",help='select an hashalgorithm (default=md5)')
parser.add_argument('file', type=argparse.FileType('rb'), nargs='+')
args = parser.parse_args()

hashalgo = args.hashalgo
spread = args.spread
for infile in args.file:
    hashvalue = get_hash(infile,hashalgo,spread)
    print(hashvalue)
