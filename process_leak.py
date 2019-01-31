#!/usr/bin/python3
import sys
import chardet
import os
from os import walk
from chardet.universaldetector import UniversalDetector
import re
import mmh3
from bs4 import UnicodeDammit
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

import string

def get_mask(s):
	mask = ""
	for c in s:
		if c.isdigit():
			mask += "?d"
		elif c.islower():
			mask += "?l"
		elif c.isupper():
			mask += "?u"
		else:
			mask += "?s"
	return mask

def check_special(s):
	for c in s:
		if c in string.punctuation or c.isspace():
			return True
	return False

def check_upper(s):
	return any(i.isupper() for i in s)

def check_lower(s):
	return any(i.islower() for i in s)

def check_digit(s):
    return any(i.isdigit() for i in s)

#list all files in dir
def get_file_enconding(file):
    detector = UniversalDetector()
    with open(file,'rb') as daf:
        i=1000
        for line in daf.readlines():
            i-=1
            detector.feed(line)
            if detector.done or i==0:
                break
        detector.close()

        # daf.seek(0)
        # dammit = UnicodeDammit(daf.read(1000))
        # print(dammit.original_encoding)



        r=detector.result
        return r["encoding"]

patter=re.compile("([^@]+)@([^@]+\.[^@]+)(:|;)(.*)")

def extract_email(line):
    global patter
    match=patter.search(line)
    if match:
        res=(match.group(1),match.group(2),match.group(4))
        return (res)
    else:
        return None

def strip_badbytes(b,encoding):
    return (b.decode(encoding, errors='ignore')).strip()

def get_files(dir):
 f = []
 path=""
 for (dirpath, dirnames, filenames) in walk(dir):
  f.extend(filenames)
  path=dirpath
  break
 for x in f:
  yield os.path.join(path,x)

def get_lines(file):
    encoding=get_file_enconding(file)
    with open(file, 'rb') as f:
        for line in f:
            yield(strip_badbytes(line,encoding))

def get_parsable_lines(file):
    for line in get_lines(file):
        doc=extract_email(line)
        if doc:
            yield doc


def create_doc(file):
    for cred in get_parsable_lines(file):
        doc={}
        doc["user"],doc["domain"],doc["password"] = cred
        doc["file"]=file
        doc["length"] = len(doc["password"])
        doc["passwordMask"] = get_mask(doc["password"])
        doc["containsDigits"] = check_digit(doc["password"])
        doc["containsLowerCase"] = check_lower(doc["password"])
        doc["containsUpperCase"] = check_upper(doc["password"])
        doc["containsSpecial"] = check_special(doc["password"])
        yield doc



def set_data(input_file, index_name = "leaks", doc_type_name = "credential"):
    for doc in create_doc(input_file):
        id=mmh3.hash128(",".join((doc["user"],doc["domain"],doc["password"])),signed=False)
        yield {
            "_index": index_name,
            "_type": doc_type_name,
            "_id": id,
            "_source": doc
        }
        # except Exception as ex:
        #     pass

def load(es, input_file, **kwargs):
	print('[*] Indexing file: %s' % input_file)
	success, _ = bulk(es, set_data(input_file, **kwargs), request_timeout = 60, raise_on_exception = False)

es = Elasticsearch()
for data in get_files(sys.argv[1]):
    load(es,data)
