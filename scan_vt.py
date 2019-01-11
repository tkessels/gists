#!/usr/bin/python3
import requests
import sys
import hashlib
from os.path import expanduser


out_sep=';'

with open(expanduser('~/.virustotal_api_key')) as api_f:
  api_key=api_f.readline().strip()

with open(sys.argv[1],'rb') as f:
  hash=hashlib.md5(f.read())

params = {'apikey': api_key, 'resource': hash.hexdigest()}
headers = {
  "Accept-Encoding": "gzip, deflate",
  "User-Agent" : "gzip,python_requests,scan_vt.py"
  }

response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)

try:
  json_response = response.json()
except:
  print(response)
  exit(1)

if json_response["response_code"]:
  print("{}{}{}{}{}/{}{}{}".format(sys.argv[1],out_sep,hash.hexdigest(),out_sep,json_response["positives"],json_response["total"],out_sep,json_response["permalink"]))
else:
  print("{}{}{}{}{}".format(sys.argv[1],out_sep,hash.hexdigest(),out_sep,out_sep))
