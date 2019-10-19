#!/usr/bin/env python3
import pprint
import math
import itertools
try:
    import tqdm
    has_tqdm=True
except ImportError:
    print("Install tqdm for Progressbar! (pip3 install tqdm)")
    has_tqdm=False


secret="OUHRSTHFSOENOFETURFELIRFTSNEMOEEMELNTARETOKCAETBFIHFTTTNMEELEEOHYBAERORCRSEDNCEUUTHITOYRSTEDSBEIEOTNLRMOEFPOHHAYLAGXYISNIARAUABGBURILFERPEEHTECDINNDITHFFIEHTKESYTDHEREOALGNABSMWEHVEFSOAMETAOCRFTAHEOFSINAMEOTRNGRINTHFFIEHTIEGMELNTSTEOMCOHEOWTEWREAIDANHTRARARTEHEETVFIYREAHVSAONDPROSTRAEUOYCTTTHWISANMUHETENTIISEDHETSUSENTEITNG   OOLEEB L"
col_key="EJALMVWUSTRPOBY" # (16)missing 1 char
row_key="GHPTYPAMTAPQRNDHD" # (21) missing 4 chars one of which is 'D'
col_alpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
row_alpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def cell_length(text_length,key_length):
    return math.ceil(text_length/key_length)

def padded_length(text_length,key_length):
    return cell_length(text_length,key_length)*key_length

def revert_key(enc_key):
    return [x[0] for x in sorted(enumerate(enc_key), key=lambda x: x[1])]

def mosh(text,enc_key):
    tmp=sorted(zip(text,enc_key), key=lambda x: x[1])
    return [x[0] for x in tmp]

def cols(text,key_length):
    # col_length=cell_length(len(text),key_length)
    columns=[ "" for i in range(0,key_length) ]
    cursor=0
    for c in text:
        columns[cursor%key_length]+=c
        cursor += 1
    return columns

def rows(text,key_length):
    # row_length=math.ceil(len(text)/key_length)
    rows=[text[i:i+key_length] for i in range(0,len(text),key_length)]
    return rows

def cols_to_str(a):
    max_length=max([len(i) for i in a] )
    result=""
    for i in range(0,max_length):
        for x in a:
            try:
                result+=x[i]
            except:
                pass
    return result

def rows_to_str(a):
    return "".join(a)

def pcols(a):
    print("COLUMS:")
    text=cols_to_str(a)
    split_text=rows(text,len(a))
    for x in split_text:
        print(x)

def prows(a,header=None):
    print("ROWS:")
    counter=0
    for x in a:
        if header:
            heading="{}".format(header[counter]).ljust(5)
        else:
            heading="{}".format(counter).ljust(5)
        counter+=1
        print("%s : %s"%(heading,x))

def encode(text,key):
    text=text.ljust(padded_length(len(text),len(key)),'_')
    columnized_text=cols(text,len(key))
    shuffled_colums=mosh(columnized_text,key)
    return rows_to_str(shuffled_colums)

def decode(text,key):
    row_data=rows(text,cell_length(len(text), len(key)))
    reorderd=mosh(row_data,revert_key(key))
    return cols_to_str(reorderd)

def get_col_keys():
    for x in col_alpha:
        yield col_key+x

def get_row_keys():
    for x in row_alpha:
        for y in row_alpha:
            for z in row_alpha:
                # for d in row_alpha:
                #     yield(row_key+d+x+y+z)
                yield(row_key+"D"+x+y+z)
                yield(row_key+x+"D"+y+z)
                yield(row_key+x+y+"D"+z)
                yield(row_key+x+y+z+"D")

def normalize_keys(key_generator):
    k = [revert_key(revert_key(x)) for x in key_generator]
    k.sort()
    return list(k for k,_ in itertools.groupby(k))

def decryptor():
    rowkeys=normalize_keys(get_row_keys())
    colkeys=normalize_keys(get_col_keys())
    if has_tqdm:
        pbar=tqdm.tqdm(total=(len(rowkeys)*len(colkeys)))

    with open("normalized2.txt",'w') as f:
        for col_key in colkeys:
            for row_key in rowkeys:
                text=encode(encode(secret,col_key),row_key)
                f.write("{};{};{}\n".format(row_key,col_key,text))
                if has_tqdm:
                    pbar.update(1)
    if has_tqdm:
        pbar.close()

decryptor()
