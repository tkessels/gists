#!/usr/bin/python3
import sys
import pprint
import requests
from os.path import expanduser


out_sep=';'

with open(expanduser('~/.virustotal_api_key')) as api_f:
  api_key=api_f.readline().strip()

domain=sys.argv[1]
url='https://www.virustotal.com/vtapi/v2/domain/report'
params = {'apikey': api_key, 'domain':domain }
headers = {
  "Accept-Encoding": "gzip, deflate",
  "User-Agent" : "gzip,python_requests,vt_pdns.py"
  }


cat_fields=["Alexa category",
"categories",
"BitDefender category",
"TrendMicro category",
"Forcepoint ThreatSeeker category"]
#
# "whois",
# "WOT domain info",
# "Webutation domain info",
# "BitDefender domain info",
# "Alexa domain info",
# BitDefender category
# WOT domain info
# Webutation domain info
# Alexa category
# Opera domain info
# TrendMicro category
# categories
# domain_siblings
# BitDefender domain info
# whois
# Alexa domain info
# Forcepoint ThreatSeeker category
# Alexa rank
#
# detected_downloaded_samples
# detected_urls
#
# detected_communicating_samples
# detected_referrer_samples
# undetected_downloaded_samples
# undetected_referrer_samples
# undetected_urls
# undetected_communicating_samples
# resolutions
# response_code
# verbose_msg
# pcaps
#
try:
    response = requests.get(url, params=params, headers=headers)
    response_data = response.json()
except requests.exceptions.ProxyError as e:
    print("Proxy Error")
    print(e)
    exit(1)

# resolutions=[r for r in response.json()['resolutions']]


def get(key,dict):
    split_key=key.split(sep=" ")
    if len(split_key)>1:
        prefix="{}: ".format(split_key[0])
    else:
        prefix="VT: "
    if key in dict:
        print("{}{}".format(prefix,dict[key]))

# # detected_downloaded_samples=[d for d in response.json()['detected_downloaded_samples']]
# # detected_url=[d for d in response.json()['detected_url']]

print("=== Short report for : {} ===".format(domain))
print(response_data['verbose_msg'])
if 'detected_urls' in response_data :
    print("{} detected URLs found".format(len(response_data['detected_urls'])))
if 'detected_downloaded_samples' in response_data :
    print("{} detected Downloads found".format(len(response_data['detected_downloaded_samples'])))
if any([True for x in cat_fields if x in response_data]):
    print("== Categories ==")
    for cat in cat_fields:
        get(cat,response_data)
if 'resolutions' in response_data:
    print("== Resolutions ==")
    data=sorted(response_data['resolutions'], key=lambda i:i['last_resolved']) if len(response_data['resolutions'])>1 else response_data['resolutions']
    for r in data:
        print("  {} : {}".format(r["last_resolved"],r["ip_address"]))

# print('--------------------------infos')
# for k in response.json():
#     print(k)
