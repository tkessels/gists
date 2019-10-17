import pprint
import math

secret="OUHRSTHFSOENOFETURFELIRFTSNEMOEEMELNTARETOKCAETBFIHFTTTNMEELEEOHYBAERORCRSEDNCEUUTHITOYRSTEDSBEIEOTNLRMOEFPOHHAYLAGXYISNIARAUABGBURILFERPEEHTECDINNDITHFFIEHTKESYTDHEREOALGNABSMWEHVEFSOAMETAOCRFTAHEOFSINAMEOTRNGRINTHFFIEHTIEGMELNTSTEOMCOHEOWTEWREAIDANHTRARARTEHEETVFIYREAHVSAONDPROSTRAEUOYCTTTHWISANMUHETENTIISEDHETSUSENTEITNG   OOLEEB L"
col_key="EJALMVWUSTRPOBY_" # (16)missing 1 char
row_key="GHPTYPAMTAPQRNDHD____" # (21) missing 4 chars one of which is 'D'
# KLINGON_ALPHABET="ABDEHIJLMNOPQRSTUVWY"
# HIERACH_ALPHABET="ABDFGHIJKMNPQRSTUWYZ"
# cleartext="ABDEFGHIJKLMOPQRSTUVWXYZ"
# my_first_col_key="TEST"
# my_row_key="HALLOABBIEGALE"



#As we know from the cold wars in the galaxy with the KLI, the Mondoshiva used the double transposition cipher with first/inner column and second/outer row transformation for encryption to secure the most powerful information. Furthermore, they usually used the longer keys for the rows


def cell_length(text_length,key_length):
    return math.ceil(text_length/key_length)

def padded_length(text_length,key_length):
    return cell_length(text_length,key_length)*key_length

def revert_key(key):
    return [x[0] for x in sorted(enumerate(key), key=lambda x: x[1])]

def mosh(text,key):
    tmp=sorted(zip(text,key), key=lambda x: x[1])
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
    text=text.ljust(math.ceil(len(text)/len(key))*len(key),'_')
    print("encoding <%s>"%text)
    columnized_text=cols(text,len(key))
    pcols(columnized_text)
    shuffled_colums=mosh(columnized_text,key)
    pcols(shuffled_colums)
    return rows_to_str(shuffled_colums)

def decode(text,key):
    print("decoding <%s>"%text)
    row_data=rows(text,cell_length(len(text), len(key)))
    prows(row_data)
    reorderd=mosh(row_data,revert_key(key))
    prows(reorderd)
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

decross(secret,row_key,col_key)