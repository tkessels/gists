#!/usr/bin/python3
import sys
import pprint
import requests
import os.path


# os.path.exists(file_path)


out_sep=';'

with open(os.path.expanduser('~/.virustotal_api_key')) as api_f:
  api_key=api_f.readline().strip()


hash=sys.argv[1]
url = 'https://www.virustotal.com/vtapi/v2/file/download'
params = {'apikey': api_key, 'hash':hash }
headers = {
  "Accept-Encoding": "gzip, deflate",
  "User-Agent" : "gzip,python_requests,vt_pdns.py"
  }




try:
    response = requests.get(url, params=params, headers=headers)
    if response.ok:
        with open(hash, 'wb') as f:
            f.write(response.content)
    else:
        print("NOTFOUND:{}".format(hash))



except requests.exceptions.ProxyError as e:
    print("Proxy Error")
    print(e)
    exit(1)
