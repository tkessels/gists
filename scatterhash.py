#!/usr/bin/python3
import sys
import hashlib
import os
import numpy as np

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

def get_offsets(chunksize, spread):
    selection=even_select(100,spread)
    for i in range(0,100):
        if selection[i]==0:
            offset=int(chunksize*i)
            yield offset

def get_blocks(filename,spread,blocksize):
    filesize=os.path.getsize(filename)
    chunksize=filesize/100
    with open(filename,'rb') as infile:
        for of in get_offsets(chunksize,spread):
            infile.seek(of)
            tohashsize=chunksize
            while tohashsize > 0:
                yield infile.read(blocksize)
                tohashsize-=h.block_size



hashalgo="md5"
filename=sys.argv[2]
spread=int(sys.argv[1]) #percentage of hash
h=hashlib.new(hashalgo)

blocksize=h.block_size*4
for block in get_blocks(filename,spread,blocksize):
    h.update(block)
print(h.hexdigest())
