#!/usr/bin/python3
import sys
import pprint
import requests
import os.path


# os.path.exists(file_path)


out_sep=';'

with open(os.path.expanduser('~/.virustotal_api_key')) as api_f:
  api_key=api_f.readline().strip()

if os.path.exists(os.path.expanduser('~/.ipinfo_api_key')):
    with open(os.path.expanduser('~/.ipinfo_api_key')) as api_g:
        ipinfo_api_key=api_g.readline().strip()
    ipinfo_data=requests.get('http://ipinfo.io/{}'.format(sys.argv[1]), params={'token':ipinfo_api_key})
    print(ipinfo_data.json())

ip=sys.argv[1]
# url='https://www.virustotal.com/vtapi/v2/ip/report'
url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
params = {'apikey': api_key, 'ip':ip }
headers = {
  "Accept-Encoding": "gzip, deflate",
  "User-Agent" : "gzip,python_requests,vt_pdns.py"
  }



try:
    response = requests.get(url, params=params, headers=headers)
    response_data = response.json()
except requests.exceptions.ProxyError as e:
    print("Proxy Error")
    print(e)
    exit(1)

print("=== Short report for : {} ===".format(ip))
print(response_data['verbose_msg'])
if 'detected_urls' in response_data :
    print("{} detected URLs found".format(len(response_data['detected_urls'])))
if 'detected_downloaded_samples' in response_data :
    print("{} detected Downloads found".format(len(response_data['detected_downloaded_samples'])))
if 'resolutions' in response_data:
    print("== Resolutions ==")
    data=sorted(response_data['resolutions'], key=lambda i:i['last_resolved']) if len(response_data['resolutions'])>1 else response_data['resolutions']
    for r in data:
        print("  {} : {}".format(r["last_resolved"],r["hostname"]))


for k in response.json():
    print("=== {} ===".format(k))
    print(response_data[k])
