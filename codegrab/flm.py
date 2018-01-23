#!/usr/bin/python
import sys
import re

ignore_case=True

pattern=str(sys.argv[1])
if ignore_case:
    pattern=pattern.lower()
filename=str(sys.argv[2])
shortpattern=""
print("Pattern is '%s'" % pattern)
chars={}

for char in pattern:
    if not char in chars:
        newchar={}
        newchar['char']=char
        newchar['count']=pattern.count(char)
        newchar['idx']=[m.start() for m in re.finditer(re.escape(char),pattern)]
        print(char)
        #print("Char '%s' occurs %d times in pattern %s" % (c,newchar['count'],newchar['idx']))
        chars[char]=newchar
        shortpattern=shortpattern + char
try:
    f=file(filename,'r')
except:
    print("[-] Can't open File %s" % filename)
    exit(1)

print(shortpattern)
longest_match_yet=0
def get_char():
    return f.read(1).lower() if ignore_case else f.read(1)

while longest_match_yet<len(pattern):
    # read_a_char=f.read(1)
    read_a_char=get_char()
    if read_a_char in shortpattern and read_a_char in chars:
        #candidate
        for index in chars[read_a_char]['idx']:
            #lets see if its long enough
            possible_length=len(pattern) - index
            if possible_length>longest_match_yet:
                sub_pattern=pattern[(index+1):]
                match_so_far=read_a_char
                offset=f.tell()
                # print("Possible new Match starting with %s found at %d" % (read_a_char,offset))
                # print("trying to find rest of pattern '%s'" % sub_pattern)
                x=1
                for char_to_compare in sub_pattern:
                    # next_char=f.read(1)
                    next_char=get_char()
                    if not read_a_char:
                        print("No more Chars to consume in File")
                        break
                    # print("comparing %s <> %s  (%d)" % (next_char,char_to_compare,x))
                    if next_char != char_to_compare:
                        break
                    match_so_far=match_so_far+next_char
                    x=x+1
                # print("matching endet with %d matching chars (%d)" % (x,longest_match_yet))
                if x > longest_match_yet:
                    #new longest Match
                    print("found new longest match %s at %d" % (match_so_far,offset))
                    longest_match_yet=x
                f.seek(offset)

    if not read_a_char:
        print("No more Chars to consume in File")
        break
