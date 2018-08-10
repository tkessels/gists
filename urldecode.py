#!/usr/bin/python3
from urllib.parse import unquote
import html
import sys
url=' '.join(sys.argv[1:])
print(html.unescape(unquote(url)))
