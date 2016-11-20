#!/usr/bin/env python

import sys
import json

# Read each line from STDIN
for line in sys.stdin:
    record = json.loads(line)

    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
        print ('%s\t%s' %(w, key))