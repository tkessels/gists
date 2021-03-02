#!/usr/bin/env python3
import argparse
import logging
import owncloud
import gnupg
import os
import requests
import re
from icecream import ic


def isurl(text):
    pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    matcher = re.compile(pattern)
    return matcher.match(text)

def upload(file,url):
    try:
        oc = owncloud.Client.from_public_link(args.url)
        ic(oc)
        response = oc.drop_file(fn)
        ic(response)
        return response
    except owncloud.owncloud.HTTPResponseError as e:
        logging.error(f'Error while uploading file {fn} <{e}>')

def upload_rq(file,url):
    CLOUDURL=""
    FOLDERTOKEN=""

# FILENAME="$1"

# CLOUDURL=''
# # if we have index.php in the URL, process accordingly
# if [[ $2 == *"index.php"* ]]; then
#         CLOUDURL="${2%/index.php/s/*}"
# else
#         CLOUDURL="${2%/s/*}"
# fi

# FOLDERTOKEN="${2##*/s/}"
# -T "$FILENAME" -u "$FOLDERTOKEN":"$PASSWORD" -H "$HEADER" "$CLOUDURL/$PUBSUFFIX/$BFILENAME"
# if [ ! -f "$FILENAME" ]; then
#         initError "Invalid input file: $FILENAME"
# fi

# if [ -z "$CLOUDURL" ]; then
#         initError "Empty URL! Nowhere to send..."
# fi

# if [ -z "$FOLDERTOKEN" ]; then
#         initError "Empty Folder Token! Nowhere to send..."
# fi


    PUBSUFFIX="public.php/webdav"
    HEADER='X-Requested-With: XMLHttpRequest'
    INSECURE=''

    headers = {
        'X-Requested-With': 'XMLHttpRequest',
    }


    response = requests.put('https://nextcloud.exampyocclientple.com/public.php/webdav/testfile.txt', headers=headers, verify=args.insecure, auth=('AtAxVrKorgC5YJf', ''))



parser = argparse.ArgumentParser()
parser.add_argument("-k","--insecure",action="store_false")
parser.add_argument("-x","--encryption",action="store",default=None,const='*',nargs="?",type=str)
parser.add_argument("url")
parser.add_argument("file",nargs="+")
args=parser.parse_args()

if args.encryption is not None:
    ic(args.encryption)

if not isurl(args.url):
    logging.warning(f"URL '{args.url}' is not valid")

ic(args)
for fn in args.file:
    ic(os.path.isdir(fn))
    ic(os.path.isfile(fn))
    if os.path.isdir(fn):
        logging.warning("Foldersupport not implemented yet")
        continue
    if upload(fn,args.url):
        logging.info(f"{fn} successfully uploaded")
    else:
        logging.warning(f"Error uploading {fn}")






