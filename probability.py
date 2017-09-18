#!/usr/bin/env python

import sys
import random

from random import shuffle
from collections import Counter


def main():
    employees = []
    for i in range(0, 19):
        employees.append(1)
    for i in range(0, 23):
        employees.append(0)

    count = 0
    for i in xrange(1, 1000001):
        temp = employees[:]
        shuffle(temp)
        if Counter(temp[0:11])[1] == 4:
            count += 1

    print count / 1000000.


if __name__ == '__main__':
    main()
    sys.exit(0)
