#!/usr/bin/env python3
import ntplib
import sys
from time import ctime
c = ntplib.NTPClient()
try:
    response = c.request(sys.argv[1])
    print(ctime(response.tx_time))
except:
    print("ERROR")
