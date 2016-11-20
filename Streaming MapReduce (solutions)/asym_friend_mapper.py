#!/usr/bin/env python

import sys
import json

# input comes from STDIN (standard input)
for dataline in sys.stdin:
    record = json.loads(dataline, encoding='latin-1')
    person = record[0]
    friend = record[1]
    friendship = [str(person), str(friend)]
    sym_friendship = [str(friend), str(person)]
    print '%s\t%s' % (friendship, person)
    print '%s\t%s' % (sym_friendship, person)
