#!/usr/bin/env python

import sys
import json

# input comes from STDIN (standard input)
for dataline in sys.stdin:
    record = json.loads(dataline, encoding='latin-1')
    # remove leading and trailing whitespace
    key = record[0]
    line = record[1]
    line = line.strip()
    words = line.split()
    for word in words:
      print '%s\t%s' % (word, key)

