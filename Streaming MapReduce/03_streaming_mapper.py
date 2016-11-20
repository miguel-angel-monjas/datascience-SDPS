#!/usr/bin/env python

import sys
import json

# Read each line from STDIN
for line in sys.stdin:
    record = json.loads(line)

    # key: document identifier
    # value: document contents
    friend_a = record[0]
    friend_b = record[1]
    print ('%s\t%s' %(friend_a, friend_b))
