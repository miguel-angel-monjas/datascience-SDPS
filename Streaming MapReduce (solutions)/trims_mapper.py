#!/usr/bin/env python

import sys
import json

# input comes from STDIN (standard input)
for dataline in sys.stdin:
    record = json.loads(dataline, encoding='latin-1')
    # remove leading and trailing whitespace
    id = record[0]
    sequence = record[1]
    sequence = sequence[:10]
    print '%s\t%s' % (sequence, 1)

