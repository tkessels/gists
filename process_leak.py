#!/usr/bin/python3
import os
import re
import mmh3
import string
import sys
from os import walk

from chardet.universaldetector import UniversalDetector
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


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


# list all files in dir
def get_file_enconding(file):
    detector = UniversalDetector()
    with open(file, 'rb') as daf:
        i = 1000
        for line in daf.readlines():
            i -= 1
            detector.feed(line)
            if detector.done or i == 0:
                break
        detector.close()

        r = detector.result
        return r["encoding"]


patter = re.compile("([^@]+)@([^@]+\.[^@]+)(\s|:|;)(.*)")


def extract_email(line):
    global patter
    match = patter.search(line)
    if match:
        res = (match.group(1), match.group(2), match.group(4))
        return (res)
    else:
        return None


def strip_badbytes(b, encoding):
    return (b.decode(encoding, errors='ignore')).strip()


def get_files(dir):
    files_in_log={}
    global threshold
    try:
        with open(log_filename,'r') as file_log:
            for line in file_log.readlines():
                try:
                    filedata=line.split(";")
                    files_in_log[filedata[0]]=float(filedata[1])
                except:
                    print("Can't parse Line")
                    pass
    except:
        print("Can't open Logfile")
        pass

    for (dirpath, dirnames, filenames) in walk(dir):
        for file in filenames:
            full_filename=os.path.join(dirpath, file)
            if full_filename in files_in_log and files_in_log[full_filename] > threshold:
                print('[~] Skipping file [Already Parsed]: %s' % full_filename)
                continue

            encoding=get_file_enconding(full_filename)
            if encoding:
                yield encoding, full_filename
            else:
                print('[~] Skipping file [Unknown Encoding]: %s' % full_filename)


def get_lines(file,encoding=None):
    if not encoding:
        encoding = get_file_enconding(file)
    with open(file, 'rb') as f:
        for line in f:
            yield (strip_badbytes(line, encoding))


def get_parsable_lines(file):
    global log_filename
    success = 0  # initialized with 1 to preven div/0
    failure = 0
    for line in get_lines(file):
        doc = extract_email(line)
        if doc:
            success += 1
            yield doc
        else:
            failure += 1
    success_rate = (success / (success + failure))
    print('[+] Done with file: {} ({})'.format(file,success_rate))
    with open(log_filename, 'a+') as file_log:
        file_log.write("{};{}\n".format(file, success_rate))


def create_doc(file):
    for cred in get_parsable_lines(file):
        doc = {
            "user"              :   cred[0],
            "domain"            :   cred[1],
            "password"          :   cred[2],
            "file"              :   file,
            "length"            :   len(cred[2]),
            "passwordMask"      :   get_mask(cred[2]),
            "containsDigits"    :   check_digit(cred[2]),
            "containsLowerCase" :   check_lower(cred[2]),
            "containsUpperCase" :   check_upper(cred[2]),
            "containsSpecial"   :   check_special(cred[2])
           }
        username_split=cred[0].split(";")
        if len(username_split)==2:
            doc["username"]=username_split[0]
            doc["user"]=username_split[1]
        id_hash=hex(mmh3.hash128(",".join((doc["user"], doc["domain"], doc["password"])), 12,signed=False) % 1000000000000000000000)
        yield id_hash, doc


def process_file(input_file):
    global index, doc_type_name
    for id_hash, doc in create_doc(input_file):
        yield {
            "_index": index,
            "_type": doc_type_name,
            "_id": id_hash,
            "_source": doc
        }


index = "leak_col1"
doc_type_name = "credential"
log_filename = "processed_files"
threshold = 0 #threshold for reparsing an already parsed file

def main():
    es = Elasticsearch()
    dir=sys.argv[1]
    for encoding, data in get_files(dir):
        count = es.count(index=index, doc_type=doc_type_name, body={ "query": {"match_all" : { }}})
        pre=count["count"]
        print('[*] Indexing file: %s' % data)
        success, _ = bulk(es, process_file(data), request_timeout=60, raise_on_exception=False)
        count = es.count(index=index, doc_type=doc_type_name, body={ "query": {"match_all" : { }}})
        post=count["count"]
        print('[=] Added {} Documents with {}'.format(post-pre,data))



main()
