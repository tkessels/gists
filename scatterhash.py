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

def get_hash(file,hashalgo,spread=-1,maxsize=-1,blocks_to_hash=-1):
    h=hashlib.new(hashalgo)
    filesize = os.path.getsize(file.name)
    blocksize = h.block_size*65535
    blockcount = math.ceil(filesize/blocksize)
    if blocks_to_hash == -1 :
        blocks_to_hash = math.ceil(blockcount*spread/100)
        if (blocks_to_hash * blocksize) > maxsize:
            blocks_to_hash = math.ceil(maxsize/blocksize)
    if filesize>blocksize:
        for of in get_offsets(blocksize,blockcount,blocks_to_hash):
            file.seek(of)
            h.update(file.read(blocksize))
    else:
        h.update(file.read(blocksize))
    result="{};{};{};{};{}".format(h.hexdigest(),blocks_to_hash,filesize,hashalgo,file.name)
    return result

parser = argparse.ArgumentParser(description='Sparsly hash large files. Only a given percentage of the file is actualy hashed.')

parser.add_argument('-p',metavar='N', action="store",dest="spread",type=int, nargs='?',default=10,help='percentage of file to hash. 0 < N < 100 (default=10)')
parser.add_argument('-s',metavar='N', action="store",dest="size",type=int, nargs='?',default=10,help='maximum amount of data per file in MB')
parser.add_argument('-c', action="store",dest="hashalgo",nargs='?',default="md5",help='select an hashalgorithm (default=md5)')
parser.add_argument('file', type=argparse.FileType('rb'), nargs='+')
parser.add_argument('-v', default=False, dest="validate", action='store_true', help='read output-file of previous run and validate hashes')
parser.add_argument('-1', default=True, dest="mismatches", action='store_false', help='suppress mismatches')
parser.add_argument('-0', default=True, dest="matches", action='store_false', help='suppress matches')
args = parser.parse_args()

if not args.validate:
    hashalgo = args.hashalgo
    spread = args.spread
    maxsize = args.size * 1024 * 1024
    for infile in args.file:
        print(get_hash(infile,hashalgo,spread,maxsize))
else:
    print("validating")
    for line in args.file[0]:
        line=line.decode().strip()
        hash, blocks_hashed, filesize, hashalgo, file = line.split(';')
        blocks_hashed=int(blocks_hashed)
        filesize=int(filesize)
        if os.path.isfile(file):
            if os.path.getsize(file) != filesize:
                result="BAD_SIZE"
            else:
                rehash=get_hash(open(file,'rb'),hashalgo,blocks_to_hash=blocks_hashed)
                if hash == rehash.split(";")[0]:
                    result = "OK"
                else:
                    result = "BAD_HASH"
        else:
            result="FILE_NOT_FOUND"
        if args.mismatches and not result == "OK":
            print("{};{}".format(result,line))
        elif args.matches and result == "OK":
            print("{};{}".format(result,line))
