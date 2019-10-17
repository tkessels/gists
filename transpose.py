import pprint
import math
# secret="OUHRSTHFSOENOFETURFELIRFTSNEMOEEMELNTARETOKCAETBFIHFTTTNMEELEEOHYBAERORCRSEDNCEUUTHITOYRSTEDSBEIEOTNLRMOEFPOHHAYLAGXYISNIARAUABGBURILFERPEEHTECDINNDITHFFIEHTKESYTDHEREOALGNABSMWEHVEFSOAMETAOCRFTAHEOFSINAMEOTRNGRINTHFFIEHTIEGMELNTSTEOMCOHEOWTEWREAIDANHTRARARTEHEETVFIYREAHVSAONDPROSTRAEUOYCTTTHWISANMUHETENTIISEDHETSUSENTEITNG   OOLEEB L"
# first_col_key="EJALMVWUSTRPOBY" # missing 1 char
# second_row_key="GHPTYPAMTAPQRNDHD" # missing 4 chars one of which is 'D'
# KLINGON_ALPHABET="ABDEHIJLMNOPQRSTUVWY"
# HIERACH_ALPHABET="ABDFGHIJKMNPQRSTUWYZ"
# cleartext="ABDEFGHIJKLMOPQRSTUVWXYZ"
# my_first_col_key="TEST"
# my_row_key="HALLOABBIEGALE"


def rows(text,row_key):
    key_length=len(row_key)
    row_length=math.ceil(len(text)/key_length)
    rows=[text[i:i+key_length] for i in range(0,len(text),key_length)]
    return mosh(rows,row_key)

def cols(text,col_key):
    key_length=len(col_key)
    col_length=math.ceil(len(text)/key_length)
    cols=[ "" for char in col_key ]
    cursor=0
    for c in text:
        cols[cursor%key_length]+=c
        cursor += 1
    return cols


def get_index_key(key):
    return [x[0] for x in sorted(enumerate(key), key=lambda x: x[1])]

def mosh(text,key):
    tmp=sorted(zip(text,key), key=lambda x: x[1])
    return [x[0] for x in tmp]

def cols_encode(text,cols_key):
    return mosh(cols(text,cols_key),cols_key)

#def cols_2_rows

def cols_decode(text,cols_key):
    rows=rows(text)
    reorderd=mosh(rows,cols_key)
    return reorderd
