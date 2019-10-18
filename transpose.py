import pprint
import math


secret="OUHRSTHFSOENOFETURFELIRFTSNEMOEEMELNTARETOKCAETBFIHFTTTNMEELEEOHYBAERORCRSEDNCEUUTHITOYRSTEDSBEIEOTNLRMOEFPOHHAYLAGXYISNIARAUABGBURILFERPEEHTECDINNDITHFFIEHTKESYTDHEREOALGNABSMWEHVEFSOAMETAOCRFTAHEOFSINAMEOTRNGRINTHFFIEHTIEGMELNTSTEOMCOHEOWTEWREAIDANHTRARARTEHEETVFIYREAHVSAONDPROSTRAEUOYCTTTHWISANMUHETENTIISEDHETSUSENTEITNG   OOLEEB L"
col_key="EJALMVWUSTRPOBY" # (16)missing 1 char
row_key="GHPTYPAMTAPQRNDHD" # (21) missing 4 chars one of which is 'D'
col_alpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
row_alpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"



#As we know from the cold wars in the galaxy with the KLI, the Mondoshiva used the double transposition cipher with first/inner column and second/outer row transformation for encryption to secure the most powerful information. Furthermore, they usually used the longer keys for the rows


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


def decross(text,key_rows,key_cols):
    #revert row transformation
    matrix_cells=len(key_rows)*len(key_cols)
    if len(text) != matrix_cells:
        print("!!TEXT HAD TO BE PADDED!!")
        text=text.ljust(matrix_cells,'_')
    #generate rows with a length of the column-key
    matrix=rows(text,len(key_cols))
    prows(matrix,key_rows)

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

def nub(it):
    seen = set()
    for x in it:
        if x not in seen:
            yield x
            seen.add(x)



def decryptor():
    for col_key in get_col_keys():
        for row_key in get_row_keys():
            text=encode(encode(secret,col_key),row_key)
            yield "{};{};{}".format(row_key,col_key,text)

with open("output3.txt",'w') as f:
    for possiblematch in decryptor():
        f.write(possiblematch+'\n')
