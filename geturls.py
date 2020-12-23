#!/usr/bin/env python3
import sys
from bs4 import BeautifulSoup

if sys.argv[1].startswith("http://") or sys.argv[1].startswith("https://"):
    import requests
    response = requests.get(sys.argv[1])
    data = response.content
else:
    with open(sys.argv[1],'rt',encoding='ISO-8859-1') as f:
        data=f.read()

page=str(BeautifulSoup(data,features="lxml"))

def getURL(page):
    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote


while True:
    url, n = getURL(page)
    page = page[n:]
    if url:
        print(url)
    else:
        break
