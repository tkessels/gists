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
from multiprocessing import Pool,Lock
import multiprocessing
import hashlib
import json

import argparse




lock = Lock()

def log_to_file(text):
    global log_filename
    with lock: # thread blocks at this line until it can obtain lock
        with open(log_filename, 'a+') as file_log:
            file_log.write("{}\n".format(text))

def log_to_console(text):
    with lock: # thread blocks at this line until it can obtain lock
        print(text)


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
                    log_to_console("Can't parse Line")
                    pass
    except:
        log_to_console("Can't open Logfile")
        pass

    for (dirpath, dirnames, filenames) in walk(dir):
        for file in filenames:
            full_filename=os.path.join(dirpath, file)
            if full_filename in files_in_log and files_in_log[full_filename] > threshold:
                log_to_console('[~] Skipping file [Already Parsed]: %s' % full_filename)
                continue
            yield full_filename


def get_lines(file,encoding=None):
    if not encoding:
        encoding = get_file_enconding(file)
    with open(file, 'rb') as f:
        return [strip_badbytes(line, encoding) for line in f]
        # for line in f:
        #     yield (strip_badbytes(line, encoding))


def get_parsable_lines(file,encoding):
    global log_filename
    success = 0  # initialized with 1 to preven div/0
    failure = 0
    for line in get_lines(file,encoding):
        doc = extract_email(line)
        if doc:
            success += 1
            yield doc
        else:
            failure += 1
    success_rate = (success / (success + failure))
    log_to_console('[+] Done with file: {} ({})'.format(file,success_rate))
    log_to_file("{};{}".format(file, success_rate))


def get_hash(text):
    hash_object = hashlib.md5(text.encode())
    return hash_object.hexdigest()
    # return hex(mmh3.hash(text, 12, signed=False)).split("x")[1]

def get_user_pw_hash(text):
    return get_hash(text)
    # return hex(mmh3.hash128(text, 12,signed=False) % 1000000000000000).split("x")[1]

def create_doc(file,encoding):
    for cred in get_parsable_lines(file,encoding):
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
            if len(username_split[0]) > 0 and len(username_split[1]) > 0:
                doc["username"]=username_split[0]
                doc["user"]=username_split[1]
        id_hash=get_user_pw_hash("{}{}{}".format(doc["user"],doc["domain"],doc["password"]))
        id_domain=id_hash[:1]
        yield id_domain, id_hash, doc


def process_file(input_file,encoding):
    global index, doc_type_name
    for id_domain, id_hash, doc in create_doc(input_file,encoding):
        yield {
                "_index": "{}_{}".format(index,id_domain),
                "_type": doc_type_name,
                "_id": id_hash,
                "_source": doc
        }




def index_file(input_file):
    ps=multiprocessing.current_process()
    encoding=get_file_enconding(input_file)
    if encoding:
        es = Elasticsearch(["172.16.1.141"],http_compress=True)
        # count = es.count(index=index, doc_type=doc_type_name, body={ "query": {"match_all" : { }}})
        # pre=count["count"]
        log_to_console('[{}:*] Indexing file: {}'.format(ps.pid,input_file))
        try:
            success, _ = bulk(es, process_file(input_file,encoding), chunk_size=10000, request_timeout=60, raise_on_error=True, raise_on_exception=False)
            # es.bulk()
        except Exception as e:
            log_to_console('[{}:!] Indexing failed for: {}\n[{}:!] REASON: {}'.format(ps.pid,input_file,e.message))
        # count = es.count(index=index, doc_type=doc_type_name, body={ "query": {"match_all" : { }}})
        # post=count["count"]
        # log_to_console('[{}:=] Added {} Documents with {}'.format(ps.pid,post-pre,input_file))
    else:
        log_to_console('[{}:~] Skipping file [Unknown Encoding]: {}'.format(ps.pid,input_file))

def bench_file(input_file):
    ps=multiprocessing.current_process()
    encoding=get_file_enconding(input_file)
    devnull=open(os.devnull,'w')
    if encoding:
        es = Elasticsearch()
        # count = es.count(index=index, doc_type=doc_type_name, body={ "query": {"match_all" : { }}})
        # pre=count["count"]
        log_to_console('[{}:*] Benching file: {}'.format(ps.pid,input_file))
        docs=0
        try:
            # success, _ = bulk(es, process_file(input_file,encoding), chunk_size=1000, request_timeout=60, raise_on_error=False, raise_on_exception=False)
            for doc in process_file(input_file,encoding):
                docs+=1
                devnull.write(json.dumps(doc))


            log_to_console('[{}:*] Benching Done: {} [processed {} docs]'.format(ps.pid,input_file,docs))




        except Exception as e:
            log_to_console('[{}:!] Benching failed for: {}\n[{}:!] REASON: {}'.format(ps.pid,input_file,e.message))
        # count = es.count(index=index, doc_type=doc_type_name, body={ "query": {"match_all" : { }}})
        # post=count["count"]
        # log_to_console('[{}:=] Added {} Documents with {}'.format(ps.pid,post-pre,input_file))
    else:
        log_to_console('[{}:~] Skipping file [Unknown Encoding]: {}'.format(ps.pid,input_file))



index=""
doc_type_name = "credential"
log_filename = "processed_files"
threshold = -1 #threshold for reparsing an already parsed file

def main():
    global index
    parser = argparse.ArgumentParser(description="Put Leakdata into local Elasticsearch")
    parser.add_argument("-p",help="how many workers (default:4)",default=4,type=int,nargs='?')
    parser.add_argument("-i",help="index suffix",default="leak_data")
    parser.add_argument("-b",help="dont write to es just benchmark",action='store_true')
    parser.add_argument('folder')
    args = parser.parse_args()
    index=args.i
    workers=args.p
    dir=args.folder
    p=Pool(workers)
    if args.b:
        p.map(bench_file,get_files(dir))
    else:
        p.map(index_file,get_files(dir))



if __name__ == '__main__':
    main()
